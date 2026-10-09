---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在 Discover 中分析指標"
nav_order: 50
parent: Using Discover for observability
---

# 在 Discover 中分析指標
**於 3.5 版推出**
{: .label .label-purple }

OpenSearch Dashboards 中的 **Metrics** 頁面提供專屬介面，用來探索、查詢及視覺化時間序列指標資料。下圖所示的這個頁面已針對使用 PromQL 處理 Prometheus 指標進行最佳化。

![Metrics 頁面介面]({{site.url}}{{site.baseurl}}/images/dashboards/prometheus.png){: width="700" }

**Metrics** 頁面可在可觀測性工作區中使用。若要存取 **Metrics** 頁面，請瀏覽至 **Observability** 工作區。接著在左側導覽中展開 **Discover**，然後選取 **Metrics**。

## 先決條件

使用 **Metrics** 頁面之前，請確認您已符合下列先決條件：

1. **啟用功能旗標**：將下列設定新增至您的 `opensearch_dashboards.yml` 檔案：

   ```yaml
   workspace.enabled: true
   data_source.enabled: true
   explore.enabled: true
   explore.discoverMetrics.enabled: true
   ```
   {% include copy.html %}

   更新組態檔案後，請重新啟動 OpenSearch Dashboards 讓變更生效。

1. **建立可觀測性工作區**：您必須在可觀測性工作區內作業。**Metrics** 頁面僅在此工作區類型中提供。

1. **設定 Prometheus 資料來源**：您必須設定 Prometheus 資料來源。如需操作說明，請參閱[設定 Prometheus 資料來源](#configuring-a-prometheus-data-source)。

## 設定 Prometheus 資料來源

開始之前，請使用下列其中一種方法設定 Prometheus 資料來源。

### 在 OpenSearch Dashboards 中設定 Prometheus 資料來源

若要在 OpenSearch Dashboards 中設定 Prometheus 資料來源，請依照下列步驟操作：

1. 在左側導覽中，前往 **Data Administration** > **Data sources**。
1. 選取 **Create data source**。
1. 選取 **Prometheus**。
1. 輸入 **Data source name** 及選用的 **Description**。
1. 輸入 **Prometheus URI** 端點 (例如 `http://prometheus-server:9090`)。
1. 設定 **Authentication method**：
   - **No authentication**：若您的 Prometheus 伺服器不需要驗證，請使用此選項。
   - **Basic authentication**：輸入使用者名稱與密碼。
   - **AWS Signature Version 4**：用於 Amazon Managed Service for Prometheus。
1. 選取 **Connect**。

### 使用 API 設定 Prometheus 資料來源

或者，您也可以透過程式設計方式設定 Prometheus 資料來源。如需詳細資訊，請參閱[資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/data-sources/)。

## 查詢面板

您可以在 **Metrics** 頁面頂端的查詢面板中撰寫及執行指標查詢。查詢編輯器提供 PromQL 的自動完成建議與語法醒目提示。

### 撰寫查詢

使用 PromQL 語法撰寫查詢。例如：

```json
up{job="prometheus"}
```
{% include copy.html %}

### 執行查詢

若要執行查詢，請在查詢編輯器中輸入您的查詢，然後選取 **Refresh** 按鈕。

您可以使用分號 (`;`) 分隔多個 PromQL 查詢，將它們一起執行：

```json
up{job="prometheus"};
node_cpu_seconds_total{mode="idle"};
```
{% include copy.html %}

每個查詢會獨立執行，結果會合併在輸出中。

## 時間篩選器

使用時間篩選器指定指標資料的時間範圍。選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/calendar-icon.png" class="inline-icon" alt="calendar icon"/>{:/} (日曆) 圖示以存取時間篩選器選項：

- **Quick select**：選擇相對時間範圍 (例如過去 15 分鐘或過去 1 小時)。
- **Commonly used**：從預先定義的時間範圍中選取。
- **Custom**：指定絕對開始與結束時間。
- **Auto-refresh**：設定自動重新整理間隔。

如需詳細資訊，請參閱[時間篩選器]({{site.url}}{{site.baseurl}}/dashboards/discover/time-filter/)。

## 檢視結果

執行查詢後，結果會顯示在包含下列檢視的索引標籤式介面中：

- **Metrics** 索引標籤會以表格格式顯示每個序列的最新資料點。

- **Raw** 索引標籤會顯示每個序列的最新資料點，也就是資料來源傳回的原始 JSON。

- **Visualization** 索引標籤會為您的指標資料提供互動式圖表。

#### 設定視覺化

選取 **Visualization** 索引標籤時，畫面右側會出現設定面板。使用此面板來：

1. **選取圖表類型**：從折線圖、長條圖、圓餅圖、量表或表格視覺化中選擇。
2. **對應軸**：將欄位指派給 X 軸與 Y 軸。
3. **自訂樣式**：調整色彩、圖例、格線及其他視覺選項。

當您修改設定時，視覺化會自動更新。
