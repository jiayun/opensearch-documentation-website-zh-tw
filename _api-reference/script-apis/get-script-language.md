---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得指令碼語言"
parent: Script APIs
nav_order: 60
---

# 取得指令碼語言 API
**1.0 版引入**
{: .label .label-purple }

取得指令碼語言 API 會擷取所有支援的指令碼語言（例如 Painless），以及這些語言可使用的情境。如需詳細資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

## 請求範例

<!-- spec_insert_start
component: example_code
rest: GET /_script_language
-->
{% capture step1_rest %}
GET /_script_language
{% endcapture %}

{% capture step1_python %}

response = client.get_script_languages()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

`GET _script_language` 請求會傳回每種語言可用的情境：

```json
{
  "types_allowed" : [
    "inline",
    "stored"
  ],
  "language_contexts" : [
    {
      "language" : "expression",
      "contexts" : [
        "aggregation_selector",
        "aggs",
        "bucket_aggregation",
        "field",
        "filter",
        "number_sort",
        "score",
        "terms_set"
      ]
    },
    {
      "language" : "mustache",
      "contexts" : [
        "template"
      ]
    },
    {
      "language" : "opensearch_query_expression",
      "contexts" : [
        "aggs",
        "filter"
      ]
    },
    {
      "language" : "painless",
      "contexts" : [
        "aggregation_selector",
        "aggs",
        "aggs_combine",
        "aggs_init",
        "aggs_map",
        "aggs_reduce",
        "analysis",
        "bucket_aggregation",
        "field",
        "filter",
        "ingest",
        "interval",
        "moving-function",
        "number_sort",
        "painless_test",
        "processor_conditional",
        "score",
        "script_heuristic",
        "similarity",
        "similarity_weight",
        "string_sort",
        "template",
        "terms_set",
        "trigger",
        "update"
      ]
    }
  ]
}
```

## 回應本文欄位

此請求包含下列回應欄位。

欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
`types_allowed` | 字串清單 | 已啟用的指令碼類型，由 `script.allowed_types` 設定決定。可能包含 `inline` 和/或 `stored`。
`language_contexts` | 物件清單 | 物件清單，其中每個物件都會將一種支援的語言對應至其可用的情境。
`language_contexts.language` | 字串 | 已註冊的指令碼語言名稱。
`language_contexts.contexts` | 字串清單 | 該語言所有情境的清單，由 `script.allowed_contexts` 設定決定。
