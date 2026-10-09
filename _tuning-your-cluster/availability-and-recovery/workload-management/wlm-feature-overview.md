---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工作負載管理"
nav_order: 90
has_children: true
parent: Availability and recovery
---

# 工作負載管理
於 2.18 版推出
{: .label .label-purple }

工作負載管理可讓您將搜尋流量分組並隔離網路資源，避免特定請求過度使用網路資源。它提供下列優點：

- 租用戶層級的准入控制與反應式查詢管理。當資源使用量超過設定的限制時，它會自動識別並取消高耗資源的查詢，確保資源公平分配。

- 叢集內搜尋工作負載的租用戶層級隔離，於節點層級運作。

## 安裝工作負載管理

使用工作負載管理需要安裝 Workload Management 外掛程式。若要安裝此外掛程式，請使用下列命令：

```bash
./bin/opensearch-plugin install workload-management
```
{% include copy.html %}

然後重新啟動您的叢集。如需更多資訊，請參閱[管理 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)。

## 工作負載群組

_工作負載群組_是具有已定義資源限制之工作的邏輯分組。系統管理員可以使用 Workload Management API 動態管理工作負載群組。這些工作負載群組可用來建立具有資源限制的搜尋請求。您也可以定義群組專屬設定，這些設定會自動套用至路由到該群組的每個請求。如需更多資訊，請參閱[工作負載群組]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/workload-management/workload-groups/)和[工作負載群組設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/workload-management/workload-group-settings/)。

下列範例請求會新增名為 `analytics` 的工作負載群組：

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

建立工作負載群組時，請確定單一資源 (例如 `cpu` 或 `memory`) 的資源限制總和不超過 `1`。
{: .important}

OpenSearch 會回應已設定的資源限制與工作負載群組 ID：

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

## 使用工作負載群組 ID

您可以將請求與工作負載群組 ID 建立關聯，以在工作負載群組定義的限制內管理及分配資源。使用此 ID 時，請求路由與追蹤會與工作負載群組建立關聯，確保維持資源配額與工作限制。

下列範例請求會使用前述回應中的工作負載群組 ID，以確保請求不超過 `analytics` 工作負載群組的資源限制。請將工作負載群組 ID 作為自訂請求標頭傳遞：

```json
curl -X GET "http://localhost:9200/testindex/_search?pretty" \
  -H "Content-Type: application/json" \
  -H "workloadGroupId: preXpc67RbKKeCyka72_Gw" \
  -d '{
    "query": {
      "range": {
        "total_amount": {
          "gte": 5,
          "lt": 15
        }
      }
    }
  }'
```
{% include copy.html %}

為了避免在每個查詢中傳遞 ID，您可以建立規則來自動套用 ID。如需更多資訊，請參閱[工作負載群組規則]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/workload-management/workload-group-rules/)。

## 運作模式

`wlm.workload_group.mode` 叢集層級設定可控制是否全域啟用工作負載管理。下列運作模式會決定工作負載管理的運作層級：

- `monitor_only` (預設)：工作負載管理會監視工作，但不會取消或拒絕任何查詢。

- `disabled`：工作負載管理已停用，不會進行監視或強制執行。

- `enabled`：工作負載管理已啟用，並會在達到設定的閾值時取消及拒絕查詢。

