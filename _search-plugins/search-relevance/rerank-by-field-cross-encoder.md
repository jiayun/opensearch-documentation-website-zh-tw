---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用交叉編碼器依欄位重新排序"
parent: Reranking search results
grand_parent: Optimizing search quality
has_children: false
nav_order: 30
---

# 使用交叉編碼器模型依欄位重新排序
**於 2.18 版推出**
{: .label .label-purple }

在本教學中，您將學習如何使用託管於 Amazon SageMaker 的交叉編碼器模型，重新排序搜尋結果並提升搜尋相關性。

若要重新排序文件，您將設定一個在查詢時處理搜尋結果的搜尋管線。此管線會攔截搜尋結果，並將其傳遞至 [`ml_inference` 搜尋回應處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/ml-inference-search-response/)，該處理器會叫用交叉編碼器模型。模型會產生分數，用來重新排序相符的文件 [`by_field`]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/rerank-by-field/)。

## 先決條件：在 Amazon SageMaker 上部署模型

執行下列程式碼，在 Amazon SageMaker 上部署模型。在此範例中，您將使用託管於 Amazon SageMaker 的 [`ms-marco-MiniLM-L-6-v2`](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2) Hugging Face 交叉編碼器模型。我們建議使用 GPU 以獲得更好的效能：

```python
import sagemaker
import boto3
from sagemaker.huggingface import HuggingFaceModel

sess = sagemaker.Session()
role = sagemaker.get_execution_role()

hub = {
    'HF_MODEL_ID':'cross-encoder/ms-marco-MiniLM-L-6-v2',
    'HF_TASK':'text-classification'
}
huggingface_model = HuggingFaceModel(
    transformers_version='4.37.0',
    pytorch_version='2.1.0',
    py_version='py310',
    env=hub,
    role=role, 
)
predictor = huggingface_model.deploy(
    initial_instance_count=1, # number of instances
    instance_type='ml.m5.xlarge' # ec2 instance type
)
```
{% include copy.html %}

部署模型後，您可以前往 AWS Management Console 中的 Amazon SageMaker 主控台，並在左側索引標籤選取 **Inference > Endpoints**，以找到模型端點。請記下所建立模型的 URL；您將使用它來建立連接器。

## 執行含重新排序的搜尋

若要執行含重新排序的搜尋，請依照下列步驟：

