---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定"
nav_order: 7
grand_parent: User guide
parent: Install and configure OpenSearch Benchmark
redirect_from:
  - /benchmark/configuring-benchmark/
  - /benchmark/user-guide/configuring-benchmark/
  - /benchmark/tutorials/sigv4/
---

# 設定 OpenSearch Benchmark

OpenSearch Benchmark 的組態資料儲存於 `~/.benchmark/benchmark.ini`，該檔案會在 OpenSearch Benchmark 首次執行時自動建立。

該檔案分為以下幾個區段，您可以依據叢集的需求進行自訂。

## client_options

本節說明如何在執行基準測試期間，使用 `--client-options` 命令列旗標來自訂用戶端層級的設定。

您可以使用 `--client-options` 旗標將用戶端專屬的參數傳遞給 OpenSearch Benchmark。這些參數可讓您控制低階用戶端行為，例如逾時、驗證方法及 SSL 設定。

`--client-options` 旗標接受以逗號分隔的鍵值對清單，如下列範例所示：

```bash
--client-options=timeout:120,verify_certs:false
```

您可以使用下列設定來自訂 `--client-options`。

| 選項 | 類型 | 說明 |
| :---- | :---- | :---- |
| `timeout` | 整數 | 設定請求逾時值，單位為秒。 |
| `verify_certs` | 布林值 | 決定連線至 OpenSearch 叢集時是否驗證 SSL 憑證。 |
| `basic_auth_user` | 字串 | 用於向 OpenSearch 叢集驗證的使用者名稱 (若已啟用驗證)。 |
| `basic_auth_password` | 字串 | 用於向 OpenSearch 叢集驗證的密碼 (若已啟用驗證)。 |

下列範例會執行基準測試，並設定 2 分鐘逾時及停用憑證驗證：

```bash
opensearch-benchmark run \
--target-hosts=https://localhost:9200 \
--pipeline=benchmark-only \
--workload=geonames \
--client-options=timeout:120,verify_certs:false
```

<!-- vale off -->
## meta
<!-- vale on -->

本節包含組態檔的相關中繼資訊。

| 參數 | 類型 | 說明 |
| :---- | :---- | :---- |
| `config.version` | 整數 |  組態檔格式的版本。此屬性由 OpenSearch Benchmark 管理，不應變更。 |

<!-- vale off -->
## system
<!-- vale on -->

本節包含目前基準測試環境的全域資訊。在安裝 OpenSearch Benchmark 的所有機器上，此資訊應完全相同。

| 參數 | 類型 | 說明 |
| :---- | :---- | :---- |
| `env.name` | 字串 | 基準測試環境的名稱，當設定了 OpenSearch 指標儲存區時，會作為指標文件中的中繼資料。僅允許英數字元。預設值為 `local`。 |
| `available.cores` | 整數 | 決定可用的 CPU 核心數。OpenSearch Benchmark 的目標是為每個核心建立一個 `asyncio` 事件迴圈，並將其平均分配給各事件迴圈上的用戶端。預設值為您叢集的邏輯 CPU 核心數。 |
| `async.debug` | 布林值 | 在 OpenSearch Benchmark 的 `asyncio` 事件迴圈上啟用偵錯模式。預設值為 `false`。 |
| `passenv` | 字串 | 以逗號分隔的環境變數名稱清單，這些變數應傳遞給 OpenSearch 進行處理。 |

<!-- vale off -->
## node
<!-- vale on -->

本節包含節點專屬的資訊，可依據叢集的需求進行自訂。

