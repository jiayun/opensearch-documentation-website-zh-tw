---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "依查詢與依桶監視器"
nav_order: 5
parent: Monitors
grand_parent: Alerting
has_children: false
---

# 依查詢與依桶監視器

依查詢與依桶監視器會依排程執行查詢，並使用觸發條件評估結果：

- _依查詢監視器_ 會將查詢結果視為整體來評估。例如，當符合的文件數超過閾值時，它可以產生警示。依查詢監視器中的觸發條件一次最多只會有一個作用中的警示。
- _依桶監視器_ 會使用一個或多個欄位將查詢結果分組為桶，並分別評估每個桶。例如，它可以為每個請求數超過閾值的主機或國家/地區分別產生警示。

本頁的範例使用 OpenSearch Dashboards 的範例網路記錄。若要新增範例資料，請在 OpenSearch Dashboards 首頁選取 **Add sample data**，然後在 **Sample web logs** 卡片上選取 **Add data**。

## 建立依查詢監視器

下列範例會建立一個監視器，在網站一天內收到超過 100 個請求時產生警示。

若要建立監視器，請依照下列步驟操作：

1. 在頂端選單中，前往 **OpenSearch Plugins** > **Alerting**。
1. 選取 **Monitors** 索引標籤，然後選取 **Create monitor**。
1. 在 **Monitor details** 中，設定下列設定：
   - **Monitor name**：輸入 `Daily web traffic`。
   - **Monitor type**：選取 **Per query monitor**。
   - **Monitor defining method**：選取 **Visual editor**。若要使用查詢領域專用語言（DSL）撰寫查詢，請改為選取 **Extraction query editor**。如需詳細資訊，請參閱[使用擷取查詢編輯器定義查詢](#defining-the-query-using-the-extraction-query-editor)。若要根據異常偵測結果產生警示，請選取 **Anomaly detector**。如需詳細資訊，請參閱[將監視器與異常偵測器配對](#pairing-a-monitor-with-an-anomaly-detector)。
   - **Schedule**：保留預設值，每分鐘執行一次監視器。若要在特定時間執行監視器，請選取 **Daily**、**Weekly**、**Monthly** 或 **Custom cron expression**，然後選取時區。如需 cron 運算式的詳細資訊，請參閱 [cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/cron-expressions/)。
1. 在 **Select data** 的 **Indexes** 中，輸入 `opensearch_dashboards_sample_data_logs` 並按 Enter。在 **Time field** 中，選取 `timestamp`。

   如果您使用 Security 外掛程式，則只能選取您有權存取的索引。如需詳細資訊，請參閱[警示安全性]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/security/)。
1. 在 **Query** 中，設定查詢：
   - **Metrics**：保留 **COUNT OF documents**。若要使用其他彙總，例如數值欄位的平均值或最大值，請選取 **Add metric**。
   - **Time range for the last**：輸入 `1` 並選取 **day(s)**。
   - **Data filter**：您可以選取 **Add filter**，以監視部分文件。

   若要檢視查詢及其執行所需的時間，請展開 **Preview query and performance**。監視器會依排程指定的頻率執行此查詢，因此請確認其效能可以接受。
1. 在 **Triggers** 中，選取 **Add trigger**，然後設定觸發條件：
   - **Trigger name**：輸入 `More than 100 requests`。
   - **Severity level**：保留 **1 (Highest)**。
   - **Trigger condition**：選取 **IS ABOVE** 並輸入 `100`。

   觸發條件預覽會顯示所選時間範圍內的文件數量。如需詳細資訊，請參閱[觸發條件]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/triggers/)。
1. 您可以在 **Actions** 中新增動作，以在符合觸發條件時傳送通知。動作需要通知管道。如果您尚未建立通知管道，請選取 **Manage channels** 來建立。如需詳細資訊，請參閱[動作]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/actions/)。
1. 選取 **Create**。

由於範例網站記錄檔通常包含一天內超過 100 個請求的記錄，因此會符合觸發條件，監視器便會產生處於 **Active** 狀態的警示。若要檢視警示，請在 **Alerting** 頁面上選取 **Alerts** 索引標籤。

## 建立依桶監視器

以下範例建立一個監視器，為一天內送出超過 20 個請求的每個國家分別產生警示。

若要建立此監視器，請依照下列步驟操作：

