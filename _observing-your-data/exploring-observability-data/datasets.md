---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "資料集"
nav_order: 10
parent: Using Discover for observability
redirect_from:
  - /observability-plugin/datasets/
---

# 資料集
**於 3.5 版推出**
{: .label .label-purple }

_資料集_ 代表您想要一起分析的一組索引集合。資料集提供了一種方便使用的方式，讓您在 OpenSearch Dashboards 中組織及存取您的可觀測性資料。資料集可讓您為資料來源和索引指派類型、名稱和描述，讓您更輕鬆地處理記錄檔和追蹤資料。

相較於傳統的索引模式，資料集提供了幾項優點：

- **方便使用的名稱**：指派描述性名稱，而不必依賴索引模式語法。
- **描述**：新增資料集所含資料的相關內容。
- **結構描述對應**：將非標準格式的欄位對應至與 OpenTelemetry 相容的欄位，以便進行關聯。
- **類型專屬行為**：記錄檔和追蹤資料集會與其各自的 Discover 頁面整合。

## 資料集類型

OpenSearch 支援下列資料集類型。

| 類型 | 描述 | 使用案例 |
|:-----|:------------|:---------|
| **Logs** | 用於分析和探索的一般記錄資料 | 應用程式記錄檔、系統記錄檔、存取記錄檔 |
| **Traces** | 透過 OpenSearch Data Prepper 匯入的 OpenTelemetry span 資料 | 分散式追蹤、效能監控 |

## 先決條件

使用資料集之前，請確認您已符合下列先決條件：

1. **啟用功能旗標**：將下列設定新增至您的 `opensearch_dashboards.yml` 檔案：

   ```yaml
   workspace.enabled: true
   data_source.enabled: true
   explore.enabled: true
   explore.discoverTraces.enabled: true
   datasetManagement.enabled: true
   ```
   {% include copy.html %}

   更新組態檔案後，請重新啟動 OpenSearch Dashboards，變更才會生效。

1. **將資料編製索引**：您的記錄或追蹤資料必須已編製索引至 OpenSearch。

1. **確保具備適當權限**：您需要具備在工作區中建立及管理資料集的權限。

## 建立記錄資料集

若要建立記錄資料集，請依照下列步驟進行：

1. 在工作區左側導覽中，選取 **Datasets**。

2. 選取 **Create dataset**，然後從下拉式功能表中選擇 **Logs**。

3. 在 **Step 1: Select data** 中，選取您的資料來源，如下圖所示。您可以使用萬用字元模式 (例如 `logs-*`) 來比對多個索引。

   ![選取資料來源]({{site.url}}{{site.baseurl}}/images/datasets/datasets-select-data-source.png)

4. 在 **Step 2: Configure data** 中，設定資料集設定，如下圖所示。

   ![設定記錄資料集設定]({{site.url}}{{site.baseurl}}/images/datasets/datasets-configure-logs.png)

   您可以設定下列設定：

   - **Name** -- 輸入資料集的描述性名稱。
   - **Description** (選用) -- 新增資料描述。
   - **Time field**：選擇用於時間型查詢的時間戳記欄位。
   - **Schema mappings** (選用) -- 將您的記錄欄位對應至標準 OpenTelemetry 欄位，以便與追蹤建立關聯：
     - **Trace ID field**：包含追蹤識別碼的欄位。
     - **Span ID field**：包含 span 識別碼的欄位。
     - **Service name field**：包含服務名稱的欄位。
     - **Timestamp field**：包含事件時間戳記的欄位。  

5. 選取 **Create dataset** 以儲存您的組態。

## 建立追蹤資料集

若要建立追蹤資料集，請依照下列步驟進行：

1. 在工作區左側導覽中，選取 **Datasets**。

2. 選取 **Create dataset**，然後從下拉式功能表中選擇 **Traces**。

3. 在 **Step 1: Select data** 中，選取您的追蹤資料來源。資料來源必須參照包含使用 Data Prepper 匯入之 OpenTelemetry span 資料的索引。

4. 在 **Step 2: Configure data** 中，設定資料集設定，如下圖所示。

   ![設定追蹤資料集設定]({{site.url}}{{site.baseurl}}/images/datasets/datasets-configure-traces.png)

   您可以設定下列設定：

   - **Name** -- 輸入資料集的描述性名稱。
   - **Description** (選用) -- 新增資料描述。
   - **Time field** -- 選擇時間戳記欄位 (通常是 `startTime` 或 `@timestamp`)。

5. 選取 **Create dataset** 以儲存您的組態。

## 檢視資料集

建立資料集之後，您可以透過下列步驟從 **Datasets** 頁面檢視及管理這些資料集：

1. 在工作區左側導覽中，選取 **Datasets**。

2. 清單檢視會顯示所有資料集及其名稱、類型和資料來源，如下圖所示。

   ![資料集清單檢視]({{site.url}}{{site.baseurl}}/images/datasets/datasets-list.png)

3. 選取資料集以檢視其詳細資料，包括組態設定和任何關聯。

## 在 Discover 頁面中分析資料集

資料集會與 Discover 介面整合，以便探索您的資料。

### 記錄檔資料集

若要分析記錄檔資料集，請依照下列步驟進行：

1. 瀏覽至 **Discover** > **Logs**。
2. 從資料集選取器中，選取您的記錄檔資料集。
3. 使用 Piped Processing Language (PPL) 查詢來探索及分析您的記錄資料。

### 追蹤資料集

若要分析追蹤資料集，請依照下列步驟進行：

1. 瀏覽至 **Discover** > **Traces**。
2. 從資料集選取器中選取您的追蹤資料集。
3. 探索 span 資料和追蹤流程。

## 相關文件

- [索引模式]({{site.url}}{{site.baseurl}}/dashboards/management/index-patterns/) -- 比較資料集與傳統索引模式。
- [Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) -- 將 OpenTelemetry 資料匯入 OpenSearch。
- [關聯]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/correlations/) -- 連結追蹤資料集和記錄檔資料集。
