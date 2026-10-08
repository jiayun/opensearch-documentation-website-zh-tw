---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 OpenSearch 索引最佳化查詢效能"
parent: Connecting data sources
nav_order: 40
---

# 使用 OpenSearch 索引最佳化查詢效能
2.11 版引入
{: .label .label-purple }


使用外部資料來源時，查詢效能可能因網路延遲、資料轉換和資料量等原因而變慢。您可以使用 OpenSearch 索引（例如略過索引或涵蓋索引）來最佳化查詢效能。

- _略過索引_ 使用略過加速方法（例如分割區、最小值與最大值，以及值集合）來匯入資料並建立精簡的彙總資料結構。這使其成為直接查詢情境中的經濟選擇。如需詳細資訊，請參閱[略過索引]({{site.url}}{{site.baseurl}}/dashboards/management/accelerate-external-data/#skipping-indexes)。
- _涵蓋索引_ 會將來源中的全部或部分資料匯入 OpenSearch，讓您能夠使用所有 OpenSearch Dashboards 和外掛程式功能。如需詳細資訊，請參閱[涵蓋索引]({{site.url}}{{site.baseurl}}/dashboards/management/accelerate-external-data/#covering-indexes)。
- _具體化檢視_ 透過儲存來源資料中預先計算和彙總的資料來提升查詢效能。如需詳細資訊，請參閱[具體化檢視]({{site.url}}{{site.baseurl}}/dashboards/management/accelerate-external-data/#materialized-views)。

如需各索引編製程序的完整指引，請參閱 [Flint 索引參考手冊](https://github.com/opensearch-project/opensearch-spark/blob/main/docs/index.md)。

## 資料來源使用案例：加速效能

若要開始加速查詢效能，請執行下列步驟：

1. 前往 **OpenSearch Plugins** > **Query Workbench**，然後從 **Data sources** 下拉式選單中選取您的資料來源。
2. 從導覽選單中選取資料庫。
3. 檢視表格中的結果，並確認資料正確無誤。
4. 依照下列步驟建立 OpenSearch 索引：
    1. 選取 **Accelerate data**。隨即出現快顯視窗。
    2. 在 **Select data fields** 下輸入您的資料庫和資料表詳細資訊。
5. 在 **Acceleration type** 中，根據您的使用案例選取加速類型。接著，輸入該加速類型的資訊。如需詳細資訊，請參閱下列章節：
      - [略過索引]({{site.url}}{{site.baseurl}}/dashboards/management/accelerate-external-data/#skipping-indexes)
      - [涵蓋索引]({{site.url}}{{site.baseurl}}/dashboards/management/accelerate-external-data/#covering-indexes)
      - [具體化檢視]({{site.url}}{{site.baseurl}}/dashboards/management/accelerate-external-data/#materialized-views)

## 略過索引

_略過索引_ 使用略過加速方法（例如分割區、最小值/最大值和值集合），透過精簡的彙總資料結構來匯入資料。這使其成為直接查詢情境中的經濟選擇。

使用略過索引時，您可以只為儲存在 Amazon S3 中的資料之中繼資料編製索引。當您查詢具有略過索引的資料表時，查詢規劃器會參考該索引並重寫查詢，以有效率地找出資料，而不必掃描所有分割區和檔案。這讓略過索引能夠快速縮小已儲存資料的特定位置範圍。

### 定義略過索引設定

1. 在 **Skipping index definition** 下，選取 **Generate** 以自動產生略過索引。或者，若要手動選擇要新增的欄位，請選取 **Add fields**。可從下列類型中選擇：
  - `Partition`：使用資料分割區詳細資訊來找出資料。此類型最適合以分割為基礎的資料行，例如年、月、日、時。
  - `MinMax`：使用已編製索引之資料行的下限和上限來找出資料。此類型最適合數值資料行。
  - `ValueSet`：使用唯一值集合來找出資料。此類型最適合基數為低至中等且需要完全相符的資料行。
  - `BloomFilter`：使用 Bloom 篩選器演算法來找出資料。此類型最適合基數高且不需要完全相符的資料行。
2. 選取 **Create acceleration** 以套用您的略過索引設定。
3. 檢視略過索引查詢詳細資訊，然後按一下 **Run**。OpenSearch 會將您的索引新增至左側導覽窗格。

或者，您也可以使用 Query Workbench 手動建立略過索引。從下拉式選單中選取您的資料來源，然後執行類似下列的查詢：

```sql
CREATE SKIPPING INDEX
ON datasourcename.gluedatabasename.vpclogstable(
 `srcaddr` BLOOM_FILTER, 
 `dstaddr` BLOOM_FILTER, 
 `day` PARTITION, 
 `account_id`BLOOM_FILTER
 ) WITH (
index_settings = '{"number_of_shards":5,"number_of_replicas":1}',
auto_refresh = true,
checkpoint_location = 's3://accountnum-vpcflow/AWSLogs/checkpoint'
)
```

## 涵蓋索引

_涵蓋索引_ 會將來源中的全部或部分資料匯入 OpenSearch，讓您能夠使用所有 OpenSearch Dashboards 和外掛程式功能。

使用涵蓋索引時，您可以從資料表中的指定資料行匯入資料。這是三種索引類型中效能最佳的一種。由於 OpenSearch 會匯入您所需資料行中的所有資料，因此您可以獲得更好的效能，並能執行進階分析。

OpenSearch 會從涵蓋索引資料建立新的索引。您可以使用這個新索引來建立視覺化，或用於異常偵測和地理空間功能。您可以使用 Index State Management 管理涵蓋檢視索引。如需詳細資訊，請參閱 [Index State Management]({{site.url}}{{site.baseurl}}/im-plugin/ism/index/)。

### 定義涵蓋索引設定

1. 在 **Index name** 中，輸入有效的索引名稱。請注意，每個資料表可以有多個涵蓋索引。
2. 選擇 **Refresh type**。根據預設，OpenSearch 會自動重新整理索引。否則，您必須使用 REFRESH 陳述式手動觸發重新整理。
3. 輸入 **Checkpoint location**，這是重新整理工作檢查點的路徑。此位置必須是與 Hadoop 分散式檔案系統 (HDFS) 相容之檔案系統中的路徑。如需詳細資訊，請參閱[啟動串流查詢](https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html#starting-streaming-queries)。
4. 在 **Covering index definition** 下選取 **(add fields here)**，以定義涵蓋索引欄位。
5. 選取 **Create acceleration** 以套用您的涵蓋索引設定。
6. 檢視涵蓋索引查詢詳細資訊，然後按一下 **Run**。OpenSearch 會將您的索引新增至左側導覽窗格。

或者，您也可以使用 Query Workbench 在資料表上手動建立涵蓋索引。從下拉式選單中選取您的資料來源，然後執行類似下列的查詢：

```sql
CREATE INDEX vpc_covering_index
ON datasourcename.gluedatabasename.vpclogstable (version, account_id, interface_id, 
srcaddr, dstaddr, srcport, dstport, protocol, packets, 
bytes, start, action, log_status STRING, 
`aws-account-id`, `aws-service`, `aws-region`, year, 
month, day, hour )
WITH (
  auto_refresh = true,
  refresh_interval = '15 minute',
  checkpoint_location = 's3://accountnum-vpcflow/AWSLogs/checkpoint'
)
```

## 具體化檢視

透過 _具體化檢視_，您可以使用複雜的查詢（例如彙總）來支援 Dashboards 視覺化。具體化檢視會依據查詢，將少量資料匯入 OpenSearch。接著，OpenSearch 會從匯入的資料形成索引，供您用於視覺化。您可以使用 Index State Management 管理具體化檢視索引。如需詳細資訊，請參閱 [Index State Management]({{site.url}}{{site.baseurl}}/im-plugin/ism/index/)。

### 定義具體化檢視設定

1. 在 **Index name** 中，輸入有效的索引名稱。請注意，每個資料表可以有多個涵蓋索引。
2. 選擇 **Refresh type**。根據預設，OpenSearch 會自動重新整理索引。否則，您必須使用 `REFRESH` 陳述式手動觸發重新整理。
3. 輸入 **Checkpoint location**，這是重新整理作業檢查點的路徑。此位置必須是與 HDFS 相容之檔案系統中的路徑。
4. 輸入 **Watermark delay**，此值定義資料最晚可延遲多久送達且仍會被處理，例如 1 分鐘或 10 秒。
5. 在 **Materialized view definition** 下定義涵蓋索引欄位。
6. 選取 **Create acceleration** 以套用您的具體化檢視索引設定。
7. 檢視具體化檢視查詢的詳細資訊，然後按一下 **Run**。OpenSearch 會將您的索引新增至左側導覽窗格。

或者，您也可以使用 Query Workbench 在資料表上手動建立具體化檢視索引。從下拉式選單中選取您的資料來源，然後執行如下的查詢：

```sql
CREATE MATERIALIZED VIEW {table_name}__week_live_mview AS
  SELECT
    cloud.account_uid AS `aws.vpc.cloud_account_uid`,
    cloud.region AS `aws.vpc.cloud_region`,
    cloud.zone AS `aws.vpc.cloud_zone`,
    cloud.provider AS `aws.vpc.cloud_provider`,

    CAST(IFNULL(src_endpoint.port, 0) AS LONG) AS `aws.vpc.srcport`,
    CAST(IFNULL(src_endpoint.svc_name, 'Unknown') AS STRING)  AS `aws.vpc.pkt-src-aws-service`,
    CAST(IFNULL(src_endpoint.ip, '0.0.0.0') AS STRING)  AS `aws.vpc.srcaddr`,
    CAST(IFNULL(src_endpoint.interface_uid, 'Unknown') AS STRING)  AS `aws.vpc.src-interface_uid`,
    CAST(IFNULL(src_endpoint.vpc_uid, 'Unknown') AS STRING)  AS `aws.vpc.src-vpc_uid`,
    CAST(IFNULL(src_endpoint.instance_uid, 'Unknown') AS STRING)  AS `aws.vpc.src-instance_uid`,
    CAST(IFNULL(src_endpoint.subnet_uid, 'Unknown') AS STRING)  AS `aws.vpc.src-subnet_uid`,

    CAST(IFNULL(dst_endpoint.port, 0) AS LONG) AS `aws.vpc.dstport`,
    CAST(IFNULL(dst_endpoint.svc_name, 'Unknown') AS STRING) AS `aws.vpc.pkt-dst-aws-service`,
    CAST(IFNULL(dst_endpoint.ip, '0.0.0.0') AS STRING)  AS `aws.vpc.dstaddr`,
    CAST(IFNULL(dst_endpoint.interface_uid, 'Unknown') AS STRING)  AS `aws.vpc.dst-interface_uid`,
    CAST(IFNULL(dst_endpoint.vpc_uid, 'Unknown') AS STRING)  AS `aws.vpc.dst-vpc_uid`,
    CAST(IFNULL(dst_endpoint.instance_uid, 'Unknown') AS STRING)  AS `aws.vpc.dst-instance_uid`,
    CAST(IFNULL(dst_endpoint.subnet_uid, 'Unknown') AS STRING)  AS `aws.vpc.dst-subnet_uid`,
    CASE
      WHEN regexp(dst_endpoint.ip, '(10\\..*)|(192\\.168\\..*)|(172\\.1[6-9]\\..*)|(172\\.2[0-9]\\..*)|(172\\.3[0-1]\\.*)')
        THEN 'ingress'
      ELSE 'egress'
      END AS `aws.vpc.flow-direction`,

    CAST(IFNULL(connection_info['protocol_num'], 0) AS INT) AS `aws.vpc.connection.protocol_num`,
    CAST(IFNULL(connection_info['tcp_flags'], '0') AS STRING)  AS `aws.vpc.connection.tcp_flags`,
    CAST(IFNULL(connection_info['protocol_ver'], '0') AS STRING)  AS `aws.vpc.connection.protocol_ver`,
    CAST(IFNULL(connection_info['boundary'], 'Unknown') AS STRING)  AS `aws.vpc.connection.boundary`,
    CAST(IFNULL(connection_info['direction'], 'Unknown') AS STRING)  AS `aws.vpc.connection.direction`,

    CAST(IFNULL(traffic.packets, 0) AS LONG) AS `aws.vpc.packets`,
    CAST(IFNULL(traffic.bytes, 0) AS LONG) AS `aws.vpc.bytes`,

    CAST(FROM_UNIXTIME(time / 1000) AS TIMESTAMP) AS `@timestamp`,
    CAST(FROM_UNIXTIME(start_time / 1000) AS TIMESTAMP) AS `start_time`,
    CAST(FROM_UNIXTIME(start_time / 1000) AS TIMESTAMP) AS `interval_start_time`,
    CAST(FROM_UNIXTIME(end_time / 1000) AS TIMESTAMP) AS `end_time`,
    status_code AS `aws.vpc.status_code`,

    severity AS `aws.vpc.severity`,
    class_name AS `aws.vpc.class_name`,
    category_name AS `aws.vpc.category_name`,
    activity_name AS `aws.vpc.activity_name`,
    disposition AS `aws.vpc.disposition`,
    type_name AS `aws.vpc.type_name`,

    region AS `aws.vpc.region`,
    accountid AS `aws.vpc.account-id`
  FROM
  datasourcename.gluedatabasename.vpclogstable 
WITH (
  auto_refresh = true,
  refresh_interval = '15 Minute',
  checkpoint_location = 's3://accountnum-vpcflow/AWSLogs/checkpoint',
  watermark_delay = '1 Minute',
)
```

## 限制

此功能仍在開發中，因此有一些限制。如需即時更新，請參閱 [GitHub 上的開發人員文件](https://github.com/opensearch-project/opensearch-spark/blob/main/docs/index.md#limitations)。
