---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "資源共享與存取控制"
parent: Access control
nav_order: 110
has_children: true
has_toc: false
---

# 資源共享與存取控制

**於 3.3 版導入**
{: .label .label-purple }

OpenSearch Security 外掛程式中的資源共享與存取控制框架，為外掛程式定義的資源提供*文件層級*的細微存取管理。它擴充了 OpenSearch 現有的角色型存取控制，讓資源擁有者能夠明確地將個別資源與其他主體共享。

_資源_是儲存在外掛程式系統索引中的文件。資源共享資訊儲存在由安全性功能集中管理的系統索引中。

資源共享需要外掛程式開發人員、管理員和使用者之間的協調。外掛程式開發人員必須先在其外掛程式中實作資源共享支援，並定義可共享的資源類型（例如 `ml-model-group` 或 `anomaly-detector`）。安裝支援資源共享的外掛程式後，管理員可在整個叢集啟用此功能，並設定使用資源層級授權的資源類型。最後，使用者只要具備必要的叢集權限，即可透過 UI 或 API 建立與共享資源。

本文件適用於想要設定與使用資源共享的**使用者**和**管理員**。如果您是正在為外掛程式實作資源共享支援的**外掛程式開發人員**，請參閱[開發人員文件](https://github.com/opensearch-project/security/blob/main/RESOURCE_SHARING_AND_ACCESS_CONTROL.md)。

資源共享可執行下列操作：

- **資源擁有者**可以共享或撤銷其資源的存取權。
- **資源擁有者**可以允許具備共享權限的使用者重新分配存取權。
- 具備 superadmin 權限的**管理員**可以檢視和管理所有可共享的資源。
- **所有使用者**都可以搜尋資源索引，Security 外掛程式會自動套用每位使用者的篩選。

## 設定資源共享

資源共享預設為停用。若要設定資源共享，請依照下列步驟操作。

在設定資源共享之前，請確認您要搭配資源共享使用的外掛程式已實作資源共享支援。如果您需要為外掛程式新增資源共享支援，請參閱[開發人員文件](https://github.com/opensearch-project/security/blob/main/RESOURCE_SHARING_AND_ACCESS_CONTROL.md)。
{: .note}

### 步驟 1：啟用資源共享

若要啟用資源共享，請將下列設定新增至 `opensearch.yml` 檔案：

```yaml
plugins.security.resource_sharing.enabled: true
plugins.security.system_indices.enabled: true
```
{% include copy.html %}

新增至 `opensearch.yml` 的設定會在叢集重新啟動後生效。若要在不重新啟動叢集的情況下更新這兩項資源共享設定，請使用 Cluster Settings API：

```json
PUT _cluster/settings
{
  "transient": {
    "plugins.security.resource_sharing.enabled": true,
    "plugins.security.resource_sharing.protected_types": ["sample-resource"]
  }
}
```
{% include copy-curl.html security=true %}

### 步驟 2：設定受保護的資源類型

在受保護類型組態中列出資源類型，以指定使用資源層級授權的資源類型。此設定會決定哪些外掛程式定義的資源使用共享與存取控制框架：

```yaml
plugins.security.resource_sharing.protected_types: ["sample-resource", "ml-model"]
```
{% include copy.html %}

您指定的資源類型必須與已安裝外掛程式支援的資源類型完全相符。若要找出叢集中可用的資源類型，請依照下列步驟操作：

1. 一開始先以空的 `protected_types` 組態**啟用資源共享**。
2. **使用 [List resource types API]({{site.url}}{{site.baseurl}}/security/access-control/resource-sharing-api/#list-resource-types)** 找出已安裝外掛程式所有可用的資源類型。
3. 以您要啟用的資源類型**更新 `protected_types` 組態**。

## 各外掛程式的資源類型

下表說明支援資源共享的外掛程式所註冊的資源類型。每個外掛程式的頁面會說明其資源類型的存取層級，以及從舊版後端角色篩選設定遷移的步驟。

| 外掛程式 | 資源類型 | 外掛程式文件 |
| :--- | :--- | :--- |
| Alerting | `monitor`, `alerting-workflow` | [Alerting 資源存取控制]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/alerting-access-control/) |
| Anomaly Detection | `anomaly-detector` | [異常偵測器存取控制]({{site.url}}{{site.baseurl}}/observing-your-data/ad/detector-access-control/) |
| Anomaly Detection | `forecaster` | [Forecaster 存取控制]({{site.url}}{{site.baseurl}}/observing-your-data/forecast/forecaster-access-control/) |
| Flow Framework | `workflow` | [工作流程存取控制]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-access-control/) |
| Flow Framework | `workflow-state` | [工作流程狀態存取控制]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-state-access-control/) |
| ML Commons | `ml-model-group` | [透過資源共享進行模型存取控制]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-sharing-access-control/) |
| Notifications | `notification_config` | [通知存取控制]({{site.url}}{{site.baseurl}}/observing-your-data/notifications/notification-access-control/) |
| Reporting | `report-definition` | [報告定義存取控制]({{site.url}}{{site.baseurl}}/reporting/report-definition-access-control/) |
| Reporting | `report-instance` | [報告執行個體存取控制]({{site.url}}{{site.baseurl}}/reporting/report-instance-access-control/) |
| Security Analytics | `detector`, `correlation-rule` | [Security Analytics 資源存取控制]({{site.url}}{{site.baseurl}}/security-analytics/resource-access-control/) |

