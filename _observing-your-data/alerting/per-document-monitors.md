---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "逐文件監視器"
nav_order: 20
parent: Monitors
grand_parent: Alerting
has_children: false
---

# 逐文件監視器
於 2.0 版推出
{: .label .label-purple }

逐文件監視器是一種警示監視器，可用來識別 OpenSearch 索引中的特定文件並對其發出警示。例如，您可以使用此監視器來：

- 偵測損毀的資料或未經授權的變更。
- 強制執行資料品質政策，例如確保所有文件都包含特定欄位，或欄位中的值位於特定範圍內。
- 追蹤特定文件隨時間的變化，這對稽核與合規用途很有幫助。

逐文件監視器不支援跨叢集搜尋。
{: .note} 

## 定義查詢

逐文件監視器允許您定義最多 10 個查詢，將所選欄位與期望的值進行比較。您可以使用下列運算子來定義支援的欄位資料類型：

- `is` 
- `is not`
- `is greater than`
- `is greater than equal`
- `is less than`
- `is less than equal`

您可以為每個[觸發條件]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/triggers/)使用最多 10 個標籤，將標籤新增為單一觸發條件，而不是指定單一查詢。[Alerting 外掛程式]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/monitors/)會將所有查詢的觸發條件視為邏輯 `OR` 運算來處理，因此只要符合任一查詢條件，就會觸發警示。接著 Alerting 外掛程式會通知 [Notifications 外掛程式]({{site.url}}{{site.baseurl}}/observing-your-data/notifications/index/)將警示通知傳送至頻道。

您只能在逐文件監視器中使用 _標籤_，也就是可套用至多個查詢、以邏輯 `OR` 運算將它們合併的標記。
{: .important}

## 文件發現結果

Alerting 外掛程式會建立一份 _發現結果_ 清單，其中包含哪些文件符合每個查詢的中繼資料。_發現結果_ 是由逐文件監視器查詢識別為符合警示條件之文件的記錄。發現結果的關鍵元件包括文件 ID、時間戳記與警示條件詳細資料。發現結果會儲存在發現結果索引 `.opensearch-alerting-finding*` 中。

Security Analytics 可以使用發現結果資料，將查詢資料與警示程序分開追蹤與分析。若要了解更多資訊，請參閱[使用發現結果]({{site.url}}{{site.baseurl}}/security-analytics/usage/findings/)。
{: .note}

Alerting API 也提供 _document-level monitor_，可透過程式方式達成與 OpenSearch Dashboards 中 _逐文件監視器_ 相同的功能。若要了解更多資訊，請參閱[文件層級監視器]({{site.url}}{{site.baseurl}}/monitoring-plugins/alerting/api/#document-level-monitors)。

為避免在高匯入量的叢集中產生大量發現結果，除非規則已妥善定義，否則不建議為每個發現結果設定警示通知。
{: .important}

每個文件發現結果項目都會提供下列中繼資料：

* **Document**：文件 ID 與索引名稱。例如：`Re5akdirhj3fl | test-logs-index`。
* **Query**：符合該文件的查詢名稱。
* **Time found**：表示在執行期間何時找到該文件的時間戳記。
