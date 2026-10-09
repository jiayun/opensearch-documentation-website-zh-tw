---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "非同步批次匯入"
nav_order: 90
parent: Batch ingestion
grand_parent: Connecting to externally hosted models 
great_grand_parent: Integrating ML models
---


# 非同步批次匯入
**已棄用 3.0**
{: .label .label-red }

此功能已棄用。如需類似功能，請使用 [OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/)。若您希望恢復此功能，請在 ML Commons 儲存庫中[建立問題](https://github.com/opensearch-project/ml-commons/issues)。
{: .warning}


[批次匯入]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/batch-ingestion/)會設定資料匯入管線，逐一處理文件。批次匯入會針對每份文件呼叫外部託管的模型，從文件文字產生文字嵌入，然後將文件 (包含文字與嵌入) 匯入 OpenSearch 索引。

此即時程序的替代方案是_非同步_批次匯入，它會同時匯入文件及其嵌入，而這些嵌入是在 OpenSearch 外部產生並儲存在遠端檔案伺服器上，例如 Amazon Simple Storage Service (Amazon S3) 或 OpenAI。非同步匯入會傳回任務 ID，並以非同步方式執行，將資料離線匯入您的 k-NN 叢集以進行神經搜尋。您可以將非同步批次匯入與 [Batch Predict API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/batch-predict/) 搭配使用，以非同步方式執行推論。批次預測作業會接收包含文件的輸入檔案，並呼叫外部託管的模型，將這些文件的嵌入產生到輸出檔案中。接著，您可以使用非同步批次匯入，將包含文件的輸入檔案及包含其嵌入的輸出檔案一併匯入 OpenSearch 索引。

非同步批次匯入 API 支援 Amazon SageMaker、Amazon Bedrock 及 OpenAI。
{: .note}

## 先決條件

使用非同步批次匯入之前，您必須使用您選擇的模型產生文字嵌入，並將輸出儲存在檔案伺服器上，例如 Amazon S3。舉例來說，您可以將對 Amazon SageMaker 文字嵌入模型進行 Batch API 呼叫的輸出，儲存在 Amazon S3 輸出路徑 `s3://offlinebatch/output/sagemaker_batch.json.out` 的檔案中。輸出為 JSONL 格式，每一行代表一筆文字嵌入結果。檔案內容格式如下：

```
{"SageMakerOutput":[[-0.017166402,0.055771016,...],[-0.06422759,-0.004301484,...],"content":["this is chapter 1","harry potter"],"id":1}
{"SageMakerOutput":[[-0.017455402,0.023771016,...],[-0.02322759,-0.009101284,...],"content":["this is chapter 2","draco malfoy"],"id":1}
...
```

## 從單一檔案匯入資料

首先，建立一個 k-NN 索引，您將把資料匯入其中。k-NN 索引中的欄位代表來源檔案中資料的結構。

在此範例中，來源檔案包含含有標題與章節的文件，以及其對應的嵌入。因此，您將建立一個包含欄位 `id`、`chapter_embedding`、`chapter`、`title_embedding` 及 `title` 的 k-NN 索引：

