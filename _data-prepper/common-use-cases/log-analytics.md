---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "記錄檔分析"
parent: Common use cases
nav_order: 30
---

# 記錄檔分析

OpenSearch Data Prepper 是一套可擴充、可設定且可調整規模的解決方案，可將記錄檔匯入 OpenSearch 和 Amazon OpenSearch Service。Data Prepper 支援透過 [HTTP 來源](https://github.com/opensearch-project/data-prepper/blob/main/data-prepper-plugins/http-source/README.md) 接收來自 [Fluent Bit](https://fluentbit.io/) 的記錄檔，並使用 [Grok 處理器](https://github.com/opensearch-project/data-prepper/blob/main/data-prepper-plugins/grok-processor/README.md) 處理這些記錄檔，再透過 [OpenSearch 接收端](https://github.com/opensearch-project/data-prepper/blob/main/data-prepper-plugins/opensearch/README.md) 將其匯入 OpenSearch。

下圖顯示使用 Fluent Bit、Data Prepper 和 OpenSearch 進行記錄檔分析所用的所有元件。

![記錄檔分析元件]({{site.url}}{{site.baseurl}}/images/data-prepper/log-analytics/log-analytics-components.jpg)

在應用程式環境中執行 Fluent Bit。您可以透過 Kubernetes、Docker 或 Amazon Elastic Container Service（Amazon ECS）將 Fluent Bit 容器化。您也可以在 Amazon Elastic Compute Cloud（Amazon EC2）上將 Fluent Bit 作為代理程式執行。設定 [Fluent Bit HTTP 輸出外掛程式](https://docs.fluentbit.io/manual/pipeline/outputs/http)，將記錄資料匯出至 Data Prepper。接著，將 Data Prepper 部署為中介元件，並設定它將擴充後的記錄資料傳送至您的 OpenSearch 叢集。然後，使用 OpenSearch Dashboards 進行更深入的視覺化與分析。 

## 記錄檔分析管線 

Data Prepper 中的記錄檔分析管線具有極高的自訂彈性。下圖顯示一個簡單的管線。 

![記錄檔分析元件]({{site.url}}{{site.baseurl}}/images/data-prepper/log-analytics/log-ingestion-pipeline.jpg)

### HTTP 來源

[HTTP 來源](https://github.com/opensearch-project/data-prepper/blob/main/data-prepper-plugins/http-source/README.md) 接受來自 Fluent Bit 的記錄資料。此來源接受 JSON 陣列格式的記錄資料，並支援符合業界標準的 TLS/HTTPS 加密與 HTTP 基本驗證。

### 處理器

Data Prepper 1.2 及更新版本隨附 [Grok 處理器](https://github.com/opensearch-project/data-prepper/blob/main/data-prepper-plugins/grok-processor/README.md)。Grok 處理器是將記錄檔結構化並從中擷取重要欄位的實用工具，可讓記錄檔更容易查詢。

Grok 處理器隨附多種[預設模式](https://github.com/thekrakken/java-grok/blob/master/src/main/resources/patterns/patterns)，可比對 Apache 記錄檔或 syslog 等常見記錄檔格式，也能輕鬆接受符合您特定記錄檔格式的任何自訂模式。

如需 Grok 功能的詳細資訊，請參閱文件。

### 接收端

有一個通用接收端可將資料寫入作為目的地的 OpenSearch。[OpenSearch 接收端](https://github.com/opensearch-project/data-prepper/blob/main/data-prepper-plugins/opensearch/README.md) 提供與 OpenSearch 叢集相關的組態選項，例如端點、SSL/使用者名稱、索引名稱、索引範本和索引狀態管理。

## 管線組態

以下各節說明管線組態。

### 啟用 SSL 和基本驗證的管線範例

此管線組態範例已為 `http-source` 啟用 SSL 和基本驗證：

```yaml
log-pipeline:
  source:
    http:
      ssl_certificate_file: "/full/path/to/certfile.crt"
      ssl_key_file: "/full/path/to/keyfile.key"
      authentication:
        http_basic:
          username: "myuser"
          password: "mys3cret"
  processor:
    - grok:
        match:
          # This will match logs with a "log" key against the COMMONAPACHELOG pattern (ex: { "log": "actual apache log..." } )
          # You should change this to match what your logs look like. See the grok documenation to get started.
          log: [ "%{COMMONAPACHELOG}" ]
  sink:
    - opensearch:
        hosts: [ "https://localhost:9200" ]
        # Change to your credentials
        username: "admin"
        password: "admin"
        # Add a certificate file if you are accessing an OpenSearch cluster with a self-signed certificate
        #cert: /path/to/cert
        # If you are connecting to an Amazon OpenSearch Service domain without
        # Fine-Grained Access Control, enable these settings. Comment out the
        # username and password above.
        #aws_sigv4: true
        #aws_region: us-east-1
        # Since we are grok matching for apache logs, it makes sense to send them to an OpenSearch index named apache_logs.
        # You should change this to correspond with how your OpenSearch indexes are set up.
        index: apache_logs
```
{% include copy.html %}

此管線組態是匯入 Apache 記錄檔的範例。別忘了，您可以輕鬆設定 Grok 處理器來處理自己的自訂記錄檔。您需要針對您的 OpenSearch 叢集修改組態。

您需要進行的主要變更如下：

* `hosts` – 設定為您的主機。
* `index` – 將此項變更為您要傳送記錄檔的 OpenSearch 索引。
* `username` – 提供您的 OpenSearch 使用者名稱。
* `password` – 提供您的 OpenSearch 密碼。
* `aws_sigv4` – 如果您使用採用 AWS 簽署的 Amazon OpenSearch Service，請將此項設為 true。它會使用預設的 AWS 憑證提供者簽署請求。
* `aws_region` – 如果您使用採用 AWS 簽署的 Amazon OpenSearch Service，請將此值設為託管您叢集的 AWS 區域。

## Fluent Bit

您需要在服務環境中執行 Fluent Bit。如需安裝指示，請參閱 [Fluent Bit 入門](https://docs.fluentbit.io/manual/installation/getting-started-with-fluent-bit)。請確保您可以將 [Fluent Bit HTTP 輸出外掛程式](https://docs.fluentbit.io/manual/pipeline/outputs/http) 設定為連接您的 Data Prepper HTTP 來源。以下是 `fluent-bit.conf` 範例，它會持續讀取名為 `test.log` 的記錄檔尾端，並將其轉送至在本機執行的 Data Prepper HTTP 來源；此來源預設在連接埠 2021 上執行。 

請注意，您應根據 Fluent Bit 和 Data Prepper 的執行方式與位置，調整檔案 `path`、輸出 `Host` 和 `Port`。

### 範例：未啟用 SSL 和基本驗證的 Fluent Bit 檔案

以下是 HTTP 來源未啟用 SSL 和基本驗證的 `fluent-bit.conf` 檔案範例：

```text
[INPUT]
  name                  tail
  refresh_interval      5
  path                  test.log
  read_from_head        true

[OUTPUT]
  Name http
  Match *
  Host localhost
  Port 2021
  URI /log/ingest
  Format json
```
{% include copy.html %}

如果您的 HTTP 來源已啟用 SSL 和基本驗證，您需要將 `http_User`、`http_Passwd`、`tls.crt_file` 和 `tls.key_file` 的詳細資訊新增至 `fluent-bit.conf` 檔案，如下列範例所示。

### 範例：啟用 SSL 和基本驗證的 Fluent Bit 檔案

以下是 HTTP 來源已啟用 SSL 和基本驗證的 `fluent-bit.conf` 檔案範例：

```text
[INPUT]
  name                  tail
  refresh_interval      5
  path                  test.log
  read_from_head        true

[OUTPUT]
  Name http
  Match *
  Host localhost
  http_User myuser
  http_Passwd mys3cret
  tls On
  tls.crt_file /full/path/to/certfile.crt
  tls.key_file /full/path/to/keyfile.key
  Port 2021
  URI /log/ingest
  Format json
```
{% include copy.html %}

# 後續步驟

請參閱 [Data Prepper 記錄檔匯入示範指南](https://github.com/opensearch-project/data-prepper/blob/main/examples/log-ingestion/README.md)，了解從透過 Docker 執行的 `FluentBit -> Data Prepper -> OpenSearch` 匯入 Apache 記錄檔的具體範例。

未來，Data Prepper 將提供更多來源和處理器，讓您能使用更複雜的記錄檔分析管線。請查看 [Data Prepper 專案路線圖](https://github.com/orgs/opensearch-project/projects/221)，了解即將推出的功能。

如果您想在記錄檔分析工作流程中納入某個特定來源、處理器或接收端，但目前的路線圖尚未包含它，請建立 GitHub 議題。此外，如果您有興趣為 Data Prepper 貢獻，請參閱我們的[貢獻指南](https://github.com/opensearch-project/data-prepper/blob/main/CONTRIBUTING.md)、[開發人員指南](https://github.com/opensearch-project/data-prepper/blob/main/docs/developer_guide.md)及[外掛程式開發指南](https://github.com/opensearch-project/data-prepper/blob/main/docs/plugin_development.md)。