| 參數 | 類型 | 說明 |
| :---- | :---- | :---- |
| `root.dir` | 字串 | 儲存所有 OpenSearch Benchmark 資料的目錄。OpenSearch Benchmark 會掌控此目錄及其所有子目錄。 |
| `src.root.dir` | 字串 | 呼叫 OpenSearch 原始碼及任何 OpenSearch 外掛程式的來源目錄。僅與來自 [sources](#source) 的基準測試相關。 |

<!-- vale off -->
## source
<!-- vale on -->

本節包含 OpenSearch 原始碼樹狀結構的更多詳細資料。

| 參數 | 類型 | 說明 |
| :---- | :---- | :---- |
| `remote.repo.url` | URL | 用於簽出 OpenSearch 的 URL。預設值為 `https://github.com/opensearch-project/OpenSearch.git`。
| `opensearch.src.subdir` | 字串 | 相對於 OpenSearch 搜尋樹狀結構 `src.root.dir` 的本機路徑。預設值為 `OpenSearch`。
| `cache` | 布林值 | 啟用 OpenSearch 的內部原始碼成品快取 `opensearch*.tar.gz`，以及任何外掛程式 zip 檔案。成品會依其 Git 修訂版本進行快取。預設值為 `true`。 |
| `cache.days` | 整數 | 成品應保留在原始碼成品快取中的天數。預設值為 `7`。 |

<!-- vale off -->
## benchmarks
<!-- vale on -->

本節包含可在 OpenSearch Benchmark 資料目錄中自訂的設定。

| 參數 | 類型 | 說明 |
| :---- | :---- | :---- |
| `local.dataset.cache` | 字串 | 儲存基準測試資料集的目錄。視執行的基準測試而定，此目錄可能包含數百 GB 的資料。預設路徑為 `$HOME/.benchmark/benchmarks/data`。 |

<!-- vale off -->
## reporting
<!-- vale on -->

本節定義基準測試指標的儲存方式。

| 參數 | 類型 | 說明 |
| :---- | :---- | :---- |
| `datastore.type` | 字串 | 若設為 `in-memory`，執行基準測試期間所有指標都會保留在記憶體中。若設為 `opensearch`，所有指標則會改寫入持續性指標儲存區，並提供資料供進一步分析。預設值為 `in-memory`。 |
| `sample.queue.size` | 函式 | 可儲存在 OpenSearch Benchmark 記憶體內佇列中的指標樣本數。預設值為 `2^20`。 |
| metrics.request.downsample.factor | 整數| (預設值：1)：決定指標儲存區中會儲存多少服務時間與延遲樣本。根據預設，所有值都會儲存。若您想只保留每 100 個樣本，請指定 `100`。這在用戶端眾多的基準測試中，有助於避免指標儲存區不堪負荷。預設值為 `1`。 |
| `output.processingtime` | 布林值 | 若設為 `true`，OpenSearch 會在命令列報告中顯示額外的指標處理時間。預設值為 `false`。 |

<!-- vale off -->
### `datastore.type` 參數
<!-- vale on -->

當 `datastore.type` 設為 `opensearch` 時，可自訂下列報告設定。

| 參數 | 類型 | 說明 |
| :---- | :---- | :---- |
| `datastore.host` | IP 位址 | 指標儲存區的主機名稱，例如 `124.340.200.22`。 |
| `datastore.port`| 連接埠 | 指標儲存區的連接埠號碼，例如 `9200`。 |
| `datastore.secure` | 布林值 | 若設為 `false`，OpenSearch 會採用 HTTP 連線。若設為 true，則會採用 HTTPS 連線。 |
| `datastore.ssl.verification_mode` | 字串 | 設為預設值 `full` 時，會檢查指標儲存區的 SSL 憑證。若要停用憑證驗證，請將此值設為 `none`。 |
| `datastore.ssl.certificate_authorities` | 字串 | 決定憑證授權單位簽署憑證的本機檔案系統路徑。
| `datastore.user` | 使用者名稱 | 設定指標儲存區的使用者名稱 |
| `datastore.password` | 字串 | 設定指標儲存區的密碼。或者，可使用 `OSB_DATASTORE_PASSWORD` 環境變數來設定此密碼，以避免將認證儲存在純文字檔案中。若兩者皆定義密碼，環境變數的優先順序高於組態檔。 |
| `datastore.probe.cluster_version` | 字串 | 啟用指標儲存區版本的自動偵測。預設值為 `true`。 |
| `datastore.number_of_shards` | 整數 | `opensearch-*` 索引應有的主要分片數。初始索引建立後對此設定的任何更新，僅會套用至新的 `opensearch-*` 索引。預設值為 [OpenSearch 靜態索引值]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#static-index-settings)。 |
| `datastore.number_of_replicas` | 整數 | 資料儲存區中每個主要分片所含的副本數。初始索引建立後對此設定的任何更新，僅會套用至新的 `opensearch-* `索引。預設值為 [OpenSearch 靜態索引值]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#static-index-settings)。 |

### 範例

您可以使用下列範例，在叢集中設定報告值。

此範例定義本機網路中未受保護的指標儲存區：

```
[reporting]
datastore.type = opensearch
datastore.host = 192.168.10.17
datastore.port = 9200
datastore.secure = false
datastore.user =
datastore.password =
```

此範例定義使用自我簽署憑證，安全連線至本機網路中的指標儲存區：

```
[reporting]
datastore.type = opensearch
datastore.host = 192.168.10.22
datastore.port = 9200
datastore.secure = true
datastore.ssl.verification_mode = none
datastore.user = user-name
datastore.password = the-password-to-your-cluster
```

<!-- vale off -->
## workloads
<!-- vale on -->

本節定義如何擷取工作負載。OpenSearch 使用 `<<workload-repository-name>>.url` 語法讀取所有索引鍵，您可以使用 OpenSearch Benchmark CLI 的 `--workload-repository=workload-repository-name"` 選項選取該語法。依預設，OpenSearch 使用 `default.url` `https://github.com/opensearch-project/opensearch-benchmark-workloads` 選擇工作負載儲存庫。

<!-- vale off -->
## defaults
<!-- vale on -->

本節定義特定 OpenSearch Benchmark CLI 參數的預設值。

| 參數 | 類型 | 說明 |
| :---- | :---- | :---- |
| `preserve_benchmark_candidate` | 布林值 | 決定基準測試結束後，預設要保留還是清除 OpenSearch 安裝。若要為單次基準測試保留安裝，請使用命令列旗標 `--preserve-install`。預設值為 `false`。

<!-- vale off -->
## distributions
<!-- vale on -->

本節定義 OpenSearch 版本的散布方式。

| 參數 | 類型 | 說明 |
| :---- | :---- | :---- |
| `release.cache` | 布林值 | 決定是否應在本機快取新發行的 OpenSearch 版本。 |

## 使用 AWS Signature Version 4 執行 OpenSearch Benchmark

OpenSearch Benchmark 支援 AWS Signature Version 4 驗證。若要使用 AWS Signature Version 4 執行 OpenSearch Benchmark，您需要設定 [AWS Identity and Access Management（IAM）使用者或角色](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create.html)，並允許其透過 AWS Signature Version 4 驗證存取 OpenSearch 叢集。

要使用 IAM 角色還是使用者，取決於測試叢集的存取管理需求。如需進一步瞭解何時使用 IAM 角色或使用者，請參閱[何時建立 IAM 使用者（而非角色）](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html#id_which-to-choose)。

### OpenSearch Benchmark 1.15.0 版及更新版本

從 OpenSearch Benchmark 1.15.0 版開始，您可以使用以工作階段為基礎的驗證，自動處理臨時憑證的產生與重新整理。此方法可免除手動匯出 AWS 憑證的需求：

1. 在 AWS Management Console 中建立具有存取 OpenSearch 叢集所需權限的 IAM 角色或使用者。確保該角色或使用者已附加存取 OpenSearch 所需的政策。

2. 執行下列 `execute-test` 命令，並加上 `--client-options=amazon_aws_log_in:session` 旗標。OpenSearch Benchmark 會自動產生臨時憑證並處理自動重新整理：

   ```bash
   opensearch-benchmark execute-test \
   --target-hosts=<CLUSTER ENDPOINT> \
   --pipeline=benchmark-only \
   --workload=geonames \
   --client-options=timeout:120,amazon_aws_log_in:session,region:<region>,service:<aoss for serverless, es for managed service>
   ```
   {% include copy.html %}

### OpenSearch Benchmark 1.14.0 版及更早版本

對於 OpenSearch Benchmark 1.15.0 版之前的版本，請使用環境變數方法：

1. 在 AWS Management Console 中建立 IAM 角色或使用者。

2. 設定您的環境變數。如果您使用 Amazon OpenSearch Serverless 進行測試，請將 `OSB_SERVICE` 設為 `aoss`。

   - 對於 IAM 使用者，請設定下列環境變數：

   ```bash
   export OSB_AWS_ACCESS_KEY_ID=<IAM USER AWS ACCESS KEY ID>
   export OSB_AWS_SECRET_ACCESS_KEY=<IAM USER AWS SECRET ACCESS KEY>
   export OSB_REGION=<YOUR REGION>
   export OSB_SERVICE=es
   ```
   {% include copy.html %}

   - 對於 IAM 角色，請設定下列環境變數：

   ```bash
   export OSB_AWS_ACCESS_KEY_ID=<IAM Role AWS ACCESS KEY ID>
   export OSB_AWS_SECRET_ACCESS_KEY=<IAM Role AWS SECRET ACCESS KEY>
   export OSB_AWS_SESSION_TOKEN=<IAM Role SESSION TOKEN>
   export OSB_REGION=<YOUR REGION>
   export OSB_SERVICE=es
   ```
   {% include copy.html %}


3. 自訂並執行下列 `run` 命令，並加上 `--client-options=amazon_aws_log_in:environment` 旗標。此旗標會向 OpenSearch Benchmark 提供您匯出憑證的位置。

   ```bash
   opensearch-benchmark run \
   --target-hosts=<CLUSTER ENDPOINT> \
   --pipeline=benchmark-only \
   --workload=geonames \
   --client-options=timeout:120,amazon_aws_log_in:environment
   ```
   {% include copy.html %}


## Proxy 組態

OpenSearch 會自動為您下載所有必要的 Proxy 資料，包括：

- 當您指定 `--distribution-version=<OPENSEARCH-VERSION>` 時，下載 OpenSearch 發行套件。
- 當您指定 Git 修訂編號（例如 `--revision=1e04b2w`）時，下載 OpenSearch 原始碼。
- 從 [OpenSearch GitHub 儲存庫](https://github.com/opensearch-project/OpenSearch)追蹤的任何中繼資料。

截至 OpenSearch Benchmark 0.5.0 版，僅支援 `http_proxy`。
{: .warning}

您可以使用 `http_proxy` 將 OpenSearch Benchmark 連線至特定 Proxy，並將 Proxy 連線至基準測試工作負載。若要新增 Proxy：


1. 將您的 Proxy URL 新增至 shell 設定檔：

   ```
   export http_proxy=http://proxy.proxy.org:4444/
   ```

2. 載入您的 shell 設定檔，並確認 Proxy URL 設定正確：

   ```
   source ~/.bash_profile ; echo $http_proxy
   ```

3. 使用下列命令設定 Git，使其連線至您的 Proxy。如需詳細資訊，請參閱 [Git 文件](https://git-scm.com/docs/git-config)。

   ```
   git config --global http_proxy $http_proxy
   ```

4. 使用 `git clone`，透過下列命令複製工作負載儲存庫。如果 Proxy 設定正確，複製就會成功。

   ```
   git clone http://github.com/opensearch-project/opensearch-benchmark-workloads.git
   ```

5. 最後，檢查 `/.benchmark/logs/benchmark.log` 記錄檔，確認 OpenSearch Benchmark 可以連線至 Proxy 伺服器。當 OpenSearch Benchmark 啟動時，您應該會在記錄檔頂端看到下列內容：

    ```
    Connecting via proxy URL [http://proxy.proxy.org:4444/] to the Internet (picked up from the environment variable [http_proxy]).
    ```

## 記錄

您可以在 `~/.benchmark/logging.json` 檔案中設定 OpenSearch Benchmark 的記錄檔。如需進一步瞭解如何設定記錄檔格式，請參閱下列 Python 文件：

- 如需一般提示與技巧，請參閱 [Python 記錄實用指南](https://docs.python.org/3/howto/logging-cookbook.html)。
- 如需檔案格式，請參閱 Python 的[記錄組態結構描述](https://docs.python.org/3/library/logging.config.html#logging-config-dictschema)。
- 如需自訂記錄輸出寫入位置的指示，請參閱[記錄處理常式文件](https://docs.python.org/3/library/logging.handlers.html)。

依預設，OpenSearch Benchmark 會將所有輸出記錄至 `~/.benchmark/logs/benchmark.log`。







