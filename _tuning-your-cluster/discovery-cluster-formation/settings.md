---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "探索與叢集形成設定"
parent: Discovery and cluster formation
nav_order: 100
---

# 探索與叢集形成設定

本頁提供所有控制 OpenSearch 中探索與叢集形成行為之設定的完整參考。這些設定決定節點如何找到彼此、選出叢集管理員，以及維持叢集協調。

## 核心探索設定

下列設定控制基本的探索程序：

- `discovery.seed_hosts`（靜態，清單）：提供叢集中符合叢集管理員資格之節點的位址清單。此設定對於節點在叢集形成期間能找到彼此至關重要。每個位址可指定為 `host:port` 或僅 `host`。`host` 可以是主機名稱（透過 DNS 解析——若解析出多個 IP，OpenSearch 會嘗試連線至全部）、IPv4 位址或 IPv6 位址（必須以方括號括住）。若未指定連接埠，OpenSearch 會依序檢查 `transport.profiles.default.port`、`transport.port` 來決定連接埠。若兩者皆未設定，則使用預設連接埠 `9300`。預設為 `["127.0.0.1", "[::1]"]`。

- `discovery.seed_providers`（靜態，清單）：指定探索期間使用哪些種子主機提供者來取得種子節點位址。可用的提供者為 `settings`（使用 `discovery.seed_hosts` 設定中的位址）與 `file`（從 `unicast_hosts.txt` 檔案讀取位址）。您可以指定多個提供者來合併探索方法。預設為 `["settings"]`。

- `discovery.type`（靜態，字串）：指定 OpenSearch 應形成多節點叢集或以單一節點運作。設為 `single-node` 時，OpenSearch 會形成單節點叢集並抑制特定逾時。此設定適用於開發與測試環境。有效值為 `multi-node`（預設）與 `single-node`。

- `cluster.initial_cluster_manager_nodes`（靜態，清單）：設定用於啟動全新叢集的初始符合叢集管理員資格節點。首次啟動叢集時需要此設定，且應包含初始符合叢集管理員資格節點的節點名稱（如 `node.name` 所定義）。對於加入現有叢集的節點，此清單應為空。預設為 `[]`（空）。

## 探索程序設定

這些設定控制探索程序期間的時序與行為：

- `discovery.find_peers_interval`（靜態，時間單位）：設定當初始嘗試失敗時，節點在嘗試下一輪探索前等待的時間長度。預設為 `1s`。

- `discovery.cluster_formation_warning_timeout`（靜態，時間單位）：設定節點在記錄警告訊息前嘗試形成叢集的時間長度。警告會以「cluster manager not discovered」開頭，並描述目前的探索狀態。預設為 `10s`。

### DNS 解析設定

下列設定控制種子主機的 DNS 查閱行為：

- `discovery.seed_resolver.max_concurrent_resolvers`（靜態，整數）：指定解析種子節點位址時要執行多少個並行 DNS 查閱。預設為 `10`。

- `discovery.seed_resolver.timeout`（靜態，時間單位）：指定解析種子節點位址時每次 DNS 查閱的逾時。預設為 `5s`。

### 連線設定

下列設定控制探索期間的連線嘗試：

- `discovery.probe.connect_timeout`（靜態，時間單位）：設定探索期間嘗試連線至每個位址時的逾時。預設為 `3s`。

- `discovery.probe.handshake_timeout`（靜態，時間單位）：設定探索期間嘗試透過握手識別遠端節點時的逾時。預設為 `1s`。

- `discovery.request_peers_timeout`（靜態，時間單位）：設定探索期間節點在將請求視為失敗前，等待對等節點資訊請求的時間長度。預設為 `3s`。

## 叢集管理員選舉設定

這些設定控制叢集管理員選舉程序：

- `cluster.election.back_off_time`（靜態，時間單位）：設定每次選舉失敗後新增的遞增延遲（線性退避）。每次選舉失敗都會在下一次嘗試前依此數量增加等待時間。預設為 `100ms`。**警告**：將此值從預設值變更可能會導致叢集管理員選舉無法進行。

