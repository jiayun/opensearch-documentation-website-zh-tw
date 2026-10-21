---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 ML 推論處理器的多模態搜尋"
parent: Semantic search
grand_parent: Vector search
nav_order: 95
---

# 使用 ML 推論處理器的多模態搜尋

本教學說明如何使用 [Amazon Bedrock Titan Multimodal Embeddings 模型](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-multiemb-models.html)（`amazon.titan-embed-image-v1`）與 ML 推論處理器來搜尋文字與影像資料。透過這些處理器，您可以使用單一搜尋管線，以文字、影像或文字與影像同時搜尋索引。如需多模態搜尋的更多資訊，請參閱[多模態搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/multimodal-search/)。

在本教學中，您將使用下列 OpenSearch 元件：
- [ML 推論資料匯入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/ml-inference/)
- [ML 推論搜尋請求處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/ml-inference-search-request/)
- [k-NN 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/k-nn/)

如需相關的 Python 範例，請參閱[電子商務示範筆記本](https://github.com/opensearch-project/ml-commons/blob/main/docs/tutorials/ml_inference/ecommerce_demo.ipynb)，其中使用 ML 推論處理器將產品影像編製索引，並以文字或影像進行搜尋。

本教學的步驟使用自行管理的 OpenSearch，並在連接器的認證資訊中使用 AWS 存取金鑰。若使用 Amazon OpenSearch Service，請參閱[使用 Amazon OpenSearch Service](#using-amazon-opensearch-service)。
{: .note}

請將以 `your_` 為前置詞的預留位置替換為您自己的值。
{: .note}

## 步驟 1：建立嵌入模型

依照下列步驟建立並測試嵌入模型。

### 步驟 1.1：建立連接器

若要建立模型的連接器，請傳送下列請求。由於本教學會使用 ML 推論處理器，因此您不需要在連接器中指定前置或後置處理函式：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Amazon Bedrock connector: Titan Multimodal Embeddings",
  "description": "The connector to the Amazon Bedrock Titan Multimodal Embeddings model",
  "version": 1,
  "protocol": "aws_sigv4",
  "credential": {
    "access_key": "your_aws_access_key",
    "secret_key": "your_aws_secret_key",
    "session_token": "your_aws_session_token"
  },
  "parameters": {
    "region": "your_aws_region",
    "service_name": "bedrock",
    "model": "amazon.titan-embed-image-v1"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "headers": {
        "content-type": "application/json"
      },
      "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/invoke",
      "request_body": "{\"inputText\": \"${parameters.inputText:-null}\", \"inputImage\": \"${parameters.inputImage:-null}\"}"
    }
  ]
}
```
{% include copy-curl.html %}

模型接受 `inputText` 參數中的文字，以及 `inputImage` 參數中以 Base64 編碼的影像。`:-null` 後綴會在請求未提供參數時將其設為 `null`，因此您可以傳送文字、影像或兩者。

回應包含連接器 ID：

```json
{
  "connector_id": "P8c_JZUB7judm8f4591w"
}
```

請記下連接器 ID；您將在下一步使用它。

### 步驟 1.2：註冊並部署模型

若要註冊並部署模型，請傳送下列請求：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "Amazon Bedrock Titan Multimodal Embeddings",
  "function_name": "remote",
  "description": "Multimodal embedding model",
  "connector_id": "P8c_JZUB7judm8f4591w"
}
```
{% include copy-curl.html %}

回應包含模型 ID：

```json
{
  "task_id": "nMdJJZUB7judm8f4HN29",
  "status": "CREATED",
  "model_id": "ncdJJZUB7judm8f4HN3P"
}
```

請記下模型 ID；您將在後續步驟使用它。

### 步驟 1.3：測試模型

若要測試模型，請傳送下列請求。若要為影像產生嵌入，請在 `inputImage` 參數中提供以 Base64 編碼的影像。若您同時提供 `inputText` 與 `inputImage`，模型會產生一個代表兩項輸入的嵌入：

```json
POST /_plugins/_ml/models/ncdJJZUB7judm8f4HN3P/_predict
{
  "parameters": {
    "inputText": "Say this is a test"
  }
}
```
{% include copy-curl.html %}

