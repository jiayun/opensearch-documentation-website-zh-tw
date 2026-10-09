---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: hasTags()
parent: Functions
grand_parent: Pipelines
nav_order: 20
---

<!-- vale off -->
# hasTags() 函式
<!-- vale on -->

`hasTags()` 函式接受一個或多個字串類型的引數，如果傳入的所有引數都存在於事件的標籤中，則傳回 `true`。如果某個引數不存在於事件的標籤中，則函式傳回 `false`。

例如，如果您使用運算式 `hasTags("tag1")`，且事件包含 `tag1`，則 OpenSearch Data Prepper 會傳回 `true`。如果您使用運算式 `hasTags("tag2")`，但事件僅包含 `tag1`，則 Data Prepper 會傳回 `false`。

#### 範例

```json
{
  "events": [
    {
      "tags": ["tag1"],
      "data": {
        // ...
      }
    },
    {
      "tags": ["tag1", "tag2"],
      "data": {
        // ...
      }
    }
  ],
  "expressions": [
    {
      "expression": "hasTags(\"tag1\")",
      "expected_results": [true, true]
    },
    {
      "expression": "hasTags(\"tag2\")",
      "expected_results": [false, true]
    }
  ]
}
```
{% include copy.html %}
