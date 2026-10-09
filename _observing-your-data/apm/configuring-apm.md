---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在 OpenSearch Dashboards 中設定 APM"
nav_order: 15
parent: Application Performance Monitoring
---

# 在 OpenSearch Dashboards 中設定 APM
**自 3.6 版起推出**
{: .label .label-purple }

使用 OpenTelemetry Collector 和 Data Prepper 匯入遙測資料後，您需要在 OpenSearch Dashboards 中設定應用程式效能監控 (APM)。您將建立資料集、設定索引模式、附加 Prometheus 資料來源，並在工作區中設定 APM 設定。

## 步驟 1：建立記錄檔與追蹤的資料集

在您的可觀測性工作區中建立資料集，以定義 APM 如何存取您的追蹤與記錄資料：

1. 瀏覽至您的可觀測性工作區。
2. 選取 **Datasets**，然後選取 **Create dataset**。
3. 建立指向您追蹤資料索引的**追蹤資料集** (例如 `otel-v1-apm-span-*`)。
4. 建立指向您應用程式記錄檔索引的**記錄檔資料集** (例如 `logs-otel-v1-*`)。

如需建立與設定資料集的詳細指示，請參閱[資料集]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/datasets/)。

## 步驟 2：建立追蹤與記錄檔資料集之間的關聯

連結追蹤與記錄檔資料集，讓 APM 在您調查追蹤時能顯示相關記錄檔：

1. 瀏覽至 **Datasets** > **Correlations**。
2. 選取您在[步驟 1](#step-1-create-datasets-for-logs-and-traces)建立的追蹤資料集。
3. 將記錄檔資料集新增為相關聯的資料集。
4. 儲存關聯。

這可讓整個 APM 介面 (包括 **Services** 和 **Application Map** 頁面) 都能使用情境內的記錄檔關聯。如需詳細指示，請參閱[關聯]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/correlations/)。

## 步驟 3：為服務地圖建立索引模式

APM 需要一個索引模式，用於 Data Prepper 中 `otel_apm_service_map` 處理器所產生的服務地圖資料。若要建立索引模式，請依照下列步驟：

1. 瀏覽至 **Dashboards Management** > **Index patterns**。
2. 選取 **Create index pattern**。
3. 輸入 `otel-v2-apm-service-map*` 作為索引模式名稱。
4. 選取適當的時間欄位並儲存。

APM 會使用此索引模式來顯示服務拓撲資料與相依性資訊。

## 步驟 4：將 Prometheus 資料來源附加至您的工作區

APM 使用 Prometheus 來儲存與查詢速率、錯誤、持續時間 (RED) 指標。若要將 Prometheus 資料來源新增至您的工作區，請依照下列步驟：

1. 瀏覽至 **Dashboards Management** > **Data sources**。
2. 選取 **Create data source**，然後選擇 **Prometheus**。
3. 輸入您 Prometheus 執行個體的連線詳細資料 (例如 `http://prometheus:9090`)。
4. 儲存資料來源並將其附加至您的可觀測性工作區。

如需設定 Prometheus 資料來源的詳細指示，請參閱[設定 Prometheus 資料來源]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/discover-metrics/#configuring-a-prometheus-data-source)。

## 步驟 5：設定 APM 設定



若要設定 APM 設定，請依照下列步驟：

1. 瀏覽至 **APM** > **Services** 或 **APM** > **Application Map**。
2. 選取右上角的 **APM Settings** 按鈕。畫面會出現 **Application monitoring settings** 對話方塊，如下圖所示。
   ![APM 設定對話方塊]({{site.url}}{{site.baseurl}}/images/apm/apm-settings-modal.png)
3. 在 **Application monitoring settings** 對話方塊中，設定下列設定：

   - **Traces**：選取您在[步驟 1](#step-1-create-datasets-for-logs-and-traces)建立的追蹤資料集 (例如 `Trace Dataset - Local Cluster`)。相關記錄檔的數量會顯示在選取項目下方。
   - **Services**：選取您在[步驟 3](#step-3-create-an-index-pattern-for-the-service-map)建立的服務地圖索引模式 (例如 `otel-v2-apm-service-map*`)。
   - **RED Metrics**：選取您在[步驟 4](#step-4-attach-a-prometheus-data-source-to-your-workspace)設定的 Prometheus 資料來源 (例如 `ObservabilityStack_Prometheus`)。

4. 選取 **Update** 以儲存您的組態。

完成此設定後，APM 將在 Services 和 Application Map 頁面中顯示服務拓撲、RED 指標及情境內關聯。

## 後續步驟

- [服務]({{site.url}}{{site.baseurl}}/observing-your-data/apm/services/)：檢視服務效能指標與相依性。
- [應用程式地圖]({{site.url}}{{site.baseurl}}/observing-your-data/apm/application-map/)：探索服務拓撲視覺化。
