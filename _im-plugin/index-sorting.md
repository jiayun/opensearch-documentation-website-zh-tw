---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引排序"
parent: Tuning indexes
nav_order: 20
---


# 索引排序

OpenSearch 允許您在建立索引時設定文件在每個分段內的組織方式。預設情況下，Lucene 不會對文件進行排序。`index.sort.*` 設定可指定文件在每個分段內的組織方式。

排序行為由 `index.sort.field`、`index.sort.order`、`index.sort.mode` 和 `index.sort.missing` 設定控制。如需更多資訊，請參閱 [靜態索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#index-sort-settings)。

索引排序只能在建立索引時設定，之後無法修改。此功能會影響索引效能，因為文件必須在排清與合併作業期間進行排序。我們建議在正式環境中實作排序之前，先測試其對效能的影響。
{: .note}

## 依單一欄位排序

下列範例依 `timestamp` 欄位以遞減順序排序索引：

```json
PUT /sample-index
{
  "settings": {
    "index": {
      "sort.field": "timestamp",
      "sort.order": "desc"
    }
  },
  "mappings": {
    "properties": {
      "timestamp": {
        "type": "date"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 依多個欄位排序

您也可以依多個欄位排序，優先順序以第一個欄位為準。下列範例先依 `category` 以遞增順序排序文件，再依 `timestamp` 以遞減順序排序：

```json
PUT /multi-sort-index
{
  "settings": {
    "index": {
      "sort.field": [
        "category",
        "timestamp"
      ],
      "sort.order": [
        "asc",
        "desc"
      ]
    }
  },
  "mappings": {
    "properties": {
      "category": {
        "type": "keyword",
        "doc_values": true
      },
      "timestamp": {
        "type": "date"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 依巢狀欄位排序
**3.3 版推出**
{: .label .label-purple }

您可以對對應包含巢狀欄位的索引設定索引排序。請依索引的頂層欄位排序；巢狀欄位可以出現在對應中，但不能出現在 `sort.field` 中。下列範例對具有 `comments` 巢狀欄位的索引，依頂層的 `user_id` 和 `created_at` 欄位排序：

```json
PUT /nested-index
{
  "settings": {
    "index": {
      "sort.field": [
        "user_id",
        "created_at"
      ],
      "sort.order": [
        "asc",
        "desc"
      ]
    }
  },
  "mappings": {
    "properties": {
      "user_id": {
        "type": "keyword"
      },
      "created_at": {
        "type": "date"
      },
      "comments": {
        "type": "nested",
        "properties": {
          "message": { "type": "text" },
          "timestamp": { "type": "date" }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

索引排序無法套用於巢狀物件內部的欄位，這可保持巢狀文件的結構完整性。若指定巢狀物件內的欄位（例如 `comments.timestamp`），系統會以 `400` 拒絕該請求。
{: .note}

## 提前終止的搜尋最佳化

當您的索引排序組態符合搜尋排序條件時，OpenSearch 可以透過限制每個分段檢查的文件數量來最佳化查詢效能。此最佳化對擷取排名最前的結果特別有效。

假設有一個依時間戳記以遞減順序排序的索引：

```json
PUT /events
{
  "settings": {
    "index": {
      "sort.field": "timestamp",
      "sort.order": "desc"
    }
  },
  "mappings": {
    "properties": {
      "timestamp": {
        "type": "date"
      }
    }
  }
}
```
{% include copy-curl.html %}

加入一些事件：

```json
POST /events/_bulk?refresh=true
{ "index": {} }
{ "timestamp": "2025-01-01T00:00:00" }
{ "index": {} }
{ "timestamp": "2025-01-02T00:00:00" }
{ "index": {} }
{ "timestamp": "2025-01-03T00:00:00" }
```
{% include copy-curl.html %}

若要擷取最近的 10 筆事件，請使用下列請求：

```json
GET /events/_search
{
  "size": 10,
  "sort": [
    {
      "timestamp": "desc"
    }
  ]
}
```
{% include copy-curl.html %}

OpenSearch 會辨識出分段內的文件已排序，因此每個分段只檢查前 10 筆文件，同時仍會收集其餘文件以計算總數與執行彙總。

如果您不需要總命中數，可以停用命中追蹤以獲得最佳效能：

```json
GET /events/_search
{
    "size": 10,
    "sort": [
        { "timestamp": "desc" }
    ],
    "track_total_hits": false
}
```
{% include copy-curl.html %}

這樣 OpenSearch 就能在每個分段找到所需數量的文件後終止收集。

無論 `track_total_hits` 設定為何，彙總都會處理所有符合條件的文件。
{: .note}

## 最佳化合取查詢

索引排序可以透過組織文件 ID，將符合相似條件的文件分組，藉此提升合取查詢（AND 運算）的效能。這種組織方式有助於略過不符合查詢條件的大量文件範圍。

此技術最適合經常用於篩選的低基數欄位。排序優先順序應優先考慮基數低且篩選頻率高的欄位。排序方向（遞增或遞減）對此最佳化沒有影響。

例如，在為車輛清單編製索引時，您可以依燃料類型、車身樣式、製造商、年份，最後依里程數排序，以最佳化常見的篩選組合。
