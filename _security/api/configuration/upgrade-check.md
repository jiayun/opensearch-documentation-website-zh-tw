---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "檢查升級"
parent: Security configuration APIs
grand_parent: Security APIs
nav_order: 40
redirect_from:
  - /api-reference/security/configuration/upgrade-check/
---

# 檢查安全性組態升級 API
**於 2.14 版推出**
{: .label .label-purple }

Check for Upgrades API 可讓您檢查 Security 外掛程式組態是否需要任何升級。這在將 OpenSearch 升級至新版本後特別實用，因為它有助於找出需要更新的安全性組態元件，以維持相容性或善用新功能。

每個新的 OpenSearch 版本都會變更預設的安全性組態。此 API 會將主機 Security 外掛程式隨附的組態與叢集目前的組態進行比較，並在回應中指出是否可以執行升級，以及升級會更新哪些資源。您可以使用此 API 判斷叢集是否缺少預設值，或是否具有過時的預設值定義。

<!-- spec_insert_start
api: security.config_upgrade_check
component: endpoints
-->
## 端點
```json
GET /_plugins/_security/api/_upgrade_check
```
<!-- spec_insert_end -->

## 範例請求

```json
GET /_plugins/_security/api/_upgrade_check
```
{% include copy-curl.html security=true %}

## 範例回應

有可用的升級時，`upgradeActions` 會列出升級將變更的物件：

```json
{
  "status": "OK",
  "upgradeAvailable": true,
  "upgradeActions": {
    "roles": {
      "add": [
        "flow_framework_full_access"
      ]
    }
  }
}
```

組態已是最新狀態時，會省略 `upgradeActions`：

```json
{
  "status": "OK",
  "upgradeAvailable": false
}
```

## 回應本文欄位

回應本文是包含下列欄位的 JSON 物件。

| 屬性 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `status` | 字串 | 請求的狀態。成功的請求會傳回「OK」。 |
| `upgradeAvailable` | 布林值 | 有可用的安全性組態升級時，傳回 `true`。 |
| `upgradeActions` | 物件 | 升級主機的 Security 外掛程式時將會修改的安全性物件，依組態類型分類，例如 `roles`。每個組態類型都對應至一個物件，其鍵為將套用的動作 (例如 `add`)，其值則列出受影響物件的名稱。 |

## 使用注意事項

在 OpenSearch 升級過程中管理安全性組態時，了解如何解讀 Check for Upgrades API 的結果並據以採取行動非常重要。下列注意事項提供使用此 API 的指引：

- 執行此 API 不會對您的組態進行任何變更，只會檢查潛在的升級。
- 使用此 API 找出必要的升級後，您可以使用適當的 Configuration API 實作所需的變更。
- 建議您在每次升級 OpenSearch 版本後執行此檢查。
- 您可能需要管理員權限才能使用此 API。
