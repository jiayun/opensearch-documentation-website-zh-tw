---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "條件式執行"
has_children: true
nav_order: 40
---

# 條件式執行

在資料匯入管線中，您可以使用選用的 `if` 參數來控制處理器是否執行。這可讓處理器根據傳入文件的內容進行條件式執行。條件以 Painless 指令碼撰寫，並根據文件上下文（`ctx`）進行評估。如需更多資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

## 基本條件執行

每個處理器都可以包含一個 `if` 子句。如果條件評估為 `true`，則執行該處理器；否則會略過。

在條件中，`ctx` 是唯讀的。條件可以讀取文件欄位，但無法新增、變更或移除欄位。若要有條件地修改文件，請將修改動作放在處理器中，並僅使用條件來決定是否執行該處理器。

### 範例：捨棄偵錯層級的記錄檔

下列管線會捨棄 `log_level` 欄位等於 `debug` 的所有文件：

```json
PUT _ingest/pipeline/drop_debug_logs
{
  "processors": [
    {
      "drop": {
        "if": "ctx.log_level == 'debug'"
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 索引請求範例

```json
POST logs/_doc/1?pipeline=drop_debug_logs
{
  "message": "User logged in",
  "log_level": "debug"
}
```
{% include copy-curl.html %}

由於條件評估為 `true`，此文件會被捨棄：

```json
{
  "_index": "logs",
  "_id": "1",
  "_version": -3,
  "result": "noop",
  "_shards": {
    "total": 0,
    "successful": 0,
    "failed": 0
  }
}
```

## 使用巢狀欄位時的 Null 安全欄位檢查

處理巢狀欄位時，務必避免 null 指標例外。請在 Painless 指令碼中使用 null 安全的 `?.` 運算子。

### 範例：根據巢狀欄位捨棄文件

下列 drop 處理器只有在巢狀 `app.env` 欄位存在且等於 `debug` 時才會執行：

```json
PUT _ingest/pipeline/drop_debug_env
{
  "processors": [
    {
      "drop": {
        "if": "ctx.app?.env == 'debug'"
      }
    }
  ]
}
```
{% include copy-curl.html %}

若未設定可安全處理 null 的 `?.` 運算子，則對任何不含 `app` 物件的文件編製索引時，會觸發下列空指標例外：

```json
{
  "error": "IngestProcessorException[ScriptException[runtime error]; nested: NullPointerException[Cannot invoke \"Object.getClass()\" because \"callArgs[0]\" is null];]",
  "status": 400
}
```

## 處理扁平化欄位

如果您的文件有扁平化欄位，例如 `"app.env": "debug"`，請使用 [`dot_expander`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/dot-expander/) 處理器將其轉換為巢狀結構：

```json
PUT _ingest/pipeline/drop_debug_env
{
  "processors": [
    {
      "dot_expander": {
        "field": "app.env"
      }
    },
    {
      "drop": {
        "if": "ctx.app?.env == 'debug'"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 條件中的安全方法呼叫

如果物件為 `null`，`?.` 運算子會傳回 `null`，而 `==` 運算子會處理 `null` 值，因此 `ctx.app?.env == 'debug'` 這類條件可安全處理 null。然而，對 `null` 值呼叫方法會導致空指標例外。例如，對於不包含 `app.env` 欄位的文件，`ctx.app?.env.equalsIgnoreCase('debug')` 會失敗，因為 `ctx.app?.env` 會傳回 `null`。

若要讓方法呼叫可安全處理 null，請對絕不會是 `null` 的常數呼叫方法，並將欄位作為引數傳入：

```json
{
  "drop": {
    "if": "'debug'.equalsIgnoreCase(ctx.app?.env)"
  }
}
```

如果無法對常數呼叫任何方法，請在呼叫方法之前明確檢查是否為 `null`：

```json
{
  "drop": {
    "if": "ctx.app?.env != null && ctx.app.env.contains('debug')"
  }
}
```

## 完整範例：多步驟條件管線

下列資料匯入管線使用三個處理器：

1. `set`：如果 `user` 欄位未提供值，則將 `user` 欄位設為 `guest`。
2. `set`：如果提供了 `status_code` 且大於或等於 `400`，則將 `error` 欄位設為 `true`。
3. `drop`：如果 `app.env` 欄位等於 `debug`，則捨棄整份文件。

```json
PUT _ingest/pipeline/logs_processing
{
  "processors": [
    {
      "set": {
        "field": "user",
        "value": "guest",
        "if": "ctx.user == null"
      }
    },
    {
      "set": {
        "field": "error",
        "value": true,
        "if": "ctx.status_code != null && ctx.status_code >= 400"
      }
    },
    {
      "drop": {
        "if": "ctx.app?.env == 'debug'"
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 模擬管線

下列模擬請求對三份文件套用條件式邏輯：

```json
POST _ingest/pipeline/logs_processing/_simulate
{
  "docs": [
    {
      "_source": {
        "message": "Successful login",
        "status_code": 200
      }
    },
    {
      "_source": {
        "message": "Database error",
        "status_code": 500,
        "user": "alice"
      }
    },
    {
      "_source": {
        "message": "Debug mode trace",
        "app": { "env": "debug" }
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應示範了處理器如何根據各項條件做出回應：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "status_code": 200,
          "message": "Successful login",
          "user": "guest"
        },
        "_ingest": {
          "timestamp": "2025-04-16T14:04:35.923159885Z"
        }
      }
    },
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "status_code": 500,
          "message": "Database error",
          "error": true,
          "user": "alice"
        },
        "_ingest": {
          "timestamp": "2025-04-16T14:04:35.923198551Z"
        }
      }
    },
    null
  ]
}
```


