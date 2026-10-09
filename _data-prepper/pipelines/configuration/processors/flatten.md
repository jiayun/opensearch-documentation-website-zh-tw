---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "扁平化"
parent: Processors
grand_parent: Pipelines
nav_order: 140
---

# 扁平化處理器

`flatten` 處理器會將事件中的巢狀物件轉換為扁平化結構。

## 組態

下表說明 `flatten` 處理器的組態選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`source` | 是 | 字串 | 要執行操作的來源鍵。若設為空字串 (`""`)，處理器會使用事件的根層級作為來源。
`target` | 是 | 字串 | 要放入扁平化欄位的目標鍵。若設為空字串 (`""`)，處理器會使用事件的根層級作為目標。
`exclude_keys` | 否 | 清單 | 來源欄位中應排除於處理之外的鍵。預設為空清單 (`[]`)。
`remove_processed_fields` | 否 | 布林值 | 若為 `true`，處理器會從來源移除所有已處理的欄位。預設為 `false`。
`remove_list_indices` | 否 | 布林值 | 若為 `true`，處理器會將來源對應中的欄位轉換為清單，並將這些清單放入目標欄位。預設為 `false`。
`flatten_when` | 否 | 字串 | [條件運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)，例如 `/some-key == "test"'`，用於決定是否要對事件執行 `flatten` 處理器。預設為 `null`，表示除非另有指定，否則會處理所有事件。
`flatten_separator` | 否 | 字串 | 用於將巢狀鍵名稱連接成扁平化鍵的字元。必須是單一字元。預設為 `.`。
`tags_on_failure` | 否 | 清單 | 事件處理失敗時，要新增至事件中繼資料的標籤清單。

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

將事件的所有巢狀物件扁平化時，請使用 `remove_processed_fields` 選項。這會移除事件中所有已處理的欄位，如下列範例所示：

```yaml
...
  processor:
    - flatten:
        source: ""   # empty string represents root of event
        target: ""   # empty string represents root of event
        remove_processed_fields: true
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


`flatten` 處理器會建立不含任何已處理欄位的扁平化結構，如下列輸出所示：

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

### 排除特定鍵不進行扁平化

請使用 `exclude_keys` 選項來防止特定鍵在輸出中被扁平化，如下列範例所示，其中排除了 `key2` 值：

```yaml
...
  processor:
    - flatten:
        source: ""   # empty string represents root of event
        target: ""   # empty string represents root of event
        remove_processed_fields: true
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

輸入事件中除了 `key2` 鍵以外的所有其他巢狀物件都會被扁平化，如下列範例所示：

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

請使用 `remove_list_indices` 選項將來源對應中的欄位轉換為清單，並將這些清單放入目標欄位，如下列範例所示：

```yaml
...
  processor:
    - flatten:
        source: ""   # empty string represents root of event
        target: ""   # empty string represents root of event
        remove_processed_fields: true
        remove_list_indices: true
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

處理器會從輸出中移除所有清單索引，並將其以扁平化的結構化清單放入來源對應中，如下列範例所示：

```json
{
  "key1": "val1",
  "key2.key3.key4": "val2",
  "list1[].list2[].name": ["name1","name2"],
  "list1[].list2[].value": ["value1","value2"]
}
```

### 自訂分隔字元

請使用 `flatten_separator` 選項來指定連接巢狀鍵名稱的自訂字元。預設分隔字元為 `.`，但您可以使用任何單一字元，例如 `_`，如下列範例所示：

```yaml
...
  processor:
    - flatten:
        source: "log"
        target: ""
        flatten_separator: "_"
        remove_processed_fields: true
...
```
{% include copy.html %}

假設輸入事件包含下列巢狀物件：

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

`flatten` 處理器會使用 `_` 作為分隔字元將 `log` 欄位扁平化，並將結果放在事件的根層級，如下列輸出所示：

```json
{
  "timestamp": "2026-07-29T12:00:00Z",
  "service": "user-service",
  "request_method": "POST",
  "request_url": "/api/v1/users",
  "request_headers_content_type": "application/json",
  "response_status": 200,
  "response_body_user_id": "usr_12345"
}
```
