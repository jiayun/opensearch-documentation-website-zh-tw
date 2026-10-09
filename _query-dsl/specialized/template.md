---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "範本"
parent: AI and vector search queries
nav_order: 70
---

# Template 查詢
於 2.19 版推出
{: .label .label-purple }

使用 `template` 查詢來建立包含預留位置變數的搜尋查詢。預留位置使用 `"${variable_name}"` 語法指定（請注意，變數必須以引號括住）。當您提交搜尋請求時，這些預留位置會保持未解析狀態，直到搜尋請求處理器處理它們為止。當您的初始搜尋請求包含需要在執行階段轉換或產生的資料時，這種方法特別有用。

舉例來說，當您使用 [ml_inference 搜尋請求處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/ml-inference-search-request/) 時，可能會使用 template 查詢，該處理器會在搜尋過程中將文字輸入轉換為向量嵌入。處理器會在最終查詢執行之前，以產生的值取代預留位置。

如需完整範例，請參閱[使用 template 查詢改寫查詢]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/template-query/)。

本頁說明 `template` 查詢，其使用由搜尋請求處理器（例如 ML 推論）在執行階段解析的預留位置變數。如果您想使用 Mustache 語法 (`{{variable}}`) 建立可重複使用、參數化的查詢，請參閱[搜尋範本 API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search-template/)。
{: .note}

## 範例

下列範例顯示帶有 `"vector": "${text_embedding}"` 預留位置的 template k-NN 查詢。預留位置 `"${text_embedding}"` 將由 `ml_inference` 搜尋請求處理器從 `text` 輸入欄位產生的嵌入取代：

```json
GET /template-knn-index/_search?search_pipeline=my_knn_pipeline
{
  "query": {
    "template": {
      "knn": {
        "text_embedding": {
          "vector": "${text_embedding}", // Placeholder for the vector field
          "k": 2
        }
      }
    }
  },
  "ext": {
    "ml_inference": {
      "text": "sneakers" // Input text for the ml_inference processor
    }
  }
}
```
{% include copy-curl.html %}

若要將 template 查詢與搜尋請求處理器搭配使用，您需要設定搜尋管線。以下是 `ml_inference` 搜尋請求處理器的範例組態。`input_map` 會將文件欄位對應至模型輸入。在此範例中，文件中的 `ext.ml_inference.text` 來源欄位會對應至 `inputText` 欄位，也就是模型預期的輸入欄位。`output_map` 會將模型輸出對應至文件欄位。在此範例中，模型的 `embedding` 輸出欄位會對應至您文件中的 `text_embedding` 目的地欄位：

```json
PUT /_search/pipeline/my_knn_pipeline
{
  "request_processors": [
    {
      "ml_inference": {
        "model_id": "Sz-wFZQBUpPSu0bsJTBG",
        "input_map": [
          {
            "inputText": "ext.ml_inference.text" // Map input text from the request
          }
        ],
        "output_map": [
          {
            "text_embedding": "embedding" // Map output to the placeholder
          }
        ]
      }
    }
  ]
}
```
{% include copy-curl.html %}

`ml_inference` 搜尋請求處理器執行之後，搜尋請求會遭到改寫。`vector` 欄位包含處理器產生的嵌入，而 `text_embedding` 欄位包含處理器輸出：

```json
GET /template-knn-1/_search
{
  "query": {
    "template": {
      "knn": {
        "text_embedding": {
          "vector": [0.6328125, 0.26953125, ...], 
          "k": 2
        }
      }
    }
  },
  "ext": {
    "ml_inference": {
      "text": "sneakers",
      "text_embedding": [0.6328125, 0.26953125, ...] 
    }
  }
}
```
{% include copy-curl.html %}

## 限制

Template 查詢需要至少一個搜尋請求處理器，才能解析預留位置。搜尋請求處理器必須設定為產生管線中預期的變數。

## 後續步驟

- 如需完整範例，請參閱 [Template 查詢]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/template-query/)。