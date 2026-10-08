---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "TSVB 視覺化"
parent: Visualization types
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 170
redirect_from:
  - /dashboards/visualize/tsvb/
---

# TSVB 視覺化

時間序列視覺化建構器 (TSVB) 是 OpenSearch Dashboards 中的資料視覺化工具，可用於建立詳細的時間序列視覺化。TSVB 支援根據索引資料在特定時間點新增註解或標記、在多個索引之間建立連結，以及建立隨時間顯示資料的視覺化。TSVB 支援下列視覺化類型：區域圖、折線圖、指標、量表、Markdown 和資料表。

## 何時使用 TSVB 視覺化

當時間序列分析的需求超出基本圖表功能時，請使用 TSVB 視覺化，包括進階數學函式、多指標比較，以及精密的時間分析。

## 從多個資料來源建立 TSVB 視覺化
於 2.14 版推出
{: .label .label-purple }

繼續之前，請確認已在 `config/opensearch_dashboards.yaml` 檔案中啟用下列組態設定：

```yaml
data_source.enabled: true
vis_type_timeseries.enabled: true
```
{% include copy.html %}

在 OpenSearch Dashboards 中設定好[多個資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/multi-data-sources/)之後，您就可以使用 TSVB 查詢這些資料來源。下列 GIF 顯示在 OpenSearch Dashboards 中建立 TSVB 視覺化的過程。

![在 OpenSearch Dashboards 中建立 TSVB 視覺化的過程]({{site.url}}{{site.baseurl}}/images/dashboards/configure-tsvb.gif)

**步驟 1：設定並連線資料來源**

開啟 OpenSearch Dashboards 並依照下列步驟操作：

1. 從左側主選單中選取 **Dashboards Management**。
2. 選取 **Data sources**，然後選取 **Create data source** 按鈕。
3. 在 **Create data source** 頁面上，輸入連線詳細資料和端點 URL。
4. 在首頁上，選取 **Add sample data**，然後為 **Sample web logs** 資料集選取 **Add data** 按鈕。

下列 GIF 顯示設定並連線資料來源所需的步驟。

![建立資料來源]({{site.url}}{{site.baseurl}}/images/dashboards/create-datasource.gif)

**步驟 2：建立視覺化**

請依照下列步驟建立視覺化：

1. 從左側選單中選取 **Visualize**。
2. 在 **Visualizations** 頁面上，選取 **Create Visualization**，然後在彈出式視窗中選取 **TSVB**。

**步驟 3：指定資料來源**

建立 TSVB 視覺化之後，可能會根據您的預設索引模式顯示資料。若要變更索引模式或設定其他設定，請依照下列步驟操作：

1. 在 **Create** 視窗中，選取 **Panel options**。
2. 在 **Data source** 底下，選取要從中提取資料的 OpenSearch 叢集。在此情況下，請選擇您剛建立的資料來源。
3. 在 **Index name** 底下，輸入 `opensearch_dashboards_sample_data_logs`。
4. 在 **Time field** 底下，選取 `@timestamp`。此設定會指定呈現視覺化的時間範圍。

**（選用）步驟 4：新增註解**

註解是可新增至時間序列視覺化的標記。請依照下列步驟新增註解：

1. 在頁面左上角，選取 **Time Series**。
2. 選取 **Annotations** 索引標籤，然後選取 **Add data source**。
3. 在 **Index** 名稱欄位中，指定適當的索引。在此情況下，請繼續使用先前步驟中的相同索引，即 `opensearch_dashboards_sample_data_logs`。
4. 在 **Time** 欄位中，選取 `@timestamp`。
5. 在 **Fields** 欄位中，輸入 `timestamp`。
6. 在 **Row template** 欄位中，輸入 `timestamp`。

視覺化會自動更新以顯示您的註解，如下圖所示。

  ![含註解的 TSVB 視覺化]({{site.url}}{{site.baseurl}}/images/dashboards/tsvb-with-annotations.png){: width="700" }

## 後續步驟

- 若要選擇不同的視覺化類型，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。
- 若要將此視覺化新增至儀表板，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
