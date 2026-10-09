---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Security Analytics 資源存取控制"
nav_order: 3
has_children: false
---

# Security Analytics 資源存取控制

Security Analytics 與 Security 外掛程式的資源共用與存取控制框架整合，為偵測器與關聯規則提供文件層級授權。此功能以更彈性的共用系統取代舊版 `plugins.security_analytics.filter_by_backend_roles` 設定，讓資源擁有者可以授予使用者、角色或後端角色特定的存取層級。

如需端對端框架概念與 API，請參閱[資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/)。
{: .note}

## 資源組態

Security Analytics 註冊了兩種資源類型。下表說明 Security Analytics 的資源組態。

| 資源類型 | 系統索引 | 導入版本 |
| :--- | :--- | :--- |
| `detector` | `.opensearch-sap-detectors-config` | OpenSearch 3.8 |
| `correlation-rule` | `.opensearch-sap-correlation-rules-config` | OpenSearch 3.8 |

啟用資源層級授權後，每個偵測器與關聯規則的可見性都由中央共用記錄管理。資源擁有者與具備共用能力的使用者可以授予或撤銷特定使用者、角色或後端角色的存取權限。

## 啟用 Security Analytics 資源共用

若要啟用 Security Analytics 的資源共用，請將 Security Analytics 資源類型加入受保護類型清單，並在整個叢集範圍內啟用資源共用。

僅限管理員：這些設定只能由具備 superadmin 權限的叢集管理員設定。
{: .important }

### 使用 opensearch.yml 設定

將下列設定加入您的 `opensearch.yml` 組態檔，以啟用 Security Analytics 的資源共用：

```yaml
plugins.security.resource_sharing.enabled: true
plugins.security.system_indices.enabled: true
plugins.security.resource_sharing.protected_types:
  - "detector"
  - "correlation-rule"
```
{% include copy.html %}

### 使用 Cluster Settings API 設定

或者，您可以使用 Cluster Settings API 動態啟用資源共用：

```json
PUT _cluster/settings
{
  "transient": {
    "plugins.security.resource_sharing.enabled": true,
    "plugins.security.resource_sharing.protected_types": ["detector", "correlation-rule"]
  }
}
```
{% include copy-curl.html %}

將 Security Analytics 資源類型加入現有組態時，請在 `protected_types` 陣列中包含所有先前已設定的資源類型。
{: .note}

## Security Analytics 存取層級

Security Analytics 提供三種預先定義的存取層級，適用於 `detector` 與 `correlation-rule` 兩種資源類型。這些存取層級決定被授予偵測器或關聯規則資源存取權的使用者所取得的特定權限。

### sa_read_only

`sa_read_only` 唯讀存取層級讓使用者可以檢視與搜尋共用資源，但無法修改。對於偵測器，此存取層級包含下列權限：

```yaml
- 'cluster:admin/opensearch/securityanalytics/detector/get'
- 'cluster:admin/opensearch/securityanalytics/detector/search'
- 'cluster:admin/opensearch/securityanalytics/alerts/get'
- 'cluster:admin/opensearch/securityanalytics/findings/get'
- 'cluster:admin/opensearch/securityanalytics/mapping/get'
- 'cluster:admin/opensearch/securityanalytics/mapping/view/get'
```
{% include copy.html %}

對於關聯規則，此存取層級包含下列權限：

```yaml
- 'cluster:admin/opensearch/securityanalytics/correlation/rule/search'
- 'cluster:admin/opensearch/securityanalytics/correlations/list'
- 'cluster:admin/opensearch/securityanalytics/correlations/findings'
- 'cluster:admin/opensearch/securityanalytics/correlationAlerts/get'
```
{% include copy.html %}

### sa_read_write

`sa_read_write` 讀寫存取層級讓使用者可以完整執行資源操作，但不包含共用能力。對於偵測器，此存取層級包含下列權限：

```yaml
- 'cluster:admin/opensearch/securityanalytics/detector/*'
- 'cluster:admin/opensearch/securityanalytics/alerts/*'
- 'cluster:admin/opensearch/securityanalytics/findings/*'
- 'cluster:admin/opensearch/securityanalytics/mapping/*'
- 'cluster:admin/opensearch/securityanalytics/rule/*'
```
{% include copy.html %}

對於關聯規則，此存取層級包含下列權限：

```yaml
- 'cluster:admin/index/correlation/rules/*'
- 'cluster:admin/opensearch/securityanalytics/correlation/rule/search'
- 'cluster:admin/opensearch/securityanalytics/correlations/*'
- 'cluster:admin/opensearch/securityanalytics/correlationAlerts/*'
```
{% include copy.html %}

### sa_full_access

`sa_full_access` 完整存取層級讓使用者對資源擁有完整控制權，包括類似擁有者的權限，例如與其他使用者共用資源。此存取層級包含該資源類型的所有讀寫權限，以及資源共用權限：

```yaml
- 'cluster:admin/security/resource/share'
```
{% include copy.html %}

這些存取層級是預先定義的，無法修改。若要要求新增存取層級，請在 [Security Analytics GitHub 儲存庫](https://github.com/opensearch-project/security-analytics/)建立 issue。
{: .note}

## 從舊版框架遷移

啟用資源共用並將 Security Analytics 資源類型標記為受保護之後，叢集管理員必須執行遷移 API，將現有的偵測器與關聯規則共用資訊從舊版框架轉移到新的資源共用系統。每個資源索引只需執行遷移一次。

僅限管理員：Migrate API 只能由具備 superadmin 或 REST 管理員權限的叢集管理員執行。
{: .important }

使用下列 API 呼叫，將舊版偵測器共用資料遷移至資源共用框架：

```json
POST _plugins/_security/api/resources/migrate
{
  "source_index": ".opensearch-sap-detectors-config",
  "username_path": "/user/name",
  "backend_roles_path": "/user/backend_roles",
  "default_owner": "<replace-with-existing-user>",
  "default_access_level": {
    "detector": "<select-appropriate-access-level>"
  }
}
```
{% include copy-curl.html %}

接著對關聯規則索引再次執行遷移，使用 `.opensearch-sap-correlation-rules-config` 作為 `source_index`，並使用 `correlation-rule` 作為 `default_access_level` 鍵。

將 `<replace-with-existing-user>` 取代為現有使用者的使用者名稱，該使用者將擁有沒有明確擁有權資訊的資源。將 `<select-appropriate-access-level>` 取代為其中一個可用的 Security Analytics 存取層級：`sa_read_only`、`sa_read_write` 或 `sa_full_access`。

## 相關文件

- [資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/) -- 後端概念、組態與設定
- [資源共用 API]({{site.url}}{{site.baseurl}}/security/access-control/resource-sharing-api/) -- 用於程式化管理 REST API 參考
- [資源存取管理]({{site.url}}{{site.baseurl}}/dashboards/management/resource-sharing/) -- UI 工作流程與使用者指引
- [Security Analytics 的 OpenSearch 安全性]({{site.url}}{{site.baseurl}}/security-analytics/security/) -- 基本權限與舊版後端角色篩選
