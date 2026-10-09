---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立叢集"
nav_order: 1
nav_exclude: true
permalink: /tuning-your-cluster/
redirect_from: 
  - /opensearch/cluster/
  - /tuning-your-cluster/cluster/
  - /tuning-your-cluster/index/
---

# 建立叢集

在深入使用 OpenSearch 並搜尋與彙總資料之前，您必須先建立 OpenSearch 叢集。

OpenSearch 可以單一節點或多節點叢集的形式運作。一般而言，設定兩者的步驟相當類似。本頁示範如何建立及設定多節點叢集，但只要稍作調整，您就能依照相同步驟建立單一節點叢集。

若要依照您的需求建立及部署 OpenSearch 叢集，重要的是了解節點探索與叢集形成如何運作，以及有哪些設定控制它們。

設計叢集的方式有很多種。下圖顯示一個基本架構，其中包含一個七節點叢集，內有三個專用叢集管理員節點（兩個符合叢集管理員資格的節點與一個經選出的領導者）、三個資料節點，以及一個專用協調節點。

![多節點叢集架構圖]({{site.url}}{{site.baseurl}}/images/cluster.png)

先前的「master node」現在稱為叢集管理員節點。
   {: .note }

### 節點

下表簡要說明各種節點類型。

節點類型 | 說明 | 生產環境的最佳做法
:--- | :--- | :-- |
叢集管理員節點 | 管理叢集的整體運作並追蹤叢集狀態。這包括建立及刪除索引、追蹤加入與離開叢集的節點、檢查叢集中每個節點的健康狀態（透過執行 ping 請求），以及將分片配置給節點。 | 在三個不同區域中各部署一個專用叢集管理員節點，幾乎是所有生產環境使用案例的正確做法。此組態可確保您的叢集永遠不會失去仲裁。除了某個節點故障或需要進行維護時，其中兩個節點大部分時間都會閒置。
符合叢集管理員資格的節點 | 透過投票程序從中選出一個節點做為叢集管理員節點。 | 對於生產環境叢集，請確保您有專用叢集管理員節點。達成專用節點類型的方式，是將所有其他節點類型標記為 false。在此情況下，您必須將所有其他節點標記為不符合叢集管理員資格。
資料節點 | 儲存及搜尋資料。在本機分片上執行所有與資料相關的操作（編製索引、搜尋、彙總）。這些是叢集中的工作節點，需要比其他任何節點類型更多的磁碟空間。 | 當您新增資料節點時，請讓它們在各區域之間保持平衡。例如，如果您有三個區域，請以三的倍數新增資料節點，每個區域一個。我們建議使用儲存空間與 RAM 較大的節點。
匯入節點 | 在將資料儲存至叢集之前先行處理。執行資料匯入管線，在將資料新增至索引之前轉換資料。 | 如果您打算匯入大量資料並執行複雜的資料匯入管線，我們建議您使用專用匯入節點。您也可以選擇將編製索引的工作從資料節點卸載，讓資料節點專用於搜尋與彙總。
協調節點 | 將用戶端請求轉送至資料節點上的分片，收集並彙總結果成為單一最終結果，再將此結果傳回用戶端。 | 部署幾個專用協調節點，適合用來避免搜尋密集型工作負載發生瓶頸。我們建議使用核心數越多越好的 CPU。
動態節點 | 將特定節點指派給自訂工作，例如機器學習 (ML) 任務，避免耗用資料節點的資源，因此不會影響任何 OpenSearch 功能。 
暖節點 | 提供對[可搜尋快照]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/searchable_snapshot/)的存取。採用諸如快取常用分段及移除最少使用資料分段等技術，以存取可搜尋快照索引（儲存於遠端長期儲存來源，例如 Amazon Simple Storage Service [Amazon S3] 或 Google Cloud Storage）。 | 暖節點包含一個配置為快照快取的索引。因此，我們建議使用運算能力（CPU 與記憶體）高於儲存容量（硬碟）的專用節點。
搜尋節點 | 搜尋節點是專用節點，僅裝載搜尋副本分片，有助於將搜尋工作負載與編製索引工作負載分開。 | 由於搜尋節點裝載搜尋副本並處理搜尋流量，我們建議將它們用於專用的記憶體最佳化執行個體。 

