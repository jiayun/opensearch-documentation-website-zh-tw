---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "模擬管線"
nav_order: 11
redirect_from:
  - /opensearch/rest-api/ingest-apis/simulate-ingest/
  - /api-reference/ingest-apis/simulate-ingest/
---

# 模擬管線
**推出於 1.0**
{: .label .label-purple }

使用模擬資料匯入管線 API 操作來執行或測試管線。

## 端點

下列請求會**模擬最新建立的資料匯入管線**：

```
GET _ingest/pipeline/_simulate
POST _ingest/pipeline/_simulate
```

下列請求會**根據管線 ID 模擬單一管線**：

```
GET _ingest/pipeline/{pipeline-id}/_simulate
POST _ingest/pipeline/{pipeline-id}/_simulate
```

## 請求本文欄位

下表列出用來執行管線的請求本文欄位。

欄位 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`docs` | 必要 | 陣列 | 用來測試管線的文件。
`pipeline` | 選用 | 物件 | 要模擬的管線。若未包含管線識別碼，則回應會模擬最新建立的管線。

`docs` 欄位可包含下表所列的子欄位。

欄位 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`source` | 必要 | 物件 | 文件的 JSON 本文。
`id` | 選用 | 字串 | 唯一的文件識別碼。此識別碼不能在索引中的其他位置使用。
`index` | 選用 | 字串 | 文件轉換後資料所在的索引。

## 查詢參數 

下表列出執行管線的查詢參數。 

參數 | 類型 | 說明
:--- | :--- | :---
`verbose` | 布林值 | 詳細模式。顯示所執行管線中每個處理器的資料輸出。

#### 範例：在路徑中指定管線

```json
POST /_ingest/pipeline/my-pipeline/_simulate
{
  "docs": [
    {
      "_index": "my-index",
      "_id": "1",
      "_source": {
        "grad_year": 2024,
        "graduated": false,
        "name": "John Doe"
      }
    },
    {
      "_index": "my-index",
      "_id": "2",
      "_source": {
        "grad_year": 2025,
        "graduated": false,
        "name": "Jane Doe"
      }
    }
  ]
}
```
{% include copy-curl.html %}

請求會傳回下列回應：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "my-index",
        "_id": "1",
        "_source": {
          "name": "JOHN DOE",
          "grad_year": 2023,
          "graduated": true
        },
        "_ingest": {
          "timestamp": "2023-06-20T23:19:54.635306588Z"
        }
      }
    },
    {
      "doc": {
        "_index": "my-index",
        "_id": "2",
        "_source": {
          "name": "JANE DOE",
          "grad_year": 2023,
          "graduated": true
        },
        "_ingest": {
          "timestamp": "2023-06-20T23:19:54.635746046Z"
        }
      }
    }
  ]
}
```

#### 範例：詳細模式

當先前的請求以 `verbose` 參數設為 `true` 執行時，回應會顯示每份文件的轉換順序。例如，對於 ID 為 `1` 的文件，回應會包含依序套用管線中每個處理器的結果：

```json
{
  "docs": [
    {
      "processor_results": [
        {
          "processor_type": "set",
          "status": "success",
          "description": "Sets the graduation year to 2023",
          "doc": {
            "_index": "my-index",
            "_id": "1",
            "_source": {
              "name": "John Doe",
              "grad_year": 2023,
              "graduated": false
            },
            "_ingest": {
              "pipeline": "my-pipeline",
              "timestamp": "2023-06-20T23:23:26.656564631Z"
            }
          }
        },
        {
          "processor_type": "set",
          "status": "success",
          "description": "Sets 'graduated' to true",
          "doc": {
            "_index": "my-index",
            "_id": "1",
            "_source": {
              "name": "John Doe",
              "grad_year": 2023,
              "graduated": true
            },
            "_ingest": {
              "pipeline": "my-pipeline",
              "timestamp": "2023-06-20T23:23:26.656564631Z"
            }
          }
        },
        {
          "processor_type": "uppercase",
          "status": "success",
          "doc": {
            "_index": "my-index",
            "_id": "1",
            "_source": {
              "name": "JOHN DOE",
              "grad_year": 2023,
              "graduated": true
            },
            "_ingest": {
              "pipeline": "my-pipeline",
              "timestamp": "2023-06-20T23:23:26.656564631Z"
            }
          }
        }
      ]
    }
  ]
}
```

#### 範例：在請求本文中指定管線

或者，您可以直接在請求本文中指定管線，而不必先建立管線：

```json
POST /_ingest/pipeline/_simulate
{
  "pipeline" :
  {
    "description": "Splits text on white space characters",
    "processors": [
      {
        "csv" : {
          "field" : "name",
          "separator": ",",
          "target_fields": ["last_name", "first_name"],
          "trim": true
        }
      },
      {
      "uppercase": {
        "field": "last_name"
      }
    }
    ]
  },
  "docs": [
    {
      "_index": "second-index",
      "_id": "1",
      "_source": {
        "name": "Doe,John"
      }
    },
    {
      "_index": "second-index",
      "_id": "2",
      "_source": {
        "name": "Doe, Jane"
      }
    }
  ]
}
```
{% include copy-curl.html %}

#### 回應

請求會傳回下列回應：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "second-index",
        "_id": "1",
        "_source": {
          "name": "Doe,John",
          "last_name": "DOE",
          "first_name": "John"
        },
        "_ingest": {
          "timestamp": "2023-08-24T19:20:44.816219673Z"
        }
      }
    },
    {
      "doc": {
        "_index": "second-index",
        "_id": "2",
        "_source": {
          "name": "Doe, Jane",
          "last_name": "DOE",
          "first_name": "Jane"
        },
        "_ingest": {
          "timestamp": "2023-08-24T19:20:44.816492381Z"
        }
      }
    }
  ]
}
```
