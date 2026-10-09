---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: length()
parent: Functions
grand_parent: Pipelines
nav_order: 30
---

<!-- vale off -->
# length() 函式
<!-- vale on -->

`length()` 函式接受一個 JSON pointer 類型的引數，並傳回所傳入值的長度。例如，當事件中存在名為 message 的鍵，且其值為 `1234567890` 時，`length(/message)` 會傳回長度 `10`。

#### 範例 

```json
{
  "event": {
    "/message": "1234567890"
  },
  "expression": "length(/message)",
  "expected_output": 10
}
```
{% include copy.html %}
