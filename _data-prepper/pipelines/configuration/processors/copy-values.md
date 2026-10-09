---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Copy values 
parent: Processors
grand_parent: Pipelines
nav_order: 60
---

# Copy values 處理器

`copy_values` 處理器會複製事件中的值，是一種[變更事件]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/mutate-event/)處理器。

## 組態

您可以使用下列選項來設定 `copy_values` 處理器。

| 選項 | 必要 | 類型 | 說明 |
:--- | :--- | :--- | :---
| `entries` | 是 | [entry](#entry) | 要在事件中複製的項目清單。如需更多資訊，請參閱 [entry](#entry)。 |
| `from_list` | 否 | 字串 | 要複製的物件清單的鍵。 |
| `to_list` | 否 | 字串 | 要新增的新清單的鍵。 |
| `overwrite_if_to_list_exists` | 否 | 布林值 | 設定為 `true` 時，如果 `to_list` 指定的 `key` 已存在於事件中，則會覆寫現有的值。預設為 `false`。 |

<!-- vale off -->
## entry
<!-- vale on -->

對於每個項目，您可以設定下列選項。

| 選項 | 必要 | 類型 | 說明 |
:--- | :--- | :--- | :---
| `from_key` | 是 | 字串 | 要複製的項目的鍵。 |
| `to_key` | 是 | 字串 | 要新增的新項目的鍵。 |
| `overwrite_if_to_key_exists` | 否 | 布林值 | 設定為 `true` 時，如果 `key` 已存在於事件中，則會覆寫現有的值。預設為 `false`。 |
| `copy_when` | 否 | 字串 | 使用 [Data Prepper 運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)指定執行 `copy_values` 操作的條件。若有指定，則只有當運算式評估為 `true` 時，`copy_values` 操作才會執行。 |


## 用法

下列範例示範如何使用 `copy_values` 處理器。

### 範例：複製值並略過現有欄位

下列範例示範如何設定處理器以複製值並略過現有欄位：

```yaml
...
  processor:
    - copy_values:
        entries:
          - from_key: "message1"
            to_key: "message2"
          - from_key: "message1"
            to_key: "message3"
...
```
{% include copy.html %}

當輸入事件包含下列資料時：

```json
{"message1": "hello", "message2": "bye"}
```

處理器會將 "message1" 複製到 "message3"，但不會複製到 "message2"，因為 "message2" 已經存在。處理後的事件包含下列資料：

```json
{"message1": "hello", "message2": "bye", "message3": "hello"}
```

### 範例：複製值並覆寫

下列範例示範如何設定處理器以複製值：

```yaml
...
  processor:
    - copy_values:
        entries:
          - from_key: "message1"
            to_key: "message2"
            overwrite_if_to_key_exists: true
          - from_key: "message1"
            to_key: "message3"
...
```
{% include copy.html %}

當輸入事件包含下列資料時：

```json
{"message1": "hello", "message2": "bye"}
```

處理器會將 "message1" 複製到 "message2" 和 "message3"，並覆寫 "message2" 中現有的值。處理後的事件包含下列資料：

```json
{"message1": "hello", "message2": "hello", "message3": "hello"}
```

### 範例：在兩個物件清單之間選擇性複製值

下列範例示範如何設定處理器以在清單之間複製值：

```yaml
...
  processor:
    - copy_values:
        from_list: mylist
        to_list: newlist
        entries:
          - from_key: name
            to_key: fruit_name
...
```
{% include copy.html %}

當輸入事件包含下列資料時：

```json
{
  "mylist": [
    {"name": "apple", "color": "red"},
    {"name": "orange", "color": "orange"}
  ]
}
```

處理後的事件包含一個 `newlist`，其中含有選擇性複製的欄位：

```json
{
  "newlist": [
    {"fruit_name": "apple"},
    {"fruit_name": "orange"}
  ],
  "mylist": [
    {"name": "apple", "color": "red"},
    {"name": "orange", "color": "orange"}
  ]
}
```