Security Analytics 的 `detector` 資源類型與 Anomaly Detection 的 `anomaly-detector` 資源類型不同，Alerting 的 `alerting-workflow` 資源類型也與 Flow Framework 的 `workflow` 資源類型不同。
{: .note}

以下是保護 ML Commons 與 Anomaly Detection 資源類型的範例組態：

```yaml
plugins.security.resource_sharing.protected_types: ["ml-model-group", "anomaly-detector", "forecaster"]
```
{% include copy.html %}

## 必要權限

若要透過外掛程式 API 存取共享資源，使用者需要這些特定外掛程式的叢集層級權限。管理員應在 `roles.yml` 中設定適當的角色。以下範例顯示 `sample-resource-plugin` 的組態：

```yaml
sample_full_access:
  cluster_permissions:
    - 'cluster:admin/sample-resource-plugin/*'

sample_read_access:
  cluster_permissions:
    - 'cluster:admin/sample-resource-plugin/get'
```
{% include copy.html %}

資源共享不會自動授予 API 存取權。若要透過 API 存取資源，使用者必須同時具備：

1. 外掛程式 API 的叢集權限。
2. 透過共享 API 與其共享的資源。

## 資料模型

所有共享中繼資料（列於下表）都儲存在專屬的*安全性自有*系統索引中。

| 欄位         | 說明                                    |
|:---|:---|
| `resource_id` | 資源的唯一識別碼。              |
| `created_by`  | 資源建立者的使用者名稱（以及租用戶，若適用）。    |
| `share_with`  | 動作群組與允許主體的對應。 |
| `source_idx`  | 由外掛程式管理的資源索引。           |

以下範例顯示由使用者 `bob` 在 `analytics` 租用戶中建立的 ID 為 `model-group-123` 的資源。該資源與特定使用者、角色和後端角色共享，並具有唯讀存取權：

```json
{
  "resource_id": "model-group-123",
  "created_by": {
    "user": "bob",
    "tenant": "analytics"
  },
  "share_with": {
    "read_only": {
      "users": ["alice"],
      "roles": ["data_viewer"],
      "backend_roles": ["analytics_backend"]
    }
  }
}
```
{% include copy.html %}

在此範例中：

- 在唯讀層級：

 - 使用者：`alice` 可以存取該資源。

 - 角色：任何被指派 `data_viewer` 角色的使用者都可以存取該資源。

 - 後端角色：任何對應到 `analytics_backend` 後端角色的使用者都可以存取該資源。

若要將此資源設為公開，請將 `users` 設為 `["*"]`：

```json
PATCH _plugins/_security/api/resource/share
{
  "resource_id": "model-group-123",
  "resource_type": "ml-model-group",
  "add": {
    "read_only": { "users": ["*"] }
  }
}
```
{% include copy-curl.html security=true %}

若要將資源保持為私人，請將 `share_with` 物件設為空：

```json
PUT _plugins/_security/api/resource/share
{
  "resource_id": "model-group-123",
  "resource_type": "ml-model-group",
  "share_with": {}
}
```
{% include copy-curl.html security=true %}

## REST API

您可以使用資源共享 API 操作來共享資源、管理存取權限，以及自動化資源共享工作流程。

完整的 API 文件請參閱[資源共享 API]({{site.url}}{{site.baseurl}}/security/access-control/resource-sharing-api/)。

## 需求與限制

為確保資源共享與存取控制正常運作，適用下列需求與限制：

* 只有資源擁有者、superadmin，或被明確授予共享權限的使用者，才能共享或撤銷存取權。
* 所有資源都必須位於系統索引中。
* 必須啟用系統索引保護。
* 使用者仍需要外掛程式層級的叢集權限，包括建立資源的權限。
* 動作群組必須在外掛程式組態中定義。

## 最佳做法

管理資源共享時，管理員應遵循下列最佳做法：

- 在新叢集使用前先啟用資源共享。

- 保持系統索引保護為啟用狀態。

- 以最小且明確的方式共享資源，以維持安全性與控制。

## 相關文件

- [資源共享 API]({{site.url}}{{site.baseurl}}/security/access-control/resource-sharing-api/) -- 以程式化管理為目的的 REST API 參考
- [資源存取管理]({{site.url}}{{site.baseurl}}/dashboards/management/resource-sharing/) -- UI 工作流程與使用者指引
- [各外掛程式的資源類型](#resource-types-by-plugin) -- 各外掛程式的存取層級與遷移步驟
- [開發人員文件](https://github.com/opensearch-project/security/blob/main/RESOURCE_SHARING_AND_ACCESS_CONTROL.md) -- 適用於外掛程式開發人員、使用者與管理員的詳細技術文件
