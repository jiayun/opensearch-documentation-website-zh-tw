---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "節點探索與種子主機"
parent: Discovery and cluster formation
nav_order: 10
---

# 節點探索與種子主機

節點探索是 OpenSearch 節點找到並連線至其他節點，以組成或加入叢集的過程。當您第一次啟動節點，或節點失去與叢集管理員的連線而需要重新加入叢集時，此過程至關重要。

探索過程分為兩個不同的階段：

1. **初始種子探索**：每個啟動中的節點會連線至預先定義的種子位址清單，並嘗試辨識這些位址上的節點是否具備叢集管理員資格。

2. **對等探索**：一旦連線至種子節點，該節點便會交換已知且具備叢集管理員資格的對等節點清單。這會形成串聯式的探索過程，每個新探索到的節點都會提供額外的對等節點資訊。

探索過程會持續進行，直到符合下列其中一個條件為止：

- **對於不具備叢集管理員資格的節點**：探索會持續進行，直到找到已選出的叢集管理員為止。
- **對於具備叢集管理員資格的節點**：探索會持續進行，直到找到已選出的叢集管理員，或探索到足夠且具備叢集管理員資格的節點以完成叢集管理員選舉為止。

若在設定的時間內未符合任一條件，節點會在 `discovery.find_peers_interval` 指定的間隔後重試探索過程（預設為 `1s`）。

## 種子主機提供者

OpenSearch 使用 _種子主機提供者_ 來提供節點探索的初始位址清單。這些提供者定義節點如何取得啟動探索過程所需的種子位址。

您可以使用 `discovery.seed_providers` 設定來設定種子主機提供者，該設定接受提供者類型清單。這可讓您為叢集合併多種探索方法。預設提供者為 `settings`，其使用靜態組態。

### 以設定為基礎的種子主機提供者

以設定為基礎的提供者使用靜態組態來定義種子節點位址清單。對於節點位址已知的內部部署而言，這是最常見的做法。

在 `opensearch.yml` 中使用 `discovery.seed_hosts` 設定來設定種子主機：

```yaml
discovery.seed_hosts:
  - 192.168.1.10:9300
  - 192.168.1.11          # Port defaults to transport.port
  - seeds.example.com     # DNS hostnames are resolved
```
{% include copy.html %}

每個種子主機位址可透過下列方式指定。

| 格式                  | 範例                  | 備註                                    |
| ----------------------- | ------------------------ | ---------------------------------------- |
| 含連接埠的 IP 位址    | `192.168.1.10:9300`      | 指定自訂傳輸連接埠        |
| 不含連接埠的 IP 位址 | `192.168.1.11`           | 使用預設傳輸連接埠          |
| 含連接埠的主機名稱      | `node1.example.com:9300` | 指定自訂傳輸連接埠        |
| 不含連接埠的主機名稱   | `node1.example.com`      | 使用預設傳輸連接埠          |
| IPv6 位址            | `[2001:db8::1]:9300`     | IPv6 位址必須加上方括號 |

未指定連接埠時，OpenSearch 會依序使用下列設定中的第一個連接埠：

1. `transport.profiles.default.port`
2. `transport.port`

若兩者皆未設定，則使用預設連接埠 `9300`。

當您指定主機名稱作為種子位址時，OpenSearch 會執行下列 DNS 解析步驟：

- OpenSearch 執行 DNS 查詢，將主機名稱解析為 IP 位址。
- 若主機名稱解析為多個 IP 位址，OpenSearch 會嘗試連線至所有解析出的位址。
- DNS 查詢受 JVM DNS 快取設定所規範。
- 解析會在每一輪探索時進行，允許動態變更 IP。

DNS 解析行為由下列設定控制：

- `discovery.seed_resolver.max_concurrent_resolvers`：並行 DNS 查詢數上限（預設為 `10`）
- `discovery.seed_resolver.timeout`：每次 DNS 查詢的逾時時間（預設為 `5s`）

### 以檔案為基礎的種子主機提供者

以檔案為基礎的提供者會從外部檔案讀取種子主機位址，允許在不重新啟動節點的情況下動態更新。這在啟動時可能還不知道 IP 位址的容器化環境中特別有用。

在 `opensearch.yml` 中啟用以檔案為基礎的提供者：

```yaml
discovery.seed_providers: file
```
{% include copy.html %}

您也可以將其與以設定為基礎的提供者合併使用：

```yaml
discovery.seed_providers: [settings, file]
```
{% include copy.html %}

在您的 OpenSearch 組態目錄（`$OPENSEARCH_PATH_CONF/unicast_hosts.txt`）中建立名為 `unicast_hosts.txt` 的檔案。該檔案應遵循下列格式：

```
# Static IP addresses
10.0.1.10
10.0.1.11:9305

# Hostnames
node1.example.com
node2.example.com:9301

# IPv6 addresses (brackets required)
[2001:db8::1]:9300
[2001:db8::2]

# Comments start with # and must be on separate lines
# This is a comment
```
{% include copy.html %}

檔案中的每一行都必須遵循下列規則：

- 每一行包含單一主機位址。
- 指定 `host:port` 或僅指定 `host`（使用預設連接埠）。
- 以 `#` 開頭的行會被視為註解。
- IPv6 位址必須以方括號括住，並可在方括號後選擇性指定連接埠。
- 空行會被忽略。

OpenSearch 會自動偵測 `unicast_hosts.txt` 檔案的變更，並重新載入種子主機清單，而不需要重新啟動節點。這可讓您：

- 在叢集成長時新增種子主機。
- 從種子清單中移除已除役的節點。
- 在基礎結構變更後更新 IP 位址。

請注意，以檔案為基礎的探索會補充（而非取代）在 `discovery.seed_hosts` 設定中設定的任何種子主機。

## 組態範例

下列範例示範如何設定不同的探索機制。

### 合併探索提供者

您可以同時使用多個種子主機提供者：

```yaml
discovery.seed_providers: [settings, file]
discovery.seed_hosts:
  - 10.0.1.10:9300  # Always include this seed host
# Additional hosts loaded from unicast_hosts.txt
```
{% include copy.html %}

此組態同時使用靜態種子主機與從檔案動態載入的主機。

### 單節點開發設定

適用於開發或測試環境：

```yaml
discovery.type: single-node
```
{% include copy.html %}

當 `discovery.type` 設為 `single-node` 時，OpenSearch 會略過一般探索過程，並立即形成單節點叢集。

## 相關文件

- 若要對探索問題進行疑難排解，請使用 [探索與叢集形成]({{site.url}}{{site.baseurl}}/tuning-your-cluster/discovery-cluster-formation/#monitoring-discovery-and-cluster-formation) 概觀中詳述的監控命令。

- 如需探索相關設定的完整清單，請參閱 [探索與叢集形成設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/discovery-cluster-formation/settings/)。
