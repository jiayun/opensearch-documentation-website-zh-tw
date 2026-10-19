---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "複雜條件式"
parent: Conditional execution
nav_order: 50
---

# 複雜條件

在資料匯入管線中，處理器的 `if` 參數可以使用 Painless 指令碼評估複雜條件。這些條件有助於微調文件處理，允許型別檢查、正規表示式及結合多項準則等進階邏輯。如需詳細資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

OpenSearch 會針對通過處理器的每份文件評估條件，因此成本高昂的條件會拖慢匯入速度。請盡可能保持條件簡單。
{: .tip}

## 撰寫多重陳述式條件

條件可以包含多個 Painless 陳述式，例如變數宣告與迴圈，只要其回傳布林值即可。由於 JSON 字串無法包含換行符號，請將整個指令碼寫在同一行，並使用分號分隔各陳述式。在 OpenSearch Dashboards 的 Dev Tools 中，您也可以改用三引號（`"""`）包住多行指令碼。如需更多資訊，請參閱[在查詢中使用三引號]({{site.url}}{{site.baseurl}}/dashboards/dev-tools/console/#using-triple-quotation-marks-in-queries)。

下列管線會從訂單的 `items` 陣列計算訂單總金額，並標記總金額超過 `1000` 的訂單以供審核。沒有 `items` 欄位的訂單不會被標記：

```json
PUT _ingest/pipeline/flag_large_orders
{
  "processors": [
    {
      "set": {
        "field": "review_required",
        "value": true,
        "if": "if (ctx.items == null) { return false; } double total = 0; for (def item : ctx.items) { total += item.price * item.quantity; } return total > 1000;"
      }
    }
  ]
}
```
{% include copy-curl.html %}

使用下列 `_simulate` 請求測試此管線：

```json
POST _ingest/pipeline/flag_large_orders/_simulate
{
  "docs": [
    {
      "_source": {
        "order_id": "A-2001",
        "items": [
          { "name": "Laptop stand", "price": 45.0, "quantity": 2 },
          { "name": "Monitor", "price": 329.0, "quantity": 1 }
        ]
      }
    },
    {
      "_source": {
        "order_id": "A-2002",
        "items": [
          { "name": "Monitor", "price": 329.0, "quantity": 4 }
        ]
      }
    }
  ]
}
```
{% include copy-curl.html %}

第一筆訂單總金額為 `419`，不會被標記。第二筆訂單總金額為 `1316`，因此會新增 `review_required` 欄位：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "order_id": "A-2001",
          "items": [
            { "name": "Laptop stand", "price": 45.0, "quantity": 2 },
            { "name": "Monitor", "price": 329.0, "quantity": 1 }
          ]
        },
        "_ingest": {
          "timestamp": "2026-10-14T20:23:18.723081887Z"
        }
      }
    },
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "review_required": true,
          "order_id": "A-2002",
          "items": [
            { "name": "Monitor", "price": 329.0, "quantity": 4 }
          ]
        },
        "_ingest": {
          "timestamp": "2026-10-14T20:23:18.723092429Z"
        }
      }
    }
  ]
}
```

## 多條件檢查

您可以合併 `&&` (and)、`||` (or) 及 `!` (not) 等邏輯運算子，建構更複雜的條件。下列管線會將文件標記為 `spam`，並在文件包含高於 `1000` 的 `error_code` 時予以捨棄：

```json
PUT _ingest/pipeline/spammy_error_handler
{
  "processors": [
    {
      "set": {
        "field": "tags",
        "value": ["spam"],
        "if": "ctx.message != null && ctx.message.contains('OutOfMemoryError')"
      }
    },
    {
      "drop": {
        "if": "ctx.tags != null && ctx.tags.contains('spam') && ctx.error_code != null && ctx.error_code > 1000"
      }
    }
  ]
}
```
{% include copy-curl.html %}

您可以使用下列 `_simulate` 請求測試此管線：

```json
POST _ingest/pipeline/spammy_error_handler/_simulate
{
  "docs": [
    { "_source": { "message": "OutOfMemoryError occurred", "error_code": 1200 } },
    { "_source": { "message": "OutOfMemoryError occurred", "error_code": 800 } },
    { "_source": { "message": "All good", "error_code": 200 } }
  ]
}
```
{% include copy-curl.html %}

第一份文件會遭到捨棄，因為它包含 `OutOfMemoryError` 字串及高於 `1000` 的 `error_code`：

```json
{
  "docs": [
    null,
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "error_code": 800,
          "message": "OutOfMemoryError occurred",
          "tags": [
            "spam"
          ]
        },
        "_ingest": {
          "timestamp": "2025-04-23T10:20:10.704359884Z"
        }
      }
    },
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "error_code": 200,
          "message": "All good"
        },
        "_ingest": {
          "timestamp": "2025-04-23T10:20:10.704369801Z"
        }
      }
    }
  ]
}
```

## 型別安全評估

使用 `instanceof` 以確保在執行作業前使用正確的資料類型。下列管線設定為僅在 `message` 為 `String` 類型且長度超過 `10` 個字元時，新增設為 `true` 的 `processed` 欄位：

```json
PUT _ingest/pipeline/string_message_check
{
  "processors": [
    {
      "set": {
        "field": "processed",
        "value": true,
        "if": "ctx.message != null && ctx.message instanceof String && ctx.message.length() > 10"
      }
    }
  ]
}
```
{% include copy-curl.html %}

使用下列 `_simulate` 請求測試此管線：

```json
POST _ingest/pipeline/string_message_check/_simulate
{
  "docs": [
    { "_source": { "message": "short" } },
    { "_source": { "message": "This is a longer message" } },
    { "_source": { "message": 1234567890 } }
  ]
}
```
{% include copy-curl.html %}

只有第二份文件會新增欄位：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "message": "short"
        },
        "_ingest": {
          "timestamp": "2025-04-23T10:28:14.040115261Z"
        }
      }
    },
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "processed": true,
          "message": "This is a longer message"
        },
        "_ingest": {
          "timestamp": "2025-04-23T10:28:14.040141469Z"
        }
      }
    },
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "message": 1234567890
        },
        "_ingest": {
          "timestamp": "2025-04-23T10:28:14.040144844Z"
        }
      }
    }
  ]
}
```


