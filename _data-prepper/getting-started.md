---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "OpenSearch Data Prepper 入門"
nav_order: 5
redirect_from:
  - /clients/data-prepper/get-started/
---

# OpenSearch Data Prepper 入門

OpenSearch Data Prepper 是一個獨立元件，而非 OpenSearch 外掛程式，用於轉換資料以供 OpenSearch 使用。它並未包含在 OpenSearch 的一體式安裝套件中。

如果您要從 Open Distro Data Prepper 遷移，請參閱[從 Open Distro 遷移]({{site.url}}{{site.baseurl}}/data-prepper/migrate-open-distro/)。
{: .note}

## 1. 安裝 Data Prepper

安裝 Data Prepper 的方式有兩種：您可以執行 Docker 映像檔，或從原始碼建置。

使用 Data Prepper 最簡單的方式是執行 Docker 映像檔。如果您有可用的 [Docker](https://www.docker.com)，建議您採用此方式。請執行下列命令：

```bash
docker pull opensearchproject/data-prepper:latest
```
{% include copy.html %}

如果您有特殊需求而必須從原始碼建置，或者您想要貢獻，請參閱[開發人員指南](https://github.com/opensearch-project/data-prepper/blob/main/docs/developer_guide.md)。

## 2. 設定 Data Prepper

執行 Data Prepper 執行個體需要兩個組態檔案。您也可以選擇設定 Log4j 2 組態檔案。如需詳細資訊，請參閱[設定 Log4j]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/configuring-log4j/)。下列清單說明每個組態檔案的用途：

* `pipelines.yaml`：此檔案描述要執行哪些資料管線，包括來源、處理器和接收器 (sink)。
* `data-prepper-config.yaml`：此檔案包含 Data Prepper 伺服器設定，可讓您與公開的 Data Prepper 伺服器 API 互動。
* `log4j2-rolling.properties` (選用)：此檔案包含 Log4j 2 組態選項，檔案類型可以是 JSON、YAML、XML 或 .properties。

對於 2.0 之前的 Data Prepper 版本，`.jar` 檔案預期先指定管線組態檔案路徑，再接著指定伺服器組態檔案路徑。請參閱下列組態路徑範例：

```bash
java -jar data-prepper-core-$VERSION.jar pipelines.yaml data-prepper-config.yaml
```
{% include copy.html %}

您也可以選擇在命令中加入 `"-Dlog4j.configurationFile=config/log4j2.properties"`，以傳入自訂的 Log4j 2 組態檔案。如果您未提供 properties 檔案，Data Prepper 會預設使用 `shared-config` 目錄中的 `log4j2.properties` 檔案。


從 Data Prepper 2.0 開始，您可以使用下列 `data-prepper` 指令碼啟動 Data Prepper，不需要任何額外的命令列引數：

```bash
bin/data-prepper
```
{% include copy.html %}

組態檔案會從應用程式主目錄中的特定子目錄讀取：
1. `pipelines/`：用於管線組態。管線組態可以寫在一個或多個 YAML 檔案中。
2. `config/data-prepper-config.yaml`：用於 Data Prepper 伺服器組態。

您可以提供自己的管線組態檔案路徑，再接著提供伺服器組態檔案路徑。不過，未來的版本將不再支援此方法。請參閱下列範例：
```bash
bin/data-prepper pipelines.yaml data-prepper-config.yaml
```
{% include copy.html %}

Log4j 2 組態檔案會從位於應用程式主目錄中的 `config/log4j2.properties` 檔案讀取。

若要設定 Data Prepper，請參閱下列各使用案例的資訊：

* [追蹤分析]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/trace-analytics/)：了解如何收集追蹤資料，並自訂匯入和轉換該資料的管線。
* [記錄檔分析]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/log-analytics/)：了解如何設定 Data Prepper 以實現記錄檔可觀測性。

## 3. 定義管線

使用下列組態建立名為 `pipelines.yaml` 的 Data Prepper 管線檔案：

```yaml
simple-sample-pipeline:
  workers: 2
  delay: "5000"
  source:
    random:
  sink:
    - stdout:
```
{% include copy.html %}

## 4. 執行 Data Prepper

使用您的管線組態 YAML 執行下列命令。

```bash
docker run --name data-prepper \
    -v /${PWD}/pipelines.yaml:/usr/share/data-prepper/pipelines/pipelines.yaml \
    opensearchproject/data-prepper:latest
    
```
{% include copy.html %}

上述管線組態範例示範了一個簡單的管線，由來源 (`random`) 將資料傳送至接收器 (`stdout`)。如需更進階的管線組態範例，請參閱[管線]({{site.url}}{{site.baseurl}}/clients/data-prepper/pipelines/)。

