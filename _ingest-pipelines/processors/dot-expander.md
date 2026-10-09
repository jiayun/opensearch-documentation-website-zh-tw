---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "點號展開器"
parent: Ingest processors
nav_order: 65
---

# 點號展開器

`dot_expander` 處理器是一項工具，可協助您處理階層式資料。它會將包含點號的欄位轉換為物件欄位，使其可供管線中的其他處理器存取。若沒有這項轉換，包含點號的欄位將無法被處理。

以下是 `dot_expander` 處理器的語法：

```json
{
  "dot_expander": {
    "field": "field.to.expand" 
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `dot_expander` 處理器的必要與選用參數。

參數 | 必要/選用 | 說明 |
|-----------|-----------|-----------|
`field`  | 必要  | 要展開為物件欄位的欄位。 |
`path` | 選用 | 只有在要展開的欄位巢狀地位於另一個物件欄位內時，才需要此欄位。這是因為 `field` 參數只會辨識葉節點欄位。 |
`description`  | 選用  | 處理器的簡短說明。 |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 若設為 `true`，則會忽略失敗。預設為 `false`。 |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別碼標籤。有助於偵錯，以區分相同類型的處理器。 |

## 使用處理器

請依照下列步驟在管線中使用處理器。

### 步驟 1：建立管線
 
下列查詢會建立 `dot_expander` 處理器，將名為 `user.address.city` 和 `user.address.state` 的兩個欄位展開為巢狀物件：

```json
PUT /_ingest/pipeline/dot-expander-pipeline
{
  "description": "Dot expander processor",
  "processors": [
    {
      "dot_expander": {
        "field": "user.address.city"
      }
    },
    {
      "dot_expander":{
       "field": "user.address.state"
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 2 (選用)：測試管線

建議您在匯入文件之前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/dot-expander-pipeline/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "user.address.city": "New York",
        "user.address.state": "NY"
      }
    }
  ]
}
```
{% include copy-curl.html %}

#### 回應

下列範例回應確認管線運作正常：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "user": {
            "address": {
              "city": "New York",
              "state": "NY"
            }
          }
        },
        "_ingest": {
          "timestamp": "2024-01-17T01:32:56.501346717Z"
        }
      }
    }
  ]
}
```

### 步驟 3：匯入文件

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=dot-expander-pipeline
{
  "user.address.city": "Denver",
  "user.address.state": "CO"
}
```
{% include copy-curl.html %}

### 步驟 4 (選用)：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

#### 回應

下列回應確認指定的欄位已展開為巢狀欄位：

```json
{
  "_index": "testindex1",
  "_id": "1",
  "_version": 1,
  "_seq_no": 3,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "user": {
      "address": {
        "city": "Denver",
        "state": "CO"
      }
    }
  }
}
```

## `path` 參數

您可以使用 `path` 參數來指定物件內含點號欄位的路徑。例如，下列管線會指定位於 `user` 物件內的 `address.city` 欄位：

```json
PUT /_ingest/pipeline/dot-expander-pipeline
{
  "description": "Dot expander processor",
  "processors": [
    {
      "dot_expander": {
        "field": "address.city",
        "path": "user"
      }
    },
    {
      "dot_expander":{
       "field": "address.state",
       "path": "user"
      }
    }
  ]
}
```
{% include copy-curl.html %}

您可以如下模擬管線：

```json
POST _ingest/pipeline/dot-expander-pipeline/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "user": {
          "address.city": "New York",
          "address.state": "NY"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

`dot_expander` 處理器會將文件轉換為下列結構：

```json
{
  "user": {
    "address": {
      "city": "New York",
      "state": "NY"
    }
  }
}
```

## 欄位名稱衝突

如果某個欄位已存在，且其路徑與 `dot_expander` 處理器應展開值的目的路徑相同，則處理器會將這兩個值合併為陣列。

請考慮下列會展開 `user.name` 欄位的管線：

```json
PUT /_ingest/pipeline/dot-expander-pipeline
{
  "description": "Dot expander processor",
  "processors": [
    {
      "dot_expander": {
        "field": "user.name"
      }
    }
  ]
}
```
{% include copy-curl.html %}

您可以使用包含兩個路徑完全相同 `user.name` 之值的文件來模擬管線：

```json
POST _ingest/pipeline/dot-expander-pipeline/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "user.name": "John", 
        "user": {
          "name": "Steve"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應確認這些值已合併為陣列：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "user": {
            "name": [
              "Steve",
              "John"
            ]
          }
        },
        "_ingest": {
          "timestamp": "2024-01-17T01:44:57.420220551Z"
        }
      }
    }
  ]
}
```

如果欄位包含相同名稱但路徑不同，則需要重新命名該欄位。例如，下列 `_simulate` 呼叫會傳回剖析例外狀況：

```json
POST _ingest/pipeline/dot-expander-pipeline/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "user": "John",
        "user.name": "Steve"
      }
    }
  ]
}
```

若要避免剖析例外狀況，請先使用 `rename` 處理器重新命名欄位：

```json
PUT /_ingest/pipeline/dot-expander-pipeline
{
  "processors" : [
    {
      "rename" : {
        "field" : "user",
        "target_field" : "user.name"
      }
    },
    {
      "dot_expander": {
        "field": "user.name"
      }
    }
  ]
}
```
{% include copy-curl.html %}

現在您可以模擬管線：

```json
POST _ingest/pipeline/dot-expander-pipeline/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "user": "John",
        "user.name": "Steve"
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應確認這些欄位已合併：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "user": {
            "name": [
              "John",
              "Steve"
            ]
          }
        },
        "_ingest": {
          "timestamp": "2024-01-17T01:52:12.864432419Z"
        }
      }
    }
  ]
}
```
