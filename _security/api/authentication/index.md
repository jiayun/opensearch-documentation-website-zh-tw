---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "驗證 API"
parent: Security APIs
nav_order: 10
has_children: true
has_toc: false
redirect_from:
  - /api-reference/security/authentication/
  - /api-reference/security/authentication/index/
  - /security/api/authentication/
---

# 驗證 API

驗證 API 會傳回已驗證使用者的相關資訊、授予該使用者的權限，以及用於發出請求的 TLS 連線。

OpenSearch 支援下列驗證 API。

| API | 說明 |
| :--- | :--- |
| [Authentication Information API]({{site.url}}{{site.baseurl}}/security/api/authentication/auth-info/) | 傳回目前驗證使用者的名稱、角色、後端角色、自訂屬性及租用戶成員資格。 |
| [Who Am I API]({{site.url}}{{site.baseurl}}/security/api/authentication/who-am-i/) | 傳回目前驗證使用者的身分資訊。 |
| [Who Am I Protected API]({{site.url}}{{site.baseurl}}/security/api/authentication/who-am-i-protected/) | 傳回目前驗證使用者的身分資訊，並強制執行 REST 層授權。 |
| [Permissions Info API]({{site.url}}{{site.baseurl}}/security/api/authentication/permissions-info/) | 傳回目前驗證使用者經評估的 REST API 權限。 |
| [SSL Info API]({{site.url}}{{site.baseurl}}/security/api/authentication/ssl-info/) | 傳回 TLS 連線及用於該請求之憑證的相關資訊。 |
| [Authorization Token API]({{site.url}}{{site.baseurl}}/security/api/authentication/auth-token/) | 傳回帶有空訊息的 `OK` 狀態。此端點不會核發權杖。 |
| [Generate On-Behalf-Of Token API]({{site.url}}{{site.baseurl}}/security/api/authentication/generate-obo-token/) | 產生 On-Behalf-Of 權杖，允許服務代表目前驗證的使用者執行動作。 |