```json
PUT /my-nlp-index
{
  "settings": {
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "id": {
        "type": "text"
      },
      "chapter_embedding": {
        "type": "knn_vector",
        "dimension": 384,
        "method": {
          "engine": "faiss",
          "space_type": "cosinesimil",
          "name": "hnsw",
          "parameters": {
            "ef_construction": 512,
            "m": 16
          }
        }
      },
      "chapter": {
        "type": "text"
      },
      "title_embedding": {
        "type": "knn_vector",
        "dimension": 384,
        "method": {
          "engine": "faiss",
          "space_type": "cosinesimil",
          "name": "hnsw",
          "parameters": {
            "ef_construction": 512,
            "m": 16
          }
        }
      },
      "title": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

使用 S3 檔案作為非同步批次匯入的來源時，您必須將來源檔案中的欄位對應至索引中的欄位，以指出每一筆資料要匯入哪個索引。若未提供某個欄位的 JSON 路徑，該欄位在 k-NN 索引中將設為 `null`。

在 `field_map` 中，指出來源檔案中每個欄位的資料位置。您也可以將欄位的 JSON 路徑新增至 `ingest_fields` 陣列，以指定要直接匯入索引的欄位，而不對來源檔案做任何變更。舉例來說，在下列非同步批次匯入請求中，來源檔案中 JSON 路徑為 `$.id` 的元素會直接匯入您索引的 `id` 欄位。若要從 Amazon S3 檔案匯入此資料，請將下列請求傳送至您的 OpenSearch 端點：

```json
POST /_plugins/_ml/_batch_ingestion
{
  "index_name": "my-nlp-index",
  "field_map": {
    "chapter": "$.content[0]",
    "title": "$.content[1]",
    "chapter_embedding": "$.SageMakerOutput[0]",
    "title_embedding": "$.SageMakerOutput[1]",
    "_id": "$.id"
  },
  "ingest_fields": ["$.id"],
  "credential": {
    "region": "us-east-1",
    "access_key": "<your access key>",
    "secret_key": "<your secret key>",
    "session_token": "<your session token>"
  },
  "data_source": {
    "type": "s3",
    "source": ["s3://offlinebatch/output/sagemaker_batch.json.out"]
  }
}
```
{% include copy-curl.html %}

回應包含匯入任務的任務 ID：

```json
{
  "task_id": "cbsPlpEBMHcagzGbOQOx",
  "task_type": "BATCH_INGEST",
  "status": "CREATED"
}
```

若要檢查作業狀態，請將任務 ID 提供給 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/)。匯入完成後，任務 `state` 會變更為 `COMPLETED`。


## 從多個檔案匯入資料

您也可以在 `source` 中指定檔案位置，從多個檔案匯入資料。下列範例會從三個 OpenAI 檔案匯入資料。

OpenAI Batch API 輸入檔案的格式如下：

```
{"custom_id": "request-1", "method": "POST", "url": "/v1/embeddings", "body": {"model": "text-embedding-ada-002", "input": [ "What is the meaning of life?", "The food was delicious and the waiter..."]}}
{"custom_id": "request-2", "method": "POST", "url": "/v1/embeddings", "body": {"model": "text-embedding-ada-002", "input": [ "What is the meaning of work?", "The travel was fantastic and the view..."]}}
{"custom_id": "request-3", "method": "POST", "url": "/v1/embeddings", "body": {"model": "text-embedding-ada-002", "input": [ "What is the meaning of friend?", "The old friend was far away and the time..."]}}
...
```

OpenAI Batch API 輸出檔案的格式如下：

```
{"id": "batch_req_ITKQn29igorXCAGp6wzYs5IS", "custom_id": "request-1", "response": {"status_code": 200, "request_id": "10845755592510080d13054c3776aef4", "body": {"object": "list", "data": [{"object": "embedding", "index": 0, "embedding": [0.0044326545, ... ...]}, {"object": "embedding", "index": 1, "embedding": [0.002297497, ... ... ]}], "model": "text-embedding-ada-002", "usage": {"prompt_tokens": 15, "total_tokens": 15}}}, "error": null}
...
```

若您已在 OpenAI 中執行 Batch API 以進行文字嵌入，並想將模型輸入與輸出檔案以及一些中繼資料匯入您的索引，請傳送下列非同步匯入請求。請務必使用 `source[file-index]` 來識別檔案在請求本文中來源陣列的位置。舉例來說，`source[0]` 指的是 `data_source.source` 陣列中的第一個檔案。

下列請求會將七個欄位匯入您的索引：其中五個指定於 `field_map` 區段，兩個指定於 `ingest_fields`。格式遵循 `sourcefile.jsonPath` 模式，指出每個檔案的 JSON 路徑。在 field_map 中，`$.body.input[0]` 用作 JSON 路徑，以從 `source` 陣列中的第二個檔案將資料匯入 `question` 欄位。`ingest_fields` 陣列列出 `source` 檔案中將直接匯入您索引的所有元素：

```json
POST /_plugins/_ml/_batch_ingestion
{
  "index_name": "my-nlp-index-openai",
  "field_map": {
    "question": "source[1].$.body.input[0]",
    "answer": "source[1].$.body.input[1]",
    "question_embedding":"source[0].$.response.body.data[0].embedding",
    "answer_embedding":"source[0].$.response.body.data[1].embedding",
    "_id": ["source[0].$.custom_id", "source[1].$.custom_id"]
  },
  "ingest_fields": ["source[2].$.custom_field1", "source[2].$.custom_field2"],
  "credential": {
    "openAI_key": "<you openAI key>"
  },
  "data_source": {
    "type": "openAI",
    "source": ["file-<your output file id>", "file-<your input file id>", "file-<your other file>"]
  }
}
```
{% include copy-curl.html %}

在請求中，請務必在 `field_map` 中定義 `_id` 欄位。這是為了對應來自三個不同檔案的每一筆資料項目所必需。

回應包含匯入任務的任務 ID：

```json
{
  "task_id": "cbsPlpEBMHcagzGbOQOx",
  "task_type": "BATCH_INGEST",
  "status": "CREATED"
}
```

若要檢查作業狀態，請將任務 ID 提供給 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/)。匯入完成後，任務 `state` 會變更為 `COMPLETED`。

如需請求欄位說明，請參閱 [Asynchronous Batch Ingestion API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/async-batch-ingest/)。