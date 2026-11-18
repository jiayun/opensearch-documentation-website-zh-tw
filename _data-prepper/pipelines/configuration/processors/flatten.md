---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "扁平化"
parent: Processors
grand_parent: Pipelines
nav_order: 140
canonical_url: https://docs.opensearch.org/latest/data-prepper/pipelines/configuration/processors/flatten/
redirect_to: https://docs.opensearch.org/latest/data-prepper/pipelines/configuration/processors/flatten/
---

# 扁平化處理器

`flatten` 處理器會將事件中的巢狀物件轉換為扁平化結構。

## 組態

下表說明 `flatten` 處理器的組態選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`source` | 是 | 字串 | 要執行此操作的來源索引鍵。若設為空字串（`""`），處理器會使用事件的根層級作為來源。
`target` | 是 | 字串 | 用來存放扁平化欄位的目標索引鍵。若設為空字串（`""`），處理器會使用事件的根層級作為目標。
`exclude_keys` | 否 | 清單 | 來源欄位中應排除、不予處理的索引鍵。預設為空清單（`[]`）。
`remove_source_keys` | 否 | 布林值 | 若為 `true`，處理器會從來源中移除所有已處理的欄位。預設為 `false`。
`remove_list_elements` | 否 | 布林值 | 若為 `true`，處理器會從扁平化索引鍵中移除清單索引，並將相符索引鍵的值收集到目標欄位的清單中。例如，`list[0].name` 和 `list[1].name` 會合併成單一 `list[].name` 索引鍵，其中包含這兩個值的清單。預設為 `false`。
`remove_brackets` | 否 | 布林值 | 若為 `true`，處理器還會移除清單索引被移除後，扁平化索引鍵中殘留的空括號（`[]`）。例如，`list[].name` 會變成 `list.name`。只有在 `remove_list_elements` 為 `true` 時，此設定才會生效。預設為 `false`。
`flatten_when` | 否 | 字串 | 一個[條件運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)，例如 `/some-key == "test"'`，用來決定是否要對事件執行 `flatten` 處理器。預設為 `null`，表示除非另有指定，否則會處理所有事件。
`flatten_separator` | 否 | 字串 | 將巢狀索引鍵名稱串接成扁平化索引鍵時所使用的字元。必須是單一字元。預設為 `.`。
`tags_on_failure` | 否 | 清單 | 事件處理失敗時，要加入事件中繼資料的標籤清單。

## 使用方式

下列範例說明如何在 OpenSearch Data Prepper 管線中使用 `flatten` 處理器。

### 最低組態

下列範例僅顯示使用 `flatten` 處理器所需的參數：`source` 和 `target`：

```yaml
...
  processor:
    - flatten:
        source: "key2"   
        target: "flattened-key2"  
...
```
{% include copy.html %}

例如，當輸入事件包含下列巢狀物件時：

```json
{
  "key1": "val1",
  "key2": {
    "key3": {
      "key4": "val2"
    }
  }
}
```

`flatten` 處理器會在 `flattened-key2` 物件下建立扁平化結構，如下列輸出所示：

```json
{
  "key1": "val1",
  "key2": {
    "key3": {
      "key4": "val2"
    }
  },
  "flattened-key2": {
    "key3.key4": "val2"
  }
}
```

### 移除已處理的欄位

在將事件的所有巢狀物件扁平化時，請使用 `remove_source_keys` 選項。這會移除事件中所有已處理的欄位，如下列範例所示：

```yaml
...
  processor:
    - flatten:
        source: ""   # empty string represents root of event
        target: ""   # empty string represents root of event
        remove_source_keys: true
...
```
{% include copy.html %}

例如，當輸入事件包含下列巢狀物件時：

```json
{
  "key1": "val1",
  "key2": {
    "key3": {
      "key4": "val2"
    }
  },
  "list1": [
    {
      "list2": [
        {
          "name": "name1",
          "value": "value1"
        },
        {
          "name": "name2",
          "value": "value2"
        }
      ]
    }
  ]
}
```


`flatten` 處理器會建立一個扁平化結構，其中不包含任何已處理的欄位，如下列輸出所示：

