---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "命令參考"
nav_order: 2
parent: Migration Console
permalink: /classic/migration-assistant/migration-console/migration-console-command-reference/
---

# Migration Console 命令參考

Migration Console 命令遵循以下語法：`console [component] [action]`。其組成元件包括 `clusters`、`backfill`、`snapshot`、`metadata` 和 `replay`。主控台會以已部署服務的註冊資訊，以及來源與目標叢集進行設定，這些資訊由 `cdk.context.json` 值產生。

## 常用命令

實際使用的命令會因使用情境與目標而有很大差異，以下是一系列常見命令及其用途的簡要說明。

### 檢查連線

回報來源與目標叢集是否皆可連線，並提供其版本。

```sh
console clusters connection-check
```
{% include copy.html %}

### 執行 `cat-indices`

在叢集上執行 `cat-indices` API。

```sh
console clusters cat-indices
```
{% include copy.html %}

### 對叢集執行 HTTP 請求

若要直接對已設定的來源或目標叢集呼叫 OpenSearch 或 Elasticsearch API，請使用類似 `curl` 的介面。驗證、TLS 與端點皆取自您的主控台組態。

```sh
console clusters curl <source_cluster|target_cluster> <path> [OPTIONS]
```
{% include copy.html %}

#### 引數

* `<source_cluster|target_cluster>` — 指定要呼叫的 `source_cluster` 或 `target_cluster`。
* `<path>` — 要在叢集上呼叫的 API 端點（例如 `/_cat/indexes` 或 `/my-index/_search`）。

#### 選項

* `--json <JSON_DATA>` — 傳送 JSON 本文並自動設定 `Content-Type: application/json`。
* `-X, --request <METHOD>` — HTTP 方法（`GET`、`POST`、`PUT`、`DELETE` 或 `HEAD`）。預設為 `GET`。
* `-H, --header <HEADER>` — 自訂標頭，例如 `-H 'Accept: application/json'`。您可以指定多個標頭，例如 `-H 'Accept: application/json' -H 'Authorization: Bearer TOKEN'`。
* `-d, --data <DATA>` — 原始請求本文。

#### 範例

*取得叢集健康狀態*：

```sh
console clusters curl source_cluster /_cluster/health
```
{% include copy.html %}

*以 JSON 格式列出索引*：

```sh
console clusters curl source_cluster "/_cat/indexes?format=json&v=true"
```
{% include copy.html %}

*建立索引*：

```sh
console clusters curl target_cluster /my-new-index --json '{"settings":{"number_of_shards":3,"number_of_replicas":1}}'
```
{% include copy.html %}

*執行含本文的查詢*：

```sh
console clusters curl source_cluster /_search --json '{"query":{"match_all":{}}}'
```
{% include copy.html %}


### 建立快照

建立來源叢集的快照，並將其儲存在預先設定的 Amazon Simple Storage Service (Amazon S3) 儲存桶中。

```sh
console snapshot create
```
{% include copy.html %}

### 檢查快照狀態

對快照建立狀態執行詳細檢查，包括預估完成時間：

```sh
console snapshot status --deep-check
```

{% include copy.html %}

### 評估中繼資料

執行中繼資料遷移的試執行，顯示哪些索引、範本及其他物件將被遷移至目標叢集。

```sh
console metadata evaluate
```

{% include copy.html %}

### 遷移中繼資料

將中繼資料從來源叢集遷移至目標叢集。

```sh
console metadata migrate
```

{% include copy.html %}

### 啟動回填

若已啟用 `Reindex-From-Snapshot` (RFS)，此命令會啟動該服務的一個執行個體，開始將文件移動至目標叢集：

另有類似的 `scale UNITS` 與 `stop` 命令，可變更 RFS 的作用中執行個體數量。


```sh
console backfill start
```
{% include copy.html %}

### 檢查回填狀態

取得回填遷移的目前狀態，包括運作中的執行個體數量與分片的進度。

```sh
console backfill status
```
{% include copy.html %}

### 啟動 Traffic Replayer

若已啟用 Traffic Replayer，此命令會啟動一個 Traffic Replayer 執行個體，開始對目標叢集重播流量。
`stop` 命令會停止所有作用中的執行個體。

```sh
console replay start
```
{% include copy.html %}

### 讀取記錄檔

讀取執行 Traffic Replayer 時產生的所有記錄檔。使用路徑的 Tab 鍵自動補全來填入可用的 `NODE_IDs`，以及（若適用）記錄檔案名稱。元組記錄會在達到特定大小門檻時輪替，因此可能會有許多以時間戳記命名的檔案。`jq` 命令會在將元組輸出寫入檔案前，先將每一行格式化輸出。

```sh
console tuples show --in /shared-logs-output/traffic-Replayer-default/[NODE_ID]/tuples/console.log | jq > readable_tuples.json
```
{% include copy.html %}

### 顯示版本

顯示目前安裝的 Migration Assistant 版本。

```sh
console --version
```
{% include copy.html %}

### Help 選項

所有命令與選項都可以在工具本身內探索，方法是使用 `--help` 選項，可用於整個 `console` 應用程式或個別元件（例如 `console backfill --help`）。例如：

```sh
$ console --help
Usage: console [OPTIONS] COMMAND [ARGS]...

Options:
  --config-file TEXT  Path to config file
  --json
  -v, --verbose       Verbosity level. Default is warn, -v is info, -vv is
                      debug.
  --version           Show the Migration Assistant version.
  --help              Show this message and exit.

Commands:
  backfill    Commands related to controlling the configured backfill...
  clusters    Commands to interact with source and target clusters
  completion  Generate shell completion script and instructions for setup.
  kafka       All actions related to Kafka operations
  metadata    Commands related to migrating metadata to the target cluster.
  metrics     Commands related to checking metrics emitted by the capture...
  replay      Commands related to controlling the Replayer.
  snapshot    Commands to create and check status of snapshots of the...
  tuples      All commands related to tuples.
```
