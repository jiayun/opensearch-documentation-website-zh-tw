---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "投票組態管理"
parent: Discovery and cluster formation
nav_order: 30
---

# 投票組態管理

每個 OpenSearch 叢集都會維護一個投票組態，定義具備叢集管理員資格的節點集合，在做出關鍵叢集決策時，這些節點的回應才會被計入。了解 OpenSearch 如何管理投票組態，對於維持叢集的穩定性與可用性至關重要。

_投票組態_ 是具備叢集管理員資格節點的權威清單，這些節點參與：

- **叢集管理員選舉**：選擇由哪個節點領導叢集。
- **叢集狀態更新**：核准叢集中繼資料與分片配置的變更。
- **關鍵叢集決策**：任何需要叢集全域共識的操作。

只有在投票組態中過半數（超過一半）的節點回應同意後，才會做出決策。

## 投票組態與叢集成員資格的比較

投票組態通常與叢集中所有具備叢集管理員資格的節點一致，但有時兩者會不同。在穩定叢集的正常運作期間，所有健康的具備叢集管理員資格節點都會參與投票。然而，在節點轉換期間（例如節點加入或離開時）、部分具資格節點無法連線的故障情境，或管理員為了維護而手動排除節點時，兩者可能出現差異。

## 自動投票組態管理

隨著叢集變化，OpenSearch 會自動調整投票組態以維持韌性。當新的具備叢集管理員資格節點加入時，叢集管理員會評估狀態、將新節點加入投票組態，並將更新後的狀態發布到所有節點。較大的組態能提供更好的容錯能力，因此 OpenSearch 偏好納入所有可用的具資格節點。

節點移除行為取決於 `cluster.auto_shrink_voting_configuration` 設定，該設定預設為啟用。啟用時，OpenSearch 會自動移除已離開的節點，同時確保至少保留三個投票節點。這可提升可用性，讓叢集在節點故障後仍能繼續運作。停用時（false），您必須使用 Voting Exclusions API 手動移除已離開的節點，讓管理員能精確控制組態變更的時機與方式。

在可能的情況下，OpenSearch 會以其他具資格節點取代已離開的投票節點，而不是縮減組態規模。這種取代策略可維持相同的投票節點數量，在不中斷服務的情況下保留容錯能力。

## 檢視目前的投票組態

使用 Cluster State API 檢查目前的投票組態：

```bash
curl -X GET "localhost:9200/_cluster/state?filter_path=metadata.cluster_coordination.last_committed_config"
```
{% include copy.html %}

回應範例：

```json
{
  "metadata": {
    "cluster_coordination": {
      "last_committed_config": [
        "KfEEGG7_SsKZVFqI4ko2FA"
      ]
    }
  }
}
```

`last_committed_config` 陣列包含目前投票組態中所有節點的節點 ID。

## 具備叢集管理員資格節點數量為偶數的情況

OpenSearch 會智慧地處理具備叢集管理員資格節點數量為偶數的情況，以防止腦裂（split-brain）情境。腦裂情境是指分散式系統中，網路故障將叢集分割成兩個或多個彼此無法通訊的隔離節點群組。當投票節點數量為偶數時，網路分割可能將叢集分成兩個等半，導致任何一方都無法取得選出叢集管理員所需的過半數。例如，在四節點叢集中，決策需要三票。如果網路分割成二對二，任何一方都無法達到三票，叢集就會變得無法使用。

為了防止這種情況，OpenSearch 會自動從投票組態中排除一個節點，使投票節點數量變成奇數（例如四個具資格節點中取三個）。這項調整確保其中一個分割區可以維持過半數並繼續運作，而另一個則無法。因此，OpenSearch 在不降低整體容錯能力的情況下，提升了對腦裂狀況的韌性。

## 新叢集的引導組態

首次啟動全新叢集時，OpenSearch 需要初始引導組態，以決定哪些節點應參與第一次叢集管理員選舉。此引導程序會建立叢集將使用的初始投票組態。

引導組態僅在新叢集時需要，一旦叢集成功啟動後即被忽略。在初始引導之後，OpenSearch 會依照前述章節的說明自動管理投票組態。

有關設定叢集引導的完整資訊，包括設定程序、需求、疑難排解與範例，請參閱 [叢集引導]({{site.url}}{{site.baseurl}}/tuning-your-cluster/discovery-cluster-formation/bootstrapping/)。

## 監控投票組態變更

若要追蹤投票組態變更並檢查叢集形成狀態，請使用 [探索與叢集形成]({{site.url}}{{site.baseurl}}/tuning-your-cluster/discovery-cluster-formation/#monitoring-discovery-and-cluster-formation) 中詳述的監控命令。

## 相關文件

- [投票與法定人數]({{site.url}}{{site.baseurl}}/tuning-your-cluster/discovery-cluster-formation/voting-quorums/)：了解以法定人數為基礎的決策機制
- [探索與叢集形成設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/discovery-cluster-formation/settings/)：設定投票行為
- [叢集引導]({{site.url}}{{site.baseurl}}/tuning-your-cluster/discovery-cluster-formation/bootstrapping/)：叢集初始啟動程序