1. 在頂端選單中，前往 **OpenSearch Plugins** > **Alerting**。
1. 選取 **Monitors** 索引標籤，然後選取 **Create monitor**。
1. 在 **Monitor details** 中，輸入 **Monitor name**，例如 `Daily requests by country`。在 **Monitor type** 中，選取 **Per bucket monitor**。在 **Monitor defining method** 中，選取 **Visual editor**。
1. 在 **Select data** 中，於 **Indexes** 輸入 `opensearch_dashboards_sample_data_logs` 並按 Enter。在 **Time field** 中，選取 `timestamp`。
1. 在 **Query** 中，設定查詢：
   - **Metrics**：保留 **COUNT OF documents**。
   - **Time range for the last**：輸入 `1` 並選取 **day(s)**。
   - **Group by**：選取 **Add group by**，然後選取 `geo.src` 欄位。依桶監視器至少需要一個 group-by 欄位。
1. 在 **Triggers** 中，選取 **Add trigger**，然後設定觸發條件：
   - **Trigger name**：輸入 `More than 20 requests`。
   - **Trigger conditions**：在 **Metric** 中，保留 **Count of documents**。在 **Threshold** 中，選取 **IS ABOVE**。在 **Value** 中，輸入 `20`。
   - **Keyword filter**：選用，可選取 **Add filter**，僅評估其 group-by 值符合關鍵字的桶。
1. 選用：在 **Actions** 中，新增一項動作，為符合觸發條件的每個桶傳送通知。
1. 選取 **Create**。

監視器會為請求數超過門檻的每個國家產生警示。每個警示都會包含桶鍵 (bucket key)，例如 `CN`。

## 使用擷取查詢編輯器定義查詢

若要使用 [query DSL]({{site.url}}{{site.baseurl}}/query-dsl/index/) 定義查詢，請在 **Monitor defining method** 中選取 **Extraction query editor**。接著在 **Query** 中輸入查詢，並選取 **Run** 進行測試。**Monitor performance** 面板會顯示查詢執行所需的時間，以及傳回的文件數量。

若要將查詢限制在每次監視器執行的時間範圍內，請使用 `{% raw %}{{period_end}}{% endraw %}` 變數。下列查詢會傳回每次監視器執行前一天內的 `404` 回應數量：

```json
{% raw %}{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        {
          "range": {
            "timestamp": {
              "gte": "{{period_end}}||-1d",
              "lte": "{{period_end}}",
              "format": "epoch_millis"
            }
          }
        },
        {
          "term": {
            "response.keyword": "404"
          }
        }
      ]
    }
  }
}{% endraw %}
```
{% include copy.html %}

使用擷取查詢編輯器時，您會使用 [Painless]({{site.url}}{{site.baseurl}}/scripting/painless/) 指令碼定義觸發條件。下列條件會在查詢傳回超過 5 份文件時產生警示：

```
ctx.results[0].hits.total.value > 5
```
{% include copy.html %}

若要測試條件，請選取 **Preview condition response**。關於觸發條件中可使用的變數，請參閱 [監視器變數]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/monitors/#monitor-variables)。

## 將監視器與異常偵測器配對

若要從[異常偵測器]({{site.url}}{{site.baseurl}}/observing-your-data/ad/index/)的結果產生警示，請建立依查詢監視器，在 **Monitor defining method** 中選取 **Anomaly detector**，然後選取該偵測器。**Anomaly detector** 方法不適用於依桶監視器。

請將監視器間隔設定為至少偵測器間隔的兩倍，否則監視器可能會遺漏異常結果。例如，若監視器與偵測器都是每 5 分鐘執行一次，而您在 12:00 啟動偵測器，則 12:05 偵測到的異常可能要到 12:06 才能用於查詢。監視器會讀取 12:00 到 12:05 的結果，因此會遺漏該異常。當您在 OpenSearch Dashboards 中從偵測器建立監視器時，監視器間隔預設會設定為偵測器間隔的兩倍。

若您變更偵測器的間隔，也必須一併更新監視器間隔。監視器間隔不會自動更新。

## 查詢遠端索引

兩種監視器類型都能查詢遠端叢集上的索引。在 **Select data** 中，於 **Select clusters** 選取遠端叢集，然後選取索引。當您使用擷取查詢編輯器定義查詢時，請使用 [跨叢集搜尋]({{site.url}}{{site.baseurl}}/security/access-control/cross-cluster-search/) 所用的 `<cluster-name>:<index-name>` 模式指定遠端索引。

若要在 OpenSearch Dashboards 中建立跨叢集監視器，您需要下列[權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/)：`cluster:admin/opensearch/alerting/remote/indexes/get`、`indices:admin/resolve/index`、`cluster:monitor/health` 和 `indices:admin/mappings/get`。
{: .note}

下圖顯示為依查詢監視器選取的遠端索引。

![為監視器選取遠端索引]({{site.url}}{{site.baseurl}}/images/alerting/cross-cluster-per-query-per-bucket-monitors.png){: width="700" }
