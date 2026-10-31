---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指標"
nav_order: 30
parent: Observability workspace apps
---

# 在 Discover 中分析指標
**於 3.5 版導入**
{: .label .label-purple }

OpenSearch Dashboards 的 **Metrics** 頁面提供專屬介面，可用於探索、查詢及視覺化時間序列指標資料。此頁面（如下圖所示）已針對使用 PromQL 處理 Prometheus 指標進行最佳化。

![Metrics 頁面介面]({{site.url}}{{site.baseurl}}/images/dashboards/prometheus.png){: width="700" }

**Metrics** 頁面可在可觀測性工作區中使用。若要存取 **Metrics** 頁面，請前往 **Observability** 工作區，然後在左側導覽列選取 **Metrics**。

## 必要條件

使用 **Metrics** 頁面之前，請確認您已符合下列必要條件：

1. **啟用功能旗標**：將下列設定加入您的 `opensearch_dashboards.yml` 檔案：

   ```yaml
   workspace.enabled: true
   explore.enabled: true
   explore.discoverMetrics.enabled: true
   ```
   {% include copy.html %}

   更新組態檔後，請重新啟動 OpenSearch Dashboards，讓變更生效。

1. **建立可觀測性工作區**：您必須在可觀測性工作區中作業。**Metrics** 頁面僅在此類工作區中提供。

1. **設定 Prometheus 資料來源**：您必須設定 Prometheus 資料來源。相關指示請參閱[設定 Prometheus 資料來源](#configuring-a-prometheus-data-source)。

## 設定 Prometheus 資料來源

開始之前，請使用下列其中一種方法設定 Prometheus 資料來源。

### 在 OpenSearch Dashboards 中設定 Prometheus 資料來源

若要在 OpenSearch Dashboards 中設定 Prometheus 資料來源，請依照下列步驟操作：

1. 在左側導覽列中，前往 **Data Administration** > **Data sources**。
1. 選取 **Create data source**。
1. 選取 **Prometheus**。
1. 輸入 **Data source name** 與選用的 **Description**。
1. 輸入 **Prometheus URI** 端點（例如 `http://prometheus-server:9090`）。
1. 設定 **Authentication method**：
   - **No authentication**：當您的 Prometheus 伺服器不需要驗證時使用。
   - **Basic authentication**：輸入用戶名稱（username）與密碼。
   - **AWS Signature Version 4**：用於 Amazon Managed Service for Prometheus。
1. 選取 **Connect**。

### 使用 API 設定 Prometheus 資料來源

您也可以改用程式方式設定 Prometheus 資料來源。詳細資訊請參閱[Data sources]({{site.url}}{{site.baseurl}}/dashboards/management/data-sources/)。

## 查詢面板

您可以在 **Metrics** 頁面頂端的查詢面板中撰寫並執行指標查詢。查詢編輯器提供 PromQL 的自動完成建議與語法醒目提示。

### 撰寫查詢

請使用 PromQL 語法撰寫查詢。例如：

```json
up{job="prometheus"}
```
{% include copy.html %}

### 執行查詢

若要執行查詢，請在查詢編輯器中輸入查詢，然後選取 **Refresh** 按鈕。

您可以將多個 PromQL 查詢以分號（`;`）分隔後一起執行：

```json
up{job="prometheus"};
node_cpu_seconds_total{mode="idle"};
```
{% include copy.html %}

每個查詢會獨立執行，結果會在輸出中合併。

## 時間篩選器

使用時間篩選器來指定指標資料的時間範圍。選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/calendar-icon.png" class="inline-icon" alt="calendar icon"/>{:/}（行事曆）圖示以存取時間篩選器選項：

- **Quick select**：選擇相對時間範圍（例如最近 15 分鐘或最近 1 小時）。
- **Commonly used**：從預先定義的時間範圍中選取。
- **Custom**：指定絕對的開始與結束時間。
- **Auto-refresh**：設定自動重新整理間隔。

詳細資訊請參閱[Time filter]({{site.url}}{{site.baseurl}}/dashboards/discover/time-filter/)。

## 檢視結果

執行查詢後，結果會顯示在具有下列檢視的分頁介面中：

- **Metrics** 分頁以表格格式顯示每個序列的最新資料點。

- **Raw** 分頁顯示每個序列的最新資料點，為資料來源傳回的原始 JSON。

- **Visualization** 分頁提供指標資料的互動式圖表。

#### 設定視覺化

選取 **Visualization** 分頁時，畫面右側會出現設定面板。您可以使用此面板：

1. **選取圖表類型**：從折線圖、長條圖、圓餅圖、量測計或表格視覺化中選擇。
2. **對應軸**：將欄位指派到 X 軸與 Y 軸。
3. **自訂樣式**：調整顏色、圖例、格線及其他視覺選項。

當您修改設定時，視覺化會自動更新。
