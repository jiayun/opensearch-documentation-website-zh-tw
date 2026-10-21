---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "安裝與設定 Data Prepper"
parent: Getting started
nav_order: 10
---

# 安裝與設定 Data Prepper

您可以使用 Docker 映像檔或 Linux 封存檔來安裝 OpenSearch Data Prepper。若要從原始碼建置 Data Prepper，請參閱 [Data Prepper 開發人員指南](https://github.com/opensearch-project/data-prepper/blob/main/docs/developer_guide.md)。

## 安裝 Docker 映像檔

若要在 Docker 中使用 Data Prepper，請安裝 [Docker](https://docs.docker.com/get-docker/) 並拉取 Data Prepper 映像檔：

```bash
docker pull opensearchproject/data-prepper:latest
```
{% include copy.html %}

映像檔中的 Data Prepper 主目錄為 `/usr/share/data-prepper`。若要提供組態檔案，請在啟動容器時將這些檔案掛載到該目錄。如需詳細資訊，請參閱[執行 Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/getting-started/running/)。

## 安裝 Linux 封存檔

從 [OpenSearch 下載頁面](https://opensearch.org/downloads/){:target='\_blank'}下載適用於您平台的 Data Prepper 封存檔。每個版本都提供下列封存檔：

- `opensearch-data-prepper-jdk-<version>-linux-<architecture>.tar.gz`：包含 Java 執行環境。
- `opensearch-data-prepper-<version>-linux-<architecture>.tar.gz`：不包含 Java 執行環境。若要使用此封存檔，請在主機上安裝 Java。

解壓縮封存檔，並將 `<version>` 和 `<architecture>` 替換為檔案名稱中的值：

```bash
tar -xzf opensearch-data-prepper-jdk-<version>-linux-<architecture>.tar.gz
```
{% include copy.html %}

解壓縮後的目錄即為 Data Prepper 主目錄。

## 目錄結構

Data Prepper 主目錄包含下列檔案與目錄。

| 路徑 | 說明 |
| :--- | :--- |
| `bin/data-prepper` | 啟動 Data Prepper 的指令碼。 |
| `pipelines/` | 管線組態檔案的目錄。Data Prepper 會載入此目錄中的每個 YAML 檔案。安裝後，此目錄中沒有任何管線。 |
| `config/data-prepper-config.yaml` | Data Prepper 伺服器組態檔案。 |
| `config/log4j2-rolling.properties` | Log4j 2 記錄組態檔案。 |
| `lib/` | Data Prepper 程式庫與外掛程式。 |

## 伺服器與記錄組態

Data Prepper 也會從 Data Prepper 主目錄的 `config` 目錄讀取下列選用組態檔案。

### 伺服器組態

`config/data-prepper-config.yaml` 檔案會設定 Data Prepper 伺服器，該伺服器會在連接埠 `4900` 上公開[核心 API]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/core-apis/)。Docker 映像檔與 Linux 封存檔包含不同的預設伺服器組態。

| 設定 | Docker 映像檔 | Linux 封存檔 |
| :--- | :--- | :--- |
| TLS | 已啟用，使用自我簽署憑證。使用 `https` 傳送請求。 | 已停用。使用 `http` 傳送請求。 |
| 驗證 | 使用使用者名稱 `admin` 與密碼 `admin` 的 HTTP 基本驗證。 | 無。 |

Docker 映像檔中的預設憑證與認證資訊僅供測試使用。在生產環境中使用 Data Prepper 之前，請先替換這些內容。
{: .warning}

若要變更這些設定，請以您自己的檔案取代 `config/data-prepper-config.yaml`。例如，下列檔案會停用核心 API 的 TLS：

```yaml
ssl: false
serverPort: 4900
```
{% include copy.html %}

如需所有伺服器設定，請參閱[設定 OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/configuring-data-prepper/)。

### 記錄組態

Data Prepper 會從 `config/log4j2-rolling.properties` 讀取其記錄組態。若要自訂記錄，請取代此檔案，或將 `JAVA_OPTS` 環境變數設為指向其他檔案：

```bash
export JAVA_OPTS="-Dlog4j.configurationFile=/path/to/log4j2.properties"
```
{% include copy.html %}

如需詳細資訊，請參閱[設定 Log4j]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/configuring-log4j/)。

## 後續步驟

- 為 Data Prepper [設定管線]({{site.url}}{{site.baseurl}}/data-prepper/getting-started/configuring-pipelines/)以執行。
