---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "探索與叢集形成"
nav_order: 5
has_children: true
permalink: /tuning-your-cluster/discovery-cluster-formation/
---

# 探索與叢集形成

探索與叢集形成是 OpenSearch 中的基本程序，讓節點能夠彼此找到對方、選出叢集管理員、建立可運作的叢集，並在叢集狀態演變時維持協調。了解這些機制對於設定可靠且效能良好的 OpenSearch 叢集至關重要。

當您啟動 OpenSearch 叢集時，會有多個協調的程序共同運作：

- **節點探索**：節點在網路中找出並識別應屬於叢集的其他節點。
- **叢集管理員選舉**：符合資格的節點透過以共識為基礎的投票程序參與選出叢集管理員節點。
- **叢集形成**：選出叢集管理員後，叢集狀態隨之建立，節點加入叢集。
- **狀態管理**：叢集管理員維護權威的叢集狀態並分發給所有節點。
- **健康狀態監控**：節點持續監控彼此的健康狀態並偵測故障。

這些程序的所有節點間通訊都使用 OpenSearch 的[傳輸層]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/network-settings/)，確保安全且高效的資料交換。

## 探索程序

探索是節點在啟動時或與叢集管理員的連線中斷時尋找其他節點的方式。此程序包括：

1. **種子主機**：一份可設定的已知節點位址清單，作為探索的進入點。
2. **主機提供者**：提供種子主機資訊的機制，包括靜態組態與動態的雲端探索。
3. **節點識別**：驗證探索到的節點是否有資格參與叢集。

## 叢集管理員選舉

OpenSearch 使用精密的投票機制，確保任何時刻都只有一個叢集管理員：

- **投票組態**：參與選舉的叢集管理員候選節點集合。
- **法定人數要求**：選舉需要過半數的投票節點，以防止腦裂 (split-brain) 情境。
- **自動重新組態**：投票組態會隨著節點加入與離開叢集而調整。

## 叢集狀態管理

當選的叢集管理員負責：

- 維護具權威性的叢集狀態（例如節點成員資格、索引中繼資料與分片配置）。
- 將狀態更新發布至叢集中的所有節點。
- 協調分片配置與重新平衡。
- 管理叢集層級的設定與政策。

## 核心元件

下列主題針對探索與叢集形成的每個階段提供詳細指引：

[節點探索與種子主機]({{site.url}}{{site.baseurl}}/tuning-your-cluster/discovery-cluster-formation/discovery/)：了解 OpenSearch 節點如何透過種子主機提供者彼此探索，以及如何設定靜態或動態主機探索。

[投票與法定人數]({{site.url}}{{site.baseurl}}/tuning-your-cluster/discovery-cluster-formation/voting-quorums/)：了解 OpenSearch 如何使用以法定人數為基礎的投票來選出叢集管理員並防止腦裂狀況。

[投票組態管理]({{site.url}}{{site.baseurl}}/tuning-your-cluster/discovery-cluster-formation/voting-configuration/)：了解 OpenSearch 如何自動管理投票組態，以及處理新叢集的初始啟動需求。

[叢集初始啟動]({{site.url}}{{site.baseurl}}/tuning-your-cluster/discovery-cluster-formation/bootstrapping/)：設定叢集初始啟動，並了解安全啟動新叢集的需求。

[探索與叢集形成設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/discovery-cluster-formation/settings/)：控制探索與叢集形成行為之所有組態選項的完整參考，包括故障偵測與叢集狀態發布設定。

## 監控探索與叢集形成

您可以使用這些 API 命令來監控叢集形成與健康狀態。

### 檢查叢集健康狀態

```json
GET /_cluster/health
```
{% include copy-curl.html %}

回傳叢集的健康狀態，包括節點數量與分片資訊。

### 檢視叢集節點

```json
GET /_cat/nodes
```
{% include copy-curl.html %}

回傳叢集中節點的資訊，包括角色以及哪個節點是叢集管理員。

### 檢查投票組態

```json
GET /_cluster/state?filter_path=metadata.cluster_coordination.last_committed_config
```
{% include copy-curl.html %}

回傳目前的投票組態，顯示哪些節點參與叢集管理員選舉。

## 後續步驟

- 從[節點探索與種子主機]({{site.url}}{{site.baseurl}}/tuning-your-cluster/discovery-cluster-formation/discovery/)開始，了解叢集形成的基礎。
- 檢視[探索與叢集形成設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/discovery-cluster-formation/settings/)以了解組態選項。
- 請參閱[建立叢集]({{site.url}}{{site.baseurl}}/tuning-your-cluster/)以取得實際設定叢集的指引。