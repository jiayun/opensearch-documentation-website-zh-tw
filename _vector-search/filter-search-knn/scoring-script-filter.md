---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "評分指令碼篩選器"
parent: Filtering data
nav_order: 30
---

# 評分指令碼篩選器

評分指令碼篩選器會先篩選文件，然後對結果使用暴力精確 k-NN 搜尋。例如，下列查詢會搜尋評分介於 8 到 10（含）之間且提供停車位的飯店，然後執行 k-NN 搜尋，以傳回最接近指定 `location` 的 3 間飯店：

```json
POST /hotels-index/_search
{
  "size": 3,
  "query": {
    "script_score": {
      "query": {
        "bool": {
          "filter": {
            "bool": {
              "must": [
                {
                  "range": {
                    "rating": {
                      "gte": 8,
                      "lte": 10
                    }
                  }
                },
                {
                  "term": {
                    "parking": "true"
                  }
                }
              ]
            }
          }
        }
      },
      "script": {
        "source": "knn_score",
        "lang": "knn",
        "params": {
          "field": "location",
          "query_value": [
            5.0,
            4.0
          ],
          "space_type": "l2"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}
