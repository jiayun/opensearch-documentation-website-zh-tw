---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "gRPC API"
has_children: true
has_toc: false
nav_order: 140
description: "OpenSearch gRPC API 的參考資料，包含使用 protocol buffers 進行高效能通訊的 bulk 與 k-NN 搜尋操作。"
redirect_from:
  - /api-reference/grpc-apis/
---

# gRPC API
**於 3.0 版推出**
{: .label .label-purple }

**Bulk 與 k-NN 搜尋於 3.2 版正式推出**
{: .label .label-green }

gRPC [Bulk API]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/bulk/) 與 [k-NN 搜尋查詢]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/knn/)已正式推出。這些功能使用 [protobuf 1.2.0 版](https://github.com/opensearch-project/opensearch-protobufs/releases/tag/1.2.0)。不過，隨著此功能在後續版本中逐漸成熟，protobuf 結構預期會有所更新。其他 gRPC 搜尋功能仍為實驗性，不建議用於正式環境。如需這些功能的進度更新或提供意見回饋，請參閱相關的 [GitHub issue](https://github.com/opensearch-project/OpenSearch/issues/16787)。
{: .note}

OpenSearch gRPC 功能提供另一種高效能的傳輸層，使用 [gRPC](https://grpc.io/) 與 OpenSearch 通訊。它在 gRPC 上使用 protocol buffers，以降低額外負擔並加快序列化。根據初步的基準測試結果，這可降低額外負擔、加快序列化，並改善請求端的延遲。如需詳細資訊，請參閱[效能優勢](#grpc-performance-benefits)。

## 支援的 API

支援下列 gRPC API：
- [Bulk]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/bulk/) **於 3.2 版正式推出**
- [k-NN]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/knn/) **於 3.2 版正式推出**
- [Search]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/search/)（適用於特定查詢類型）
- [Predict Model Stream]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/predict-model-stream/)
- [Execute Agent Stream]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/execute-agent-stream/)

## 如何使用 gRPC API

