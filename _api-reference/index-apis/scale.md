---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Scale
parent: Index operations
grand_parent: Index APIs
nav_order: 80
---

# Scale API
**於 3.0 版推出**
{: .label .label-purple }

Scale API 可讓您在索引上啟用或停用 `search_only` 模式。當索引處於 `search_only` 模式時，只會保留其搜尋副本，並縮減主要分片與一般副本分片。此最佳化有助於在寫入活動較少的期間降低資源消耗，同時維持搜尋功能。

此功能支援縮減至零 (scale-to-zero) 部署與讀取器/寫入器分離模式等情境，可在正式環境中大幅提升資源使用率並降低成本。

如果您使用 Security 外掛程式，則必須具備 `manage index` 權限。
{: .note}

## 端點

```json
POST /{index}/_scale
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `index` | **必要** | 字串 | 要調整規模的索引名稱。不支援萬用字元。 |

## 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `search_only` | **必要** | 布林值 | 若為 `true`，則在索引上啟用僅限搜尋模式。若為 `false`，則停用僅限搜尋模式，並將索引恢復為正常運作。 |

## 請求範例：啟用僅限搜尋模式

下列請求會為名為 `my-index` 的索引啟用僅限搜尋模式：

```json
POST /my-index/_scale
{
  "search_only": true
}
```
{% include copy-curl.html %}

## 請求範例：停用僅限搜尋模式

下列請求會停用僅限搜尋模式，並將索引恢復為正常運作：

```json
POST /my-index/_scale
{
  "search_only": false
}
```
{% include copy-curl.html %}

## 回應範例

此 API 會傳回下列回應：

```json
{
  "acknowledged": true
}
```
