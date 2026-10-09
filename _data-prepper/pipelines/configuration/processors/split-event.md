---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分割事件"
parent: Processors
grand_parent: Pipelines
nav_order: 340
---

# 分割事件處理器

`split_event` 處理器可根據分隔符號分割事件，並從使用者指定的欄位產生多個事件。

## 組態

下表說明 `split_event` 處理器的組態選項。

| 選項           | 類型    | 說明                                                                                   |
|------------------|---------|-----------------------------------------------------------------------------------------------|
| `field`          | String  | 要分割的事件欄位。                                                           |
| `delimiter_regex`| String  | 用作分割欄位之分隔符號的規則運算式。                         |
| `delimiter`      | String  | 用於分割欄位的分隔符號。若未指定，則使用預設分隔符號。  |
| `split_when`     | String  | 決定是否將處理器套用至事件的[條件運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)。若條件評估結果為 `false`，事件將保持不變。預設為 `null`（處理所有事件）。 |

# 使用方式

若要使用 `split_event` 處理器，請將下列內容新增至您的 `pipelines.yaml` 檔案：

```yaml
split-event-pipeline:
  source:
    http:
  processor:
    - split_event:
        field: query
        delimiter: ' '    
  sink:
    - stdout:
```
{% include copy.html %}

當事件包含下列範例輸入時：

```json
{"query" : "open source", "some_other_field" : "abc" }
```

輸入將根據 `query` 欄位分割成多個事件，並以空白字元作為分隔符號，如下列範例所示：

```json
{"query" : "open", "some_other_field" : "abc" }
{"query" : "source", "some_other_field" : "abc" }
```

## 使用 split_when 進行條件式分割

您可以使用 `split_when` 根據事件內容有條件地套用分割。這在多租用戶管線中很實用，因為只有特定事件需要分割。在下列範例中，`split_event` 處理器只會分割 `body` 欄位包含換行字元的事件。不含換行的事件將保持不變：

```yaml
split-event-pipeline:
  source:
    http:
  processor:
    - split_event:
        field: body
        delimiter: "\n"
        split_when: 'contains(/body, "\n")'
  sink:
    - stdout:
```
{% include copy.html %}


