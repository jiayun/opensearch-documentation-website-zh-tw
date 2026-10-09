---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "警示資源存取控制"
nav_order: 12
parent: Alerting
has_children: false
---

# 警示資源存取控制

警示功能與 Security 外掛程式的資源共用與存取控制架構整合，為監視器和工作流程提供文件層級的授權。這會以更具彈性的共用系統取代舊版 `plugins.alerting.filter_by_backend_roles` 設定，讓資源擁有者能將特定存取層級授予使用者、角色或後端角色。

如需端對端架構的概念與 API，請參閱[資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/)。
{: .note}

## 資源組態

警示功能會註冊兩種資源類型，兩者都儲存在同一個組態索引中。下表說明警示資源組態。

| 資源類型 | 系統索引 | 導入版本 |
| :--- | :--- | :--- |
| `monitor` | `.opendistro-alerting-config` | OpenSearch 3.8 |
| `alerting-workflow` | `.opendistro-alerting-config` | OpenSearch 3.8 |

工作流程資源類型命名為 `alerting-workflow`，以避免與 Flow Framework 外掛程式註冊的 `workflow` 資源類型名稱衝突。由於兩種警示類型共用 `.opendistro-alerting-config` 索引，架構會依各文件中的欄位來區分它們。

啟用資源層級授權後，每個監視器和工作流程的可見性會由中央共用記錄控管。資源擁有者及具備共用能力的使用者，可以授予或撤銷特定使用者、角色或後端角色的存取權限。

警示和註解隸屬於其監視器。它們不是已註冊的資源類型，因此對它們的存取權限是衍生自對產生它們的監視器的存取權限。能存取某個監視器的使用者可以讀取其警示。新增註解則需要具備讀寫或完整存取層級的監視器存取權限。

## 啟用警示資源共用

若要為警示啟用資源共用，請將警示資源類型新增至受保護類型清單，並在叢集範圍內啟用資源共用。

僅限管理員：這些設定只能由具備超級管理員權限的叢集管理員進行設定。
{: .important }

### 使用 opensearch.yml 進行組態設定

將下列設定新增至您的 `opensearch.yml` 組態檔，以啟用警示的資源共用：

```yaml
plugins.security.resource_sharing.enabled: true
plugins.security.system_indices.enabled: true
plugins.security.resource_sharing.protected_types:
  - "monitor"
  - "alerting-workflow"
```
{% include copy.html %}

### 使用 Cluster Settings API 進行組態設定

或者，您可以使用 Cluster Settings API 動態啟用資源共用：

```json
PUT _cluster/settings
{
  "transient": {
    "plugins.security.resource_sharing.enabled": true,
    "plugins.security.resource_sharing.protected_types": ["monitor", "alerting-workflow"]
  }
}
```
{% include copy-curl.html %}

將警示資源類型新增至現有組態時，請在 `protected_types` 陣列中包含所有先前已設定的資源類型。
{: .note}

## 警示存取層級

警示功能提供三種預先定義的存取層級，適用於 `monitor` 和 `alerting-workflow` 兩種資源類型。這些存取層級會決定授予已取得監視器或工作流程資源存取權之使用者的特定權限。

### alerting_read_only

`alerting_read_only` 唯讀存取層級授予使用者檢視和搜尋共用監視器、工作流程及其警示的能力，但無法修改它們。此存取層級包含下列權限：

```yaml
- 'cluster:admin/opendistro/alerting/monitor/get'
- 'cluster:admin/opendistro/alerting/monitor/search'
- 'cluster:admin/opendistro/alerting/alerts/get'
- 'cluster:admin/opensearch/alerting/workflow/get'
- 'cluster:admin/opensearch/alerting/workflow_alerts/get'
- 'cluster:admin/opensearch/alerting/findings/get'
- 'cluster:admin/opendistro/alerting/destination/get'
```
{% include copy.html %}

### alerting_read_write

