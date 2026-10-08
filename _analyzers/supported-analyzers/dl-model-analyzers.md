---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "DL 模型分析器"
parent: Analyzers
nav_order: 130
---

# DL 模型分析器

深度學習 (DL) 模型分析器專為搭配[神經稀疏搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-search/)使用而設計。這些分析器實作與機器學習 (ML) 模型相同的斷詞規則，以確保與神經稀疏搜尋相容。傳統的 OpenSearch 分析器使用以規則為基礎的標準斷詞方式（例如空白字元或字詞邊界），而 DL 模型分析器則使用與特定 ML 模型相符的斷詞規則（例如 BERT WordPiece 斷詞方式）。已編製索引的文件與搜尋查詢之間保持一致的斷詞，是神經稀疏搜尋正確運作的關鍵。

OpenSearch 支援下列 DL 模型分析器：

* [`bert-uncased`](#the-bert-uncased-analyzer)：以 [google-bert/bert-base-uncased](https://huggingface.co/google-bert/bert-base-uncased) 模型斷詞器為基礎的分析器。
* [`mbert-uncased`](#the-mbert-uncased-analyzer)：以 [google-bert/bert-base-multilingual-uncased](https://huggingface.co/google-bert/bert-base-multilingual-uncased) 模型斷詞器為基礎的多語言分析器。

## 使用考量

使用 DL 模型分析器時，請留意下列考量事項：

* 這些分析器採用延遲載入。由於需要載入相依項目與相關資源，第一次呼叫這些分析器可能需要較長的時間。
* 這些斷詞器遵循與其對應模型斷詞器相同的規則。

## bert-uncased 分析器

`bert-uncased` 分析器以 [google-bert/bert-base-uncased](https://huggingface.co/google-bert/bert-base-uncased) 模型為基礎，並依據 BERT WordPiece 斷詞方式將文字斷詞。此分析器特別適用於英文文字。

若要使用 `bert-uncased` 分析器分析文字，請在 `analyzer` 欄位中指定該分析器：

```json
POST /_analyze
{
  "analyzer": "bert-uncased",
  "text": "It's fun to contribute to OpenSearch!"
}
```
{% include copy-curl.html %}

## mbert-uncased 分析器

`mbert-uncased` 分析器以 [google-bert/bert-base-multilingual-uncased](https://huggingface.co/google-bert/bert-base-multilingual-uncased) 模型為基礎，支援跨多種語言的斷詞。因此，此分析器適合處理多語言內容的應用程式。

若要分析多語言文字，請在請求中指定 `mbert-uncased` 分析器：

```json
POST /_analyze
{
  "analyzer": "mbert-uncased",
  "text": "It's fun to contribute to OpenSearch!"
}
```
{% include copy-curl.html %}

## 範例

如需在神經稀疏搜尋查詢中使用 DL 模型分析器的完整範例，請參閱[自動產生稀疏向量嵌入]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-with-pipelines/)。