---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "通知存取控制"
nav_order: 30
parent: Notifications
has_children: false
---

# 通知存取控制

通知功能與 Security 外掛程式的資源共用與存取控制架構整合，為通知組態提供文件層級的授權。通知組態是頻道的基礎文件，因此共用組態即可控制對應頻道的存取權。資源共用取代了舊版的 `opensearch.notifications.general.filter_by_backend_roles` 設定，讓資源擁有者能將特定的存取層級授予使用者、角色或後端角色。

如需端對端架構概念與 API 的說明，請參閱[資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/)。
{: .note}

## 資源組態

下表說明通知組態資源。

| 欄位 | 值 |
| :--- | :--- |
| 資源類型 | `notification_config` |
| 系統索引 | `.opensearch-notifications-config` |
| 採用版本 | OpenSearch 3.9 |

啟用資源層級授權時，每個通知組態的可見性由中央共用記錄管理。資源擁有者與具備共用能力的使用者，可以授予或撤銷特定使用者、角色或後端角色的存取權限。當使用者列出通知組態或頻道時，回應只會包含該使用者擁有或與該使用者共用的組態。

## 啟用通知資源共用

若要啟用通知的資源共用，請將通知組態資源類型加入受保護類型清單，並在整個叢集範圍啟用資源共用。

僅限管理員：這些設定只能由具有更新叢集設定權限的叢集管理員設定。
{: .important }

### 使用 opensearch.yml 進行組態設定

將下列設定新增至您的 `opensearch.yml` 組態檔，以啟用通知的資源共用：

```yaml
plugins.security.resource_sharing.enabled: true
plugins.security.system_indices.enabled: true
plugins.security.resource_sharing.protected_types:
  - "notification_config"
```
{% include copy.html %}

新增至 `opensearch.yml` 的設定會在叢集重新啟動後生效。

### 使用 Cluster Settings API 進行組態

若要在不重新啟動叢集的情況下啟用資源共用，請使用 Cluster Settings API：

```json
PUT _cluster/settings
{
  "transient": {
    "plugins.security.resource_sharing.enabled": true,
    "plugins.security.resource_sharing.protected_types": ["notification_config"]
  }
}
```
{% include copy-curl.html %}

`plugins.security.system_indices.enabled` 設定無法使用 Cluster Settings API 更新，因此請在 `opensearch.yml` 中設定。

將通知組態資源類型新增至現有組態時，請在 `protected_types` 陣列中包含所有先前已設定的資源類型。
{: .note}

## 通知存取層級

Notifications 為通知組態文件提供三個預先定義的存取層級。每個存取層級決定使用者可對與其共用的通知組態執行哪些操作。

### notifications_read_only

`notifications_read_only` 唯讀存取層級可讓使用者檢視共用的通知組態與通道，但無法修改。此存取層級包含下列權限：

```yaml
- 'cluster:admin/opensearch/notifications/configs/get'
- 'cluster:admin/opensearch/notifications/channels/get'
- 'cluster:admin/opensearch/notifications/features'
```
{% include copy.html %}

### notifications_read_write

`notifications_read_write` 讀寫存取層級可讓使用者完整存取通知組態操作，但不含共用功能。此存取層級包含所有讀取權限，以及寫入與傳送操作：

```yaml
- 'cluster:admin/opensearch/notifications/configs/*'
- 'cluster:admin/opensearch/notifications/channels/get'
- 'cluster:admin/opensearch/notifications/features'
- 'cluster:admin/opensearch/notifications/feature/send'
- 'cluster:admin/opensearch/notifications/test_notification'
```
{% include copy.html %}

### notifications_full_access

`notifications_full_access` 完整存取層級可讓使用者完整控制通知組態，包括將資源與其他使用者共用等類似擁有者的權限。此存取層級包含所有通知操作，以及資源共用權限：

```yaml
- 'cluster:admin/opensearch/notifications/configs/*'
- 'cluster:admin/opensearch/notifications/channels/get'
- 'cluster:admin/opensearch/notifications/features'
- 'cluster:admin/opensearch/notifications/feature/send'
- 'cluster:admin/opensearch/notifications/test_notification'
- 'cluster:admin/security/resource/share'
```
{% include copy.html %}

這些存取層級為預先定義且無法修改。如需其他存取層級，請在 [Notifications GitHub 儲存庫](https://github.com/opensearch-project/notifications/)中建立問題。
{: .note}

## 從舊版架構遷移

啟用資源共用並將通知組態資源類型標記為受保護後，叢集管理員必須執行遷移 API，將現有通知共用資訊從舊版架構轉移至新的資源共用系統。在您執行遷移之前，現有通知組態沒有共用記錄，因此所有使用者都無法存取，包括建立這些組態的使用者。

僅限管理員：Migrate API 只能由具有 superadmin 或 REST admin 權限的叢集管理員執行。
{: .important }

通知組態文件會在 `metadata.access` 下追蹤其授權的後端角色，且不會儲存個別使用者擁有者。將 `backend_roles_path` 設為 `/metadata/access`。`username_path` 參數為必要且不可為空，因此請將其指向通知文件未包含的欄位，例如 `/metadata/owner`。該路徑解析後不會得到任何值，因此擁有權會回退至 `default_owner`。

使用下列 API 呼叫，將舊版通知共用資料遷移至資源共用架構：

```json
POST _plugins/_security/api/resources/migrate
{
  "source_index": ".opensearch-notifications-config",
  "username_path": "/metadata/owner",
  "backend_roles_path": "/metadata/access",
  "default_owner": "<replace-with-existing-user>",
  "default_access_level": {
    "notification_config": "<select-appropriate-access-level>"
  }
}
```
{% include copy-curl.html %}

將 `<replace-with-existing-user>` 取代為應擁有通知組態之現有使用者的使用者名稱。由於通知文件不帶有擁有者名稱，每個遷移的組態都會歸屬於此使用者。將 `<select-appropriate-access-level>` 取代為可用的通知存取層級之一：`notifications_read_only`、`notifications_read_write` 或 `notifications_full_access`。遷移會以此存取層級，將每個組態共用給其 `metadata.access` 欄位中儲存的後端角色。若您省略 `default_access_level`，遷移會使用 `notifications_read_only`。沒有後端角色的組態會在不共用的情況下遷移，因此只有預設擁有者可以存取。

## 相關文件

下列頁面提供更多資源共用的相關資訊：

- [資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/)
- [資源共用 API]({{site.url}}{{site.baseurl}}/security/access-control/resource-sharing-api/)
- [資源存取管理]({{site.url}}{{site.baseurl}}/dashboards/management/resource-sharing/)
