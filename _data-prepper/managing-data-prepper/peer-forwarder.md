---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Peer Forwarder
nav_order: 12
parent: Managing OpenSearch Data Prepper
---

# Peer Forwarder

Peer Forwarder 是一種 HTTP 服務，會在 OpenSearch Data Prepper 節點之間對 `event` 執行對等轉送以進行彙總。此 HTTP 服務使用雜湊環（hash-ring）方式來彙總事件，並在重新路由之前判斷給定追蹤應由哪個 Data Prepper 節點處理，然後將其重新路由至該節點。目前，`aggregate`、`service_map` 與 `otel_traces` [處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/processors/) 支援 Peer Forwarder。

Peer Forwarder 會根據支援的處理器所提供的識別鍵來將事件分組。對於 `service_map` 與 `otel_traces`，識別鍵預設為 `traceId` 且無法設定。`aggregate` 處理器則是使用 `identification_keys` 組態選項來設定。您可以在其中指定 Peer Forwarder 要使用哪些鍵。如需識別鍵的更多資訊，請參閱 [Aggregate Processor 頁面](https://github.com/opensearch-project/data-prepper/tree/main/data-prepper-plugins/aggregate-processor#identification_keys)。

對等探索（peer discovery）可讓 Data Prepper 找到它要與之通訊的其他節點。目前，對等探索由靜態清單、DNS 記錄查詢或 AWS Cloud Map 提供。  

## 探索模式

下列各節提供探索模式的相關資訊。

### 靜態

靜態探索模式可讓 Data Prepper 節點使用 IP 位址或網域名稱清單來探索節點。靜態探索模式的範例請參閱下列 YAML 檔案：

```yaml
peer_forwarder:4
  discovery_mode: static
  static_endpoints: ["data-prepper1", "data-prepper2"]
```

### DNS 查詢

在擴充 Data Prepper 叢集時，DNS 探索比靜態探索更為合適。DNS 探索會設定 DNS 供應商，在給定單一網域名稱時傳回 Data Prepper 主機清單。此清單由 [DNS A 記錄](https://www.cloudflare.com/learning/dns/dns-records/dns-a-record/) 以及給定網域的 IP 位址清單組成。DNS 查詢的範例請參閱下列 YAML 檔案：

```yaml
peer_forwarder:
  discovery_mode: dns
  domain_name: "data-prepper-cluster.my-domain.net"
```

### AWS Cloud Map

[AWS Cloud Map](https://docs.aws.amazon.com/cloud-map/latest/dg/what-is-cloud-map.html) 同時提供以 API 為基礎的服務探索以及以 DNS 為基礎的服務探索。

Peer Forwarder 可以使用 AWS Cloud Map 中以 API 為基礎的服務探索。若要支援此功能，您必須已為 API 執行個體探索設定好現有的命名空間。您可以依照 [AWS Cloud Map 文件](https://docs.aws.amazon.com/cloud-map/latest/dg/working-with-namespaces.html) 所提供的指示建立新的命名空間。

您的 Data Prepper 組態必須包含下列項目：
* `aws_cloud_map_namespace_name` – 設定為您的 AWS Cloud Map 命名空間名稱。
* `aws_cloud_map_service_name` – 設定為您指定命名空間內的服務名稱。
* `aws_region` – 設定為您的命名空間所在的 AWS 區域。
* `discovery_mode` – 設定為 `aws_cloud_map`。

您的 Data Prepper 組態可以選擇性包含下列項目：
* `aws_cloud_map_query_parameters` – 鍵值對用於根據附加至執行個體的自訂屬性篩選結果。結果僅包含符合所有指定鍵值對的執行個體。

#### 組態範例

AWS Cloud Map 組態的 YAML 檔案範例請參閱下列內容：

```yaml
peer_forwarder:
  discovery_mode: aws_cloud_map
  aws_cloud_map_namespace_name: "my-namespace"
  aws_cloud_map_service_name: "data-prepper-cluster"
  aws_cloud_map_query_parameters:
    instance_type: "r5.xlarge"
  aws_region: "us-east-1"
```

### 具有必要權限的 IAM 政策

Data Prepper 也必須以必要的權限執行。下列 AWS Identity and Access Management (IAM) 政策顯示必要的權限：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "CloudMapPeerForwarder",
            "Effect": "Allow",
            "Action": "servicediscovery:DiscoverInstances",
            "Resource": "*"
        }
    ]
}
```


## 組態

下表提供選用的組態值。


| 值 | 類型 | 說明 |
| ----  | --- |  ----------- |
| `port` | Integer | 介於 0 與 65535 之間的值，代表 Peer Forwarder 伺服器執行所在的連接埠。預設值為 `4994`。 |
| `request_timeout` | Integer | 代表 Peer Forwarder HTTP 伺服器的請求逾時時間長度（毫秒）。預設值為 `10000`。 |
| `server_thread_count` | Integer | 代表 Peer Forwarder 伺服器使用的執行緒數量。預設值為 `200`。|
| `client_thread_count` | Integer | 代表 Peer Forwarder 用戶端使用的執行緒數量。預設值為 `200`。|
| `maxConnectionCount`  | Integer | 代表 Peer Forwarder 伺服器的最大開啟連線數。預設值為 `500`。 |
| `discovery_mode` | String | 代表要使用的對等探索模式。允許的值為 `local_node`、`static`、`dns` 與 `aws_cloud_map`。預設為 `local_node`，即在本機處理事件。 |
| `static_endpoints` | List | 包含所有 Data Prepper 執行個體的端點。當 `discovery_mode` 設定為 `static` 時為必要。 |
|  `domain_name` | String | 代表要用來查詢 DNS 的單一網域名稱。通常透過為同一網域建立多個 [DNS A 記錄](https://www.cloudflare.com/learning/dns/dns-records/dns-a-record/) 來使用。當 `discovery_mode` 設定為 `dns` 時為必要。 |
| `aws_cloud_map_namespace_name`  | String | 代表使用 AWS Cloud Map 服務探索時的 AWS Cloud Map 命名空間。當 `discovery_mode` 設定為 `aws_cloud_map` 時為必要。  |
| `aws_cloud_map_service_name` | String | 代表使用 AWS Cloud Map 服務探索時的 AWS Cloud Map 服務。當 `discovery_mode` 設定為 `aws_cloud_map` 時為必要。 |
| `aws_cloud_map_query_parameters`  | Map | 鍵值對，用於根據附加至執行個體的自訂屬性篩選結果。僅會傳回符合所有指定鍵值對的執行個體。 |
| `buffer_size` | Integer | 代表緩衝區可接受的最大未檢查記錄數（未檢查記錄數等於寫入緩衝區的記錄數加上仍在處理中且尚未由 Checkpointing API 檢查的記錄數）。預設為 `512`。 |
| `batch_size` |  Integer | 代表緩衝區在讀取時可傳回的最大記錄數。預設為 `48`。 |
| `batch_delay` | Integer | 代表從 Peer Forwarder 緩衝區擷取 `batch_size` 筆記錄的最長時間（毫秒）。如果在此時間內未達到 `batch_size`，則會傳回部分批次。如果設定為 `0`，則會立即傳回最多 `batch_size` 筆的所有可用記錄。如果緩衝區為空，則會封鎖最多 5 毫秒以等待記錄。預設為 `3000`。 |
|  `aws_region` |  String | 代表使用 `ACM`、`Amazon S3` 或 `AWS Cloud Map` 的 AWS 區域，並在符合下列任一條件時為必要：<br> - `use_acm_certificate_for_ssl` 設定已設為 `true`。 <br> - `ssl_certificate_file` 或 `ssl_key_file` 指定了 Amazon Simple Storage Service (Amazon S3) URI（例如 s3://mybucket/path/to/public.cert）。<br> - `discovery_mode` 已設為 `aws_cloud_map`。 |
| `drain_timeout`  | Duration | 代表 Peer Forwarder 在關機前等待完成資料處理的時間長度。 |
| `forwarding_batch_size` | Integer | 代表在每次對對等節點的請求中要傳送的最大記錄數。預設為 `1500`。最大值為 `15000`。 |
| `forwarding_batch_queue_depth` | Integer | 代表批次處理佇列的深度。此值為一個純量，用於決定在將記錄傳送至對等節點之前，用於批次處理記錄的鏈結封鎖佇列的大小。佇列大小由公式 `workers * forwarding_batch_size * forwarding_batch_queue_depth` 決定。預設為 `1`。 |
| `forwarding_batch_timeout` | Duration | 代表將批次排清至對等節點之間可發生的最長時間。預設為 `3s`。 |

## SSL 組態

下表提供選用的 SSL 組態值，可讓您為 Peer Forwarder 用戶端設定信任管理員，以便連線至其他 Data Prepper 執行個體。

| 值 | 類型 | 說明 |
| ----- | ---- | ----------- |
| `ssl` | Boolean | 啟用 TLS/SSL。預設值為 `true`。 |
| `ssl_certificate_file`| String | 代表 SSL 憑證鏈檔案路徑或 Amazon S3 路徑。以下為 Amazon S3 路徑的範例：`s3://<bucketName>/<path>`。預設為預設憑證檔案 `config/default_certificate.pem`。如需憑證產生方式的詳細資訊，請參閱[預設憑證](https://github.com/opensearch-project/data-prepper/tree/main/examples/certificates)。 |
| `ssl_key_file`| String | 代表 SSL 金鑰檔案路徑或 Amazon S3 路徑。Amazon S3 路徑範例：`s3://<bucketName>/<path>`。預設為 `config/default_private_key.pem`，即預設私密金鑰檔案。如需私密金鑰檔案產生方式的詳細資訊，請參閱[預設憑證](https://github.com/opensearch-project/data-prepper/tree/main/examples/certificates)。 |
| `ssl_insecure_disable_verification` | Boolean | 停用伺服器 TLS 憑證鏈的驗證。預設值為 `false`。 |
| `ssl_fingerprint_verification_only` | Boolean | 停用伺服器 TLS 憑證鏈的驗證，改為僅驗證憑證指紋。預設值為 `false`。 |
| `use_acm_certificate_for_ssl` | Boolean | 使用 AWS Certificate Manager (ACM) 的憑證與私密金鑰啟用 TLS/SSL。預設值為 `false`。 |
| `acm_certificate_arn`| String | 代表 ACM 憑證的 Amazon Resource Name (ARN)。ACM 憑證優先於 Amazon S3 或本機檔案系統憑證。若 `use_acm_certificate_for_ssl` 設為 `true` 則為必要。 |
| `acm_private_key_password` | String | 代表將用於解密私密金鑰的 ACM 私密金鑰密碼。若未提供，將產生隨機密碼。 |
| `acm_certificate_timeout_millis` | Integer | 代表 ACM 取得憑證所需的逾時時間 (毫秒)。預設值為 `120000`。 |
| `aws_region` | String | 代表使用 ACM、Amazon S3 或 AWS Cloud Map 的 AWS 區域。若 `use_acm_certificate_for_ssl` 設為 `true` 或 `ssl_certificate_file` 則為必要。當 `ssl_key_file` 設為使用 Amazon S3 路徑，或 `discovery_mode` 設為 `aws_cloud_map` 時亦為必要。 |

#### 範例組態

以下 YAML 檔案提供範例組態：

```yaml
peer_forwarder:
  ssl: true
  ssl_certificate_file: "<cert-file-path>"
  ssl_key_file: "<private-key-file-path>"
```

## 驗證

`Authentication` 為選用，且為啟用雙向 TLS (mTLS) 的 `Map`。其可為 `mutual_tls` 或 `unauthenticated`。預設值為 `unauthenticated`。以下 YAML 檔案提供驗證範例：

```yaml
peer_forwarder:
  authentication:
    mutual_tls:
```

## 指標

Core Peer Forwarder 引進下列自訂指標。所有指標皆以 `core.peerForwarder` 為前置字元。

### 計時器

Peer Forwarder 的計時器功能提供下列資訊：

- `requestForwardingLatency`：測量 Peer Forwarder 用戶端轉送之請求的延遲。
- `requestProcessingLatency`：測量 Peer Forwarder 伺服器處理之請求的延遲。

### 計數器

下表提供計數器指標選項。

| 值 | 說明 |
| ----- | ----------- |
| `requests`| 測量轉送請求的總數。 |
| `requestsFailed`| 測量失敗請求的總數。適用於 HTTP 回應碼非 `200` 的請求。 |
| `requestsSuccessful`|  測量成功請求的總數。適用於 HTTP 回應碼為 `200` 的請求。 |
| `requestsTooLarge`| 測量因過大而無法寫入 Peer Forwarder 緩衝區的請求總數。適用於 HTTP 回應碼為 `413` 的請求。 |
| `requestTimeouts`| 測量將內容寫入 Peer Forwarder 緩衝區時逾時的請求總數。適用於 HTTP 回應碼為 `408` 的請求。 |
| `requestsUnprocessable`| 測量因無法處理的實體而失敗的請求總數。適用於 HTTP 回應碼為 `422` 的請求。 |
| `badRequests`| 測量請求格式錯誤的請求總數。適用於 HTTP 回應碼為 `400` 的請求。 |
| `recordsSuccessfullyForwarded`| 測量成功轉送的記錄總數。 |
| `recordsFailedForwarding`| 測量轉送失敗的記錄總數。 |
| `recordsToBeForwarded` | 測量待轉送的記錄總數。 |
| `recordsToBeProcessedLocally` | 測量待於本機處理的記錄總數。 |
| `recordsActuallyProcessedLocally`| 測量實際於本機處理的記錄總數。此值為 `recordsToBeProcessedLocally` 與 `recordsFailedForwarding` 的總和。 |
| `recordsReceivedFromPeers`| 測量從遠端對等節點接收的記錄總數。 |

### 計量

`peerEndpoints` 測量動態探索到的對等 Data Prepper 端點數量。在 `static` 模式下，大小為固定。
