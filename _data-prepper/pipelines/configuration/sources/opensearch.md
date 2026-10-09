---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: OpenSearch
parent: Sources
grand_parent: Pipelines
nav_order: 50
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

您可以視需要在管線組態中參照此中繼資料。例如，您可以使用 `opensearch-document_id`，避免在支援文件更新的接收端（例如 `opensearch` 接收端）產生重複文件。您也可以使用原始文件中繼資料進行條件式路由。

下列管線組態範例會將事件傳送至 `opensearch` 接收端，並在目的地叢集中使用與來源叢集相同的索引、`document_id` 和 `document_version`，以避免產生重複文件：


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
`username` | 否 | 字串  | HTTP 基本驗證的使用者名稱。自 Data Prepper 2.5 起，若套用 [AWS 機密參照]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/configuring-data-prepper/#reference-secrets)，即可在執行階段重新整理此設定。
`password` | 否 | 字串  | HTTP 基本驗證的密碼。自 Data Prepper 2.5 起，若套用 [AWS 機密參照]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/configuring-data-prepper/#reference-secrets)，即可在執行階段重新整理此設定。
`disable_authentication` | 否 | 布林值 | 是否停用驗證。預設為 `false`。
`aws` | 否 | 物件  | AWS 組態。如需詳細資訊，請參閱 [`aws`](#aws)。
`acknowledgments` | 否 | 布林值 | 當值為 `true` 時，啟用 `opensearch` 來源，使其在 OpenSearch 接收端收到事件時接收[端對端確認]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines/#end-to-end-acknowledgments)。預設為 `false`。
`connection` | 否 | 物件  | 連線組態。如需詳細資訊，請參閱[連線](#connection)。
`indices` | 否 | 物件 | 用於篩選要處理哪些索引的組態。預設為所有索引，包括系統索引。如需詳細資訊，請參閱[索引](#indices)。
`scheduling` | 否 | 物件 | 排程組態。如需詳細資訊，請參閱[排程](#scheduling)。
`search_options` | 否 | 物件 | 來源執行的搜尋選項清單。如需詳細資訊，請參閱[搜尋選項](#search_options)。
`serverless` | 否 | 布林值 | 決定 OpenSearch 後端是否為 Amazon OpenSearch Serverless。當 `opensearch` 來源的目的地為 Amazon OpenSearch Serverless 集合時，請將此值設為 `true`。預設為 `false`。
`serverless_options` | 否 | 物件 | 當 `opensearch` 來源的後端設為 Amazon OpenSearch Serverless 時可用的網路組態選項。如需詳細資訊，請參閱[無伺服器選項](#serverless-options)。

### 無伺服器選項

下列選項可用於 `serverless_options` 物件。

選項 | 必要 | 類型 | 說明
:--- | :--- | :---| :---
`network_policy_name` | 是 | 字串 | 要建立的網路政策名稱。
`collection_name` | 是 | 字串 | 要設定的 Amazon OpenSearch Serverless 集合名稱。
`vpce_id` | 是 | 字串 | 來源連線的虛擬私有雲端（VPC）端點。

### 排程

`scheduling` 組態可讓使用者根據 `index_read_count` 和重新計數時間 `interval`，設定來源如何重新處理索引。

例如，將 `index_read_count` 設為 `3`，並將 `interval` 設為 `1h`，會使所有索引重新處理 3 次，每次間隔 1 小時。預設情況下，索引只會處理一次。

請在 `scheduling` 組態下使用下列選項。

選項 | 必要 | 類型            | 說明
:--- | :--- |:----------------| :---
`index_read_count` | 否 | 整數 | 每個索引的處理次數。預設為 `1`。
`interval` | 否 | 字串 | 決定重新處理之間相隔時間的間隔。支援 ISO 8601 表示法字串，例如「PT20.345S」或「PT15M」，也支援以秒（「60s」）和毫秒（「1500ms」）表示的簡易表示法字串。預設為 `8h`。
`start_time` | 否 | 字串 | 應開始處理的時間。來源在此時間之前不會開始處理。字串必須採用 ISO 8601 格式，例如 `2007-12-03T10:15:30.00Z`。預設選項會立即開始處理。


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

使用 `search_options` 組態下的下列設定。

選項 | 必要 | 類型    | 說明
:--- |:---------|:--------| :---
`batch_size` | 否       | 整數 | 從 OpenSearch 分頁讀取時要讀取的文件數。預設為 `1000`。
`search_context_type` | 否 | 列舉值 | 覆寫要在索引上使用的搜尋/分頁類型。可為 [point_in_time]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#point-in-time-with-search_after))、[scroll]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#scroll-search) 或 `none`。`none` 選項會使用 [search_after]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#the-search_after-parameter) 參數。如需更多資訊，請參閱[預設搜尋行為](#default-search-behavior)。

### 預設搜尋行為

根據預設，`opensearch` 來源會使用叢集的版本與發行版來判斷要使用哪個 `search_context_type`。對於支援 [Point in Time]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#point-in-time-with-search_after) 的叢集與網域，來源會使用 `point_in_time`。如果叢集不支援 Point in Time 搜尋，則會改用 [scroll search]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#scroll-search)。

對於 Amazon OpenSearch Serverless 集合，預設行為是使用 [`search_after`]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/paginate/#the-search_after-parameter)。不過，我們建議改用 `point_in_time`。

### 連線

使用 `connection` 組態下的下列設定。

選項 | 必要 | 類型    | 說明
:--- | :--- |:--------| :---
`cert` | 否 | 字串  | 安全性憑證的路徑，例如當叢集使用 OpenSearch Security 外掛程式時的 `"config/root-ca.pem"`。
`insecure` | 否 | 布林值 | 是否要驗證 SSL 憑證。若設為 `true`，則會停用憑證授權單位 (CA) 憑證驗證，並傳送不安全的 HTTP 請求。預設為 `false`。


### AWS

為 `aws` 服務設定驗證時，請使用下列選項。

選項 | 必要 | 類型    | 說明
:--- | :--- |:--------| :---
`region` | 否 | 字串  | 要用於憑證的 AWS Region。預設為[標準 SDK 判斷 Region 的行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/region-selection.html)。
`sts_role_arn` | 否 | 字串  | 對 Amazon OpenSearch Service 和 Amazon OpenSearch Serverless 的請求所要擔任的 AWS Security Token Service (AWS STS) 角色。預設為 `null`，其會使用[憑證的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。
`serverless` | 否 | 布林值 | 從 Amazon OpenSearch Serverless 集合處理時，應設為 `true`。預設為 `false`。

## 指標

`opensearch` 來源包含下列指標。

### 計數器

- `documentsProcessed`：測量 `opensearch` 來源外掛程式處理的文件總數。
- `indicesProcessed`：測量 `opensearch` 來源外掛程式處理的索引總數。
- `processingErrors`：測量 `opensearch` 來源外掛程式發生的索引處理錯誤總數。
- `credentialsChanged`：測量 `opensearch` 來源重新整理基本憑證 (使用者名稱/密碼) 的次數。
- `clientRefreshErrors`：測量因 `opensearch` 來源重新整理基本憑證而產生新用戶端時遇到的錯誤數。

### 計時器

- `indexProcessingTime`：測量 `opensearch` 來源外掛程式的索引處理延遲，單位為秒。

### 分布摘要

- `bytesReceived`：測量 `opensearch` 來源外掛程式所接收傳入文件的大小分布，單位為位元組。
- `bytesProcessed`：測量 `opensearch` 來源外掛程式成功處理的傳入文件大小分布，單位為位元組。

## OpenSearch 叢集安全性

為了使用 `opensearch` 來源外掛程式從 OpenSearch 叢集提取資料，您必須在管線組態中指定您的使用者名稱與密碼。下列範例 `pipeline.yaml` 檔案示範如何指定預設的管理員安全性憑證：

```yaml
source:
  opensearch:
    username: "admin"
    password: "admin"
  ...
```

### Amazon OpenSearch Service 網域安全性

`opensearch` 來源外掛程式可以從 [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) 網域提取資料，該網域使用 AWS Identity and Access Management (IAM) 來提供安全性。此外掛程式會使用預設的 Amazon OpenSearch Service 憑證鏈。請使用 [AWS Command Line Interface (AWS CLI)](https://aws.amazon.com/cli/) 執行 `aws configure` 來設定您的憑證。

請確定您設定的憑證具有必要的 IAM 權限。下列網域存取政策顯示最低必要權限：

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
