---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Vega 視覺化"
parent: Visualization types
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 180
redirect_from:
  - /dashboards/visualize/vega/
---

# Vega 視覺化

[Vega](https://vega.github.io/vega/) 和 [Vega-Lite](https://vega.github.io/vega-lite/) 是開放原始碼的宣告式語言視覺化工具。您可以使用 OpenSearch 資料和 [Vega 資料](https://vega.github.io/vega/docs/data/)，透過這些工具建立自訂資料視覺化。這些工具最適合能夠直接撰寫 OpenSearch 查詢的進階使用者。您可以在 Vega 規格中以內嵌方式定義資料來源。

## 何時使用 Vega 視覺化

當您需要標準 OpenSearch 視覺化類型所未提供的視覺化類型或分析功能時，請使用 Vega 視覺化，包括進階統計分析、自訂互動行為及專門的分析技術。

## 啟用 Vega 視覺化

Vega 視覺化預設為啟用。請以 JSON 或 [Hjson](https://hjson.github.io/) 格式撰寫您的 [Vega 規格](https://vega.github.io/vega/docs/specification/)。您可以在一個規格中指定一或多個 OpenSearch 查詢。

若要停用 Vega 視覺化，請在 `opensearch_dashboards.yml` 檔案中將 `vis_type_vega.enabled` 設定為 `false`。

## 建立 Vega 視覺化

本頁中的範例使用 **Sample e-commerce data** 資料集。若要了解如何新增範例資料集，請參閱[新增範例資料]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。
{: .note}

下列範例會建立一個網路圖，以視覺化方式呈現範例電子商務資料集中各產品製造商之間的關係。此範例使用 [`adjacency_matrix` 彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/adjacency-matrix/)來判斷不同製造商的產品在同一筆訂單中一起出現的頻率。

若要為此彙總建立 Vega 視覺化，請依照下列步驟操作：

1. 從左側選單中選取 **Visualize**。
2. 選取 **Create Visualization**，然後選取 **Vega**。
3. 將預設規格取代為下列內容，然後選取 **Update**：

```json
{
  "$schema": "https://vega.github.io/schema/vega/v5.json",
  "description": "Network graph from adjacency matrix aggregation",
  "autosize": "none",
  "width": 500,
  "height": 400,
  "padding": 50,

  "data": [
    {
      "name": "raw",
      "url": {
        "index": "opensearch_dashboards_sample_data_ecommerce",
        "body": {
          "size": 0,
          "aggs": {
            "interactions": {
              "adjacency_matrix": {
                "filters": {
                  "Low Tide Media": {"match": {"manufacturer.keyword": "Low Tide Media"}},
                  "Elitelligence": {"match": {"manufacturer.keyword": "Elitelligence"}},
                  "Oceanavigations": {"match": {"manufacturer.keyword": "Oceanavigations"}}
                }
              }
            }
          }
        }
      },
      "format": {"property": "aggregations.interactions.buckets"}
    },
    {
      "name": "nodes",
      "source": "raw",
      "transform": [
        {"type": "filter", "expr": "indexof(datum.key, '&') === -1"},
        {"type": "window", "ops": ["row_number"], "as": ["index"]},
        {"type": "formula", "as": "x", "expr": "250 + 150 * cos(2 * PI * (datum.index - 1) / 3)"},
        {"type": "formula", "as": "y", "expr": "200 + 150 * sin(2 * PI * (datum.index - 1) / 3)"}
      ]
    },
    {
      "name": "edges",
      "source": "raw",
      "transform": [
        {"type": "filter", "expr": "indexof(datum.key, '&') !== -1"},
        {"type": "formula", "as": "source", "expr": "split(datum.key, '&')[0]"},
        {"type": "formula", "as": "target", "expr": "split(datum.key, '&')[1]"},
        {"type": "lookup", "from": "nodes", "key": "key", "fields": ["source"], "as": ["sourceNode"]},
        {"type": "lookup", "from": "nodes", "key": "key", "fields": ["target"], "as": ["targetNode"]}
      ]
    }
  ],

  "scales": [
    {
      "name": "nodeSize",
      "type": "linear",
      "domain": {"data": "nodes", "field": "doc_count"},
      "range": [400, 2000]
    },
    {
      "name": "linkWidth",
      "type": "linear",
      "domain": {"data": "edges", "field": "doc_count"},
      "range": [2, 8]
    }
  ],

  "marks": [
    {
      "type": "rule",
      "from": {"data": "edges"},
      "encode": {
        "enter": {
          "x": {"field": "sourceNode.x"},
          "y": {"field": "sourceNode.y"},
          "x2": {"field": "targetNode.x"},
          "y2": {"field": "targetNode.y"},
          "stroke": {"value": "#888"},
          "strokeWidth": {"scale": "linkWidth", "field": "doc_count"},
          "strokeOpacity": {"value": 0.6}
        }
      }
    },
    {
      "type": "text",
      "from": {"data": "edges"},
      "encode": {
        "enter": {
          "x": {"signal": "(datum.sourceNode.x + datum.targetNode.x) / 2"},
          "y": {"signal": "(datum.sourceNode.y + datum.targetNode.y) / 2"},
          "text": {"signal": "datum.doc_count"},
          "align": {"value": "center"},
          "baseline": {"value": "middle"},
          "fontSize": {"value": 11},
          "fill": {"value": "#555"}
        }
      }
    },
    {
      "type": "symbol",
      "from": {"data": "nodes"},
      "encode": {
        "enter": {
          "x": {"field": "x"},
          "y": {"field": "y"},
          "size": {"scale": "nodeSize", "field": "doc_count"},
          "fill": {"value": "#4C78A8"},
          "stroke": {"value": "#fff"},
          "strokeWidth": {"value": 2},
          "tooltip": {"signal": "datum.key + ': ' + datum.doc_count + ' docs'"}
        }
      }
    },
    {
      "type": "text",
      "from": {"data": "nodes"},
      "encode": {
        "enter": {
          "x": {"field": "x"},
          "y": {"field": "y"},
          "dy": {"value": -30},
          "text": {"field": "key"},
          "align": {"value": "center"},
          "fontSize": {"value": 12},
          "fontWeight": {"value": "bold"}
        }
      }
    }
  ]
}
```
{% include copy.html %}

下圖顯示產生的網路圖。節點大小代表每個製造商的文件數，邊線粗細則代表同時包含兩個製造商產品的訂單數。

![OpenSearch Dashboards 中的鄰接矩陣網路圖視覺化]({{site.url}}{{site.baseurl}}/images/dashboards/adjacency-graph.png)

## 從多個資料來源建立 Vega 視覺化
於 2.13 版推出
{: .label .label-purple }

繼續操作之前，請確認已在 `config/opensearch_dashboards.yaml` 檔案中啟用下列組態設定。如需組態詳細資訊，請參閱 `vis_type_vega` [`README`](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/src/plugins/vis_type_vega/README.md)。

```
data_source.enabled: true
vis_type_vega.enabled: true
```

在 OpenSearch Dashboards 中設定[多個資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/multi-data-sources/)之後，您就可以使用 Vega 查詢這些資料來源。下列 GIF 顯示在 OpenSearch Dashboards 中建立 Vega 視覺化的過程。

![在 OpenSearch Dashboards 中建立 Vega 視覺化的過程]({{site.url}}{{site.baseurl}}/images/dashboards/configure-vega.gif)

### 步驟 1：設定並連接資料來源

開啟 OpenSearch Dashboards，並依照下列步驟操作：

1. 從左側選單中選取 **Dashboards Management**。
2. 選取 **Data sources**，然後選取 **Create data source** 按鈕。
3. 在 **Create data source** 頁面上，輸入連線詳細資訊和端點 URL，如下列 GIF 所示。
4. 在 **Home page** 上，選取 **Add sample data**。在 **Data source** 下，選取您新建立的資料來源，然後為 **Sample web logs** 資料集選取 **Add data button**。

下列 GIF 顯示設定並連接資料來源所需的步驟。

![使用 OpenSearch Dashboards 設定並連接資料來源]({{site.url}}{{site.baseurl}}/images/dashboards/Add_datasource.gif)

### 步驟 2：建立視覺化

1. 從左側選單中選取 **Visualize**。
2. 在 **Visualizations** 頁面上，選取 **Create Visualization**，然後在快顯視窗中選取 **Vega**。

### 步驟 3：新增 Vega 規格

根據預設，查詢會使用本機叢集的資料。您可以為 Vega 規格中的每個 OpenSearch 查詢個別指定 `data_source_name` 值。如此一來，您就能在單一視覺化中查詢不同資料來源的多個索引。

1. 確認您建立的資料來源已指定於 `data_source_name` 下。或者，您也可以在 Vega 規格中，於 `url` 屬性下新增 `data_source_name` 欄位，依名稱指定特定資料來源。
2. 複製下列 Vega 規格，然後選取右下角的 **Update** 按鈕。視覺化應會隨即顯示。

```json
{
  $schema: https://vega.github.io/schema/vega-lite/v5.json
  data: {
    url: {
      %context%: true
      %timefield%: @timestamp
      index: opensearch_dashboards_sample_data_logs
      data_source_name: YOUR_DATA_SOURCE_TITLE
      body: {
        aggs: {
          1: {
            date_histogram: {
              field: @timestamp
              fixed_interval: 3h
              time_zone: America/Los_Angeles
              min_doc_count: 1
            }
            aggs: {
              2: {
                avg: {
                  field: bytes
                }
              }
            }
          }
        }
        size: 0
      }
    }
    format: {
      property: aggregations.1.buckets
    }
  }
  transform: [
    {
      calculate: datum.key
      as: timestamp
    }
    {
      calculate: datum[2].value
      as: bytes
    }
  ]
  layer: [
    {
      mark: {
        type: line
      }
    }
    {
      mark: {
        type: circle
        tooltip: true
      }
    }
  ]
  encoding: {
    x: {
      field: timestamp
      type: temporal
      axis: {
        title: @timestamp
      }
    }
    y: {
      field: bytes
      type: quantitative
      axis: {
        title: Average bytes
      }
    }
    color: {
      datum: Average bytes
      type: nominal
    }
  }
}
```
{% include copy.html %}

## 其他資源

下列資源提供有關 OpenSearch Dashboards 中 Vega 視覺化的其他資訊：

- [使用 Vega 視覺化提升 OpenSearch Dashboards 的易用性](https://opensearch.org/blog/Improving-Dashboards-usability-with-Vega/)

## 後續步驟

- 若要選擇其他視覺化類型，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。
- 若要將此視覺化新增至儀表板，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
