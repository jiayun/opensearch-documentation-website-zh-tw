---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "時間點"
parent: Customizing search results
nav_order: 20
redirect_from:
  - /opensearch/point-in-time/
  - /search-plugins/point-in-time/
---

# 時間點

時間點 (PIT) 可讓您對固定在某個時間點的資料集執行不同的查詢。

一般來說，如果您對某個索引執行查詢多次，相同的查詢可能會傳回不同的結果，因為文件會不斷地被編製索引、更新和刪除。如果您需要對相同的資料執行查詢，可以建立 PIT 來保留該資料的狀態。PIT 功能的主要用途是將其與 `search_after` 功能結合，以對搜尋結果進行深度分頁。

## 為搜尋結果分頁

除了 PIT 功能之外，在 OpenSearch 中還有三種[為搜尋結果分頁]({{site.url}}{{site.baseurl}}/opensearch/search/paginate/)的方式：使用 Scroll API、為您的搜尋指定 `from` 和 `size` 參數，以及使用 `search_after` 功能。然而，這三種方式都有其限制：

- Scroll API 的搜尋結果會在請求當下凍結，但它們會繫結至特定的查詢。此外，scroll 只能在搜尋中向前移動，因此如果某個頁面的請求失敗，後續的請求會略過該頁面並傳回下一頁。
- 如果您為搜尋指定 `from` 和 `size` 參數，搜尋結果不會凍結在時間點上，因此可能會因為文件被編製索引或刪除而不一致。不建議將 `from` 和 `size` 功能用於深度分頁，因為每個頁面請求都需要處理所有結果，並為所請求的頁面進行篩選。
- `search_after` 的搜尋結果不會凍結在時間點上，因此可能會因為文件同時被編製索引或刪除而不一致。

PIT 功能沒有其他分頁方法的限制，因為 PIT 搜尋不會繫結至查詢，且支援向前和向後的一致分頁。如果您已看過結果的第一頁，而現在位於第二頁，當您返回時仍會看到相同的第一頁。

## PIT 搜尋

PIT 搜尋與一般搜尋具有相同的能力，差別在於 PIT 搜尋會作用於較舊的資料集，而一般搜尋則作用於即時資料集。PIT 搜尋不會繫結至查詢，因此您可以對同一個凍結在時間點的資料集執行不同的查詢。

