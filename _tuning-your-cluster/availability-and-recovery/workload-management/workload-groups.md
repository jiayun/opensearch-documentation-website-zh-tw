---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工作負載群組"
nav_order: 20
parent: Workload management
grand_parent: Availability and recovery
redirect_from:
  - /tuning-your-cluster/availability-and-recovery/workload-management/workload-group-lifecycle-api/
  - /tuning-your-cluster/availability-and-recovery/workload-management/query-group-lifecycle-api/
---

# 工作負載群組

_工作負載群組_ 是具有已定義資源限制之任務的邏輯分組。您可以使用 Workload Group API 建立、更新、擷取及刪除工作負載群組。


## 建立工作負載群組

若要建立工作負載群組，請傳送下列請求：

```json
PUT _wlm/workload_group
{
  "name": "analytics",
  "resiliency_mode": "enforced",
  "resource_limits": {
    "cpu": 0.4,
    "memory": 0.2
  }
}
```
{% include copy-curl.html %}


OpenSearch 會傳回包含工作負載群組 ID 的回應，您可以使用該 ID 將查詢請求與群組建立關聯，並強制執行群組的資源限制：

```json
{
  "_id":"preXpc67RbKKeCyka72_Gw",
  "name":"analytics",
  "resiliency_mode":"enforced",
  "resource_limits":{
    "cpu":0.4,
    "memory":0.2
  },
  "updated_at":1726270184642
}
```

如需更多資訊，請參閱[使用工作負載群組 ID]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/workload-management/wlm-feature-overview/#using-the-workload-group-id)。

## 參數

建立或更新工作負載群組時，您可以指定下列參數。

| 參數 | 操作 | 說明	 |
| :--- | :--- | :--- |
| `name`  | 建立 | 工作負載群組的名稱。 |
| `resiliency_mode`  | 建立或更新 | 工作負載群組的韌性模式。有效值為：<br>- `enforced` (若超過閾值，查詢會被拒絕)。 <br>- `soft` (若有可用資源，查詢可以超過閾值)。 <br>- `monitor` (查詢會受到監控，但不會被取消或拒絕)。 <br> **注意**：只有在叢集層級的 `wlm.workload_group.mode` 設定為 `enabled` 時，這些設定才會生效。請參閱[操作模式]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/workload-management/wlm-feature-overview/#operating-modes)。 |
| `resource_limits` | 建立或更新 | 工作負載群組中查詢請求的資源限制。有效的資源為 `cpu` 和 `memory`。建立工作負載群組時，請確認單一資源 (`cpu` 或 `memory`) 的資源限制總和不超過 1。 |
| `settings` | 建立或更新 | 群組專屬設定，會自動套用至路由到工作負載群組的請求。如需支援的設定和更新行為，請參閱[工作負載群組設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/workload-management/workload-group-settings/)。 |

## 更新工作負載群組

若要更新工作負載群組，請提供工作負載群組名稱作為路徑參數，並將您要更新的[參數](#parameters)作為請求本文欄位。當您更新工作負載群組時，只有您指定的參數會變更；其他所有參數維持不變：

```json
PUT _wlm/workload_group/analytics
{
  "resiliency_mode": "monitor",
  "resource_limits": {
    "cpu": 0.41,
    "memory": 0.21
  },
  "settings": {
    "search.default_search_timeout": "1m"
  }
}
```
{% include copy-curl.html %}

如需 `settings` 欄位的更多資訊，包括支援的設定和更新行為，請參閱[工作負載群組設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/workload-management/workload-group-settings/)。

## 擷取工作負載群組

若要擷取所有工作負載群組，請使用下列請求：

```json
GET /_wlm/workload_group
```
{% include copy-curl.html %}

若要擷取特定工作負載群組，請提供其 ID 作為路徑參數： 

```json
GET /_wlm/workload_group/{name}
```
{% include copy-curl.html %}

 
## 刪除工作負載群組

若要刪除工作負載群組，請指定其名稱作為路徑參數：

```json
DELETE /_wlm/workload_group/{name}
```
{% include copy-curl.html %}

