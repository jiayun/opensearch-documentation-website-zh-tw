---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "管理 OpenSearch 外掛程式"
nav_order: 90
has_children: true
redirect_from:
   - /opensearch/install/plugins/
   - /install-and-configure/install-opensearch/plugins/
---

# 管理 OpenSearch 外掛程式

OpenSearch 包含許多外掛程式，可為核心平台新增功能。您可使用的外掛程式取決於 OpenSearch 的安裝方式，以及之後新增或移除了哪些外掛程式。例如，OpenSearch 的最小發行版本僅啟用核心功能，例如編製索引和搜尋。當您在測試環境中工作、擁有自訂外掛程式，或打算將 OpenSearch 與其他服務整合時，使用 OpenSearch 的最小發行版本會很有幫助。

OpenSearch 的標準發行版本包含更多外掛程式，提供更豐富的功能。您可以選擇新增其他外掛程式，或移除任何不需要的外掛程式。

如需可用外掛程式的清單，請參閱[可用的外掛程式](#available-plugins)。

若要管理 OpenSearch Dashboards 外掛程式，請參閱[管理 OpenSearch Dashboards 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/plugins/)。

為了讓外掛程式能與 OpenSearch 正常運作，外掛程式可能會在安裝過程中要求特定權限。請檢閱所要求的權限，再據此繼續操作。在安裝之前，務必了解外掛程式的功能。選擇社群提供的外掛程式時，請確認其來源值得信賴且可靠。
{: .warning}

## 使用 CAT API 列出已安裝的外掛程式

您可以使用 [CAT API]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-plugins/) 列出已安裝的外掛程式。

#### 用法

```json
GET _cat/plugins
```
{% include copy-curl.html %}

#### 回應範例

```bash
opensearch-node1 opensearch-alerting                  2.0.1.0
opensearch-node1 opensearch-anomaly-detection         2.0.1.0
opensearch-node1 opensearch-asynchronous-search       2.0.1.0
opensearch-node1 opensearch-cross-cluster-replication 2.0.1.0
opensearch-node1 opensearch-index-management          2.0.1.0
opensearch-node1 opensearch-job-scheduler             2.0.1.0
opensearch-node1 opensearch-knn                       2.0.1.0
opensearch-node1 opensearch-ml                        2.0.1.0
opensearch-node1 opensearch-notifications             2.0.1.0
opensearch-node1 opensearch-notifications-core        2.0.1.0
```

## 使用 `opensearch-plugin` 工具

若要管理 OpenSearch 中的外掛程式，您可以使用名為 `opensearch-plugin` 的命令列工具。此工具可讓您執行下列動作：

