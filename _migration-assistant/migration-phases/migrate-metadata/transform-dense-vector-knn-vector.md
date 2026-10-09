---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "將 dense_vector 欄位轉換為 knn_vector"
nav_order: 5
parent: Migrate metadata
grand_parent: Migration workflows
permalink: /migration-assistant/migration-phases/migrate-metadata/transform-dense-vector-knn-vector/
---

# 將 dense_vector 欄位轉換為 knn_vector

Migration Assistant 可以在中繼資料遷移期間，自動將 Elasticsearch `dense_vector` 對應轉換為 OpenSearch `knn_vector` 對應。目標對應必須對 OpenSearch k-NN 模型有效，且應用程式在遷移後可能需要變更查詢。

## 內建轉換行為

中繼資料遷移路徑可以：

- 將 `dense_vector` 轉換為 `knn_vector`。
- 轉譯向量維度及相關設定。
- 為 OpenSearch 向量搜尋準備目標對應。

視目標而定，也可能套用其他向量相容性轉換，包括 Serverless-NextGen 專屬的調整。

## 識別 dense_vector 欄位

若要確認您的來源是否使用 `dense_vector` 欄位，請執行下列命令：

```bash
console clusters curl source /_mapping
```
{% include copy.html %}

如果來源對應包含 `"type":"dense_vector"`，請在評估與先導驗證期間仔細檢查那些索引。

## 遷移後驗證

驗證目標對應：

```bash
console clusters curl target /your-index/_mapping
workflow show
```
{% include copy.html %}

此外，請驗證目標叢集支援您打算使用的向量搜尋功能。

## 應用程式影響

即使對應遷移成功，查詢行為可能仍需要變更。如果您的應用程式目前依賴 Elasticsearch 向量查詢模式，請仔細驗證搜尋層。

## 其他考量

在下列情況下，請在切換前使用具代表性的查詢執行先導遷移：

- 目標是 Amazon OpenSearch Serverless NextGen。
- 目標版本有向量引擎相容性限制。
- 應用程式依賴特定的向量查詢語法或排名行為。
