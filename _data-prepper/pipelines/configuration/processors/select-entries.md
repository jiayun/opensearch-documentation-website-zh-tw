---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Select entries
parent: Processors
grand_parent: Pipelines
nav_order: 320
---

# Select entries 處理器

`select_entries` 處理器會從 OpenSearch Data Prepper 事件中選取項目。
只有被選取的項目會保留在處理後的事件中，其餘所有項目都會被移除。不過，此處理器不會從 Data Prepper 管線中移除任何事件。

## 組態

您可以使用下列選項來設定 `select_entries` 處理器。

| Option | Required | Description |
| :--- |:---------| :--- |
| `include_keys` | No       | 要從事件中選取的鍵清單。 |
| `include_keys_regex` | No | 符合要從事件中選取之鍵的規則運算式 (regex) 模式。 |
| `select_when` | No       | 一個[條件運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)，例如 `/some-key == "test"`，用於評估是否要在事件上執行此處理器。若條件不符合，事件將以未修改的狀態繼續通過管線，並保留所有原始欄位。 |

## 用法

首先，建立下列 `pipeline.yaml` 檔案：

```yaml
pipeline:
  source:
    ...
  ....  
  processor:
    - select_entries:
        include_keys: [ "key1", "key2" ]
        select_when: '/some_key == "test"'
  sink:
```
{% include copy.html %}


例如，當您的來源包含下列事件記錄時：

```json
{
  "message": "hello",
  "key1" : "value1",
  "key2" : "value2",
  "some_key" : "test"
}
```

處理後，只有 `include_keys` 中列出的鍵會保留在事件中；其餘所有鍵都會被移除：

```json
{"key1": "value1", "key2": "value2"}
```

### 使用 regex 選取鍵

下列範例示範如何在 `pipeline.yaml` 檔案中設定 `include_keys_regex` 欄位：

```yaml
pipeline:
  source:
    ...
  ....  
  processor:
    - select_entries:
        include_keys: [ "key1", "key2" ]
        include_keys_regex: ["^ran.*"]
        select_when: '/some_key == "test"'
  sink:
```
{% include copy.html %}

例如，當您的來源包含下列事件記錄時：

```json
{
  "message": "hello",
  "key1" : "value1",
  "key2" : "value2",
  "some_key" : "test",
  "random1": "another",
  "random2" : "set",
  "random3": "of",
  "random4": "values"
}
```

處理器會保留 `include_keys` 中明確列出的鍵，以及符合 ` include_keys_regex` 模式的任何鍵，並從事件中移除其餘所有鍵：

```json
{"key1": "value1", "key2": "value2", "random1": "another", "random2" : "set", "random3": "of", "random4": "values"}
```

### 存取巢狀欄位

使用 `/` 來存取巢狀欄位。

例如，當您的來源包含下列含巢狀欄位的事件時：

```
{
  "field1": "abc",
  "field2": 123,
  "field3": {
    "name": "Alice",
    "surname": "Smith"
  },
  "field4": {
    "address": "123 Main St"
  }
}
```

您可以使用下列語法來選取欄位的子集：

```
pipeline:
  source:
    ...
  ....  
  processor:
    - select_entries:
        include_keys:
          - field1
          - field2
          - field3/name
        select_when: '/field3/surname == "Smith"'
  sink:
```

