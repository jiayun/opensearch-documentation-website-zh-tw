---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工作流程存取控制"
nav_order: 30
---

# 工作流程存取控制

Flow Framework 整合 Security 外掛程式的資源共用與存取控制架構，為工作流程記錄提供文件層級的授權。這以更具彈性的共用系統取代舊版 `plugins.flow_framework.filter_by_backend_roles` 設定，讓資源擁有者能授予使用者、角色或後端角色特定的存取層級。

如需端對端架構概念與 API，請參閱[資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/)。
{: .note}

## 資源組態

下表說明工作流程資源組態。

| 欄位 | 值 |
| :--- | :--- |
| 資源類型 | `workflow` |
| 系統索引 | `.plugins-flow-framework-templates` |
| 納入支援的版本 | OpenSearch 3.4 |

為工作流程啟用資源層級授權後，每個工作流程的可見性都由中央共用記錄控管。資源擁有者和具備共用能力的使用者可以授予或撤銷特定使用者、角色或後端角色的存取權限。

## 啟用工作流程資源共用

若要為工作流程啟用資源共用，您必須將工作流程資源類型新增至受保護類型清單，並在整個叢集啟用資源共用。

僅限管理員：只有具備 superadmin 權限的叢集管理員才能設定這些設定。
{: .important }

### 使用 opensearch.yml 設定組態

將下列設定新增至您的 `opensearch.yml` 組態檔案，以啟用工作流程資源共用：

```yaml
plugins.security.resource_sharing.enabled: true
plugins.security.system_indices.enabled: true
plugins.security.resource_sharing.protected_types:
  - "workflow"
```
{% include copy.html %}

### 使用 Cluster Settings API 設定組態

或者，您可以使用 Cluster Settings API 動態啟用資源共用：

```json
PUT _cluster/settings
{
  "transient": {
    "plugins.security.resource_sharing.enabled": true,
    "plugins.security.resource_sharing.protected_types": ["workflow"]
  }
}
```
{% include copy-curl.html %}

將工作流程資源類型新增至現有組態時，請在 `protected_types` 陣列中包含所有先前設定的資源類型。
{: .note}

## 工作流程存取層級

Flow Framework 為工作流程文件提供下列預先定義的存取層級。這些存取層級決定已獲授權存取工作流程資源的使用者所擁有的具體權限。

### workflow_read_only

`workflow_read_only` 唯讀存取層級允許使用者檢視和搜尋共用的工作流程，但無法修改。此存取層級包含下列權限：

```yaml
- "cluster:admin/opensearch/flow_framework/workflow/get"
- "cluster:admin/opensearch/flow_framework/workflow/search"
```
{% include copy.html %}

### workflow_read_write

`workflow_read_write` 讀寫存取層級授予使用者完整的工作流程操作存取權，但不包含共用能力。此存取層級包含所有讀取權限以及寫入操作：

```yaml
- "cluster:admin/opensearch/flow_framework/workflow/*"
- "cluster:monitor/*"
```
{% include copy.html %}

### workflow_full_access

`workflow_full_access` 完整存取層級授予使用者對工作流程的完整控制權，包括類似擁有者的權限，例如與其他使用者共用資源。此存取層級包含所有工作流程操作以及資源共用權限：

```yaml
- "cluster:admin/opensearch/flow_framework/workflow/*"
- "cluster:monitor/*"
- "cluster:admin/security/resource/share"
```
{% include copy.html %}

這些存取層級已預先定義，無法修改。若要要求新增存取層級，請在 [Flow Framework GitHub 儲存庫](https://github.com/opensearch-project/flow-framework/)中建立議題。
{: .note}

## 從舊版架構遷移

啟用資源共用並將工作流程標記為受保護的資源類型後，叢集管理員必須執行遷移 API，將現有的工作流程共用資訊從舊版架構移轉至新的資源共用系統。

僅限管理員：只有具備 superadmin 或 REST admin 權限的叢集管理員才能執行 Migrate API。
{: .important }

使用下列 API 呼叫，將舊版工作流程共用資料遷移至資源共用架構：

```json
POST _plugins/_security/api/resources/migrate
{
  "source_index": ".plugins-flow-framework-templates",
  "username_path": "/user/name",
  "backend_roles_path": "/user/backend_roles",
  "default_owner": "<replace-with-existing-user>",
  "default_access_level": {
    "workflow": "<select-appropriate-access-level>"
  }
}
```
{% include copy-curl.html %}

將 `<replace-with-existing-user>` 替換為現有使用者的使用者名稱，該使用者應擁有未明確指定擁有者資訊的工作流程。將 `<select-appropriate-access-level>` 替換為其中一個可用的工作流程存取層級：`workflow_read_only`、`workflow_read_write` 或 `workflow_full_access`。

## 相關文件

- [資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/) -- 後端概念、組態與設定
- [資源共用 API]({{site.url}}{{site.baseurl}}/security/access-control/resource-sharing-api/) -- 透過程式管理的 REST API 參考文件
- [資源存取管理]({{site.url}}{{site.baseurl}}/dashboards/management/resource-sharing/) -- UI 工作流程與使用者指引
- [工作流程狀態存取控制]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-state-access-control/) -- 工作流程執行狀態的存取控制