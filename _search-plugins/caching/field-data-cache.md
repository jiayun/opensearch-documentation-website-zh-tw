---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "欄位資料快取"
parent: Caching
grand_parent: Improving search performance
nav_order: 20
---

# 欄位資料快取

欄位資料快取是節點層級的記憶體內快取，用於儲存欄位資料與全域序數。這些是資料結構，可讓您對經過分析的文字欄位進行彙總與排序。由於運算成本可能很高，因此建立後會加以快取，以便日後需要重複使用。

## 什麼是欄位資料

欄位資料是一種資料結構，可讓您對文字欄位進行快速排序與彙總。文字欄位儲存於反向索引中，該索引針對快速搜尋特定詞元進行最佳化，而非逐一走訪個別文件。由於彙總或排序需要這項功能，OpenSearch 必須將反向索引處理成另一種針對個別文件存取最佳化的資料結構。

## 什麼是全域序數

在對特定欄位運算彙總時，每個 Lucene 分段會為每個唯一詞元指派一個唯一的序數，藉此支援桶彙總等功能。在整個叢集上運算彙總時，必須為每個全域唯一的詞元建立全域序數，並儲存這些全域序數與分段序數之間的對應。這可讓您合併每個分段的彙總結果。此對應隨後會儲存在欄位資料快取中，以供日後的彙總重複使用。

如果欄位具有對應參數 `"eager_global_ordinals": true`（預設為 `false`），則全域序數會在索引重新整理時計算並儲存，而非在查詢時延遲計算。

如需全域序數的詳細資訊，請參閱 [預先建立全域序數]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/eager_global_ordinals/)。

## 最佳實務

根據預設，文字欄位會停用欄位資料，因為它可能耗用大量堆積記憶體。如果您想要對文字欄位進行排序或彙總，建議您改為建立 keyword 子欄位。Keyword 欄位不會經過分析，因此不會儲存在反向索引中，也不需要為彙總建立個別的資料結構。

如果您想要直接在文字欄位上啟用排序或彙總，請在該欄位的對應中設定 `"fielddata": true`。

## 設定欄位資料快取 

設定 | 資料類型  | 預設 | 層級 | 靜態/動態 | 說明
:--- |:-----------|:--------| :--- | :--- | :---
`indices.breaker.fielddata.limit` | 百分比  | `40%`  | 叢集 | 動態 | 設定欄位資料快取大小上限，超過此上限時，若傳入的請求需要在快取中放入更多項目，將會被斷路器擋下。 
`indices.fielddata.cache.size` | 位元組大小或總堆積記憶體大小的百分比 | `35%` | 叢集 | 動態 | 設定欄位資料快取大小上限，超過此上限時將會發生逐出。此值必須小於斷路器上限。若設為 -1，則此上限不適用，只有斷路器上限會生效。

## 監視欄位資料快取 

[Nodes Stats API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/) 會傳回叢集中所有節點的快取統計資料：

```json
GET /_nodes/stats/indices/fielddata
```
{% include copy-curl.html %}

回應會包含快取統計資料：

```json
{
  "nodes" : {
    "oeR83dkUSPmnQqzBEGc4fQ" : {
      "indices" : {
        "fielddata" : {
          "memory_size_in_bytes" : 0,
          "evictions" : 0,
          "item_count" : 0
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

您可以提供參數 `level=indices` 來依索引彙總這些值。 

您也可以使用 [Cat Field Data API]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-field-data/) 取得每個節點上每個欄位的欄位資料大小清單。 