- `cluster.election.duration`（靜態，時間單位）：設定每次選舉嘗試在視為失敗並排程重試前允許的最大持續時間。預設為 `500ms`。**警告**：將此值從預設值變更可能會導致叢集管理員選舉無法進行。

- `cluster.election.initial_timeout`（靜態，時間單位）：設定節點在嘗試第一次選舉前等待時間的初始上限，無論是在啟動時或目前叢集管理員失敗後。預設為 `100ms`。**警告**：將此值從預設值變更可能會導致叢集管理員選舉無法進行。

- `cluster.election.max_timeout`（靜態，時間單位）：設定選舉延遲的最大上限，以防止在長時間網路分割期間選舉過於稀疏。預設為 `10s`。**警告**：將此值從預設值變更可能會導致叢集管理員選舉無法進行。

## 投票組態設定

下列設定控制叢集管理員選舉的投票機制：

- `cluster.auto_shrink_voting_configuration`（動態，布林值）：控制投票組態是否自動移除已離開的節點，前提是至少保留三個節點。設為 `false` 時，您必須使用 Voting Configuration Exclusions API 手動移除已離開的節點。預設為 `true`。

- `cluster.max_voting_config_exclusions`（動態，整數）：設定同時允許的投票組態排除項目數量上限。這用於叢集管理員節點維護作業期間。預設為 `10`。

## 故障偵測設定

OpenSearch 透過兩種類型的健康狀態檢查持續監視叢集健康狀態：

