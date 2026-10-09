---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "UBI Query DSL 查詢範例"
parent: User Behavior Insights
grand_parent: Optimizing search quality
has_children: false
nav_order: 15
---

# UBI Query DSL 查詢範例

您可以使用 OpenSearch 搜尋查詢語言 [Query DSL]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/) 來撰寫 User Behavior Insights (UBI) 查詢。下列範例會傳回每個 `action_name` 事件發生的次數。
如需更完整的分析查詢，請參閱 [UBI SQL 查詢範例]({{site.url}}{{site.baseurl}}/search-plugins/ubi/sql-queries/)。 
#### 請求範例
```json
GET ubi_events/_search
{
  "size":0, 
  "aggs":{ 
    "event_types":{
      "terms": {
        "field":"action_name", 
        "size":10
      }
    }
  }
}
```
{% include copy.html %}

#### 回應範例

```json
{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 10000,
      "relation": "gte"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "event_types": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "brand_filter",
          "doc_count": 3084
        },
        {
          "key": "product_hover",
          "doc_count": 3068
        },
        {
          "key": "button_click",
          "doc_count": 3054
        },
        {
          "key": "product_sort",
          "doc_count": 3012
        },
        {
          "key": "on_search",
          "doc_count": 3010
        },
        {
          "key": "type_filter",
          "doc_count": 2925
        },
        {
          "key": "login",
          "doc_count": 2433
        },
        {
          "key": "logout",
          "doc_count": 1447
        },
        {
          "key": "new_user_entry",
          "doc_count": 207
        }
      ]
    }
  }
}
```
{% include copy.html %}

您可以在 OpenSearch Dashboards 的 [Dev Tools]({{site.url}}{{site.baseurl}}/dashboards/dev-tools/index/) 主控台中執行上述查詢。
