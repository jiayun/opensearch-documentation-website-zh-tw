---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "產生使用者權杖"
parent: Internal user APIs
grand_parent: Security APIs
nav_order: 50
---

# 產生使用者權杖 API
**於 2.7 版推出**
{: .label .label-purple }

為指定的使用者產生授權權杖。

權杖只能為服務帳戶產生：服務帳戶是將 `service` 與 `enabled` 屬性設為 `true` 所建立的內部使用者。對任何其他使用者的請求都會失敗。如需更多資訊，請參閱[服務帳戶]({{site.url}}{{site.baseurl}}/security/access-control/authentication-tokens/#service-accounts)。

<!-- spec_insert_start
api: security.generate_user_token
component: endpoints
-->
## 端點
```json
POST /_plugins/_security/api/internalusers/{username}/authtoken
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: security.generate_user_token
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `username` | **必要** | 字串 | 要為其核發授權權杖的使用者名稱。 |

<!-- spec_insert_end -->

## 請求範例

下列請求會為 `svc-account` 服務帳戶產生權杖：

```json
POST _plugins/_security/api/internalusers/svc-account/authtoken
```
{% include copy-curl.html security=true %}

## 回應範例

產生的權杖會於 `message` 欄位中傳回：

```json
{
  "status": "OK",
  "message": "'svc-account' authtoken generated Basic auth token with user=svc-account, password=4Yz0kQJsliaQ35"
}
```

## 回應本文欄位

回應本文是包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `status` | 字串 | 請求的狀態。`OK` 表示 OpenSearch 已產生權杖。 |
| `message` | 字串 | 產生的認證資料，格式為 `'<username>' authtoken generated Basic auth token with user=<username>, password=<password>`。 |