- [追隨者檢查](#follower-checks)（由叢集管理員傳送給非叢集管理員節點）
- [領導者檢查](#leader-checks)（由非叢集管理員節點傳送給叢集管理員）

OpenSearch 允許偶發的檢查失敗，並使用下列準則來採取行動：

- 暫時性問題（單次檢查失敗）會被忽略；必須連續多次失敗才會採取行動。
- 網路中斷會觸發立即回應。
- 所有逾時與重試次數皆可設定。

### 追隨者檢查

選出的叢集管理員會定期檢查叢集中的每個節點：

1. 傳送定期健康狀態檢查請求至所有節點。
2. 在設定的逾時內等待回應。
3. 追蹤每個節點的連續檢查失敗次數。
4. 移除連續檢查失敗的節點（依據重試次數）。

若叢集管理員偵測到某節點已中斷連線（網路層級中斷），會略過逾時與重試設定，並立即嘗試將該節點從叢集移除。

### 領導者檢查

每個非叢集管理員節點會定期檢查選出的叢集管理員健康狀態：

1. 傳送定期健康狀態檢查請求至叢集管理員。
2. 在設定的逾時內等待回應。
3. 追蹤叢集管理員的連續檢查失敗次數。
4. 若連續檢查失敗，則開始新的叢集管理員選舉。

若節點偵測到叢集管理員已中斷連線，會略過逾時與重試設定，並立即重新啟動其探索階段，以尋找或選出新的叢集管理員。

下列設定控制健康狀態監視與故障偵測。

### 追隨者檢查設定

這些設定控制叢集管理員如何監視其他節點：

- `cluster.fault_detection.follower_check.interval`（靜態，時間單位）：設定叢集管理員對其他節點執行追隨者檢查的間隔。預設為 `1s`。**警告**：變更此設定可能導致叢集不穩定。

- `cluster.fault_detection.follower_check.timeout`（靜態，時間單位）：設定叢集管理員等待追隨者檢查回應的時間，超過此時間便視為檢查失敗。預設為 `10s`。**警告**：變更此設定可能導致叢集不穩定。

- `cluster.fault_detection.follower_check.retry_count`（靜態，整數）：設定追隨者檢查必須連續失敗多少次，叢集管理員才會將節點視為故障並從叢集移除。預設為 `3`。**警告**：變更此設定可能導致叢集不穩定。

### 領導者檢查設定

這些設定控制非叢集管理員節點如何監視叢集管理員：

- `cluster.fault_detection.leader_check.interval`（靜態，時間單位）：設定節點對叢集管理員執行領導者檢查的間隔。預設為 `1s`。**警告**：變更此設定可能導致叢集不穩定。

- `cluster.fault_detection.leader_check.timeout`（靜態，時間單位）：設定節點等待領導者檢查回應的時間，超過此時間便視為叢集管理員失效。預設為 `10s`。**警告**：變更此設定可能導致叢集不穩定。

- `cluster.fault_detection.leader_check.retry_count`（靜態，整數）：設定領導者檢查必須連續失敗多少次，節點才會將叢集管理員視為故障，並嘗試尋找或選出新的叢集管理員。預設為 `3`。**警告**：變更此設定可能導致叢集不穩定。

## 叢集狀態發布設定

下列設定控制叢集狀態更新的分送方式：

- `cluster.publish.timeout`（靜態，時間單位）：設定叢集管理員等待叢集狀態更新發布至所有節點的時間，超過此時間便逾時。當 `discovery.type` 設為 `single-node` 時，會忽略此設定。預設為 `30s`。

- `cluster.publish.info_timeout`（靜態，時間單位）：設定叢集管理員在叢集狀態發布期間，等待多久才記錄有關回應緩慢節點的訊息。預設為 `10s`。

- `cluster.follower_lag.timeout`（靜態，時間單位）：設定叢集管理員等待落後節點確認叢集狀態更新的時間。未在此時間內回應的節點會被視為失效，並從叢集移除。預設為 `90s`。

## 叢集協調設定

下列設定控制叢集加入與協調：

- `cluster.join.timeout`（靜態，時間單位）：設定節點傳送加入請求後的等待時間，超過此時間便視為請求失敗並重試。當 `discovery.type` 設為 `single-node` 時，會忽略此設定。預設為 `60s`。

- `cluster.no_cluster_manager_block`（動態，字串）：指定沒有作用中的叢集管理員時，會拒絕哪些操作。有效值為 `all`（拒絕所有操作，包括讀取／寫入與叢集狀態 API）和 `write`（僅拒絕寫入操作；讀取操作會根據最後已知的叢集狀態成功執行，但可能傳回過時的資料）。此設定不影響以節點為基礎的 API（Cluster Stats、Node Info、Node Stats）。若要使用完整的叢集功能，必須有作用中的叢集管理員。預設為 `write`。

## 組態範例

以下是探索的組態範例。

### 基本正式環境叢集

```yaml
# Cluster identification
cluster.name: production-cluster

# Discovery configuration
discovery.seed_hosts:
  - 10.0.1.10:9300
  - 10.0.1.11:9300
  - 10.0.1.12:9300

# Initial cluster manager nodes (only for bootstrapping)
cluster.initial_cluster_manager_nodes:
  - cluster-manager-1
  - cluster-manager-2
  - cluster-manager-3

# Voting configuration
cluster.auto_shrink_voting_configuration: true
cluster.max_voting_config_exclusions: 10
```
{% include copy.html %}

### 開發環境單一節點設定

```yaml
# Single-node development cluster
cluster.name: dev-cluster
discovery.type: single-node

# Optional: Disable cluster formation timeouts for faster startup
cluster.publish.timeout: 5s
cluster.join.timeout: 10s
```
{% include copy.html %}

### 高可用性正式環境叢集

```yaml
# Production cluster with dedicated cluster manager nodes
cluster.name: production-cluster

# Discovery configuration
discovery.seed_hosts:
  - cluster-manager-1.example.com:9300
  - cluster-manager-2.example.com:9300
  - cluster-manager-3.example.com:9300

# Bootstrap configuration (only for initial setup)
cluster.initial_cluster_manager_nodes:
  - cluster-manager-1
  - cluster-manager-2
  - cluster-manager-3

# Production-optimized settings
cluster.auto_shrink_voting_configuration: true
cluster.max_voting_config_exclusions: 3
cluster.publish.timeout: 60s
cluster.join.timeout: 120s
```
{% include copy.html %}

## 相關文件

- [節點探索與種子主機]({{site.url}}{{site.baseurl}}/tuning-your-cluster/discovery-cluster-formation/discovery/)：提供探索機制與種子主機提供者的資訊
- [建立叢集]({{site.url}}{{site.baseurl}}/tuning-your-cluster/)：逐步叢集設定指南
- [設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)：一般組態指引