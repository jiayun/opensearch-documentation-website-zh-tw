---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: OpenSearch 
parent: Sinks
grand_parent: Pipelines
nav_order: 50
canonical_url: https://docs.opensearch.org/latest/data-prepper/pipelines/configuration/sinks/opensearch/
redirect_to: https://docs.opensearch.org/latest/data-prepper/pipelines/configuration/sinks/opensearch/
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

下表說明您可以為 `opensearch` 接收器 (sink) 設定的選項。

選項 | 必要 | 類型 | 說明
:--- | :--- |:---| :---
`hosts` | 是 | 清單 | 要寫入的 OpenSearch 主機清單，例如 `["https://localhost:9200", "https://remote-cluster:9200"]`。
`cert` | 否 | 字串 | 安全性憑證的路徑。例如，若叢集使用 OpenSearch Security 外掛程式，則為 `"config/root-ca.pem"`。
`username` | 否 | 字串  | HTTP 基本驗證的使用者名稱。
`password` | 否 | 字串 | HTTP 基本驗證的密碼。許多 Data Prepper 範例會以 `admin` 使用者身分進行驗證，並使用 `<custom-admin-password>` 預留位置代表其[密碼]({{site.url}}{{site.baseurl}}/security/configuration/passwords/#admin-password)。您也可以使用僅具備接收器所需權限的使用者進行驗證。如需詳細資訊，請參閱 [OpenSearch 叢集安全性](#opensearch-cluster-security)。
`authentication` | 否 | 物件 | 連線至 OpenSearch 時使用的驗證組態。使用此物件設定 HTTP 基本驗證或用戶端憑證驗證。不能與頂層的 `username` 和 `password` 選項一起使用。如需詳細資訊，請參閱[驗證](#authentication)。
`api_token` | 否 | 字串 | 接收器在傳送至 OpenSearch 的每個請求中，以持有人權杖 (bearer token) 形式放入 `Authorization` 標頭的權杖。設定 `authentication` 時會忽略此選項。
`aws` | 否 | AWS  | [AWS](#aws) 組態。 
[`max_retries`](#configure-max_retries) | 否 | 整數 | `opensearch` 接收器在將推送視為失敗之前，嘗試將資料推送至 OpenSearch 伺服器的最大次數。預設為 `Integer.MAX_VALUE`。若未提供，接收器會無限期地嘗試將資料推送至 OpenSearch 伺服器，且指數退避會增加重試前的等待時間。
`aws_sigv4` | 否 | 布林值 | **已於 Data Prepper 2.7 中棄用。** 預設為 `false`。是否使用 AWS Identity and Access Management (IAM) 簽署來連線至 Amazon OpenSearch Service 網域。對於您的存取金鑰、秘密金鑰及選用的工作階段權杖，OpenSearch Data Prepper 會使用預設的認證資訊鏈（環境變數、Java 系統屬性、`~/.aws/credential`）。 
`aws_region` | 否 | 字串 | **已於 Data Prepper 2.7 中棄用。** 連線至 Amazon OpenSearch Service 時，網域所在的 AWS 區域（例如 `"us-east-1"`）。
`aws_sts_role_arn` | 否 | 字串 | **已於 Data Prepper 2.7 中棄用。** 外掛程式用來簽署傳送至 Amazon OpenSearch Service 之請求的 IAM 角色。若未提供此資訊，外掛程式會使用預設的認證資訊。
`socket_timeout` | 否 | 整數 | 等待資料傳回時的逾時值（以毫秒為單位），即兩個連續資料封包之間的最長閒置時間。逾時值 `0` 會被解讀為無限逾時。若此逾時值為負數或未設定，底層的 Apache HttpClient 將依賴作業系統設定來管理通訊端逾時。
`connect_timeout` | 否 | 整數| 向連線管理員請求連線時的逾時值（以毫秒為單位）。逾時值 `0` 會被解讀為無限逾時。若此逾時值為負數或未設定，底層的 Apache HttpClient 將依賴作業系統設定來管理連線逾時。
`insecure` | 否 | 布林值  | 是否驗證 SSL 憑證。若設為 `true`，則會停用憑證授權單位 (CA) 憑證驗證，並改為傳送不安全的 HTTP 請求。預設為 `false`。
`proxy` | 否 | 字串 | [正向 HTTP 代理伺服器](https://en.wikipedia.org/wiki/Proxy_server)的位址。格式為 `"&lt;hostname or IP&gt;:&lt;port&gt;"`（例如 `"example.com:8100"`、`"http://example.com:8100"`、`"112.112.112.112:8100"`）。連接埠號碼不可省略。
`path_prefix` | 否 | 字串 | 接收器加在傳送至 OpenSearch 之每個請求路徑前的路徑前置詞，例如 `/opensearch`。當 OpenSearch 需透過子路徑存取時（例如位於反向代理伺服器之後），請使用此選項。
`index` | 視條件而定 | 字串 | 匯出索引的名稱。僅在 `index_type` 為 `custom` 時為必要。索引可以是一般字串（例如 `my-index-name`）、包含 [Java 日期時間模式](https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html)（例如 `my-index-%{yyyy.MM.dd}` 或 `my-%{yyyy-MM-dd-HH}-index`）、使用欄位值格式化（例如 `my-index-${/my_field}`），或使用 [Data Prepper 運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)（例如 `my-index-${getMetadata(\"my_metadata_field\"}`）。所有格式化選項皆可組合使用，以便在建立靜態、動態及輪替索引時提供彈性。 
`index_type` | 否 | 字串 | 指定接收器外掛程式所處理的資料類型。有效值包括 `custom`、`trace-analytics-raw`、`trace-analytics-plain-raw`、`trace-analytics-plain-raw-v2`、`trace-analytics-service-map`、`otel-v2-apm-service-map`、`log-analytics`、`log-analytics-plain`、`metric-analytics`、`metric-analytics-plain`、`tsdb` 及 `management_disabled`。<br><br>若要從搭配 `output_format: otel` 的 `otel_logs_source` 產生符合 Amazon Security Lake 規範的資料，請將 `index_type` 設為 `log-analytics-plain`。<br>若為搭配 `output_format: otel` 的 `otel_metrics_source`，請將 `index_type` 設為 `metric-analytics-plain`。<br>若為搭配 `output_format: otel` 的 `otel_trace_source`，請將 `index_type` 設為 `trace-analytics-plain-raw`。<br><br>`trace-analytics-plain-raw-v2` 值會使用可組合索引範本，將追蹤區段 (span) 寫入 `otel-v2-apm-span` 索引別名。當 `distribution_version` 為 `es6` 時不支援此值。<br><br>預設為 `custom`。


`template_type` | 否 | 字串 | 定義要使用的 OpenSearch 範本類型。可用選項為 `v1` 和 `index-template`。預設值為 `v1`，會使用 `_template` API 端點所提供的原始 OpenSearch 範本。`index-template` 選項使用可組合的[索引範本]({{site.url}}{{site.baseurl}}/opensearch/index-templates/)，可透過 OpenSearch `_index_template` API 取得。可組合的索引類型比預設值更具彈性，且當 OpenSearch 叢集中已有現有的索引範本時必須使用。所有版本的 OpenSearch 以及部分較新版本的 Elasticsearch 皆提供可組合範本。當 `distribution_version` 設為 `es6` 時，Data Prepper 會將 `template_type` 強制設為 `v1`。
`template_file` | 否 | 字串 | 當 `index_type` 設為 `custom` 時，JSON [索引範本]({{site.url}}{{site.baseurl}}/opensearch/index-templates/)檔案的路徑，例如 `/your/local/template-file.json`。如需範本檔案範例，請參閱 [otel-v1-apm-span-index-template.json](https://github.com/opensearch-project/data-prepper/blob/main/data-prepper-plugins/opensearch/src/main/resources/otel-v1-apm-span-index-template.json)。若您提供範本檔案，該檔案必須符合 `template_type` 參數所指定的範本格式。
`template_content` | 否 | JSON | 包含索引[索引範本]({{site.url}}{{site.baseurl}}/opensearch/index-templates/)中的所有內嵌 JSON。如需範本內容範例，請參閱[範本內容範例](#example-with-template_content-and-actions)。
`component_templates` | 否 | 清單 | 要新增至 Data Prepper 所建立之索引範本 `composed_of` 清單中的[元件範本]({{site.url}}{{site.baseurl}}/im-plugin/index-templates/#reusing-configuration-with-component-templates)名稱清單。這些名稱會新增在索引範本已列出的任何元件範本之後，無論索引範本來自 `template_file`、`template_content`，或是 `index_type` 的內建範本。OpenSearch 會依序套用元件範本，而索引範本本身的設定與對應優先於所有元件範本。Data Prepper 不會建立這些元件範本，因此這些範本必須在管線啟動前就已存在於叢集中。需要將 `template_type` 設為 `index-template`。`trace-analytics-plain-raw-v2` 索引類型一律使用 `index-template`，因此不需要設定 `template_type`。當 `index_type` 為 `management_disabled` 時無法使用。
`document_id_field` | 否 | 字串 | **已在 Data Prepper 2.7 中棄用，請改用 `document_id`。** 當 `index_type` 為 `custom` 時，來源資料中要用作 OpenSearch 文件 ID 的欄位（例如 `"my-field"`）。
`document_id` | 否 | 字串 | 用作 OpenSearch 文件中 `_id` 的格式字串。若要指定事件中的單一欄位，請使用 `${/my_field}`。您也可以使用 Data Prepper 運算式來建構 `document_id`，例如 `${getMetadata(\"some_metadata_key\")}`。這些選項可組合成更複雜的格式，例如 `${/my_field}-test-${getMetadata(\"some_metadata_key\")}`。 
`document_version` | 否 | 字串  |  用作 OpenSearch 文件中 `_version` 的格式字串。若要指定事件中的單一欄位，請使用 `${/my_field}`。您也可以使用 Data Prepper 運算式來建構 `document_version`，例如 `${getMetadata(\"some_metadata_key\")}`。這些選項可組合成更複雜的版本，例如 `${/my_field}${getMetadata(\"some_metadata_key\")}`。`document_version` 格式的求值結果必須為 long 類型，且只能在 `document_version_type` 設為 `external` 或 `external_gte` 時使用。
`document_version_type` | 否 | 字串  | 索引操作的文件版本類型。必須是 `external`、`external_gte` 或 `internal` 其中之一。若設為 `external` 或 `external_gte`，則 `document_version` 為必要項目。
`dlq_file` | 否 | 字串 | 您偏好的死信佇列檔案路徑（例如 `/your/local/dlq-file`）。當 Data Prepper 無法在 OpenSearch 叢集上將文件編製索引時，會寫入此檔案。
`dlq` | 否 | 不適用 | [DLQ 組態]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/dlq/)。 
`bulk_size` | 否 | 整數 (long) | 傳送至 OpenSearch 叢集之大量請求的大小上限（單位為 MiB）。低於 `0` 的值表示大小不受限制。若單一文件超過大量請求大小上限，Data Prepper 會個別傳送每個請求。預設值為 `5`。
`estimate_bulk_size_using_compression` | 否 | 布林值 | 判斷請求是否已達到 `bulk_size` 時，是否以壓縮後的大小來估算大量請求的大小。接收器會在本機壓縮部分填入的請求，以計算近似大小。停用請求壓縮時會忽略此設定（請參閱 `enable_request_compression`）。預設為 `false`。
`max_local_compressions_for_estimation` | 否 | 整數 | 接收器為估算大小而壓縮部分填入之大量請求的最大次數。值越高，估算越準確，但效能會降低。僅在 `estimate_bulk_size_using_compression` 為 `true` 時適用。預設為 `2`。
`ism_policy_file` | 否 | 字串 | Index State Management (ISM) 政策 JSON 檔案的絕對檔案路徑。此政策檔案僅在該索引類型沒有內建政策檔案時生效。例如，`custom` 索引類型是目前唯一沒有內建政策檔案的類型，因此若透過此參數提供政策檔案，就會使用該檔案。如需政策 JSON 檔案的詳細資訊，請參閱 [ISM 政策]({{site.url}}{{site.baseurl}}/im-plugin/ism/policies/)。
`number_of_shards` | 否 | 整數  | 索引在目的地 OpenSearch 伺服器上應具有的主要分片數量。此參數僅在接收器組態中明確提供 `template_file` 或其為內建時才會生效。若設定此參數，將會覆寫索引範本檔案中的值。如需詳細資訊，請參閱[建立索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/)。
`number_of_replicas` | 否 | 整數 | 每個主要分片在目的地 OpenSearch 伺服器上應具有的副本分片數量。例如，若您有 4 個主要分片並將 `number_of_replicas` 設為 `3`，則該索引會有 12 個副本分片。此參數僅在接收器組態中明確提供 `template_file` 或其為內建時才會生效。若設定此參數，將會覆寫索引範本檔案中的值。如需詳細資訊，請參閱[建立索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/)。
`distribution_version` | 否 | 字串  | 指出接收器的後端版本是否為 Elasticsearch 6 或更新版本。`es6` 代表 Elasticsearch 6。`default` 代表最新的相容後端版本，例如 Elasticsearch 7.x、OpenSearch 1.x 或 OpenSearch 2.x。預設為 `default`。
`enable_request_compression` | 否 | 布林值 | 傳送請求至 OpenSearch 時是否啟用壓縮。當 `distribution_version` 設為 `es6` 時，預設為 `false`。對於所有其他發行版本，預設為 `true`。
`action` | 否 | 字串 | 用於文件的 OpenSearch 大量動作。必須是 `create`、`index`、`update`、`upsert` 或 `delete` 其中之一。預設為 `index`。
`actions` | 否 | 清單 | 可作為 `action` 替代方案的[動作清單](#actions)，其運作方式如同 switch case 陳述式，會依條件決定對事件採取的大量動作。 
`script` | 否 | 物件 | OpenSearch 為更新文件而執行的 [Painless]({{site.url}}{{site.baseurl}}/scripting/painless/) 指令碼。僅能在 `action` 設為 `update`、`upsert` 或運算式時使用。如需詳細資訊，請參閱[指令碼](#script)。
`flush_timeout` | 否 | Long | 一個 long 類別，包含在排清請求前，嘗試將大量請求填充至 `bulk_size` 的時間長度（單位為毫秒）。若此逾時在大量請求達到 `bulk_size` 之前到期，就會排清該請求。設為 `-1` 可停用排清逾時，改為在每個批次結束時排清目前所有內容。預設為 `60,000`，即 1 分鐘。
`normalize_index` | 否 | 布林值 | 若為 true，OpenSearch 接收器會嘗試建立動態索引名稱。依據[索引命名限制]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/#index-naming-restrictions)，在 `${})` 中指定格式選項的索引名稱為有效名稱。任何無效字元都會被移除。預設值為 `false`。
`routing` | 否 | 字串 | 在 OpenSearch 中儲存文件時，用來作為產生該文件 `shard_id` 之雜湊的字串。系統會搜尋每一筆傳入記錄。若存在該字串，則會將其用作文件的路由欄位。若不存在，OpenSearch 在儲存文件時會使用預設路由機制（`document_id`）。支援使用事件中的欄位及 [Data Prepper 運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)進行格式化，例如 `${/my_field}-test-${getMetadata(\"some_metadata_key\")}`。
`document_root_key` | 否 | 字串  | 事件中要用作文件根的鍵。預設為事件的根。若該鍵不存在，則整個事件會寫入為文件。若 `document_root_key` 為基本值類型（例如字串或整數），則文件結構將為 `{"data": <value of the document_root_key>}`。
`serverless` | 否 | 布林值 | **已在 Data Prepper 2.7 中棄用。請改為搭配 `aws` 組態使用此選項。** 判斷 OpenSearch 後端是否為 Amazon OpenSearch Serverless。當 `opensearch` 接收器的目的地為 Amazon OpenSearch Serverless 集合時，請將此值設為 `true`。預設為 `false`。
`serverless_options` | 否 | 物件 | **已在 Data Prepper 2.7 中棄用。請改為搭配 `aws` 組態使用此選項。** 當 `opensearch` 接收器的後端設為 Amazon OpenSearch Serverless 時可用的網路組態選項。如需詳細資訊，請參閱 [Serverless 選項](#serverless-options)。
`query_lookup` | 否 | 物件 | 在編製索引前查詢現有文件以防止重複的組態。如需詳細資訊，請參閱[查詢查閱](#query-lookup)。
`pull_indexing` | 否 | 物件 | 設定接收器將文件寫入串流平台，再由 OpenSearch 索引透過拉取式匯入 (pull-based ingestion) 從該平台匯入這些文件。設定此選項後，接收器不會傳送大量請求至 OpenSearch。這是實驗性功能。如需詳細資訊，請參閱[拉取式編製索引](#pull-based-indexing)。


## 驗證

`authentication` 物件支援下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`username` | 否 | 字串 | HTTP 基本驗證所使用的使用者名稱。
`password` | 否 | 字串 | HTTP 基本驗證所使用的密碼。
`client_certificate` | 視情況而定 | 字串 | 用於 TLS 用戶端憑證驗證的用戶端憑證，採用 PEM 格式。請指定 PEM 檔案的路徑，或以 `-----BEGIN` 開頭的 PEM 內容。若已設定 `client_key`，則為必要。
`client_key` | 視情況而定 | 字串 | 用戶端憑證的未加密私密金鑰，採用 PEM 格式。請指定 PEM 檔案的路徑，或以 `-----BEGIN` 開頭的 PEM 內容。若已設定 `client_certificate`，則為必要。

下列範例設定用戶端憑證驗證：

```yaml
pipeline:
  ...
  sink:
    - opensearch:
        hosts: ["https://localhost:9200"]
        cert: path/to/root-ca.pem
        index: my-index
        authentication:
          client_certificate: path/to/client.pem
          client_key: path/to/client-key.pem
```
{% include copy.html %}

## 查詢查閱

`query_lookup` 組態會在為新文件編製索引之前，先查詢 OpenSearch 中的現有文件，藉此避免產生重複文件。此功能可在以下兩種情況下協助防止重複：

1. **條件式查詢**：在為文件編製索引之前，根據條件查詢文件。
2. **錯誤觸發查詢**：當發生可能導致部分成功的批次作業錯誤（例如通訊端逾時或 500 內部伺服器錯誤）時，查詢文件。

### 查詢查找選項

`query_lookup` 物件支援下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`query_when` | 是 | 字串 | 一個 [Data Prepper 運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)，用於決定哪些文件在編製索引前符合查詢資格。例如，`getMetadata("potential_duplicate") == true` 只會查詢該中繼資料欄位設為 `true` 的文件。
`query_term` | 是 | 字串 | 文件的唯一欄位，用於在 OpenSearch 中查詢現有文件。這通常是 ID 欄位。
`query_on_bulk_errors` | 否 | 布林值 | 設為 `true` 時，遇到可復原大量操作錯誤（例如通訊端逾時或 500 錯誤）的文件將會被查詢，而不是立即重試。當初始編製索引請求可能已部分成功時，這有助於避免產生重複文件。預設值為 `false`。
`query_duration` | 否 | 持續時間 | 在將指定文件編製索引之前查詢該文件的時間長度。請使用 ISO 8601 持續時間格式，例如 `PT5M` 代表 5 分鐘。預設值為 `PT3M`。
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
`region` | 否 | 字串 | 用於認證資訊的 AWS 區域。預設為[以標準 SDK 行為判斷區域](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/region-selection.html)。
`sts_role_arn` | 否 | 字串 | 對 Amazon SQS 與 Amazon S3 發出請求時要擔任的 AWS Security Token Service（AWS STS）角色。預設為 `null`，這會使用[認證資訊的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。
`sts_header_overrides` | 否 | Map | IAM 角色為接收器（sink）外掛程式擔任時所使用的標頭覆寫對應表。
`sts_external_id` | 否 | 字串 | 要附加到 AWS STS 之 AssumeRole 請求的外部 ID。
`serverless` | 否 | 布林值 | 決定 OpenSearch 後端是否為 Amazon OpenSearch Serverless。當 `opensearch` 接收器的目的地是 Amazon OpenSearch Serverless 集合時，請將此值設為 `true`。預設為 `false`。
`serverless_options` | 否 | 物件 | 當 `opensearch` 接收器的後端設為 Amazon OpenSearch Serverless 時，可用的網路組態選項。如需詳細資訊，請參閱 [Serverless 選項](#serverless-options)。
`resource_name` | 否 | 字串 | 設定 `semantic_enrichment` 時，接收器在其中建立索引的 Amazon OpenSearch Service 網域名稱或 Amazon OpenSearch Serverless 集合 ID。若未設定，接收器會從 `hosts` 中的第一個主機推導出網域名稱或集合 ID。
`semantic_enrichment` | 否 | 物件 | 接收器建立索引時要啟用語意擴充的欄位。如需詳細資訊，請參閱[語意擴充](#semantic-enrichment)。

### 語意擴充

設定 `aws.semantic_enrichment` 後，接收器 (sink) 會先建立 `index` 中指定的索引，再將文件寫入該索引。接收器會使用 Amazon OpenSearch Service 或 Amazon OpenSearch Serverless `CreateIndex` API 建立索引，並將列出的每個欄位對應為已啟用語意擴充的 `text` 欄位。如果索引已存在，接收器不會修改該索引。語意擴充僅適用於 Amazon OpenSearch Service 網域及 Amazon OpenSearch Serverless 集合。

`semantic_enrichment` 物件支援下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`fields` | 是 | 清單 | 要啟用語意擴充的欄位。

`fields` 清單中的每個物件支援下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`name` | 是 | 字串 | 欄位的名稱。
`language` | 是 | 字串 | 欄位內容的語言。有效值為 `english` 和 `multilingual`。

下列範例會建立一個索引，其中 `title` 和 `description` 欄位已啟用語意擴充：

```yaml
pipeline:
  ...
  sink:
    - opensearch:
        hosts: ["https://search-my-domain-abc123.us-east-1.es.amazonaws.com"]
        index: my-index
        aws:
          region: us-east-1
          sts_role_arn: arn:aws:iam::123456789012:role/PipelineRole
          resource_name: my-domain
          semantic_enrichment:
            fields:
              - name: title
                language: english
              - name: description
                language: multilingual
```
{% include copy.html %}

<!-- vale off -->
## actions
<!-- vale on -->

以下選項可在 `actions` 選項內使用。

選項 | 必要 | 類型 | 說明
:--- |:---| :--- | :---
`type` | 是 | 字串 | 當 `when` 條件評估為 true 時要使用的批次動作類型。必須是 `create`、`index`、`update`、`upsert` 或 `delete` 其中之一。
`when` | 否 | 字串 | 一個 [Data Prepper 運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)，用於有條件地評估是否要使用 `type` 中設定的批次動作將事件傳送至 OpenSearch。若為空，則在事件傳送至 OpenSearch 時會自動選擇批次動作。


## 指令碼

`script` 物件會設定一個 [Painless]({{site.url}}{{site.baseurl}}/scripting/painless/) 指令碼，OpenSearch 會針對每個更新作業執行此指令碼。指令碼會以 `params.doc` 參數接收事件。當 `action` 為 `update` 時，指令碼會在現有文件上執行。當 `action` 為 `upsert` 時，接收器 (sink) 會傳送指令碼式 upsert，因此即使文件不存在，指令碼也會執行。在此情況下，事件會作為初始文件使用。

`script` 物件支援下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`source` | 是 | 字串 | Painless 指令碼。以 `//` 開頭的行會在指令碼傳送至 OpenSearch 之前移除。
`params` | 否 | Map | 要傳遞給指令碼的參數，指令碼可透過 `params.<parameter_name>` 存取這些參數。字串值可以包含格式運算式，例如 `${/my_field}`，這些運算式會針對每個事件進行評估。請勿將參數命名為 `doc`，因為它會取代 `params.doc` 中的事件。

下列範例會將 `inc` 參數的值加到現有文件的 `counter` 欄位，並記錄最新事件的 `source` 值：

```yaml
pipeline:
  ...
  sink:
    - opensearch:
        hosts: ["https://localhost:9200"]
        index: my-index
        document_id: "${/id}"
        action: upsert
        script:
          source: |
            if (ctx._source.counter == null) { ctx._source.counter = params.doc.counter; }
            else { ctx._source.counter += params.inc; }
            ctx._source.last_source = params.source_name;
          params:
            inc: 5
            source_name: "${/source}"
```
{% include copy.html %}

## 拉取式編製索引

這是實驗性功能，不建議在生產環境中使用。
{: .warning}

設定 `pull_indexing` 後，接收器 (sink) 會將文件寫入串流平台（例如 Apache Kafka），再由 OpenSearch 索引透過[拉取式匯入 (pull-based ingestion)]({{site.url}}{{site.baseurl}}/api-reference/document-apis/pull-based-ingestion/) 匯入這些文件。接收器啟動時，會讀取索引的分片數量和 `ingestion_source.param.topic` 設定，並在主題 (topic) 不存在時建立該主題。主題中每個分片各對應一個分割區 (partition)。接收器會根據 `routing` 或文件 ID，將每份文件寫入 OpenSearch 路由該文件時的目標分片所對應的分割區。

### 先決條件

在設定拉取式索引 (pull-based indexing) 之前，請完成下列步驟：

1. 建立 `index` 中指定的索引，並將其設定為使用拉取式匯入 (pull-based ingestion)。接收器 (sink) 不會建立此索引。
1. 在 `data-prepper-config.yaml` 中啟用實驗性功能：

    ```yaml
    experimental:
      enable_all: true
    ```
    {% include copy.html %}

### 組態

拉取式索引 (pull-based indexing) 有下列需求：

- `index` 選項必須包含靜態索引名稱。
- `action` 選項以及 `actions` 中每個項目的 `type` 必須為 `index`、`create` 或 `delete`。
- 必須設定 `document_id` 和 `document_version` 選項。接收器無法判定文件 ID 或版本的事件不會被寫入。

`pull_indexing` 物件支援下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`engine` | 是 | 物件 | 接收器寫入文件的串流平台。唯一支援的引擎是 `kafka`。

`kafka` 引擎支援下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`bootstrap_servers` | 是 | 清單 | Kafka 代理伺服器的主機與連接埠配對，例如 `["kafka-broker:9092"]`。

下列範例會將文件寫入為 `my-pull-index` 索引設定的 Kafka 主題：

```yaml
pipeline:
  ...
  sink:
    - opensearch:
        hosts: ["https://localhost:9200"]
        index: my-pull-index
        document_id: "${/id}"
        document_version: "${/version}"
        document_version_type: external
        action: index
        pull_indexing:
          engine:
            kafka:
              bootstrap_servers: ["kafka-broker:9092"]
```
{% include copy.html %}

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
