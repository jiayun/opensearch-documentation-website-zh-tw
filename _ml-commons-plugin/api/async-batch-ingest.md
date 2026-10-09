---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "非同步批次匯入"
parent: ML Commons APIs
has_children: false
has_toc: false
nav_order: 80
---

# 非同步批次匯入 API
**已於 3.0 棄用**
{: .label .label-red }

此功能已棄用。若需要類似功能，請使用 [OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/)。如果您希望此功能重新提供，請在 ML Commons 儲存庫中[建立 issue](https://github.com/opensearch-project/ml-commons/issues)。
{: .warning}


使用非同步批次匯入 API，將遠端檔案伺服器（例如 Amazon Simple Storage Service (Amazon S3) 或 OpenAI）上的檔案資料匯入您的 OpenSearch 叢集。詳細的設定步驟請參閱[非同步批次匯入]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/async-batch-ingestion/)。

## 端點

```json
POST /_plugins/_ml/_batch_ingestion
```

#### 請求本文欄位

下表列出可用的請求欄位。

欄位 | 資料類型 | 必要／選用 | 說明
:---  | :--- | :--- 
`index_name`| 字串 | 必要 | 索引名稱。 
`field_map` | 物件 | 必要 | 將來源檔案中的欄位對應至 OpenSearch 索引中要匯入的特定欄位。 
`ingest_fields` | 陣列 | 選用 | 列出來源檔案中不需額外對應即可直接匯入 OpenSearch 索引的欄位。 
`credential` | 物件 | 必要 | 包含存取外部資料來源（例如 Amazon S3 或 OpenAI）所需的驗證資訊。
`data_source` | 物件 | 必要 | 指定匯入資料的外部檔案之類型與位置。
`data_source.type` | 字串 | 必要 | 指定外部資料來源的類型。有效值為 `s3` 與 `openAI`。
`data_source.source` | 陣列 | 必要 | 指定一或多個匯入資料的檔案位置。對於 `s3`，請指定 Amazon S3 桶的檔案路徑（例如 `["s3://offlinebatch/output/sagemaker_batch.json.out"]`）。對於 `openAI`，請指定輸入或輸出檔案的檔案 ID（例如 `["file-<your output file id>", "file-<your input file id>", "file-<your other file>"]`）。

## 範例請求：匯入單一檔案

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

## 範例請求：匯入多個檔案

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

## 範例回應

```json
{
  "task_id": "cbsPlpEBMHcagzGbOQOx",
  "task_type": "BATCH_INGEST",
  "status": "CREATED"
}
```
