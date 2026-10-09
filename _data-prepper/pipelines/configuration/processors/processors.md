---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "處理器"
has_children: true
parent: Pipelines
nav_order: 35
redirect_from:
  - /data-prepper/pipelines/configuration/processors/mutate-event/
  - /data-prepper/pipelines/configuration/processors/mutate-string/
  - /data-prepper/pipelines/configuration/processors/
---

# Data Prepper 處理器

處理器是 OpenSearch Data Prepper 管線中的元件，讓您能在將記錄發佈到 `sink` 元件之前，以所需的格式篩選、轉換和充實事件。如果管線組態中未定義 `processor`，事件將以 `source` 元件指定的格式發佈。您可以在單一管線中加入多個處理器，它們會依照管線中定義的順序依序執行。

在 Data Prepper 1.3 之前，這些元件稱為 *preppers*。在 Data Prepper 1.3 中，*prepper* 一詞已被棄用，改用 *processor*。在 Data Prepper 2.0 中，*prepper* 一詞已被移除。
{: .note }

# 事件變更處理器

使用事件變更處理器來修改 OpenSearch Data Prepper 中的事件。以下是可用的處理器。

| 處理器 | 說明 |
|-----------|-------------|
| [`add_entries`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/add-entries/) | 在事件中新增項目。 |
| [`convert_entry_type`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/convert-entry-type/) | 轉換事件中的值類型。 |
| [`copy_values`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/copy-values/) | 在事件內複製值。 |
| [`delete_entries`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/delete-entries/) | 從事件中刪除項目。 |
| [`list_to_map`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/list-to-map) | 將事件中的物件清單（其中每個物件都包含 `key` 欄位）轉換為以目標鍵組成的對應表。 |
| [`map_to_list`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/map-to-list) | 將事件中的物件對應表（其中每個物件都包含 `key` 欄位）轉換為目標鍵的清單。 |
| [`rename_keys`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/rename-keys/) | 重新命名事件中的鍵。 |
| [`select_entries`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/select-entries/) | 從事件中選取項目。 |

## 字串變更處理器

使用字串變更處理器來修改字串值的內容或格式。以下是可用的處理器。

| 處理器 | 說明 |
|-----------|-------------|
| [`substitute_string`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/substitute-string/) | 使用規則運算式將字串的一部分替換為指定的值。 |
| [`split_string`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/split-string/) | 使用指定的分隔符號將字串分割成清單。 |
| [`uppercase_string`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/uppercase-string/) | 將字串轉換為大寫。 |
| [`lowercase_string`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/lowercase-string/) | 將字串轉換為小寫。 |
| [`trim_string`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/trim-string/) | 移除字串開頭和結尾的空白字元。 |

