---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在管線中存取資料"
nav_order: 20
---

# 在管線中存取資料

在資料匯入管線中，您可以使用 `ctx` 物件來存取文件資料。此物件代表正在處理的文件，並允許您讀取、修改或擴充文件欄位。管線處理器對文件的 `_source` 欄位及其中介資料欄位皆具有讀取和寫入權限。

## 存取文件欄位

`ctx` 物件會公開所有文件欄位。您可以使用點標記法直接存取這些欄位。

### 範例：存取最上層欄位

給定以下範例文件：

```json
{
  "user": "alice"
}
```

您可以如下方式存取 `user`：

```json
"field": "ctx.user"
```

### 範例：存取巢狀欄位

給定以下範例文件：

```json
{
  "user": {
    "name": "alice"
  }
}
```

您可以如下方式存取 `user.name`：

```json
"field": "ctx.user.name"
```

## 存取來源中的欄位

若要存取文件 `_source` 中的欄位，請以欄位名稱來參照該欄位：

```json
{
  "set": {
    "field": "environment",
    "value": "production"
  }
}
```

或者，您也可以明確使用 `_source`：

```json
{
  "set": {
    "field": "_source.environment",
    "value": "production"
  }
}
```

## 存取中介資料欄位

您可以讀取或寫入下列中介資料欄位：

- `_index`
- `_type`
- `_id`
- `_routing`

### 範例：動態設定 `_routing`

```json
{
  "set": {
    "field": "_routing",
    "value": "{% raw %}{{region}}{% endraw %}"
  }
}
```


## 存取匯入中介資料欄位

`_ingest.timestamp` 欄位代表匯入節點收到文件的時間。若要保存此時間戳記，請使用 `set` 處理器：

```json
{
  "set": {
    "field": "received_at",
    "value": "{% raw %}{{_ingest.timestamp}}{% endraw %}"
  }
}
```

## 在 Mustache 範本中使用 `ctx`

使用 Mustache 範本將欄位值插入處理器設定中。使用三個大括號（{% raw %}`{{{` 和 `}}}`{% endraw %}）來表示未逸出的欄位值。

### 範例：合併來源欄位

下列處理器組態會合併 `app` 和 `env` 欄位，並以底線（_）分隔，然後將結果儲存在 `log_label` 欄位中：

```json
{
  "set": {
    "field": "log_label",
    "value": "{% raw %}{{{app}}}_{{{env}}}{% endraw %}"
  }
}
```

### 範例：使用 `set` 處理器產生動態問候語

如果文件的 `user` 欄位設為 `alice`，請使用下列語法來產生結果 `"greeting": "Hello, alice!"`：

```json
{
  "set": {
    "field": "greeting",
    "value": "Hello, {% raw %}{{{user}}}{% endraw %}!"
  }
}
```

## 動態欄位名稱

您可以使用欄位的值作為新欄位的名稱：

```json
{
  "set": {
    "field": "{% raw %}{{service}}{% endraw %}",
    "value": "{% raw %}{{code}}{% endraw %}"
  }
}
```

## 範例：根據狀態路由至動態索引

下列處理器組態會將 `-events` 附加至 `status` 欄位的值，以動態設定目標索引：

```json
{
  "set": {
    "field": "_index",
    "value": "{% raw %}{{status}}{% endraw %}-events"
  }
}
```

## 在 `script` 處理器中使用 `ctx`

使用 `script` 處理器進行進階轉換。

### 範例：僅在另一個欄位缺少時新增欄位

下列處理器僅在文件中缺少該欄位時，新增值為「none」的 `error_message` 欄位：

```json
{
  "script": {
    "lang": "painless",
    "source": "if (ctx.error_message == null) { ctx.error_message = 'none'; }"
  }
}
```

### 範例：將值從一個欄位複製到另一個欄位

下列處理器會將 `timestamp` 欄位的值複製到名為 `event_time` 的新欄位中：

```json
{
  "script": {
    "lang": "painless",
    "source": "ctx.event_time = ctx.timestamp;"
  }
}
```

## 完整管線範例

下列範例定義了一個完整的資料匯入管線，其使用 `source` 欄位設定標語、從 `date` 欄位擷取 `year`，並將文件的匯入時間戳記記錄在 `received_at` 欄位中：

```json
PUT _ingest/pipeline/example-pipeline
{
  "description": "Sets tags, log label, and defaults error message",
  "processors": [
    {
      "set": {
        "field": "tagline",
        "value": "{% raw %}{{{user.first}}} from {{{department}}}{% endraw %}"
      }
    },
    {
      "script": {
        "lang": "painless",
        "source": "ctx.year = ctx.date.substring(0, 4);"
      }
    },
    {
      "set": {
        "field": "received_at",
        "value": "{% raw %}{{_ingest.timestamp}}{% endraw %}"
      }
    }
  ]
}
```

若要測試此管線，請使用下列請求：

```json
POST _ingest/pipeline/example-pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "user": {
          "first": "Liam"
        },
        "department": "Engineering",
        "date": "2024-12-03T14:05:00Z"
      }
    }
  ]
}
```

回應會顯示處理後經過擴充的文件，包括新增的 `tagline`、擷取出的 `year`，以及由資料匯入管線產生的 `received_at` 時間戳記：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "user": {
            "first": "Liam"
          },
          "department": "Engineering",
          "date": "2024-12-03T14:05:00Z",
          "tagline": "Liam from Engineering",
          "year": "2024",
          "received_at": "2025-04-14T18:40:00.000Z"
        },
        "_ingest": {
          "timestamp": "2025-04-14T18:40:00.000Z"
        }
      }
    }
  ]
}
```
