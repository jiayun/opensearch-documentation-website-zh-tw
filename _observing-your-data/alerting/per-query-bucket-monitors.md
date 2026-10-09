---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "每個查詢與每個桶監視器"
nav_order: 5
parent: Monitors
grand_parent: Alerting
has_children: false
---

# 每個查詢與每個桶監視器

每個查詢監視器是一種警示監視器，可用來識別並警示針對 OpenSearch 索引執行的特定查詢；例如，偵測並回應特定查詢中異常的查詢。每個查詢監視器一次只會觸發一個警示。

每個桶監視器是一種警示監視器，可用來識別並警示由針對 OpenSearch 索引的查詢所建立的特定資料桶。

這兩種監視器類型都支援使用與[跨叢集搜尋]({{site.url}}{{site.baseurl}}/security/access-control/cross-cluster-search/)相同的 `cluster-name:index-name` 模式查詢遠端索引，或使用 OpenSearch Dashboards 2.12 或更新版本。

若要透過儀表板 UI 建立跨叢集監視器，需要下列[權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/)：`cluster:admin/opensearch/alerting/remote/indexes/get`、`indices:admin/resolve/index`、`cluster:monitor/health` 及 `indices:admin/mappings/get`。
{: .note}

![叢集指標監視器]({{site.url}}{{site.baseurl}}/images/alerting/cross-cluster-per-query-per-bucket-monitors.png){: width="700" }

## 建立每個查詢或每個桶監視器

若要建立每個查詢監視器，請依照下列步驟：

**步驟 1.** 定義您的查詢與[觸發條件]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/triggers/)。您可以使用下列任一方法：視覺化編輯器、查詢編輯器或異常偵測器。

   - 視覺化定義適用於可定義為「某個值在某段時間內高於或低於某個閾值」的監視器。它也適用於大多數監視器。

   - 查詢定義可讓您靈活地定義查詢（使用 [OpenSearch query DSL]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/full-text/index/)）以及評估該查詢結果的方式（Painless 指令碼）。如需詳細資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

下列範例會計算 `cpu_usage` 欄位的平均值：

```json
     {
       "size": 0,
       "query": {
         "match_all": {}
       },
       "aggs": {
         "avg_cpu": {
           "avg": {
             "field": "cpu_usage"
           }
         }
       }
     }
```

您也可以使用 `{% raw %}{{period_start}}{% endraw %}` 與 `{% raw %}{{period_end}}{% endraw %}` 篩選查詢結果：

```json
     {
       "size": 0,
       "query": {
         "bool": {
           "filter": [{
             "range": {
               "timestamp": {
                 "from": "{% raw %}{{period_end}}{% endraw %}||-1h",
                 "to": "{% raw %}{{period_end}}{% endraw %}",
                 "include_lower": true,
                 "include_upper": true,
                 "format": "epoch_millis",
                 "boost": 1
               }
             }
           }],
           "adjust_pure_negative": true,
           "boost": 1
         }
       },
       "aggregations": {}
     }
```

「Start」與「end」指的是監視器執行的間隔。請參閱[監視器變數]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/monitors/#monitor-variables)。

若要以視覺化方式定義監視器，請選擇 **Visual editor**。然後選擇來源索引、時間範圍、彙總（例如 `count()` 或 `average()`）、資料篩選條件（如果您想要監視來源索引的子集），以及群組依據欄位（如果您想要在查詢中包含彙總欄位）。如果您要定義每個桶監視器，則至少需要一個群組依據欄位。

視覺化定義適用於大多數監視器。
{: .tip }

如果您使用 Security 外掛程式，則只能選擇您有權存取的索引。如需詳細資訊，請參閱[警示安全性]({{site.url}}{{site.baseurl}}/security/)。

若要使用查詢，請選擇 **Extraction query editor**，新增您的查詢（使用 [OpenSearch query DSL]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/full-text/index/)），並使用 **Run** 按鈕進行測試。

監視器會依排程指定的頻率向 OpenSearch 發出此查詢；請檢查 **Query Performance** 區段，並確認您能接受其效能影響。

只有在您定義每個查詢監視器時，才能使用異常偵測。
{: .warning}

若要使用異常偵測器，請選擇 **Anomaly detector** 並選取您的 **Detector**。

異常偵測選項是用來與 Anomaly Detection 外掛程式搭配使用。請參閱 [Anomaly Detection]({{site.url}}{{site.baseurl}}/monitoring-plugins/ad/)。

針對異常偵測器，請根據偵測器間隔為監視器選擇適當的排程。否則，警示監視器可能會漏讀結果。例如，假設您將監視器間隔與偵測器間隔設為 5 分鐘，並在 12:00 啟動偵測器。如果在 12:05 偵測到異常，由於寫入異常與可供查詢之間有延遲，該異常可能在 12:06 才可供使用。監視器會讀取 12:00 到 12:05 之間的異常結果，因此不會取得 12:06 才可供使用的異常結果。

若要避免此問題，請確認警示監視器的間隔至少是偵測器間隔的兩倍。當您使用 OpenSearch Dashboards 建立監視器時，異常偵測外掛程式會產生預設的監視器排程，其為偵測器間隔的兩倍。

每當您更新偵測器的間隔時，請務必更新相關聯的監視器間隔，因為 Anomaly Detection 外掛程式不會自動執行此操作。

**步驟 2.** 選擇執行監視器的頻率，例如依時間間隔（分鐘、小時、天）或依排程。如果您依時間間隔或依[自訂 cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/#cron-expressions)執行，則必須提供時區。

**步驟 3.** 新增觸發條件至監視器。
