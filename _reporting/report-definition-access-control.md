---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "報表定義存取控制"
nav_order: 15
---

# 報表定義存取控制

Reporting 外掛程式與 Security 外掛程式的資源共用與存取控制架構整合，為報表定義記錄提供文件層級的授權。這會以更具彈性的共用系統取代舊版的 `plugins.alerting.filter_by_backend_roles` 設定，讓資源擁有者可以將特定的存取層級授予使用者、角色或後端角色。

如需端對端架構的概念與 API，請參閱[資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/)。
{: .note}

## 資源組態

下表說明報表定義的資源組態。

| 欄位 | 值                             |
| :--- |:----------------------------------|
| 資源類型 | `report-definition`               |
| 系統索引 | `.opendistro-reports-definitions` |
| 導入版本 | OpenSearch 3.5                    |

為報表定義啟用資源層級授權後，每個報表定義的可見性會由一筆中央共用記錄控管。資源擁有者以及具備共用能力的使用者，可以為特定的使用者、角色或後端角色授予或撤銷存取權限。

## 啟用報表定義資源共用

若要為報表定義啟用資源共用，您必須將報表定義資源類型加入受保護類型清單，並在整個叢集啟用資源共用。

僅限管理員：這些設定只能由具備超級管理員權限的叢集管理員進行設定。
{: .important }

### 使用 opensearch.yml 進行組態設定

將下列設定加入您的 `opensearch.yml` 組態檔，以啟用報表定義的資源共用：

```yaml
plugins.security.resource_sharing.enabled: true
plugins.security.system_indices.enabled: true
plugins.security.resource_sharing.protected_types:
  - "report-definition"
```
{% include copy.html %}

### 使用 Cluster Settings API 進行組態設定

或者，您可以使用 Cluster Settings API 動態啟用資源共用：

```json
PUT _cluster/settings
{
  "transient": {
    "plugins.security.resource_sharing.enabled": true,
    "plugins.security.resource_sharing.protected_types": ["report-definition"]
  }
}
```
{% include copy-curl.html %}

將報表定義資源類型加入現有組態時，請在 `protected_types` 陣列中包含所有先前已設定的資源類型。
{: .note}

## 報表定義存取層級

Reporting 為報表定義文件提供下列預先定義的存取層級。這些存取層級會決定授予給已獲報表定義資源存取權之使用者的特定權限。

### rd_read_only

`rd_read_only` 唯讀存取層級可讓使用者檢視及搜尋共用的報表定義，但無法修改。此存取層級包含下列權限：

```yaml
- "cluster:admin/opendistro/reports/definition/get"
- "cluster:admin/opendistro/reports/definition/list"
- "cluster:admin/opendistro/reports/instance/get"
- "cluster:admin/opendistro/reports/instance/list"
- "cluster:admin/opendistro/reports/menu/download"
```
{% include copy.html %}

### rd_read_write

`rd_read_write` 讀寫存取層級可讓使用者完整存取報表定義作業，但共用功能除外。此存取層級包含所有讀取權限以及寫入作業：

```yaml
- "cluster:admin/opendistro/reports/definition/*"
- "cluster:admin/opendistro/reports/instance/*"
- "cluster:admin/opendistro/reports/menu/download"
```
{% include copy.html %}

### rd_full_access

`rd_full_access` 完整存取層級可讓使用者完整控制報表定義，包括將資源與其他使用者共用等擁有者層級的權限。此存取層級包含所有報表定義作業以及資源共用權限：

```yaml
- "cluster:admin/opendistro/reports/definition/*"
- "cluster:admin/opendistro/reports/instance/get"
- "cluster:admin/opendistro/reports/instance/list"
- "cluster:admin/opendistro/reports/menu/download"
- "cluster:admin/security/resource/share"
```
{% include copy.html %}

這些存取層級為預先定義，無法修改。如需其他存取層級，請在 [Reporting GitHub 儲存庫](https://github.com/opensearch-project/reporting/) 建立 issue。
{: .note}

## 從舊版架構遷移

啟用資源共用並將報表定義標記為受保護資源類型後，叢集管理員必須執行 Migrate API，將現有的報表定義共用資訊從舊版架構轉移至新的資源共用系統。

僅限管理員：Migrate API 只能由具備超級管理員或 REST 管理員權限的叢集管理員執行。
{: .important }

使用下列 API 呼叫，將舊版報表定義共用資料遷移至資源共用架構：

```json
POST _plugins/_security/api/resources/migrate
{
  "source_index": ".opendistro-reports-definitions",
  "username_path": "/user/name",
  "backend_roles_path": "/user/backend_roles",
  "default_owner": "<replace-with-existing-user>",
  "default_access_level": {
    "report-definition": "<select-appropriate-access-level>"
  }
}
```
{% include copy-curl.html %}

將 `<replace-with-existing-user>` 取代為應擁有無明確擁有權資訊之報表定義的現有使用者名稱。將 `<select-appropriate-access-level>` 取代為可用的報表定義存取層級之一：`rd_read_only`、`rd_read_write` 或 `rd_full_access`。

## 相關文件

- [資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/) -- 後端概念、組態與設定
- [資源共用 API]({{site.url}}{{site.baseurl}}/security/access-control/resource-sharing-api/) -- 以程式化管理所需的 REST API 參考
- [資源存取管理]({{site.url}}{{site.baseurl}}/dashboards/management/resource-sharing/) -- UI 工作流程與使用者指引
- [報表執行個體存取控制]({{site.url}}{{site.baseurl}}/reporting/report-instance-access-control/) -- 報表執行個體的存取控制