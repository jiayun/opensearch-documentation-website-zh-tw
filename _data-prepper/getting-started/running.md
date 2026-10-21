---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "執行 Data Prepper"
parent: Getting started
nav_order: 20
---

# 執行 Data Prepper

OpenSearch Data Prepper 至少需要一條管線才能啟動。如果 Data Prepper 找不到任何管線組態檔案，它會記錄下列錯誤並結束：

```text
ERROR org.opensearch.dataprepper.pipeline.parser.PipelineConfigurationFileReader - Pipelines configuration file not found at /usr/share/data-prepper/pipelines
```

在本頁中，您將定義一條最簡的管線、啟動 Data Prepper，並向它傳送一個測試事件。如果您尚未安裝 Data Prepper，請參閱[安裝 Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/getting-started/installing/)。如需管線組態的更多資訊，請參閱[設定管線]({{site.url}}{{site.baseurl}}/data-prepper/getting-started/configuring-pipelines/)。

## 步驟 1：定義管線

建立一個名為 `pipelines.yaml` 的檔案，內容為下列管線組態：

```yaml
test-pipeline:
  source:
    http:
      ssl: false
  sink:
    - stdout:
```
{% include copy.html %}

這條名為 `test-pipeline` 的管線，會透過連接埠 `2021` 上的 [`http`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/http/) 來源接收事件，並使用 [`stdout`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sinks/stdout/) 接收端將每個事件列印到 Data Prepper 記錄檔。此管線不含任何處理器，因此事件不會被修改。

## 步驟 2：啟動 Data Prepper

使用 Docker 映像或 Linux 壓縮檔啟動 Data Prepper。

### Docker

在包含 `pipelines.yaml` 的目錄中，執行下列命令：

```bash
docker run --name data-prepper \
  -p 2021:2021 -p 4900:4900 \
  -v ${PWD}/pipelines.yaml:/usr/share/data-prepper/pipelines/pipelines.yaml \
  opensearchproject/data-prepper:latest
```
{% include copy.html %}

`-v` 選項會將 `pipelines.yaml` 掛載到容器的 `pipelines` 目錄。`${PWD}` 是您目前的目錄，因此 `${PWD}/pipelines.yaml` 是該檔案的絕對路徑，這是 Docker 掛載所需的格式。`-p` 選項會發布連接埠 `2021` 給 `http` 來源，以及連接埠 `4900` 給[核心 API]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/core-apis/)。

若要使用您自己的伺服器組態檔案，請將它掛載為 `/usr/share/data-prepper/config/data-prepper-config.yaml`：

```bash
docker run --name data-prepper \
  -p 2021:2021 -p 4900:4900 \
  -v ${PWD}/pipelines.yaml:/usr/share/data-prepper/pipelines/pipelines.yaml \
  -v ${PWD}/data-prepper-config.yaml:/usr/share/data-prepper/config/data-prepper-config.yaml \
  opensearchproject/data-prepper:latest
```
{% include copy.html %}

### Linux 壓縮檔

將 `pipelines.yaml` 複製到 Data Prepper 主目錄的 `pipelines` 目錄中。然後從主目錄執行下列命令：

```bash
bin/data-prepper
```
{% include copy.html %}

或者，依序以管線組態檔案和伺服器組態檔案作為引數提供：

```bash
bin/data-prepper /path/to/pipelines.yaml /path/to/data-prepper-config.yaml
```
{% include copy.html %}

## 步驟 3：傳送測試事件

當管線就緒時，Data Prepper 記錄檔會包含下列一行：

```text
INFO  org.opensearch.dataprepper.plugins.source.loghttp.HTTPSource - Started http source on port 2021...
```

在新的終端機視窗中，向 `http` 來源傳送一個事件。該來源接受 JSON 陣列，其中每個物件都會成為一個事件：