依預設，每個節點都是符合叢集管理員資格、資料、匯入及協調節點。決定節點數量、指派節點類型，以及為每個節點類型選擇硬體，取決於您的使用案例。您必須考量各種因素，例如您想保留資料的時間長度、文件的平均大小、您典型的工作負載（編製索引、搜尋、彙總）、您預期的價格效能比、您的風險承受度等等。

在評估所有這些需求之後，我們建議您使用像是 [OpenSearch Benchmark](https://github.com/opensearch-project/opensearch-benchmark) 的基準測試工具，佈建一個小型範例叢集，並以不同的工作負載與組態執行測試。比較並分析這些測試的系統與查詢指標，以設計最佳架構。

本頁示範如何使用不同的節點類型。文中假設您有一個類似上圖的四節點叢集。

最佳做法是將來自外部來源的流量（例如 [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/dashboards/)、[OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) 及其他來源）依下列可用性順序導向節點：匯入節點、協調節點、資料節點。我們不建議將流量直接傳送至叢集管理員節點。
{: .note}

## 先決條件

開始之前，您必須在所有節點上安裝及設定 OpenSearch。如需可用選項的相關資訊，請參閱[安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/)。

完成後，請使用 SSH 連線至每個節點，然後開啟 `config/opensearch.yml` 檔案。您可以在此檔案中設定叢集的所有組態。

## 步驟 1：為叢集命名

為叢集指定唯一的名稱。如果您未指定叢集名稱，預設會設為 `opensearch`。設定具描述性的叢集名稱很重要，尤其是如果您想在單一網路內執行多個叢集。

若要指定叢集名稱，請將下列這一行：

```yml
#cluster.name: my-application
```

變更為

```yml
cluster.name: opensearch-cluster
```

請在所有節點上進行相同的變更，以確保它們會加入並形成叢集。

## 步驟 2：為叢集中的每個節點設定節點屬性

為叢集命名之後，請為叢集中的每個節點設定節點屬性。

#### 叢集管理員節點

為您的叢集管理員節點命名。如果您未指定名稱，OpenSearch 會指派機器產生的名稱，使該節點難以監控與疑難排解。

```yml
node.name: opensearch-cluster_manager
```

您也可以明確指定此節點為叢集管理員節點，即使它預設已設為 true。將節點角色設為 `cluster_manager`，以便更容易識別叢集管理員節點。

```yml
node.roles: [ cluster_manager ]
```

#### 資料節點

將兩個節點的名稱分別更改為 `opensearch-d1` 和 `opensearch-d2`：

```yml
node.name: opensearch-d1
```

```yml
node.name: opensearch-d2
```

您可以將它們設定為具備叢集管理員資格的資料節點，同時也用於匯入資料：

```yml
node.roles: [ data, ingest ]
```

您也可以為資料節點指定任何其他想要設定的屬性。

#### 協調節點

將協調節點的名稱更改為 `opensearch-c1`：

```yml
node.name: opensearch-c1
```

每個節點預設都是協調節點，因此若要讓此節點成為專用的協調節點，請將 `node.roles` 設定為空清單：

```yml
node.roles: []
```

## 步驟 3：將叢集繫結至特定 IP 位址

`network.bind_host` 定義用於繫結節點的 IP 位址。預設情況下，OpenSearch 會監聽本機主機，這會將叢集限制為單一節點。您也可以使用 `_local_` 和 `_site_` 繫結至任何回送或站內本機位址，無論是 IPv4 還是 IPv6：

```yml
network.bind_host: [_local_, _site_]
```

若要組成多節點叢集，請指定節點的 IP 位址：

```yml
network.bind_host: <IP address of the node>
```

請務必在所有節點上設定這些設定。

## 步驟 4：為叢集設定探索主機與初始叢集管理員節點

設定好網路主機之後，您需要設定探索主機，並為初始叢集選舉指定叢集管理員節點。請注意，這裡使用的是節點名稱，而非 IP 位址、主機名稱或完整網域名稱。

例如，該設定如下所示：

```yml
cluster.initial_cluster_manager_nodes: ["opensearch-cluster_manager"]
```

Zen Discovery 是內建的預設機制，使用[單點傳播](https://en.wikipedia.org/wiki/Unicast)來尋找叢集中的其他節點。

一般而言，您可以將所有具備叢集管理員資格的節點加入 `discovery.seed_hosts` 陣列。當節點啟動時，它會找出其他具備叢集管理員資格的節點，判斷哪一個是叢集管理員，並請求加入叢集。

例如，對於 `opensearch-cluster_manager`，該行看起來像這樣：

```yml
discovery.seed_hosts: ["<private IP of opensearch-d1>", "<private IP of opensearch-d2>", "<private IP of opensearch-c1>"]
```

## 步驟 5：啟動叢集

設定組態之後，請在所有節點上啟動 OpenSearch：

```bash
sudo systemctl start opensearch.service
```

從 tar 封存檔安裝 OpenSearch 不會自動使用 `systemd` 建立服務。如果您收到類似 `Failed to start opensearch.service: Unit not found.` 的錯誤，請參閱[使用 `systemd` 將 OpenSearch 作為服務執行]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/tar/#run-opensearch-as-a-service-using-systemd)，以取得建立並啟動服務的說明
{: .tip}

然後前往記錄檔查看叢集的形成過程：

```bash
less /var/log/opensearch/opensearch-cluster.log
```

在任何節點上執行下列 `_cat` 查詢，即可看到組成叢集的所有節點：

```bash
curl -XGET https://<private-ip>:9200/_cat/nodes?v -u 'admin:<custom-admin-password>' --insecure
```

```
ip             heap.percent ram.percent cpu load_1m load_5m load_15m node.role cluster_manager name
x.x.x.x           13          61   0    0.02    0.04     0.05 mi        *      opensearch-cluster_manager
x.x.x.x           16          60   0    0.06    0.05     0.05 md        -      opensearch-d1
x.x.x.x           34          38   0    0.12    0.07     0.06 md        -      opensearch-d2
x.x.x.x           23          38   0    0.12    0.07     0.06 md        -      opensearch-c1
```

若要更深入了解並監控您的叢集，請使用 [CAT API]({{site.url}}{{site.baseurl}}/opensearch/catapis/)。

## (進階) 步驟 6：設定分片分配感知或強制感知

若要進一步微調分片分配，您可以為分片分配感知或強制感知設定自訂節點屬性。

### 分片分配感知

您可以在 OpenSearch 節點上設定自訂節點屬性，用於分片分配感知。例如，您可以在每個節點上設定 `zone` 屬性，以代表節點所在的區域。您也可以使用 `zone` 屬性，確保主要分片及其副本分片在可用且不同的區域之間均衡分配。在此情境下，每個區域的最大分片複本數會等於 `ceil (number_of_shard_copies/number_of_distinct_zones)`。

OpenSearch 預設會將單一分片的分片複本分配到不同的節點。當只有 1 個區域可用時（例如某個區域故障後），OpenSearch 會將副本分片分配到唯一剩餘的區域——在計算每個區域允許的最大分片複本數時，只會考慮可用的區域（屬性值）。

例如，如果您的索引總共有 5 個分片複本（1 個主要分片和 4 個副本），且節點分布在 3 個不同的區域，則 OpenSearch 會執行以下操作來分配所有 5 個分片複本：

- 每個區域分配不超過 2 個分片，這需要在 2 個區域中至少各有 2 個節點。
- 將最後一個分片分配到第三個區域，第三個區域至少需要 1 個節點。

或者，如果您在第一個區域有 3 個節點，其餘每個區域各有 1 個節點，則 OpenSearch 會分配：

- 第一個區域 2 個分片複本。
- 其餘 2 個區域各 1 個分片複本。

最後一個分片複本會因節點不足而保持未分配狀態。

透過分片分配感知，如果其中一個區域的節點故障，您可以確保副本分片分散在其他區域，增加一層容錯能力，確保您的資料在區域故障時仍能保存。

若要設定分片分配感知，請分別在 `opensearch-d1` 和 `opensearch-d2` 中加入區域屬性：

```yml
node.attr.zone: zoneA
```

```yml
node.attr.zone: zoneB
```

更新叢集設定：

```json
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.awareness.attributes": "zone"
  }
}
```

您也可以將多個屬性以逗號分隔的字串形式提供，用於分片分配感知，例如 `zone,rack`。

您可以使用 `persistent` 或 `transient` 設定。我們建議使用 `persistent` 設定，因為它在叢集重新啟動後仍會保留。暫時性設定在叢集重新啟動後不會保留。

分片分配感知會嘗試將主要分片和副本分片分散到多個區域。然而，如果只有一個區域可用（例如某個區域故障後），OpenSearch 會將副本分片分配到唯一剩餘的區域。

### 強制感知

另一種選項是要求主要分片和副本分片絕不分配到同一個區域。這稱為強制感知。

若要設定強制感知，請指定區域屬性的所有可能值：

```json
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.awareness.attributes": "zone",
    "cluster.routing.allocation.awareness.force.zone.values":["zoneA", "zoneB"]
  }
}
```

現在，如果某個資料節點故障，強制感知不會將副本分配到同一區域的節點。相反地，叢集會進入黃色狀態，只有在另一個區域的節點上線時才會分配副本。

在我們的雙區域架構中，如果 `opensearch-d1` 和 `opensearch-d2` 的使用率低於 50%，我們可以使用分配感知，讓兩者都有足夠的儲存空間容量在同一區域內分配副本。
如果情況並非如此，且 `opensearch-d1` 和 `opensearch-d2` 沒有足夠容量容納所有主要分片和副本分片，我們可以使用強制感知。這種做法有助於確保在發生故障時，OpenSearch 不會讓最後剩餘的區域超載，也不會因儲存空間不足而鎖死您的叢集。

選擇分配感知或強制感知，取決於每個區域需要多少空間來平衡主要分片和副本分片。

### 強制副本數量限制

若要強制將分片平均分配到所有區域並避免熱點，您可以將 `routing.allocation.awareness.balance` 屬性設為 `true`。您可以在 opensearch.yml 檔案中設定此設定，並使用叢集更新設定 API 動態更新：

```json
PUT _cluster/settings
{
  "persistent": {
    "cluster": {
      "routing.allocation.awareness.balance": "true"
    }
  }
}
```

`routing.allocation.awareness.balance` 設定預設為 false。當此設定設為 `true` 時，索引的分片總數必須是所有感知屬性中最大數量的倍數。例如，假設組態有兩個感知屬性&mdash;區域和機架 ID。假設有兩個區域和三個機架 ID。區域數量與機架 ID 數量中，較大的數量是三。因此，分片數量必須是三的倍數。否則，OpenSearch 會擲回驗證例外。

只有在設定了 `cluster.routing.allocation.awareness.attributes` 和 `cluster.routing.allocation.awareness.force.zone.values` 時，`routing.allocation.awareness.balance` 才會生效。
{: .note}

`routing.allocation.awareness.balance` 適用於所有建立或更新索引的操作。例如，假設您在具備區域感知的設定下，執行具有三個節點和三個區域的叢集。如果您嘗試建立具有一個副本的索引，或將索引設定更新為一個副本，該操作會因驗證例外而失敗，因為分片數量必須是三的倍數。同樣地，如果您嘗試建立具有一個分片且沒有副本的索引範本，該操作也會因相同原因而失敗。不過，在所有這些操作中，如果您將分片數量設為一，並將副本數量設為二，分片總數就會是三，操作便會成功。 

## （進階）步驟 7：設定熱暖架構

您可以設計熱暖架構，先將資料編製索引至速度快且昂貴的熱節點---經過一段時間後，再將資料移至速度慢且便宜的暖節點。

如果您分析的是很少更新的時間序列資料，並希望將較舊的資料放到較便宜的儲存空間，這種架構可能很適合。

這種架構有助於節省儲存成本。您可以為較少存取的資料新增暖節點，無須增加熱節點數量並使用快速且昂貴的儲存空間。

若要設定熱暖儲存架構，請分別將 `temp` 屬性新增至 `opensearch-d1` 和 `opensearch-d2`：

```yml
node.attr.temp: hot
```

```yml
node.attr.temp: warm
```

您可以自行設定屬性名稱和值，只要熱節點與暖節點使用相同的屬性名稱，並分別一致地使用各自的屬性值即可。

若要將索引 `newindex` 新增至熱節點：

```json
PUT newindex
{
  "settings": {
    "index.routing.allocation.require.temp": "hot"
  }
}
```

請查看 `newindex` 的下列分片配置：

```json
GET _cat/shards/newindex?v
index     shard prirep state      docs store ip         node
new_index 2     p      STARTED       0  230b 10.0.0.225 opensearch-d1
new_index 2     r      UNASSIGNED
new_index 3     p      STARTED       0  230b 10.0.0.225 opensearch-d1
new_index 3     r      UNASSIGNED
new_index 4     p      STARTED       0  230b 10.0.0.225 opensearch-d1
new_index 4     r      UNASSIGNED
new_index 1     p      STARTED       0  230b 10.0.0.225 opensearch-d1
new_index 1     r      UNASSIGNED
new_index 0     p      STARTED       0  230b 10.0.0.225 opensearch-d1
new_index 0     r      UNASSIGNED
```

在此範例中，所有主要分片都配置到 `opensearch-d1`，也就是我們的熱節點。所有副本分片都未指派，因為我們強制此索引只能配置到熱節點。

若要將索引 `oldindex` 新增至暖節點：

```json
PUT oldindex
{
  "settings": {
    "index.routing.allocation.require.temp": "warm"
  }
}
```

`oldindex` 的分片配置：

```json
GET _cat/shards/oldindex?v
index     shard prirep state      docs store ip        node
old_index 2     p      STARTED       0  230b 10.0.0.74 opensearch-d2
old_index 2     r      UNASSIGNED
old_index 3     p      STARTED       0  230b 10.0.0.74 opensearch-d2
old_index 3     r      UNASSIGNED
old_index 4     p      STARTED       0  230b 10.0.0.74 opensearch-d2
old_index 4     r      UNASSIGNED
old_index 1     p      STARTED       0  230b 10.0.0.74 opensearch-d2
old_index 1     r      UNASSIGNED
old_index 0     p      STARTED       0  230b 10.0.0.74 opensearch-d2
old_index 0     r      UNASSIGNED
```

在此情況下，所有主要分片都配置到 `opensearch-d2`。同樣地，所有副本分片都未指派，因為我們只有一個暖節點。

常見的做法是設定您的[索引範本]({{site.url}}{{site.baseurl}}/opensearch/index-templates/)，將 `index.routing.allocation.require.temp` 值設為 `hot`。如此一來，OpenSearch 會將您最新的資料儲存在熱節點上。

接著，您可以使用 [Index State Management（ISM）]({{site.url}}{{site.baseurl}}/im-plugin/) 外掛程式，定期檢查索引的存續時間，並指定要對索引執行的動作。例如，當索引達到指定的存續時間時，將 `index.routing.allocation.require.temp` 設定變更為 `warm`，以自動將您的資料從熱節點移至暖節點。

## 後續步驟

如果您使用 Security 外掛程式，先前傳送至 `_cat/nodes?v` 的請求可能已因初始化錯誤而失敗。如需使用 Security 外掛程式的完整指引，請參閱[安全性組態]({{site.url}}{{site.baseurl}}/security/configuration/index/)。

如需本指南中提及的所有 OpenSearch 設定的完整文件，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)。
{: .note}
