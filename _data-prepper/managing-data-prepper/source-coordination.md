---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "來源協調"
nav_order: 35
parent: Managing OpenSearch Data Prepper
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

下表提供 `source_coordination` 的選用組態值。

| 值 | 類型 | 說明 |
| :--- | :--- | :--- |
| `partition_prefix` | 字串 | `sourceIdentifier` 的字首，用於區分共用同一個分散式儲存庫的多個 Data Prepper 叢集。 |
| `store` | 物件  | 構成所用儲存庫組態的物件，其中鍵是儲存庫的名稱，例如 `in_memory` 或 `dynamodb`，值則是該儲存庫類型上可用的任何組態。 |

### 支援的儲存庫
從 Data Prepper 2.4 開始，僅支援 `in_memory` 與 `dynamodb` 儲存庫：

- `in_memory` 儲存庫是在 `data-prepper-config.yaml` 檔案中未設定任何 `source_coordination` 設定時的預設值，且僅應用於單一節點組態。
- `dynamodb` 儲存庫用於多節點的 Data Prepper 環境。`dynamodb` 儲存庫可在需要使用來源協調的一或多個 Data Prepper 叢集之間共用。

#### DynamoDB 儲存庫

Data Prepper 會在啟動時嘗試建立 `dynamodb` 資料表，除非 `skip_table_creation` 旗標被設定為 `true`。您也可以選擇性地在資料表上設定[存留時間](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) (`ttl`)，讓儲存庫隨著時間清理項目。有些來源依賴來源協調來進行資料去重，因此請務必為管線執行期間設定足夠大的 `ttl`。 

如果資料表上未設定 `ttl`，則資料表中不再需要的項目必須手動清理。

以下顯示 Data Prepper 建立資料表、啟用 `ttl` 以及與資料表互動所需的完整權限集合：

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
    "arn:aws:dynamodb:${REGION}:${AWS_ACCOUNT_ID}:table/${TABLE_NAME}",
    "arn:aws:dynamodb:${REGION}:${AWS_ACCOUNT_ID}:table/${TABLE_NAME}/index/source-status"
  ]
}
```


| 值 | 必要 | 類型 | 說明 |
| :--- | :--- | :--- | :--- | 
| `table_name` | 是 | 字串  | 用於來源協調的資料表名稱。 |
| `region` | 是 | 字串 | DynamoDB 資料表的區域。 |
| `sts_role_arn` | 否  | 字串  |  包含資料表權限的 `sts` 角色。未提供時會使用預設憑證。 |
| `sts_external_id` | 否 | 字串  | 在 API 呼叫中用來擔任 `sts_role_arn` 的外部 ID。 |
| `skip_table_creation` | 否 | 布林值  | 使用現有儲存庫時，若設定為 `true`，則會略過建立儲存庫的嘗試。預設值為 `false`。 |
| `provisioned_write_capacity_units` | 否 | 整數 |  要在資料表上設定的寫入容量單位數量。預設值為 `10`。 |
| `provisioned_read_capacity_units`  | 否 | 整數 | 要在資料表上設定的讀取容量單位數量。預設值為 `10`。 |
| `ttl` | Duration | 選用。資料表中項目的 TTL 持續時間。對項目進行更新時，TTL 會延長此持續時間。預設為資料表上不使用 TTL。 |
  
以下範例顯示 `dynamodb` 儲存庫：

```yaml
source_coordination:
  store:
     dynamodb:
       table_name: "DataPrepperSourceCoordinationStore"
       region: "us-east-1"
       sts_role_arn: "arn:aws:iam::##########:role/SourceCoordinationTableRole"
       ttl: "P7D"
       skip_table_creation: true
```

#### 記憶體內儲存庫（預設）

以下範例顯示 `in_memory` 儲存庫，最適合與單一節點叢集搭配使用：


```yaml
source_coordination:
  store:
    in_memory:
```


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

