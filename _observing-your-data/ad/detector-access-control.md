---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "異常偵測器存取控制"
nav_order: 40
parent: Anomaly detection
has_children: false
redirect_from:
  - /monitoring-plugins/ad/detector-access-control/
---

# 異常偵測器存取控制

Anomaly Detection 與 Security 外掛程式的資源共用及存取控制架構整合，為異常偵測器資源提供文件層級的授權。此機制以更具彈性的共用系統取代舊版的 `plugins.anomaly_detection.filter_by_backend_roles` 設定，讓資源擁有者能夠將特定存取層級授予使用者、角色或後端角色。

如需完整的架構概念與 API，請參閱[資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/)。
{: .note}

## 資源組態

下表說明異常偵測器的資源組態。

| 欄位 | 值 |
| :--- | :--- |
| 資源類型 | `anomaly-detector` |
| 系統索引 | `.opendistro-anomaly-detectors` |
| 導入版本 | OpenSearch 3.3 |

為異常偵測器啟用資源層級授權後，每個偵測器的可見性皆由一份集中式共用記錄管理。資源擁有者以及具備共用功能的使用者，可以針對特定使用者、角色或後端角色授予或撤銷存取權限。

## 啟用異常偵測器資源共用

若要為異常偵測器啟用資源共用，您必須將 anomaly-detector 資源類型新增至受保護類型清單，並在整個叢集啟用資源共用。

僅限管理員：這些設定只能由具備超級管理員權限的叢集管理員進行設定。
{: .important }

### 使用 opensearch.yml 進行設定

將下列設定新增至您的 `opensearch.yml` 組態檔案，以為異常偵測器啟用資源共用：

```yaml
plugins.security.resource_sharing.enabled: true
plugins.security.system_indices.enabled: true
plugins.security.resource_sharing.protected_types:
  - "anomaly-detector"
```
{% include copy.html %}

### 使用 Cluster Settings API 進行設定

或者，您也可以使用 Cluster Settings API 動態啟用資源共用：

```json
PUT _cluster/settings
{
  "transient": {
    "plugins.security.resource_sharing.enabled": true,
    "plugins.security.resource_sharing.protected_types": ["anomaly-detector"]
  }
}
```
{% include copy-curl.html %}

將 anomaly-detector 資源類型新增至現有組態時，請在 `protected_types` 陣列中包含所有先前已設定的資源類型。
{: .note}

## 異常偵測器存取層級

Anomaly Detection 為異常偵測器文件提供三種預先定義的存取層級。這些存取層級決定了授予已獲得偵測器資源存取權之使用者的具體權限。

### ad_read_only

`ad_read_only` 唯讀存取層級讓使用者能夠檢視及搜尋共用的異常偵測器，但無法修改。此存取層級包含下列權限：

```yaml
- 'cluster:admin/opendistro/ad/detector/info'
- 'cluster:admin/opendistro/ad/detector/validate'
- 'cluster:admin/opendistro/ad/detector/preview'
- 'cluster:admin/opendistro/ad/detectors/get'
- 'cluster:admin/opendistro/ad/result/topAnomalies'
```
{% include copy.html %}

### ad_read_write

`ad_read_write` 讀寫存取層級授予使用者除共用功能以外的完整異常偵測器操作存取權。此存取層級包含所有讀取權限以及寫入操作：

```yaml
- "cluster:admin/opendistro/ad/*"
- 'cluster:monitor/*'
- "cluster:admin/ingest/pipeline/delete"
- "cluster:admin/ingest/pipeline/put"
```
{% include copy.html %}

### ad_full_access

`ad_full_access` 完整存取層級授予使用者對異常偵測器的完全控制權，包括類似擁有者的權限，例如與其他使用者共用該資源。此存取層級包含所有異常偵測器操作以及資源共用權限：

```yaml
- "cluster:admin/ingest/pipeline/delete"
- "cluster:admin/ingest/pipeline/put"
- "cluster:admin/opendistro/ad/*"
- 'cluster:monitor/*'
- "cluster:admin/security/resource/share"
```
{% include copy.html %}

這些存取層級為預先定義，無法修改。若要請求其他存取層級，請在 [Anomaly Detection GitHub 儲存庫](https://github.com/opensearch-project/anomaly-detection/)中建立 issue。
{: .note}

## 從舊版架構遷移

啟用資源共用並將異常偵測器標記為受保護的資源類型後，叢集管理員必須執行遷移 API，將現有的偵測器共用資訊從舊版架構轉移至新的資源共用系統。

僅限管理員：Migrate API 只能由具備超級管理員或 REST 管理員權限的叢集管理員執行。
{: .important }

使用下列 API 呼叫，將舊版異常偵測器共用資料遷移至資源共用架構：

```json
POST _plugins/_security/api/resources/migrate
{
  "source_index": ".opendistro-anomaly-detectors",
  "username_path": "/user/name",
  "backend_roles_path": "/user/backend_roles",
  "default_owner": "<replace-with-existing-user>",
  "default_access_level": {
    "anomaly-detector": "<select-appropriate-access-level>"
  }
}
```
{% include copy-curl.html %}

將 `<replace-with-existing-user>` 替換為現有使用者的使用者名稱，該使用者將成為沒有明確擁有權資訊之異常偵測器的擁有者。將 `<select-appropriate-access-level>` 替換為下列其中一個可用的異常偵測器存取層級：`ad_read_only`、`ad_read_write` 或 `ad_full_access`。

## 相關文件

- [資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/) -- 後端概念、組態與設定
- [資源共用 API]({{site.url}}{{site.baseurl}}/security/access-control/resource-sharing-api/) -- 用於程式化管理的 REST API 參考資料
- [資源存取管理]({{site.url}}{{site.baseurl}}/dashboards/management/resource-sharing/) -- UI 工作流程與使用者指引