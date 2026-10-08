---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工作流程狀態存取控制"
nav_order: 35
---

# 工作流程狀態存取控制

Flow Framework 與 Security 外掛程式的資源共用與存取控制架構整合，為工作流程狀態記錄提供文件層級的授權。這取代了舊版的 `plugins.flow_framework.filter_by_backend_roles` 設定，改用以更具彈性的共用系統，讓資源擁有者能將特定的存取層級授予使用者、角色或後端角色。

如需端對端架構概念與 API 的說明，請參閱[資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/)。
{: .note}

## 資源組態

下表說明工作流程狀態的資源組態。

| 欄位 | 值 |
| :--- | :--- |
| 資源類型 | `workflow-state` |
| 系統索引 | `.plugins-flow-framework-state` |
| 導入版本 | OpenSearch 3.4 |

為工作流程狀態啟用資源層級授權後，每個工作流程狀態的可見性會由一筆中央共用記錄控管。資源擁有者以及具備共用能力的使用者，可以授予或撤銷特定使用者、角色或後端角色的存取權限。

## 啟用工作流程狀態資源共用

若要為工作流程狀態啟用資源共用，您必須將 workflow-state 資源類型加入受保護類型清單，並在整個叢集啟用資源共用。

僅限管理員：這些設定只能由具備超級管理員權限的叢集管理員進行設定。
{: .important }

### 使用 opensearch.yml 進行組態設定

將下列設定加入您的 `opensearch.yml` 組態檔，以啟用工作流程狀態的資源共用：

```yaml
plugins.security.resource_sharing.enabled: true
plugins.security.system_indices.enabled: true
plugins.security.resource_sharing.protected_types:
  - "workflow-state"
```
{% include copy.html %}

### 使用 Cluster Settings API 進行組態設定

或者，您也可以使用 Cluster Settings API 動態啟用資源共用：

```json
PUT _cluster/settings
{
  "transient": {
    "plugins.security.resource_sharing.enabled": true,
    "plugins.security.resource_sharing.protected_types": ["workflow-state"]
  }
}
```
{% include copy-curl.html %}

將 workflow-state 資源類型加入現有組態時，請在 `protected_types` 陣列中包含所有先前已設定的資源類型。
{: .note}

## 工作流程狀態存取層級

Flow Framework 為工作流程狀態文件提供三種預先定義的存取層級。這些存取層級決定授予已取得工作流程狀態資源存取權之使用者的特定權限。

### workflow_state_read_only

`workflow_state_read_only` 唯讀存取層級授予使用者檢視與搜尋共用工作流程狀態的能力，但無法修改它們。此存取層級包含下列權限：

```yaml
- "cluster:admin/opensearch/flow_framework/workflow_state/get"
- "cluster:admin/opensearch/flow_framework/workflow_state/search"
```
{% include copy.html %}

### workflow_state_read_write

`workflow_state_read_write` 讀寫存取層級授予使用者對工作流程狀態作業的完整存取權，但共用功能除外。此存取層級包含所有讀取權限以及寫入作業：

```yaml
- "cluster:admin/opensearch/flow_framework/workflow_state/*"
- "cluster:monitor/*"
```
{% include copy.html %}

### workflow_state_full_access

`workflow_state_full_access` 完整存取層級授予使用者對工作流程狀態的完整控制權，包括將資源與其他使用者共用等類似擁有者的權限。此存取層級包含所有工作流程狀態作業以及資源共用權限：

```yaml
- "cluster:admin/opensearch/flow_framework/workflow_state/*"
- "cluster:monitor/*"
- "cluster:admin/security/resource/share"
```
{% include copy.html %}

這些存取層級為預先定義，無法修改。如需要求其他存取層級，請在 [Flow Framework GitHub 儲存庫](https://github.com/opensearch-project/flow-framework/)中建立 issue。
{: .note}

## 從舊版架構遷移

啟用資源共用並將工作流程狀態標記為受保護資源類型後，叢集管理員必須執行遷移 API，將現有的工作流程狀態共用資訊從舊版架構轉移至新的資源共用系統。

僅限管理員：Migrate API 只能由具備超級管理員或 REST 管理員權限的叢集管理員執行。
{: .important }

使用下列 API 呼叫，將舊版工作流程狀態共用資料遷移至資源共用架構：

```json
POST _plugins/_security/api/resources/migrate
{
  "source_index": ".plugins-flow-framework-state",
  "username_path": "/user/name",
  "backend_roles_path": "/user/backend_roles",
  "default_owner": "<replace-with-existing-user>",
  "default_access_level": {
    "workflow-state": "<select-appropriate-access-level>"
  }
}
```
{% include copy-curl.html %}

將 `<replace-with-existing-user>` 取代為現有使用者的使用者名稱，該使用者應擁有沒有明確擁有權資訊的工作流程狀態。將 `<select-appropriate-access-level>` 取代為可用的工作流程狀態存取層級之一：`workflow_state_read_only`、`workflow_state_read_write` 或 `workflow_state_full_access`。

## 相關文件

- [資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/) -- 後端概念、組態與設定
- [資源共用 API]({{site.url}}{{site.baseurl}}/security/access-control/resource-sharing-api/) -- 以程式化管理所需的 REST API 參考
- [資源存取管理]({{site.url}}{{site.baseurl}}/dashboards/management/resource-sharing/) -- UI 工作流程與使用者指引
- [工作流程存取控制]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-access-control/) -- 工作流程範本的存取控制