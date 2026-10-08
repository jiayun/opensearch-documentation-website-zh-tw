---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Hadoop 連接器"
nav_order: 110
---

# Hadoop 連接器

OpenSearch Hadoop 連接器可讓您在 [Apache Spark](http://spark.apache.org)、[Apache Hive](http://hive.apache.org)、Hadoop MapReduce 與 OpenSearch 之間讀取和寫入資料。它使 Spark 工作能夠直接將資料編製索引至 OpenSearch 並對其執行查詢，並透過跨 Spark 分割區與 OpenSearch 分片的平行讀寫，實現有效率的分散式處理。

原始碼請參閱 [OpenSearch Hadoop](https://github.com/opensearch-project/opensearch-hadoop) 儲存庫。

## 設定

使用 `--packages` 將連接器加入您的 Spark 應用程式：

- 若為 Spark 3.4.x，請執行以下命令：

```bash
pyspark --packages org.opensearch.client:opensearch-spark-30_2.12:2.0.0
```
{% include copy.html %}

- 若為 Spark 3.5.x，請執行以下命令：

```bash
pyspark --packages org.opensearch.client:opensearch-spark-35_2.12:2.0.0
```
{% include copy.html %}

- 若為 Spark 4.x，請執行以下命令：

```bash
pyspark --packages org.opensearch.client:opensearch-spark-40_2.13:2.0.0
```
{% include copy.html %}

或者，在您的建置檔案中將 Spark 加入為相依性：

```xml
<dependency>
    <groupId>org.opensearch.client</groupId>
    <artifactId>opensearch-spark-30_2.12</artifactId>
    <version>2.0.0</version>
</dependency>
```
{% include copy.html %}

請從下表中選擇符合您 Spark 與 Scala 版本的成品。

Spark 版本 | Scala 版本 | 成品
:--- | :--- | :---
3.4.x | 2.12 | `org.opensearch.client:opensearch-spark-30_2.12:2.0.0`
3.4.x | 2.13 | `org.opensearch.client:opensearch-spark-30_2.13:2.0.0`
3.5.x | 2.12 | `org.opensearch.client:opensearch-spark-35_2.12:2.0.0`
3.5.x | 2.13 | `org.opensearch.client:opensearch-spark-35_2.13:2.0.0`
4.x | 2.13 | `org.opensearch.client:opensearch-spark-40_2.13:2.0.0`

## 基本用法

以下範例示範如何使用連接器搭配不同的 Spark API 執行基本的讀取與寫入操作。

### PySpark

不需要額外的 Python 套件。Java 連接器會透過 `--packages` 或 `spark.jars` 載入：

```python
# Write (index documents into OpenSearch)
df = spark.createDataFrame([("John", 30), ("Jane", 25)], ["name", "age"])
df.write.format("opensearch").save("people")

# Read (query documents from OpenSearch)
df = spark.read.format("opensearch").load("people")
df.show()

# Read with a query (only matching documents are transferred to Spark)
filtered = spark.read \
    .format("opensearch") \
    .option("opensearch.query", '{"query":{"match":{"name":"John"}}}') \
    .load("people")
```
{% include copy.html %}

### Scala

使用 Scala API 存取 `saveToOpenSearch` 等輔助方法，以取得更簡潔的語法：

```scala
import org.opensearch.spark.sql._

// Write (index documents into OpenSearch)
val df = spark.createDataFrame(Seq(("John", 30), ("Jane", 25))).toDF("name", "age")
df.saveToOpenSearch("people")

// Read (query documents from OpenSearch)
val result = spark.read.format("opensearch").load("people")
result.show()

// Read with a query
val filtered = spark.read
  .format("opensearch")
  .option("opensearch.query", """{"query":{"match":{"name":"John"}}}""")
  .load("people")
```
{% include copy.html %}

### Java

在 Java 應用程式中使用 `JavaOpenSearchSparkSQL` 包裝類別：

```java
import org.opensearch.spark.sql.api.java.JavaOpenSearchSparkSQL;

// Write
Dataset<Row> df = spark.createDataFrame(data, schema);
JavaOpenSearchSparkSQL.saveToOpenSearch(df, "people");

// Read
Dataset<Row> result = spark.read().format("opensearch").load("people");
result.show();
```
{% include copy.html %}

### Spark SQL

您可以將 OpenSearch 索引註冊為暫時檢視，並使用 SQL 查詢它：

```python
spark.sql("""
  CREATE TEMPORARY VIEW people
  USING opensearch
  OPTIONS (resource 'people')
""")

spark.sql("SELECT * FROM people WHERE age > 25").show()
```
{% include copy.html %}

## 寫入操作

設定文件寫入 OpenSearch 索引的方式，包括文件 ID、寫入模式與路由策略。

### 指定文件 ID

使用 `opensearch.mapping.id` 控制每個文件的 `_id`：

```python
df.write.format("opensearch") \
    .option("opensearch.mapping.id", "id") \
    .save("my-index")
```
{% include copy.html %}

### 寫入模式

使用 Spark 的寫入模式控制資料寫入 OpenSearch 的方式：

```python
# Append (default): add documents to the index
df.write.format("opensearch").mode("append").save("my-index")

# Overwrite: delete the index and recreate it with the new data
df.write.format("opensearch").mode("overwrite").save("my-index")
```
{% include copy.html %}

### Upsert

若文件存在則更新，若不存在則插入為新文件。此操作需要指定文件 ID 欄位：

```python
df.write.format("opensearch") \
    .option("opensearch.mapping.id", "id") \
    .option("opensearch.write.operation", "upsert") \
    .save("my-index")
```
{% include copy.html %}

### 動態索引路由

在索引名稱中使用預留位置，即可根據欄位值將文件路由至不同的索引。此功能需要 Scala 的 `saveToOpenSearch` 方法：

```scala
import org.opensearch.spark.sql._

// Route by field value: {"category": "electronics", "name": "TV"} -> index "electronics"
df.saveToOpenSearch("{category}")

// Prefix + field value: {"env": "prod", "msg": "ok"} -> index "logs-prod"
df.saveToOpenSearch("logs-{env}")

// Date formatting: {"timestamp": "2026-02-16T10:30:00.000Z", "msg": "ok"} -> index "logs-2026.02.16"
df.saveToOpenSearch("logs-{timestamp|yyyy.MM.dd}")
```
{% include copy.html %}

## 讀取操作

透過篩選查詢與選取特定欄位來最佳化從 OpenSearch 擷取資料的過程，以減少資料傳輸量。

### 使用查詢讀取

在 OpenSearch 層級篩選資料，只將符合條件的文件載入 Spark：

```python
# Query DSL
df = spark.read.format("opensearch") \
    .option("opensearch.query", '{"query":{"range":{"age":{"gte":25}}}}') \
    .load("my-index")

# URI query
df = spark.read.format("opensearch") \
    .option("opensearch.query", "?q=name:John") \
    .load("my-index")
```
{% include copy.html %}

### 選取欄位

僅載入特定欄位以減少資料傳輸量：

```python
df = spark.read.format("opensearch") \
    .option("opensearch.read.field.include", "name,age") \
    .load("my-index")
```
{% include copy.html %}

## 安全性

使用驗證與加密保護 OpenSearch 叢集的連線安全。

### 基本驗證

為已啟用驗證的 OpenSearch 叢集提供憑證：

```python
df.write.format("opensearch") \
    .option("opensearch.net.http.auth.user", "<username>") \
    .option("opensearch.net.http.auth.pass", "<password>") \
    .save("my-index")
```
{% include copy.html %}

### HTTPS

啟用 SSL/TLS 加密以確保連線安全：

```python
df.write.format("opensearch") \
    .option("opensearch.net.ssl", "true") \
    .save("my-index")
```
{% include copy.html %}

## 進階 Spark 功能

存取低階 Spark API 與串流功能，以應對特殊使用情境。

### Spark 彈性分散式資料集

若需低階存取，連接器提供以彈性分散式資料集 (RDD) 為基礎的讀取與寫入方法：

```scala
import org.opensearch.spark._

// Write
val data = sc.makeRDD(Seq(
  Map("name" -> "John", "age" -> 30),
  Map("name" -> "Jane", "age" -> 25)
))
data.saveToOpenSearch("people")

// Read
val rdd = sc.opensearchRDD("people")
rdd.collect().foreach(println)

// Read with query
val filtered = sc.opensearchRDD("people", "?q=name:John")
```
{% include copy.html %}

### Spark Structured Streaming

此連接器支援將 Spark Structured Streaming 作為接收端：

```scala
val query = streamingDF.writeStream
  .format("opensearch")
  .option("checkpointLocation", "/tmp/checkpoint")
  .start("streaming-index")
```
{% include copy.html %}

## 替代介面

您可以將此連接器與 Hadoop MapReduce 和 Apache Hive 搭配使用，以進行替代工作流程。

### Hadoop MapReduce

對於 Hadoop MapReduce 工作，此連接器提供 `OpenSearchInputFormat` 和 `OpenSearchOutputFormat`。請將 `opensearch-hadoop-mr-2.0.0.jar` 加入您工作的 `classpath`。

```java
// Writing
Configuration conf = new Configuration();
conf.set("opensearch.resource", "my-index");
Job job = new Job(conf);
job.setOutputFormatClass(OpenSearchOutputFormat.class);
job.waitForCompletion(true);

// Reading
Configuration conf = new Configuration();
conf.set("opensearch.resource", "my-index");
Job job = new Job(conf);
job.setInputFormatClass(OpenSearchInputFormat.class);
job.waitForCompletion(true);
```
{% include copy.html %}

### Apache Hive

此連接器提供 Apache Hive 儲存處理器。請將 `opensearch-hadoop-hive-2.0.0.jar` 加入您的 Hive classpath：

```sql
ADD JAR /path/opensearch-hadoop-hive-2.0.0.jar;

CREATE EXTERNAL TABLE people (
    name STRING,
    age  INT)
STORED BY 'org.opensearch.hadoop.hive.OpenSearchStorageHandler'
TBLPROPERTIES('opensearch.resource' = 'people');

SELECT * FROM people;
```
{% include copy.html %}

## 連線至 Amazon OpenSearch Service

若要透過 IAM 驗證連線至 Amazon OpenSearch Service，請啟用 AWS Signature Version 4 簽署與 HTTPS：

```python
df.write.format("opensearch") \
    .option("opensearch.nodes", "https://search-xxx.us-east-1.es.amazonaws.com") \
    .option("opensearch.port", "443") \
    .option("opensearch.net.ssl", "true") \
    .option("opensearch.nodes.wan.only", "true") \
    .option("opensearch.aws.sigv4.enabled", "true") \
    .option("opensearch.aws.sigv4.region", "us-east-1") \
    .save("my-index")
```
{% include copy.html %}

在 `classpath` 上需要下列 AWS SDK v2 相依套件：
- `software.amazon.awssdk:auth:2.31.59` (或更新版本)
- `software.amazon.awssdk:regions:2.31.59` (或更新版本)
- `software.amazon.awssdk:http-client-spi:2.31.59` (或更新版本)
- `software.amazon.awssdk:identity-spi:2.31.59` (或更新版本)
- `software.amazon.awssdk:sdk-core:2.31.59` (或更新版本)
- `software.amazon.awssdk:utils:2.31.59` (或更新版本)

## 連線至 Amazon OpenSearch Serverless

若要連線至 Amazon OpenSearch Serverless，請新增 `opensearch.serverless` 並將 Signature Version 4 服務名稱設定為 `aoss`：

```python
df.write.format("opensearch") \
    .option("opensearch.nodes", "https://xxx.us-east-1.aoss.amazonaws.com") \
    .option("opensearch.port", "443") \
    .option("opensearch.net.ssl", "true") \
    .option("opensearch.nodes.wan.only", "true") \
    .option("opensearch.aws.sigv4.enabled", "true") \
    .option("opensearch.aws.sigv4.region", "us-east-1") \
    .option("opensearch.aws.sigv4.service.name", "aoss") \
    .option("opensearch.serverless", "true") \
    .save("my-index")
```
{% include copy.html %}

## 組態屬性

所有組態屬性都以 `opensearch` 前綴開頭。屬性可以透過 Spark 組態 (`--conf`)、`DataFrame` 讀取器/寫入器的選項，或 Hadoop 組態來設定。

屬性 | 預設值 | 說明
:--- | :--- | :---
`opensearch.resource` | (none) | OpenSearch 索引名稱。也可以指定為 `saveToOpenSearch()` 或 `load()` 的引數。
`opensearch.nodes` | `localhost` | OpenSearch 主機位址。
`opensearch.port` | `9200` | OpenSearch REST 連接埠。
`opensearch.nodes.wan.only` | `false` | 透過負載平衡器或代理伺服器連線時，請設定為 `true`。
`opensearch.query` | match all | 用於讀取的 Query DSL 或統一資源識別碼 (URI) 查詢。
`opensearch.net.ssl` | `false` | 啟用 HTTPS。
`opensearch.mapping.id` | (none) | 用作 `_id` 的文件欄位。
`opensearch.write.operation` | `index` | 寫入操作：`index`、`create`、`update` 或 `upsert`。
`opensearch.scroll.size` | `1000` | 讀取時每批擷取的文件數。
`opensearch.read.field.include` | (none) | 要讀取的欄位清單，以逗號分隔。

## 相容性

下表列出連接器版本及其相容的執行階段版本。

用戶端版本 | 最低 Java 執行階段版本 | OpenSearch 版本 | Spark 版本
:--- | :--- | :--- | :---
1.0.0--1.3.0 | Java 8 | 1.x, 2.x | 3.4.x
2.0.0 | Java 11 | 1.x, 2.x, 3.x | 3.4.x, 3.5.x, 4.x

