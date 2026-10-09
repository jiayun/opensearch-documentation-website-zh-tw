---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "API 金鑰 API"
parent: Security APIs
nav_order: 70
has_children: true
has_toc: false
redirect_from:
  - /api-reference/security/api-keys/
  - /api-reference/security/api-keys/index/
  - /security/api/api-keys/
---

# API 金鑰 API
**於 3.7 版推出**
{: .label .label-purple }

API 金鑰 API 可建立、列出及撤銷用於在沒有使用者名稱和密碼的情況下驗證請求的 API 金鑰。

OpenSearch 支援下列 API 金鑰 API。

| API | 說明 |
| :--- | :--- |
| [Create API Key API]({{site.url}}{{site.baseurl}}/security/api/api-keys/create/) | 建立具有指定權限和到期時間的 API 金鑰。 |
| [List API Keys API]({{site.url}}{{site.baseurl}}/security/api/api-keys/list/) | 傳回所有 API 金鑰，包括作用中、已過期和已撤銷的金鑰。 |
| [Revoke API Key API]({{site.url}}{{site.baseurl}}/security/api/api-keys/revoke/) | 撤銷 API 金鑰，使其立即無法用於驗證。 |

## 必要權限

若要使用 API 金鑰 API，您必須擁有 `cluster:admin/plugins/security/api_token` 權限。
