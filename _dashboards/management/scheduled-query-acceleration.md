---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "排程查詢加速"
parent: Connecting data sources
nav_order: 50
has_children: false
---

# 排程查詢加速
於 2.17 版推出
{: .label .label-purple }

排程查詢加速 (Scheduled Query Acceleration，SQA) 旨在最佳化從 OpenSearch 直接傳送至外部資料來源（例如 Amazon Simple Storage Service (Amazon S3)）的查詢。它透過自動化來解決管理及重新整理索引、檢視和資料時常見的問題。

查詢加速是透過次要索引來實現，例如[略過索引]({{site.url}}{{site.baseurl}}/dashboards/management/accelerate-external-data/#skipping-indexes)、[涵蓋索引]({{site.url}}{{site.baseurl}}/dashboards/management/accelerate-external-data/#covering-indexes)或[具體化檢視]({{site.url}}{{site.baseurl}}/dashboards/management/accelerate-external-data/#materialized-views)。執行查詢時，查詢會使用這些索引，而不是直接查詢 Amazon S3。

次要索引需要定期重新整理，才能與 Amazon S3 資料保持同步。此重新整理作業可以使用內部排程器（在 Spark 內）或外部排程器進行排程。

SQA 提供下列優點：

- **透過最佳化資源使用來降低成本**：SQA 可減輕驅動程式節點的作業負載，降低為索引和檢視維持自動重新整理的相關成本。

- **提升重新整理作業的可觀測性**：SQA 提供索引狀態和重新整理時間的可見性，讓您深入了解資料處理情形及目前的系統狀態。

- **更有效地控制重新整理排程**：SQA 可彈性排程重新整理間隔，協助您依據特定需求管理資源使用量和重新整理頻率。

- **簡化索引管理**：SQA 可讓您在單一查詢中更新索引設定（例如重新整理間隔），進而簡化工作流程。

## 概念

設定 SQA 之前，請先熟悉下列主題：

- [使用 OpenSearch 索引最佳化查詢效能]({{site.url}}{{site.baseurl}}/dashboards/management/accelerate-external-data/)
- [Flint 索引重新整理](https://github.com/opensearch-project/opensearch-spark/blob/main/docs/index.md#flint-index-refresh)
- [Index State Management](https://github.com/opensearch-project/opensearch-spark/blob/main/docs/index.md#index-state-transition-1)

## 先決條件

設定 SQA 之前，請確認符合下列需求：

- 請確定您執行的是 OpenSearch 2.17 版或更新版本。
- 請確定您已安裝 SQL 外掛程式。大多數 OpenSearch 發行版本都包含 SQL 外掛程式。如需更多資訊，請參閱[管理 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)。
- 請確定您已設定資料來源（在此範例中為 Amazon S3）：設定略過索引、涵蓋索引或具體化檢視。這些次要資料來源是額外的資料結構，可透過最佳化傳送至外部資料來源（例如 Amazon S3）的查詢來提升查詢效能。如需更多資訊，請參閱[使用 OpenSearch 索引最佳化查詢效能]({{site.url}}{{site.baseurl}}/dashboards/management/accelerate-external-data/)。
- 設定 Amazon EMR Serverless（存取 Apache Spark 時需要）。

## 設定 SQA 設定

若要覆寫預設組態值，請變更下列叢集設定：

-  **啟用非同步查詢執行**：將 `plugins.query.executionengine.async_query.enabled` 設為 `true`（預設值）：
    ```json
    PUT /_cluster/settings
    {
      "transient": {
        "plugins.query.executionengine.async_query.enabled": "true"
      }
    }
    ```
    {% include copy-curl.html %}

    如需更多資訊，請參閱[設定](https://github.com/opensearch-project/sql/blob/main/docs/user/admin/settings.rst#pluginsqueryexecutionengineasync_queryenabled)。

- **設定非同步查詢的外部排程器間隔**：此設定定義外部排程器檢查工作的頻率，讓您能自訂重新整理頻率。此設定沒有預設值：若此值為空，則預設值來自 `opensearch-spark`，且為 `5 minutes`。根據工作負載量調整間隔，有助於您最佳化資源並管理成本：
    ```json
    PUT /_cluster/settings
    {
      "transient": {
        "plugins.query.executionengine.async_query.external_scheduler.interval": "10 minutes"
      }
    }
    ```
    {% include copy-curl.html %}

    如需更多資訊，請參閱[設定](https://github.com/opensearch-project/sql/blob/main/docs/user/admin/settings.rst#pluginsqueryexecutionengineasync_queryexternal_schedulerinterval)。

## 執行加速查詢

您可以在 [Query Workbench]({{site.url}}{{site.baseurl}}/dashboards/query-workbench/) 中執行加速查詢。若要執行加速查詢，請使用下列語法：

```sql
CREATE SKIPPING INDEX example_index
WITH (
    auto_refresh = true,
    refresh_interval = '15 minutes'
);
```
{% include copy.html %}

根據預設，查詢會使用外部排程器。若要使用內部排程器，請將 `scheduler_mode` 設為 `internal`：

```sql
CREATE SKIPPING INDEX example_index
WITH (
    auto_refresh = true,
    refresh_interval = '15 minutes',
    scheduler_mode = 'internal'
);
```
{% include copy.html %}

## 參數

使用加速查詢建立索引時，您可以在 `WITH` 子句中指定下列參數，以控制重新整理行為、排程和時間。

| 參數  | 說明  | 
|:--- | :--- | 
| `auto_refresh`      | 為索引啟用自動重新整理。若為 `true`，索引會依指定的間隔自動重新整理。若為 `false`，則必須使用 `REFRESH` 陳述式手動觸發重新整理作業。預設為 `false`。   |
| `refresh_interval`  | 定義索引各次重新整理作業之間的時間長度，這決定了新資料匯入索引的頻率。僅在啟用 `auto_refresh` 時適用。此間隔決定整合新資料的頻率，可使用 `1 minute` 或 `10 seconds` 等格式指定。如需有效的時間單位，請參閱[時間單位](#time-units)。| 
| `scheduler_mode`    | 指定自動重新整理的排程模式（內部或外部排程）。外部排程器需要 `checkpoint_location`（重新整理工作檢查點的路徑）以進行狀態管理。如需更多資訊，請參閱[啟動串流查詢](https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html#starting-streaming-queries)。有效值為 `internal` 和 `external`。| 

如需更多資訊及其他可用參數，請參閱 [Flint 索引重新整理](https://github.com/opensearch-project/opensearch-spark/blob/main/docs/index.md#flint-index-refresh)。

## 時間單位

定義時間間隔時，您可以指定下列時間單位：

- 毫秒：`ms`、`millisecond` 或 `milliseconds`
- 秒：`s`、`second` 或 `seconds`
- 分鐘：`m`、`minute` 或 `minutes`
- 小時：`h`、`hour` 或 `hours`
- 天：`d`、`day` 或 `days`

## 監控索引狀態

若要監控索引的狀態，請使用下列陳述式：

```sql
SHOW FLINT INDEXES IN spark_catalog.default;
```
{% include copy.html %}

## 管理排程工作

使用下列命令來管理排程工作。

### 啟用工作

若要停用使用內部或外部排程器的自動重新整理，請將 `auto_refresh` 設為 `false`：

```sql
ALTER MATERIALIZED VIEW myglue_test.default.count_by_status_v9 WITH (auto_refresh = false);
```
{% include copy.html %}

### 更新排程

若要更新排程並修改重新整理設定，請在 `WITH` 子句中指定 `refresh_interval`：

```sql
ALTER INDEX example_index
WITH (refresh_interval = '30 minutes');
```
{% include copy.html %}

### 切換排程器模式

若要切換排程器模式，請在 `WITH` 子句中指定 `scheduler_mode`：

```sql
ALTER MATERIALIZED VIEW myglue_test.default.count_by_status_v9 WITH (scheduler_mode = 'internal');
```
{% include copy.html %}

### 檢查排程器中繼資料

若要檢查排程器中繼資料，請使用下列請求：

```json
GET /.async-query-scheduler/_search
```
{% include copy-curl.html %}

## 最佳做法

使用 SQA 時，建議您遵循下列最佳做法。

### 效能最佳化

- **建議的重新整理間隔**：選擇適當的重新整理間隔，對於平衡資源使用量和系統效能至關重要。設定間隔時，請考量您的工作負載需求以及所需的資料新鮮度。

- **並行工作限制**：限制同時執行的工作數量，以避免系統資源超載。請監控系統容量並據以調整工作限制，以確保最佳效能。

- **資源使用量**：有效率的資源配置是發揮最大效能的關鍵。請根據工作負載及您執行的查詢類型，適當配置記憶體、CPU 和 I/O。

### 成本管理

- **使用外部排程器**：外部排程器可分擔重新整理作業，減少對核心驅動程式節點的需求。

- **依您的使用案例設定重新整理間隔**：較長的重新整理間隔可降低成本，但可能影響資料新鮮度。

- **最佳化重新整理排程**：根據工作負載模式調整重新整理間隔，以減少不必要的重新整理作業。

- **監控成本**：定期監控與排程查詢及重新整理作業相關的成本。使用可觀測性工具，有助於您深入了解一段時間內的資源使用量和成本。

## 驗證設定

您可以執行測試查詢並驗證排程器組態，以驗證您的設定：

```sql
SHOW FLINT INDEXES EXTENDED
```
{% include copy.html %}

如需更多資訊，請參閱 [OpenSearch Spark 文件](https://github.com/opensearch-project/opensearch-spark/blob/main/docs/index.md#all-indexes)。

## 疑難排解

若重新整理作業未如預期觸發，請確定已啟用 `auto_refresh` 設定，且已正確設定重新整理間隔。
