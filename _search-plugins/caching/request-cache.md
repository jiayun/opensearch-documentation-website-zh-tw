---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引請求快取"
parent: Caching
grand_parent: Improving search performance
nav_order: 5
---

# 索引請求快取

OpenSearch 索引請求快取是一種專門的快取機制，旨在將經常執行的搜尋查詢結果儲存在分片層級，以提升搜尋效能。這可降低叢集負載，並改善重複搜尋的回應時間。此快取預設為啟用，對於某些查詢會頻繁執行的讀取密集型工作負載特別有用。

快取會在設定的重新整理間隔自動失效。失效範圍包括文件更新 (包含文件刪除) 以及索引設定的變更。這可確保快取永遠不會傳回過時的結果。當快取大小超過設定的上限時，會逐出最近最少使用的項目，以騰出空間給新項目。

部分查詢不符合使用請求快取的資格。這些包括啟用效能分析的查詢、捲動查詢，以及具有非決定性特性 (例如使用 `Math.random()` 或 DFS 查詢) 或相對時間 (例如 `now` 或 `new Date()`) 的搜尋請求。根據預設，只有 `size=0` 的請求可快取。在 OpenSearch 2.19 及更新版本中，可使用 `indices.requests.cache.maximum_cacheable_size` 變更此行為。
{: .note}

## 設定請求快取

您可以透過在 `opensearch.yml` 組態檔案中設定參數，或使用 REST API 來設定索引請求快取。如需詳細資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。

### 設定

下表列出索引請求快取的設定。如需動態設定的詳細資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。

設定 | 資料類型  | 預設值 | 層級 | 靜態／動態 | 說明
:--- |:-----------|:--------| :--- | :--- | :---
`indices.cache.cleanup_interval` | 時間單位  | `1m`（1 分鐘）  | 叢集 | 靜態 | 依指定間隔排程執行定期背景工作，清除快取中已過期的項目。 
`indices.requests.cache.size` | 百分比 | `1%`      | 叢集 | 靜態 | 快取大小占堆積記憶體大小的百分比（例如，若要使用堆積記憶體的 1%，請指定 `1%`）。 
`index.requests.cache.enable` | 布林值    | `true`    | 索引 | 動態 | 啟用或停用請求快取。 
`indices.requests.cache.maximum_cacheable_size` | 整數    | `0`    | 叢集 | 動態 | 設定可加入請求快取的查詢之最大 `size` 值。

### 範例

若要停用某個索引的請求快取，請傳送下列請求：

```json
PUT /my_index/_settings
{
  "index.requests.cache.enable": false
}
```
{% include copy-curl.html %}

## 快取特定請求

除了為請求快取提供索引層級或叢集層級的設定之外，您也可以將 `request_cache` 查詢參數設為 `true`，以選擇性地快取特定的搜尋請求：

```json
GET /students/_search?request_cache=true
{
  "query": {
    "match": {
      "name": "doe john"
    }
  }
}
```
{% include copy-curl.html %}

## 將請求與快取結果進行比對

請求快取會為每個分片儲存結果。為了找到快取的結果，OpenSearch 會比較剖析後的搜尋請求，因此只有格式不同的請求會共用快取的結果。例如，只有空白字元或 JSON 鍵順序不同的請求會傳回相同的快取結果。兩個 `terms` 彙總若只有是否指定預設 `size` 為 `10` 的差異，也會傳回相同的快取結果。內容不同的請求 (例如名稱不同的彙總) 則會分開快取。

## 監視請求快取

監視快取使用量與效能，對於維持高效率的快取策略至關重要。OpenSearch 提供多個 API 來協助監視快取。

### 擷取所有節點的快取統計資料

[Nodes Stats API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/) 會傳回叢集中所有節點的快取統計資料：

```json
GET /_nodes/stats/indices/request_cache
```
{% include copy-curl.html %}

回應包含請求快取統計資料：

```json
{
  "nodes": {
    "T7aqO6zaQX-lt8XBWBYLsA": {
      "indices": {
        "request_cache": {
          "memory_size_in_bytes": 10240,
          "evictions": 0,
          "hit_count": 50,
          "miss_count": 10
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 擷取特定索引的快取統計資料

[Index Stats API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/stats/) 會傳回特定索引的快取統計資料：

```json
GET /my_index/_stats/request_cache
```
{% include copy-curl.html %}

回應包含請求快取統計資料：

```json
{
  "_shards": {
    "total": 5,
    "successful": 5,
    "failed": 0
  },
  "_all": {
    "primaries": {
      "request_cache": {
        "memory_size_in_bytes": 2048,
        "evictions": 1,
        "hit_count": 30,
        "miss_count": 5
      }
    },
    "total": {
      "request_cache": {
        "memory_size_in_bytes": 4096,
        "evictions": 2,
        "hit_count": 60,
        "miss_count": 10
      }
    }
  },
  "indices": {
    "my_index": {
      "primaries": {
        "request_cache": {
          "memory_size_in_bytes": 2048,
          "evictions": 1,
          "hit_count": 30,
          "miss_count": 5
        }
      },
      "total":{
        "request_cache": {
          "memory_size_in_bytes": 4096,
          "evictions": 2,
          "hit_count": 60,
          "miss_count": 10
        }
      }
    }
  }
}
```

## 最佳實務

使用索引請求快取時，請考量下列最佳實務：

- **適當的快取大小**：根據您的查詢模式設定快取大小。較大的快取可儲存更多結果，但可能耗用大量資源。
- **查詢最佳化**：確保經常執行的查詢經過最佳化，以便從快取中獲益。
- **監視**：定期監視快取命中率與快取未命中率，以了解快取效率並進行必要的調整。