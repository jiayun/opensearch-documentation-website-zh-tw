---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "匯入資料"
nav_order: 30
has_children: true
has_toc: false
redirect_from:
  - /vector-search/ingesting-data/
---

# 將資料匯入向量索引

建立向量索引之後，您需要匯入原始向量資料，或在匯入時將資料轉換為嵌入。

## 匯入方法比較

下表比較了這兩種匯入方法。

| 功能                       | 資料格式          | 資料匯入管線 | 向量產生         | 額外欄位            |
|-------------------------------|----------------------------|---------------------|---------------------------------|-----------------------------------|
| **原始向量匯入**      | 預先產生的向量      | 不需要        | 外部                        | 選用的中繼資料                |
| **匯入時將資料轉換為嵌入** | 文字或圖片資料                   | 需要            | 內部 (匯入期間)     | 原始資料 + 嵌入        |

## 原始向量匯入

使用在 OpenSearch 之外產生的原始向量或嵌入時，您可以直接將向量資料匯入 `knn_vector` 欄位。不需要管線，因為向量已經產生：

```json
PUT /my-raw-vector-index/_doc/1
{
  "my_vector": [0.1, 0.2, 0.3],
  "metadata": "Optional additional information"
}
```
{% include copy-curl.html %}

您也可以使用 [Bulk API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) 有效地匯入多個向量：

```json
PUT /_bulk
{"index": {"_index": "my-raw-vector-index", "_id": 1}}
{"my_vector": [0.1, 0.2, 0.3], "metadata": "First item"}
{"index": {"_index": "my-raw-vector-index", "_id": 2}}
{"my_vector": [0.2, 0.3, 0.4], "metadata": "Second item"}
```
{% include copy-curl.html %}

## 匯入時將資料轉換為嵌入

[設定好會自動產生嵌入的資料匯入管線]({{site.url}}{{site.baseurl}}/vector-search/creating-vector-index/#converting-data-to-embeddings-during-ingestion)之後，您可以直接將文字資料匯入索引：

```json
PUT /my-ai-search-index/_doc/1
{
  "input_text": "Example: AI search description"
}
```
{% include copy-curl.html %}

管線會自動產生嵌入並儲存在 `output_embedding` 欄位中。

您也可以使用 [Bulk API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) 有效地匯入多份文件：

```json
PUT /_bulk
{"index": {"_index": "my-ai-search-index", "_id": 1}}
{"input_text": "Example AI search description"}
{"index": {"_index": "my-ai-search-index", "_id": 2}}
{"input_text": "Bulk API operation description"}
```
{% include copy-curl.html %}

## 使用稀疏向量

OpenSearch 也支援稀疏向量。如需更多資訊，請參閱[神經稀疏搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-search/)。

## 文字分塊

如需在稠密或稀疏 AI 搜尋中產生嵌入之前，將大型文件分割成較小段落的資訊，請參閱[文字分塊]({{site.url}}{{site.baseurl}}/vector-search/ingesting-data/text-chunking/)。

## 後續步驟

- [搜尋向量資料]({{site.url}}{{site.baseurl}}/vector-search/searching-data/)
- [Bulk API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/)
- [資料匯入管線]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/index/)
- [文字嵌入處理器]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/processors/text-embedding/)