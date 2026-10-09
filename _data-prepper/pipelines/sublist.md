---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: subList()
parent: Functions
grand_parent: Pipelines
nav_order: 50
---

<!-- vale off -->
# subList() 函式
<!-- vale on -->

`subList(<key>, <start_index, inclusive>, <end_index, exclusive>)` 函式會從事件中的清單欄位擷取子清單。此函式接受下列引數：

- 指向包含清單的事件欄位的 JSON 指標
- 起始索引（包含）
- 結束索引（不包含）

此函式會傳回指定起始索引與結束索引之間的清單部分。如果結束索引為 `-1`，此函式會擷取從起始索引到清單結尾的元素。


## 範例

下列範例說明 `sublist()` 函式的運作方式。

<!-- vale off -->
### add_entries 處理器
<!-- vale on -->

您可以在 `add_entries` 處理器中使用 `subList()`，如下列範例所示。

此函式使用下列輸入來擷取子清單：

```
input: {"my_list": [ 0, 1, 2, 3, 4, 5, 6]}
```

接著，下列組態使用 `add_entries` 處理器，從 `my_list` 擷取子清單，從索引 `1` 開始，並在索引 `4` 之前結束： 

```yaml
add_entries:
  entries:
    - key: "my_list"
      value_expression: '/subList(/my_list, 1, 4)'
      overwrite_if_key_exists: true
```
{% include copy.html %}

下列輸出顯示擷取索引 `1` 到 `3` 的元素並覆寫原始清單後所得到的清單：

```
output: my_list: [1, 2, 3]
```

### 特定範圍

下列各個範例示範 `subList()` 函式如何從清單擷取特定範圍的元素。

下列範例擷取索引 `0` 到 `2` 的元素（不包含索引 `3`），得到清單的前三個元素：

```json
{
  "event": {
    "/my_list": [0, 1, 2, 3, 4, 5, 6]
  },
  "expression": "subList(/my_list, 4, -1)",
  "expected_output": [4, 5, 6]
}
```
{% include copy.html %}

下列範例使用 `-1` 作為結束索引，指定包含從索引 `4` 到清單結尾的所有元素：

```json
{
  "event": {
    "/my_list": [0, 1, 2, 3, 4, 5, 6]
  },
  "expression": "subList(/my_list, 4, -1)",
  "expected_output": [4, 5, 6]
}
```
{% include copy.html %}