啟動 Data Prepper 後，幾秒鐘內您應該會看到記錄檔輸出和一些 UUID：

```text
2021-09-30T20:19:44,147 [main] INFO  com.amazon.dataprepper.pipeline.server.DataPrepperServer - Data Prepper server running at :4900
2021-09-30T20:19:44,681 [random-source-pool-0] INFO  com.amazon.dataprepper.plugins.source.RandomStringSource - Writing to buffer
2021-09-30T20:19:45,183 [random-source-pool-0] INFO  com.amazon.dataprepper.plugins.source.RandomStringSource - Writing to buffer
2021-09-30T20:19:45,687 [random-source-pool-0] INFO  com.amazon.dataprepper.plugins.source.RandomStringSource - Writing to buffer
2021-09-30T20:19:46,191 [random-source-pool-0] INFO  com.amazon.dataprepper.plugins.source.RandomStringSource - Writing to buffer
2021-09-30T20:19:46,694 [random-source-pool-0] INFO  com.amazon.dataprepper.plugins.source.RandomStringSource - Writing to buffer
2021-09-30T20:19:47,200 [random-source-pool-0] INFO  com.amazon.dataprepper.plugins.source.RandomStringSource - Writing to buffer
2021-09-30T20:19:49,181 [simple-test-pipeline-processor-worker-1-thread-1] INFO  com.amazon.dataprepper.pipeline.ProcessWorker -  simple-test-pipeline Worker: Processing 6 records from buffer
07dc0d37-da2c-447e-a8df-64792095fb72
5ac9b10a-1d21-4306-851a-6fb12f797010
99040c79-e97b-4f1d-a70b-409286f2a671
5319a842-c028-4c17-a613-3ef101bd2bdd
e51e700e-5cab-4f6d-879a-1c3235a77d18
b4ed2d7e-cf9c-4e9d-967c-b18e8af35c90
```
本頁其餘部分提供從 Docker 映像檔執行 Data Prepper 的範例。如果您
是從原始碼建置，請參閱[開發人員指南](https://github.com/opensearch-project/data-prepper/blob/main/docs/developer_guide.md)以取得詳細資訊。

無論您如何設定管線，執行 Data Prepper 的方式都相同。您會執行 Docker
映像檔，並修改 `pipelines.yaml` 和 `data-prepper-config.yaml` 這兩個檔案。

對於 Data Prepper 2.0 或更新版本，請使用此命令：

```bash
docker run --name data-prepper -p 4900:4900 -v ${PWD}/pipelines.yaml:/usr/share/data-prepper/pipelines/pipelines.yaml -v ${PWD}/data-prepper-config.yaml:/usr/share/data-prepper/config/data-prepper-config.yaml opensearchproject/data-prepper:latest
```
{% include copy.html %}

對於 2.0 之前的 Data Prepper 版本，請使用此命令：

```bash
docker run --name data-prepper -p 4900:4900 -v ${PWD}/pipelines.yaml:/usr/share/data-prepper/pipelines.yaml -v ${PWD}/data-prepper-config.yaml:/usr/share/data-prepper/data-prepper-config.yaml opensearchproject/data-prepper:1.x
```
{% include copy.html %}

Data Prepper 執行後，會持續處理資料，直到被關閉為止。完成後，請使用下列命令將其關閉：

```bash
POST /shutdown
```
{% include copy-curl.html %}

### 其他組態

對於 Data Prepper 2.0 或更新版本，Log4j 2 組態檔案會從應用程式主目錄中的 `config/log4j2.properties` 讀取。預設會使用 *shared-config* 目錄中的 `log4j2-rolling.properties`。

對於 Data Prepper 1.5 或更早版本，如果您想傳入自訂的 log4j2 properties 檔案，可以選擇在命令中加入 `"-Dlog4j.configurationFile=config/log4j2.properties"`。如果未提供 properties 檔案，Data Prepper 會預設使用 *shared-config* 目錄中的 log4j2.properties 檔案。

## 後續步驟

追蹤分析是 Data Prepper 的重要使用案例。如果您尚未設定，請參閱[追蹤分析]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/trace-analytics/)。

記錄檔匯入也是 Data Prepper 的重要使用案例。若要深入了解，請參閱[記錄檔分析]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/log-analytics/)。

如需如何監控 Data Prepper 的相關資訊，請參閱[監控]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/monitoring/)。

## 更多範例

如需更多 Data Prepper 範例，請參閱 Data Prepper 儲存庫中的[範例](https://github.com/opensearch-project/data-prepper/tree/main/examples/)。 
