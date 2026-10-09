---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "條件式執行"
has_children: true
nav_order: 40
---

# 條件式執行

在資料匯入管線中，您可以使用選用的 `if` 參數來控制處理器是否執行。這可讓處理器根據傳入文件的內容進行條件式執行。條件以 Painless 指令碼撰寫，並根據文件上下文（`ctx`）進行評估。如需更多資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

## 基本條件式執行

每個處理器都可以包含 `if` 子句。如果條件評估為 `true`，處理器就會執行；否則會被略過。

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

如果未設定 null 安全的 `?.` 運算子，對任何不含 `app.env` 欄位的文件編製索引時，將會觸發下列 null 指標例外：

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

避免在可能為 null 的值上呼叫方法。請改用常數或 null 檢查：

```json
{
  "drop": {
    "if": "ctx.app?.env != null && ctx.app.env.contains('debug')"
  }
}
```

## 完整範例：多步驟條件式管線

下列資料匯入管線使用三個處理器：

1. `set`：如果 `user` 欄位未提供值，則將 `user` 欄位設為 `guest`。
2. `set`：如果提供了 `status_code` 且高於 `400`，則將 `error` 欄位設為 `true`。
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


