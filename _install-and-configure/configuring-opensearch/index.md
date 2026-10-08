---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定 OpenSearch"
nav_order: 10
has_children: true
has_toc: false
redirect_from:
  - /opensearch/configuration/
  - /install-and-configure/configuring-opensearch/
---

# 設定 OpenSearch

每個 OpenSearch 設定不是叢集設定，就是索引設定。叢集設定套用於整個叢集或個別節點。索引設定套用於單一索引，其名稱以 `index.` 開頭。本節中的設定頁面依領域分組列出叢集設定，例如網路、安全性和執行緒集區。如需索引設定的相關資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。

設定也分為[靜態](#static-settings)或[動態](#dynamic-settings)。設定屬於靜態或動態，決定了您能否在 OpenSearch 執行期間變更該設定。

下表列出您可以指定叢集設定的方式。

| 方法 | 設定類型 | 套用對象 | 變更生效時間 |
|:---|:---|:---|:---|
| [組態檔案](#configuration-file)（`opensearch.yml`） | 靜態和動態 | 該節點 | 節點啟動時 |
| [啟動選項](#specifying-configuration-settings-at-startup)（命令列旗標或環境變數） | 靜態和動態 | 該節點 | 節點啟動時 |
| [Cluster Settings API](#updating-cluster-settings-using-the-api) | 僅限動態 | 整個叢集 | 立即 |

如果您使用多種方法指定同一個叢集設定，OpenSearch 會根據[設定優先順序](#setting-precedence)決定要使用的值。

## 靜態設定

靜態設定是指無法在叢集執行期間更新的設定。若要變更靜態設定，請在每個節點的 `opensearch.yml` 中或使用啟動旗標更新該設定，然後重新啟動節點。一般而言，靜態設定與網路、叢集形成和本機檔案系統相關。如需詳細資訊，請參閱[建立叢集]({{site.url}}{{site.baseurl}}/tuning-your-cluster/)。

## 動態設定

動態設定是指可以在叢集執行期間更新的設定。您可以使用本頁中的任何方法指定動態設定，包括 Cluster Settings API。如需詳細資訊，請參閱[使用 API 更新叢集設定](#updating-cluster-settings-using-the-api)。

對於整個叢集範圍的動態設定，我們建議使用 Cluster Settings API。使用 API 更新的設定會套用至所有節點，可讓整個叢集的組態保持一致，並使組態變更更容易追蹤。
{: .tip}

## 組態檔案

您可以在每個節點的 `/usr/share/opensearch/config/opensearch.yml`（Docker）或 `/etc/opensearch/opensearch.yml`（大多數 Linux 發行版本）中找到 `opensearch.yml`。

若要變更組態目錄位置，請設定 `OPENSEARCH_PATH_CONF` 環境變數，例如 `OPENSEARCH_PATH_CONF=/etc/opensearch`。此變數的來源為 `/etc/default/opensearch`（Debian 套件）和 `/etc/sysconfig/opensearch`（RPM 套件）。

如果您設定了自訂的 `OPENSEARCH_PATH_CONF` 變數，則不會載入其他預設環境變數。

`opensearch.yml` 中的設定不會標示為 persistent 或 transient。下列範例使用扁平格式：

```yml
cluster.name: my-application
action.auto_create_index: true
compatibility.override_main_response_version: true
```

示範組態包含數個 [Security 外掛程式的設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/security-settings/)，您應在將 OpenSearch 用於生產工作負載之前修改這些設定。若要深入了解，請參閱[安全性]({{site.url}}{{site.baseurl}}/security/)。

### （選用）CORS 標頭組態

如果您正在開發的用戶端應用程式需要對不同網域上的 OpenSearch 叢集執行，您可以在 `opensearch.yml` 中設定標頭，以便在同一部機器上開發本機應用程式。使用[跨來源資源共用 (Cross-Origin Resource Sharing)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)，讓您的應用程式可以呼叫在本機執行的 OpenSearch API。將下列幾行新增至 `opensearch.yml`：

```yml
http.host: 0.0.0.0
http.port: 9200
http.cors.allow-origin: "http://localhost"
http.cors.enabled: true
http.cors.allow-headers: X-Requested-With,X-Auth-Token,Content-Type,Content-Length,Authorization
http.cors.allow-credentials: true
```
{% include copy.html %}

## 在啟動時指定組態設定

啟動 OpenSearch 時，您可以使用命令列旗標或環境變數指定設定。這些設定僅套用於您所啟動的節點。

### 命令列旗標

若要在啟動時直接將設定傳遞給 OpenSearch，請使用 `-E` 旗標：

```bash
./opensearch -Ecluster.name=opensearch-cluster -Enode.name=opensearch-node1 -Ehttp.host=0.0.0.0 -Ediscovery.type=single-node
```
{% include copy.html %}

### 環境變數

OpenSearch 會讀取用來設定啟動程序的環境變數，例如用於 JVM 選項的 `OPENSEARCH_JAVA_OPTS`，以及用於組態目錄位置的 `OPENSEARCH_PATH_CONF`。

若要使用環境變數指定 OpenSearch 設定，請定義自訂環境變數，並在 `opensearch.yml` 中使用 `${ENV_VAR}` 語法參照該變數：

```yml
node.name: ${NODE_NAME}
cluster.name: ${CLUSTER_NAME}
```
{% include copy.html %}

您可以在 shell、`systemd` 服務檔案或 Docker 容器中設定環境變數。

#### Shell

若要在 shell 中設定環境變數，請在啟動 OpenSearch 之前匯出這些變數。請在同一個 shell 工作階段中執行下列命令。

若要設定 JVM 堆積大小，請匯出 `OPENSEARCH_JAVA_OPTS` 變數：

```bash
export OPENSEARCH_JAVA_OPTS="-Xms2g -Xmx2g"
```
{% include copy.html %}

若要設定組態目錄位置，請匯出 `OPENSEARCH_PATH_CONF` 變數：

```bash
export OPENSEARCH_PATH_CONF="/etc/opensearch"
```
{% include copy.html %}

然後啟動 OpenSearch：

```bash
./opensearch
```
{% include copy.html %}

請勿直接匯出 OpenSearch 設定，例如 `export discovery.type=single-node`。設定名稱包含點號，而大多數 shell 不接受變數名稱中含有點號。若要在啟動時直接傳遞設定，請使用 `-E` 旗標。如需詳細資訊，請參閱[命令列旗標](#command-line-flags)。

<!-- vale off -->
#### systemd 服務檔案
<!-- vale on -->

將 OpenSearch 作為由 `systemd` 管理的服務執行時，您可以在服務覆寫檔案中指定環境變數。下列範例 `/etc/systemd/system/opensearch.service.d/override.conf` 檔案設定了兩個環境變數：

```ini
[Service]
Environment="OPENSEARCH_JAVA_OPTS=-Xms2g -Xmx2g"
Environment="OPENSEARCH_PATH_CONF=/etc/opensearch"
```
{% include copy.html %}

建立或修改檔案後，請重新載入 `systemd` 組態：

```bash
sudo systemctl daemon-reload
```
{% include copy.html %}

然後重新啟動 OpenSearch 服務：

```bash
sudo systemctl restart opensearch
```
{% include copy.html %}

#### Docker

在 Docker 中執行 OpenSearch 時，您可以使用 `docker run` 命令的 `-e` 選項指定環境變數，如下列範例所示：

```bash
docker run -e "OPENSEARCH_JAVA_OPTS=-Xms2g -Xmx2g" -e "OPENSEARCH_PATH_CONF=/usr/share/opensearch/config" opensearchproject/opensearch:latest
```
{% include copy.html %}

Docker 接受包含點號的環境變數名稱，因此您可以使用 `-e` 選項直接傳遞 OpenSearch 設定。OpenSearch Docker 映像檔會將每個名稱具有設定形式的環境變數轉換為 `-E` 旗標。如果名稱開頭至少有兩個以點號分隔、由小寫字母、數字或底線組成的部分，則該名稱具有設定形式，例如 `discovery.type`。`processors` 設定也會被轉換。下列命令以環境變數的形式傳遞兩個設定：

```bash
docker run -e "discovery.type=single-node" -e "cluster.name=my-cluster" opensearchproject/opensearch:latest
```
{% include copy.html %}

映像檔會略過值為空的環境變數，因此您無法使用空變數來清除在 `opensearch.yml` 中設定的值。若要將清單設定設為空清單，請使用 `[]`，例如 `-e "node.roles=[]"`。

## 使用 API 更新叢集設定

使用 [Cluster Settings API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/)，您可以在叢集執行期間更新整個叢集的動態設定。您可以將設定更新為「持續性」(_persistent_) 或「暫時性」(_transient_)。持續性設定會寫入叢集狀態，並在叢集重新啟動後保留。重新啟動後，OpenSearch 會清除暫時性設定。暫時性設定的優先順序高於持續性設定。如需詳細資訊，請參閱[設定的優先順序](#setting-precedence)。

變更設定之前，請傳送下列請求以檢視目前的設定：

```json
GET _cluster/settings?include_defaults=true
```
{% include copy-curl.html %}

若要取得非預設設定的精簡摘要，請傳送下列請求：

```json
GET _cluster/settings
```
{% include copy-curl.html %}

若要變更設定，請將新值指定為持續性或暫時性。下列範例顯示扁平的設定格式：

```json
PUT _cluster/settings
{
  "persistent" : {
    "action.auto_create_index" : false
  }
}
```
{% include copy-curl.html %}

您也可以使用展開格式，這樣就能從 GET 回應中複製並貼上內容，再變更現有的值：

```json
PUT _cluster/settings
{
  "persistent": {
    "action": {
      "auto_create_index": false
    }
  }
}
```
{% include copy-curl.html %}

## 設定的優先順序

如果您在多個位置指定同一個設定，OpenSearch 會使用下列清單中最先出現的來源所提供的值：

1. 使用 Cluster Settings API 指定的暫時性叢集設定
2. 使用 Cluster Settings API 指定的持續性叢集設定
3. 啟動時使用 `-E` 旗標傳入的設定
4. `opensearch.yml` 中的值，包括由 `${ENV_VAR}` 參照提供的值
5. 預設的設定值

OpenSearch 會讀取 `opensearch.yml`、套用 `-E` 旗標，然後解析所有 `${ENV_VAR}` 參照。因此，`-E` 旗標會覆寫 `opensearch.yml` 中的值，包括由環境變數提供的值。

暫時性與持續性叢集設定僅適用於動態設定。對於靜態設定，優先順序從 `-E` 旗標開始。

當您傳送 `GET _cluster/settings?include_defaults=true` 請求時，回應中的 `defaults` 物件除了內建的預設值之外，還包含在 `opensearch.yml` 中指定以及使用 `-E` 旗標指定的值。回應不會標示每個值的來源。

## 重設設定

若要重設您使用 Cluster Settings API 更新的設定，請將其指派為 `null` 值。OpenSearch 接著會依照[優先順序](#setting-precedence)套用下一個可用來源的值。例如，當您重設暫時性設定時，如果存在持續性值，OpenSearch 會套用該持續性值。下列請求會重設一項暫時性設定：

```json
PUT _cluster/settings
{
  "transient": {
    "action.auto_create_index": null
  }
}
```
{% include copy-curl.html %}

您也可以使用萬用字元一次重設多個相關設定：

```json
PUT _cluster/settings
{
  "persistent": {
    "indices.recovery.*": null
  }
}
```
{% include copy-curl.html %}

### 還原預設值

只有在沒有其他來源指定某項設定時，重設的設定才會回到其預設值。若要還原預設值，請從每個來源中移除該設定：

1. 使用 Cluster Settings API 重設暫時性值與持續性值：

    ```json
    PUT _cluster/settings
    {
      "transient": {
        "action.auto_create_index": null
      },
      "persistent": {
        "action.auto_create_index": null
      }
    }
    ```
    {% include copy-curl.html %}

1. 在每個節點上，從 `opensearch.yml` 以及任何指定該設定的 `-E` 旗標中移除該設定，包括 OpenSearch 會轉換為 `-E` 旗標的 Docker 環境變數。如果 `opensearch.yml` 參照了該設定的環境變數，請移除該參照。
1. 重新啟動您在上一個步驟中變更過的每個節點。

如果該設定未在 `opensearch.yml` 中或啟動時指定，只需執行第一個步驟即可，不需要重新啟動。

## 設定參考

下列頁面依領域分組列出叢集設定：

- [組態與系統設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/configuration-system/)
- [網路設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/network-settings/)
- [探索與閘道設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/discovery-gateway-settings/)
- [安全性設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/security-settings/)
- [叢集管理設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/cluster-settings/)
- [索引的叢集設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/cluster-settings-for-indexes/)
- [快取設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/cache-settings/)
- [搜尋設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/search-settings/)
- [監控設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/monitoring-settings/)
- [可用性與復原設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/availability-recovery/)
- [執行緒集區設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/thread-pool-settings/)
- [斷路器設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/circuit-breaker/)
- [准入控制設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/admission-control-settings/)
- [外掛程式設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/plugin-settings/)
- [匯入設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/ingest-settings/)
- [指令碼與資源設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/script-and-resource-settings/)

下列頁面列出適用於個別索引的設定：

- [索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)

下列頁面說明其他組態選項：

- [實驗性功能旗標]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/experimental/)
- [記錄檔]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/logs/)

## 相關文件

若要了解如何檢視及更新叢集設定，請參閱 [Cluster Settings API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/)。
