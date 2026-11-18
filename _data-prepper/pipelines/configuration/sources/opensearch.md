---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: OpenSearch
parent: Sources
grand_parent: Pipelines
nav_order: 50
canonical_url: https://docs.opensearch.org/latest/data-prepper/pipelines/configuration/sources/opensearch/
redirect_to: https://docs.opensearch.org/latest/data-prepper/pipelines/configuration/sources/opensearch/
---

# OpenSearch 來源

`opensearch` 來源外掛程式用於從 OpenSearch 叢集、舊版 Elasticsearch 叢集、Amazon OpenSearch Service 網域或 Amazon OpenSearch Serverless 集合讀取索引。

此外掛程式支援 OpenSearch 2.x 和 Elasticsearch 7.x。

## 使用方式

若要使用 `opensearch` 來源並採用最低必要設定，請將下列組態新增至您的 `pipeline.yaml` 檔案：

```yaml
opensearch-source-pipeline:
 source:
  opensearch:
    hosts: [ "https://localhost:9200" ]
    username: "username"
    password: "password"
 ...
```

若要使用 `opensearch` 來源並採用所有組態設定，包括 `indices`、`scheduling`、`search_options` 和 `connection`，請將下列範例新增至您的 `pipeline.yaml` 檔案：

```yaml
opensearch-source-pipeline:
  source:
    opensearch:
      hosts: [ "https://localhost:9200" ]
      username: "username"
      password: "password"
      indices:
        include:
          - index_name_regex: "test-index-.*"
        exclude:
          - index_name_regex: "\..*"
      scheduling:
        interval: "PT1H"
        index_read_count: 2
        start_time: "2023-06-02T22:01:30.00Z"
      search_options:
        search_context_type: "none"
        batch_size: 1000
      connection:
        insecure: false
        cert: "/path/to/cert.crt"
  ...
```

## Amazon OpenSearch Service

您可以傳入具有網域存取權的 `sts_role_arn`，將 `opensearch` 來源設定為使用 Amazon OpenSearch Service 網域，如下列範例所示：

```yaml
opensearch-source-pipeline:
  source:
    opensearch:
      hosts: [ "https://search-my-domain-soopywaovobopgs8ywurr3utsu.us-east-1.es.amazonaws.com" ]
      aws:
        region: "us-east-1"
        sts_role_arn: "arn:aws:iam::123456789012:role/my-domain-role"
  ...
```

## Amazon OpenSearch Serverless

您可以將 `serverless` 選項設為 `true`，將 `opensearch` 來源設定為使用 Amazon OpenSearch Serverless，如下列範例所示：

```yaml
    - opensearch:
        hosts: [ 'https://1234567890abcdefghijkl.us-west-2.aoss.amazonaws.com' ]
        aws:
          sts_role_arn: 'arn:aws:iam::123456789012:role/my-domain-role'
          region: 'us-west-2'
          serverless: true
```


## 使用中繼資料

當 `opensource` 來源從文件建立 OpenSearch Data Prepper 事件時，文件索引會以 `opensearch-index` 為鍵儲存在 `EventMetadata` 中，而 `document_id` 則會以 `opensearch-document_id` 為鍵儲存在 `EventMetadata` 中。文件版本會以 `opensearch_document_version` 儲存在中繼資料中。

您可以視需要在管線組態中參照此中繼資料。例如，您可以使用 `opensearch-document_id`，避免在支援文件更新的接收器（例如 `opensearch` 接收器）產生重複文件。您也可以使用原始文件中繼資料進行條件式路由。

下列管線組態範例會將事件傳送至 `opensearch` 接收器，並在目的地叢集中使用與來源叢集相同的索引、`document_id` 和 `document_version`，以避免產生重複文件：


