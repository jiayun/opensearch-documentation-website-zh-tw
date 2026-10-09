---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "產生 On-Behalf-Of 權杖"
parent: Authentication APIs
grand_parent: Security APIs
nav_order: 70
---

# 產生 On-Behalf-Of 權杖 API
**於 2.12 版導入**
{: .label .label-purple }

為目前使用者產生 On-Behalf-Of 權杖。

呼叫此 API 之前，必須先設定 On-Behalf-Of 驗證。請在 `config.yml` 檔案的 `config.dynamic` 區段中加入包含 `signing_key` 的 `on_behalf_of` 區段，並使用 `securityadmin.sh` 套用。如需更多資訊，請參閱 [On-Behalf-Of 驗證]({{site.url}}{{site.baseurl}}/security/access-control/authentication-tokens/#on-behalf-of-authentication)。

<!-- spec_insert_start
api: security.generate_obo_token
component: endpoints
-->
## 端點
```json
POST /_plugins/_security/api/generateonbehalfoftoken
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: security.generate_obo_token
component: request_body_parameters
-->
## 請求本文欄位

請求本文為 __必要__。它是一個包含下列欄位的 JSON 物件。

| 屬性 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `description` | **必要** | 字串 | 使用者提供的權杖說明。 |
| `duration` | _選用_ | 字串 | 以秒為單位的持續時間。 |
| `service` | _選用_ | 字串 | 為該服務產生權杖時的服務名稱。 |

<!-- spec_insert_end -->

## 範例請求

```json
POST _plugins/_security/api/generateonbehalfoftoken
{
  "description": "Reason for token",
  "service": "self-issued",
  "durationSeconds": "300"
}
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "user": "admin",
  "authenticationToken": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZG1pbiIsImF1ZCI6InNlbGYtaXNzdWVkIiwibmJmIjoxNzg5MDUxOTQ1LCJpc3MiOiJvcGVuc2VhcmNoLWNsdXN0ZXIiLCJleHAiOjE3ODkwNTIyNDUsImlhdCI6MTc4OTA1MTk0NSwiZW5jcnlwdGVkX3JvbGVzIjoiZkE3blFnZW9hdmgrM1ZJWkZkRWNmUT09In0.1H6eSXlIsOfqZv7AeBPghgEC6tg4jrq5g-XiuNUYL3e705aP97c16xNXOnEUecOHsiqXskXqzH56Sw6ZLYSxSA",
  "durationSeconds": 300
}
```

<!-- spec_insert_start
api: security.generate_obo_token
component: response_body_parameters
-->
## 回應本文欄位

回應本文是一個包含下列欄位的 JSON 物件。

| 屬性 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `authenticationToken` | 字串 | 產生的 OBO 權杖。 | N/A |
| `durationSeconds` | 字串 | 權杖的持續時間。 | `300s` |
| `user` | 字串 | 請求權杖的實體名稱。 | N/A |

<!-- spec_insert_end -->
