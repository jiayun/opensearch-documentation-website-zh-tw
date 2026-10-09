---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "安全性組態版本 API"
parent: Security APIs
nav_order: 115
has_children: true
has_toc: false
redirect_from:
  - /security/api/configuration-versions/
  - /security/configuration/versioning/
---

# 安全性組態版本 API
**於 3.3 版推出**
{: .label .label-purple }

這是實驗性功能，不建議在正式環境中使用。如需功能進度的最新消息，或想提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/)的討論。
{: .warning}

安全性組態版本 API 會追蹤 Security 外掛程式組態的歷史記錄，並還原先前的版本。您可以使用這些 API 檢閱組態隨時間的變化，並在發生非預期的變更後將叢集還原至已知狀態。

OpenSearch 支援下列安全性組態版本 API。

| API | 說明 |
| :--- | :--- |
| [Get Security Configuration Versions API]({{site.url}}{{site.baseurl}}/security/api/configuration-versions/get-versions/) | 擷取安全性組態版本歷史記錄，或依 ID 擷取單一版本。 |
| [Roll Back Security Configuration API]({{site.url}}{{site.baseurl}}/security/api/configuration-versions/rollback/) | 還原先前版本的安全性組態。 |

## 版本控制

當安全性組態變更與最近儲存的版本不同時，OpenSearch 會建立一個版本。相同的變更不會建立版本，因此歷史記錄只會包含有意義的項目。

每個版本包含下列資訊：

- 版本 ID，例如 `v1` 或 `v2`
- 建立版本時完整安全性組態的快照
- 建立版本的時間
- 進行變更的使用者 (若 OpenSearch 可將該變更歸因於某位使用者)

回復本身也是一項組態變更，因此會建立新版本。

## 啟用版本控制

版本控制預設為停用。若要啟用，請將下列設定新增至 `opensearch.yml`：

```yaml
plugins.security.configurations_versions.enabled: true
```
{% include copy.html %}

若要變更保留的版本數，請將下列設定新增至 `opensearch.yml`：

```yaml
plugins.security.config_version.retention_count: 10
```
{% include copy.html %}

預設為 `10`。當叢集達到保留上限時，OpenSearch 會移除最舊的版本，以騰出空間給新版本。

請重新啟動叢集以套用這些設定。如需詳細資訊，請參閱[實驗性功能旗標]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/experimental/)。

## 必要權限

這些 API 使用與所有其他 Security API 相同的存取控制，因此呼叫的使用者必須對應至 `plugins.security.restapi.roles_enabled` 中列出的角色。沒有這類角色的使用者會收到 `403 Forbidden`，除非該使用者擁有下列其中一項權限。如需詳細資訊，請參閱 [API 的存取控制]({{site.url}}{{site.baseurl}}/security/access-control/api/#access-control-for-the-api)。

若要分別控制這兩項操作，請啟用 REST API 管理員權限，並授予角色下列叢集權限。每一項都是獨立的授權，因此擁有該權限的角色不需要同時列在 `plugins.security.restapi.roles_enabled` 中。沒有任何內建角色包含這些權限，包括 `security_rest_api_full_access`。

| 操作 | 必要權限 |
| :--- | :--- |
| 取得版本 | `restapi:admin/view_version` |
| 回復組態 | `restapi:admin/rollback_version` |

若要防止角色使用任一操作，請使用 `plugins.security.restapi.endpoints_disabled` 為該角色停用 `VIEW_VERSION` 或 `ROLLBACK_VERSION` 端點。
