---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: OpenSearch 
parent: Sinks
grand_parent: Pipelines
nav_order: 50
---

# OpenSearch sink

您可以使用 `opensearch` sink 外掛程式將資料傳送至 OpenSearch 叢集、舊版 Elasticsearch 叢集或 Amazon OpenSearch Service 網域。

此外掛程式支援 OpenSearch 1.0 及更新版本，以及 Elasticsearch 7.3 及更新版本。

## 使用方式

若要設定 `opensearch` sink，請在管線組態中指定 `opensearch` 選項：

```yaml
pipeline:
  ...
  sink:
    opensearch:
      hosts: ["https://localhost:9200"]
      cert: path/to/cert
      username: YOUR_USERNAME
      password: YOUR_PASSWORD
      index_type: trace-analytics-raw
      dlq_file: /your/local/dlq-file
      max_retries: 20
      bulk_size: 4
```

若要設定 [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) sink，請將網域端點指定為 `hosts` 選項，如下列範例所示：

```yaml
pipeline:
  ...
  sink:
    opensearch:
      hosts: ["https://your-amazon-opensearch-service-endpoint"]
      aws_sigv4: true
      cert: path/to/cert
      insecure: false
      index_type: trace-analytics-service-map
      bulk_size: 4
```

## 組態選項

下表說明您可以為 `opensearch` sink 設定的選項。

