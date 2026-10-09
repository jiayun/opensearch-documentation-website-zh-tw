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

`from` 與 `size` 參數會一次一頁地傳回結果。

`from` 參數是您希望開始顯示結果的文件編號。`size` 參數是您希望顯示的結果數量。兩者搭配使用，可讓您傳回搜尋結果的子集。

例如，若 `size` 的值為 10 且 `from` 的值為 0，您會看到前 10 筆結果。若將 `from` 的值改為 10，您會看到接下來的 10 筆結果（因為結果是從零開始編號）。因此，若您想從第 11 筆結果開始查看，`from` 必須為 10。

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

每當使用者選擇結果的下一頁時，您的應用程式都需要以遞增後的 `from` 值執行相同的搜尋查詢。

您也可以在搜尋 URI 中指定 `from` 與 `size` 參數：

```json
GET shakespeare/_search?from=0&size=10
```

若您只指定 `size` 參數，`from` 參數會預設為 0。

查詢結果深處的頁面可能對效能造成重大影響，因此 OpenSearch 將此方法限制為 10,000 筆結果。

`from` 與 `size` 參數是無狀態的，因此結果會以最新可用的資料為基礎。
這可能導致分頁不一致。
例如，假設使用者停留在結果的第一頁，然後前往第二頁。在這段期間，一筆與使用者搜尋相關的新文件被編製索引並出現在第一頁。在這種情況下，第一頁的最後一筆結果會被推到第二頁，使用者會看到重複的結果（也就是第一頁與第二頁都顯示該筆最後的結果）。

請使用 `scroll` 操作來實現一致的分頁。`scroll` 操作會將搜尋情境保持開啟一段時間。在這段時間內，任何資料變更都不會影響結果。


## Scroll 搜尋

`from` 與 `size` 參數可讓您對搜尋結果進行分頁，但一次最多只能 10,000 筆結果。

如果您需要請求超過 1 PB 的資料量（例如來自機器學習工作），請改用 `scroll` 操作。`scroll` 操作可讓您請求不限數量的結果。

若要使用 scroll 操作，請在請求標頭中加入 `scroll` 參數，並在搜尋情境中告訴 OpenSearch 您需要持續捲動多久。此搜尋情境的時間必須足夠處理單一批次的結果。

若要設定每個批次要傳回的結果數量，請使用 `size` 參數：

```json
GET shakespeare/_search?scroll=10m
{
  "size": 10000
}
```

OpenSearch 會快取結果並傳回一個 scroll ID，您可以使用它在批次中存取這些結果：

```json
"_scroll_id" : "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAUWdmpUZDhnRFBUcWFtV21nMmFwUGJEQQ=="
```

將此 scroll ID 傳遞給 `scroll` 操作以取得下一批結果：

```json
GET _search/scroll
{
  "scroll": "10m",
  "scroll_id": "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAUWdmpUZDhnRFBUcWFtV21nMmFwUGJEQQ=="
}
```

只要搜尋情境仍處於開啟狀態，使用此 scroll ID 就能以每批 10,000 筆的方式取得結果。一般而言，scroll ID 在請求之間不會改變，但它*可能*會改變，因此請務必一律使用最新的 scroll ID。如果您未在設定的搜尋情境時間內傳送下一個 scroll 請求，`scroll` 操作將不會傳回任何結果。

如果您預期會有數十億筆結果，請使用 sliced scroll。切片 (slicing) 可讓您針對同一請求平行執行多個 scroll 操作。
設定 scroll 的 ID 與最大切片數：

```json
GET shakespeare/_search?scroll=10m
{
  "slice": {
    "id": 0,
    "max": 10
  },
  "query": {
    "match_all": {}
  }
}
```

使用單一 scroll ID，您會收到 10 筆結果。
您最多可以有 10 個 ID。
以 ID 等於 1 執行相同的命令：

```json
GET shakespeare/_search?scroll=10m
{
  "slice": {
    "id": 1,
    "max": 10
  },
  "query": {
    "match_all": {}
  }
}
```

捲動完成後，請關閉搜尋情境，因為它會持續消耗運算資源直到逾時：

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

請使用下列請求來關閉所有開啟的 scroll 情境：

```json
DELETE _search/scroll/_all
```

`scroll` 操作對應特定的時間戳記。它不會將該時間戳記之後新增的文件視為潛在結果。

由於開啟的搜尋情境會消耗大量記憶體，我們建議您不要在不需要保持搜尋情境開啟的頻繁使用者查詢中使用 `scroll` 操作。請改用 `sort` 參數搭配 `search_after` 參數來捲動使用者查詢的回應。

## `search_after` 參數

`search_after` 參數提供一個即時游標，使用上一頁的結果來取得下一頁的結果。它類似於 `scroll` 操作，旨在平行捲動多個查詢。只有在套用排序時才能使用 `search_after`。

例如，下列查詢依台詞編號與台詞 ID 排序戲劇「Hamlet」中的所有台詞，並擷取前三筆結果：

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

與 `scroll` 操作不同，`search_after` 參數是無狀態的，因此文件順序可能因文件被編製索引或刪除而改變。

## 搭配 `search_after` 的 Point in Time

搭配 `search_after` 的 Point in Time (PIT) 是 OpenSearch 中建議使用的分頁方法，尤其適用於深層分頁。它避開了所有其他方法的限制，因為它作用於時間凍結的資料集、不受查詢約束，並且支援向前與向後的一致性分頁。若要了解更多，請參閱 [Point in Time]({{site.url}}{{site.baseurl}}/opensearch/point-in-time/)。