```json
{
  "key1": "val1",
  "key2.key3.key4": "val2",
  "list1[0].list2[0].name": "name1",
  "list1[0].list2[0].value": "value1",
  "list1[0].list2[1].name": "name2",
  "list1[0].list2[1].value": "value2",
}
```

### 將特定索引鍵排除於扁平化之外

使用 `exclude_keys` 選項可防止特定索引鍵在輸出中被扁平化，如下列範例所示，其中排除了 `key2` 值：

```yaml
...
  processor:
    - flatten:
        source: ""   # empty string represents root of event
        target: ""   # empty string represents root of event
        remove_source_keys: true
        exclude_keys: ["key2"]
...
```
{% include copy.html %}

例如，當輸入事件包含下列巢狀物件時：

```json
{
  "key1": "val1",
  "key2": {
    "key3": {
      "key4": "val2"
    }
  },
  "list1": [
    {
      "list2": [
        {
          "name": "name1",
          "value": "value1"
        },
        {
          "name": "name2",
          "value": "value2"
        }
      ]
    }
  ]
}
```

輸入事件中除了 `key2` 索引鍵以外的所有其他巢狀物件都會被扁平化，如下列範例所示：

```json
{
  "key1": "val1",
  "key2": {
    "key3": {
      "key4": "val2"
    }
  },
  "list1[0].list2[0].name": "name1",
  "list1[0].list2[0].value": "value1",
  "list1[0].list2[1].name": "name2",
  "list1[0].list2[1].value": "value2",
}
```

### 移除清單索引

使用 `remove_list_elements` 選項，將來源對應表中的欄位轉換為清單，並將這些清單放入目標欄位，如下列範例所示：

```yaml
...
  processor:
    - flatten:
        source: ""   # empty string represents root of event
        target: ""   # empty string represents root of event
        remove_source_keys: true
        remove_list_elements: true
...
```
{% include copy.html %}

例如，當輸入事件包含下列巢狀物件時：

```json
{
  "key1": "val1",
  "key2": {
    "key3": {
      "key4": "val2"
    }
  },
  "list1": [
    {
      "list2": [
        {
          "name": "name1",
          "value": "value1"
        },
        {
          "name": "name2",
          "value": "value2"
        }
      ]
    }
  ]
}
```

處理器會從輸出中移除所有索引，並以扁平化的結構化清單形式放入來源對應表，如下列範例所示：

```json
{
  "key1": "val1",
  "key2.key3.key4": "val2",
  "list1[].list2[].name": ["name1","name2"],
  "list1[].list2[].value": ["value1","value2"]
}
```

如果您同時將 `remove_brackets` 設定為 `true`，處理器會移除鍵中的空方括號，如下列輸出所示：

```json
{
  "key1": "val1",
  "key2.key3.key4": "val2",
  "list1.list2.name": ["name1","name2"],
  "list1.list2.value": ["value1","value2"]
}
```

### 自訂分隔字元

使用 `flatten_separator` 選項指定用來串接巢狀鍵名稱的自訂字元。預設分隔字元為 `.`，但您可以使用任何單一字元，例如 `_`，如下列範例所示：

```yaml
...
  processor:
    - flatten:
        source: "log"
        target: ""
        flatten_separator: "_"
        remove_source_keys: true
...
```
{% include copy.html %}

假設有一個輸入事件包含下列巢狀物件：

```json
{
  "timestamp": "2026-07-29T12:00:00Z",
  "service": "user-service",
  "log": {
    "request": {
      "method": "POST",
      "url": "/api/v1/users",
      "headers": {
        "content_type": "application/json"
      }
    },
    "response": {
      "status": 200,
      "body": {
        "user_id": "usr_12345"
      }
    }
  }
}
```

`flatten` 處理器會以 `_` 作為分隔字元將 `log` 欄位扁平化，並將結果放在事件的根層級。由於 `remove_source_keys` 為 `true`，已處理的巢狀欄位會被移除，只留下一個空的 `log` 物件，如下列輸出所示：

```json
{
  "timestamp": "2026-07-29T12:00:00Z",
  "service": "user-service",
  "log": {},
  "request_method": "POST",
  "request_url": "/api/v1/users",
  "request_headers_content_type": "application/json",
  "response_status": 200,
  "response_body_user_id": "usr_12345"
}
```
