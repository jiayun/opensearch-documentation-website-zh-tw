---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Job Scheduler
nav_order: 1
has_children: true
has_toc: false
redirect_from:
  - /job-scheduler-plugin/index/
  - /monitoring-your-cluster/job-scheduler/
---

# Job Scheduler

OpenSearch Job Scheduler 外掛程式提供一個框架，可用來為叢集上執行的常見工作建立排程。您可以使用 Job Scheduler 的服務提供者介面 (SPI)，為叢集管理工作定義排程，例如建立快照、管理資料的生命週期，以及執行定期作業。Job Scheduler 具有一個清掃器 (sweeper) 和一個排程器：清掃器會監聽 OpenSearch 叢集上的更新事件，排程器則負責管理作業的執行時間。

您可以依照標準的 [OpenSearch 外掛程式安裝]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/plugins/)程序安裝 Job Scheduler 外掛程式。[Job Scheduler GitHub 儲存庫](https://github.com/opensearch-project/job-scheduler)中提供的 sample-extension-plugin 範例，完整示範了如何在建置外掛程式時使用 Job Scheduler。若要定義排程，您需要建置一個外掛程式，實作 Job Scheduler 程式庫所提供的介面。您可以指定時間間隔來排程作業，也可以使用 Unix cron 運算式 (例如 `0 12 * * ?`，表示每天中午執行) 來定義更彈性的排程。

## 為 Job Scheduler 建置外掛程式

OpenSearch 外掛程式開發人員可以擴充 Job Scheduler 外掛程式，以排程要在叢集上執行的作業。您可以排程的作業包括：對原始資料執行彙總查詢，並每小時將彙總後的資料儲存到新索引；或是透過呼叫 OpenSearch API 持續監視分片配置，再將輸出內容張貼到 webhook。

如需建置使用 Job Scheduler 外掛程式之外掛程式的範例，請參閱 Job Scheduler [`README`](https://github.com/opensearch-project/job-scheduler/blob/main/README.md)。

## 定義端點

您可以參考[範例](https://github.com/opensearch-project/job-scheduler/blob/main/sample-extension-plugin/src/main/java/org/opensearch/jobscheduler/sampleextension/SampleExtensionRestHandler.java) `SampleExtensionRestHandler.java` 檔案來設定外掛程式的 API 端點。使用 `WATCH_INDEX_URI` 設定外掛程式要公開的端點 URL：

```java
public class SampleExtensionRestHandler extends BaseRestHandler {
    public static final String WATCH_INDEX_URI = "/_plugins/scheduler_sample/watch";
```

您可以透過[擴充](https://github.com/opensearch-project/job-scheduler/blob/main/sample-extension-plugin/src/main/java/org/opensearch/jobscheduler/sampleextension/SampleJobParameter.java) `ScheduledJobParameter` 來定義作業組態。您也可以定義外掛程式使用的欄位，例如 `indexToWatch`，如[範例](https://github.com/opensearch-project/job-scheduler/blob/main/sample-extension-plugin/src/main/java/org/opensearch/jobscheduler/sampleextension/SampleJobParameter.java) `SampleJobParameter` 檔案所示。此作業組態會以文件形式儲存在您定義的索引中，如[此範例](https://github.com/opensearch-project/job-scheduler/blob/main/sample-extension-plugin/src/main/java/org/opensearch/jobscheduler/sampleextension/SampleExtensionPlugin.java#L54)所示。

## 設定參數

您可以參考[範例](https://github.com/opensearch-project/job-scheduler/blob/main/sample-extension-plugin/src/main/java/org/opensearch/jobscheduler/sampleextension/SampleJobParameter.java) `SampleJobParameter.java` 檔案，並依您的需求修改，以設定外掛程式的參數：

```java
/**
 * A sample job parameter.
 * <p>
 * It adds an additional "indexToWatch" field to {@link ScheduledJobParameter}, which stores the index
 * the job runner will watch.
 */
public class SampleJobParameter implements ScheduledJobParameter {
    public static final String NAME_FIELD = "name";
    public static final String ENABLED_FILED = "enabled";
    public static final String LAST_UPDATE_TIME_FIELD = "last_update_time";
    public static final String LAST_UPDATE_TIME_FIELD_READABLE = "last_update_time_field";
    public static final String SCHEDULE_FIELD = "schedule";
    public static final String ENABLED_TIME_FILED = "enabled_time";
    public static final String ENABLED_TIME_FILED_READABLE = "enabled_time_field";
    public static final String INDEX_NAME_FIELD = "index_name_to_watch";
    public static final String LOCK_DURATION_SECONDS = "lock_duration_seconds";
    public static final String JITTER = "jitter";

    private String jobName;
    private Instant lastUpdateTime;
    private Instant enabledTime;
    private boolean isEnabled;
    private Schedule schedule;
    private String indexToWatch;
    private Long lockDurationSeconds;
    private Double jitter;
```

接著，設定您希望外掛程式搭配 Job Scheduler 使用的請求參數。這些參數將以您設定外掛程式時宣告的變數為基礎。下列範例顯示您在建置外掛程式時設定的請求參數：

```java
public SampleJobParameter(String id, String name, String indexToWatch, Schedule schedule, Long lockDurationSeconds, Double jitter) {
        this.jobName = name;
        this.indexToWatch = indexToWatch;
        this.schedule = schedule;

        Instant now = Instant.now();
        this.isEnabled = true;
        this.enabledTime = now;
        this.lastUpdateTime = now;
        this.lockDurationSeconds = lockDurationSeconds;
        this.jitter = jitter;
    }

    @Override
    public String getName() {
        return this.jobName;
    }

    @Override
    public Instant getLastUpdateTime() {
        return this.lastUpdateTime;
    }

    @Override
    public Instant getEnabledTime() {
        return this.enabledTime;
    }

    @Override
    public Schedule getSchedule() {
        return this.schedule;
    }

    @Override
    public boolean isEnabled() {
        return this.isEnabled;
    }

    @Override
    public Long getLockDurationSeconds() {
        return this.lockDurationSeconds;
    }

    @Override public Double getJitter() {
        return jitter;
    }
```

下表說明上一個範例中設定的請求參數。所示的所有請求參數皆為必要。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `getName` | 字串 | 傳回作業的名稱。 |
| `getLastUpdateTime` | 時間單位 | 傳回作業上次執行的時間。 |
| `getEnabledTime` | 時間單位 | 傳回作業啟用的時間。 |
| `getSchedule` | Unix cron | 傳回以 Unix cron 語法格式化的作業排程。 |
| `isEnabled` | 布林值 | 指出作業是否已啟用。 |
| `getLockDurationSeconds` | 整數 | 傳回作業被鎖定的持續時間。 |
| `getJitter` | 整數 | 傳回已定義的抖動 (jitter) 值。 |

作業所使用的邏輯應定義在 `SampleJobParameter.java` 範例檔案中擴充自 `ScheduledJobRunner` 的類別內，例如 `SampleJobRunner`。作業執行期間，您可以使用鎖定機制來防止其他節點執行相同的作業。首先，[取得](https://github.com/opensearch-project/job-scheduler/blob/main/sample-extension-plugin/src/main/java/org/opensearch/jobscheduler/sampleextension/SampleJobRunner.java#L96)鎖定。接著，請務必在[作業完成](https://github.com/opensearch-project/job-scheduler/blob/main/sample-extension-plugin/src/main/java/org/opensearch/jobscheduler/sampleextension/SampleJobRunner.java#L116)前釋放鎖定。

如需詳細資訊，請參閱 [Job Scheduler GitHub 儲存庫](https://github.com/opensearch-project/job-scheduler)中的 Job Scheduler [範例擴充](https://github.com/opensearch-project/job-scheduler/blob/main/sample-extension-plugin/src/main/java/org/opensearch/jobscheduler/sampleextension/SampleJobParameter.java)目錄。

## Job Scheduler API

Job Scheduler 外掛程式支援下列 API，可用來監視叢集上執行的作業：

- [Jobs API]({{site.url}}{{site.baseurl}}/monitoring-your-cluster/job-scheduler/jobs/)
- [Locks API]({{site.url}}{{site.baseurl}}/monitoring-your-cluster/job-scheduler/locks/)

## Job Scheduler 叢集設定

Job Scheduler 外掛程式支援下列叢集設定。所有設定皆為動態設定。若要進一步了解靜態與動態設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

| 設定 | 資料類型 | 說明 |
:--- | :--- | :---
| `plugins.jobscheduler.jitter_limit` | 雙精度浮點數 | 定義作業執行時間的最大延遲乘數。太多作業同時啟動可能會造成大量資源消耗。為了平衡負載，您可以在啟動時間加上隨機的抖動延遲。例如，若時間間隔為 10 分鐘且抖動值為 0.6，則下一次作業執行將隨機延遲 0 到 6 分鐘之間的時間。 |
| `plugins.jobscheduler.request_timeout` | 時間單位 | 背景清掃的搜尋逾時。背景清掃是指自動排程並執行已註冊的作業。它會依時間間隔執行，逐一檢查每個擴充外掛程式的已註冊作業索引，搜尋要執行的作業。 |
| `plugins.jobscheduler.retry_count` | 整數 | 用於定義指數退避策略的重試次數。退避策略決定大量處理器在重試大量操作前要等待多久。每當大量編製索引請求在請求當下因資源限制而受到影響或遭到拒絕時，就會使用此策略。對 Job Scheduler 外掛程式而言，這會影響已註冊作業索引的搜尋。 |
| `plugins.jobscheduler.sweeper.backoff_millis` | 時間單位 | 用於定義指數退避策略的初始等待時間，單位為毫秒。退避策略決定大量處理器在重試大量操作前要等待多久。每當大量編製索引請求在請求當下因資源限制而受到影響或遭到拒絕時，就會使用此策略。對 Job Scheduler 外掛程式而言，這會影響已註冊作業索引的搜尋。 |
| `plugins.jobscheduler.sweeper.page_size` | 整數 | 設定用於在已註冊作業索引中尋找作業文件的搜尋請求。定義要傳回的搜尋命中數。 |
| `plugins.jobscheduler.sweeper.period` | 時間單位 | 定義執行背景清掃前的初始延遲時間。 |