若要變更運作模式，請更新 [`wlm.workload_group.mode` 設定](#workload-management-settings)，如下一節所述。

此外，每個工作負載群組都會定義自己的 `resiliency_mode`。`resiliency_mode` 會定義強制執行行為，但只有在 `wlm.workload_group.mode` 為 `enabled` 時才會生效。如需 `resiliency_mode` 的更多資訊，請參閱[工作負載群組參數]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/workload-management/workload-groups/#parameters)。

## 工作負載管理設定

您可以使用 Cluster Settings API 更新工作負載管理的值來進行設定。如需更多資訊，請參閱[動態設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/#dynamic-settings)。

OpenSearch 支援下列工作負載管理設定：

- `wlm.workload_group.duress_streak` (動態，整數)：決定節點受壓閾值。一旦達到閾值，節點就會標記為受壓。預設值為 `3`。最小值為 `3`。

- `wlm.workload_group.enforcement_interval` (動態，long)：定義監視間隔，單位為毫秒。預設值為 `1000`。最小值為 `1000`。

 <p id="mode"> </p>

- `wlm.workload_group.mode` (動態，enum)：定義運作模式。有效值為 `enabled`、`disabled` 和 `monitor_only`。預設值為 `monitor_only`。如需更多資訊，請參閱[運作模式](#operating-modes)。

- `wlm.workload_group.node.memory_rejection_threshold` (動態，double)：定義工作負載群組層級的記憶體閾值。達到閾值時，請求會被拒絕。預設值為 `0.8`。最大值為 `0.9`。

- `wlm.workload_group.node.cpu_rejection_threshold` (動態，double)：定義工作負載群組層級的 CPU 閾值。達到閾值時，請求會被拒絕。預設值為 `0.8`。最大值為 `0.9`。

- `wlm.workload_group.node.memory_cancellation_threshold` (動態，double)：控制達到記憶體閾值時是否將節點視為受壓。路由到受壓節點的請求會被取消。預設值為 `0.9`。最大值為 `0.95`。

- `wlm.workload_group.node.cpu_cancellation_threshold` (動態，double)：控制達到 CPU 閾值時是否將節點視為受壓。路由到受壓節點的請求會被取消。預設值為 `0.9`。最大值為 `0.95`。

設定拒絕與取消閾值時，請記住資源的拒絕閾值一律必須低於取消閾值。
{: .important}

## Workload Management Stats API

Workload Management Stats API 提供 Workload Management 外掛程式目前狀態的相關資訊。

若要取得所有工作負載群組的統計資料，請使用下列請求：

```json
GET _wlm/stats
```
{% include copy-curl.html %}

回應會傳回每個工作負載群組的工作負載管理統計資料：

```json
{
  "_nodes": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "cluster_name": "XXXXXXYYYYYYYY",
  "A3L9EfBIQf2anrrUhh_goA": {
    "workload_groups": {
      "16YGxFlPRdqIO7K4EACJlw": {
        "total_completions": 33570,
        "total_rejections": 0,
        "total_cancellations": 0,
        "cpu": {
          "current_usage": 0.03319935314357281,
          "cancellations": 0,
          "rejections": 0
        },
        "memory": {
          "current_usage": 0.002306486276211217,
          "cancellations": 0,
          "rejections": 0
        }
      },
      "DEFAULT_WORKLOAD_GROUP": {
        "total_completions": 42572,
        "total_rejections": 0,
        "total_cancellations": 0,
        "cpu": {
          "current_usage": 0,
          "cancellations": 0,
          "rejections": 0
        },
        "memory": {
          "current_usage": 0,
          "cancellations": 0,
          "rejections": 0
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

若要依特定工作負載群組篩選，請將其 ID 作為路徑參數提供：

```json
GET _wlm/stats/wfbdJoDAS0mYiLbEAjd1sA
```
{% include copy-curl.html %}

### 回應本文欄位

回應包含下列欄位。

| 欄位名稱 | 說明                                                                                                                                      |
| :--- |:-------------------------------------------------------------------------------------------------------------------------------------------------| 
| `total_completions`  | 指定節點上 `workload_group` 中的請求完成總數。這包含所有分片層級與協調節點層級的請求。 |
| `total_rejections`    | 指定節點上 `workload_group` 中的請求拒絕總數。這包含所有分片層級與協調節點層級的請求。     |
| `total_cancellations` | 指定節點上 `workload_group` 中的取消總數。這包含所有分片層級與協調節點層級的請求。       |
| `cpu`   | `workload_group` 的 `cpu` 資源類型統計資料。                                                                                     | 
| `memory`  | `workload_group` 的 `memory` 資源類型統計資料。                                                                                  | 

### 資源類型統計資料

資源類型統計資料物件包含下列欄位。

| 欄位名稱  | 說明                                                                                                                                                                                 |
| :--- |:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
| `current_usage` | 根據監視執行緒上次執行結果，指定節點上 `workload_group` 的資源使用量。此值會根據 `wlm.workload_group.enforcement_interval` 更新。 |
| `cancellations` | 因達到取消閾值而導致的取消次數。                                                                                                        |
| `rejections`    | 因達到取消閾值而導致的拒絕次數。                                                                                                           |

## 權限

只有具備管理員層級權限的使用者，才能使用 Workload Management API 建立及更新工作負載群組。