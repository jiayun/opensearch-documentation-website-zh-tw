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
POST /_plugins/_ml/models/{model_id}/_predict
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `model_id` | 字串 | 模型 ID。必要。 |
| `algorithm_name` | 字串 | 演算法名稱，例如 `kmeans`、`text_embedding` 或 `remote`。名稱不區分大小寫。如果您使用 `/_plugins/_ml/models/{model_id}/_predict` 端點，OpenSearch 會使用模型的演算法。 |

## 請求本文欄位

下表列出可用的請求欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:---  | :--- | :--- | :---
`parameters` | 物件 | 選用 | 模型專屬的預測參數。
`parameters.input_processors` | 陣列 | 選用 | 在將輸入資料傳送給模型之前，用來轉換輸入資料的處理器清單。如需詳細資訊，請參閱[處理器鏈]({{site.url}}{{site.baseurl}}/ml-commons-plugin/processor-chain/)。
`parameters.output_processors` | 陣列 | 選用 | 用來轉換模型輸出資料的處理器清單。如需詳細資訊，請參閱[處理器鏈]({{site.url}}{{site.baseurl}}/ml-commons-plugin/processor-chain/)。
`input_index` | 陣列 | 選用 | 對於使用 [Train API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/train/) 訓練的模型，這是包含要預測之資料的索引清單。
`input_query` | 物件 | 選用 | 對於使用 Train API 訓練的模型，這是從 `input_index` 中選取文件的搜尋查詢。
`input_data` | 物件 | 選用 | 對於使用 Train API 訓練的模型，這是要預測的資料，直接以包含 `column_metas` 和 `rows` 的資料框提供。
`text_docs` | 陣列 | 選用 | 對於本機文字嵌入、稀疏編碼及文字相似度模型，這是輸入文字的清單。
`query_text` | 字串 | 選用 | 對於文字相似度模型，這是與 `text_docs` 中每個項目比對的查詢文字。
`return_number` | 布林值 | 選用 | 對於本機文字嵌入模型，指定是否以數字形式傳回嵌入。預設值為 `true`。
`target_response` | 陣列 | 選用 | 對於本機文字嵌入模型，這是要傳回的模型輸出名稱清單，例如 `sentence_embedding`。
`question` | 字串 | 選用 | 對於問答模型，這是要回答的問題。
`context` | 字串 | 選用 | 對於問答模型，這是包含答案的文字。

對於外部託管的模型，實際的輸入欄位取決於模型的連接器組態。如需詳細資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

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
