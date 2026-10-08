---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "安裝"
nav_order: 5
grand_parent: User guide
parent: Install and configure OpenSearch Benchmark
redirect_from:
  - /benchmark/installing-benchmark/
  - /benchmark/user-guide/installing-benchmark/
---

# 安裝 OpenSearch Benchmark

您可以直接在執行 Linux 或 macOS 的主機上安裝 OpenSearch Benchmark，也可以在任何相容主機上的 Docker 容器中執行 OpenSearch Benchmark。本頁提供 OpenSearch Benchmark 主機的一般考量事項，以及安裝 OpenSearch Benchmark 的指示。


## 選擇適當的硬體

OpenSearch Benchmark 可用於佈建 OpenSearch 節點以進行測試。如果您打算使用 OpenSearch Benchmark 在您的環境中佈建節點，請直接在叢集中的每台主機上安裝 OpenSearch Benchmark。此外，您必須為叢集中的每台主機設定 OpenSearch。如需重要主機設定的指引，請參閱[安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/)。

請記住，在 Docker 容器中執行 OpenSearch Benchmark 時，無法使用 OpenSearch Benchmark 佈建 OpenSearch 節點。如果您想使用 OpenSearch Benchmark 佈建節點，或使用 OpenSearch Benchmark 常駐程式分散基準測試工作負載，就必須使用 Python 和 pip 直接在每台主機上安裝 OpenSearch Benchmark。
{: .important}

