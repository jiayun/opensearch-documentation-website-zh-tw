---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "回復組態"
parent: Security configuration version APIs
grand_parent: Security APIs
nav_order: 20
---

# Roll Back Security Configuration API
**於 3.3 版推出**
{: .label .label-purple }

這是實驗性功能，不建議在正式環境中使用。若要瞭解此功能的最新進展或提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/)上的討論。
{: .warning}

還原先前版本的安全性組態。指定版本 ID 即可回復至該版本，或省略版本 ID 以回復至目前版本的前一個版本。

回復會取代整個安全性組態，包括使用者、角色、角色對應、動作群組和租用戶。請使用 [Get Security Configuration Versions API]({{site.url}}{{site.baseurl}}/security/api/configuration-versions/get-versions/)擷取目標版本，並在回復前確認其內容。
{: .warning}

回復本身也是組態變更，因此 OpenSearch 會為此記錄一個新版本。例如，將執行 `v6` 的叢集回復至 `v5` 後，叢集會使用 `v5` 組態，並將 `v7` 新增至版本歷程記錄。

## 端點

```json
POST /_plugins/_security/api/version/rollback
POST /_plugins/_security/api/version/rollback/{version_id}
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `version_id` | 字串 | 要還原的版本，以 `v` 後接數字指定，例如 `v1` 或 `v2`。若省略，OpenSearch 會還原目前版本的前一個版本。 |

## 請求範例

下列請求會還原前一個版本：

```json
POST /_plugins/_security/api/version/rollback
```
{% include copy-curl.html security=true %}

下列請求會還原 `v2` 版本：

```json
POST /_plugins/_security/api/version/rollback/v2
```
{% include copy-curl.html security=true %}

## 回應範例

回應會指出 OpenSearch 還原的版本。執行 `v6` 的叢集在回復至前一個版本時，會傳回下列回應：

```json
{
  "status": "OK",
  "message": "config rolled back to version v5"
}
```

指定 `v2` 的請求會傳回下列回應：

```json
{
  "status": "OK",
  "message": "config rolled back to version v2"
}
```

若請求的版本不存在，OpenSearch 會傳回 `404 Not Found`，並維持組態不變：

```json
{
  "status": "NOT_FOUND",
  "message": "Version v99 not found"
}
```

## 回應本文欄位

回應本文是具有下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `status` | 字串 | 回復的狀態。`OK` 表示 OpenSearch 已還原該版本。 |
| `message` | 字串 | 指出 OpenSearch 還原版本的訊息。 |