若要使用 gRPC API，請依照下列步驟操作：
1. 設定必要的 [gRPC 設定](#grpc-settings)以啟用 gRPC 傳輸。

2. 若要提交 gRPC 請求，您必須在用戶端備有一組 protobuf。您可以透過下列方式取得 protobuf。

| 語言 | 發佈方式 | 操作說明 |
| :------- | :------------------ | :----------- |
| Java | Maven Central 儲存庫 | 從 [Maven Central 儲存庫](https://repo1.maven.org/maven2/org/opensearch/protobufs/1.2.0)下載 `opensearch-protobufs` jar。 |
| Python | PyPI 儲存庫 | 從 [PyPI 儲存庫](https://pypi.org/project/opensearch-protobufs/1.2.0)下載 `opensearch-protobufs` 套件。 |
| 其他語言 | GitHub 儲存庫（原始 protobuf） | 從 [OpenSearch Protobufs GitHub 儲存庫（v1.2.0）](https://github.com/opensearch-project/opensearch-protobufs/releases/tag/1.2.0)下載原始 protobuf 結構描述。接著您可以使用 protocol buffer 編譯器為[支援的語言](https://grpc.io/docs/languages/)產生用戶端程式碼。 |


## gRPC 設定

`transport-grpc` 模組預設隨 OpenSearch 安裝一併包含。若要啟用它，請將下列設定新增至 `opensearch.yml`：

```yaml
aux.transport.types: [transport-grpc]
aux.transport.transport-grpc.port: '9400-9500' // optional
```
{% include copy.html %}

或者，使用下列設定來設定安全的傳輸協定：

```yaml
aux.transport.types: [secure-transport-grpc]
aux.transport.transport-grpc.port: '9400-9500' // optional
```
{% include copy.html %}

視需要設定其他設定（請參閱[進階 gRPC 設定](#advanced-grpc-settings)）：

```yaml
grpc.host: localhost
grpc.publish_host: 10.74.124.163
grpc.bind_host: 0.0.0.0
```
{% include copy.html %}

### 進階 gRPC 設定

OpenSearch 支援下列用於 gRPC 通訊的進階設定。這些設定可在 `opensearch.yml` 中設定。

| 設定名稱 | 說明 | 範例值 | 預設值 |
| :---- | :---- | :---- | :---- |
| `grpc.publish_port` | 此節點用來向對等節點發佈自身以供 gRPC 傳輸使用的外部連接埠號。 | `9400` | `-1`（已停用） |
| `grpc.host` | gRPC 伺服器將繫結的位址清單。 | `["0.0.0.0"]` | `[]` |
| `grpc.bind_host` | 要將 gRPC 伺服器繫結的位址清單。可與發佈主機不同。 | `["0.0.0.0", "::"]` | `grpc.host` 的值 |
| `grpc.publish_host` | 向對等節點發佈以供用戶端連線的主機名稱或 IP 清單。 | `["thisnode.example.com"]` | `grpc.host` 的值 |
| `grpc.netty.worker_count` | gRPC 伺服器的 Netty 工作執行緒數目。控制並行與平行處理。 | `2` | 處理器數目 |
| `grpc.netty.executor_count` | 用於處理 gRPC 服務呼叫的 fork-join 集區中的執行緒數目。控制請求處理的平行程度。 | `32` | `2 * number of processors` |
| `grpc.netty.max_concurrent_connection_calls` | 每個用戶端連線允許同時進行中的請求數上限。 | `200` | `100` |
| `grpc.netty.max_connection_age` | 連線在被正常關閉前可達到的最長存續時間。支援如 `ms`、`s` 或 `m` 等時間單位。請參閱[時間單位]({{site.url}}{{site.baseurl}}/api-reference/units/#time-units)。 | `500ms` | 未設定（無限制） |
| `grpc.netty.max_connection_idle` | 連線在被關閉前可閒置的最長時間。支援如 `ms`、`s` 或 `m` 等時間單位。請參閱[時間單位]({{site.url}}{{site.baseurl}}/api-reference/units/#time-units)。 | `2m` | 未設定（無限制） |
| `grpc.netty.keepalive_timeout` | 在關閉連線前等待 `keepalive` ping 確認的時間長度。支援[時間單位]({{site.url}}{{site.baseurl}}/api-reference/units/#time-units)。 | `1s` | 未設定 |
| `grpc.netty.max_msg_size` | gRPC 請求的傳入訊息大小上限。支援如 `b`、`kb`、`mb` 或 `gb` 等單位。請參閱[支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。 | `10mb` 或 `10485760` | `10mb` |

### 範例組態

以下是在 `opensearch.yml` 中完整 gRPC 組態的範例：

```yaml
# Basic gRPC transport configuration
aux.transport.types: [transport-grpc]
aux.transport.transport-grpc.port: '9400-9500'

# Advanced gRPC settings
grpc.host: ["0.0.0.0"]
grpc.bind_host: ["0.0.0.0", "::"]
grpc.publish_host: ["thisnode.example.com"]
grpc.publish_port: 9400
grpc.netty.worker_count: 4
grpc.netty.max_concurrent_connection_calls: 200
grpc.netty.max_connection_age: 500ms
grpc.netty.max_connection_idle: 2m
grpc.netty.keepalive_timeout: 1s
grpc.netty.max_msg_size: 10mb
```
{% include copy.html %}

這些設定類似於 [HTTP 網路設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/network-settings/#advanced-http-settings)，但專門適用於 gRPC 通訊。


## gRPC 效能優勢

使用 gRPC API 相較於 HTTP API 提供多項優點：

- **降低延遲**：二進位 protocol buffers 可免除 JSON 剖析的額外負擔。
- **更高輸送量**：為高頻率查詢提供更有效率的網路使用率。
- **更低 CPU 使用率**：降低序列化與還原序列化的成本。
- **型別安全**：protocol buffer 結構描述提供編譯期驗證。
- **更小的承載大小**：二進位編碼可減少網路流量。

### 額外的效能提示
將文件編製索引為支援的二進位格式（例如 SMILE）時，通常會比以 JSON 格式編製索引／搜尋時產生更低的延遲。編製索引與搜尋的延遲都應會降低。