由於連接器沒有後置處理函式，回應會在 `dataAsMap` 物件中包含模型輸出。`embedding` 欄位包含模型產生的嵌入：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "embedding": [
              0.022338867,
              ...
            ],
            "inputTextTokenCount": 7,
            "message": null,
            "successCount": null,
            "failureCount": null,
            "results": null
          }
        }
      ],
      "status_code": 200
    }
  ]
}
```

## 步驟 2：建立資料匯入管線

建立包含 ML 推論處理器的資料匯入管線。處理器的 `input_map` 會將文件的 `name` 欄位傳遞給模型的 `inputText` 參數，並將 `image` 欄位傳遞給 `inputImage` 參數。`output_map` 會將模型輸出中的 `embedding` 欄位儲存到名為 `multimodal_embedding` 的新文件欄位：

```json
PUT /_ingest/pipeline/ml_inference_pipeline_multimodal
{
  "description": "Generate multimodal embeddings for ingested documents",
  "processors": [
    {
      "ml_inference": {
        "tag": "ml_inference",
        "model_id": "ncdJJZUB7judm8f4HN3P",
        "input_map": [
          {
            "inputText": "name",
            "inputImage": "image"
          }
        ],
        "output_map": [
          {
            "multimodal_embedding": "embedding"
          }
        ],
        "ignore_missing": true,
        "ignore_failure": true
      }
    }
  ]
}
```
{% include copy-curl.html %}

兩個輸入欄位位於同一個 `input_map` 物件中，因此處理器會為每份文件呼叫模型一次。由於 `ignore_missing` 為 `true`，只包含兩個欄位之一的文件仍會傳送至模型，而兩者皆未包含的文件則會在沒有嵌入的情況下編製索引。

## 步驟 3：建立索引並匯入資料

若要建立預設使用該資料匯入管線的向量索引，請傳送下列請求。`multimodal_embedding` 欄位的維度符合模型預設的嵌入長度 1,024：

```json
PUT /my-multimodal-index
{
  "settings": {
    "index.knn": true,
    "default_pipeline": "ml_inference_pipeline_multimodal"
  },
  "mappings": {
    "properties": {
      "multimodal_embedding": {
        "type": "knn_vector",
        "dimension": 1024
      }
    }
  }
}
```
{% include copy-curl.html %}

將三份文件匯入索引。第一份文件只包含文字，第二份包含文字與以 Base64 編碼的影像，第三份則不包含 `name` 或 `image` 欄位。在下列請求中，Base64 字串已截斷；請將其替換為完整的 Base64 編碼影像：

```json
POST _bulk
{ "index": { "_index": "my-multimodal-index", "_id": "1" } }
{ "name": "Central Park", "category": "Park" }
{ "index": { "_index": "my-multimodal-index", "_id": "2" } }
{ "name": "Times Square", "category": "Square", "image": "iVBORw0KGgoAAAANSUhEUgAAAFcAAAAdCAYAAADfC/BmAAAAAXNSR0IArs4c6QAAAGJlWElmTU0AKgAAAA..." }
{ "index": { "_index": "my-multimodal-index", "_id": "3" } }
{ "category": "Bridge" }
```
{% include copy-curl.html %}

若要驗證管線已從文字與影像產生嵌入，請擷取第二份文件：

```json
GET /my-multimodal-index/_doc/2
```
{% include copy-curl.html %}

文件包含產生的 `multimodal_embedding` 欄位：

```json
{
  "_index": "my-multimodal-index",
  "_id": "2",
  "_version": 1,
  "_seq_no": 1,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "multimodal_embedding": [
      0.026977539,
      ...
    ],
    "image": "iVBORw0KGgoAAAANSUhEUgAAAFcAAAAdCAYAAADfC/BmAAAAAXNSR0IArs4c6QAAAGJlWElmTU0AKgAAAA...",
    "name": "Times Square",
    "category": "Square"
  }
}
```

第一份文件包含僅從 `name` 欄位產生的嵌入。第三份文件會在沒有 `multimodal_embedding` 欄位的情況下編製索引，因為它不含 `input_map` 中的任何欄位。

## 步驟 4：建立搜尋管線

建立一個包含 ML 推論搜尋請求處理器的搜尋管線。該處理器會將搜尋請求改寫為 `knn` 查詢，使用由查詢文字、查詢影像或兩者所產生的嵌入：

```json
PUT /_search/pipeline/multimodal_semantic_search_pipeline
{
  "request_processors": [
    {
      "ml_inference": {
        "tag": "ml_inference",
        "description": "Generates an embedding from the query text or image and runs a k-NN query",
        "model_id": "ncdJJZUB7judm8f4HN3P",
        "query_template": "{\"query\": {\"knn\": {\"multimodal_embedding\": {\"vector\": ${multimodal_embedding}, \"k\": 3}}}}",
        "optional_input_map": [
          {
            "inputText": "ext.ml_inference.text",
            "inputImage": "ext.ml_inference.image"
          }
        ],
        "output_map": [
          {
            "multimodal_embedding": "embedding"
          }
        ],
        "model_config": {},
        "ignore_missing": false,
        "ignore_failure": false
      }
    }
  ]
}
```
{% include copy-curl.html %}

該處理器包含下列設定：

- `optional_input_map` 會將搜尋請求中的 `ext.ml_inference.text` 與 `ext.ml_inference.image` 欄位對應到模型的 `inputText` 與 `inputImage` 參數。處理器只會將請求中存在的欄位傳遞給模型，因此搜尋請求可以包含文字、影像或兩者。搜尋請求必須至少包含其中一個欄位：如果兩者皆未包含，處理器會傳送一個沒有輸入的請求給模型，模型則會回傳錯誤。如果您使用 `input_map`，則每個搜尋請求都必須包含這兩個欄位。
- `output_map` 會將模型輸出中的 `embedding` 欄位儲存在 `multimodal_embedding` 變數中。
- `query_template` 定義了用來取代搜尋請求中原始查詢的查詢。該範本會插入 `multimodal_embedding` 變數作為查詢向量。

## 步驟 5：搜尋索引

當您使用該管線進行搜尋時，處理器會以來自 `query_template` 的 `knn` 查詢取代請求中的查詢。下列範例傳送 `match_all` 查詢，處理器會將其取代。

### 以文字搜尋

若要以文字搜尋索引，請在 `ext.ml_inference.text` 欄位中提供查詢文字：

```json
GET /my-multimodal-index/_search?search_pipeline=multimodal_semantic_search_pipeline
{
  "query": {
    "match_all": {}
  },
  "ext": {
    "ml_inference": {
      "text": "place where recreational activities are done, picnics happen there"
    }
  }
}
```
{% include copy-curl.html %}

回應包含兩個具有嵌入的文件。`Central Park` 文件是最接近的比對結果：

```json
{
  "took": 222,
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
    "max_score": 0.5640698,
    "hits": [
      {
        "_index": "my-multimodal-index",
        "_id": "1",
        "_score": 0.5640698,
        "_source": {
          "multimodal_embedding": [
            0.01171875,
            ...
          ],
          "name": "Central Park",
          "category": "Park"
        }
      },
      {
        "_index": "my-multimodal-index",
        "_id": "2",
        "_score": 0.5551745,
        "_source": {
          "image": "iVBORw0KGgoAAAANSUhEUgAAAFcAAAAdCAYAAADfC/BmAAAAAXNSR0IArs4c6QAAAGJlWElmTU0AKgAAAA...",
          "multimodal_embedding": [
            0.026977539,
            ...
          ],
          "name": "Times Square",
          "category": "Square"
        }
      }
    ]
  }
}
```

若要檢視處理器所產生的查詢，請在搜尋請求中加入 `verbose_pipeline=true` 查詢參數：

```json
GET /my-multimodal-index/_search?search_pipeline=multimodal_semantic_search_pipeline&verbose_pipeline=true
{
  "query": {
    "match_all": {}
  },
  "ext": {
    "ml_inference": {
      "text": "place where recreational activities are done, picnics happen there"
    }
  }
}
```
{% include copy-curl.html %}

除了搜尋結果之外，回應還包含一個 `processor_results` 陣列。`input_data` 物件包含原始搜尋請求，而 `output_data` 物件包含改寫後的 `knn` 查詢：

```json
{
  ...
  "processor_results": [
    {
      "processor_name": "ml_inference",
      "tag": "ml_inference",
      "duration_millis": 442,
      "status": "success",
      "input_data": {
        "ext": {
          "ml_inference": {
            "text": "place where recreational activities are done, picnics happen there"
          }
        },
        "verbose_pipeline": true,
        "query": {
          "match_all": {
            "boost": 1.0
          }
        }
      },
      "output_data": {
        "query": {
          "knn": {
            "multimodal_embedding": {
              "vector": [
                0.035888672,
                0.014221191,
                ...
              ],
              "boost": 1.0,
              "k": 3
            }
          }
        }
      }
    }
  ]
}
```

如需更多資訊，請參閱[偵錯搜尋管線]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/debugging-search-pipeline/)。

### 以影像搜尋

若要以影像搜尋索引，請在 `ext.ml_inference.image` 欄位中提供 Base64 編碼的影像。在下列請求中，Base64 字串已被截斷；請以完整的 Base64 編碼影像取代它：

```json
GET /my-multimodal-index/_search?search_pipeline=multimodal_semantic_search_pipeline
{
  "query": {
    "match_all": {}
  },
  "ext": {
    "ml_inference": {
      "image": "iVBORw0KGgoAAAANSUhEUgAAAFcAAAAdCAYAAADfC/BmAAAAAXNSR0IArs4c6QAAAGJlWElmTU0AKgAAAA..."
    }
  }
}
```
{% include copy-curl.html %}

包含相同影像的 `Times Square` 文件是最接近的比對結果：

```json
{
  "took": 248,
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
    "max_score": 0.7687805,
    "hits": [
      {
        "_index": "my-multimodal-index",
        "_id": "2",
        "_score": 0.7687805,
        "_source": {
          "image": "iVBORw0KGgoAAAANSUhEUgAAAFcAAAAdCAYAAADfC/BmAAAAAXNSR0IArs4c6QAAAGJlWElmTU0AKgAAAA...",
          "multimodal_embedding": [
            0.026977539,
            ...
          ],
          "name": "Times Square",
          "category": "Square"
        }
      },
      {
        "_index": "my-multimodal-index",
        "_id": "1",
        "_score": 0.4280292,
        "_source": {
          "multimodal_embedding": [
            0.01171875,
            ...
          ],
          "name": "Central Park",
          "category": "Park"
        }
      }
    ]
  }
}
```

### 以文字與影像搜尋

若要同時以文字與影像搜尋索引，請同時提供 `text` 與 `image` 欄位：

```json
GET /my-multimodal-index/_search?search_pipeline=multimodal_semantic_search_pipeline
{
  "query": {
    "match_all": {}
  },
  "ext": {
    "ml_inference": {
      "text": "any place in New York",
      "image": "iVBORw0KGgoAAAANSUhEUgAAAFcAAAAdCAYAAADfC/BmAAAAAXNSR0IArs4c6QAAAGJlWElmTU0AKgAAAA..."
    }
  }
}
```
{% include copy-curl.html %}

模型會從文字與影像產生一個嵌入，回應則包含依與該嵌入相似度排序的文件：

```json
{
  "took": 237,
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
    "max_score": 0.89464855,
    "hits": [
      {
        "_index": "my-multimodal-index",
        "_id": "2",
        "_score": 0.89464855,
        "_source": {
          "image": "iVBORw0KGgoAAAANSUhEUgAAAFcAAAAdCAYAAADfC/BmAAAAAXNSR0IArs4c6QAAAGJlWElmTU0AKgAAAA...",
          "multimodal_embedding": [
            0.026977539,
            ...
          ],
          "name": "Times Square",
          "category": "Square"
        }
      },
      {
        "_index": "my-multimodal-index",
        "_id": "1",
        "_score": 0.6142057,
        "_source": {
          "multimodal_embedding": [
            0.01171875,
            ...
          ],
          "name": "Central Park",
          "category": "Park"
        }
      }
    ]
  }
}
```

## 使用 Amazon OpenSearch Service

在 Amazon OpenSearch Service 中，連接器會使用 AWS Identity and Access Management (IAM) 角色來呼叫模型。本教學的步驟 2--5 相同。若要建立連接器，請依照[使用 Amazon Bedrock Titan 的語意搜尋]({{site.url}}{{site.baseurl}}/tutorials/vector-search/semantic-search/semantic-search-bedrock-titan/)的步驟 1--3 操作，並進行下列變更：

- 在呼叫模型之角色的權限中，將資源設定為 `arn:aws:bedrock:*::foundation-model/amazon.titan-embed-image-v1`。
- 在建立連接器的 Python 程式碼中，使用下列連接器承載 (payload)，以 IAM 角色 ARN 取代存取金鑰：

```python
payload = {
  "name": "Amazon Bedrock connector: Titan Multimodal Embeddings",
  "description": "The connector to the Amazon Bedrock Titan Multimodal Embeddings model",
  "version": 1,
  "protocol": "aws_sigv4",
  "credential": {
    "roleArn": "your_iam_role_arn_created_in_step1"
  },
  "parameters": {
    "region": "your_aws_region",
    "service_name": "bedrock",
    "model": "amazon.titan-embed-image-v1"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "headers": {
        "content-type": "application/json"
      },
      "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/invoke",
      "request_body": "{\"inputText\": \"${parameters.inputText:-null}\", \"inputImage\": \"${parameters.inputImage:-null}\"}"
    }
  ]
}
```
{% include copy.html %}

然後依照[步驟 1.2](#step-12-register-and-deploy-the-model)的說明註冊並部署模型。

## 相關文件

- [多模態搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/multimodal-search/)
- [ML 推論處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/ml-inference/)
- [ML 推論搜尋請求處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/ml-inference-search-request/)
- [k-NN 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/k-nn/)
- [第三方 ML 平台的連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)
