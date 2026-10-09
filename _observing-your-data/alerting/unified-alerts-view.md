---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "統一的警示檢視"
parent: Alerting dashboards and visualizations
grand_parent: Alerting
nav_order: 10
---

# 統一的警示檢視
**於 3.7 版推出**
{: .label .label-purple }

統一的警示檢視會將 OpenSearch 監視器與 Prometheus 警示規則的警示彙整到單一檢視中，讓您不必在不同工具之間切換，就能跨資料來源分流處理警示。在 OpenSearch Dashboards 中，此檢視會顯示為 **Observability** 底下的 **Alerts** 頁面。

**Alerts** 頁面也可以顯示異常偵測與預測資源，讓您在同一頁面調查警示、異常、偵測器與預測器。

## 啟用統一的警示檢視

統一的警示檢視預設為停用。若要啟用，請將下列這一行加入 `opensearch_dashboards.yml`：

```yaml
observability.alertManager.enabled: true
```
{% include copy.html %}

接著重新啟動 OpenSearch Dashboards。重新啟動後，OpenSearch Dashboards 主選單的 **Observability** 底下會出現 **Alerts** 選項。

## 調查警示

**Alerts** 索引標籤會顯示所選時間範圍的警示時間軸、多面向篩選面板，以及個別警示與異常的表格。您可以依資料來源、類型、嚴重性、狀態與標籤篩選表格。

若要調查警示，請在表格中選取該警示，以開啟警示詳細資料飛出視窗。飛出視窗會顯示警示中繼資料及其來源監視器。

此檢視支援下列警示狀態：`active`、`pending`、`acknowledged`、`silenced`、`resolved` 及 `error`。支援的嚴重性層級為 `critical`、`high`、`medium`、`low` 及 `info`。

## 調查異常

**Alerts** 索引標籤包含來自即時異常偵測器的異常結果。異常會與警示出現在同一個表格中，並使用 `anomaly` 狀態。

當多個異常事件屬於同一個偵測器與實體時，表格會將它們分組為單一資料列。展開該資料列以檢查個別事件，然後選取某個事件以開啟異常詳細資料飛出視窗。

異常詳細資料飛出視窗會顯示偵測器與異常中繼資料、異常等級、信賴度、開始時間、持續時間及特徵資料。對於高基數偵測器，飛出視窗會包含所選實體的偵測器結果內容。對於單一實體偵測器，飛出視窗會顯示所選異常的指標內容。

如果警示與異常結果相關聯，警示詳細資料飛出視窗也會顯示異常內容，讓您不必離開 **Alerts** 頁面，就能檢閱造成該警示的異常。

## 確認警示

在 **Alerts** 索引標籤中，您可以確認一或多個作用中的 OpenSearch 警示。在表格中選取這些警示，然後選取 **Acknowledge**。

對於 Prometheus 資料來源，此檢視為唯讀。您無法從統一的警示檢視確認 Prometheus 警示。
{: .note}

## 規則

**Rules** 索引標籤會列出所選資料來源中的警示規則、監視器、異常偵測器與預測器。您可以依類型與狀態篩選規則。

如果所選資料來源未設定任何資源，頁面會提供建立下列項目的選項：

- 記錄檔或指標警示
- 異常偵測器
- 預測器

只有在資料來源篩選器中選取 OpenSearch 資料來源時，才會啟用異常偵測與預測選項。

### 異常偵測器

偵測器在 **Type** 欄中會以 **Anomaly Detector** 類型顯示。選取偵測器以開啟飛出視窗，其中顯示下列資訊：

- 偵測器與模型組態
- 目前狀態與健全狀態

若要從此頁面管理偵測器生命週期，請使用下列其中一個選項：

- 選取一或多個偵測器，然後在動作列中選取 **Start** 或 **Stop**。
- 在偵測器飛出視窗中選取 **Start** 或 **Stop**。

### 預測器

預測器會以 **Forecaster** 類型顯示。選取預測器以開啟飛出視窗，其中顯示下列資訊：

- 預測器描述、索引詳細資料及特徵定義
- 預測範圍與間隔組態
- 預測狀態與健全狀態

您可以從飛出視窗啟動或停止預測器。若要一次啟動或停止多個預測器，請在 **Rules** 表格中選取它們，然後選取 **Start** 或 **Stop**。

預測器會產生趨勢與容量規劃的預測輸出。它們不會在 **Alerts** 時間軸中建立警示記錄。

## 通知路由

**Routing** 索引標籤會顯示所選資料來源的警示如何對應至通知管道。

## 相關文件

- [警示]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/index/)
- [警示儀表板與視覺化]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/dashboards-alerting/)
- [監視器]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/monitors/)
- [異常偵測]({{site.url}}{{site.baseurl}}/observing-your-data/ad/index/)
- [預測]({{site.url}}{{site.baseurl}}/observing-your-data/forecast/index/)
