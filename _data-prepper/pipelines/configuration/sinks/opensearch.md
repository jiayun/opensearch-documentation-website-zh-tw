---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: OpenSearch 
parent: Sinks
grand_parent: Pipelines
nav_order: 50
---

# OpenSearch 接收器

您可以使用 `opensearch` 接收器外掛程式將資料傳送至 OpenSearch 叢集、舊版 Elasticsearch 叢集或 Amazon OpenSearch Service 網域。

此外掛程式支援 OpenSearch 1.0 及更新版本，以及 Elasticsearch 7.3 及更新版本。

## 使用方式

若要設定 `opensearch` 接收器，請在管線組態中指定 `opensearch` 選項：

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

若要設定 [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) 接收器，請將網域端點指定為 `hosts` 選項，如下列範例所示：

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

下表說明您可以為 `opensearch` 接收器設定的選項。

選項 | 必要 | 類型 | 說明
:--- | :--- |:---| :---
`hosts` | 是 | 清單 | 要寫入的 OpenSearch 主機清單，例如 `["https://localhost:9200", "https://remote-cluster:9200"]`。
`cert` | 否 | 字串 | 安全性憑證的路徑。例如，若叢集使用 OpenSearch Security 外掛程式，則為 `"config/root-ca.pem"`。
`username` | 否 | 字串  | HTTP 基本驗證的使用者名稱。
`password` | 否 | 字串 | HTTP 基本驗證的密碼。許多 Data Prepper 範例會以 `admin` 使用者進行驗證，並使用 `<custom-admin-password>` 預留位置作為其[密碼]({{site.url}}{{site.baseurl}}/security/configuration/passwords/#admin-password)。您也可以使用僅具備接收器所需權限的使用者進行驗證。如需詳細資訊，請參閱 [OpenSearch 叢集安全性](#opensearch-cluster-security)。
`aws` | 否 | AWS  | [AWS](#aws) 組態。 
[max_retries](#configure-max_retries) | 否 | 整數 | `opensearch` 接收器在視為失敗之前，嘗試將資料推送至 OpenSearch 伺服器的次數上限。預設為 `Integer.MAX_VALUE`。若未提供，接收器會持續嘗試將資料推送至 OpenSearch 伺服器，且指數退避會增加重試前的等待時間。
`aws_sigv4` | 否 | 布林值 | **已於 Data Prepper 2.7 棄用。** 預設為 `false`。是否使用 AWS Identity and Access Management (IAM) 簽署來連線至 Amazon OpenSearch Service 網域。對於您的存取金鑰、私密金鑰及選用的工作階段權杖，OpenSearch Data Prepper 會使用預設認證鏈（環境變數、Java 系統屬性、`~/.aws/credential`）。 
`aws_region` | 否 | 字串 | **已於 Data Prepper 2.7 棄用。** 連線至 Amazon OpenSearch Service 時，網域所在的 AWS 區域（例如 `"us-east-1"`）。
`aws_sts_role_arn` | 否 | 字串 | **已於 Data Prepper 2.7 棄用。** 此外掛程式用來簽署傳送至 Amazon OpenSearch Service 之請求的 IAM 角色。若未提供此資訊，此外掛程式會使用預設認證資訊。
`socket_timeout` | 否 | 整數 | 等待資料傳回時的逾時值（毫秒，即兩個連續資料封包之間的最長閒置期間）。逾時值 `0` 會解譯為無限逾時。若此逾時值為負數或未設定，則基礎的 Apache HttpClient 會依賴作業系統設定來管理通訊端逾時。
`connect_timeout` | 否 | 整數| 從連線管理員請求連線時的逾時值（毫秒）。逾時值 `0` 會解譯為無限逾時。若此逾時值為負數或未設定，則基礎的 Apache HttpClient 會依賴作業系統設定來管理連線逾時。
`insecure` | 否 | 布林值  | 是否驗證 SSL 憑證。若設為 `true`，則會停用憑證授權單位 (CA) 憑證驗證，並改為傳送不安全的 HTTP 請求。預設為 `false`。
`proxy` | 否 | 字串 | [轉送 HTTP 代理伺服器](https://en.wikipedia.org/wiki/Proxy_server)的位址。格式為 `"&lt;hostname or IP&gt;:&lt;port&gt;"`（例如 `"example.com:8100"`、`"http://example.com:8100"`、`"112.112.112.112:8100"`）。連接埠號碼不可省略。
`index` | 視條件而定 | 字串 | 匯出索引的名稱。僅當 `index_type` 為 `custom` 時才需要。索引可以是純字串，例如 `my-index-name`；可包含 [Java 日期時間模式](https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html)，例如 `my-index-%{yyyy.MM.dd}` 或 `my-%{yyyy-MM-dd-HH}-index`；可使用欄位值格式化，例如 `my-index-${/my_field}`；或使用 [Data Prepper 運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)，例如 `my-index-${getMetadata(\"my_metadata_field\"}`。所有格式化選項皆可合併使用，以便在建立靜態、動態及輪替索引時提供彈性。 
`index_type` | 否 | 字串 | 指定接收器外掛程式處理的資料類型。有效值包括 `custom`、`trace-analytics-raw`、`trace-analytics-plain-raw`、`trace-analytics-service-map`、`log-analytics`、`log-analytics-plain`、`metric-analytics`、`metric-analytics-plain` 及 `management-disabled`。<br><br>若要從 `otel_logs_source` 搭配 `output_format: otel` 產生符合 Amazon Security Lake 規範的資料，請將 `index_type` 設為 `log-analytics-plain`。<br>若為 `otel_metrics_source` 搭配 `output_format: otel`，請將 `index_type` 設為 `metric-analytics-plain`。<br>若為 `otel_trace_source` 搭配 `output_format: otel`，請將 `index_type` 設為 `trace-analytics-plain-raw`。<br><br>預設為 `custom`。


`template_type` | 否 | 字串 | 定義要使用的 OpenSearch 範本類型。可用選項為 `v1` 和 `index-template`。預設值為 `v1`，其使用 `_template` API 端點提供的原始 OpenSearch 範本。`index-template` 選項使用可組合的[索引範本]({{site.url}}{{site.baseurl}}/opensearch/index-templates/)，可透過 OpenSearch `_index_template` API 取得。可組合索引類型比預設值提供更大的彈性，且當 OpenSearch 叢集包含現有索引範本時必須使用。可組合範本適用於所有版本的 OpenSearch 及部分較後期的 Elasticsearch 版本。當 `distribution_version` 設為 `es6` 時，Data Prepper 會強制將 `template_type` 設為 `v1`。
`template_file` | 否 | 字串 | 當 `index_type` 設為 `custom` 時，JSON [索引範本]({{site.url}}{{site.baseurl}}/opensearch/index-templates/)檔案的路徑，例如 `/your/local/template-file.json`。如需範本檔案範例，請參閱 [otel-v1-apm-span-index-template.json](https://github.com/opensearch-project/data-prepper/blob/main/data-prepper-plugins/opensearch/src/main/resources/otel-v1-apm-span-index-template.json)。若您提供範本檔案，則其必須符合 `template_type` 參數所指定的範本格式。
`template_content` | 否 | JSON | 包含索引[索引範本]({{site.url}}{{site.baseurl}}/opensearch/index-templates/)內所有內嵌 JSON。如需範本內容範例，請參閱[範本內容範例](#example-with-template_content-and-actions)。
`document_id_field` | 否 | 字串 | **在 Data Prepper 2.7 中已棄用，請改用 `document_id`。** 當 `index_type` 為 `custom` 時，用於 OpenSearch 文件 ID 的來源資料欄位（例如 `"my-field"`）。
`document_id` | 否 | 字串 | 用作 OpenSearch 文件中 `_id` 的格式字串。若要指定事件中的單一欄位，請使用 `${/my_field}`。您也可以使用 Data Prepper 運算式建構 `document_id`，例如 `${getMetadata(\"some_metadata_key\")}`。這些選項可合併為更複雜的格式，例如 `${/my_field}-test-${getMetadata(\"some_metadata_key\")}`。
`document_version` | 否 | 字串  | 用作 OpenSearch 文件中 `_version` 的格式字串。若要指定事件中的單一欄位，請使用 `${/my_field}`。您也可以使用 Data Prepper 運算式建構 `document_version`，例如 `${getMetadata(\"some_metadata_key\")}`。這些選項可合併為更複雜的版本，例如 `${/my_field}${getMetadata(\"some_metadata_key\")}`。`document_version` 格式必須評估為 long 類型，且僅能在 `document_version_type` 設為 `external` 或 `external_gte` 時使用。
`document_version_type` | 否 | 字串  | 索引作業的文件版本類型。必須是 `external`、`external_gte` 或 `internal` 其中之一。若設為 `external` 或 `external_gte`，則需要 `document_version`。
`dlq_file` | 否 | 字串 | 您偏好的死信佇列檔案路徑（例如 `/your/local/dlq-file`）。當 Data Prepper 無法在 OpenSearch 叢集上將文件編製索引時，會寫入此檔案。
`dlq` | 否 | 不適用 | [DLQ 組態]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/dlq/)。
`bulk_size` | 否 | 整數 (long) | 傳送至 OpenSearch 叢集的批次請求大小上限（以 MiB 為單位）。低於 `0` 的值表示大小無限制。若單一文件超過批次請求大小上限，則 Data Prepper 會個別傳送每個請求。預設值為 `5`。
`ism_policy_file` | 否 | 字串 | 索引狀態管理 (ISM) 政策 JSON 檔案的絕對檔案路徑。此政策檔案僅在索引類型沒有內建政策檔案時才有效。例如，`custom` 索引類型目前是唯一沒有內建政策檔案的類型，因此若透過此參數提供，便會使用此政策檔案。如需政策 JSON 檔案的詳細資訊，請參閱 [ISM 政策]({{site.url}}{{site.baseurl}}/im-plugin/ism/policies/)。
`number_of_shards` | 否 | 整數  | 目的地 OpenSearch 伺服器上索引應有的主要分片數。此參數僅在 `template_file` 於接收器組態中明確提供或為內建值時才有效。若設定此參數，則會覆寫索引範本檔案中的值。如需詳細資訊，請參閱[建立索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/)。
`number_of_replicas` | 否 | 整數 | 目的地 OpenSearch 伺服器上每個主要分片應有的副本分片數。例如，若您有 4 個主要分片並將 `number_of_replicas` 設為 `3`，則該索引會有 12 個副本分片。此參數僅在 `template_file` 於接收器組態中明確提供或為內建值時才有效。若設定此參數，則會覆寫索引範本檔案中的值。如需詳細資訊，請參閱[建立索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/)。
`distribution_version` | 否 | 字串  | 指出接收器的後端版本是否為 Elasticsearch 6 或更新版本。`es6` 代表 Elasticsearch 6。`default` 代表最新的相容後端版本，例如 Elasticsearch 7.x、OpenSearch 1.x 或 OpenSearch 2.x。預設為 `default`。
`enable_request_compression` | 否 | 布林值 | 傳送請求至 OpenSearch 時是否啟用壓縮。當 `distribution_version` 設為 `es6` 時，預設為 `false`。對於所有其他後端發行套件版本值，預設為 `true`。
`action` | 否 | 字串 | 用於文件的 OpenSearch 批次動作。必須是 `create`、`index`、`update`、`upsert` 或 `delete` 其中之一。預設為 `index`。
`actions` | 否 | 清單 | [動作清單](#actions)，可作為 `action` 的替代方案，其讀取方式如同 switch case 陳述式，會依條件決定要對事件採取的批次動作。
`flush_timeout` | 否 | 長整數 | 一個 long 類別，包含嘗試將批次請求打包至 `bulk_size` 再排清請求的時間量（以毫秒為單位）。若在批次請求達到 `bulk_size` 之前此逾時已到期，則會排清該請求。設為 `-1` 可停用排清逾時，改為在每個批次結束時排清當下存在的內容。預設為 `60,000`，即 1 分鐘。
`normalize_index` | 否 | 布林值 | 若為 true，則 OpenSearch 接收器會嘗試建立動態索引名稱。在 `${})` 中指定格式選項的索引名稱，依[索引命名限制]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/#index-naming-restrictions)為有效。任何無效字元都會被移除。預設值為 `false`。
`routing` | 否 | 字串 | 當文件儲存於 OpenSearch 時，用於產生該文件 `shard_id` 的雜湊字串。會搜尋每個傳入的記錄。存在時，該字串會用作文件的路由欄位。不存在時，OpenSearch 儲存文件時會使用預設路由機制 (`document_id`)。支援以事件中的欄位及 [Data Prepper 運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)進行格式化，例如 `${/my_field}-test-${getMetadata(\"some_metadata_key\")}`。
`document_root_key` | 否 | 字串  | 事件中將用作文件根層級的鍵。預設為事件的根層級。若該鍵不存在，則會將整個事件寫入為文件。若 `document_root_key` 為基本值類型（例如字串或整數），則文件結構會是 `{"data": <value of the document_root_key>}`。
`serverless` | 否 | 布林值 | **在 Data Prepper 2.7 中已棄用。請改搭配 `aws` 組態使用此選項。** 判斷 OpenSearch 後端是否為 Amazon OpenSearch Serverless。當 `opensearch` 接收器的目的地為 Amazon OpenSearch Serverless 集合時，請將此值設為 `true`。預設為 `false`。
`serverless_options` | 否 | 物件 | **在 Data Prepper 2.7 中已棄用。請改搭配 `aws` 組態使用此選項。** 當 `opensearch` 接收器的後端設為 Amazon OpenSearch Serverless 時可用的網路組態選項。如需詳細資訊，請參閱 [Serverless 選項](#serverless-options)。
`query_lookup` | 否 | 物件 | 在編製索引前查詢現有文件以防止重複的組態。如需詳細資訊，請參閱[查詢查閱](#query-lookup)。


## 查詢查閱

`query_lookup` 組態會在為新文件編製索引之前，先查詢 OpenSearch 中的現有文件，藉此避免產生重複文件。此功能可在以下兩種情況下協助防止重複：

1. **條件式查詢**：在為文件編製索引之前，根據條件查詢文件。
2. **錯誤觸發查詢**：當發生可能導致部分成功的批次作業錯誤（例如通訊端逾時或 500 內部伺服器錯誤）時，查詢文件。

### 查詢查閱選項

`query_lookup` 物件支援以下選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`query_when` | 否 | 字串 | 一個 [Data Prepper 運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)，用於決定哪些文件在編製索引之前符合查詢條件。例如，`getMetadata("potential_duplicate") == true` 只會查詢該中繼資料欄位設為 `true` 的文件。
`query_term` | 是 | 字串 | 文件的唯一欄位，用於在 OpenSearch 中查詢現有文件。此欄位通常是 ID 欄位。
`query_on_bulk_errors` | 否 | 布林值 | 設為 `true` 時，遇到可復原之批次作業錯誤（例如通訊端逾時或 500 錯誤）的文件會改為進行查詢，而不是立即重試。當初次編製索引請求可能已部分成功時，這有助於防止重複。預設值為 `false`。
`query_duration` | 否 | 持續時間 | 在為指定文件編製索引之前，對其進行查詢的時間長度。請使用 ISO 8601 持續時間格式，例如 `PT5M` 代表 5 分鐘。預設值為 `PT5M`。
`async_limit` | 否 | 整數 | 在封鎖處理器工作執行緒之前，可同時查詢的文件數量上限。預設值為 `5000`。

### 查詢查閱範例

以下範例組態會在編製索引之前，查詢具有 `potential_duplicate` 中繼資料欄位的文件：

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
- `potential_duplicate` 中繼資料設為 `true` 的文件會在編製索引之前進行查詢。
- `document_id` 欄位會作為查詢用的唯一識別碼。
- 如果批次作業遇到通訊端逾時或 500 錯誤等錯誤，受影響的文件會改為進行查詢，而不是立即重試。
- 文件在編製索引之前最多會查詢 5 分鐘。
- 最多可同時查詢 5,000 份文件。

如果文件已存在於 OpenSearch 中，該文件會被捨棄，並釋放事件控制碼，從而防止重複。

<!-- vale off -->
## aws
<!-- vale on -->

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`region` | 否 | 字串 | 用於認證資訊的 AWS 區域。預設使用[標準 SDK 行為來決定區域](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/region-selection.html)。
`sts_role_arn` | 否 | 字串 | 對 Amazon SQS 和 Amazon S3 發出請求時要擔任的 AWS Security Token Service (AWS STS) 角色。預設為 `null`，將使用[標準 SDK 認證資訊行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。
`sts_header_overrides` | 否 | 對應表 | 接收器外掛程式在擔任 IAM 角色時套用的標頭覆寫對應表。
`sts_external_id` | 否 | 字串 | 要附加至 AWS STS 之 AssumeRole 請求的外部 ID。
`serverless` | 否 | 布林值 | 決定 OpenSearch 後端是否為 Amazon OpenSearch Serverless。當 `opensearch` 接收器的目的地是 Amazon OpenSearch Serverless 集合時，請將此值設為 `true`。預設值為 `false`。
`serverless_options` | 否 | 物件 | 當 `opensearch` 接收器的後端設為 Amazon OpenSearch Serverless 時可用的網路組態選項。如需詳細資訊，請參閱 [Serverless 選項](#serverless-options)。

<!-- vale off -->
## actions
<!-- vale on -->

以下選項可在 `actions` 選項內使用。

選項 | 必要 | 類型 | 說明
:--- |:---| :--- | :---
`type` | 是 | 字串 | 當 `when` 條件評估為 true 時要使用的批次動作類型。必須是 `create`、`index`、`update`、`upsert` 或 `delete` 其中之一。
`when` | 否 | 字串 | 一個 [Data Prepper 運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)，用於有條件地評估是否要使用 `type` 中設定的批次動作將事件傳送至 OpenSearch。若為空，則在事件傳送至 OpenSearch 時會自動選擇批次動作。


## Serverless 選項

以下選項可在 `serverless_options` 物件中使用。

選項 | 必要 | 類型 | 說明
:--- | :--- | :---| :---
`network_policy_name` | 是 | 字串 | 要建立的網路政策名稱。
`collection_name` | 是 | 字串 | 要設定的 Amazon OpenSearch Serverless 集合名稱。
`vpce_id` | 是 | 字串 | 來源所連線的虛擬私有雲端 (VPC) 端點。

### 設定 max_retries

您可以在管線組態中加入 `max_retries` 選項，以控制來源使用指數退避嘗試寫入接收器的次數。如果您未加入此選項，管線會無限次持續重試。 

如果您指定了 `max_retries`，且管線已設定[死信佇列 (DLQ)]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/dlq/)，管線會持續嘗試寫入接收器，直到達到重試次數上限為止，屆時便開始將失敗的資料傳送至 DLQ。

如果您未指定 `max_retries`，只有被接收器拒絕的資料會寫入 DLQ。管線會繼續嘗試將其他所有資料寫入接收器。

### 搭配確認機制的錯誤處理

當管線啟用[端對端確認]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/#end-to-end-acknowledgments)時，錯誤處理由兩項關鍵組態控制：
* [死信佇列 (DLQ)]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/dlq/)
* [`max_retries`](#configure-max_retries)

#### DLQ 組態（強烈建議）

OpenSearch 接收器只會在以下情況下確認事件：
* 成功傳送至 OpenSearch。
* 成功傳送至 DLQ。

未設定 DLQ 時：
* 失敗的事件會維持未確認狀態。
* 來源必須自行處理重試。
* 對於無法重試的錯誤，有無限次重新處理的風險。

#### 範例：啟用確認機制的 S3 來源

假設有一個啟用確認機制的 [S3 來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/s3/)：

**未設定 DLQ**：
* 單一失敗事件就會導致整個 S3 物件無法確認。
* 整個 S3 物件都需要重新處理。
* 無法重試的錯誤可能導致無限次重新處理（「毒丸」）。

**設定 `max_retries` 但未設定 DLQ**：
* 達到 `max_retries` 時仍會導致無法確認。
* 導致整個 S3 物件不必要地重新處理。

**最佳做法**---使用確認機制時，請務必設定 DLQ，以便：
* 防止無限次重新處理。
* 妥善處理無法重試的錯誤。
* 盡量減少不必要的重新處理。

## OpenSearch 叢集安全性

若要使用 `opensearch` 接收器外掛程式將資料傳送至 OpenSearch 叢集，您必須在管線組態中指定使用者名稱與密碼。下列範例 `pipelines.yaml` 檔案示範如何指定管理員安全性認證資訊：

```yaml
sink:
  - opensearch:
      username: "admin"
      password: "<custom-admin-password>"
      ...
```

或者，您也可以不使用管理員認證資訊，而是指定已對應至具備下列各節所列最低權限之角色的使用者認證資訊。

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

如需如何將使用者對應至角色的說明，請參閱[將使用者對應至角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/#mapping-users-to-roles)。

## Amazon OpenSearch Service 網域安全性

`opensearch` 接收器外掛程式可以將資料傳送至 [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) 網域，該網域使用 IAM 進行安全性管理。外掛程式會使用預設的認證資訊鏈。請使用 [AWS Command Line Interface (AWS CLI)](https://aws.amazon.com/cli/) 執行 `aws configure` 來設定您的認證資訊。

請確認您設定的認證資訊具備必要的 IAM 權限。下列網域存取政策示範最低必要權限：

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

如需如何設定網域存取政策的說明，請參閱 Amazon OpenSearch Service 文件中的[資源型政策
](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ac.html#ac-types-resource)。

### 精細存取控制

如果您的 OpenSearch Service 網域使用[精細存取控制](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html)，`opensearch` 接收器外掛程式需要一些額外的組態。

#### 以 IAM ARN 作為主要使用者

如果您使用 IAM Amazon Resource Name (ARN) 作為主要使用者，請在接收器組態中加入 `aws_sigv4` 選項：

```yaml
...
sink:
    opensearch:
      hosts: ["https://your-fgac-amazon-opensearch-service-endpoint"]
      aws_sigv4: true
```

請使用 AWS CLI 執行 `aws configure` 以使用主要 IAM 使用者認證資訊。如果您不想使用主要使用者，可以使用 `aws_sts_role_arn` 選項指定不同的 IAM 角色。外掛程式接著會使用此角色來簽署傳送至網域接收器的請求。您指定的 ARN 必須包含在[網域存取政策]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sinks/opensearch/#amazon-opensearch-service-domain-security)中。

#### 內部使用者資料庫中的主要使用者

如果您的網域使用內部使用者資料庫中的主要使用者，請指定主要使用者名稱與密碼，以及 `aws_sigv4` 選項：

```yaml
sink:
    opensearch:
      hosts: ["https://your-fgac-amazon-opensearch-service-endpoint"]
      username: "master-username"
      password: "master-password"
```

如需更多資訊，請參閱 Amazon OpenSearch Service 文件中的[建議組態](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html#fgac-recommendations)。

***注意***：您可以建立具有 `all_access` 權限的新 IAM 角色或內部使用者資料庫使用者，並改用它來取代主要使用者。

## OpenSearch Serverless 集合安全性

`opensearch` 接收器外掛程式可以將資料傳送至 [Amazon OpenSearch Serverless](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html) 集合。

OpenSearch Serverless 集合接收器有下列限制：

- 您無法寫入使用虛擬私有雲端 (VPC) 存取的集合。集合必須可從公用網路存取。
- OTel 追蹤群組處理器目前不支援集合接收器。

### 建立管線角色

首先，建立一個 IAM 角色，供管線擔任以寫入集合。該角色必須具備下列最低權限：

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

該角色必須具備下列信任關係，讓管線可以擔任該角色：

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

接下來，使用下列設定建立集合：

- 對 OpenSearch 端點與 OpenSearch Dashboards 都開放公用[網路存取](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-network.html)。
- 下列[資料存取政策](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-data-access.html)，授予管線角色必要的權限：

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

  ***重要***：請務必將 `Principal` 元素中的 ARN 取代為您在前一步驟建立的管線角色 ARN。

  如需如何建立集合的說明，請參閱 Amazon OpenSearch Service 文件中的[建立集合](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-manage.html#serverless-create)。

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

### 使用 template_content 與 actions 的範例

下列範例管線同時包含 `template_content` 以及條件式 `actions` 的清單：

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
