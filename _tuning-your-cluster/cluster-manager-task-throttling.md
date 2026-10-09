---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "叢集管理員任務節流"
nav_order: 10
has_children: false
---

# 叢集管理員任務節流

對於許多叢集狀態更新，例如定義對應或建立索引，節點會將任務提交給叢集管理員。叢集管理員會為這些任務維護一個待處理任務佇列，並在單一執行緒環境中執行這些任務。當節點傳送數以萬計的資源密集型任務時，例如 `put-mapping` 或快照任務，這些任務可能會在佇列中堆積，並淹沒叢集管理員。這會影響叢集管理員的效能，並可能進而影響整個叢集的可用性。

第一道防線是在呼叫端節點中實作機制，以避免叢集管理員的任務超載。然而，即使這些機制已就緒，叢集管理員仍需要一種內建的方式來保護自己：叢集管理員任務節流。

根據預設，叢集管理員會使用預先定義的節流限制來判斷是否拒絕任務。您可以修改這些限制，或停用特定任務類型的節流。

叢集管理員會根據任務類型來拒絕任務。對於任何傳入的任務，叢集管理員會評估待處理任務佇列中相同類型的任務總數。如果此數量超過此任務類型的閾值，叢集管理員就會拒絕傳入的任務。拒絕任務不會影響不同類型的任務。例如，如果叢集管理員拒絕了 `put-mapping` 任務，它仍可接受後續的 `create-index` 任務。

當叢集管理員拒絕任務時，節點會以指數退避方式執行重試，將任務重新提交給叢集管理員。如果重試在逾時期間內未成功，OpenSearch 會傳回叢集逾時錯誤。

## 設定節流限制

您可以在 `cluster_manager.throttling.thresholds` 物件中指定節流限制，並更新 [OpenSearch 叢集設定]({{site.url}}{{site.baseurl}}/api-reference/cluster-settings/) 來設定這些限制。此設定為動態設定，因此您可以在不重新啟動叢集的情況下變更此功能的行為。

根據預設，所有任務類型都會啟用節流。若要停用特定任務類型的節流，請將其閾值設為 `-1`。
{: .note}

請求的格式如下：

```json
PUT _cluster/settings
{
  "persistent": {
    "cluster_manager.throttling.thresholds" : {
      "<task-type>" : {
          "value" : <threshold>
      }
    }
  }
}
```

`cluster_manager.throttling.thresholds` 物件包含下列欄位。

欄位名稱 | 說明
:--- | :---
`task-type` | 任務類型。如需有效的任務類型清單，請參閱[支援的任務類型與預設閾值](#supported-task-types-and-default-thresholds)。
`<task-type>.value` | 叢集管理員待處理任務佇列中 `task-type` 類型任務的最大數量。<br> 如需各任務類型的預設閾值，請參閱[支援的任務類型與預設閾值](#supported-task-types-and-default-thresholds)。

## 支援的任務類型與預設閾值

下表列出所有支援的任務類型及其預設節流閾值。

任務類型 | 閾值
:--- | :---
`create-index `| 50
`update-settings` | 50
`cluster-update-settings` | 50
`auto-create` | 200
`delete-index` | 50
`delete-dangling-index `| 50
`create-data-stream` | 50
`remove-data-stream` | 50
`rollover-index` | 200
`index-aliases` | 200
`put-mapping` | 10000
`create-index-template` | 50
`remove-index-template` | 50
`create-component-template` | 50
`remove-component-template` | 50
`create-index-template-v2` | 50
`remove-index-template-v2` | 50
`put-index-field-domains` | 50
`put-pipeline` | 50
`delete-pipeline` | 50
`put-search-pipeline` | 50
`delete-search-pipeline` | 50
`create-persistent-task` | 50
`finish-persistent-task` | 50
`remove-persistent-task` | 50
`update-task-state` | 50
`create-query-group` | 50
`delete-query-group` | 50
`update-query-group` | 50
`put-script` | 50
`delete-script` | 50
`put-repository` | 50
`delete-repository` | 50
`create-snapshot` | 50
`delete-snapshot` | 50
`update-snapshot-state` | 5000
`restore-snapshot` | 50
`cluster-reroute-api` | 50

## 範例請求

下列請求會將 `put-mapping` 任務類型的節流閾值設為 100：

```json
PUT _cluster/settings
{
  "persistent": {
    "cluster_manager.throttling.thresholds": {
      "put-mapping": {
        "value": 100
      }
    }
  }
}
```
{% include copy-curl.html %}