```yaml
opensearch-migration-pipeline:
  source:
    opensearch:
      hosts: [ "https://source-cluster:9200" ]
      username: "username"
      password: "password"
  sink:
    - opensearch:
        hosts: [ "https://sink-cluster:9200" ]
        username: "username"
        password: "password"
        document_version_type: external
        document_version: "${getMetadata(\"opensearch_document_version\")}"
        document_id: "${getMetadata(\"opensearch-document_id\")}"
        index: "${getMetadata(\"opensearch-index\"}"
```

## 組態選項


下表說明您可以為 `opensearch` 來源設定的選項。

選項 | 必要 | 類型    | 說明
:--- | :--- |:--------| :---
`hosts` | 是 | 清單    | 要寫入的 OpenSearch 主機清單，例如 `["https://localhost:9200", "https://remote-cluster:9200"]`。
`username` | 否 | 字串  | HTTP 基本驗證的使用者名稱。自 Data Prepper 2.5 起，若套用 [AWS 祕密參照]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/configuring-data-prepper/#reference-secrets)，即可在執行階段重新整理此設定。
`password` | 否 | 字串  | HTTP 基本驗證的密碼。自 Data Prepper 2.5 起，若套用 [AWS 祕密參照]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/configuring-data-prepper/#reference-secrets)，即可在執行階段重新整理此設定。
`authentication` | 否 | 物件 | HTTP 基本驗證組態。不能與最上層的 `username` 和 `password` 選項一起使用。如需詳細資訊，請參閱[驗證](#authentication)。
`disable_authentication` | 否 | 布林值 | 是否停用驗證。預設為 `false`。
`aws` | 否 | 物件  | AWS 組態。如需詳細資訊，請參閱 [`aws`](#aws)。
`acknowledgments` | 否 | 布林值 | 設為 `true` 時，可讓 `opensearch` 來源在 OpenSearch 接收器收到事件時接收[端對端確認]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines/#end-to-end-acknowledgments)。預設為 `false`。
`connection` | 否 | 物件  | 連線組態。如需詳細資訊，請參閱[連線](#connection)。
`indices` | 否 | 物件 | 用於篩選要處理哪些索引的組態。預設為所有索引，包括系統索引。如需詳細資訊，請參閱[索引](#indices)。
`scheduling` | 否 | 物件 | 排程組態。如需詳細資訊，請參閱[排程](#scheduling)。
`search_options` | 否 | 物件 | 來源所執行的搜尋選項清單。如需詳細資訊，請參閱[搜尋選項](#search_options)。
`serverless` | 否 | 布林值 | 決定 OpenSearch 後端是否為 Amazon OpenSearch Serverless。當 `opensearch` 來源的目的地是 Amazon OpenSearch Serverless 集合時，請將此值設為 `true`。預設為 `false`。
`serverless_options` | 否 | 物件 | 當 `opensearch` 來源的後端設為 Amazon OpenSearch Serverless 時可用的網路組態選項。如需詳細資訊，請參閱 [Serverless 選項](#serverless-options)。
`distribution_version` | 否 | 字串 | 來源叢集的發行版本。有效值為 `opensearch` 和 `es7`。如果來源無法擷取叢集資訊，便會將該叢集視為 Elasticsearch 叢集。在此情況下，請將此選項設為 `opensearch`，以將該叢集視為 OpenSearch 叢集。來源接著會使用 `scroll` 搜尋，除非已指定 `search_context_type`。

### 驗證

請在 `authentication` 物件中使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`username` | 否 | 字串 | 用於 HTTP 基本驗證的使用者名稱。
`password` | 否 | 字串 | 用於 HTTP 基本驗證的密碼。

### 無伺服器選項

下列選項可用於 `serverless_options` 物件。

選項 | 必要 | 類型 | 說明
:--- | :--- | :---| :---
`network_policy_name` | 是 | 字串 | 要建立的網路政策名稱。
`collection_name` | 是 | 字串 | 要設定的 Amazon OpenSearch Serverless 集合名稱。
`vpce_id` | 是 | 字串 | 來源連線的虛擬私有雲端（VPC）端點。

### 排程

`scheduling` 組態可讓使用者根據 `index_read_count` 與重新計數時間 `interval`，設定來源重新處理索引的方式。

例如，將 `index_read_count` 設為 `3`，並將 `interval` 設為 `PT1H`，會將所有索引重新處理 3 次，每次間隔 1 小時。預設情況下，索引只會處理一次。

請在 `scheduling` 組態下使用下列選項。

選項 | 必要 | 類型            | 說明
:--- | :--- |:----------------| :---
`index_read_count` | 否 | 整數 | 每個索引的處理次數。預設為 `1`。
`interval` | 否 | 字串 | 決定兩次重新處理之間相隔時間的間隔。支援 ISO 8601 表示法字串（例如「PT20.345S」或「PT15M」），以及表示秒數（「60s」）與毫秒數（「1500ms」）的簡易表示法字串。預設為 `PT8H`。
`start_time` | 否 | 字串 | 開始處理的時間。來源在此時間之前不會開始處理。字串必須採用 ISO 8601 格式，例如 `2007-12-03T10:15:30.00Z`。預設選項會立即開始處理。
`discovery_mode` | 否 | 字串 | 決定來源探索待處理索引的頻率。有效值為 `periodic` 與 `single_scan`。設為 `periodic` 時，來源會定期檢查是否有待處理的索引，且每個索引會依照 `index_read_count` 與 `interval` 進行處理。設為 `single_scan` 時，來源只會探索一次索引，且每個索引只會處理一次。預設為 `periodic`。


<!-- vale off -->
### indices
<!-- vale on -->

下列選項可協助 `opensearch` 來源使用 regex 模式判斷要從來源叢集處理哪些索引。索引只有在符合 `include` 設定下的其中一個 `index_name_regex` 模式，且不符合 `exclude` 設定下的任何模式時，才會被處理。

選項 | 必要 | 類型  | 說明
:--- | :--- |:-----------------| :---
`include` | 否 | 物件陣列 | 索引組態模式的清單，用於指定要處理哪些索引。
`exclude` | 否 | 物件陣列 | 索引組態模式的清單，用於指定不要處理哪些索引。例如，您可以指定 `index_name_regex` 模式為 `\..*` 來排除系統索引。


使用 `include` 和 `exclude` 選項下的下列設定，指出索引的 regex 模式。

選項 | 必要 | 類型    | 說明
:--- |:----|:-----------------| :---
`index_name_regex` | 是 | 正規表示式字串 | 用來比對索引的 regex 模式。

<!-- vale off -->
### search_options
<!-- vale on -->

請在 `search_options` 組態下使用下列設定。

選項 | 必要 | 類型    | 說明
:--- |:---------|:--------| :---
`batch_size` | 否       | 整數 | 從 OpenSearch 分頁讀取時要讀取的文件數量。預設為 `1000`。
`search_context_type` | 否 | 列舉 | 覆寫要在索引上使用的搜尋／分頁類型。可為 [point_in_time]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#point-in-time-with-search_after))、[scroll]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#scroll-search) 或 `none`。`none` 選項會使用 [search_after]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#the-search_after-parameter) 參數。如需更多資訊，請參閱[預設搜尋行為](#default-search-behavior)。
`sort` | 否 | 清單 | 分頁時用來排序文件的欄位清單。每個項目包含一個必要的 `name`，用於指定欄位名稱，以及一個選用的 `order`，其值為 `ascending`（預設）或 `descending`。請在清單中包含 `_id`，讓每份文件都有唯一的排序值；否則，分頁可能會略過或重複文件。根據預設，文件會先依 `_doc` 排序，再依 `_id` 排序（使用 `scroll` 時則僅依 `_doc` 排序）。

### 預設搜尋行為

根據預設，`opensearch` 來源會使用叢集的版本與發行版來判斷要使用哪個 `search_context_type`。對於支援[時間點搜尋 (Point in Time)]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#point-in-time-with-search_after) 的叢集與網域，來源會使用 `point_in_time`。如果叢集不支援時間點搜尋，則會改用[捲動搜尋]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#scroll-search)。

對於 Amazon OpenSearch Serverless 集合，預設行為是使用 [`search_after`]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#the-search_after-parameter)。不過，我們建議改用 `point_in_time`。

### 連線

請在 `connection` 組態下使用下列設定。

選項 | 必要 | 類型    | 說明
:--- | :--- |:--------| :---
`cert` | 否 | 字串  | 當叢集使用 OpenSearch Security 外掛程式時，安全性憑證的路徑，例如 `"config/root-ca.pem"`。
`insecure` | 否 | 布林值 | 是否驗證 SSL 憑證。若設為 `true`，則會停用憑證授權單位 (CA) 憑證驗證，並傳送不安全的 HTTP 請求。預設為 `false`。
`certificate` | 否 | 字串 | CA 憑證檔案的路徑，或 PEM 格式的憑證內容。不可與 `cert` 同時使用。
`socket_timeout` | 否 | 持續時間 | 對叢集發出請求的通訊端逾時。若未指定，則會使用底層用戶端的預設逾時。
`connection_timeout` | 否 | 持續時間 | 與叢集建立連線的逾時。若未指定，則會使用底層用戶端的預設逾時。


### AWS

為 `aws` 服務設定驗證時，請使用下列選項。

選項 | 必要 | 類型    | 說明
:--- | :--- |:--------| :---
`region` | 否 | 字串  | 用於認證資訊的 AWS 區域。預設為[以標準 SDK 行為判斷區域](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/region-selection.html)。
`sts_role_arn` | 否 | 字串  | 對 Amazon OpenSearch Service 和 Amazon OpenSearch Serverless 發出請求時所要擔任的 AWS Security Token Service (AWS STS) 角色。預設為 `null`，此時會使用[標準 SDK 的認證資訊行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。
`sts_external_id` | 否 | 字串 | 擔任 STS 角色時使用的外部 ID。長度必須介於 2 到 1,224 個字元之間。
`sts_header_overrides` | 否 | 對應表 | AWS Identity and Access Management (IAM) 角色為來源外掛程式擔任時所使用的標頭覆寫對應表。最多 5 個標頭。
`serverless` | 否 | 布林值 | 從 Amazon OpenSearch Serverless 集合進行處理時，應設為 `true`。預設為 `false`。

## 指標

`opensearch` 來源包含下列指標。

### 計數器

- `documentsProcessed`：測量 `opensearch` 來源外掛程式處理的文件總數。
- `indicesProcessed`：測量 `opensearch` 來源外掛程式處理的索引總數。
- `processingErrors`：測量 `opensearch` 來源外掛程式發生的索引處理錯誤總數。
- `credentialsChanged`：測量 `opensearch` 來源重新整理基本認證資訊（使用者名稱/密碼）的次數。
- `clientRefreshErrors`：測量因 `opensearch` 來源重新整理基本認證資訊而產生新用戶端時遇到的錯誤數。

### 計時器

- `indexProcessingTime`：測量 `opensearch` 來源外掛程式的索引處理延遲，單位為秒。

### 分布摘要

- `bytesReceived`：測量 `opensearch` 來源外掛程式所接收傳入文件的大小分布，單位為位元組。
- `bytesProcessed`：測量 `opensearch` 來源外掛程式成功處理的傳入文件大小分布，單位為位元組。

## OpenSearch 叢集安全性

為了使用 `opensearch` 來源外掛程式從 OpenSearch 叢集提取資料，您必須在管線組態中指定您的使用者名稱與密碼。下列範例 `pipeline.yaml` 檔案示範如何指定預設的管理員安全性認證資訊：

```yaml
source:
  opensearch:
    username: "admin"
    password: "<custom-admin-password>"
  ...
```

### Amazon OpenSearch Service 網域安全性

`opensearch` 來源外掛程式可以從 [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) 網域提取資料，該網域使用 AWS Identity and Access Management (IAM) 來提供安全性。此外掛程式會使用預設的 Amazon OpenSearch Service 認證資訊鏈。請使用 [AWS Command Line Interface (AWS CLI)](https://aws.amazon.com/cli/) 執行 `aws configure` 來設定您的認證資訊。

請確定您設定的認證資訊具有必要的 IAM 權限。下列網域存取政策顯示最低必要權限：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<AccountId>:user/data-prepper-user"
      },
      "Action": "es:ESHttpGet",
      "Resource": [
        "arn:aws:es:us-east-1:<AccountId>:domain/<domain-name>/",
        "arn:aws:es:us-east-1:<AccountId>:domain/<domain-name>/_cat/indices",
        "arn:aws:es:us-east-1:<AccountId>:domain/<domain-name>/_search",
        "arn:aws:es:us-east-1:<AccountId>:domain/<domain-name>/_search/scroll",
        "arn:aws:es:us-east-1:<AccountId>:domain/<domain-name>/*/_search"
      ]
    },
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<AccountId>:user/data-prepper-user"
      },
      "Action": "es:ESHttpPost",
      "Resource": [
        "arn:aws:es:us-east-1:<AccountId>:domain/<domain-name>/*/_search/point_in_time",
        "arn:aws:es:us-east-1:<AccountId>:domain/<domain-name>/*/_search/scroll"
      ]
    },
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<AccountId>:user/data-prepper-user"
      },
      "Action": "es:ESHttpDelete",
      "Resource": [
        "arn:aws:es:us-east-1:<AccountId>:domain/<domain-name>/_search/point_in_time",
        "arn:aws:es:us-east-1:<AccountId>:domain/<domain-name>/_search/scroll"
      ]
    }
  ]
}
```

如需如何設定網域存取政策的指示，請參閱 Amazon OpenSearch Service 文件中的[資源型政策
](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ac.html#ac-types-resource)。

### OpenSearch Serverless 集合安全性

`opensearch` 來源外掛程式可以從 [Amazon OpenSearch Serverless](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html) 集合接收資料。

您無法從使用虛擬私人雲端 (VPC) 存取的集合讀取資料。集合必須可從公用網路存取。
{: .warning}

#### 建立管線角色

若要使用 OpenSearch Serverless 集合安全性，請建立一個 IAM 角色，讓管線擔任該角色以從集合讀取資料。該角色必須具備下列最低權限：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "aoss:APIAccessAll"
            ],
            "Resource": "arn:aws:aoss:*:<AccountId>:collection/*"
        }
    ]
}
```

#### 建立集合

接下來，使用下列設定建立集合：

- OpenSearch 端點與 OpenSearch Dashboards 都採用公用[網路存取](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-network.html)。
- 下列[資料存取政策](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-data-access.html)，會將必要的權限授予管線角色，如下列組態所示：

  ```json
  [
   {
      "Rules":[
         {
            "Resource":[
               "index/collection-name/*"
            ],
            "Permission":[
               "aoss:ReadDocument",
               "aoss:DescribeIndex"
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

請務必將 `Principal` 元素中的 Amazon Resource Name (ARN) 取代為您在前一步驟中建立的管線角色 ARN。
{: .tip}

如需建立集合的說明，請參閱 Amazon OpenSearch Service 文件中的[建立集合](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-manage.html#serverless-create)。

#### 建立管線

在您的 `pipeline.yaml` 檔案中，將 OpenSearch Serverless 集合端點指定為 `hosts` 選項。此外，您必須將 `serverless` 選項設定為 `true`。並在 `sts_role_arn` 選項中指定管線角色，如下列範例所示：

```yaml
opensearch-source-pipeline:
  source:
    opensearch:
      hosts: [ "https://<serverless-public-collection-endpoint>" ]
      aws:
        serverless: true
        sts_role_arn: "arn:aws:iam::<AccountId>:role/PipelineRole"
        region: "us-east-1"
  processor:
    - date:
        from_time_received: true
        destination: "@timestamp"
  sink:
    - stdout:
```
