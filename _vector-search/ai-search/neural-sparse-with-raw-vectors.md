---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用原始向量進行神經稀疏搜尋"
parent: Neural sparse search
grand_parent: AI search
nav_order: 30
has_children: false
redirect_from:
  - /search-plugins/neural-sparse-with-raw-vectors/
---

# 使用原始向量進行神經稀疏搜尋

如果您使用自架的稀疏嵌入模型，您可以匯入原始稀疏向量，以供神經稀疏搜尋使用。

## 範例

下列範例會將稀疏向量匯入 OpenSearch 索引，然後使用稀疏向量搜尋相符的文件。

### 步驟 1：建立索引

若要匯入包含原始稀疏向量的文件，請建立 rank features 索引：

```json
PUT /my-nlp-index
{
  "mappings": {
    "properties": {
      "id": {
        "type": "text"
      },
      "passage_embedding": {
        "type": "rank_features"
      },
      "passage_text": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

### 步驟 2：將文件匯入索引

若要將文件匯入上一個步驟所建立的索引，請傳送下列請求：

```json
PUT /my-nlp-index/_doc/1
{
  "passage_text": "Hello world",
  "id": "s1",
  "passage_embedding": {
    "hi" : 4.338913,
    "planets" : 2.7755864,
    "planet" : 5.0969057,
    "mars" : 1.7405145,
    "earth" : 2.6087382,
    "hello" : 3.3210192
  }
}
```
{% include copy-curl.html %}

### 步驟 3：使用稀疏向量搜尋資料

若要使用稀疏向量搜尋文件，請在 `neural_sparse` 查詢中提供稀疏嵌入：

```json
GET my-nlp-index/_search
{
  "query": {
    "neural_sparse": {
      "passage_embedding": {
        "query_tokens": {
          "hi" : 4.338913,
          "planets" : 2.7755864,
          "planet" : 5.0969057,
          "mars" : 1.7405145,
          "earth" : 2.6087382,
          "hello" : 3.3210192
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 加速神經稀疏搜尋

若要進一步了解如何改善神經稀疏搜尋的擷取時間，請參閱[加速神經稀疏搜尋]({{site.url}}{{site.baseurl}}/search-plugins/neural-sparse-search/#accelerating-neural-sparse-search)。

## 後續步驟

- 探索我們的[教學]({{site.url}}{{site.baseurl}}/vector-search/tutorials/)，了解如何建置 AI 搜尋應用程式。 
