---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "執行演算法"
parent: ML Commons APIs
nav_order: 90
---

# Execute Algorithm API

有些演算法（例如 [Localization]({{site.url}}{{site.baseurl}}/ml-commons-plugin/algorithms#localization)）不需要已訓練的模型。您可以使用 `execute` API 執行不依賴模型的演算法。

## 端點

```json
POST _plugins/_ml/_execute/{algorithm_name}
```

## 範例請求：執行 Localization 演算法

下列範例使用 Localization 演算法，為彙總資料（例如隨時間彙總的資料）找出子集合層級的資訊，以呈現感興趣的活動，例如尖峰、下降、變化或異常。

```json
POST /_plugins/_ml/_execute/anomaly_localization
{
  "index_name": "rca-index",
  "attribute_field_names": [
    "attribute"
  ],
  "aggregations": [
    {
      "sum": {
        "sum": {
          "field": "value"
        }
      }
    }
  ],
  "time_field_name": "timestamp",
  "start_time": 1620630000000,
  "end_time": 1621234800000,
  "min_time_interval": 86400000,
  "num_outputs": 10
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "results" : [
    {
      "name" : "sum",
      "result" : {
        "buckets" : [
          {
            "start_time" : 1620630000000,
            "end_time" : 1620716400000,
            "overall_aggregate_value" : 65.0
          },
          {
            "start_time" : 1620716400000,
            "end_time" : 1620802800000,
            "overall_aggregate_value" : 75.0,
            "entities" : [
              {
                "key" : [
                  "attr0"
                ],
                "contribution_value" : 1.0,
                "base_value" : 2.0,
                "new_value" : 3.0
              },
              {
                "key" : [
                  "attr1"
                ],
                "contribution_value" : 1.0,
                "base_value" : 3.0,
                "new_value" : 4.0
              },
              {
                "key" : [
                  "attr2"
                ],
                "contribution_value" : 1.0,
                "base_value" : 4.0,
                "new_value" : 5.0
              },
              {
                "key" : [
                  "attr3"
                ],
                "contribution_value" : 1.0,
                "base_value" : 5.0,
                "new_value" : 6.0
              },
              {
                "key" : [
                  "attr4"
                ],
                "contribution_value" : 1.0,
                "base_value" : 6.0,
                "new_value" : 7.0
              },
              {
                "key" : [
                  "attr5"
                ],
                "contribution_value" : 1.0,
                "base_value" : 7.0,
                "new_value" : 8.0
              },
              {
                "key" : [
                  "attr6"
                ],
                "contribution_value" : 1.0,
                "base_value" : 8.0,
                "new_value" : 9.0
              },
              {
                "key" : [
                  "attr7"
                ],
                "contribution_value" : 1.0,
                "base_value" : 9.0,
                "new_value" : 10.0
              },
              {
                "key" : [
                  "attr8"
                ],
                "contribution_value" : 1.0,
                "base_value" : 10.0,
                "new_value" : 11.0
              },
              {
                "key" : [
                  "attr9"
                ],
                "contribution_value" : 1.0,
                "base_value" : 11.0,
                "new_value" : 12.0
              }
            ]
          },
          ...
        ]
      }
    }
  ]
}
```

