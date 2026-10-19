---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "模擬管線"
nav_order: 11
redirect_from:
  - /opensearch/rest-api/ingest-apis/simulate-ingest/
  - /api-reference/ingest-apis/simulate-ingest/
---

# Simulate Pipeline API
**1.0 版新增**
{: .label .label-purple }

Simulate Pipeline API 會對一組範例文件執行資料匯入管線，並回應轉換後的文件，而不會將它們編製索引。您可以在將管線套用至資料之前，先用它來測試管線。您可以模擬現有的管線，或在請求本文中提供管線定義。

## 端點

```json
GET  /_ingest/pipeline/_simulate
POST /_ingest/pipeline/_simulate
GET  /_ingest/pipeline/{pipeline-id}/_simulate
POST /_ingest/pipeline/{pipeline-id}/_simulate
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`pipeline-id` | 字串 | 要模擬的現有管線 ID。若未指定，請在 `pipeline` 請求本文欄位中提供管線定義。

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`verbose` | 布林值 | 若為 `true`，回應會包含管線中每個處理器的結果，包括每個處理器執行後的文件。預設值為 `false`。

## 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`docs` | 物件陣列 | 要透過管線執行的文件。必要。
`pipeline` | 物件 | 要模擬的管線定義。包含與 [Create or Update Pipeline API]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#request-body-fields) 請求本文相同的欄位。若路徑中未指定管線 ID，則為必要。

`docs` 陣列中的每個物件包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`_source` | 物件 | 文件的 JSON 本文。必要。
`_id` | 字串 | 文件 ID。處理器可使用 `_id` 中繼資料欄位讀取及修改 ID。選用。
`_index` | 字串 | 索引名稱。處理器可使用 `_index` 中繼資料欄位讀取及修改索引名稱。選用。

## 範例：模擬現有管線

下列請求會讓兩份文件通過在[建立或更新管線 API 範例]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#example-request)中建立的 `my-pipeline` 管線：

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

回應會包含管線處理後的每份文件：

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

## 範例：檢視每個處理器的結果

若要檢視每個處理器執行後的文件，請將 `verbose` 查詢參數設定為 `true`：

```json
POST /_ingest/pipeline/my-pipeline/_simulate?verbose=true
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
    }
  ]
}
```
{% include copy-curl.html %}

回應包含管線中依序套用每個處理器的結果：

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
          "description": "Sets graduated to true",
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

## 範例：模擬請求本文中定義的管線

若要在不建立管線的情況下測試管線，請在請求本文中提供管線定義：

```json
POST /_ingest/pipeline/_simulate
{
  "pipeline" :
  {
    "description": "Splits comma-separated text into fields",
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

此請求會傳回下列回應：

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

## 回應本文欄位

回應包含 `docs` 陣列，請求中的每份文件各有一個對應物件，順序與請求相同。如果處理器捨棄了文件，陣列中該文件的位置會包含 `null`。陣列中的每個物件都包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`doc` | 物件 | 管線處理後的文件，包含其 `_index`、`_id`、`_source` 和 `_ingest` 中繼資料。當 `verbose` 為 `false` 且文件處理成功時傳回。
`error` | 物件 | 導致管線處理此文件失敗的錯誤。處理失敗時傳回。在此情況下，不會傳回 `doc`。
`processor_results` | 物件陣列 | 每個處理器的結果，依處理器執行的順序排列。僅當 `verbose` 為 `true` 時傳回。

`processor_results` 陣列中的每個物件都包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`processor_type` | 字串 | 處理器類型，例如 `set`。
`status` | 字串 | 處理器結果。有效值為 `success`、`error`（處理器失敗；如果已定義 `on_failure`，則後面會接著列出 `on_failure` 處理器的結果）、`error_ignored`（處理器失敗，且 `ignore_failure` 為 `true`）、`skipped`（處理器的 `if` 條件傳回 `false`）和 `dropped`（處理器捨棄了文件）。
`description` | 字串 | 處理器說明。僅當處理器有說明時傳回。
`tag` | 字串 | 處理器標籤。僅當處理器有標籤時傳回。
`if` | 物件 | 處理器的 `if` 條件（`condition`）及其結果（`result`）。僅當處理器有條件時傳回。
`doc` | 物件 | 此處理器執行後的文件。
`error` | 物件 | 處理器傳回的錯誤。狀態為 `error` 時傳回。
`ignored_error` | 物件 | 處理器忽略的錯誤。狀態為 `error_ignored` 時傳回。

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:admin/ingest/pipeline/simulate`。
