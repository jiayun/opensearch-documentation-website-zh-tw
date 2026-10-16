---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分頁顯示結果"
parent: Customizing search results
nav_order: 10
redirect_from:
  - /opensearch/search/paginate/
---

# 分頁顯示結果

您可以使用下列方法在 OpenSearch 中對搜尋結果進行分頁：

1. [`from` 與 `size` 參數](#the-from-and-size-parameters)
1. [scroll 搜尋](#scroll-search)操作
1. [`search_after` 參數](#the-search_after-parameter)
1. [搭配 `search_after` 的 Point in Time](#point-in-time-with-search_after)

## `from` 與 `size` 參數

`from` 與 `size` 參數會一次傳回一頁結果。

`from` 參數是您想要開始顯示結果的文件編號。`size` 參數是您想要顯示的結果數量。兩者搭配使用，可讓您傳回搜尋結果的子集。

例如，若 `size` 的值為 10 且 `from` 的值為 0，您會看到前 10 筆結果。若將 `from` 的值改為 10，您會看到接下來的 10 筆結果（因為結果的索引從 0 開始）。因此，若您想從第 11 筆結果開始查看，`from` 必須為 10。

```json
GET shakespeare/_search
{
  "from": 0,
  "size": 10,
  "query": {
    "match": {
      "play_name": "Hamlet"
    }
  }
}
```

請使用下列公式，根據頁碼計算 `from` 參數：

```json
from = size * (page_number - 1)
```

每次使用者選擇結果的下一頁時，您的應用程式都需要以遞增後的 `from` 值執行相同的搜尋查詢。

您也可以在搜尋 URI 中指定 `from` 與 `size` 參數：

```json
GET shakespeare/_search?from=0&size=10
```

若您未指定 `size`，搜尋會傳回 10 筆命中結果。若您只指定 `size` 參數，`from` 參數會預設為 0。

查詢結果深處的頁面成本很高。若要傳回從 `from` 開始的結果，每個分片都必須找出並排序其前 `from` + `size` 筆結果，然後協調節點必須合併並排序所有分片的結果。因此記憶體使用量與延遲會隨 `from` 的值增加。為保護叢集，當 `from` + `size` 超過 `index.max_result_window` 索引設定時，OpenSearch 會拒絕請求。預設值為 `10000`。若要翻閱更多結果，請使用 [`search_after`](#the-search_after-parameter) 或 [scroll](#scroll-search)。

若多份文件具有相同的排序值，例如相同的相關性分數，其順序在不同請求之間可能不同。這是因為請求可能由不同的分片副本服務，而這些副本以不同的內部順序儲存文件。如此一來，某份文件可能出現在兩個頁面上，或完全不出現。若要保持順序穩定，請新增一個每份文件都有唯一值的欄位作為最後一個排序欄位，或使用 [`preference`]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search/#the-preference-query-parameter) 參數（例如使用者的工作階段 ID 等值），將同一使用者的所有請求傳送到相同的分片副本。

`from` 與 `size` 參數是無狀態的，因此結果會以最新可用的資料為基礎。
這可能導致分頁不一致。
例如，假設使用者停留在結果的第一頁，然後前往第二頁。在這段期間，一份與使用者搜尋相關的新文件被編製索引並出現在第一頁。在這種情況下，第一頁的最後一筆結果會被推到第二頁，使用者會看到重複的結果（也就是第一頁與第二頁都顯示該筆最後的結果）。

請使用 `scroll` 操作來實現一致的分頁。`scroll` 操作會將搜尋情境保持開啟一段時間。在這段時間內，任何資料變更都不會影響結果。


## 捲動搜尋

`from` 和 `size` 參數無法傳回超過 `index.max_result_window` 限制的結果（預設為 10,000）。若要擷取更大的結果集，例如匯出所有符合查詢的文件，或在批次工作中處理這些文件，請使用 `scroll` 操作。`scroll` 操作可以傳回任意數量的結果。

若要使用捲動操作，請在請求標頭中新增 `scroll` 參數，並附上搜尋內容，告知 OpenSearch 您需要持續捲動多久。此搜尋內容必須夠長，足以處理單一批次的結果。

若要設定每個批次要傳回的結果數量，請使用 `size` 參數：

```json
GET shakespeare/_search?scroll=10m
{
  "size": 10000
}
```

OpenSearch 會快取結果並傳回捲動 ID，您可以使用該 ID 分批存取這些結果：

```json
"_scroll_id" : "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAUWdmpUZDhnRFBUcWFtV21nMmFwUGJEQQ=="
```

將此捲動 ID 傳遞給 `scroll` 操作，以取得下一批結果。請勿在路徑中包含索引名稱：捲動 ID 已識別初始搜尋的索引，且 OpenSearch 會拒絕 `<index>/_search/scroll` 的請求：

```json
GET _search/scroll
{
  "scroll": "10m",
  "scroll_id": "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAUWdmpUZDhnRFBUcWFtV21nMmFwUGJEQQ=="
}
```

使用此捲動 ID，只要搜尋內容仍處於開啟狀態，您就會以每批 10,000 筆的方式取得結果。一般而言，捲動 ID 在請求之間不會變更，但它*可能*會變更，因此請務必一律使用最新的捲動 ID。如果您未在設定的搜尋內容內傳送下一個捲動請求，`scroll` 操作不會傳回任何結果。

請持續傳送捲動請求，直到回應包含空的 `hits.hits` 陣列，這表示已傳回所有結果。如果初始搜尋請求包含彙總，這些彙總只會在第一個回應中傳回。

每個捲動請求都會將搜尋內容的到期時間重設為該請求中指定的 `scroll` 值，因此該值只需涵蓋處理一個批次所需的時間。如果捲動請求未包含 `scroll` 值，OpenSearch 會傳回該批次，然後關閉搜尋內容。`scroll` 值不能超過 `search.max_keep_alive` 叢集設定。預設為 `24h`。

如果您需要所有符合的文件，且其順序不重要，請依 `_doc` 排序。這是捲動時最有效率的排序順序：

```json
GET shakespeare/_search?scroll=10m
{
  "size": 10000,
  "sort": ["_doc"]
}
```
{% include copy-curl.html %}

若要更快擷取大型結果集，請使用切片捲動。切片會將一個捲動分割成數個獨立的捲動，稱為_切片_，您可以平行處理這些切片。在每個請求中，將 `slice.max` 設為切片總數，並將 `slice.id` 設為該請求所擷取的切片，範圍從 `0` 到 `max` 減 1。下列請求會擷取兩個切片中的第一個：

```json
GET shakespeare/_search?scroll=10m
{
  "slice": {
    "id": 0,
    "max": 2
  },
  "query": {
    "match_all": {}
  }
}
```
{% include copy-curl.html %}

若要擷取第二個切片，請傳送相同的請求，並將 `id` 設為 `1`：

```json
GET shakespeare/_search?scroll=10m
{
  "slice": {
    "id": 1,
    "max": 2
  },
  "query": {
    "match_all": {}
  }
}
```
{% include copy-curl.html %}

每個請求都會傳回自己的捲動 ID，您可以使用該 ID 在該切片中分頁。這些切片合起來包含與未切片捲動相同的文件，且每份文件只屬於一個切片。在 `shakespeare` 索引中，兩個切片分別包含 111,396 份文件中的 55,635 份和 55,761 份。

根據預設，OpenSearch 會先依分片，再依每個分片內文件 `_id` 的雜湊，將文件指派給切片。如果您要求的切片數多於分片數，則每個切片的第一個請求會很慢，且使用的記憶體與該分片中的文件數成正比，直到 OpenSearch 快取切片篩選器為止。請限制您平行查詢的切片數。

若要避免此成本，您可以藉由在 `slice.field` 中指定欄位，根據另一個欄位的 doc values 將文件指派給切片。該欄位必須符合下列需求：

- 該欄位必須是已啟用 [doc values]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/doc-values/) 的數值欄位。OpenSearch 會拒絕在 `keyword`、`text` 或其他非數值欄位上，或在已停用 doc values 的欄位上進行切片的請求。
- 每份文件必須恰好包含一個值。欄位包含多個值的文件可能會出現在多個切片中。
- 該值在文件編製索引後不得變更，以便每份文件在捲動期間都留在同一個切片中。
- 該欄位應有許多不同的值，以便文件平均分散於各切片。例如，在只會新增文件的索引中，時間戳記是不錯的選擇。

下列請求會根據 `line_id` 欄位將結果分割成兩個切片：

```json
GET shakespeare/_search?scroll=10m
{
  "slice": {
    "field": "line_id",
    "id": 0,
    "max": 2
  },
  "query": {
    "match_all": {}
  }
}
```
{% include copy-curl.html %}

您也可以使用相同的 `slice` 物件來切片 [Point in Time]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/point-in-time/) (PIT) 搜尋。OpenSearch 會拒絕在既未使用捲動也未使用 PIT 的搜尋中使用 `slice`。

切片數上限由捲動的 `index.max_slices_per_scroll` 索引設定，以及 PIT 搜尋的 `index.max_slices_per_pit` 索引設定所控制。兩個設定的預設值皆為 `1024`。OpenSearch 會拒絕 `slice.max` 值超過限制的請求。如需詳細資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。

完成捲動後，請關閉搜尋內容，因為它會持續耗用運算資源，直到逾時為止：

```json
DELETE _search/scroll/DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAcWdmpUZDhnRFBUcWFtV21nMmFwUGJEQQ==
```

#### 回應範例

```json
{
  "succeeded": true,
  "num_freed": 1
}
```

若要一次關閉多個捲動內容，請在請求本文中以陣列指定它們的 ID：

```json
DELETE _search/scroll
{
  "scroll_id": [
    "<scroll_id_1>",
    "<scroll_id_2>"
  ]
}
```

您也可以在 `scroll_id` 欄位中指定單一 ID，或在請求路徑中提供以逗號分隔的 ID 清單，例如 `DELETE _search/scroll/<scroll_id_1>,<scroll_id_2>`。

使用下列請求關閉所有開啟中的捲動內容：

```json
DELETE _search/scroll/_all
```

`scroll` 操作對應特定的時間戳記。在該時間戳記之後新增的文件不會被視為可能的結果。

開啟中的搜尋內容會持續耗用資源，直到被關閉或到期為止。在捲動開啟期間，OpenSearch 無法刪除已合併至新分段的舊分段，因為捲動仍在讀取這些分段。這會使用更多磁碟空間與檔案控制碼。在持續接收更新或刪除的索引上，開啟中的捲動也會使用更多堆積記憶體。每個節點最多允許 `search.max_open_scroll_context` 個開啟中的捲動內容。預設值為 `500`。若要檢查開啟中的捲動內容數量，請使用 Nodes Stats API 並查看 `scroll_current` 值：

```json
GET _nodes/stats/indices/search
```
{% include copy-curl.html %}

由於這項成本，請勿將 `scroll` 操作用於頻繁的使用者查詢。若要為使用者提供分頁，請將 `sort` 參數與 `search_after` 參數搭配使用。如果使用者必須在各頁面之間看到一致的結果，請將 `search_after` 與[時間點](#point-in-time-with-search_after)（Point in Time，PIT）結合使用。PIT 同樣會讓搜尋內容保持開啟，因此請將其 `keep_alive` 設定為應用程式所需的最短期間，並在不再需要 PIT 時將其刪除。

## `search_after` 參數

`search_after` 參數提供一個即時游標，會利用前一頁的結果來取得下一頁的結果。它類似於 `scroll` 操作，因為它旨在平行捲動多個查詢。只有在套用排序時才能使用 `search_after`。

例如，下列查詢先依台詞編號、再依台詞 ID，對劇作「Hamlet」的所有台詞進行排序，並擷取前三筆結果：

```json
GET shakespeare/_search
{
  "size": 3,
  "query": {
    "match": {
      "play_name": "Hamlet"
    }
  },
  "sort": [
    { "speech_number": "asc" },
    { "line_id": "asc" }
  ]
}
```

回應包含每份文件的 `sort` 值陣列：

```json
{
  "took" : 7,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 4244,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [
      {
        "_index" : "shakespeare",
        "_id" : "32435",
        "_score" : null,
        "_source" : {
          "type" : "line",
          "line_id" : 32436,
          "play_name" : "Hamlet",
          "speech_number" : 1,
          "line_number" : "1.1.1",
          "speaker" : "BERNARDO",
          "text_entry" : "Whos there?"
        },
        "sort" : [
          1,
          32436
        ]
      },
      {
        "_index" : "shakespeare",
        "_id" : "32634",
        "_score" : null,
        "_source" : {
          "type" : "line",
          "line_id" : 32635,
          "play_name" : "Hamlet",
          "speech_number" : 1,
          "line_number" : "1.2.1",
          "speaker" : "KING CLAUDIUS",
          "text_entry" : "Though yet of Hamlet our dear brothers death"
        },
        "sort" : [
          1,
          32635
        ]
      },
      {
        "_index" : "shakespeare",
        "_id" : "32635",
        "_score" : null,
        "_source" : {
          "type" : "line",
          "line_id" : 32636,
          "play_name" : "Hamlet",
          "speech_number" : 1,
          "line_number" : "1.2.2",
          "speaker" : "KING CLAUDIUS",
          "text_entry" : "The memory be green, and that it us befitted"
        },
        "sort" : [
          1,
          32636
        ]
      }
    ]
  }
}
```

您可以使用最後一筆結果的 `sort` 值，透過 `search_after` 參數擷取下一筆結果：

```json
GET shakespeare/_search
{
  "size": 10,
  "query": {
    "match": {
      "play_name": "Hamlet"
    }
  },
  "search_after": [ 1, 32636],
  "sort": [
    { "speech_number": "asc" },
    { "line_id": "asc" }
  ]
}
```

與 `scroll` 操作不同，`search_after` 參數是無狀態的，因此文件順序可能會因文件被編製索引或刪除而改變。由於每個請求都依賴前一頁的 `sort` 值，`search_after` 一次只能向前移動一頁。您無法使用它跳到任意頁面。

使用 `search_after` 時，`from` 參數必須是 `0` 或省略。OpenSearch 會拒絕指定任何其他值的請求。

請在 `sort` 陣列的最後一個欄位加入一個對每份文件都有唯一值的欄位。此欄位充當 _tiebreaker_（決勝欄位）：若沒有它，對所有其他排序欄位具有相同值的文件就沒有明確的順序，分頁時可能會略過或重複這些文件。在上述範例中，`line_id` 對每句台詞都是唯一的，因此可作為具有相同 `speech_number` 之文件的決勝欄位。

請避免使用 `_id` 欄位作為決勝欄位。`_id` 欄位沒有 doc values，因此依它排序會將所有文件 ID 載入記憶體。此外，它只在單一索引內唯一，無法為來自不同索引的文件決勝。請改為在編製文件索引時，於應用程式中或使用 [`set` 資料匯入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/set/)，將文件 ID 複製到 `keyword` 欄位，並依該欄位排序。

## 搭配 `search_after` 的 Point in Time

搭配 `search_after` 的 Point in Time (PIT) 是 OpenSearch 中建議使用的分頁方法，尤其適用於深層分頁。它避開了所有其他方法的限制，因為它作用於時間凍結的資料集、不受查詢約束，並且支援向前與向後的一致性分頁。若要了解更多，請參閱 [Point in Time]({{site.url}}{{site.baseurl}}/opensearch/point-in-time/)。