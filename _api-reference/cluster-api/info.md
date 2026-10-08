---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "叢集資訊"
nav_order: 45
parent: Cluster APIs
has_children: false
---

# 叢集資訊 API
**於 1.0 版導入**
{: .label .label-purple }

叢集資訊 API（`/`）會擷取執行中的 OpenSearch 叢集與節點的相關資訊，包括版本、建置詳細資料與叢集名稱。這是驗證叢集是否可連線，以及查詢 OpenSearch 版本最簡單的方式。

## 端點

```json
GET /
HEAD /
```

- `GET /` 回傳包含叢集與版本詳細資料的 JSON 本文。  
- `HEAD /` 僅回傳 HTTP 狀態（若可連線則為 200），適合用於輕量級健康狀態檢查。

## 範例請求

若要取得叢集的版本與建置資訊，請傳送下列請求：

```json
GET /
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "name": "opensearch-node1",
  "cluster_name": "opensearch-cluster",
  "cluster_uuid": "sQj1b9cZQICv0b8iYc3y5A",
  "version": {
    "distribution": "opensearch",
    "number": "3.2.0",
    "build_type": "tar",
    "build_hash": "abc123def456",
    "build_date": "2025-06-18T12:34:56.000Z",
    "build_snapshot": false,
    "lucene_version": "9.10.0",
    "minimum_wire_compatibility_version": "7.10.0",
    "minimum_index_compatibility_version": "7.0.0"
  },
  "tagline": "The OpenSearch Project: https://opensearch.org/"
}
```

## 回應本文欄位

Field | Type | Description
:--- | :--- | :---
`name` | String | 服務此請求的節點名稱。
`cluster_name` | String | 叢集名稱。
`cluster_uuid` | String | 叢集的通用唯一識別碼（UUID）。
`tagline` | String | 標語字串。
`version` | Object | 包含版本與建置中繼資料的物件。
`version.distribution` | String | 發行版識別碼，通常為 `opensearch`。
`version.number` | String | OpenSearch 版本號，例如 `3.2.0`。
`version.build_type` | String | 發行版類型。
`version.build_hash` | String | 建置所依據的提交雜湊值。
`version.build_date` | String | 採用 ISO 8601 格式的建置時間戳記。
`version.build_snapshot` | Boolean | 此建置是否為快照建置。
`version.lucene_version` | String | 此建置使用的 Lucene 版本。
`version.minimum_wire_compatibility_version` | String | 最低相容的傳輸協定版本。
`version.minimum_index_compatibility_version` | String | 可讀取的最低索引版本。
