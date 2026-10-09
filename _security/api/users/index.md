---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "內部使用者 API"
parent: Security APIs
nav_order: 30
has_children: true
has_toc: false
redirect_from:
  - /security/api/users/
---

# 內部使用者 API

內部使用者 API 可在內部使用者資料庫中建立、擷取、修改及刪除使用者。如果您使用外部驗證後端，可能就不需要擔心內部使用者。

OpenSearch 支援下列內部使用者 API。

| API | 說明 |
| :--- | :--- |
| [建立或更新使用者 API]({{site.url}}{{site.baseurl}}/security/api/users/create-user/) | 建立或取代指定的內部使用者。 |
| [修補使用者 API]({{site.url}}{{site.baseurl}}/security/api/users/patch-users/) | 更新單一內部使用者的個別屬性，或在單次呼叫中建立、更新或刪除多個內部使用者。 |
| [取得使用者 API]({{site.url}}{{site.baseurl}}/security/api/users/get-users/) | 擷取單一內部使用者或所有內部使用者。 |
| [刪除使用者 API]({{site.url}}{{site.baseurl}}/security/api/users/delete-user/) | 刪除指定的內部使用者。 |
| [產生使用者權杖 API]({{site.url}}{{site.baseurl}}/security/api/users/generate-user-token/) | 為指定的內部使用者產生授權權杖。 |

## 舊版端點

`_plugins/_security/api/user` 端點是本章節所記載之 `_plugins/_security/api/internalusers` 端點的已棄用別名。新程式碼請使用 `internalusers` 端點。
