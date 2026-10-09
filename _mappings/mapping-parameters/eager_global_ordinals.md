---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "預先載入全域序數"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/eager_global_ordinals/
nav_order: 35
has_children: false
has_toc: false
---

# 預先載入全域序數對應參數

`eager_global_ordinals` 對應參數控制何時為欄位建立全域序數。啟用時，全域序數會在索引重新整理期間計算，而不是在查詢執行期間「延遲」計算。這可以改善依賴全域序數之作業的效能，例如關鍵字欄位的排序與彙總。不過，這也可能增加索引重新整理時間與記憶體使用量。

全域序數代表詞彙值到整數識別碼的對應，會在內部用於快速執行彙總與排序作業。透過「預先」載入全域序數，系統可降低查詢延遲，代價是在索引期間進行額外的前置處理。

預設情況下，`eager_global_ordinals` 為停用狀態，以確保叢集針對索引速度進行最佳化。

全域序數儲存在欄位資料快取中，並消耗堆積記憶體。高基數的欄位可能消耗大量堆積記憶體。為避免記憶體相關問題，請務必仔細設定 [欄位資料斷路器設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/circuit-breaker/#field-data-circuit-breaker-settings)。

## 何時使用全域序數

當搜尋包含下列任一項目時，會使用全域序數：

- 對 `keyword`、`ip` 與 `flattened` 欄位進行的桶彙總。這包括 `terms`、`composite`、`diversified_sampler` 與 `significant_terms` 彙總。
- 對 `text` 欄位進行且需要啟用 `fielddata` 的彙總。
- 使用 [`join`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/join/) 欄位的父/子查詢，例如 [`has_child`]({{site.url}}{{site.baseurl}}/query-dsl/joining/has-child/) 查詢或 `parent` 彙總。


## 在欄位上啟用預先載入全域序數

下列請求會建立名為 `products` 的索引並啟用 `eager_global_ordinals`：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "size": {
        "type": "keyword",
        "eager_global_ordinals": true
      }
    }
  }
}
```
{% include copy-curl.html %}

下列請求會將文件編製索引：

```json
PUT /products/_doc/1
{
  "size": "ABC123"
}
```
{% include copy-curl.html %}

下列請求會執行 `terms` 彙總：

```json
POST /products/_search
{
  "size": 0,
  "aggs": {
    "size_agg": {
      "terms": {
        "field": "size"
      }
    }
  }
}
```
{% include copy-curl.html %}
