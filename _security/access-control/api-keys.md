---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "API 金鑰"
parent: Access control
nav_order: 126
---

# API 金鑰
**3.7 版新增**
{: .label .label-purple }

API 金鑰可讓安全性管理員建立長期有效、具範圍限制的權杖，以程式設計方式存取 OpenSearch。每個金鑰都帶有自己的權限，並透過 `Authorization: ApiKey <token>` 標頭進行驗證，無需使用者名稱與密碼。

API 金鑰適用於下列情境：

- 需要將資料編製索引或執行查詢的 CI/CD 管線
- 輪詢叢集健康狀態的監控代理程式
- 採用最低權限存取的自動化指令碼
- 服務對服務的通訊

下列步驟說明 API 金鑰的驗證流程：

1. 您使用 REST API 或 OpenSearch Dashboards 建立金鑰，指定權限與有效期限。
2. 純文字權杖（以 `os_` 為字首）只會回傳**一次**，且不會被儲存。
3. 用戶端將權杖放入 `Authorization: ApiKey <token>` 標頭中。
4. Security 外掛程式使用 SHA-256 對收到的權杖進行雜湊運算，在記憶體快取中搜尋該權杖，並評估其權限。

您可以列出所有金鑰，並隨時撤銷它們。撤銷會立即生效。

## 安全性考量

下列安全性特性適用於 API 金鑰：

- 權杖使用符合密碼學安全的亂數產生器產生，因此暴力破解攻擊不可行。
- 只儲存 SHA-256 雜湊值。純文字權杖永遠不會被保存。
- 權杖的建立與撤銷會記錄在 `API_TOKEN_WRITE` 稽核類別下。驗證事件會顯示 `token:<name>` 作為使用者。
- 撤銷作業會同步廣播至所有節點。在網路分割期間，撤銷請求會失敗並回傳錯誤。權杖會根據 `duration_seconds` 自動到期。

## 限制

- 只有安全性管理員可以建立、列出及撤銷 API 金鑰。
- 以 API 金鑰驗證的請求無法存取系統索引（`.opensearch_security*`）或受保護的索引。
- 以 API 金鑰驗證的請求無法呼叫 Security API 端點。
- `indices:data/write/bulk` 動作會被視為叢集層級權限來評估。若要使用 API 金鑰將文件編製索引，請在叢集權限中加入 `indices:data/write/bulk`，或使用包含該權限的叢集動作群組。

## 設定 API 金鑰

在 `config/opensearch-security/config.yml` 的 `config.dynamic` 下啟用 API 金鑰：

```yaml
config:
  dynamic:
    api_tokens:
      enabled: true
      max_duration_seconds: 7776000   # 90 days (maximum)
      max_tokens: 100                 # Maximum outstanding tokens
```
{% include copy.html %}

編輯檔案後，套用組態：

```bash
bash tools/securityadmin.sh -cd config/opensearch-security/ -icl -nhnv
```
{% include copy.html %}

## 建立 API 金鑰

下列請求會建立一個 API 金鑰，針對符合 `logs-*` 的索引授予叢集監控與大量寫入權限：

```bash
curl -k -u admin:$PASSWORD -X POST https://localhost:9200/_plugins/_security/api/apitokens \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "my-pipeline-key",
    "cluster_permissions": ["cluster_monitor", "indices:data/write/bulk"],
    "index_permissions": [
      {
        "index_pattern": ["logs-*"],
        "allowed_actions": ["indices_all"]
      }
    ],
    "duration_seconds": 2592000
  }'
```
{% include copy.html %}

回應中包含純文字權杖：

```json
{
  "id": "abc123",
  "token": "os_VNsOYN6kDoIgyrD_sBX2jmEIdfcnK5h9zq4u8ddjn8U"
}
```

請立即複製該權杖。它不會被儲存，也無法再次取得。
{: .warning }

## 使用 API 金鑰

若要使用 API 金鑰，請將權杖放入 `Authorization` 標頭中：

```bash
curl -k -H "Authorization: ApiKey os_VNsOYN6kDoIgyrD_sBX2jmEIdfcnK5h9zq4u8ddjn8U" \
  https://localhost:9200/_cluster/health
```
{% include copy.html %}

## 列出 API 金鑰

若要列出所有可用的 API 金鑰，請傳送下列請求：

```bash
curl -k -u admin:$PASSWORD https://localhost:9200/_plugins/_security/api/apitokens
```
{% include copy.html %}

回應中包含所有金鑰（作用中、已到期與已撤銷），以及 `expires_at`、`revoked_at` 和 `created_by` 等中繼資料。

## 撤銷 API 金鑰

若要撤銷 API 金鑰，請傳送包含金鑰 ID 的 `DELETE` 請求：

```bash
curl -k -u admin:$PASSWORD -X DELETE \
  https://localhost:9200/_plugins/_security/api/apitokens/<id>
```
{% include copy.html %}

撤銷是同步的：金鑰會立即在所有節點上無法使用。

## 在 OpenSearch Dashboards 中管理 API 金鑰

若已安裝 Security Dashboards 外掛程式，您可以從 **Security** > **API Keys** 頁面管理 API 金鑰。您可以建立具有叢集與索引權限的金鑰、選取到期預設值，以及撤銷金鑰。

若要在 OpenSearch Dashboards 中啟用 API 金鑰管理，請在 `opensearch_dashboards.yml` 中加入下列一行：

```yaml
opensearch_security.api_keys.enabled: true
```
{% include copy.html %}