- [列出](#listing-installed-plugins)已安裝的外掛程式。
- [安裝](#installing-plugins)外掛程式。
- [移除](#removing-plugins)已安裝的外掛程式。

您可以傳遞 `-h` 或 `--help` 來顯示說明文字。視您的主機組態而定，您可能也需要以 `sudo` 權限執行此命令。

如果您在 Docker 容器中執行 OpenSearch，則必須透過修改 Docker 映像檔來安裝、移除和設定外掛程式。如需詳細資訊，請參閱[使用外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/docker#working-with-plugins)。
{: .note}

### 列出已安裝的外掛程式

使用 `list` 查看已安裝的外掛程式清單。

#### 用法
```bash
bin/opensearch-plugin list
```
{% include copy.html %}

#### 回應範例
```bash
$ ./opensearch-plugin list
opensearch-alerting
opensearch-anomaly-detection
opensearch-asynchronous-search
opensearch-cross-cluster-replication
opensearch-geospatial
opensearch-index-management
opensearch-job-scheduler
opensearch-knn
opensearch-ml
opensearch-notifications
opensearch-notifications-core
opensearch-observability
opensearch-performance-analyzer
opensearch-reports-scheduler
opensearch-security
opensearch-sql
```

### 安裝外掛程式

使用 `opensearch-plugin` 工具安裝外掛程式的方式有三種：

- [依名稱安裝外掛程式](#installing-a-plugin-by-name)。
- [從 zip 檔案安裝外掛程式](#installing-a-plugin-from-a-zip-file)。
- [使用 Maven 座標安裝外掛程式](#installing-a-plugin-using-maven-coordinates)。

#### 依名稱安裝外掛程式

您可以使用外掛程式名稱，安裝尚未預先安裝的外掛程式。如需可能未預先安裝的外掛程式清單，請參閱[其他外掛程式](#additional-plugins)。

##### 用法
```bash
bin/opensearch-plugin install <plugin-name>
```
{% include copy.html %}

##### 回應範例
```bash
$ sudo ./opensearch-plugin install analysis-icu
-> Installing analysis-icu
-> Downloading analysis-icu from opensearch
[=================================================] 100%   
-> Installed analysis-icu with folder name analysis-icu
```

#### 從 zip 檔案安裝外掛程式

您可以將 `<zip-file>` 替換為託管檔案的 URL，以安裝遠端 zip 檔案。此工具僅支援透過 HTTP/HTTPS 通訊協定下載。若為本機 zip 檔案，請將 `<zip-file>` 替換為 `file:`，後面接上外掛程式 zip 檔案的絕對或相對路徑，如下方第二個範例所示。

##### 用法
```bash
bin/opensearch-plugin install <zip-file>
```
{% include copy.html %}

##### 回應範例
<details markdown="block">
<summary>
    選取以展開範例
</summary>
{: .text-delta}

```bash
# Zip file is hosted on a remote server - in this case, Maven central repository.
$ sudo ./opensearch-plugin install https://repo1.maven.org/maven2/org/opensearch/plugin/opensearch-anomaly-detection/2.2.0.0/opensearch-anomaly-detection-2.2.0.0.zip
-> Installing https://repo1.maven.org/maven2/org/opensearch/plugin/opensearch-anomaly-detection/2.2.0.0/opensearch-anomaly-detection-2.2.0.0.zip
-> Downloading https://repo1.maven.org/maven2/org/opensearch/plugin/opensearch-anomaly-detection/2.2.0.0/opensearch-anomaly-detection-2.2.0.0.zip
[=================================================] 100%   
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@     WARNING: plugin requires additional permissions     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
* java.lang.RuntimePermission accessClassInPackage.sun.misc
* java.lang.RuntimePermission accessDeclaredMembers
* java.lang.RuntimePermission getClassLoader
* java.lang.RuntimePermission setContextClassLoader
* java.lang.reflect.ReflectPermission suppressAccessChecks
* java.net.SocketPermission * connect,resolve
* javax.management.MBeanPermission org.apache.commons.pool2.impl.GenericObjectPool#-[org.apache.commons.pool2:name=pool,type=GenericObjectPool] registerMBean
* javax.management.MBeanPermission org.apache.commons.pool2.impl.GenericObjectPool#-[org.apache.commons.pool2:name=pool,type=GenericObjectPool] unregisterMBean
* javax.management.MBeanServerPermission createMBeanServer
* javax.management.MBeanTrustPermission register
See http://docs.oracle.com/javase/8/docs/technotes/guides/security/permissions.html
for descriptions of what these permissions allow and the associated risks.

Continue with installation? [y/N]y
-> Installed opensearch-anomaly-detection with folder name opensearch-anomaly-detection

# Zip file in a local directory.
$ sudo ./opensearch-plugin install file:/home/user/opensearch-anomaly-detection-2.2.0.0.zip
-> Installing file:/home/user/opensearch-anomaly-detection-2.2.0.0.zip
-> Downloading file:/home/user/opensearch-anomaly-detection-2.2.0.0.zip
[=================================================] 100%   
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@     WARNING: plugin requires additional permissions     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
* java.lang.RuntimePermission accessClassInPackage.sun.misc
* java.lang.RuntimePermission accessDeclaredMembers
* java.lang.RuntimePermission getClassLoader
* java.lang.RuntimePermission setContextClassLoader
* java.lang.reflect.ReflectPermission suppressAccessChecks
* java.net.SocketPermission * connect,resolve
* javax.management.MBeanPermission org.apache.commons.pool2.impl.GenericObjectPool#-[org.apache.commons.pool2:name=pool,type=GenericObjectPool] registerMBean
* javax.management.MBeanPermission org.apache.commons.pool2.impl.GenericObjectPool#-[org.apache.commons.pool2:name=pool,type=GenericObjectPool] unregisterMBean
* javax.management.MBeanServerPermission createMBeanServer
* javax.management.MBeanTrustPermission register
See http://docs.oracle.com/javase/8/docs/technotes/guides/security/permissions.html
for descriptions of what these permissions allow and the associated risks.

Continue with installation? [y/N]y
-> Installed opensearch-anomaly-detection with folder name opensearch-anomaly-detection
```
</details>

#### 使用 Maven 座標安裝外掛程式

`opensearch-plugin install` 工具也可讓您為託管於 [Maven Central](https://central.sonatype.com/namespace/org.opensearch.plugin) 的可用構件及版本指定 Maven 座標。此工具會剖析您提供的 Maven 座標並建構 URL。因此，主機必須能夠直接連線至 Maven Central 網站。若您將座標傳遞給 Proxy 或本機儲存庫，外掛程式安裝將會失敗。

##### 用法
```bash
bin/opensearch-plugin install <groupId>:<artifactId>:<version>
```
{% include copy.html %}

##### 回應範例

<details markdown="block">
<summary>
    選取以展開範例
</summary>
{: .text-delta}

```console
$ sudo ./opensearch-plugin install org.opensearch.plugin:opensearch-anomaly-detection:2.2.0.0
-> Installing org.opensearch.plugin:opensearch-anomaly-detection:2.2.0.0
-> Downloading org.opensearch.plugin:opensearch-anomaly-detection:2.2.0.0 from maven central
[=================================================] 100%   
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@     WARNING: plugin requires additional permissions     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
* java.lang.RuntimePermission accessClassInPackage.sun.misc
* java.lang.RuntimePermission accessDeclaredMembers
* java.lang.RuntimePermission getClassLoader
* java.lang.RuntimePermission setContextClassLoader
* java.lang.reflect.ReflectPermission suppressAccessChecks
* java.net.SocketPermission * connect,resolve
* javax.management.MBeanPermission org.apache.commons.pool2.impl.GenericObjectPool#-[org.apache.commons.pool2:name=pool,type=GenericObjectPool] registerMBean
* javax.management.MBeanPermission org.apache.commons.pool2.impl.GenericObjectPool#-[org.apache.commons.pool2:name=pool,type=GenericObjectPool] unregisterMBean
* javax.management.MBeanServerPermission createMBeanServer
* javax.management.MBeanTrustPermission register
See http://docs.oracle.com/javase/8/docs/technotes/guides/security/permissions.html
for descriptions of what these permissions allow and the associated risks.

Continue with installation? [y/N]y
-> Installed opensearch-anomaly-detection with folder name opensearch-anomaly-detection
```
</details>

安裝外掛程式後，請重新啟動您的 OpenSearch 節點。
{: .note}

### 安裝多個外掛程式

您可以在單次呼叫中安裝多個外掛程式。

#### 用法
```bash
bin/opensearch-plugin install <plugin-name> <plugin-name> ... <plugin-name>
```
{% include copy.html %}

#### 回應範例
```console
$ sudo ./opensearch-plugin install analysis-nori repository-s3
```

### 以批次模式安裝外掛程式

安裝需要額外權限 (預設未包含這些權限) 的外掛程式時，外掛程式會提示您確認所需的權限。若要授予所有要求的權限，請使用批次模式略過確認提示。

若要在安裝外掛程式時強制使用批次模式，請加入 `-b` 或 `--batch` 選項：
```bash
bin/opensearch-plugin install --batch <plugin-name>
```
{% include copy.html %}


### 移除外掛程式

您可以使用 `remove` 選項移除已安裝的外掛程式。

#### 用法
```bash
bin/opensearch-plugin remove <plugin-name>
```
{% include copy.html %}

#### 回應範例
```console
$ sudo ./opensearch-plugin remove opensearch-anomaly-detection
-> removing [opensearch-anomaly-detection]...
```

移除外掛程式後，請重新啟動您的 OpenSearch 節點。
{: .note}


## 可用的外掛程式

OpenSearch 提供數個隨附的外掛程式，除了精簡版發行版本外，所有 OpenSearch 發行版本皆可立即使用這些外掛程式。另有其他可用的外掛程式，但必須使用其中一種安裝選項另行安裝。

### 隨附的外掛程式

除了精簡版發行版本外，所有 OpenSearch 發行版本皆隨附下列外掛程式。若您使用的是精簡版發行版本，可以使用其中一種安裝方法加入這些外掛程式。

| 外掛程式名稱 | 儲存庫 | 最早可用版本 |
| :--- | :--- | :--- |
| Alerting | [`opensearch-alerting`](https://github.com/opensearch-project/alerting) | 1.0.0 |
| Anomaly Detection | [`opensearch-anomaly-detection`](https://github.com/opensearch-project/anomaly-detection) | 1.0.0 |
| Asynchronous Search | [`opensearch-asynchronous-search`](https://github.com/opensearch-project/asynchronous-search) | 1.0.0 |
| Cross Cluster Replication | [`opensearch-cross-cluster-replication`](https://github.com/opensearch-project/cross-cluster-replication) | 1.1.0 |
| Custom Codecs | [`opensearch-custom-codecs`](https://github.com/opensearch-project/custom-codecs) | 2.10.0 |
| Flow Framework | [`flow-framework`](https://github.com/opensearch-project/flow-framework) | 2.12.0 |
| Notebooks<sup>1</sup> | [`opensearch-notebooks`](https://github.com/opensearch-project/dashboards-notebooks) | 1.0.0 至 1.1.0 |
| Notifications | [`notifications`](https://github.com/opensearch-project/notifications) | 2.0.0 |
| Reports Scheduler | [`opensearch-reports-scheduler`](https://github.com/opensearch-project/dashboards-reports) | 1.0.0 |
| Geospatial | [`opensearch-geospatial`](https://github.com/opensearch-project/geospatial) | 2.2.0 |
| Index Management | [`opensearch-index-management`](https://github.com/opensearch-project/index-management) | 1.0.0 |
| Job Scheduler | [`opensearch-job-scheduler`](https://github.com/opensearch-project/job-scheduler) | 1.0.0 |
| k-NN | [`opensearch-knn`](https://github.com/opensearch-project/k-NN) | 1.0.0 |
| Learning to Rank | [`opensearch-ltr`](https://github.com/opensearch-project/opensearch-learning-to-rank-base) | 2.19.0 |
| ML Commons | [`opensearch-ml`](https://github.com/opensearch-project/ml-commons) | 1.3.0 |
| Skills | [`opensearch-skills`](https://github.com/opensearch-project/skills) | 2.12.0 |
| Neural Search | [`neural-search`](https://github.com/opensearch-project/neural-search) | 2.4.0 |
| Observability | [`opensearch-observability`](https://github.com/opensearch-project/observability) | 1.2.0 |
| Performance Analyzer<sup>2</sup> | [`opensearch-performance-analyzer`](https://github.com/opensearch-project/performance-analyzer) | 1.0.0 |
| Security | [`opensearch-security`](https://github.com/opensearch-project/security) | 1.0.0 |
| Security Analytics | [`opensearch-security-analytics`](https://github.com/opensearch-project/security-analytics) | 2.4.0 |
| SQL | [`opensearch-sql`](https://github.com/opensearch-project/sql) | 1.0.0 |
| Remote Metadata SDK | [`opensearch-remote-metadata-sdk`](https://github.com/opensearch-project/opensearch-remote-metadata-sdk) | 2.19.0 |
| Query Insights | [`query-insights`](https://github.com/opensearch-project/query-insights) | 2.16.0 |
| System Templates | [`opensearch-system-templates`](https://github.com/opensearch-project/opensearch-system-templates) | 2.17.0 |
| User Behavior Insights | [`ubi`](https://github.com/opensearch-project/user-behavior-insights) | 3.0.0 |
| Search Relevance | [`search-relevance`](https://github.com/opensearch-project/search-relevance) | 3.1.0 |

_<sup>1</sup>隨著 OpenSearch 1.2.0 的發布，Dashboard Notebooks 已合併至 Observability 外掛程式。_<br>
_<sup>2</sup>Performance Analyzer 無法在 Windows 上使用。_


#### 下載隨附外掛程式以進行離線安裝

每個隨附外掛程式都可以從 [zip 檔案](#installing-a-plugin-from-a-zip-file)下載並離線安裝。

對應外掛程式的 URL 可以在解壓縮後套件根目錄中的 `manifest.yml` 檔案內找到。

### 核心外掛程式

OpenSearch 中的「核心」（或「原生」）外掛程式是指位於 [OpenSearch 核心引擎儲存庫](https://github.com/opensearch-project/OpenSearch/tree/main/plugins)中的外掛程式。這些外掛程式與 OpenSearch 引擎緊密整合，其版本與核心版本同步發布，且預設不會隨附於標準 OpenSearch 發行版本中。


#### 下載核心外掛程式以進行離線安裝

[此清單](https://github.com/opensearch-project/OpenSearch/tree/main/plugins)中的每個核心外掛程式，都可以使用官方 `plugins` 儲存庫 URL 範本，從 [zip 檔案](#installing-a-plugin-from-a-zip-file)下載並離線安裝：

```html
https://artifacts.opensearch.org/releases/plugins/<plugin-name>/<version>/<plugin-name>-<version>.zip
```

`<plugin-name>` 對應隨附外掛程式的名稱（例如 `analysis-icu`）。`<version>` 必須與 OpenSearch 發行版本的版本相符（例如 `2.19.1`）。

例如，使用下列 URL 下載適用於 OpenSearch `2.19.1` 版的 `analysis-icu` 隨附外掛程式發行版本：

```
https://artifacts.opensearch.org/releases/plugins/analysis-icu/2.19.1/analysis-icu-2.19.1.zip
```

### 其他外掛程式

除了預設發行版本所提供的外掛程式之外，還有更多外掛程式可供使用。這些其他外掛程式是由 OpenSearch 開發人員或 OpenSearch 社群成員所建置。如需可安裝的其他外掛程式清單，請參閱[其他外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/additional-plugins/index/)。

## 外掛程式相容性

您可以在 `plugin-descriptor.properties` 檔案中指定外掛程式與特定 OpenSearch 版本的相容性。例如，具有下列屬性的外掛程式僅與 OpenSearch 2.3.0 相容：

```properties
opensearch.version=2.3.0
```
或者，您也可以將 `plugin-descriptor.properties` 檔案中的 `dependencies` 屬性設定為下列其中一種表示法，以指定相容的 OpenSearch 版本範圍：
- `dependencies={ opensearch: "2.3.0" }`：外掛程式僅與 OpenSearch 2.3.0 版相容。
- `dependencies={ opensearch: "=2.3.0" }`：外掛程式僅與 OpenSearch 2.3.0 版相容。
- `dependencies={ opensearch: "~2.3.0" }`：外掛程式與從 2.3.0 到下一個次要版本（在此範例中為 2.4.0，不含）之間的所有版本相容。
- `dependencies={ opensearch: "^2.3.0" }`：外掛程式與從 2.3.0 到下一個主要版本（在此範例中為 3.0.0，不含）之間的所有版本相容。

您只能指定 `opensearch.version` 或 `dependencies` 其中一個屬性。
{: .note}

## 外掛程式相依性

部分外掛程式會擴充其他外掛程式的功能。如果某個外掛程式相依於另一個外掛程式，您必須先安裝必要的相依外掛程式，再安裝該相依的外掛程式。如需外掛程式相依性，請參閱[資訊清單檔案](https://github.com/opensearch-project/opensearch-build/blob/main/manifests/{{site.opensearch_version}}/opensearch-{{site.opensearch_version}}.yml)。在此檔案中，每個外掛程式的相依性都列於 `depends_on` 參數中。

