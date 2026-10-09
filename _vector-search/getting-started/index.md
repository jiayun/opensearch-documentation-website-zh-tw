---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "入門"
nav_order: 10
has_children: true
has_toc: false
redirect_from:
  - /vector-search/getting-started/
---

# 向量搜尋入門

本指南說明如何在 OpenSearch 中使用您自己的向量。您將學會建立向量索引、新增位置資料，並執行向量搜尋，在座標平面上找出最近的飯店。雖然這個範例為了簡化而使用二維向量，但相同做法也適用於語意搜尋和推薦系統中使用的高維向量。


## 先決條件：安裝 OpenSearch
  

<details markdown="block">
  <summary>
  如果您尚未安裝 OpenSearch，請依照下列步驟建立叢集。
  </summary>

開始之前，請確認您的環境中已安裝並執行 [Docker](https://docs.docker.com/get-docker/)。<br>
此示範組態並不安全，不應在正式環境中使用。
{: .note} 

下載並執行 OpenSearch：

```bash
docker pull opensearchproject/opensearch:latest && docker run -it -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -e "DISABLE_SECURITY_PLUGIN=true" opensearchproject/opensearch:latest
```
{% include copy.html %}

OpenSearch 現在執行於連接埠 9200。若要確認 OpenSearch 正在執行，請傳送下列請求：

```bash
curl http://localhost:9200
```
{% include copy.html %}

您應該會收到類似以下的回應：

```json
{
  "name" : "a937e018cee5",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "GLAjAG6bTeWErFUy_d-CLw",
  "version" : {
    "distribution" : "opensearch",
    "number" : <version>,
    "build_type" : <build-type>,
    "build_hash" : <build-hash>,
    "build_date" : <build-date>,
    "build_snapshot" : false,
    "lucene_version" : <lucene-version>,
    "minimum_wire_compatibility_version" : "7.10.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "The OpenSearch Project: https://opensearch.org/"
}
```

如需更多資訊，請參閱[安裝快速入門]({{site.url}}{{site.baseurl}}/getting-started/quickstart/)和[安裝及設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/)。

</details>

## 執行 API 請求

本指南包含 API 請求範例，您可以用幾種方式執行：

- **OpenSearch Dashboards Dev Tools 主控台**（建議）：在 `http://localhost:5601` 開啟 OpenSearch Dashboards，選取右上角的 **Dev Tools**，然後貼上請求。選取該請求並選擇播放按鈕。如需更多資訊，請參閱[在主控台中執行查詢]({{site.url}}{{site.baseurl}}/dashboards/visualize/run-queries/)。
- **cURL**：使用每個程式碼範例旁的 **Copy as cURL** 按鈕，以 cURL 格式複製請求，然後在終端機中貼上並執行。

## 步驟 1：建立向量索引

首先，建立一個將儲存範例飯店資料的索引。若要向 OpenSearch 表示這是向量索引，請將 `index.knn` 設為 `true`。您會將向量儲存在名為 `location` 的向量欄位中。您將匯入的向量是二維的，而向量之間的距離會使用[歐幾里得 `l2` 相似度計量]({{site.url}}{{site.baseurl}}/vector-search/getting-started/vector-search-basics/#calculating-similarity)計算：

```json
PUT /hotels-index
{
  "settings": {
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "location": {
        "type": "knn_vector",
        "dimension": 2,
        "space_type": "l2"
      }
    }
  }
}
```
{% include copy-curl.html %}

若要使用不同的方法或引擎，請參閱[方法與引擎]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/)。

向量查詢通常會有 `size` > 0，因此預設不會進入請求快取。在 OpenSearch 2.19 或更新版本中，如果您的工作負載大多由向量查詢組成，請考慮將動態 `indices.requests.cache.maximum_cacheable_size` 叢集設定調高為更大的值，例如 `256`。這可讓 `size` 最高為 256 的查詢進入請求快取，進而提升效能。如需更多資訊，請參閱[請求快取]({{site.url}}{{site.baseurl}}/search-plugins/caching/request-cache/)。

## 步驟 2：將資料新增至您的索引

接著，將資料新增至您的索引。每份文件代表一間飯店。每份文件中的 `location` 欄位包含指定該飯店位置的二維向量：

```json
POST /_bulk
{ "index": { "_index": "hotels-index", "_id": "1" } }
{ "location": [5.2, 4.4] }
{ "index": { "_index": "hotels-index", "_id": "2" } }
{ "location": [5.2, 3.9] }
{ "index": { "_index": "hotels-index", "_id": "3" } }
{ "location": [4.9, 3.4] }
{ "index": { "_index": "hotels-index", "_id": "4" } }
{ "location": [4.2, 4.6] }
{ "index": { "_index": "hotels-index", "_id": "5" } }
{ "location": [3.3, 4.5] }
```
{% include copy-curl.html %}

## 步驟 3：搜尋您的資料

現在搜尋最接近圖釘位置 `[5, 4]` 的飯店。若要搜尋最接近的三間飯店，請將 `k` 設為 `3`：

```json
POST /hotels-index/_search
{
  "size": 3,
  "query": {
    "knn": {
      "location": {
        "vector": [5, 4],
        "k": 3
      }
    }
  }
}
```
{% include copy-curl.html %}

下圖顯示座標平面上的飯店。查詢點標示為 `Pin`，而每間飯店都標有其文件編號。

![座標平面上的飯店]({{site.url}}{{site.baseurl}}/images/k-nn-search-hotels.png){:style="width: 400px;" class="img-centered"}

回應包含最接近指定圖釘位置的飯店：

```json
{
  "took": 1093,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 0.952381,
    "hits": [
      {
        "_index": "hotels-index",
        "_id": "2",
        "_score": 0.952381,
        "_source": {
          "location": [
            5.2,
            3.9
          ]
        }
      },
      {
        "_index": "hotels-index",
        "_id": "1",
        "_score": 0.8333333,
        "_source": {
          "location": [
            5.2,
            4.4
          ]
        }
      },
      {
        "_index": "hotels-index",
        "_id": "3",
        "_score": 0.72992706,
        "_source": {
          "location": [
            4.9,
            3.4
          ]
        }
      }
    ]
  }
}
```

## 自動產生向量嵌入

如果您的資料尚未是向量格式，您可以直接在 OpenSearch 中產生向量嵌入。這可讓您將文字或圖片轉換為其數值表示，以進行相似度搜尋。如需更多資訊，請參閱[自動產生向量嵌入]({{site.url}}{{site.baseurl}}/vector-search/getting-started/auto-generated-embeddings/)。

## 後續步驟

- [向量搜尋基本概念]({{site.url}}{{site.baseurl}}/vector-search/getting-started/vector-search-basics/)
- [準備向量]({{site.url}}{{site.baseurl}}/vector-search/getting-started/vector-search-options/)
- [使用篩選條件的向量搜尋]({{site.url}}{{site.baseurl}}/vector-search/filter-search-knn/)
- [自動產生向量嵌入]({{site.url}}{{site.baseurl}}/vector-search/getting-started/auto-generated-embeddings/)