選項 | 必要 | 類型 | 說明
:--- | :--- |:---| :---
`hosts` | 是 | 清單 | 要寫入的 OpenSearch 主機清單，例如 `["https://localhost:9200", "https://remote-cluster:9200"]`。
`cert` | 否 | 字串 | 安全性憑證的路徑。例如，若叢集使用 OpenSearch Security 外掛程式，則為 `"config/root-ca.pem"`。
`username` | 否 | 字串  | HTTP 基本驗證的使用者名稱。
`password` | 否 | 字串 | HTTP 基本驗證的密碼。
`aws` | 否 | AWS  | [AWS](#aws) 組態。 
[max_retries](#configure-max_retries) | 否 | 整數 | `opensearch` sink 在視為失敗之前，應嘗試將資料推送至 OpenSearch 伺服器的次數上限。預設為 `Integer.MAX_VALUE`。若未提供，sink 會持續嘗試將資料推送至 OpenSearch 伺服器，且指數退避會增加重試前的等待時間。
`aws_sigv4` | 否 | 布林值 | **在 Data Prepper 2.7 中已棄用。** 預設為 `false`。是否使用 AWS Identity and Access Management (IAM) 簽章來連線至 Amazon OpenSearch Service 網域。針對您的存取金鑰、私密金鑰及選用的工作階段權杖，OpenSearch Data Prepper 會使用預設憑證鏈（環境變數、Java 系統屬性、`~/.aws/credential`）。 
`aws_region` | 否 | 字串 | **在 Data Prepper 2.7 中已棄用。** 當您連線至 Amazon OpenSearch Service 時，網域的 AWS 區域（例如 `"us-east-1"`）。
`aws_sts_role_arn` | 否 | 字串 | **在 Data Prepper 2.7 中已棄用。** 此外掛程式用來簽署傳送至 Amazon OpenSearch Service 之請求的 IAM 角色。若未提供此資訊，此外掛程式會使用預設憑證。
`socket_timeout` | 否 | 整數 | 等待資料傳回時的逾時值（毫秒）（兩個連續資料封包之間的最長閒置期間）。逾時值 `0` 會解譯為無限逾時。若此逾時值為負數或未設定，則基礎 Apache HttpClient 會依賴作業系統設定來管理通訊端逾時。
`connect_timeout` | 否 | 整數| 從連線管理員要求連線時的逾時值（毫秒）。逾時值 `0` 會解譯為無限逾時。若此逾時值為負數或未設定，則基礎 Apache HttpClient 會依賴作業系統設定來管理連線逾時。
`insecure` | 否 | 布林值  | 是否驗證 SSL 憑證。若設為 `true`，則會停用憑證授權單位 (CA) 憑證驗證，並改為傳送不安全的 HTTP 請求。預設為 `false`。
`proxy` | 否 | 字串 | [轉送 HTTP Proxy 伺服器](https://en.wikipedia.org/wiki/Proxy_server) 的位址。格式為 `"&lt;hostname or IP&gt;:&lt;port&gt;"`（例如 `"example.com:8100"`、`"http://example.com:8100"`、`"112.112.112.112:8100"`）。連接埠號不能省略。
`index` | 有條件 | 字串 | 匯出索引的名稱。僅當 `index_type` 為 `custom` 時才需要。索引可以是純字串，例如 `my-index-name`；包含 [Java 日期時間模式](https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html)，例如 `my-index-%{yyyy.MM.dd}` 或 `my-%{yyyy-MM-dd-HH}-index`；使用欄位值格式化，例如 `my-index-${/my_field}`；或使用 [Data Prepper 運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)，例如 `my-index-${getMetadata(\"my_metadata_field\"}`。所有格式化選項皆可合併使用，以便在建立靜態、動態及輪替索引時提供彈性。 
`index_type` | 否 | 字串 | 指定 sink 外掛程式處理的資料類型。有效值包括 `custom`、`trace-analytics-raw`、`trace-analytics-plain-raw`、`trace-analytics-service-map`、`log-analytics`、`log-analytics-plain`、`metric-analytics`、`metric-analytics-plain` 及 `management-disabled`。<br><br>若要從 `otel_logs_source` 搭配 `output_format: otel` 產生符合 Amazon Security Lake 規範的資料，請將 `index_type` 設為 `log-analytics-plain`。<br>若為 `otel_metrics_source` 搭配 `output_format: otel`，請將 `index_type` 設為 `metric-analytics-plain`。<br>若為 `otel_trace_source` 搭配 `output_format: otel`，請將 `index_type` 設為 `trace-analytics-plain-raw`。<br><br>預設為 `custom`。


`template_type` | 否 | 字串 | 定義要使用的 OpenSearch 範本類型。可用選項為 `v1` 和 `index-template`。預設值為 `v1`，使用 `_template` API 端點提供的原始 OpenSearch 範本。`index-template` 選項使用可組合的[索引範本]({{site.url}}{{site.baseurl}}/opensearch/index-templates/)，可透過 OpenSearch `_index_template` API 取得。可組合的索引類型比預設類型更具彈性，且當 OpenSearch 叢集包含既有索引範本時，必須使用這些類型。所有版本的 OpenSearch 及部分較新版本的 Elasticsearch 都提供可組合範本。當 `distribution_version` 設為 `es6` 時，Data Prepper 會強制將 `template_type` 設為 `v1`。
`template_file` | 否 | 字串 | 當 `index_type` 設為 `custom` 時，JSON [索引範本]({{site.url}}{{site.baseurl}}/opensearch/index-templates/)檔案的路徑，例如 `/your/local/template-file.json`。如需範本檔案的範例，請參閱 [otel-v1-apm-span-index-template.json](https://github.com/opensearch-project/data-prepper/blob/main/data-prepper-plugins/opensearch/src/main/resources/otel-v1-apm-span-index-template.json)。如果您提供範本檔案，該檔案必須符合 `template_type` 參數指定的範本格式。
`template_content` | 否 | JSON | 包含索引  [索引範本]({{site.url}}{{site.baseurl}}/opensearch/index-templates/)內的所有內嵌 JSON。如需範本內容的範例，請參閱[範本內容範例](#example_template_content)。
`document_id_field` | 否 | 字串 | **已於 Data Prepper 2.7 中棄用，改用 `document_id`。** 當 `index_type` 為 `custom` 時，來源資料中用作 OpenSearch 文件 ID 的欄位（例如 `"my-field"`）。
`document_id` | 否 | 字串 | 用作 OpenSearch 文件中 `_id` 的格式字串。若要指定事件中的單一欄位，請使用 `${/my_field}`。您也可以使用 Data Prepper 運算式來建構 `document_id`，例如 `${getMetadata(\"some_metadata_key\")}`。這些選項可以組合成更複雜的格式，例如 `${/my_field}-test-${getMetadata(\"some_metadata_key\")}`。 
`document_version` | 否 | 字串  |  用作 OpenSearch 文件中 `_version` 的格式字串。若要指定事件中的單一欄位，請使用 `${/my_field}`。您也可以使用 Data Prepper 運算式來建構 `document_version`，例如 `${getMetadata(\"some_metadata_key\")}`。這些選項可以組合成更複雜的版本，例如 `${/my_field}${getMetadata(\"some_metadata_key\")}`。`document_version` 格式的求值結果必須為 long 類型，而且只能在 `document_version_type` 設為 `external` 或 `external_gte` 時使用。
`document_version_type` | 否 | 字串  | 編製索引作業的文件版本類型。必須為 `external`、`external_gte` 或 `internal` 其中之一。如果設為 `external` 或 `external_gte`，則必須提供 `document_version`。
`dlq_file` | 否 | 字串 | 您偏好的死信佇列檔案路徑（例如 `/your/local/dlq-file`）。當 Data Prepper 無法在 OpenSearch 叢集上將文件編製索引時，會寫入此檔案。
`dlq` | 否 | 不適用 | [DLQ 組態]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/dlq/)。 
`bulk_size` | 否 | 整數（long） | 傳送至 OpenSearch 叢集的批次請求大小上限（以 MiB 為單位）。低於 `0` 的值表示大小不受限制。如果單一文件超過批次請求大小上限，Data Prepper 會個別傳送每個請求。預設值為 `5`。
`ism_policy_file` | 否 | 字串 | Index State Management（ISM）政策 JSON 檔案的絕對檔案路徑。此政策檔案僅在索引類型沒有內建政策檔案時生效。例如，`custom` 索引類型目前是唯一沒有內建政策檔案的類型，因此，如果透過此參數提供政策檔案，就會使用該檔案。如需政策 JSON 檔案的詳細資訊，請參閱 [ISM 政策]({{site.url}}{{site.baseurl}}/im-plugin/ism/policies/)。
`number_of_shards` | 否 | 整數  | 索引在目的地 OpenSearch 伺服器上應具有的主要分片數。此參數僅在 sink 組態中明確提供 `template_file` 或其為內建時生效。如果設定此參數，便會覆寫索引範本檔案中的值。如需詳細資訊，請參閱[建立索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/)。
`number_of_replicas` | 否 | 整數 | 每個主要分片在目的地 OpenSearch 伺服器上應具有的副本分片數。例如，如果您有 4 個主要分片，並將 `number_of_replicas` 設為 `3`，則索引會有 12 個副本分片。此參數僅在 sink 組態中明確提供 `template_file` 或其為內建時生效。如果設定此參數，便會覆寫索引範本檔案中的值。如需詳細資訊，請參閱[建立索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/)。
`distribution_version` | 否 | 字串  | 指出 sink 的後端版本是 Elasticsearch 6 還是更新版本。`es6` 代表 Elasticsearch 6。`default` 代表最新的相容後端版本，例如 Elasticsearch 7.x、OpenSearch 1.x 或 OpenSearch 2.x。預設為 `default`。
`enable_request_compression` | 否 | 布林值 | 是否在向 OpenSearch 傳送請求時啟用壓縮。當 `distribution_version` 設為 `es6` 時，預設為 `false`。對於所有其他發行版本，預設為 `true`。
`action` | 否 | 字串 | 要用於文件的 OpenSearch 批次動作。必須為 `create`、`index`、`update`、`upsert` 或 `delete` 其中之一。預設為 `index`。
`actions` | 否 | 清單 | 可用來替代 `action` 的[動作清單](#actions)，其運作方式如同 switch case 陳述式，依條件決定要對事件執行的批次動作。 
`flush_timeout` | 否 | Long | 一個 long 類別，包含在排清請求之前，嘗試將批次請求填滿至 `bulk_size` 的時間長度，以毫秒為單位。如果此逾時期限在批次請求達到 `bulk_size` 之前到期，便會排清請求。設為 `-1` 可停用排清逾時，改為在每個批次結束時排清當時已有的所有內容。預設為 `60,000`，即 1 分鐘。
`normalize_index` | 否 | 布林值 | 如果為 true，OpenSearch sink 會嘗試建立動態索引名稱。在 `${})` 中指定格式選項的索引名稱，依據[索引命名限制]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/#index-naming-restrictions)為有效名稱。任何無效字元都會移除。預設值為 `false`。
`routing` | 否 | 字串 | 將文件儲存至 OpenSearch 時，用作雜湊以產生文件 `shard_id` 的字串。會搜尋每筆傳入的記錄。若存在此字串，便會將其用作文件的路由欄位。若不存在，OpenSearch 會在儲存文件時使用預設路由機制（`document_id`）。支援使用事件中的欄位和 [Data Prepper 運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)進行格式化，例如 `${/my_field}-test-${getMetadata(\"some_metadata_key\")}`。
`document_root_key` | 否 | 字串  | 事件中將用作文件根的鍵。預設為事件的根。如果該鍵不存在，則會將整個事件寫入為文件。如果 `document_root_key` 是基本值類型，例如字串或整數，則文件的結構將為 `{"data": <value of the document_root_key>}`。
`serverless` | 否 | 布林值 | **已於 Data Prepper 2.7 中棄用。請改為搭配 `aws` 組態使用此選項。** 決定 OpenSearch 後端是否為 Amazon OpenSearch Serverless。當 `opensearch` sink 的目的地為 Amazon OpenSearch Serverless 集合時，請將此值設為 `true`。預設為 `false`。
`serverless_options` | 否 | 物件 | **已於 Data Prepper 2.7 中棄用。請改為搭配 `aws` 組態使用此選項。** 當 `opensearch` sink 的後端設為 Amazon OpenSearch Serverless 時，可用的網路組態選項。如需詳細資訊，請參閱 [Serverless 選項](#serverless-options)。
`query_lookup` | 否 | 物件 | 在編製索引之前查詢既有文件，以避免重複文件的組態。如需詳細資訊，請參閱[查詢查找](#query-lookup)。


## 查詢查找

`query_lookup` 組態會在為新文件編製索引之前，先查詢 OpenSearch 中已有的文件，以啟用去重功能。此功能可在兩種情境下協助避免重複：

1. **條件式查詢**：在為文件編製索引之前，先根據條件查詢文件。
2. **錯誤導向查詢**：當大量操作發生可能導致部分成功的錯誤（例如 socket 逾時或 500 內部伺服器錯誤）時，查詢文件。

### 查詢查找選項

`query_lookup` 物件支援下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`query_when` | 否 | 字串 | 一個 [Data Prepper 運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)，用於決定哪些文件在編製索引前符合查詢條件。例如，`getMetadata("potential_duplicate") == true` 只會查詢該中繼資料欄位設定為 `true` 的文件。
`query_term` | 是 | 字串 | 文件的唯一欄位，將用於查詢 OpenSearch 中已有的文件。這通常是一個 ID 欄位。
`query_on_bulk_errors` | 否 | 布林值 | 設定為 `true` 時，遇到可復原的大量操作錯誤（例如 socket 逾時或 500 錯誤）的文件會先進行查詢，而不是立即重試。這有助於在初始索引請求可能已部分成功的情況下避免重複。預設值為 `false`。
`query_duration` | 否 | 期間 | 在為指定文件編製索引之前查詢該文件的時間長度。使用 ISO 8601 期間格式，例如 `PT5M` 表示 5 分鐘。預設值為 `PT5M`。
`async_limit` | 否 | 整數 | 在阻擋處理器工作執行緒之前，可同時查詢的最大文件數。預設值為 `5000`。

### 查詢查找範例

下列範例組態會在編製索引之前查詢具有 `potential_duplicate` 中繼資料欄位的文件：

```yaml
pipeline:
  ...
  sink:
    opensearch:
      hosts: ["https://localhost:9200"]
      username: YOUR_USERNAME
      password: YOUR_PASSWORD
      index: my-index
      query_lookup:
        query_when: 'getMetadata("potential_duplicate") == true'
        query_term: 'document_id'
        query_on_bulk_errors: true
        query_duration: PT5M
        async_limit: 5000
```

在此組態中：
- 中繼資料 `potential_duplicate` 設定為 `true` 的文件會在編製索引前先進行查詢。
- `document_id` 欄位會用作查詢時的唯一識別碼。
- 如果大量操作遇到 socket 逾時或 500 錯誤等錯誤，受影響的文件會先進行查詢，而不是立即重試。
- 文件在編製索引之前最多會被查詢 5 分鐘。
- 最多可同時查詢 5,000 份文件。

如果文件已存在於 OpenSearch 中，該文件將被捨棄並釋放事件控制碼，以避免重複。

<!-- vale off -->
## aws
<!-- vale on -->

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`region` | 否 | 字串 | 用於憑證的 AWS 區域。預設採用[判斷區域的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/region-selection.html)。
`sts_role_arn` | 否 | 字串 | 對 Amazon SQS 和 Amazon S3 發出請求時所擔任的 AWS Security Token Service (AWS STS) 角色。預設值為 `null`，將採用[憑證的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。
`sts_header_overrides` | 否 | 對應 | IAM 角色為此 sink 外掛程式所擔任時的標頭覆寫對應。
`sts_external_id` | 否 | 字串 | 要附加至來自 AWS STS 之 AssumeRole 請求的外部 ID。
`serverless` | 否 | 布林值 | 決定 OpenSearch 後端是否為 Amazon OpenSearch Serverless。當 `opensearch` sink 的目的地是 Amazon OpenSearch Serverless 集合時，請將此值設定為 `true`。預設值為 `false`。
`serverless_options` | 否 | 物件 | 當 `opensearch` sink 的後端設定為 Amazon OpenSearch Serverless 時可用的網路組態選項。如需更多資訊，請參閱 [Serverless 選項](#serverless-options)。

<!-- vale off -->
## actions
<!-- vale on -->

下列選項可在 `actions` 選項內使用。

選項 | 必要 | 類型 | 說明
:--- |:---| :--- | :---
`type` | 是 | 字串 | 當 `when` 條件評估為 true 時要使用的大量操作類型。必須是 `create`、`index`、`update`、`upsert` 或 `delete`。
`when` | 否 | 字串 | 一個 [Data Prepper 運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)，用於條件式評估是否使用 `type` 中設定的大量操作將事件傳送至 OpenSearch。留空時，會在事件傳送至 OpenSearch 時自動選擇大量操作。


## Serverless 選項

下列選項可在 `serverless_options` 物件中使用。

選項 | 必要 | 類型 | 說明
:--- | :--- | :---| :---
`network_policy_name` | 是 | 字串 | 要建立的網路政策名稱。
`collection_name` | 是 | 字串 | 要設定的 Amazon OpenSearch Serverless 集合名稱。
`vpce_id` | 是 | 字串 | 來源所連線的虛擬私人雲端 (VPC) 端點。

### 設定 max_retries

您可以在管線組態中加入 `max_retries` 選項，以控制來源以指數退避方式嘗試寫入 sink 的次數。若未加入此選項，管線將無限期重試。

如果您指定了 `max_retries`，且管線已設定[死信佇列 (DLQ)]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/dlq/)，管線會持續嘗試寫入 sink，直到達到最大重試次數，屆時便會開始將失敗的資料傳送至 DLQ。

如果您未指定 `max_retries`，只有被 sink 拒絕的資料會寫入 DLQ。管線會繼續嘗試將所有其他資料寫入 sink。

### 使用確認時的錯誤處理

當管線啟用了[端對端確認]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/#end-to-end-acknowledgments)時，錯誤處理由兩個關鍵組態控制：
* [死信佇列 (DLQ)]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/dlq/)
* [`max_retries`](#configure-max_retries)

#### DLQ 組態（強烈建議）

OpenSearch sink 只會在下列情況下確認事件：
* 成功傳送至 OpenSearch。
* 成功傳送至 DLQ。

若未設定 DLQ：
* 失敗的事件將保持未確認狀態。
* 來源必須自行處理重試。
* 對於不可重試的錯誤，可能導致無限重複處理的風險。

#### 範例：啟用確認的 S3 來源

請考慮一個啟用了確認的 [S3 來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/s3/)：

**沒有 DLQ 時**：
* 單一失敗事件會導致整個 S3 物件無法確認。
* 整個 S3 物件需要重新處理。
* 不可重試的錯誤可能導致無限重複處理（「毒丸」）。

**有 `max_retries` 但沒有 DLQ 時**：
* 達到 `max_retries` 仍會導致無法確認。
* 導致整個 S3 物件被不必要地重新處理。

**最佳實務**---在使用確認時務必設定 DLQ，以便：
* 避免無限重複處理。
* 妥善處理不可重試的錯誤。
* 將不必要的重新處理降至最低。

## OpenSearch 叢集安全性

若要使用 `opensearch` sink 外掛程式將資料傳送至 OpenSearch 叢集，您必須在管線組態中指定您的使用者名稱與密碼。下列範例 `pipelines.yaml` 檔案示範如何指定管理員安全性憑證：

```yaml
sink:
  - opensearch:
      username: "admin"
      password: "admin"
      ...
```

或者，您也可以不使用管理員憑證，改為指定對應至具有下列各節所列最低權限角色之使用者的憑證。

### 叢集權限

- `cluster_all`
- `indices:admin/template/get`
- `indices:admin/template/put`

如果目標是 OpenSearch 資料串流，資料串流偵測器需要下列權限：

- `indices:admin/data_stream/get`

### 索引權限

- 索引：`otel-v1*`；索引權限：`indices_all`
- 索引：`.opendistro-ism-config`；索引權限：`indices_all`
- 索引：`*`；索引權限：`manage_aliases`

如需如何將使用者對應至角色的操作說明，請參閱[將使用者對應至角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/#mapping-users-to-roles)。

## Amazon OpenSearch Service 網域安全性

`opensearch` sink 外掛程式可將資料傳送至使用 IAM 進行安全性的 [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) 網域。此外掛程式使用預設憑證鏈。請使用 [AWS Command Line Interface (AWS CLI)](https://aws.amazon.com/cli/) 執行 `aws configure` 來設定您的憑證。

請確認您設定的憑證具有必要的 IAM 權限。下列網域存取原則示範最低必要權限：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<AccountId>:user/data-prepper-user"
      },
      "Action": "es:ESHttp*",
      "Resource": [
        "arn:aws:es:us-east-1:<AccountId>:domain/<domain-name>/otel-v1*",
        "arn:aws:es:us-east-1:<AccountId>:domain/<domain-name>/_template/otel-v1*",
        "arn:aws:es:us-east-1:<AccountId>:domain/<domain-name>/_plugins/_ism/policies/raw-span-policy",
        "arn:aws:es:us-east-1:<AccountId>:domain/<domain-name>/_alias/otel-v1*",
        "arn:aws:es:us-east-1:<AccountId>:domain/<domain-name>/_alias/_bulk"
      ]
    },
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<AccountId>:user/data-prepper-user"
      },
      "Action": "es:ESHttpGet",
      "Resource": "arn:aws:es:us-east-1:<AccountId>:domain/<domain-name>/_cluster/settings"
    }
  ]
}
```

如需如何設定網域存取原則的操作說明，請參閱 Amazon OpenSearch Service 文件中的[資源型原則
](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ac.html#ac-types-resource)。

### 精細存取控制

如果您的 OpenSearch Service 網域使用[精細存取控制](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html)，則 `opensearch` sink 外掛程式需要一些額外的組態。

#### 以 IAM ARN 作為主使用者

如果您使用 IAM Amazon Resource Name (ARN) 作為主使用者，請在 sink 組態中加入 `aws_sigv4` 選項：

```yaml
...
sink:
    opensearch:
      hosts: ["https://your-fgac-amazon-opensearch-service-endpoint"]
      aws_sigv4: true
```

請使用 AWS CLI 執行 `aws configure` 來使用主 IAM 使用者憑證。如果您不想使用主使用者，可以使用 `aws_sts_role_arn` 選項指定不同的 IAM 角色。此外掛程式接著會使用此角色來簽署傳送至網域 sink 的請求。您指定的 ARN 必須包含在[網域存取原則]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sinks/opensearch/#amazon-opensearch-service-domain-security)中。

#### 內部使用者資料庫中的主使用者

如果您的網域使用內部使用者資料庫中的主使用者，請指定主使用者名稱與密碼，以及 `aws_sigv4` 選項：

```yaml
sink:
    opensearch:
      hosts: ["https://your-fgac-amazon-opensearch-service-endpoint"]
      username: "master-username"
      password: "master-password"
```

如需更多資訊，請參閱 Amazon OpenSearch Service 文件中的[建議組態](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html#fgac-recommendations)。

***注意***：您可以建立具有 `all_access` 權限的新 IAM 角色或內部使用者資料庫使用者，並使用它來取代主使用者。

## OpenSearch Serverless 集合安全性

`opensearch` sink 外掛程式可將資料傳送至 [Amazon OpenSearch Serverless](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html) 集合。

OpenSearch Serverless 集合 sink 有下列限制：

- 您無法寫入使用虛擬私有雲端 (VPC) 存取的集合。此集合必須可從公用網路存取。
- OTel trace group processor 目前不支援集合 sink。

### 建立管線角色

首先，建立管線為了寫入集合而將擔任的 IAM 角色。此角色必須具有下列最低權限：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "aoss:BatchGetCollection"
            ],
            "Resource": "*"
        }
    ]
}
```

此角色必須具有下列信任關係，以允許管線擔任該角色：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<AccountId>:root"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

### 建立集合

接著，建立具有下列設定的集合：

- 對 OpenSearch 端點與 OpenSearch Dashboards 的公用[網路存取](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-network.html)。
- 下列[資料存取原則](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-data-access.html)，其會將必要權限授予管線角色：

  ```json
  [
   {
      "Rules":[
         {
            "Resource":[
               "index/collection-name/*"
            ],
            "Permission":[
               "aoss:CreateIndex",
               "aoss:UpdateIndex",
               "aoss:DescribeIndex",
               "aoss:WriteDocument"
            ],
            "ResourceType":"index"
         }
      ],
      "Principal":[
         "arn:aws:iam::<AccountId>:role/PipelineRole"
      ],
      "Description":"Pipeline role access"
   }
  ]
  ```

  ***重要***：請務必將 `Principal` 元素中的 ARN 取代為您在前述步驟中建立之管線角色的 ARN。

  如需如何建立集合的操作說明，請參閱 Amazon OpenSearch Service 文件中的[建立集合](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-manage.html#serverless-create)。

### 建立管線

在您的 `pipelines.yaml` 檔案中，將 OpenSearch Serverless 集合端點指定為 `hosts` 選項。此外，您必須將 `serverless` 選項設為 `true`。在 `sts_role_arn` 選項中指定管線角色：

```yaml
log-pipeline:
  source:
    http:
  processor:
    - date:
        from_time_received: true
        destination: "@timestamp"
  sink:
    - opensearch:
        hosts: [ "https://<serverless-public-collection-endpoint>" ]
        index: "my-serverless-index"
        aws:
          serverless: true
          sts_role_arn: "arn:aws:iam::<AccountId>:role/PipelineRole"
          region: "us-east-1"
```

### 使用 template_content 和 actions 的範例 <a id="example_template_content"></a>

下列範例管線同時包含 `template_content` 和一份附帶條件的 `actions` 清單：

```yaml
log-pipeline:
  source:
    http:
  processor:
    - date:
        from_time_received: true
        destination: "@timestamp"
  sink:
    - opensearch:
        hosts: [ "https://<serverless-public-collection-endpoint>" ]
        index: "my-serverless-index"
        template_type: index-template
        template_content: >
          {
            "template" : {
              "mappings" : {
                "properties" : {
                  "Data" : {
                    "type" : "binary"
                  },
                  "EncodedColors" : {
                    "type" : "binary"
                  },
                  "Type" : {
                    "type" : "keyword"
                  },
                  "LargeDouble" : {
                    "type" : "double"
                  }          
                }
              }
            }
          }
        # index is the default case  
        actions:
         - type: "delete"
           when: '/operation == "delete"'
         - type: "update"
           when: '/operation == "update"'
         - type: "index"
        aws:
          sts_role_arn: "arn:aws:iam::<AccountId>:role/PipelineRole"
          region: "us-east-1"
```
