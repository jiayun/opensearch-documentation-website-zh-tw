---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立或更新角色對應"
parent: Role mapping APIs
grand_parent: Security APIs
nav_order: 10
---

# 建立或更新角色對應 API
**於 1.0 版導入**
{: .label .label-purple }

建立或取代指定的角色對應。

<!-- spec_insert_start
api: security.create_role_mapping
component: endpoints
-->
## 端點
```json
PUT /_plugins/_security/api/rolesmapping/{role}
```
<!-- spec_insert_end -->

## 請求本文欄位

請求本文為必要。它是一個包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `users` | 字串陣列 | 對應到該角色的使用者名稱。支援萬用字元模式。 | 否 |
| `backend_roles` | 字串陣列 | 對應到該角色的後端角色。具備其中任一後端角色的使用者即會取得該角色。 | 否 |
| `and_backend_roles` | 字串陣列 | 對應到該角色的後端角色。使用者必須具備所有這些後端角色才會取得該角色。 | 否 |
| `hosts` | 字串陣列 | 對應到該角色的主機名稱或 IP 位址。支援萬用字元模式。 | 否 |
| `description` | 字串 | 角色對應的說明。 | 否 |
| `hidden` | 布林值 | 角色對應是否在 API 與 OpenSearch Dashboards 中隱藏。預設為 `false`。 | 否 |
| `reserved` | 布林值 | 角色對應是否為唯讀且不可修改。預設為 `false`。 | 否 |

## 以主機為基礎的角色對應

`hosts` 參數會將來自特定 IP 位址或主機名稱的請求對應到指定的角色。不支援 CIDR 區塊，但可以使用萬用字元模式 (glob)，例如 `192.168.*.*` 或 `*.example.com`。當您想根據用戶端的來源位址指派角色時，這非常實用：

* 若要依 IP 位址比對 (例如 `"192.168.1.10"`)，不需要額外的組態。
* 若要依主機名稱比對 (例如 `"myserver.example.com"`)，您必須設定叢集層級的組態參數：

  ```yaml
  opensearch_security.host_resolver_mode: ip-hostname
  ```

  這會啟用反向 DNS 查詢以解析主機名稱。如需更多資訊，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

在 `hosts` 中使用 `"*"` 會比對所有用戶端 IP 與主機名稱，表示此角色會套用至每個請求，無論使用者為何。若與 `users: ["someuser"]` 搭配使用，可能會授予超出您預期的更廣泛存取權限。除非您有意將該角色授予所有用戶端 IP，否則請避免設定 `hosts: ["*"]`。
{: .warning}

## 範例請求

```json
PUT _plugins/_security/api/rolesmapping/test-role
{
  "backend_roles": [
    "starfleet",
    "captains"
  ],
  "hosts": [
    "*.starfleetintranet.com"
  ],
  "users": [
    "test-user"
  ]
}
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "status": "CREATED",
  "message": "'test-role' created."
}
```
