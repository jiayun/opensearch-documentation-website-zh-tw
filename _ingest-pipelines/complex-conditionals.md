---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "複雜條件式"
parent: Conditional execution
nav_order: 50
---

# 複雜條件式

在資料匯入管線中，處理器的 `if` 參數可使用 Painless 指令碼評估複雜條件。這些條件式有助於微調文件處理，可實現型別檢查、正規表達式及合併多項準則等進階邏輯。如需更多資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

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


## 使用正規表達式

Painless 指令碼支援 `=~` 運算子以評估正規表達式。下列管線會標記以 `192.168.` 開頭的可疑 IP 模式：

```json
PUT _ingest/pipeline/flag_suspicious_ips
{
  "processors": [
    {
      "set": {
        "field": "alert",
        "value": "suspicious_ip",
        "if": "ctx.ip != null && ctx.ip =~ /^192\.168\.\d+\.\d+$/"
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

第一份文件會新增 `alert` 欄位：

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

下列管線：

- 若 `env` 欄位尚不存在，則新增設為 `production` 的該欄位。
- 若 `status` 欄位中的值大於或等於 `500`，則新增設為 `major` 的 `severity` 欄位。
- 若 `env` 欄位設為 `test` 且 `message` 欄位包含 `debug`，則捨棄該文件。

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
        "if": "ctx.env == 'test' && ctx.message?.contains('debug')"
      }
    }
  ]
}
```
{% include copy-curl.html %}

使用下列 `_simulate` 請求測試此管線：

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

在回應中，請注意第一份文件新增了 `env: production` 及 `severity: major` 欄位。第二份文件遭到捨棄。第三份文件新增了 `env: production` 欄位：

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

## 空值安全標記法

使用空值安全導覽標記法 (`?.`) 檢查欄位是否為 `null`。請注意，此標記法可能會無訊息地傳回 `null`；因此，我們建議先檢查傳回的值是否為 `null`，再使用 `.contains` 或 `==` 等作業。

不安全的語法：

```
"if": "ctx.message?.contains('debug')"
```

若文件中不存在 `message` 欄位，此請求會傳回 `null_pointer_exception`，並附帶訊息 `Cannot invoke "Object.getClass()" because "value" is null`。

安全的語法：

```
"if": "ctx.message != null && ctx.message.contains('debug')"
```