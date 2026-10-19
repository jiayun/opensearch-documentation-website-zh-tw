---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用管線處理器的條件式"
parent: Conditional execution
nav_order: 60
---

# 使用管線處理器的條件式

資料匯入管線中的 `pipeline` 處理器可根據文件內容，有條件地執行不同的子管線。當不同類型的文件需要各自的處理邏輯時，這提供了強大的彈性。您可以在 `pipeline` 處理器中使用 `if` 參數，根據欄位值、資料類型或內容結構，將文件導向不同的管線。接著，每個管線都能獨立套用自己的一組處理器。這種做法只在相關的地方套用邏輯，讓管線保持模組化且易於維護。

## 範例：依服務路由記錄檔

以下範例示範如何根據文件中的 `service.name` 欄位，將記錄檔路由到不同的子管線。

建立名為 `webapp_logs` 的第一個管線：

```json
PUT _ingest/pipeline/webapp_logs
{
  "processors": [
    { "set": { "field": "log_type", "value": "webapp" } }
  ]
}
```
{% include copy-curl.html %}

建立名為 `api_logs` 的第二個管線：

```json
PUT _ingest/pipeline/api_logs
{
  "processors": [
    { "set": { "field": "log_type", "value": "api" } }
  ]
}
```
{% include copy-curl.html %}

建立名為 `service_router` 的主要路由管線，它會根據 `service.name` 將文件路由到對應的管線：

```json
PUT _ingest/pipeline/service_router
{
  "processors": [
    {
      "pipeline": {
        "name": "webapp_logs",
        "if": "ctx.service?.name == 'webapp'"
      }
    },
    {
      "pipeline": {
        "name": "api_logs",
        "if": "ctx.service?.name == 'api'"
      }
    }
  ]
}
```
{% include copy-curl.html %}

使用下列請求來模擬這些管線：

```json
POST _ingest/pipeline/service_router/_simulate
{
  "docs": [
    { "_source": { "service": { "name": "webapp" }, "message": "Homepage loaded" } },
    { "_source": { "service": { "name": "api" }, "message": "GET /v1/users" } },
    { "_source": { "service": { "name": "worker" }, "message": "Task started" } }
  ]
}
```
{% include copy-curl.html %}

回應確認第一份文件是由 `webapp_logs` 管線處理，第二份文件是由 `api_logs` 管線處理。第三份文件則保持不變，因為它不符合任何條件：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "log_type": "webapp",
          "message": "Homepage loaded",
          "service": {
            "name": "webapp"
          }
        },
        "_ingest": {
          "timestamp": "2025-04-24T10:54:12.555447087Z"
        }
      }
    },
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "log_type": "api",
          "message": "GET /v1/users",
          "service": {
            "name": "api"
          }
        },
        "_ingest": {
          "timestamp": "2025-04-24T10:54:12.55548442Z"
        }
      }
    },
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "message": "Task started",
          "service": {
            "name": "worker"
          }
        },
        "_ingest": {
          "timestamp": "2025-04-24T10:54:12.555490754Z"
        }
      }
    }
  ]
}
```

### 拒絕未符合條件的文件

在前面的範例中，未符合任何條件的文件會在不經處理的情況下編製索引。若要拒絕這些文件，請新增一個 [`fail` 處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/fail/)，其條件會在其他條件皆未符合時成立：

```json
PUT _ingest/pipeline/service_router
{
  "processors": [
    {
      "pipeline": {
        "name": "webapp_logs",
        "if": "ctx.service?.name == 'webapp'"
      }
    },
    {
      "pipeline": {
        "name": "api_logs",
        "if": "ctx.service?.name == 'api'"
      }
    },
    {
      "fail": {
        "if": "!['webapp', 'api'].contains(ctx.service?.name)",
        "message": "The service.name field must be webapp or api. Received: {% raw %}{{service.name}}{% endraw %}"
      }
    }
  ]
}
```
{% include copy-curl.html %}

當您使用與前面範例相同的文件模擬管線時，前兩份文件會如先前一樣處理。第三份文件會失敗並顯示訊息 `The service.name field must be webapp or api. Received: worker`，且 OpenSearch 不會將其編製索引。若文件沒有 `service.name` 欄位，訊息結尾會是空值。

### 將路由器套用至所有編製索引的請求

若要將每個編製索引至索引的文件進行路由，而不用在每個請求中指定 `pipeline` 參數，請將該管線設為索引的預設管線。若要將它套用至所有符合某模式的索引，請在[索引範本]({{site.url}}{{site.baseurl}}/im-plugin/index-templates/)中設定 `index.default_pipeline`：

```json
PUT _index_template/service_logs
{
  "index_patterns": ["service-logs-*"],
  "template": {
    "settings": {
      "index.default_pipeline": "service_router"
    }
  }
}
```
{% include copy-curl.html %}

如需更多資訊，請參閱[將管線套用至文件]({{site.url}}{{site.baseurl}}/ingest-pipelines/#applying-a-pipeline-to-documents)。

## 範例：依類型處理

您也可以使用管線處理器來套用依類型區分的管線。下列管線會在 `code` 欄位是數字時，將記錄檔導向 `numeric_handler`；若該欄位為 `String` 類型，則導向 `string_handler`。

建立名為 `numeric_handler` 的第一個管線：

```json
PUT _ingest/pipeline/numeric_handler
{
  "processors": [
    { "set": { "field": "code_type", "value": "numeric" } }
  ]
}
```
{% include copy-curl.html %}

建立名為 `string_handler` 的第二個管線：

```json
PUT _ingest/pipeline/string_handler
{
  "processors": [
    { "set": { "field": "code_type", "value": "string" } }
  ]
}
```
{% include copy-curl.html %}

建立名為 `type_router` 的主要路由管線，它會根據 `code` 欄位將文件路由到對應的管線：

```json
PUT _ingest/pipeline/type_router
{
  "processors": [
    {
      "pipeline": {
        "name": "numeric_handler",
        "if": "ctx.code instanceof Integer || ctx.code instanceof Long || ctx.code instanceof Double"
      }
    },
    {
      "pipeline": {
        "name": "string_handler",
        "if": "ctx.code instanceof String"
      }
    }
  ]
}
```
{% include copy-curl.html %}

使用下列請求來模擬這些管線：

```json
POST _ingest/pipeline/type_router/_simulate
{
  "docs": [
    { "_source": { "code": 404 } },
    { "_source": { "code": "ERR_NOT_FOUND" } }
  ]
}
```
{% include copy-curl.html %}

傳回的文件含有由個別子管線新增的 `code_type` 欄位：

```json
{
  "docs": [
    {
      "doc": {
        "_source": {
          "code": 404,
          "code_type": "numeric"
        }
      }
    },
    {
      "doc": {
        "_source": {
          "code": "ERR_NOT_FOUND",
          "code_type": "string"
        }
      }
    }
  ]
}
```