## 使用正規表示式

Painless 指令碼支援 `=~` 運算子來評估正規表示式。如需更多範例以及正規表示式的限制，請參閱[正規表示式條件式]({{site.url}}{{site.baseurl}}/ingest-pipelines/regex-conditionals/)。下列管線會標記以 `192.168.` 開頭的可疑 IP 模式：

```json
PUT _ingest/pipeline/flag_suspicious_ips
{
  "processors": [
    {
      "set": {
        "field": "alert",
        "value": "suspicious_ip",
        "if": "ctx.ip != null && ctx.ip =~ /^192\\.168\\.\\d+\\.\\d+$/"
      }
    }
  ]
}
```
{% include copy-curl.html %}

使用下列 `_simulate` 請求測試此管線：

```json
POST _ingest/pipeline/flag_suspicious_ips/_simulate
{
  "docs": [
    { "_source": { "ip": "192.168.0.1" } },
    { "_source": { "ip": "10.0.0.1" } }
  ]
}
```
{% include copy-curl.html %}

第一份文件新增了 `alert` 欄位：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "alert": "suspicious_ip",
          "ip": "192.168.0.1"
        },
        "_ingest": {
          "timestamp": "2025-04-23T10:32:45.367916428Z"
        }
      }
    },
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "ip": "10.0.0.1"
        },
        "_ingest": {
          "timestamp": "2025-04-23T10:32:45.36793772Z"
        }
      }
    }
  ]
}
```

## 合併欄位與空值檢查

下列管線會在 `level` 為 `critical` 且提供 `timestamp` 時，新增設為 `high` 的 `priority` 欄位。此指令碼也會確保所有欄位皆存在並符合特定條件後才繼續：

```json
PUT _ingest/pipeline/critical_log_handler
{
  "processors": [
    {
      "set": {
        "field": "priority",
        "value": "high",
        "if": "ctx.level != null && ctx.level == 'critical' && ctx.timestamp != null"
      }
    }
  ]
}
```
{% include copy-curl.html %}

使用下列 `_simulate` 請求測試此管線：

```json
POST _ingest/pipeline/critical_log_handler/_simulate
{
  "docs": [
    { "_source": { "level": "critical", "timestamp": "2025-04-01T00:00:00Z" } },
    { "_source": { "level": "info", "timestamp": "2025-04-01T00:00:00Z" } },
    { "_source": { "level": "critical" } }
  ]
}
```
{% include copy-curl.html %}

只有第一份文件會新增 `priority` 欄位：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "priority": "high",
          "level": "critical",
          "timestamp": "2025-04-01T00:00:00Z"
        },
        "_ingest": {
          "timestamp": "2025-04-23T10:39:25.46840371Z"
        }
      }
    },
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "level": "info",
          "timestamp": "2025-04-01T00:00:00Z"
        },
        "_ingest": {
          "timestamp": "2025-04-23T10:39:25.46843021Z"
        }
      }
    },
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "level": "critical"
        },
        "_ingest": {
          "timestamp": "2025-04-23T10:39:25.468434835Z"
        }
      }
    }
  ]
}
```