1. [建立連接器](#step-1-create-a-connector)。
1. [註冊模型](#step-2-register-the-model)。
1. [將文件匯入索引](#step-3-ingest-documents-into-an-index)。
1. [建立搜尋管線](#step-4-create-a-search-pipeline)。
1. [使用重新排序進行搜尋](#step-5-search-using-reranking)。

## 步驟 1：建立連接器

在 `actions.url` 參數中提供模型 URL，以建立與交叉編碼器模型的連接器：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "SageMaker cross-encoder model",
  "description": "Test connector for SageMaker cross-encoder hosted model",
  "version": 1,
  "protocol": "aws_sigv4",
  "credential": {
		"access_key": "<YOUR_ACCESS_KEY>",
		"secret_key": "<YOUR_SECRET_KEY>",
		"session_token": "<YOUR_SESSION_TOKEN>"
  },
  "parameters": {
    "region": "<REGION>",
    "service_name": "sagemaker"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "<YOUR_SAGEMAKER_ENDPOINT_URL>",
      "headers": {
        "content-type": "application/json"
      },
      "request_body": "{ \"inputs\": { \"text\": \"${parameters.text}\", \"text_pair\": \"${parameters.text_pair}\" }}"
    }
  ]
}
```
{% include copy-curl.html %}

請記下回應中包含的連接器 ID；您將在下一步中使用它。

## 步驟 2：註冊模型

若要註冊模型，請在 `connector_id` 參數中提供連接器 ID：

```json
POST /_plugins/_ml/models/_register
{
  "name": "Cross encoder model",
  "version": "1.0.1",
  "function_name": "remote",
  "description": "Using a SageMaker endpoint to apply a cross encoder model",
  "connector_id": "<YOUR_CONNECTOR_ID>"
} 
```
{% include copy-curl.html %}


## 步驟 3：將文件匯入索引

建立索引並匯入內含紐約市各行政區相關資訊的範例文件：

```json
POST /nyc_areas/_bulk
{ "index": { "_id": 1 } }
{ "borough": "Queens", "area_name": "Astoria", "description": "Astoria is a neighborhood in the western part of Queens, New York City, known for its diverse community and vibrant cultural scene.", "population": 93000, "facts": "Astoria is home to many artists and has a large Greek-American community. The area also boasts some of the best Mediterranean food in NYC." } 
{ "index": { "_id": 2 } }
{ "borough": "Queens", "area_name": "Flushing", "description": "Flushing is a neighborhood in the northern part of Queens, famous for its Asian-American population and bustling business district.", "population": 227000, "facts": "Flushing is one of the most ethnically diverse neighborhoods in NYC, with a large Chinese and Korean population. It is also home to the USTA Billie Jean King National Tennis Center." } 
{ "index": { "_id": 3 } }
{ "borough": "Brooklyn", "area_name": "Williamsburg", "description": "Williamsburg is a trendy neighborhood in Brooklyn known for its hipster culture, vibrant art scene, and excellent restaurants.", "population": 150000, "facts": "Williamsburg is a hotspot for young professionals and artists. The neighborhood has seen rapid gentrification over the past two decades." } 
{ "index": { "_id": 4 } }
{ "borough": "Manhattan", "area_name": "Harlem", "description": "Harlem is a historic neighborhood in Upper Manhattan, known for its significant African-American cultural heritage.", "population": 116000, "facts": "Harlem was the birthplace of the Harlem Renaissance, a cultural movement that celebrated Black culture through art, music, and literature." } 
{ "index": { "_id": 5 } }
{ "borough": "The Bronx", "area_name": "Riverdale", "description": "Riverdale is a suburban-like neighborhood in the Bronx, known for its leafy streets and affluent residential areas.", "population": 48000, "facts": "Riverdale is one of the most affluent areas in the Bronx, with beautiful parks, historic homes, and excellent schools." } 
{ "index": { "_id": 6 } }
{ "borough": "Staten Island", "area_name": "St. George", "description": "St. George is the main commercial and cultural center of Staten Island, offering stunning views of Lower Manhattan.", "population": 15000, "facts": "St. George is home to the Staten Island Ferry terminal and is a gateway to Staten Island, offering stunning views of the Statue of Liberty and Ellis Island." }
```
{% include copy-curl.html %}

## 步驟 4：建立搜尋管線

接著，建立用於重新排序的搜尋管線。在搜尋管線組態中，`input_map` 與 `output_map` 會定義如何為交叉編碼器模型準備輸入資料，以及如何解讀模型的輸出以進行重新排序：

- `input_map` 會指定搜尋文件與查詢中的哪些欄位應做為模型輸入：
    - `text` 欄位會對應至已編製索引文件中的 `facts` 欄位。它會提供模型將分析的文件特定內容。
    - `text_pair` 欄位會從搜尋請求中動態擷取搜尋查詢文字 (`multi_match.query`)。

    `text` (文件 `facts`) 與 `text_pair` (搜尋 `query`) 的組合，可讓交叉編碼器模型考量文件與查詢之間的語意關係，進而比較其相關性。

- `output_map` 欄位會指定模型的輸出如何對應至回應中的欄位：
    - 回應中的 `rank_score` 欄位將儲存模型的相關性分數，該分數將用於執行重新排序。

使用 `by_field` 重新排序類型時，`rank_score` 欄位將包含與 `_score` 欄位相同的分數。若要從搜尋結果中移除 `rank_score` 欄位，請將 `remove_target_field` 設為 `true`。

比較原始分數與重新排序後的分數，有助於您評估搜尋相關性的改善程度。若要比較原始 BM25 分數與重新排序後的分數，請將 `keep_previous_score` 設為 `true`。原始分數會基於偵錯目的納入搜尋結果中，且預設會儲存在 `previous_score` 欄位中。如果您的索引已包含名為 `previous_score` 的文件欄位，請將 `previous_score_field` 設為不同的名稱，以免重新排序處理器覆寫現有欄位。

    
若要建立搜尋管線，請傳送下列請求：

```json
PUT /_search/pipeline/my_pipeline
{
  "response_processors": [
    {
      "ml_inference": {
        "tag": "ml_inference",
        "description": "This processor runs ml inference during search response",
        "model_id": "<model_id_from_step_3>",
        "function_name": "REMOTE",
        "input_map": [
          {
            "text": "facts",
            "text_pair":"$._request.query.multi_match.query"
          }
        ],
        "output_map": [
          {
            "rank_score": "$.score"
          }
        ],
        "full_response_path": false,
        "model_config": {},
        "ignore_missing": false,
        "ignore_failure": false,
        "one_to_one": true
      },
       
      "rerank": {
        "by_field": {
          "target_field": "rank_score",
          "remove_target_field": true,
          "keep_previous_score": true,
          "previous_score_field": "original_query_score"
        }
      }
    
    }
  ]
}
```
{% include copy-curl.html %}

## 步驟 5：使用重新排序進行搜尋

使用下列請求來搜尋已編製索引的文件，並使用交叉編碼器模型重新排序。此請求會擷取在 `description` 或 `facts` 欄位中包含任何指定詞彙的文件。接著使用這些詞彙來比較並重新排序符合的文件：

```json
POST /nyc_areas/_search?search_pipeline=my_pipeline
{
  "query": {
    "multi_match": {
      "query": "artists art creative community",
      "fields": ["description", "facts"]
    }
  }
}
```
{% include copy-curl.html %}

在回應中，`original_query_score` 欄位包含文件的 BM25 分數，也就是在未套用管線的情況下文件原本會得到的分數。請注意，雖然 BM25 將 "Astoria" 排名最高，但交叉編碼器模型優先考慮 "Harlem"，因為它符合較多的搜尋詞彙：

```json
{
  "took": 4,
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
    "max_score": 0.03418137,
    "hits": [
      {
        "_index": "nyc_areas",
        "_id": "4",
        "_score": 0.03418137,
        "_source": {
          "area_name": "Harlem",
          "description": "Harlem is a historic neighborhood in Upper Manhattan, known for its significant African-American cultural heritage.",
          "original_query_score": 1.6489418,
          "borough": "Manhattan",
          "facts": "Harlem was the birthplace of the Harlem Renaissance, a cultural movement that celebrated Black culture through art, music, and literature.",
          "population": 116000
        }
      },
      {
        "_index": "nyc_areas",
        "_id": "1",
        "_score": 0.0090838,
        "_source": {
          "area_name": "Astoria",
          "description": "Astoria is a neighborhood in the western part of Queens, New York City, known for its diverse community and vibrant cultural scene.",
          "original_query_score": 2.519608,
          "borough": "Queens",
          "facts": "Astoria is home to many artists and has a large Greek-American community. The area also boasts some of the best Mediterranean food in NYC.",
          "population": 93000
        }
      },
      {
        "_index": "nyc_areas",
        "_id": "3",
        "_score": 0.0032599436,
        "_source": {
          "area_name": "Williamsburg",
          "description": "Williamsburg is a trendy neighborhood in Brooklyn known for its hipster culture, vibrant art scene, and excellent restaurants.",
          "original_query_score": 1.5632852,
          "borough": "Brooklyn",
          "facts": "Williamsburg is a hotspot for young professionals and artists. The neighborhood has seen rapid gentrification over the past two decades.",
          "population": 150000
        }
      }
    ]
  },
  "profile": {
    "shards": []
  }
}
```
 