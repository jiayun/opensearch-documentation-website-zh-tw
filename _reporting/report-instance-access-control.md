---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "報告執行個體存取控制"
nav_order: 20
---

# 報告執行個體存取控制

Reporting 外掛程式與 Security 外掛程式的資源共用及存取控制框架整合，為報告執行個體記錄提供文件層級授權。這取代了舊有的 `plugins.alerting.filter_by_backend_roles` 設定，改用更具彈性的共用系統，讓資源擁有者可以授予使用者、角色或後端角色特定的存取層級。

如需端對端框架概念與 API，請參閱[資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/)。
{: .note}

## 資源組態

下表說明報告執行個體的資源組態。

| 欄位 | 值                             |
| :--- |:----------------------------------|
| 資源類型 | `report-instance`               |
| 系統索引 | `.opendistro-reports-instances` |
| 導入版本 | OpenSearch 3.5                    |

當報告執行個體啟用資源層級授權時，每個報告執行個體的可見性都由中央共用記錄管理。資源擁有者以及具備共用能力的使用者，可以授予或撤銷特定使用者、角色或後端角色的存取權限。

## 啟用報告執行個體資源共用

若要啟用報告執行個體的資源共用，您必須將報告執行個體資源類型新增至受保護類型清單，並在整個叢集啟用資源共用。

僅限管理員：這些設定只能由具備 superadmin 權限的叢集管理員設定。
{: .important }

### 使用 opensearch.yml 進行組態

將下列設定新增至您的 `opensearch.yml` 組態檔，以啟用報告執行個體的資源共用：

```yaml
plugins.security.resource_sharing.enabled: true
plugins.security.system_indices.enabled: true
plugins.security.resource_sharing.protected_types:
  - "report-instance"
```
{% include copy.html %}

### 使用 Cluster Settings API 進行組態

或者，您可以使用 Cluster Settings API 動態啟用資源共用：

```json
PUT _cluster/settings
{
  "transient": {
    "plugins.security.resource_sharing.enabled": true,
    "plugins.security.resource_sharing.protected_types": ["report-instance"]
  }
}
```
{% include copy-curl.html %}

將報告執行個體資源類型新增至現有組態時，請在 `protected_types` 陣列中包含所有先前已設定的資源類型。
{: .note}

## 報告執行個體存取層級

Reporting 為報告執行個體文件提供下列預先定義的存取層級。這些存取層級決定被授予報告執行個體資源存取權的使用者所取得的特定權限。

### ri_read_only

`ri_read_only` 唯讀存取層級讓使用者能夠檢視與搜尋共用的報告執行個體，但無法修改。此存取層級包含下列權限：

```yaml
- "cluster:admin/opendistro/reports/instance/get"
- "cluster:admin/opendistro/reports/instance/list"
- "cluster:admin/opendistro/reports/menu/download"
```
{% include copy.html %}

### ri_read_write

`ri_read_write` 讀寫存取層級授予使用者報告執行個體作業的完整存取權，但不包含共用功能。此存取層級包含所有讀取權限以及寫入作業：

```yaml
- "cluster:admin/opendistro/reports/instance/*"
- "cluster:admin/opendistro/reports/menu/download"
```
{% include copy.html %}

### ri_full_access

`ri_full_access` 完整存取層級授予使用者對報告執行個體的完整控制權，包括類似擁有者的權限，例如與其他使用者共用資源。此存取層級包含所有報告執行個體作業以及資源共用權限：

```yaml
- "cluster:admin/opendistro/reports/instance/*"
- "cluster:admin/opendistro/reports/menu/download"
- "cluster:admin/security/resource/share"
```
{% include copy.html %}

這些存取層級為預先定義，無法修改。若要要求其他存取層級，請在 [Reporting GitHub 儲存庫](https://github.com/opensearch-project/reporting/)提出議題。
{: .note}

## 從舊有框架遷移

啟用資源共用並將報告執行個體標記為受保護資源類型後，叢集管理員必須執行 Migrate API，將現有的報告執行個體共用資訊從舊有框架轉移至新的資源共用系統。

僅限管理員：Migrate API 只能由具備 superadmin 或 REST 管理員權限的叢集管理員執行。
{: .important }

使用下列 API 呼叫，將舊有的報告執行個體共用資料遷移至資源共用框架：

```json
POST _plugins/_security/api/resources/migrate
{
  "source_index": ".opendistro-reports-instances",
  "username_path": "/user/name",
  "backend_roles_path": "/user/backend_roles",
  "default_owner": "<replace-with-existing-user>",
  "default_access_level": {
    "report-instance": "<select-appropriate-access-level>"
  }
}
```
{% include copy-curl.html %}

將 `<replace-with-existing-user>` 取代為現有使用者的使用者名稱，該使用者應擁有沒有明確擁有權資訊的報告執行個體。將 `<select-appropriate-access-level>` 取代為其中一個可用的報告執行個體存取層級：`ri_read_only`、`ri_read_write` 或 `ri_full_access`。

## 相關文件

- [資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/) -- 後端概念、組態與設定
- [資源共用 API]({{site.url}}{{site.baseurl}}/security/access-control/resource-sharing-api/) -- 供程式化管理使用的 REST API 參考文件
- [資源存取管理]({{site.url}}{{site.baseurl}}/dashboards/management/resource-sharing/) -- UI 工作流程與使用者指引
- [報告定義存取控制]({{site.url}}{{site.baseurl}}/reporting/report-definition-access-control/) -- 報告定義的存取控制