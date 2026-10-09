---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Iceberg
parent: Sources
grand_parent: Pipelines
nav_order: 35
---

# Iceberg 來源

這是實驗性功能，不建議在正式環境中使用。如需此功能的最新進度，或想提供意見回饋，請參閱相關的 [GitHub 議題](https://github.com/opensearch-project/data-prepper/issues/6552)。
{: .warning}

`iceberg` 來源為 [Apache Iceberg](https://iceberg.apache.org/) 資料表提供變更資料擷取（CDC）。它會輪詢新的 Iceberg 快照，並使用 [`IncrementalChangelogScan`](https://iceberg.apache.org/javadoc/latest/org/apache/iceberg/IncrementalChangelogScan.html) API 計算快照之間的變更，以偵測 `INSERT`、`UPDATE` 和 `DELETE` 操作。

此來源支援下列項目：
- Iceberg 資料表格式 v1、v2 和 v3。
- 僅支援寫入時複製（Copy-on-Write，CoW）資料表。不支援讀取時合併（Merge-on-Read，MoR）資料表。
- Parquet、Avro 和 ORC 檔案格式。
- 任何 Iceberg 目錄實作，包括 AWS Glue Data Catalog、Hive Metastore 和 REST 目錄。

此來源包含兩種匯入模式：

1. **Export**：初始快照載入，讀取資料表的目前狀態。
2. **Stream**：輪詢新快照並處理增量變更記錄事件。

## 先決條件

若要使用 Iceberg 來源，您必須在 `data-prepper-config.yaml` 中啟用實驗性的 `iceberg` 外掛程式：

```yaml
experimental:
  enabled_plugins:
    source:
      - iceberg
```
{% include copy.html %}

## 使用方式

下列管線範例指定了 `iceberg` 來源。它使用搭配 Amazon S3 儲存空間的 REST 目錄，從 Iceberg 資料表讀取增量變更。`catalog` 定義在最上層，讓所有資料表共用相同的目錄組態。

在接收端組態中，`action` 設為 `${getMetadata("bulk_action")}`，讓 `INSERT` 和 `UPDATE` 操作更新或插入文件，而 `DELETE` 操作則移除文件。`document_id` 設為 `${getMetadata("document_id")}`，使用 `|` 分隔符號串接 `identifier_columns` 值，讓每個 Iceberg 資料列對應到唯一的 OpenSearch 文件：

```yaml
version: "2"
iceberg-cdc-pipeline:
  source:
    iceberg:
      catalog:
        type: rest
        uri: "http://iceberg-rest-catalog:8181"
        io-impl: "org.apache.iceberg.aws.s3.S3FileIO"
        client.region: "us-east-1"
      tables:
        - table_name: "my_database.my_table"
          identifier_columns: ["id"]
      polling_interval: "PT30S"
      acknowledgments: true
  sink:
    - opensearch:
        hosts: ["https://localhost:9200"]
        index: "my-index"
        action: "${getMetadata(\"bulk_action\")}"
        document_id: "${getMetadata(\"document_id\")}"
```
{% include copy.html %}

若要為特定資料表使用不同的目錄，請在資料表層級指定 `catalog`，以覆寫最上層的定義：

```yaml
iceberg:
  catalog:
    type: rest
    uri: "http://iceberg-rest-catalog:8181"
    io-impl: "org.apache.iceberg.aws.s3.S3FileIO"
  tables:
    - table_name: "db.table_a"
      identifier_columns: ["id"]
    - table_name: "db.table_b"
      identifier_columns: ["id"]
      catalog:
        type: glue
        warehouse: "s3://other-bucket/warehouse"
        io-impl: "org.apache.iceberg.aws.s3.S3FileIO"
```
{% include copy.html %}

## 組態選項

`iceberg` 來源支援下列組態選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`catalog` | 否 | 對映表 | 套用至所有資料表的預設目錄屬性。當資料表指定自己的 `catalog` 時，資料表層級的定義會完全取代最上層的定義。如需常用屬性，請參閱 [catalog](#catalog)。
`tables` | 是 | 清單 | Iceberg 資料表組態的清單。如需支援的選項，請參閱 [tables](#tables)。
`polling_interval` | 否 | 時間長度 | 領導節點輪詢新快照的頻率。支援 [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations) 時間長度表示法，例如 `PT30S` 或 `PT5M`。預設為 `PT30S`。
`acknowledgments` | 否 | 布林值 | 當值為 `true` 時，啟用[端對端確認]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines#end-to-end-acknowledgments)。預設為 `true`。
`shuffle` | 否 | 物件 | 處理含有 `DELETE` 操作的快照時所使用的分散式重分配組態。如需支援的選項，請參閱 [shuffle](#shuffle)。

<!-- vale off -->
### tables
<!-- vale on -->

每個資料表項目可使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`table_name` | 是 | 字串 | 完整限定的 Iceberg 資料表名稱（例如 `my_database.my_table`）。
`catalog` | 否 | 對映表 | Apache Iceberg 目錄屬性的對映表。指定時，會完全取代最上層的 `catalog`。如需常用屬性，請參閱 [catalog](#catalog)。
`identifier_columns` | 否 | 清單 | 用作文件識別碼的欄名稱清單，用於偵測 `UPDATE` 和 `DELETE`。處理含有 `UPDATE` 或 `DELETE` 操作的資料表時，此選項為必要。若未指定，來源無法判定文件 ID 或正確偵測更新。
`disable_export` | 否 | 布林值 | 當值為 `true` 時，略過初始快照匯出，僅從 CDC 開始。預設為 `false`。

<!-- vale off -->
### catalog
<!-- vale on -->

`catalog` 選項接受 Apache Iceberg 目錄實作支援的任何屬性。如需可用屬性的完整清單，請參閱各目錄類型的文件，例如 [REST 目錄](https://iceberg.apache.org/rest-catalog-spec/)、[AWS Glue](https://iceberg.apache.org/docs/latest/aws/#glue-catalog) 或 [Hive Metastore](https://iceberg.apache.org/docs/latest/hive/#global-hive-catalog)。下表列出常用屬性。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`type` | 是 | 字串 | 目錄類型。支援的值包括 `glue`、`hive`、`rest` 及其他 Iceberg 目錄實作。
`io-impl` | 否 | 字串 | FileIO 實作類別。例如，Amazon S3 使用 `org.apache.iceberg.aws.s3.S3FileIO`，HDFS 使用 `org.apache.iceberg.hadoop.HadoopFileIO`。未指定時，各目錄會使用自己的預設值（REST 目錄使用 `ResolvingFileIO`，並依檔案路徑的 URI 配置自動選取實作；Glue 使用 `S3FileIO`；Hadoop 和 JDBC 使用 `HadoopFileIO`）。

如需 AWS 專用的目錄與 S3 屬性，請參閱 [Apache Iceberg AWS 整合文件](https://iceberg.apache.org/docs/latest/aws/)。

<!-- vale off -->
### shuffle
<!-- vale on -->

處理包含 `DELETE` 操作的快照（寫入時複製資料表中的 `UPDATE` 或 `DELETE`）時，來源會使用分散式重分配，確保跨多個節點的結果正確。重分配會將含有相同 `identifier_columns` 值的所有記錄傳送至同一個節點，以便正確處理相符的 `INSERT` 和 `DELETE` 配對。

當快照包含 `DELETE` 操作時，重分配會自動啟動。僅包含 `INSERT` 的快照不會使用重分配。

下表列出 `shuffle` 組態選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`partitions` | 否 | 整數 | 雜湊分割區的數量。必須為 1--10,000。預設為 `64`。
`target_partition_size` | 否 | 字串 | 合併後的重分配讀取工作的目標大小。較小的相鄰分割區會合併，以減少工作數量。預設為 `64mb`。
`storage_path` | 否 | 字串 | 存放中間重分配檔案的本機目錄。設定 `data-prepper.dir` 時，預設為 `${data-prepper.dir}/data/shuffle`，否則為 `${java.io.tmpdir}/data-prepper-shuffle`。
`port` | 否 | 整數 | 用於節點間重分配資料傳輸的 HTTP 伺服器連接埠。預設為 `4995`。
`ssl` | 否 | 布林值 | 當值為 `true` 時，為重分配 HTTP 伺服器啟用傳輸層安全性（TLS）。預設為 `true`。
`ssl_certificate_file` | 視條件而定 | 字串 | PEM 格式的 TLS 憑證檔案路徑。支援本機檔案路徑與 Amazon S3 URI（例如 `s3://my-bucket/certs/cert.pem`）。當 `ssl` 為 `true` 且 `use_acm_certificate_for_ssl` 為 `false` 時，此選項為必要。
`ssl_key_file` | 視條件而定 | 字串 | PEM 格式的 TLS 私密金鑰檔案路徑。支援本機檔案路徑與 Amazon S3 URI（例如 `s3://my-bucket/certs/key.pem`）。當 `ssl` 為 `true` 且 `use_acm_certificate_for_ssl` 為 `false` 時，此選項為必要。
`use_acm_certificate_for_ssl` | 否 | 布林值 | 當值為 `true` 時，使用 AWS Certificate Manager（ACM）提供 TLS 憑證，取代 `ssl_certificate_file` 和 `ssl_key_file`。預設為 `false`。
`acm_certificate_arn` | 視條件而定 | 字串 | ACM 憑證 ARN。當 `use_acm_certificate_for_ssl` 為 `true` 時，此選項為必要。
`aws_region` | 視條件而定 | 字串 | 用於 ACM 或 S3 憑證存取的 AWS 區域。當 `use_acm_certificate_for_ssl` 為 `true`，或憑證檔案位於 Amazon S3 時，此選項為必要。
`ssl_client_auth` | 否 | 布林值 | 當值為 `true` 時，啟用雙向 TLS（mTLS）以進行節點間驗證。所有節點都必須在重分配通訊期間提供有效的用戶端憑證。預設為 `false`。
`ssl_insecure_disable_verification` | 否 | 布林值 | 當值為 `true` 時，停用節點間重分配通訊的 TLS 憑證驗證。預設為 `false`。

執行多個 Data Prepper 節點時，每個節點都必須能透過設定的 `port` 連線至其他節點。
{: .note}

## 公開的中繼資料屬性

下列中繼資料屬性會新增至 `iceberg` 來源處理的每個事件。您可以使用[運算式語法的 `getMetadata` 函式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/get-metadata/)存取這些屬性：

- `bulk_action`：建議用於 OpenSearch 接收端的大量操作動作。對於 `INSERT` 和 `UPDATE` 操作，設為 `index`；對於 `DELETE` 操作，則設為 `delete`。
- `document_id`：文件識別碼，使用 `|` 分隔符號串接 `identifier_columns` 值而成。僅在設定 `identifier_columns` 時設定。
- `iceberg_operation`：CDC 操作類型。設為 `INSERT` 或 `DELETE`。當 Iceberg 中的資料列更新時，來源會收到一組具有相同 `identifier_columns` 值的 `DELETE` 和 `INSERT` 配對。來源會將此配對辨識為更新，並僅發出 `INSERT` 事件，因為依 `document_id` 更新或插入即可產生正確結果，無須另行刪除。
- `iceberg_table_name`：來源 Iceberg 資料表的名稱。
- `iceberg_snapshot_id`：事件來源的快照 ID。

## 權限

所需權限取決於目錄類型與儲存後端。以下是使用 AWS Glue Data Catalog 和 Amazon S3 時所需的最低 IAM 權限範例：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "allowReadingFromS3",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": [
        "arn:aws:s3:::my-iceberg-bucket",
        "arn:aws:s3:::my-iceberg-bucket/*"
      ]
    },
    {
      "Sid": "allowGlueCatalogAccess",
      "Effect": "Allow",
      "Action": [
        "glue:GetTable",
        "glue:GetTables",
        "glue:GetDatabase",
        "glue:GetDatabases"
      ],
      "Resource": [
        "arn:aws:glue:region:account-id:catalog",
        "arn:aws:glue:region:account-id:database/*",
        "arn:aws:glue:region:account-id:table/*/*"
      ]
    }
  ]
}
```
{% include copy.html %}