## 多條件處理

下列管線會：

- 若 `env` 欄位尚不存在，則新增該欄位並將其設為 `production`。
- 若 `status` 欄位中的值大於或等於 `500`，則新增 `severity` 欄位並將其設為 `major`。
- 若 `env` 欄位設為 `test`，且 `message` 欄位包含 `debug`，則捨棄該文件。

```json
PUT _ingest/pipeline/advanced_log_pipeline
{
  "processors": [
    {
      "set": {
        "field": "env",
        "value": "production",
        "if": "!ctx.containsKey('env')"
      }
    },
    {
      "set": {
        "field": "severity",
        "value": "major",
        "if": "ctx.status != null && ctx.status >= 500"
      }
    },
    {
      "drop": {
        "if": "ctx.env == 'test' && ctx.message != null && ctx.message.contains('debug')"
      }
    }
  ]
}
```
{% include copy-curl.html %}

使用下列 `_simulate` 請求來測試管線：

```json
POST _ingest/pipeline/advanced_log_pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "status": 503,
        "message": "Server unavailable"
      }
    },
    {
      "_source": {
        "env": "test",
        "message": "debug log output"
      }
    },
    {
      "_source": {
        "status": 200,
        "message": "OK"
      }
    }
  ]
}
```
{% include copy-curl.html %}

在回應中，請注意第一份文件新增了 `env: production` 和 `severity: major` 欄位。第二份文件已被捨棄。第三份文件新增了 `env: production` 欄位：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "severity": "major",
          "message": "Server unavailable",
          "env": "production",
          "status": 503
        },
        "_ingest": {
          "timestamp": "2025-04-23T10:51:46.795026554Z"
        }
      }
    },
    null,
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "message": "OK",
          "env": "production",
          "status": 200
        },
        "_ingest": {
          "timestamp": "2025-04-23T10:51:46.795048304Z"
        }
      }
    }
  ]
}
```

## 空值安全表示法

使用空值安全巡覽表示法（`?.`）來檢查欄位是否為 `null`。請注意，此表示法可能會無聲地傳回 `null`；因此，建議先檢查傳回的值是否為 `null`，然後再使用 `.contains` 或 `==` 等運算。

不安全的語法：

```
"if": "ctx.message?.contains('debug')"
```

如果文件中不存在 `message` 欄位，此請求會傳回 `null_pointer_exception`，並附帶訊息 `Cannot invoke "Object.getClass()" because "value" is null`。

安全的語法：

```
"if": "ctx.message != null && ctx.message.contains('debug')"
```

## 偵錯條件

若要檢查每個條件是如何評估的，請執行 [Simulate Pipeline API]({{site.url}}{{site.baseurl}}/ingest-pipelines/simulate-ingest/)，並將 `verbose` 參數設為 `true`。對每個處理器而言，回應中會包含 `status` 欄位。若處理器的條件評估為 `false`，則 `status` 為 `skipped`，且 `if` 物件會顯示該條件及其結果。

下列請求會模擬一個處理器，其條件對所提供的文件評估為 `false`：

```json
POST _ingest/pipeline/_simulate?verbose=true
{
  "pipeline": {
    "processors": [
      {
        "set": {
          "field": "severity",
          "value": "major",
          "if": "ctx.status != null && ctx.status >= 500"
        }
      }
    ]
  },
  "docs": [
    { "_source": { "status": 200 } }
  ]
}
```
{% include copy-curl.html %}

回應顯示 `set` 處理器遭到略過，因為條件傳回 `false`：

```json
{
  "docs": [
    {
      "processor_results": [
        {
          "processor_type": "set",
          "status": "skipped",
          "if": {
            "condition": "ctx.status != null && ctx.status >= 500",
            "result": false
          }
        }
      ]
    }
  ]
}
```