選擇主機時，您也應考慮想要執行哪些工作負載。如需查看預設基準測試工作負載的清單，請造訪 GitHub 上的 [`opensearch-benchmark-workloads`](https://github.com/opensearch-project/opensearch-benchmark-workloads) 儲存庫。一般而言，請確保 OpenSearch Benchmark 主機有足夠的可用儲存空間，以便在安裝 OpenSearch Benchmark 後儲存壓縮資料和完全解壓縮的資料集。

如果您想使用預設工作負載進行基準測試，請使用下表，將壓縮大小與未壓縮大小相加，以估算所需的最低可用空間。

| 工作負載名稱 | 文件數量 | 壓縮大小 | 未壓縮大小 |
| :----: | :----: | :----: | :----: |
| `eventdata` | 20,000,000 | 756.0 MB | 15.3 GB |
| `geonames` | 11,396,503 | 252.9 MB | 3.3 GB |
| `geopoint` | 60,844,404 | 482.1 MB | 2.3 GB |
| `geopointshape` | 60,844,404 | 470.8 MB | 2.6 GB |
| `geoshape` | 60,523,283 | 13.4 GB | 45.4 GB |
| `http_logs` | 247,249,096 | 1.2 GB | 31.1 GB |
| `nested` | 11,203,029 | 663.3 MB | 3.4 GB |
| `noaa` | 33,659,481 | 949.4 MB | 9.0 GB |
| `nyc_taxis` | 165,346,692 | 4.5 GB | 74.3 GB |
| `percolator` | 2,000,000 | 121.1 kB | 104.9 MB |
| `pmc` | 574,199 | 5.5 GB | 21.7 GB |
| `so` | 36,062,278 | 8.9 GB | 33.1 GB |

您的 OpenSearch Benchmark 主機應使用固態硬碟（SSD）作為儲存裝置，因為其讀寫速度明顯快於傳統的旋轉式硬碟。旋轉式硬碟可能造成效能瓶頸，使基準測試結果不可靠且不一致。
{: .tip}

## 在 Linux 和 macOS 上安裝

如果您想在 Docker 容器中執行 OpenSearch Benchmark，請參閱[使用 Docker 安裝](#installing-with-docker)。OpenSearch Benchmark Docker 映像包含所有必要軟體，因此不需要額外步驟。
{: .important}

若要直接在 Linux 或 macOS 等 UNIX 主機上安裝 OpenSearch Benchmark，請確保已安裝 **Python 3.8 或更新版本**。

如果您需要安裝 Python 的協助，請參閱官方的 [Python 設定與使用](https://docs.python.org/3/using/index.html)文件。

### 檢查軟體相依性

開始安裝 OpenSearch Benchmark 前，請檢查下列軟體相依性。

使用 [`pyenv`](https://github.com/pyenv/pyenv) 管理主機上的多個 Python 版本。如果您的「系統」Python 版本早於 3.8 版，這尤其有用。
{: .tip}

- 檢查是否已安裝 Python 3.8 或更新版本：

  ```bash
  python3 --version
  ```
  {% include copy.html %}

- 檢查是否已安裝 `pip` 且可正常運作：

  ```bash
  pip --version
  ```
  {% include copy.html %}

- _選用_：使用下列命令，檢查您安裝的 `git` 版本是否為 **Git 1.9 或更新版本**。安裝 OpenSearch Benchmark 不需要 `git`，但當您想進行測試時，必須使用它從儲存庫擷取基準測試工作負載資源。如需安裝 Git 的協助，請參閱官方 Git [文件](https://git-scm.com/doc)。

  ```bash
  git --version
  ```
  {% include copy.html %}

### 完成安裝

安裝必要軟體後，您可以使用下列命令安裝 OpenSearch Benchmark：

```bash
pip install opensearch-benchmark
```
{% include copy.html %}

安裝完成後，您可以使用下列命令顯示說明資訊：

```bash
opensearch-benchmark -h
```
{% include copy.html %}


現在您的主機已安裝 OpenSearch Benchmark，您可以了解如何[設定 OpenSearch Benchmark]({{site.url}}{{site.baseurl}}/benchmark/configuring-benchmark/)。

## 使用 Docker 安裝

您可以在 [Docker Hub](https://hub.docker.com/r/opensearchproject/opensearch-benchmark) 或 [Amazon ECR Public Gallery](https://gallery.ecr.aws/opensearchproject/opensearch-benchmark) 上找到 OpenSearch Benchmark 的官方 Docker 映像。


### Docker 限制

在 Docker 容器中執行 OpenSearch Benchmark 時，部分 OpenSearch Benchmark 功能無法使用。具體而言，有下列限制：

- OpenSearch Benchmark 無法從多台主機（例如負載工作者協調器主機）分散負載。
- OpenSearch Benchmark 無法佈建 OpenSearch 節點，只能在既有叢集上執行測試。您只能使用 `benchmark-only` 管線呼叫 OpenSearch Benchmark 命令。

### 拉取 Docker 映像

若要從 Docker Hub 拉取映像，請執行下列命令：

```bash
docker pull opensearchproject/opensearch-benchmark:latest
```
{% include copy.html %}

若要從 Amazon Elastic Container Registry（Amazon ECR）拉取映像：

```bash
docker pull public.ecr.aws/opensearchproject/opensearch-benchmark:latest
```
{% include copy.html %}

### 使用 Docker 執行 OpenSearch Benchmark

若要執行 OpenSearch Benchmark，請使用 `docker run` 啟動容器。啟動容器時，OpenSearch Benchmark 子命令會以引數形式傳入。接著，OpenSearch Benchmark 會處理命令，並在請求的操作完成後停止容器。

例如，下列命令會將 OpenSearch Benchmark 的說明文字輸出至命令列，然後停止容器：

```bash
docker run opensearchproject/opensearch-benchmark -h
```
{% include copy.html %}

### 在 Docker 容器中建立磁碟區持久性

為確保 Docker 容器停止後，您的基準測試資料和記錄檔仍會保留，在 Docker 中執行 OpenSearch Benchmark 時，您必須將本機目錄掛載為磁碟區。

使用 `-v` 選項指定要掛載的本機目錄，以及容器中掛接磁碟區的目錄。

下列範例會將使用者家目錄中的磁碟區掛載至 OpenSearch Benchmark 容器的預設基準測試資料路徑 `/opensearch-benchmark/.benchmark`，然後使用 `geonames` 工作負載執行一次基準測試：

```bash
docker run -v $HOME/benchmarks:/opensearch-benchmark/.benchmark opensearchproject/opensearch-benchmark run --target-hosts https://198.51.100.25:9200 --pipeline benchmark-only --workload geonames --client-options basic_auth_user:admin,basic_auth_password:admin,verify_certs:false --test-mode
```
{% include copy.html %}

預設情況下，OpenSearch Benchmark 容器會以 `benchmark` 使用者身分執行，其家目錄為 `/opensearch-benchmark`，因此 `$HOME/.benchmark` 會解析為 `/opensearch-benchmark/.benchmark`。
{: .note}

#### 以 root 使用者身分執行 OpenSearch Benchmark

如果您以 `root` 使用者身分執行容器，實際使用的家目錄會變成 `/root`，而基準測試路徑會變成 `/root/.benchmark`。在此情況下，請據此指定磁碟區掛載：

```bash
docker run -v $HOME/benchmarks:/root/.benchmark opensearchproject/opensearch-benchmark run --target-hosts https://198.51.100.25:9200 --pipeline benchmark-only --workload geonames --client-options basic_auth_user:admin,basic_auth_password:admin,verify_certs:false --test-mode
```
{% include copy.html %}

若要進一步了解 `/opensearch-benchmark/.benchmark` 中的檔案和子目錄，請參閱[設定 OpenSearch Benchmark]({{site.url}}{{site.baseurl}}/benchmark/configuring-benchmark/)。

## 透過測試佈建 OpenSearch 叢集

OpenSearch Benchmark 與 JDK 17、16、15、14、13、12、11 和 8 版相容。
{: .note}

如果您透過 PyPi 安裝 OpenSearch，也可以在 `run` 命令中指定 `distribution-version`，以佈建新的 OpenSearch 叢集。

如果您打算讓 Benchmark 佈建叢集，就必須告知 Benchmark 該 Benchmark 叢集的 `JAVA_HOME` 路徑位置。若要設定 `JAVA_HOME` 路徑並佈建叢集：

1. 找出您目前使用的 `JAVA_HOME` 路徑。開啟終端機並輸入 `/usr/libexec/java_home`。

2. 輸入上一步的路徑，設定對應 JDK 版本的環境變數。輸入 `export JAVA17_HOME=<Java Path>`。

3. 執行 `run` 命令，並指定您想使用的 OpenSearch 發行版本：

  ```bash
  opensearch-benchmark run --distribution-version=2.3.0 --workload=geonames --test-mode
  ```

## 目錄結構

首次執行 OpenSearch Benchmark 後，您可以在 `~/.benchmark` 目錄中搜尋所有相關檔案，包括組態檔案。此目錄包含下列檔案樹狀結構：

```
# ~/.benchmark Tree
.
├── benchmark.ini
├── benchmarks
│   ├── data
│   │   └── geonames
│   ├── distributions
│   │   ├── opensearch-1.0.0-linux-x64.tar.gz
│   │   └── opensearch-2.3.0-linux-x64.tar.gz
│   ├── test-runs
│   │   ├── 0279b13b-1e54-49c7-b1a7-cde0b303a797
│   │   └── 0279c542-a856-4e88-9cc8-04306378cd38
│   └── workloads
│       └── default
│           └── geonames
├── logging.json
├── logs
│   └── benchmark.log
```

* `benchmark.ini`：包含測試的所有可調整組態。如需如何設定 OpenSearch Benchmark 的資訊，請參閱[設定 OpenSearch Benchmark]({{site.url}}{{site.baseurl}}/benchmark/configuring-benchmark/)。
* `data`：包含與 OpenSearch Benchmark [官方工作負載](https://github.com/opensearch-project/opensearch-benchmark-workloads/tree/main/geonames)相關的所有資料集和文件。
* `distributions`：包含從 [OpenSearch.org](http://opensearch.org/) 下載並用於佈建叢集的所有 OpenSearch 發行版本。
* `test-runs`：包含先前執行 OpenSearch Benchmark 時產生的每個測試 `execution_id`。
* `workloads`：包含與工作負載相關的所有檔案，但不包含資料集。
* `logging.json`：包含與 OpenSearch Benchmark 內部記錄方式相關的所有組態選項。
* `logs`：包含執行 OpenSearch Benchmark 所產生的所有記錄檔。當您在執行期間遇到錯誤時，這些記錄檔會有所幫助。


## 後續步驟

- [設定 OpenSearch Benchmark]({{site.url}}{{site.baseurl}}/benchmark/configuring-benchmark/)
- [建立自訂工作負載]({{site.url}}{{site.baseurl}}/benchmark/creating-custom-workloads/)
