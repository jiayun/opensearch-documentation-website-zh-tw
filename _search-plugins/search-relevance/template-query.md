---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "範本查詢"
nav_order: 70
parent: Query rewriting
grand_parent: Optimizing search quality
has_children: false
has_toc: false
---

# 範本查詢
**於 2.19 版推出**
{: .label .label-purple }

範本查詢可讓您建立含有動態預留位置的查詢，這些預留位置會在查詢執行期間由搜尋請求處理器解析。當您的查詢參數需要在搜尋過程中產生或轉換時，這項功能特別有用，例如使用機器學習（ML）推論將文字轉換為向量嵌入。

下列搜尋實作可受益於範本查詢：

- 將輸入文字轉換為向量嵌入，以進行向量搜尋
- 根據執行階段的計算結果動態產生查詢參數
- 需要中間處理的複雜查詢轉換

預留位置使用 `"${variable_name}"` 語法定義（請注意，變數必須以引號括住）。搜尋請求處理器可以在處理查詢之前產生或轉換資料，以填入這些預留位置。範本查詢充當最終可執行查詢的容器。

## 範例 

下列範例示範如何搭配 [`ml_inference` 搜尋請求處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/ml-inference-search-request/)使用範本查詢，以進行語意搜尋。

### 先決條件

使用 `ml_inference` 搜尋請求處理器之前，您必須先設定 ML 模型。如需本機模型的詳細資訊，請參閱[在 OpenSearch 中使用 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/using-ml-models/)。如需外部託管模型的詳細資訊，請參閱[連線至外部託管模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。 

設定模型後，您可以傳送 Predict API 請求來測試模型：

```json
POST /_plugins/_ml/models/mBGzipQB2gmRjlv_dOoB/_predict
{
  "parameters": {
    "inputText": "happy moments"
  }
}
```
{% include copy-curl.html %}

回應包含 `embedding` 欄位，其中有從 `inputText` 產生的向量嵌入： 

```json
{
    "inference_results": [
    {
        "output": [
        {
            "name": "response",
            "dataAsMap": {
            "embedding": [
                0.6328125,
                0.26953125,
                0.41796875,
                -0.00579833984375,
                1.859375,
                0.2734375,
                0.130859375,
                -0.001007080078125,
                0.138671875,
                ...],
            "inputTextTokenCount": 2
            }
        }
        ],
        "status_code": 200
    }
    ]
}
```
 
### 步驟 1：建立資料匯入管線

建立資料匯入管線，以便在將文件編製索引時，從文字欄位產生向量嵌入。`input_map` 將文件欄位對應至模型輸入。在此範例中，文件中的 `text` 來源欄位會對應至 `inputText` 欄位，也就是模型預期的輸入欄位。`output_map` 將模型輸出對應至文件欄位。在此範例中，模型的 `embedding` 輸出欄位會對應至您文件中的 `text_embedding` 目的地欄位：

```json
PUT /_ingest/pipeline/knn_pipeline
{
  "description": "knn_pipeline",
  "processors": [
    {
      "ml_inference": {
        "model_id": "Sz-wFZQBUpPSu0bsJTBG",
        "input_map": [
          {
            "inputText": "text"
          }
        ],
        "output_map": [
          {
            "text_embedding": "embedding"
          }
        ]
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 2：將文件編製索引

將下列文件編製索引至 `template-knn-1` 索引：

```json
PUT /template-knn-1/_doc/1
{
  "text": "red shoes"
}
```
{% include copy-curl.html %}

若要檢視文件，請傳送 GET 請求：

```json
GET /template-knn-1/_doc/1
```
{% include copy-curl.html %}

回應顯示，模型產生的嵌入會與原始 `text` 一併儲存在 `text_embedding` 欄位中：

```json
{
    "_index": "template-knn-1",
    "_id": "1",
    "_version": 2,
    "_seq_no": 1,
    "_primary_term": 1,
    "found": true,
    "_source": {
    "text_embedding": [
        -0.69140625,
        0.8125,
        0.51953125,
        -0.7421875,
        0.6875,
        0.4765625,
        -0.34375,
        ...],
    "text": "red shoes"
    }
}
```

### 步驟 3：使用範本查詢進行搜尋

使用下列範本查詢來搜尋索引。`ml_inference` 處理器會從輸入文字 `sneakers` 產生向量嵌入，以產生的向量取代 `${text_embedding}`，並搜尋最接近該向量的文件：

```json
GET /template-knn-1/_search?search_pipeline=my_knn_pipeline
{
  "query": {
    "template": {
      "knn": {
        "text_embedding": {
          "vector": "${text_embedding}",
          "k": 2
        }
      }
    }
  },
  "ext": {
    "ml_inference": {
      "text": "sneakers"
    }
  }
}
```
{% include copy-curl.html %}
   
回應包含符合條件的文件：

```json
{
    "took": 611,
    "timed_out": false,
    "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
    },
    "hits": {
    "total": {
        "value": 1,
        "relation": "eq"
    },
    "max_score": 0.0019327316,
    "hits": [
        {
        "_index": "template-knn-1",
        "_id": "1",
        "_score": 0.0019327316,
        "_source": {
            "text_embedding": [
            -0.69140625,
            0.8125,
            0.51953125,
            ..],
            "text": "red shoes"
        }
        }
    ]
    }
}
```

## 相關文件

- [範本查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/template/)
- [ML 推論搜尋請求處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/ml-inference-search-request/)