```bash
curl -X POST http://localhost:2021/log/ingest \
  -H "Content-Type: application/json" \
  -d '[{"message": "Hello, Data Prepper!"}]'
```
{% include copy.html %}

Data Prepper 會回應 `200 OK`，而 `stdout` 接收端會將事件列印到 Data Prepper 記錄檔：

```json
{"message":"Hello, Data Prepper!"}
```

## 步驟 4：列出執行中的管線

若要列出執行中的管線，請向核心 API 傳送請求。請求方式取決於您安裝的[預設伺服器組態]({{site.url}}{{site.baseurl}}/data-prepper/getting-started/installing/#server-configuration)。

若使用 Docker 映像，請使用 `https` 與預設認證資訊。`-k` 選項會略過憑證驗證，因為該映像使用自我簽署憑證：

```bash
curl -k -u admin:admin https://localhost:4900/list
```
{% include copy.html %}

若使用 Linux 壓縮檔，請使用 `http`：

```bash
curl http://localhost:4900/list
```
{% include copy.html %}

回應會包含您定義的管線：

```json
{"pipelines":[{"name":"test-pipeline"}]}
```

## 步驟 5：停止 Data Prepper

若要停止 Data Prepper，請在 Data Prepper 執行所在的終端機中按下 `Ctrl+C`。如果您是在背景啟動 Docker 容器，請執行 `docker stop data-prepper`。

或者，向核心 API 傳送關機請求。若使用 Docker 映像，請傳送下列請求：

```bash
curl -k -u admin:admin -X POST https://localhost:4900/shutdown
```
{% include copy.html %}

若使用 Linux 壓縮檔，請傳送下列請求：

```bash
curl -X POST http://localhost:4900/shutdown
```
{% include copy.html %}

若要移除已停止的 Docker 容器以便重複使用 `data-prepper` 容器名稱，請執行 `docker rm data-prepper`。

## 執行讀寫檔案的管線

[設定管線]({{site.url}}{{site.baseurl}}/data-prepper/getting-started/configuring-pipelines/)中以檔案為基礎的範例會從 `/usr/share/data-prepper/data` 目錄讀取資料，並將資料寫入該目錄。若要執行這些範例，請建立一個包含 `input.txt` 檔案的 `data` 目錄。

在 Docker 中，將 `data` 目錄連同管線檔案一起掛載到容器中：

```bash
docker run --name data-prepper \
  -v ${PWD}/pipelines.yaml:/usr/share/data-prepper/pipelines/pipelines.yaml \
  -v ${PWD}/data:/usr/share/data-prepper/data \
  opensearchproject/data-prepper:latest
```
{% include copy.html %}

Data Prepper 會將處理後的事件寫入 `data/output.txt`。

若使用 Linux 壓縮檔，請將管線中的 `path` 值替換為主機上輸入與輸出檔案的絕對路徑。

## 執行多條管線

Data Prepper 會載入 `pipelines` 目錄中的每個 YAML 檔案，且每個檔案可以定義一或多條管線。如需更多資訊，請參閱[多條管線]({{site.url}}{{site.baseurl}}/data-prepper/getting-started/configuring-pipelines/#multiple-pipelines)。若要在 Docker 中執行來自多個檔案的管線，請掛載一個目錄而非單一檔案：

```bash
docker run --name data-prepper \
  -p 2021:2021 -p 4900:4900 \
  -v ${PWD}/pipelines:/usr/share/data-prepper/pipelines \
  opensearchproject/data-prepper:latest
```
{% include copy.html %}

## 更新管線

Data Prepper 只會在啟動時讀取管線組態檔案。在您編輯、新增或刪除管線組態檔案之後，請重新啟動 Data Prepper 以套用變更。

## 後續步驟

- [將記錄資料匯入 OpenSearch]({{site.url}}{{site.baseurl}}/data-prepper/getting-started/ingesting-log-data/)：建立一條管線，解析原始 Apache 存取記錄並將其寫入 OpenSearch。