您可以使用 [Create PIT API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/point-in-time-api/#create-a-pit) 來建立 PIT。當您為一組索引建立 PIT 時，OpenSearch 會鎖定這些索引的一組分段，將其凍結在時間點上。在較低層級，此 PIT 所需的資源都不會被修改或刪除。如果屬於某個 PIT 的分段被合併，OpenSearch 會依建立 PIT 時透過 `keep_alive` 參數指定的期間保留這些分段的副本。

建立 PIT 作業會傳回 PIT ID，您可以使用它對凍結的資料集執行多個查詢。即使索引持續匯入資料並修改或刪除文件，PIT 仍會參考自建立 PIT 以來未曾變更的資料。當您的查詢包含 PIT ID 時，您不需要將索引傳遞給搜尋，因為它會使用該 PIT。使用 PIT ID 的搜尋在您執行多次時會產生完全相同的結果。

如果發生叢集或節點故障，所有 PIT 資料都會遺失。
{: .note}

### SQL 中的 PIT

[SQL 外掛程式]({{site.url}}{{site.baseurl}}/search-plugins/sql/index/)也支援使用 PIT 進行分頁。當 `plugin.sql.pagination.api` 設定啟用時 (預設)，OpenSearch 中的 SQL 搜尋查詢會在內部自動使用 PIT。如需更多資訊，請參閱 [SQL 中的分頁]({{site.url}}{{site.baseurl}}/search-plugins/sql/sql-ppl-api/#paginating-results)。

## 使用 PIT 和 search_after 進行分頁

當您使用 PIT ID 執行查詢時，可以使用 `search_after` 參數來擷取下一頁的結果。這可讓您控制結果頁面中文件的順序。

使用 PIT ID 執行搜尋查詢：

```json
GET /_search
{
  "size": 10000,
  "query": {
    "match" : {
      "user.id" : "elkbee"
    }
  },
  "pit": {
    "id":  "46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA==", 
    "keep_alive": "100m"
  },
  "sort": [ 
    {"@timestamp": {"order": "asc"}}
  ]
}
```

回應包含符合查詢的前 10,000 份文件。若要取得下一組文件，請使用最後一份文件的排序值作為 `search_after` 參數來執行相同的查詢，並保持相同的 `sort` 和 `pit.id`。您可以使用選用的 `keep_alive` 參數來延長 PIT 時間：

```json
GET /_search
{
  "size": 10000,
  "query": {
    "match" : {
      "user.id" : "elkbee"
    }
  },
  "pit": {
    "id":  "46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA==", 
    "keep_alive": "100m"
  },
  "sort": [ 
    {"@timestamp": {"order": "asc"}}
  ],
  "search_after": [  
    "2021-05-20T05:30:04.832Z"
  ]
}
```

## 搜尋切片

使用 `search_after` 搭配 PIT 進行分頁，可讓您控制結果的順序。如果您不需要依特定順序取得結果，或希望能從某一頁跳至不連續的另一頁，可以使用搜尋切片。搜尋切片會將 PIT 搜尋分割成多個切片，供用戶端應用程式各自獨立讀取。

例如，符合 1,000,000 份文件的 PIT 搜尋可以分割成 2 個切片，每個切片約有 500,000 份文件，讓用戶端應用程式中的兩個執行緒平行讀取。每個執行緒都使用 `search_after` 逐頁讀取自己的切片。所有切片都使用相同的 PIT ID。

若要使用搜尋切片，請在 `slice` 物件中指定下列參數：

- `slice.max` 是要將搜尋分割成的切片數量。此數量不得超過 `index.max_slices_per_pit` 索引設定（預設為 `1024`）。
- `slice.id` 是您請求的切片 ID，範圍從 `0` 到 `slice.max` - 1。

OpenSearch 會根據每份文件的分片與文件 ID，將文件指派至切片，因此各切片包含的文件數量大致相同，但不會完全相等。

下列請求會傳回兩個切片中的第一個：

```json
GET /_search
{
  "slice": {
    "id": 0,
    "max": 2
  },
  "query": {
    "match": {
      "message": "foo"
    }
  },
  "pit": {
    "id": "46ToAwMDaWR5BXV1aWQyKwZub2RlXzMAAAAAAAAAACoBYwADaWR4BXV1aWQxAgZub2RlXzEAAAAAAAAAAAEBYQADaWR5BXV1aWQyKgZub2RlXzIAAAAAAAAAAAwBYgACBXV1aWQyAAAFdXVpZDEAAQltYXRjaF9hbGw_gAAAAA=="
  }
}
```
{% include copy-curl.html %}

每個請求會傳回一個切片。若要請求第二個切片，請傳送相同的請求，並將 `slice.id` 設為 `1`。

每個切片的分頁方式與其他搜尋相同。使用 `from` 和 `size` 逐頁讀取切片時，會受到 `index.max_result_window` 索引設定（預設為 `10000`）的限制：`from` 與 `size` 的總和不得超過此值。若要從切片讀取更多文件，請在請求中加入 `sort`，並使用 `search_after` 進行分頁，如[使用 PIT 與 `search_after` 進行分頁](#pagination-with-pit-and-search_after)所述。如需索引設定的詳細資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。


## API

下表列出所有 [Point in Time API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/point-in-time-api/) 函式。

功能 | API | 說明
:--- | :--- | :---
[Create PIT]({{site.url}}{{site.baseurl}}/api-reference/search-apis/point-in-time-api/#create-a-pit) | `POST /<target_indexes>/_search/point_in_time?keep_alive=1h` | 建立 PIT。
[List PIT]({{site.url}}{{site.baseurl}}/api-reference/search-apis/point-in-time-api/#list-all-pits) | `GET /_search/point_in_time/_all` | 列出所有 PIT。
[Delete PIT]({{site.url}}{{site.baseurl}}/api-reference/search-apis/point-in-time-api/#delete-pits) | `DELETE /_search/point_in_time`<br> `DELETE /_search/point_in_time/_all` | 刪除一個 PIT 或所有 PIT。
[CAT PIT segments]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-pit-segments/) | `GET /_cat/pit_segments/_all` | 透過描述 PIT 的 Lucene 分段，提供其磁碟使用量的相關資訊。

如需必要的權限，請參閱[安全性模型]({{site.url}}{{site.baseurl}}/api-reference/search-apis/point-in-time-api#security-model)。

## PIT 設定

您可以為 PIT 指定下列設定。

設定 | 說明 | 預設值 
:--- | :--- | :---
`point_in_time.max_keep_alive` | 叢集層級設定，用於指定 `keep_alive` 參數的最大值。 | `24h`
`search.max_open_pit_context` | 節點層級設定，用於指定該節點可開啟的 PIT 脈絡數量上限。 | `300`
