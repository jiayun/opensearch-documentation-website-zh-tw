---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用延遲互動模型依欄位重新排序"
parent: Reranking search results
grand_parent: Optimizing search quality
has_children: false
nav_order: 40
---

# 使用延遲互動模型依欄位重新排序
**3.3 版新增**
{: .label .label-purple }

在本教學中，您將學習如何使用託管於 Amazon SageMaker 的延遲互動模型 (例如 ColBERT 或 ColPali)，重新排序搜尋結果並提升多模態內容的搜尋相關性。

延遲互動模型會為每份文件與查詢產生多個向量，並在搜尋期間執行細緻的詞元層級比對，藉此兼顧速度與準確度。這種方法對多模態內容 (例如含文字的圖片、技術圖表及複雜文件) 特別有效，因為詳細的語意分析可提升其相關性。延遲互動模型結合快速的 k-NN 擷取與詞元層級重新排序，能有效率地處理複雜查詢，並擷取文字與其他內容類型之間細微的語意關聯。

若要實作延遲互動重新排序，您需要同時設定資料匯入管線與搜尋管線：
- **資料匯入管線**：在文件編製索引期間，使用 [`ml_inference` 匯入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/ml-inference/) 產生多向量與單一 k-NN 向量。
- **搜尋管線**：在搜尋時處理查詢，使用 [`ml_inference` 搜尋請求處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/ml-inference-search-request/) 與 [`lateInteractionScore`]({{site.url}}{{site.baseurl}}/query-dsl/specialized/script-score/#late-interaction-score) 函式，為 k-NN 擷取及延遲互動重新排序產生查詢向量。

## 先決條件：在 Amazon SageMaker 上部署 ColPali 模型

以下是在 Amazon SageMaker 上部署 [`vidore/colpali-v1.3-hf`](https://huggingface.co/vidore/colpali-v1.3-hf) 模型的範例部署指令碼。您可以使用任何延遲互動模型及偏好的部署方式。由於 ColPali 需要自訂推論邏輯來處理文字查詢與 Base64 編碼的圖片，因此本範例使用自訂推論指令碼，而非標準的 Hugging Face 任務介面。請在 SageMaker 筆記本中執行下列步驟。

### 步驟 1：建立自訂推論指令碼

下列指令碼會同時處理查詢 (文字清單) 與圖片 (Base64 清單) 輸入，並傳回多向量詞元層級嵌入。它會在容器啟動時從 Hugging Face Hub 下載模型權重：

```python
import os
os.makedirs('colpali_code', exist_ok=True)

inference_code = r'''
# Requires Python >= 3.12 and transformers >= 4.51.3
import torch
import base64
from io import BytesIO
from PIL import Image
from transformers import ColPaliForRetrieval, ColPaliProcessor

def model_fn(model_dir):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = ColPaliForRetrieval.from_pretrained(
        "vidore/colpali-v1.3-hf", torch_dtype=torch.float32,
    ).to(device).eval()
    processor = ColPaliProcessor.from_pretrained("vidore/colpali-v1.3-hf")
    return {"model": model, "processor": processor, "device": device}

def predict_fn(data, model_dict):
    model = model_dict["model"]
    processor = model_dict["processor"]
    device = model_dict["device"]
    queries = data.get("queries", [])
    images_b64 = data.get("images", [])
    result = {}
    if queries:
        inputs = processor(text=queries, return_tensors="pt", padding=True)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = model(**inputs)
        result["query_embeddings"] = outputs.embeddings.cpu().tolist()
    if images_b64:
        pil_images = []
        for b64 in images_b64:
            pil_images.append(Image.open(BytesIO(base64.b64decode(b64))).convert("RGB"))
        inputs = processor(images=pil_images, return_tensors="pt", padding=True)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = model(**inputs)
        result["image_embeddings"] = outputs.embeddings.cpu().tolist()
    return result

def input_fn(request_body, request_content_type):
    import json
    if request_content_type == "application/json":
        return json.loads(request_body)
    raise ValueError(f"Unsupported content type: {request_content_type}")

def output_fn(prediction, accept):
    import json
    return json.dumps(prediction)
'''.strip()

with open('colpali_code/inference.py', 'w') as f:
    f.write(inference_code)
print('Created colpali_code/inference.py')
```
{% include copy.html %}

### 步驟 2：封裝指令碼並上傳至 Amazon S3

使用下列程式碼封裝 `inference.py` 指令碼並上傳至 Amazon S3：

```python
import subprocess
import sagemaker
import boto3

subprocess.run(['tar', '-czf', 'model.tar.gz', '-C', 'colpali_code', 'inference.py'], check=True)
print('Created model.tar.gz')

session = sagemaker.Session()
region = session.boto_region_name
account_id = boto3.client('sts').get_caller_identity()['Account']
bucket = f'sagemaker-{region}-{account_id}'
s3_key = 'colpali-custom/model.tar.gz'

s3 = boto3.client('s3', region_name=region)
s3.upload_file('model.tar.gz', bucket, s3_key)
model_data_url = f's3://{bucket}/{s3_key}'
print(f'Uploaded to {model_data_url}')
```
{% include copy.html %}

### 步驟 3：部署 SageMaker 端點

下列程式碼會將模型部署至 GPU 執行個體 (此程序大約需要 5--10 分鐘)：

```python
import time
from datetime import datetime

role = sagemaker.get_execution_role()

# HuggingFace PyTorch Inference DLC - GPU, Python 3.12, Transformers 4.51.3
# Replace 123456789012 with your AWS Deep Learning Containers account ID for your region.
# See https://github.com/aws/deep-learning-containers/blob/master/available_images.md
dlc_account_id = '123456789012'
image_uri = (
    f'{dlc_account_id}.dkr.ecr.{region}.amazonaws.com/'
    'huggingface-pytorch-inference:2.6.0-transformers4.51.3-gpu-py312-cu124-ubuntu22.04'
)

sm = boto3.client('sagemaker', region_name=region)
ts = datetime.now().strftime('%Y%m%d%H%M%S')

model_name = f'colpali-custom-{ts}'
epc_name = f'colpali-custom-epc-{ts}'
ep_name = f'colpali-custom-ep-{ts}'

sm.create_model(
    ModelName=model_name,
    PrimaryContainer={
        'Image': image_uri,
        'ModelDataUrl': model_data_url,
        'Environment': {
            'SAGEMAKER_PROGRAM': 'inference.py',
            'SAGEMAKER_SUBMIT_DIRECTORY': model_data_url,
        },
    },
    ExecutionRoleArn=role,
)
print(f'Model created: {model_name}')

sm.create_endpoint_config(
    EndpointConfigName=epc_name,
    ProductionVariants=[{
        'VariantName': 'AllTraffic',
        'ModelName': model_name,
        'InstanceType': 'ml.g4dn.xlarge',
        'InitialInstanceCount': 1,
    }],
)
print(f'Endpoint config created: {epc_name}')

sm.create_endpoint(EndpointName=ep_name, EndpointConfigName=epc_name)
print(f'Creating endpoint: {ep_name} (takes 5-10 min)...')

while True:
    resp = sm.describe_endpoint(EndpointName=ep_name)
    status = resp['EndpointStatus']
    print(f'  Status: {status}')
    if status == 'InService':
        break
    if status == 'Failed':
        print(f'  FAILED: {resp.get("FailureReason")}')
        break
    time.sleep(30)

print(f'\nEndpoint ready: {ep_name}')
```
{% include copy.html %}

部署後，請在 Amazon SageMaker 主控台的 **Inference > Endpoints** 中找到您的端點名稱。您將在連接器組態中使用此端點 URL。

## 執行使用延遲互動重新排序的搜尋

若要實作延遲互動重新排序，請依照下列步驟操作：

1. [註冊模型](#step-1-register-the-model)。
1. [建立具有適當對應的索引](#step-2-create-an-index)。
1. [建立資料匯入管線](#step-3-create-an-ingest-pipeline)。
1. [匯入文件](#step-4-ingest-documents)。
1. [建立搜尋管線](#step-5-create-a-search-pipeline)。
1. [使用延遲互動重新排序進行搜尋](#step-6-search-using-late-interaction-reranking)。

## 步驟 1：註冊模型

建立連接器並將 ColPali 模型註冊至 OpenSearch：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
    "name": "ColPali model",
    "function_name": "remote",
    "description": "ColPali model for multimodal search",
    "connector": {
        "name": "Amazon SageMaker connector",
        "description": "Connector for ColPali in SageMaker",
        "version": 1,
        "protocol": "aws_sigv4",
        "parameters": {
            "region": "us-east-1",
            "service_name": "sagemaker"
        },
        "credential": {
            "access_key": "<YOUR_ACCESS_KEY>",
            "secret_key": "<YOUR_SECRET_KEY>",
            "session_token": "<YOUR_SESSION_TOKEN>"
        },
        "actions": [
            {
                "action_type": "predict",
                "method": "POST",
                "url": "<YOUR_SAGEMAKER_ENDPOINT>",
                "headers": {
                    "content-type": "application/json"
                },
                "request_body": "{ \"queries\": ${parameters.queries:-[]}, \"images\": ${parameters.images:-[]} }"
            }
        ]
    }
}
```
{% include copy-curl.html %}

請記下回應中的 `model_id`；您將在後續步驟中使用它。

## 步驟 2：建立索引

建立索引，並使用針對儲存多向量及單一 k-NN 向量最佳化的對應。`colbert_vectors` 欄位儲存為 `object`，並搭配 `enabled: false` 以獲得最佳效能。`knn_vector` 欄位設定為使用 `hnsw` 演算法，其維度數與模型的維度數相符。`image` 欄位將 Base64 編碼的影像資料儲存為 `keyword`：


```json
PUT /multimodal_docs
{
  "settings": {
    "index.knn": true,
    "index.knn.algo_param.ef_search": 100
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text"
      },
      "description": {
        "type": "text"
      },
      "image": {
        "type": "keyword"
      },
      "colbert_vectors": {
        "type": "object",
        "enabled": false
      },
      "knn_vector": { 
        "type": "knn_vector", 
        "dimension": 128,
        "method": {
          "name": "hnsw",
          "engine": "lucene"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 步驟 3：建立資料匯入管線

建立資料匯入管線，同時產生用於延遲互動的多向量及用於 k-NN 搜尋的單一向量：

```json
PUT /_ingest/pipeline/colpali_pipeline
{
  "processors": [
    {
      "ml_inference": {
        "tag": "ml_inference",
        "description": "Generate multi-vectors and mean pooling vector for multimodal content",
        "model_id": "<YOUR_MODEL_ID>",
        "input_map": [
          {
            "images": "$..image"
          }
        ],
        "output_map": [
          {
            "colbert_vectors": "image_embeddings[0]",
            "knn_vector": "image_embeddings[0].meanPooling()"
          }
        ],
        "ignore_missing": false,
        "ignore_failure": false
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 步驟 4：匯入文件

匯入包含 Base64 編碼影像及描述性內容的範例文件：

```json
PUT /multimodal_docs/_doc/1?pipeline=colpali_pipeline
{
  "title": "Data Visualization Chart",
  "description": "A comprehensive bar chart showing quarterly sales performance with multiple data series and trend analysis",
  "image": "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"
}

```
{% include copy-curl.html %}

```json
PUT /multimodal_docs/_doc/2?pipeline=colpali_pipeline
{
  "title": "Technical Architecture Diagram",
  "description": "System architecture diagram showing microservices, databases, and API connections with detailed component relationships",
  "image": "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"
}
```
{% include copy-curl.html %}

```json
PUT /multimodal_docs/_doc/3?pipeline=colpali_pipeline
{
  "title": "Financial Report Summary",
  "description": "Quarterly financial report with revenue charts, expense breakdowns, and profit margin analysis across different business units",
  "image": "iVBORw0KGgoAAAANSUhEUgAAANAAAAAZCAYAAABAQ6AIAAAAAXNSR0IArs4c6QAAAGJlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAABJKGAAcAAAASAAAAUKABAAMAAAABAAEAAKACAAQAAAABAAAA0KADAAQAAAABAAAAGQAAAABBU0NJSQAAAFNjcmVlbnNob3Q2LTWaAAAB1WlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNi4wLjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczpleGlmPSJodHRwOi8vbnMuYWRvYmUuY29tL2V4aWYvMS4wLyI+CiAgICAgICAgIDxleGlmOlBpeGVsWURpbWVuc2lvbj4yNTwvZXhpZjpQaXhlbFlEaW1lbnNpb24+CiAgICAgICAgIDxleGlmOlBpeGVsWERpbWVuc2lvbj4yMDg8L2V4aWY6UGl4ZWxYRGltZW5zaW9uPgogICAgICAgICA8ZXhpZjpVc2VyQ29tbWVudD5TY3JlZW5zaG90PC9leGlmOlVzZXJDb21tZW50PgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4K9xJAjQAADF9JREFUeAHtWwlYVdUW/kEGAVERxXnEOZxQe5mKQzkEipSWOJQ+U1PLtHzVs7TnVJqmllIOmRo4JOaY5ZiaOX2IWjiBYyo44KwoMqhv/Vv25RJwuV0wh+8sP+45Z09nnbXX8K91jnan487dg0GGBAwJ2CQBe5tmGZMMCRgSUBIwDMhQBEMCuZCAYUC5EJ4x1ZCAYUCGDhgSyIUEDAPKhfCMqYYEDAMydMCQQC4kYBhQLoRnTDUk4GCrCG6nJuH2nSQUdi5o6xL/yDxb+LyHezibcMHEn5ujCwo5u5uujRNDAloCDhduXUYx1yLq+s9rsYi5fEL3mY71iz+FomljdGP3H99FxNk/EN1nA1wd8+vmR+5oC5/Jd1LwTOhLpmcJrPI8QlqNMF1be7Lx5Hak3L2jhrs7uaJS4XIo4VbM2un/6LikO8m4lHgVpQp42Xzfk9fiEHluHxJSbsGnaBX4lvCBnfx70mjUtqk4df0MZr0wFg5JEkU0bTy5AyO2fokGJWvpJnX87zP9MhkQlaqaZyW4ODpnGPuoXdjCp3M+J5wasFU9ykdbJuJa0g2bHuutdSPg5eaJ0u4lsPfcAaVY7zTsBf49arTrbBSGybNu7rrQJtbWnfgNvVcPFSdRVpyEF4ZvmYTnKzRWSmZv92RlCseunETUhRglJ4eCThmhSbmCpbD0xWk5CvE1nxdzHPMoDHjYfL7doCdeqtpGQOE9fPtHOOi9/l270yMHfa/b6CT0Hk/dHYqgKq0wpdX/VNPZhHjQKJ804+HDebgUQpH8hdRzOhR0LqBOrPmZu28JFh5caRrq5VYUYe0mmq5T76YiYPHr+Lzlh5i2dz42n9yJp0vVxZu+3dGwZG017owIdnZUODZJ35Erf+Ll6v541ScIdb1qqv4/4g/hy8i5GFCvOyZEzMS++Bgwigys/5ry5PpmSw+vRfihn7E9brfyep1rtEOfOsFwsM+HnPjkGr/HH8TcqCXYcWYvCNleET561uqIkrmAMJq3rI6EMi3KPaMM6MTVWNQrfv9595w/gCmR34Fwj/cmD33rdkE+8dpanv3qdUPYgWWIPLsPPsWqYlyz91Hbq7q6zd17dxGyOwxLD69B/M1LaFbuX/iw0QCULVjSxMYC2TNGUb+yDZVs1xzfou61pdv32H1uPz6P+AZxN85L3hePNot6mOZ93WY0vAV2WkNXbl9DrWLVTEP5LNw3Tf6Le2FEk0F4umQd1XT+5kW8tmoI5gZMULy8v2kc3J0KYNWxjfBy9USv2i8rWTUUNPR161EIj/4Z+y8cxj7x/LE3zuETvyGYGDELzg5Oqr9CoTK4mZKo9PPn45uVrCiLYNGLAO8Wmg1ExUcjZE8oxjX/AON3zsBaiZxJks9/32GK6I4D3vllNOa3n5wBcVEfb8naQxv1V+sQhl9xv6bOM8XWFDGCE5IL6T/iYk2tJCTzxvxrXbGpeiDdxyO97KFLx9B5+UA0LdMQoWnGRa+raUfcHjCxH9/iA2zqMh+ES4M3jNbdwuhtbPhzGz7Y/BneEEX6qs0obI2NFAVabhpD4+Qcf+/mao1RTd9RgmFRg5QTnxyzLGadgqBz/McrJ7Bd+PpqTxi7HghdlFzzu/1LUcDRVRStqrrH3vMHEbTkDdTw9MaG4DB83HggpooxLTq0SvVreVJR3vJ9FQsDv4Srgwve2zTWxONIke2cfT+gd53OmOU/TsHEwCV9wftporIuP7wO3X8cgvolamFlp5mY1PIjJXvee/izA9FBlN3TxcO0v9zjMgI9raUB4iTnyR4FrxiknMEdMWxzovInJN80NSWm3la6Qn0jnbp+VpzAWsUXIVKIRLSJLYeCxk64dCnxilq/b91gZdT91g7DsMZv4XpSAlYf/1WtcSbhvDjUPeJse4DOoXWFJui/djjO3UwvCCWk3MTW05F4edmb6vmniZOY5T8W3h7lUaOot1pn3sEV6sgf8jlj7wI0LlPf1EbnoB1tpiocvVBAeDpGf6laG4wRaycRy/OPdFSiR3Y06blhaFvJT3X3rdtZCZUeykPCXsdqbdUfk9bjV08rj0rBR4vhVZfN1BQeNFVtKK85Z40IibkYPS6VjN5MwzM+vF/Zp/VUq/gc2XSwGn8jOUEi4UmV8C4+9BNGijHS++cVDft1IkZvC1EKQAWdIEpBT0f6IWa1Mp7+EmFI9GxBVVtj5ZFf0LVmoGrjD53Ns6Xvb6C7kxva/dAbjOTFXD0wJ2oxhosidX8qSI2nDOvODsCW2F0KOupF6NjmtZ+UQU7s457wb78oaSFBIzoy6nnWHslvtSIVxQnNQ8+f3leo4NNm7wnfvtYuIc/QQSkq97NLzfZoWf5Z5XBY3CL5SjGrfeXncPDiUVXsYERn2wnRI1IVjwqY7f8ZaLyxYpCl3Yur+etPbBWUk55ysMjRrnLLLHPRQQK5/7NxrHLeLg75sfrYryjiUlj4aqDuwR/qY3LlFHWdyYCYA23tHm4abMuJOSwsVaC4WoKeghvF6gUj0vbY3QrWVZCkk2Qe6XjNcK6JnjA+zaNyPgXQQDxpbmib3H/czumy7iW1CXZ2dmrdFIFz+RzyrjDS37ebRMQm6LJyMF4U4zCHE5GSI1Cxfb5tm+FRCNMyUnoli8pFIpQpL3tFalQqXUmJzTmfHp+5l6ZGpetlMh7dl1dHRjcqMNHLJ9u/Esf5Nnb1WI7iAvWtIZ0v0YHpc2ezvbC3v+/Y8slR9+s2rk/0Qti/6OAq1JQqYFUxaHdxChclev2VmBJkRa0r+onBTMPSmLXoJgYdKqiBsNrcqRJFwPH+7EwGlNWiedk2ZnsIHMUDR/RcrrxDqpR56UWtJXoV0lGJGjoPsHauHsecp49UjJjg9xFIQOGwJL/q6EY9xHRkX7JES1uJEZtRYYzfuwpOdK4RIJ66klrOR3IGNylvW1O00fffLWViUmXJTUqlySLqQrQyGrbTudB4dERimzXEXII5FCO8Vk5r5ukxhDr02KSKko+MlkjOylzM5eMmAzJXZO5BXlN49E9gtFnfJQyl0xw3IWXWlO6UzPuZQzMKMe9hGZ456uyA8eZDMpznHVbJsGz2F4flPRNfSjrZO4LYfNS2KdkPzqLHUeYxMWTJdcvpCBAK8v0Dy83mWDeLqaamq0nXlaJ5SmgmMQpMipht6jc/YaQjZo4TfE0czrm2EPM1JtAf/zZZ5Ypcg3CEhQHmdJQFiwabTu0EcwBzWhKzRuU0jDpfRM5R8KiiRG4qLCPazN8XqjwxTpLrMQIXSSwY/B2qLPCHxrf8yHrFh5aRNWsQftefE6iqjNwLQq7pkjeQ6njVUEc+/1LJO4kgDlw8jIHrR6j2vPw5fvWUymvcHd3Us4TuX6aKTH/3Hh2kmsiCxOANo0CHpytuWa2TyYBogdaSU760OJY2Qb80s+TBWCFiVajyjBZosaCr8k5MyARBKbJPO9HXmhfzexFbBwtG7rdmGKrMaImm8zurKJHfLNzreTyaz+U1qzxvSlI+ZOOnqDjNT0WjF7ybsUv4SGNEXQHNBWfXl0pQo9COqDenPVYc2ZDWY91By4THkU0HYUfcXoWrObu5VIlmtP0E8w+sQMPvglBpenOMlPdw5wVWmhPzR9+5garCmXInFQukmKBlPOm5j1C7WHV0FYjYKKwTdkpVcUXHmVIASK/Cma+V3TlzidfrvKKKM+Sj9rf+CmZnN968ne8DmVOymMG98JsfjF+kqhgeFGL6goNVtSu3r6LJvFdUMWOo6AFJy0edp8neHJbpMRwnwI2XpqM+17LoIVCLDpWQuOY3rQXmRisH89c9VYtY+KG+vN2gh3KshHGWyO5h/JduwjZ6c75kNBegJUaz6mOVip6bkYSR6e8SMXNiaqKpWGFp/mVRYsK5B/VJT1brp9xNgff0FljUYapK7i19OkXFSUi+pWRh6Tly6iO0upB4GZ75CyM7h2RpDZbLuS/ZfeLFfWcx5UER782vazzyF7RJJzRfk3fNlmriDvzY6RvdlOXxH8+ByAWjnLWJZZZcpzXS+HLzaQw/QbL2MyRLYdwSj9b2WVqfSkFltqTQfB3g7OJk7e2yHUfvq/OHbAdZ6MjJwTxI4yFb1AkiDFuJ7wcJq2lACwK/yHGZh2JAOXJlDFASIGjhpzE6OTfE8mAlwPdU+vOr6W3GoIlZ6Tq7Oz8UCJcdM0a7IYHHTQKZigiP2wMY/BoSeJgSMAzoYUrfuPdjL4H/AzhAzGbMOihRAAAAAElFTkSuQmCC"
}
```
{% include copy-curl.html %}

## 步驟 5：建立搜尋管線

建立搜尋管線，以產生查詢向量並執行 k-NN 擷取與延遲互動重新排序：

```json
PUT /_search/pipeline/colpali_search_pipeline
{
  "description": "Generate query vectors for KNN search and late interaction reranking",
  "request_processors": [
    {
      "ml_inference": {
        "model_id": "<YOUR_MODEL_ID>",
        "query_template": "{\n    \"query\": {\n        \"knn\": {\n            \"knn_vector\": {\n                \"vector\": ${query_knn_vector},\n                \"k\": 100\n            }\n        }\n    },\n    \"rescore\": {\n        \"query\": {\n            \"rescore_query\": {\n                \"script_score\": {\n                    \"query\": {\n                        \"match_all\": {}\n                    }, \n                    \"script\": {\n                        \"source\": \"lateInteractionScore(params.query_vector, 'colbert_vectors', params._source)\",\n                        \"params\": {\n                            \"query_vector\": ${query_colbert_vectors}\n                        }\n                    }\n                }\n            }\n        }\n    },\n    \"size\": 10,\n  \"_source\": {\n    \"excludes\": [\"knn_vector\"]\n  }\n}",
        "input_map": [
          {
            "queries": "$..query.term.search_text.value"
          }
        ],
        "output_map": [
          {
            "query_colbert_vectors": "query_embeddings[0]",
            "query_knn_vector": "query_embeddings[0].meanPooling()"
          }
        ]
      }
    }
  ]
}
```
{% include copy-curl.html %}

以下是前述搜尋管線中的 `query_template`，為了清楚呈現而格式化。此範本定義了原始搜尋查詢的重寫方式：

```json
{
  "query": {
    "knn": {
      "knn_vector": {
        "vector": ${query_knn_vector},
        "k": 100
      }
    }
  },
  "rescore": {
    "query": {
      "rescore_query": {
        "script_score": {
          "query": {
            "match_all": {}
          },
          "script": {
            "source": "lateInteractionScore(params.query_vector, 'colbert_vectors', params._source)",
            "params": {
              "query_vector": ${query_colbert_vectors}
            }
          }
        }
      }
    }
  },
  "size": 10,
  "_source": {
    "excludes": ["knn_vector"]
  }
}
```

請注意查詢範本的下列元件：

- 範本變數：
   - `${query_knn_vector}`：用於快速 k-NN 擷取的平均池化向量
   - `${query_colbert_vectors}`：用於精確延遲互動評分的多重向量
- 重寫後的查詢結構：
   - `knn` 查詢：使用 `query_knn_vector` 快速找出前 100 個候選項目
   - `rescore_query`：使用 `query_colbert_vectors` 搭配 `lateInteractionScore` 函式進行精確的重新排序
   - `_source` 篩選：從回應中排除向量欄位以縮減承載大小

## 步驟 6：使用延遲互動重新排序進行搜尋

現在您可以使用 k-NN 擷取與延遲互動重新排序來搜尋文件：

```json
GET /multimodal_docs/_search?search_pipeline=colpali_search_pipeline
{
  "query": {
    "term": {
      "search_text": {
        "value": "financial report"
      }
    }
  }
}
```
{% include copy-curl.html %}

當您執行此搜尋請求時，OpenSearch 會執行下列步驟：

1. **查詢處理**：搜尋文字 (`"financial data charts"`) 會傳送至 ColPali 模型，由該模型產生查詢向量。

1. **k-NN 擷取**：平均池化查詢向量 (`query_knn_vector`) 會執行近似 k-NN 搜尋，以擷取前 100 個候選文件。此步驟以速度為優先。

1. **延遲互動重新排序**：多重向量 (`query_colbert_vectors`) 會搭配 `lateInteractionScore` 函式，根據細微的詞元層級比對來重新排序結果。此步驟以準確度為優先。

1. **最終結果**：傳回前 10 個文件，並依其延遲互動分數排序。

此混合方法兼顧速度與準確度，適合用於正式環境的搜尋系統。回應包含根據與查詢的語意相似度重新排序的文件，其中延遲互動評分比單純的傳統向量搜尋提供更細緻的相關性：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 2135,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 11.68498,
    "hits": [
      {
        "_index": "multimodal_docs",
        "_id": "3",
        "_score": 11.68498,
        "_source": {
          "image": "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",
          "description": "Quarterly financial report with revenue charts, expense breakdowns, and profit margin analysis across different business units",
          "title": "Financial Report Summary"
        }
      },
      {
        "_index": "multimodal_docs",
        "_id": "1",
        "_score": 9.761469,
        "_source": {
          "image": "iVBORw0KGgoAAAANSUhEUgAAAMwAAAAgCAYAAABepJcLAAAAAXNSR0IArs4c6QAAAGJlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAABJKGAAcAAAASAAAAUKABAAMAAAABAAEAAKACAAQAAAABAAAAzKADAAQAAAABAAAAIAAAAABBU0NJSQAAAFNjcmVlbnNob3SjVaBQAAAB1WlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNi4wLjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczpleGlmPSJodHRwOi8vbnMuYWRvYmUuY29tL2V4aWYvMS4wLyI+CiAgICAgICAgIDxleGlmOlBpeGVsWURpbWVuc2lvbj4zMjwvZXhpZjpQaXhlbFlEaW1lbnNpb24+CiAgICAgICAgIDxleGlmOlBpeGVsWERpbWVuc2lvbj4yMDQ8L2V4aWY6UGl4ZWxYRGltZW5zaW9uPgogICAgICAgICA8ZXhpZjpVc2VyQ29tbWVudD5TY3JlZW5zaG90PC9leGlmOlVzZXJDb21tZW50PgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4K23hIHgAAC3pJREFUeAHtXAl0jlcafhLZEJKISIg9lliGhIptLKOxDLGvpSVqKYo0nTqtGkuHU13o4BQdjK1qjS1irZ0oofa1xBZECLFLSGTuc5PvP/+S/P/304yeuq/z59ve+977Pffdv3M4JCXfzYQihYBCQBcCjrq4FJNCQCEgEVAGoxRBIWAHAspg7ABLsSoElMEoHVAI2IGAMhg7wFKsCgFlMEoHFAJ2IKAMxg6wFKtCQBmM0gGFgB0IKIOxAyzFqhBQBqN0QCFgBwLKYOwAS7EqBJTBKB1QCNiBgDIYO8BSrAoBZTBKBxQCdiDwRhhManoa7qU+sAOW34c1Lf0ZbjxMMvyepqdaFfy61mm+qJuPbiNT/PujEddEPInr6yLH9ssH4tbjO3J+btjG+F3yt/3yL7h87xpeZL54qbVpyvJSg20M+jXxJPgzpwPXj+J08gXz2+i+ahgCZ4biyfOnFs/y8sbhmydRa05bwy/qzEar0+X1Ou+nPsTdp/esriE24VcEzW6DKQfmWeXLy4fPM54j7sYxzD6yFNRDzUDSM9IllocST+Tl9AbZV+5fR/qLDMM1TxypZGkZWRZLL9w3egS+2/9fjNs9BfXmdULbZf1x6V6CySA9FwduHEXXlR/qYbWbJzbhEPpE/8PECz5/kY5eaz7CiaSzFvI6Vm6B8Jqdkd/ZzeJZXt6oX7IWbkbGyV8ZD3+bU+X1OmcdWYJJ++dYXUeAV2m0qxSKev5BVvny6iEjSPCcMLRbNgBbL8Vi+OZxCBM6SCP6fxKzgbpzOyL5yV2TaZ14VdjV3eTmd81H4S/FKsvw9+6aSAxcPwqbe86Ho4P+DO5B2kMTmb/nRYuARvgydgZO376Aaj4VpejDIuI8evYEb5draDFVeM0uFvf+iDfyep0pOtJSP3cfzGrz5WuBh0pKfSvvWRoH+61Ffic3PEh7hF1XDsA5n7PBaBwc8n55nDcnkgbj4Voop2coUcgXkXX7YcD6kdgrvHrj0iF4/PwJFp1Yg/Xnd8iw+bcy9dCzenu0rfS2lMGQ/vW+H5DwIBGJj26h2Y89DbJnh01EgFcZaYgMt9su78Nvdy6he7UwhNfojGC/agZeayeB3gGgx94uxmsGw9BdV3jFogW85NC5R5fLdWpyfAsWxZJO07RLeYxPuYLph37Elot7wHS0nn8wBtd+Fw1L1ZbPm//UGxOafizl8gZz+56rI/BTxyko7l4MGSJd3XhhJxafjBZYHJV49RJY9BHv4ubkKmXY+qNnnUM2jsbZ5HgLUYs7TgUVnF7ZGp7/ObwY0b9txbk7F6WM/dcOyyMj7voec2WqGra0n4n8TxsMQsuAxib3Ys5vw6zDS+W+/7XUWxgeEi51gkyM8C0FXlNajMH3hxbKvSGew+r0MeBnIiyHC6bZTKk1YyELnbmmW9qQ24/vYtCGf4oItFfumfEctvSTMo4lncHUuHmYFPo5JsbOFCXITrn/K7vMRGmPEuiz9hPcS8uqeTtHDYZrPhc59bCQPnBiCLZGNBLShbuXJTjXHySBRvFR3b4o51lKWH+cNKgjJdYLJfJBVZ8KGNckAjHCoJafjsGk5p8bxJcsVFye7xXjnwoFnRw6Cl5uheVmD900FrHhUQZeWycdRJq1SdRbBIvEl6bRadSifCME+VWVl1svxmLhiVXaI8MxcssEFMnvKZWG0XPbpX3SyDWGE7fO4uGzx9qlWHOq3NBn2ekBc+qlp9ahY2ALjG8aKZzETfSP+RQl3H0tNtkgxOxEzzr5jlrDgHn14A2j8X5QN2ksFGcLz1YBTVCnRA1M2DNdKuBwsfEkLWNwEQphvE/dVg7FfTMPG3N+u3i3kYgI6YuxjSOw6uwmkG911x/A1BOZmRKbTlGD8EWTSPQP7o5pcfMxdtcUbBLZiR6iItMRliqcpSe5jflgwyhMFlnQ+0FdLeawpZ+UyT3dfTUOHVZ8gEal6mB2m4nS+VUoUgYujs5Sfy+mJIA6OabRcPgULCKX4l/ID05RXWbkti5538OtkPSmd7KLxUre5bCw/WQ5QcL9GyhZ2A/uLgWwOX63rBO83Dzg5eeB40nnwMhVy6+6hfxuVVuDPxZz8feuivQvEAuOr8IZ4V2qFK1gwZ/TjVbC+9FLJD9JEd4hVUaq5sJINCopQOePdP7OZXk0/8PNOXbrDM4LZ8CowjrHHnJ1csGiDv+WQ5IeJ8PZ0QlBvlURfX6rboPRs04NkztPUzBs0zhZY4wXkU8jW3jyPfnzLuAJnwLeFnvi5JjP5F5O0ZFRNFSkuyMbDpbT1i5eHb+ISLXizIYsg8lezLSW49C6QlN5Nah2L3SJGoKU1PvCMXpkc+R+uCqcQVnPkrkzZD+Z2/abXOewpZ+acKbv7SqG4pP6A7RbhiN1lukgqaZvFYNj4rUTUwtrRI/G1IrWRWKn6SuRci0+uVakQ5UQ6F0ehVzcLYojWzLpefYmHERIiSCU9yol2an8eokvwvRr19UDMpzS6Gx5JnPZjITTDy0S4X2UrH/o7enN6Y310rxjK4SXWyAjJfFg9El6lKx3uG4+phq9VkdKJ/B9q3HIZ1RPco9eFU9bC2HKyTTNmJqVayDTWeN7xum9v0jpSezO6TGYwKIBWH9hh7G4HM+tzWGPfkaILMlekjWMtUE7Lu+Xj4Oz0xumIIwmu3ovNRhRfMoQCxFuwvvS67ItrYV+jemL3VNFEeeEowM2yOjE1t2cI8u0x7qOlNkpsBV+vrhXGnHbis10jTNm8s7vJULuMIxuNFTm97MOL5FdwXNDtsnoSF7jLomWimkyTtw6h5Hbv8XabrMMeTrbsaytzIlePF3k+S9D7BD1X/eZjOpzwr4CUyhj0ounWz5Xk/cxlmHrnM7gyM1TJmwHbxxHdXH/96IaxarIjIGRS6Z5LyFYr35StIP4lxu5ZtegrGVYJ2qUY9uL6RcLRKZJn23/WhSxnQyp0oWUq2Aq4u5SUHrl+ceiZENAE6gdKxYpJ5+vOrtZFoRsWTMMkiibXsJFGA0L6TG7stIabazeY8vyjbHm3Bbp5dg5s4cYzZjesNCkwVbwKgtuGClT5OOkMGGE/HZCD07jGCwKTWPifZKnqMNY9NJQFhxfacxiOGeRzEYJuy9s05NfD9HhRP48AQcTj2NqyzEyjeXa+dNk6MWTHpxrPC5a7/wIyMaMXmLLm3u57FSMnJuRlZ8kwipmNXv0yrHGR6fcpcrf8d7aj7FBNFP4fZDNnIbzu8g9sDZWe6ZXPzX+3I5atrLk5DpRzz2UuHM9JhFGiwQ9xIc+EvPxic1GyK6PJrifKLS2if545RlZQL1TrZ3M1x3Men3McQfWekcWTiyeSPPbfQsWoKOFVw8X33vYbWP9M7xOuKyTzGVoc+Z2DPGvKcczUrBzZo2cRTFnTDT6ciIV5PccLRXkWqaKLg8NgDQguIeIIN/IfjzTP+bn7JJpnqlZ2fpgl7DJwh6Sv0HJ2ugqarP9147Ia+M/vap3wNDNY1FpRlYk3NJzIWr4BhqzyHPzde68sl8aLR8adxx5Hd19tkhpa+rGkzUaO4ItFvfmcIndnj7LJfbyhtEfR7P9ZMubxj5q5yREbPmXTIfZZdLqFWTzm48zEmnzlPrHTxp0xvz+QgfLPWGnlt0r7SOitTn06qetxbAendl6PEZsnQh2GUkfvvUeHF7mf76kd6K1FRGFHPvj1uiZ+Ch6W3z8oVIbF5N8eaY7vu5FDQpoTU5ePmP0y8jMkGvMaR4alNauzuk5c3RHR0dRyxXM6bHJvUQRUT1FI0UrKk0evsKFPXhyP8jvU6AImCraQ4x43Pu83jfOw3UWK+htt37Yo5+23p3rYBZEI2aL+6UMxtYk6rlC4M+KQI41zJ/1ZdV7KQReFQFlMK+KoBr/RiGgDOaN2m71sq+KgDKYV0VQjX+jEPgf9X05Z4Ml7BIAAAAASUVORK5CYII=",
          "description": "A comprehensive bar chart showing quarterly sales performance with multiple data series and trend analysis",
          "title": "Data Visualization Chart"
        }
      },
      {
        "_index": "multimodal_docs",
        "_id": "2",
        "_score": 9.619822,
        "_source": {
          "image": "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",
          "description": "System architecture diagram showing microservices, databases, and API connections with detailed component relationships",
          "title": "Technical Architecture Diagram"
        }
      }
    ]
  }
}
```

</details>

## 偵錯與測試

您可以執行下列動作來偵錯與測試搜尋。

### 模擬資料匯入管線

在匯入文件之前，請先測試資料匯入管線，以驗證它是否能正確處理文件：

```json
POST /_ingest/pipeline/colpali_pipeline/_simulate?verbose=true
{
  "docs": [
    {
      "_index": "multimodal_docs",
      "_id": "test_1",
      "_source": {
        "title": "Test Chart",
        "description": "Sample chart for testing pipeline",
        "image": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAAoADwDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3+iiigAooooAKKKKACiiigAooooAKKKKACiiigD//2Q=="
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應會顯示文件將如何被處理，並包含產生的 `colbert_vectors` 與 `knn_vector` 欄位：

```json
{
  "docs": [
    {
      "processor_results": [
        {
          "processor_type": "ml_inference",
          "status": "success",
          "description": "Generate multi-vectors and mean pooling vector for multimodal content",
          "tag": "ml_inference",
          "doc": {
            "_index": "multimodal_docs",
            "_id": "test_1",
            "_source": {
              "title": "Test Chart",
              "description": "Sample chart for testing pipeline",
              "image": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAAoADwDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3+iiigAooooAKKKKACiiigAooooAKKKKACiiigD//2Q==",
              "colbert_vectors": [
                [
                  -0.0653999000787735,
                  0.1100006103515625,
                  0.2052547186613083
                ],
                [
                  0.0234567890123456,
                  -0.0987654321098765,
                  0.1357924680135792
                ]
              ],
              "knn_vector": [
                0.025610961,
                0.045123789,
                0.067891234
              ]
            },
            "_ingest": {
              "pipeline": "colpali_pipeline",
              "timestamp": "2025-10-02T23:17:01.615598095Z"
            }
          }
        }
      ]
    }
  ]
}
```

### 偵錯搜尋管線

使用詳細輸出測試搜尋管線，以查看查詢如何被改寫：

```json
GET /multimodal_docs/_search?search_pipeline=colpali_search_pipeline&verbose_pipeline=true
{
  "query": {
    "term": {
      "search_text": {
        "value": "financial data charts"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應提供 `processor_results` 區段中所擷取查詢轉換過程的完整檢視。它顯示了作為輸入提交的原始查詢文字（「financial data charts」）、產生的查詢向量（包括多向量與平均池化向量），以及使用 k-NN 搜尋搭配延遲互動重新評分的改寫後查詢結構。其中也包含每個步驟的處理時間，為偵錯與效能最佳化提供詳細資訊：

```json
{
  "took": 1835,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 8.247408,
    "hits": [
      {
        "_index": "multimodal_docs",
        "_id": "3",
        "_score": 8.247408,
        "_source": {
          "title": "Financial Report Summary",
          "description": "Quarterly financial report with revenue charts, expense breakdowns, and profit margin analysis across different business units"
        }
      }
    ]
  },
  "processor_results": [
    {
      "processor_name": "ml_inference",
      "duration_millis": 1200,
      "status": "success",
      "input_data": {
        "query": {
          "term": {
            "search_text": {
              "boost": 1,
              "value": "financial data charts"
            }
          }
        }
      },
      "output_data": {
        "size": 10,
        "query": {
          "knn": {
            "knn_vector": {
              "vector": [
                -0.06357764,
                0.021222984,
                0.06605018,
                0.07643713
              ],
              "boost": 1,
              "k": 100
            }
          }
        },
        "_source": {
          "excludes": [
            "knn_vector"
          ]
        },
        "rescore": [
          {
            "query": {
              "rescore_query": {
                "script_score": {
                  "query": {
                    "match_all": {
                      "boost": 1
                    }
                  },
                  "script": {
                    "source": "lateInteractionScore(params.query_vector, 'colbert_vectors', params._source)",
                    "params": {
                      "query_vector": [
                        [
                          -0.0024404169525951147,
                          0.14708828926086426,
                          0.15877428650856018
                        ],
                        [
                          0.08923456789012346,
                          -0.03456789012345679,
                          0.20123456789012345
                        ]
                      ]
                    }
                  }
                }
              }
            }
          }
        ]
      }
    }
  ]
}
```

## 相關文件

- [延遲互動分數函式]({{site.url}}{{site.baseurl}}/query-dsl/specialized/script-score/#late-interaction-score)

