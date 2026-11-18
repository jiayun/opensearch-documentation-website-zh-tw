---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "來源協調"
nav_order: 35
parent: Managing OpenSearch Data Prepper
canonical_url: https://docs.opensearch.org/latest/data-prepper/managing-data-prepper/source-coordination/
redirect_to: https://docs.opensearch.org/latest/data-prepper/managing-data-prepper/source-coordination/
---

# 來源協調

_來源協調_ (source coordination) 是在多節點環境中協調與分配 OpenSearch Data Prepper 資料來源之間工作的概念。有些資料來源，例如 Amazon Kinesis 或 Amazon Simple Queue Service (Amazon SQS)，本身原生就支援協調。其他資料來源，例如 OpenSearch、Amazon Simple Storage Service (Amazon S3)、Amazon DynamoDB 與 JDBC/ODBC，則不支援來源協調。

Data Prepper 來源協調會決定 Data Prepper 叢集中每個節點要執行哪個工作分割區，並防止重複的工作分割區。

Data Prepper 受 [Kinesis Client Library](https://docs.aws.amazon.com/streams/latest/dev/shared-throughput-kcl-consumers.html) 啟發，利用分散式儲存庫以租約 (lease) 的形式來處理工作的分配與去重。

## 分割區格式

來源協調會將來源區分為「工作分割區」。例如，S3 物件就是 Amazon S3 的一個工作分割區，而 OpenSearch 索引則是 OpenSearch 的一個工作分割區。

Data Prepper 會為來源所選取的每個工作分割區，在其用於來源協調的分散式儲存庫中建立對應的項目。每個項目都具有下列標準格式，並可由分散式儲存庫的實作加以擴充。

| 值 | 類型 | 說明 |
| :--- | :--- | :--- |
| `sourceIdentifier` | 字串  | 識別哪個 Data Prepper 管線在此分割區上工作。預設情況下，`sourceIdentifier` 會以子管線名稱作為字首，但可以在 data-prepper-config.yaml 檔案中透過 `partition_prefix` 設定額外的字首。 |
| `sourcePartitionKey` | 字串  | 與此項目相關聯之工作分割區的識別碼。例如，對於具有掃描功能的 `s3` 來源，此識別碼是 S3 儲存貯體的 `objectKey` 組合。
| `partitionOwner` | 字串   | 目前擁有並正在處理此分割區之節點的識別碼。此 ID 包含節點的主機名稱，但當此分割區未被擁有時則為 `null`。 |
| `partitionProgressState` | 字串  | 一個 JSON 字串物件，代表工作分割區上已完成的進度，或在另一個節點於前一個節點當機停止處接續處理時，來源可能需要的任何其他中繼資料。  |
| `partitionOwnershipTimeout` | 時間戳記  | 每當 Data Prepper 節點取得分割區時，會給予分割區擁有者 10 分鐘的逾時時間，以處理節點當機的情況。當擁有者儲存分割區的狀態時，擁有權會再延長 10 分鐘。  |
| `sourcePartitionStatus` | 列舉 | 代表分割區目前的狀態：`ASSIGNED` 表示分割區目前正在處理中，`UNASSIGNED` 表示分割區正在等待處理，`CLOSED` 表示分割區等待日後再處理，`COMPLETED` 表示分割區已經處理完畢。 |           
| `reOpenAt` | 時間戳記  | 代表 CLOSED 分割區重新開放並被視為可供處理的時間。僅適用於 CLOSED 分割區。 |
| `closedCount` | Long | 追蹤分割區被標記為 `CLOSED` 的次數。|


## 取得分割區

分割區會按照來源在 `List<PartitionIdentifer>` 中回傳的順序被取得。當節點嘗試取得分割區時，Data Prepper 會執行下列步驟：

1. Data Prepper 會查詢 `ASSIGNED` 分割區，檢查是否有 `ASSIGNED` 分割區的分割區擁有者已逾時。這是為了優先處理在處理過程中節點當機的分割區，以便能使用可能具有時效性的分割區狀態。 
2. 查詢 `ASSIGNED` 分割區之後，Data Prepper 會查詢 `CLOSED` 分割區，判斷是否有任何分割區的 `reOpenAt` 時間戳記已到期。 
3. 如果沒有可用的 `ASSIGNED` 或 `CLOSED` 分割區，Data Prepper 會查詢 `UNASSIGNED` 分割區，直到其中一個分割區變為 `ASSIGNED`。

如果發生此流程且節點未取得任何分割區，則在 `SourceCoordinator` 的 `getNextPartition` 方法中提供的分割區供應函式會建立新的分割區。供應函式完成後，Data Prepper 會再次查詢 `ASSIGNED`、`CLOSED` 與 `UNASSIGNED` 的分割區。

## 全域狀態

傳遞給 `getNextPartition` 方法的任何函式，都會以 `Map<String, Object>` 的全域狀態建立新的分割區。此狀態由叢集中的所有節點共用；來源會決定該函式每次只由單一節點執行。

## 組態

下表列出 `source_coordination` 的選用組態值。

| 值 | 類型 | 說明 |
| :--- | :--- | :--- |
| `partition_prefix` | 字串 | `sourceIdentifier` 的前置詞，用於區分共用同一個分散式儲存區的 Data Prepper 叢集。 |
| `store` | 物件 | 包含一組鍵值對的物件，用於設定儲存區。鍵為儲存區名稱，例如 `in_memory` 或 `dynamodb`；值為包含該儲存區選項的物件。如需所有支援的儲存區清單，請參閱[支援的儲存區](#supported-stores)。 |

### 支援的儲存區

Data Prepper 支援下列來源協調儲存區。

| 儲存區 | 環境 | 說明 |
| :--- | :--- | :--- |
| `in_memory` | 單一節點 | 當 `data-prepper-config.yaml` 檔案中未設定任何 `source_coordination` 設定時的預設儲存區。如需更多資訊，請參閱[記憶體內儲存區](#in-memory-store)。 |
| `dynamodb` | 多節點 | 將協調資料儲存在 Amazon DynamoDB 中。多個使用來源協調的 Data Prepper 叢集可以共用此儲存區。如需更多資訊，請參閱 [DynamoDB 儲存區](#dynamodb-store)。 |
| `jdbc` | 多節點 | 將協調資料儲存在 PostgreSQL 或 MySQL 中。如需更多資訊，請參閱 [JDBC 儲存區](#jdbc-store)。 |

#### 記憶體內儲存區

`in_memory` 儲存區是預設的儲存區，沒有任何選項。請僅將其用於單一節點的 Data Prepper 部署。

以下範例設定 `in_memory` 儲存區：

```yaml
source_coordination:
  store:
    in_memory:
```
{% include copy.html %}

#### DynamoDB 儲存區

`dynamodb` 儲存區使用 Amazon DynamoDB 資料表，在各 Data Prepper 節點之間協調工作。多個 Data Prepper 叢集可以共用同一個資料表。若要區分這些叢集，請設定 `partition_prefix`。

根據預設，Data Prepper 會在儲存區啟動時建立資料表及其索引。若資料表已存在，請將 `skip_table_creation` 設為 `true`。下列政策陳述式授予 Data Prepper 建立資料表、啟用 TTL 以及讀取和寫入項目所需的權限：

```json
{
  "Sid": "ReadWriteSourceCoordinationDynamoStore",
  "Effect": "Allow",
  "Action": [
    "dynamodb:DescribeTimeToLive",
    "dynamodb:UpdateTimeToLive",
    "dynamodb:DescribeTable",
    "dynamodb:CreateTable",
    "dynamodb:GetItem",
    "dynamodb:PutItem",
    "dynamodb:Query"
  ],
  "Resource": [
    "arn:aws:dynamodb:<region>:<account-id>:table/<table-name>",
    "arn:aws:dynamodb:<region>:<account-id>:table/<table-name>/index/source-status"
  ]
}
```
{% include copy.html %}

您可以設定 `ttl` 來啟用 DynamoDB [存留時間 (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)，以從資料表中移除已過期的項目。部分來源會使用這些項目來防止重複處理，因此請將 `ttl` 設定為超過預期的管線執行時間。若未設定 `ttl`，您必須手動刪除不再需要的項目。

當 `skip_table_creation` 為 `true` 時，Data Prepper 不會在資料表上啟用 TTL。若您為現有資料表設定 `ttl`，請在啟動 Data Prepper 之前，於該資料表的 `expirationTime` 屬性上啟用 TTL。

`dynamodb` 儲存區支援下列選項。

| 選項 | 必要 | 類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `table_name` | 是 | 字串 | 用於來源協調的資料表名稱。 |
| `region` | 是 | 字串 | DynamoDB 資料表所在的 AWS 區域。 |
| `sts_role_arn` | 否 | 字串 | 具有資料表權限之 AWS Identity and Access Management (IAM) 角色的 Amazon Resource Name (ARN)。若未提供，Data Prepper 會使用預設認證資訊。 |
| `sts_external_id` | 否 | 字串 | 在 API 呼叫中用於擔任 `sts_role_arn` 角色的外部 ID。 |
| `skip_table_creation` | 否 | 布林值 | 設為 `true` 時，Data Prepper 不會建立資料表。預設為 `false`。 |
| `provisioned_write_capacity_units` | 否 | 整數 | 要在資料表上設定的寫入容量單位數。預設為 `10`。 |
| `provisioned_read_capacity_units` | 否 | 整數 | 要在資料表上設定的讀取容量單位數。預設為 `10`。 |
| `ttl` | 否 | 持續時間 | 用於設定資料表中項目到期時間的持續時間。請使用 ISO 8601 持續時間格式，例如 `P7D`。Data Prepper 更新項目時會延長其到期時間。根據預設，項目不會過期。 |

下列範例將 DynamoDB 資料表設定為來源協調儲存區：

```yaml
source_coordination:
  store:
    dynamodb:
      table_name: "DataPrepperSourceCoordinationStore"
      region: "us-east-1"
      sts_role_arn: "arn:aws:iam::123456789012:role/SourceCoordinationTableRole"
      ttl: "P7D"
      skip_table_creation: true
```
{% include copy.html %}

#### JDBC 儲存區

`jdbc` 儲存區使用關聯式資料庫，在各個 Data Prepper 節點之間協調工作。Data Prepper 內建適用於 PostgreSQL 和 MySQL 的 Java Database Connectivity (JDBC) 驅動程式。

根據預設，Data Prepper 會在儲存區啟動時建立協調資料表及其索引。資料庫使用者必須具備建立資料表和索引的權限，以及選取、插入、更新和刪除資料列的權限。若所需的資料表和索引已存在，請將 `skip_table_creation` 設為 `true`。

Data Prepper 會在使用來源協調的來源啟動時驗證儲存區設定，而不是在 Data Prepper 啟動時驗證。如果某項設定無效，Data Prepper 會記錄錯誤，且不會執行該管線。

您可以設定 `ttl`，定期移除已過期的分割區記錄。部分來源會使用這些記錄來避免重複處理，因此請將 `ttl` 設定為超過預期的管線執行時間。

`jdbc` 儲存區支援下列選項。

| 選項 | 必要 | 類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `url` | 是 | 字串 | JDBC 連線 URL。 |
| `username` | 是 | 字串 | 資料庫使用者名稱。 |
| `password` | 是 | 字串 | 資料庫密碼。 |
| `table_name` | 否 | 字串 | 用於來源協調的資料表名稱。您可以指定未限定名稱，或以結構描述 (schema) 限定的名稱，例如 `schema.table`。預設值為 `source_coordination`。 |
| `skip_table_creation` | 否 | 布林值 | 設為 `true` 時，Data Prepper 不會建立協調資料表或其索引。預設值為 `false`。 |
| `max_pool_size` | 否 | 整數 | JDBC 連線集區中的連線數上限。此值至少須為 `2`，因為儲存區在開啟另一個連線以更新分割區時，會同時保留一個連線。預設值為 `5`。 |
| `ttl` | 否 | 持續時間 | 用於設定分割區記錄到期時間的持續時間。請使用 ISO 8601 持續時間格式，例如 `P7D`。Data Prepper 更新記錄時會延長其到期時間。根據預設，記錄不會過期。 |
| `connection_properties` | 否 | 對應表 | 要傳遞給每個資料庫連線的 JDBC 驅動程式屬性。 |

下列範例將要求 TLS 連線的 PostgreSQL 資料庫設定為來源協調儲存區。如果您的資料庫不支援 TLS，請移除 `ssl` 連線屬性：

```yaml
source_coordination:
  store:
    jdbc:
      url: "jdbc:postgresql://db:5432/dataprepper"
      username: "dp_user"
      password: {% raw %}"${{aws_secrets:db-secrets:password}}"{% endraw %}
      table_name: "source_coordination"
      max_pool_size: 5
      ttl: "P7D"
      connection_properties:
        ssl: "true"
```
{% include copy.html %}

## 指標

來源協調指標的解讀方式取決於所設定的來源。來源協調指標的格式為 `<sub-pipeline-name>_source_coordinator_<metric-name>`。您可以使用子管線名稱來識別這些指標的來源，因為每個子管線對應的來源都是唯一的。

### 進度指標

以下為與分割區進度相關的指標：

* `partitionsCreatedCount`：已建立的分割區項目數量。對於 S3 掃描，這是已為其建立分割區的物件數量。
* `partitionsCompleted`：已完整處理並標記為 `COMPLETED` 的分割區數量。對於 S3 掃描，這是已處理的物件數量。
* `noPartitionsAcquired`：節點嘗試取得分割區以執行工作，但在儲存庫中找不到可用分割區的次數。可用來表示來源已沒有更多資料進入。
* `partitionsAcquired`：已被節點取得以執行工作的分割區數量。在非錯誤情況下，此數值應等於已建立的分割區數量。
* `partitionsClosed`：已被標記為 `CLOSED` 的分割區數量。僅適用於使用 CLOSED 功能的來源。

以下為與分割區錯誤相關的指標：

* `partitionNotFoundErrors`：表示某個正由節點擁有的分割區項目沒有對應的儲存庫項目。只有在資料表中的項目被手動刪除時才會發生。
* `partitionNotOwnedErrors`：表示擁有分割區的節點因分割區擁有權逾時到期而失去擁有權。除非來源能夠透過 `saveState` 對分割區進行檢查點標記，否則此錯誤會導致項目重複處理。
* `partitionUpdateErrors`：對此分割區項目的儲存庫更新失敗時所收到的錯誤數量。會加上 `saveState`、`close` 或 `complete` 字首，以指出哪個更新動作失敗。

