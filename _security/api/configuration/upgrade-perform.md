---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "執行升級"
parent: Security configuration APIs
grand_parent: Security APIs
nav_order: 50
redirect_from:
  - /api-reference/security/configuration/upgrade-perform/
---

# 執行安全性組態升級 API
**2.14 版新增**
{: .label .label-purple }


Perform Upgrade API 可讓您升級 Security 外掛程式的組態元件。此 API 通常在透過 [Check for Upgrades API]({{site.url}}{{site.baseurl}}/security/api/configuration/upgrade-check/) 識別出必要的升級之後使用。它會更新您的組態元件，以確保與目前版本的 Security 外掛程式相容。

此 API 會從隨所安裝 Security 外掛程式版本一併提供的組態中，新增並更新叢集現有安全性組態的資源。隨附的組態檔位於 `<OPENSEARCH_HOME>/security/config` 目錄。預設組態檔會在 OpenSearch 升級時更新，而叢集組態僅會由叢集維運人員更新，因此此 API 可讓維運人員升級缺少的預設值與過時的預設定義。

<!-- spec_insert_start
api: security.config_upgrade_perform
component: endpoints
-->
## 端點
```json
POST /_plugins/_security/api/_upgrade_perform
```
<!-- spec_insert_end -->

## 請求本文欄位

請求本文為選用。它是一個包含下列欄位的 JSON 物件。

| 屬性 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `config` | 字串陣列 | 要升級的特定組態元件清單。若省略，將處理所有需要升級的元件。有效值包括 `roles`、`rolesmapping`、`actiongroups`、`config`、`internalusers` 與 `tenants`。 |

## 範例請求

```json
POST /_plugins/_security/api/_upgrade_perform
{
  "configs": [
    "roles"
  ]
}
```
{% include copy-curl.html security=true %}

## 範例回應

`upgrades` 物件列出已套用的變更：

```json
{
  "status": "OK",
  "upgrades": {
    "roles": {
      "add": [
        "flow_framework_full_access"
      ]
    }
  }
}
```

若指定的組態已是最新狀態，請求會失敗並傳回 `400 Bad Request`：

```json
{
  "status": "BAD_REQUEST",
  "message": "Unable to upgrade, no differences found in 'roles' config"
}
```

## 回應本文欄位

回應本文是一個包含下列欄位的 JSON 物件。

| 屬性 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `status` | 字串 | 請求的狀態。成功的請求會傳回 `OK`。 |
| `upgrades` | 物件 | 升級結果的容器，依組態類型組織，例如 `roles`。每個已變更的組態類型都會以這個物件中的一個鍵表示。 |

<details markdown="block">
  <summary>
    回應本文欄位：<code>upgrades</code>
  </summary>
  {: .text-delta}

`upgrades` 中的每個組態類型都對應到一個物件，其鍵為套用至該類型的動作，例如 `add` 或 `modify`。每個動作都對應到一個清單，列出該升級所修改物件的名稱。

</details>
