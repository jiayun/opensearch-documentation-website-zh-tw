---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "叢集引導"
parent: Discovery and cluster formation
nav_order: 40
---

# 叢集引導

在首次啟動 OpenSearch 叢集時，您必須明確定義將參與第一次叢集管理員選舉的初始叢集管理員候選節點集合。此程序稱為 _叢集引導_ (cluster bootstrapping)，對於防止叢集初始形成期間發生腦裂 (split-brain) 情境至關重要。

在下列情況中需要進行叢集引導：

- 首次啟動全新的叢集。
- 任何節點上都不存在現有的叢集狀態。
- 需要進行初始叢集管理員選舉。

在下列情況中不需要進行引導：

- 節點加入現有叢集：它們會從目前的叢集管理員取得組態。
- 叢集重新啟動：先前已加入叢集的節點會儲存必要的資訊。
- 叢集完整重新啟動：現有的叢集狀態會被保留並用於復原。

## 設定引導節點

使用 `cluster.initial_cluster_manager_nodes` 設定來定義哪些節點應參與初始叢集管理員選舉。在每個叢集管理員候選節點的 `opensearch.yml` 中設定此組態：

```yaml
cluster.initial_cluster_manager_nodes:
  - cluster-manager-1
  - cluster-manager-2
  - cluster-manager-3
```
{% include copy.html %}

或者，您可以在啟動 OpenSearch 時指定引導組態：

```bash
./bin/opensearch -Ecluster.initial_cluster_manager_nodes=cluster-manager-1,cluster-manager-2,cluster-manager-3
```
{% include copy.html %}

您可以使用下列任一方法來識別引導組態中的節點：

1. 使用 `node.name` 的值 (建議)：

   ```yaml
   cluster.initial_cluster_manager_nodes:
     - cluster-manager-1
     - cluster-manager-2
   ```
   {% include copy.html %}

2. 若未明確設定 `node.name`，則使用節點的主機名稱：

   ```yaml
   cluster.initial_cluster_manager_nodes:
     - server1.example.com
     - server2.example.com
   ```
   {% include copy.html %}

3. 使用節點的公用 IP 位址：

   ```yaml
   cluster.initial_cluster_manager_nodes:
     - 192.168.1.10
     - 192.168.1.11
   ```
   {% include copy.html %}

4. 當多個節點共用同一個 IP 時，使用節點的 IP 位址與連接埠：

   ```yaml
   cluster.initial_cluster_manager_nodes:
     - 192.168.1.10:9300
     - 192.168.1.10:9301
   ```
   {% include copy.html %}

## 關鍵引導需求

正確的引導可確保所有叢集管理員候選節點以一致且正確的組態啟動，防止叢集分裂並確保初始選舉程序穩定。

### 所有節點的組態必須完全相同

所有叢集管理員候選節點都必須具有相同的 `cluster.initial_cluster_manager_nodes` 設定。這可確保在引導期間只形成一個叢集。

**正確的組態**：

```yaml
# Node 1
cluster.initial_cluster_manager_nodes:
  - cluster-manager-1
  - cluster-manager-2
  - cluster-manager-3

# Node 2
cluster.initial_cluster_manager_nodes:
  - cluster-manager-1
  - cluster-manager-2
  - cluster-manager-3

# Node 3
cluster.initial_cluster_manager_nodes:
  - cluster-manager-1
  - cluster-manager-2
  - cluster-manager-3
```
{% include copy.html %}

**不正確的組態**：

```yaml
# Node 1 – different list
cluster.initial_cluster_manager_nodes:
  - cluster-manager-1
  - cluster-manager-2

# Node 2 – different list
cluster.initial_cluster_manager_nodes:
  - cluster-manager-2
  - cluster-manager-3
```

當節點的引導清單不一致時，可能會形成多個獨立的叢集。

### 名稱必須完全相符

引導組態中的節點名稱必須與每個節點的 `node.name` 值完全相符。

**常見的命名問題**：

* 如果節點的名稱是 `server1.example.com`，引導清單也必須使用 `server1.example.com`，而不是 `server1`。
* 節點名稱區分大小寫。
* 名稱必須完全相符，不得加入任何額外字元或空白。

如果節點的名稱與引導組態中的項目不完全相符，記錄檔將包含錯誤訊息。在此範例中，節點名稱 `cluster-manager-1.example.com` 與引導項目 `cluster-manager-1` 不相符：

```
[cluster-manager-1.example.com] cluster manager not discovered yet, this node has
not previously joined a bootstrapped cluster, and this node must discover
cluster-manager-eligible nodes [cluster-manager-1, cluster-manager-2] to
bootstrap a cluster: have discovered [{cluster-manager-2.example.com}...]
```

## 為叢集命名

請選擇一個描述性的叢集名稱，以便將您的叢集與其他叢集區別開來：

```yaml
cluster.name: production-search-cluster
```
{% include copy.html %}

為叢集命名時，請遵循下列準則：

- 每個叢集都必須有唯一的名稱，以避免衝突。

- 確保所有節點在加入前都會驗證叢集名稱是否相符。

- 在生產環境中避免使用預設的 `opensearch` 名稱。

- 選擇能反映叢集用途的描述性名稱。

## 開發模式自動引導

在下列條件下，OpenSearch 可以在開發環境中自動引導叢集：

- 未明確設定任何探索設定。
- 多個節點在同一台機器上執行。
- OpenSearch 偵測到它正在開發環境中執行。

### 停用自動引導的設定

如果設定了下列任一設定，您就必須明確設定 `cluster.initial_cluster_manager_nodes`：

- `discovery.seed_providers`
- `discovery.seed_hosts`
- `cluster.initial_cluster_manager_nodes`

### 自動引導的限制

自動引導僅適用於開發用途。請勿在生產環境中使用，原因如下：

- 節點可能無法及時互相探索，導致延遲。

- 網路狀況可能導致探索失敗。

- 行為可能無法預測，且不受保證。

- 有形成多個叢集的風險，導致腦裂情境。

## 疑難排解引導問題

如果您在沒有正確組態的情況下，意外在不同主機上啟動節點，它們可能會形成個別的叢集。您可以透過檢查叢集 UUID 來偵測這種情況：

```bash
curl -X GET "localhost:9200/"
```
{% include copy.html %}

如果每個節點回報的 `cluster_uuid` 不同，表示它們屬於不同的叢集。若要修正此問題並形成單一叢集，請依照下列步驟操作：

1. 停止所有節點。
2. 刪除每個節點資料目錄中的所有資料。
3. 設定正確的引導設定。
4. 重新啟動所有節點，並驗證是否形成單一叢集。

## 引導驗證

啟動叢集後，請使用[監視命令]({{site.url}}{{site.baseurl}}/tuning-your-cluster/discovery-cluster-formation/#monitoring-discovery-and-cluster-formation)來檢查叢集健康狀態與形成情況，以驗證引導是否成功：

- 驗證叢集健康狀態與節點數量。
- 確認已選出一個節點作為叢集管理員。
- 確保所有節點回報相同的叢集 UUID。

## 相關文件

- [投票組態管理]({{site.url}}{{site.baseurl}}/tuning-your-cluster/discovery-cluster-formation/voting-configuration/)：OpenSearch 如何在引導後管理投票
- [探索與叢集形成設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/discovery-cluster-formation/settings/)：完整的設定參考
- [建立叢集]({{site.url}}{{site.baseurl}}/tuning-your-cluster/)：逐步叢集設定指南