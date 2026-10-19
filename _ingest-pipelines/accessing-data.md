---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在管線中存取資料"
nav_order: 20
---

# 在管線中存取資料

管線處理器對文件的 `_source` 欄位及其中繼資料欄位皆具有讀取與寫入權限。您如何參照欄位取決於參照的位置：

- 在處理器參數（例如 `field` 和 `target_field`）中，請使用欄位名稱。
- 在 [`script` 處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/script/) 和 `if` 條件中，請使用 `ctx` 物件，該物件代表正在處理的文件，例如 `ctx.user`。

## 存取文件欄位

在處理器參數中，請以名稱參照頂層欄位。請使用點標記法參照巢狀欄位。

### 範例：存取頂層欄位

假設有下列範例文件：

```json
{
  "user": "alice"
}
```

您可以依照下列方式存取 `user`：

```json
"field": "user"
```

在指令碼或條件中，請使用 `ctx.user`。

### 範例：存取巢狀欄位

給定以下範例文件：

```json
{
  "user": {
    "name": "alice"
  }
}
```

您可以如下所示存取 `user.name`：

```json
"field": "user.name"
```

在指令碼或條件中，請使用 `ctx.user.name`。如果 `user` 物件可能不存在，請使用空值安全運算子：`ctx.user?.name`。

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

## 存取中繼資料欄位

文件的 `_source` 不能包含名稱與中繼資料欄位相同的欄位，因此您可以像參照來源欄位一樣，直接以名稱參照中繼資料欄位。處理器可以讀取和寫入下列中繼資料欄位：

- `_index`
- `_id`
- `_routing`
- `_version`
- `_version_type`
- `_if_seq_no`
- `_if_primary_term`

### 範例：動態設定 `_routing`

```json
{
  "set": {
    "field": "_routing",
    "value": "{% raw %}{{region}}{% endraw %}"
  }
}
```


## 存取匯入中繼資料欄位

`_ingest.timestamp` 欄位代表匯入節點收到文件的時間。若要保存此時間戳記，請使用 `set` 處理器：

```json
{
  "set": {
    "field": "received_at",
    "value": "{% raw %}{{_ingest.timestamp}}{% endraw %}"
  }
}
```

匯入中繼資料僅在管線處理文件期間存在。OpenSearch 不會將 `_ingest` 欄位編製索引，因此若要保留某個值，請將其複製到文件欄位中，如前述範例所示。

文件的 `_source` 可以包含名為 `_ingest` 的欄位。若要存取此欄位，請使用 `_source._ingest` 前綴。若沒有前綴，`_ingest` 會指向匯入中繼資料。下列處理器會將 `_ingest` 來源欄位的值複製到 `ingest_source` 欄位：

```json
{
  "set": {
    "field": "ingest_source",
    "value": "{% raw %}{{_source._ingest}}{% endraw %}"
  }
}
```

## 在 Mustache 範本中使用欄位值

使用 Mustache 範本將欄位值插入處理器設定中。只有部分處理器參數支援範本；各處理器的參數表會說明哪些參數支援範本。如需詳細資訊，請參閱[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。範本以名稱參照欄位，不加上 `ctx`。

雙大括號（{% raw %}`{{` 和 `}}`{% endraw %}）會在值中的特殊字元（例如引號和反斜線）前加上反斜線，以進行逸出。三重大括號（{% raw %}`{{{` 和 `}}}`{% endraw %}）則直接插入值，不進行逸出。例如，若 `title` 欄位包含 `say "hi"`，則 {% raw %}`{{title}}`{% endraw %} 會產生 `say \"hi\"`，而 {% raw %}`{{{title}}}`{% endraw %} 會產生 `say "hi"`。

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

下列範例定義一個完整的資料匯入管線，使用 `user.first` 與 `department` 欄位設定標語、從 `date` 欄位擷取 `year`，並將文件的匯入時間戳記記錄在 `received_at` 欄位：

```json
PUT _ingest/pipeline/example-pipeline
{
  "description": "Sets a tagline, extracts the year, and records the ingest time",
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

回應會顯示經處理充實後的文件，包括新增的 `tagline`、擷取的 `year`，以及由資料匯入管線產生的 `received_at` 時間戳記：

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
