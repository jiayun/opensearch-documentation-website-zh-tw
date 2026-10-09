---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "透過資源共用進行模型存取控制"
parent: Integrating ML models
has_children: false
nav_order: 30
---

# 透過資源共用進行模型存取控制

在 ML Commons 中，模型的存取是透過[模型群組]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control/#model-groups)來控制——模型群組是共用相同存取權限之特定模型版本的集合。ML Commons 與 Security 外掛程式的資源共用及存取控制框架整合，為這些模型群組資源提供文件層級的授權。

這種資源共用方式是控制模型群組存取的新方法，並且比[原始的模型存取控制系統]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control/)提供更彈性的共用功能。資源擁有者可以針對個別模型群組，授予使用者、角色或後端角色特定的存取層級。

如需端對端框架概念與 API，請參閱[資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/)。
{: .note}

## 資源組態

下表說明機器學習 (ML) 模型群組的資源組態。

| 欄位 | 值 |
| :--- | :--- |
| 資源類型 | `ml-model-group` |
| 系統索引 | `.plugins-ml-model-group` |
| 導入版本 | OpenSearch 3.3 |

當 ML 模型群組啟用資源層級授權時，每個模型群組的可見性都由中央共用記錄管理。資源擁有者以及具備共用功能的使用者，可以授予或撤銷特定使用者、角色或後端角色的存取權限。

## 啟用 ML 模型群組資源共用

若要為 ML 模型群組啟用資源共用，您必須將 ml-model-group 資源類型新增至受保護類型清單，並在整個叢集範圍啟用資源共用。

僅限管理員：這些設定只能由具備 superadmin 權限的叢集管理員設定。
{: .important }

### 使用 opensearch.yml 進行組態

將下列設定新增至您的 `opensearch.yml` 組態檔，以啟用 ML 模型群組的資源共用：

```yaml
plugins.security.resource_sharing.enabled: true
plugins.security.system_indices.enabled: true
plugins.security.resource_sharing.protected_types:
  - "ml-model-group"
```
{% include copy.html %}

### 使用 Cluster Settings API 進行組態

或者，您可以使用 Cluster Settings API 動態啟用資源共用：

```json
PUT _cluster/settings
{
  "transient": {
    "plugins.security.resource_sharing.enabled": true,
    "plugins.security.resource_sharing.protected_types": ["ml-model-group"]
  }
}
```
{% include copy-curl.html %}

將 ml-model-group 資源類型新增至現有組態時，請在 `protected_types` 陣列中包含所有先前已設定的資源類型。
{: .note}

## ML 模型群組存取層級

ML Commons 為 ML 模型群組文件提供三個預先定義的存取層級。這些存取層級決定被授予模型群組資源存取權的使用者所取得的特定權限。

### ml_read_only

`ml_read_only` 唯讀存取層級讓使用者能夠檢視及搜尋共用的 ML 模型群組，但無法修改。此存取層級包含下列權限：

```yaml
- "cluster:admin/opensearch/ml/model_groups/get"
- "cluster:admin/opensearch/ml/models/get"
```
{% include copy.html %}

### ml_read_write

`ml_read_write` 讀寫存取層級授予使用者 ML 模型群組作業的完整存取權，但不包含共用功能。此存取層級包含所有讀取權限以及寫入作業：

```yaml
- "cluster:admin/opensearch/ml/*"
```
{% include copy.html %}

### ml_full_access

`ml_full_access` 完整存取層級授予使用者對 ML 模型群組的完整控制權，包括類似擁有者的權限，例如與其他使用者共用資源。此存取層級包含所有 ML 模型群組作業以及資源共用權限：

```yaml
- "cluster:admin/opensearch/ml/*"
- "cluster:admin/security/resource/share"
```
{% include copy.html %}

這些存取層級是預先定義的，無法修改。若要要求其他存取層級，請在 [ML Commons GitHub 儲存庫](https://github.com/opensearch-project/ml-commons/)中建立 issue。
{: .note}

## 從舊版框架遷移

啟用資源共用並將 ML 模型群組標記為受保護資源類型之後，叢集管理員必須執行遷移 API，將現有的模型群組共用資訊從舊版框架轉移至新的資源共用系統。

僅限管理員：Migrate API 只能由具備 superadmin 或 REST admin 權限的叢集管理員執行。
{: .important }

使用下列 API 呼叫，將舊版 ML 模型群組共用資料遷移至資源共用框架：

```json
POST _plugins/_security/api/resources/migrate
{
  "source_index": ".plugins-ml-model-group",
  "username_path": "/owner/name",
  "backend_roles_path": "/owner/backend_roles",
  "default_owner": "<replace-with-existing-user>",
  "default_access_level": {
    "ml-model-group": "<select-appropriate-access-level>"
  }
}
```
{% include copy-curl.html %}

將 `<replace-with-existing-user>` 取代為應擁有沒有明確擁有權資訊之 ML 模型群組的現有使用者名稱。將 `<select-appropriate-access-level>` 取代為其中一個可用的 ML 模型群組存取層級：`ml_read_only`、`ml_read_write` 或 `ml_full_access`。

## 相關文件

- [資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/) -- 後端概念、組態與設定
- [資源共用 API]({{site.url}}{{site.baseurl}}/security/access-control/resource-sharing-api/) -- 用於程式化管理之 REST API 參考
- [資源存取管理]({{site.url}}{{site.baseurl}}/dashboards/management/resource-sharing/) -- UI 工作流程與使用者指引