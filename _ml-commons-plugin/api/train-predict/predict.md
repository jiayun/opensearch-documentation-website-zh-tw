---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "預測"
parent: Model APIs
grand_parent: ML Commons APIs
nav_order: 60
---

# Predict API

ML Commons 可以使用您訓練好的模型，從已編製索引的資料或資料框預測新資料。若要使用 Predict API，需要 `model_id`。

有關此 API 的使用者存取權資訊，請參閱[模型存取控制注意事項]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/index/#model-access-control-considerations)。

## 端點

```json
POST /_plugins/_ml/_predict/{algorithm_name}/{model_id}
```

## 請求本文欄位

下表列出可用的請求欄位。

欄位 | 資料類型 | 必要／選用 | 說明
:---  | :--- | :--- | :---
`parameters` | 物件 | 選用 | 用於預測的模型專屬參數。
`parameters.input_processors` | 陣列 | 選用 | 在將輸入資料傳送至模型之前，用來轉換輸入資料的處理器清單。如需更多資訊，請參閱[處理器鏈]({{site.url}}{{site.baseurl}}/ml-commons-plugin/processor-chain/)。
`parameters.output_processors` | 陣列 | 選用 | 用來轉換模型輸出資料的處理器清單。如需更多資訊，請參閱[處理器鏈]({{site.url}}{{site.baseurl}}/ml-commons-plugin/processor-chain/)。

對於外部託管的模型，實際的輸入欄位取決於模型的連接器組態。如需更多資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

## 範例請求

```json
POST /_plugins/_ml/_predict/kmeans/{model-id}
{
    "input_query": {
        "_source": ["petal_length_in_cm", "petal_width_in_cm"],
        "size": 10000
    },
    "input_index": [
        "iris_data"
    ]
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "status" : "COMPLETED",
  "prediction_result" : {
    "column_metas" : [
      {
        "name" : "ClusterID",
        "column_type" : "INTEGER"
      }
    ],
    "rows" : [
      {
        "values" : [
          {
            "column_type" : "INTEGER",
            "value" : 1
          }
        ]
      },
      {
        "values" : [
          {
            "column_type" : "INTEGER",
            "value" : 1
          }
        ]
      },
      {
        "values" : [
          {
            "column_type" : "INTEGER",
            "value" : 0
          }
        ]
      },
      {
        "values" : [
          {
            "column_type" : "INTEGER",
            "value" : 0
          }
        ]
      },
      {
        "values" : [
          {
            "column_type" : "INTEGER",
            "value" : 0
          }
        ]
      },
      {
        "values" : [
          {
            "column_type" : "INTEGER",
            "value" : 0
          }
        ]
      }
    ]
  }
}
```