`alerting_read_write` 讀寫存取層級授予使用者對監視器和工作流程作業的完整存取權，包括警示和註解，但共用功能除外。此存取層級包含所有讀取權限以及寫入作業：

```yaml
- 'cluster:admin/opendistro/alerting/monitor/*'
- 'cluster:admin/opensearch/alerting/workflow/*'
- 'cluster:admin/opendistro/alerting/alerts/*'
- 'cluster:admin/opensearch/alerting/workflow_alerts/*'
- 'cluster:admin/opensearch/alerting/findings/*'
- 'cluster:admin/opendistro/alerting/destination/*'
- 'cluster:admin/opensearch/alerting/comments/*'
```
{% include copy.html %}

### alerting_full_access

`alerting_full_access` 完整存取層級授予使用者對監視器或工作流程的完整控制權，包括將資源與其他使用者共用等類似擁有者的權限。此存取層級包含所有讀寫權限以及遠端索引和資源共用權限：

```yaml
- 'cluster:admin/opendistro/alerting/monitor/*'
- 'cluster:admin/opensearch/alerting/workflow/*'
- 'cluster:admin/opendistro/alerting/alerts/*'
- 'cluster:admin/opensearch/alerting/workflow_alerts/*'
- 'cluster:admin/opensearch/alerting/findings/*'
- 'cluster:admin/opendistro/alerting/destination/*'
- 'cluster:admin/opensearch/alerting/comments/*'
- 'cluster:admin/opensearch/alerting/remote/indexes/get'
- 'cluster:admin/security/resource/share'
```
{% include copy.html %}

這些存取層級是預先定義的，無法修改。如需要求其他存取層級，請在 [Alerting GitHub 儲存庫](https://github.com/opensearch-project/alerting/) 中建立問題。
{: .note}

## 從舊版架構遷移

啟用資源共用並將警示資源類型標記為受保護後，叢集管理員必須執行遷移 API，將現有的監視器和工作流程共用資訊從舊版架構轉移至新的資源共用系統。

僅限管理員：Migrate API 只能由具備超級管理員或 REST 管理員權限的叢集管理員執行。
{: .important }

兩種警示資源類型都儲存在同一個索引中，但會將擁有者資訊保存在不同的路徑下 (`monitor.user` 和 `workflow.user`)。警示功能會在其資源提供者上宣告這些各類型專屬的路徑，因此架構會從正確的路徑讀取每份文件的擁有者。請求層級的 `username_path` 和 `backend_roles_path` 參數仍是必要，並會作為備援使用。

使用下列 API 呼叫，將舊版警示共用資料遷移至資源共用架構：

```json
POST _plugins/_security/api/resources/migrate
{
  "source_index": ".opendistro-alerting-config",
  "username_path": "/monitor/user/name",
  "backend_roles_path": "/monitor/user/backend_roles",
  "default_owner": "<replace-with-existing-user>",
  "default_access_level": {
    "monitor": "<select-appropriate-access-level>",
    "alerting-workflow": "<select-appropriate-access-level>"
  }
}
```
{% include copy-curl.html %}

將 `<replace-with-existing-user>` 取代為現有使用者的使用者名稱，該使用者應在沒有明確擁有權資訊的情況下擁有監視器和工作流程。將 `<select-appropriate-access-level>` 取代為可用的警示存取層級之一：`alerting_read_only`、`alerting_read_write` 或 `alerting_full_access`。

## 相關文件

- [資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/) -- 後端概念、組態與設定
- [資源共用 API]({{site.url}}{{site.baseurl}}/security/access-control/resource-sharing-api/) -- 以程式化管理為主的 REST API 參考
- [資源存取管理]({{site.url}}{{site.baseurl}}/dashboards/management/resource-sharing/) -- UI 工作流程與使用者指引
- [警示安全性]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/security/) -- 內建警示角色與舊版後端角色篩選
