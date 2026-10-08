---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Maps Stats API
nav_order: 20
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
parent: Maps application
has_children: false
redirect_from:
  - /dashboards/visualize/maps-stats-api/
---

# Maps Stats API
於 2.7 版推出
{: .label .label-purple }

當您在 OpenSearch Dashboards 中建立並儲存[地圖]({{site.url}}{{site.baseurl}}/dashboards/visualize/maps/)時，該地圖會成為類型為 `map` 的已儲存物件。Maps Stats API 提供 OpenSearch Dashboards 中此類已儲存物件的資訊。

#### 範例請求

您可以透過以下格式提供 URL 位址來存取 Maps Stats API：

```
{opensearch-dashboards-endpoint-address}/api/maps-dashboards/stats
```

OpenSearch Dashboards 端點位址可能包含連接埠號碼（若該號碼已在 OpenSearch 組態檔中指定）。具體的 URL 格式取決於 OpenSearch 部署的類型及其所在的網路環境。
{: .note}  

您可以透過兩種方式查詢該端點：
  
  - 在瀏覽器中存取端點位址（例如 `http://localhost:5601/api/maps-dashboards/stats`）

  - 在終端機中使用 `curl` 命令：
    ```bash
    curl -X GET http://localhost:5601/api/maps-dashboards/stats
    ```
    {% include copy.html %}

#### 範例回應

以下是前述請求的回應：

```json
{
   "maps_total":4,  
   "layers_filters_total":4, 
   "layers_total":{ 
      "opensearch_vector_tile_map":2, 
      "documents":7, 
      "wms":1, 
      "tms":2 
   },
   "maps_list":[
      {
         "id":"88a24e6c-0216-4f76-8bc7-c8db6c8705da", 
         "layers_filters_total":4,
         "layers_total":{
            "opensearch_vector_tile_map":1,
            "documents":3,
            "wms":0,
            "tms":0
         }
      },
      {
         "id":"4ce3fe50-d309-11ed-a958-770756e00bcd",
         "layers_filters_total":0,
         "layers_total":{
            "opensearch_vector_tile_map":0,
            "documents":2,
            "wms":0,
            "tms":1
         }
      },
      {
         "id":"af5d3b90-d30a-11ed-a605-f7ad7bc98642",
         "layers_filters_total":0,
         "layers_total":{
            "opensearch_vector_tile_map":1,
            "documents":1,
            "wms":0,
            "tms":1
         }
      },
      {
         "id":"5ca1ec10-d30b-11ed-a042-93d8ff0f09ee",
         "layers_filters_total":0,
         "layers_total":{
            "opensearch_vector_tile_map":0,
            "documents":1,
            "wms":1,
            "tms":0
         }
      }
   ]
}
```

## 回應本文欄位

回應包含下列圖層類型的統計資料：

- 底圖：預設的 OpenSearch 地圖或自訂底層地圖。

- WMS 圖層：自訂的 WMS 底層地圖。

- TMS 圖層：自訂的 TMS 底層地圖。

- 文件圖層：地圖的資料圖層。

如需圖層類型的更多資訊，請參閱[新增圖層]({{site.url}}{{site.baseurl}}/dashboards/visualize/maps/#adding-layers)。

下表列出所有回應欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- | 
| `maps_total` | 整數 | 已註冊為 Maps 外掛程式已儲存物件的地圖總數。 |
| `layers_filters_total` | 整數 | 所有地圖中所有圖層的篩選器總數。這包括[圖層層級篩選器]({{site.url}}{{site.baseurl}}/dashboards/visualize/maps/#filtering-data-at-the-layer-level)，但不包括全域篩選器，例如[形狀篩選器]({{site.url}}{{site.baseurl}}/dashboards/visualize/maps/#drawing-shapes-to-filter-data)。 |
| `layers_total` | 物件 | 所有地圖中所有圖層的彙總統計資料。 |
| `layers_total.opensearch_vector_tile_map` | 整數 | 所有地圖中 OpenSearch 底圖的總數。 |
| `layers_total.documents` | 整數 | 所有地圖中文件圖層的總數。 |
| `layers_total.wms` | 整數 | 所有地圖中 WMS 圖層的總數。 |
| `layers_total.tms` | 整數 | 所有地圖中 TMS 圖層的總數。 |
| `maps_list` | 陣列 | 儲存在 OpenSearch Dashboards 中所有地圖的清單。 |

`map_list` 中的每個地圖都包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- | 
| `id` | 字串 | 地圖的已儲存物件 ID。 |
| `layers_filters_total` | 整數 | 該地圖中所有圖層的篩選器總數。這包括[圖層層級篩選器]({{site.url}}{{site.baseurl}}/dashboards/visualize/maps/#filtering-data-at-the-layer-level)，但不包括全域篩選器，例如[形狀篩選器]({{site.url}}{{site.baseurl}}/dashboards/visualize/maps/#drawing-shapes-to-filter-data)。 |
| `layers_total` | 物件 | 該地圖中所有圖層的彙總統計資料。 |
| `layers_total.opensearch_vector_tile_map` | 整數 | 該地圖中 OpenSearch 底圖的總數。 |
| `layers_total.documents` | 整數 | 該地圖中文件圖層的總數。 |
| `layers_total.wms` | 整數 | 該地圖中 WMS 圖層的總數。 |
| `layers_total.tms` | 整數 | 該地圖中 TMS 圖層的總數。 |

已儲存物件 ID 可協助您前往特定地圖，因為該 ID 是地圖 URL 的最後一部分。例如，在 OpenSearch Playground 中，`[Flights] Flights Status on Maps Destination Location` 地圖的位址是 `https://playground.opensearch.org/app/maps-dashboards/88a24e6c-0216-4f76-8bc7-c8db6c8705da`，其中 `88a24e6c-0216-4f76-8bc7-c8db6c8705da` 就是此地圖的已儲存物件 ID。
{: .tip}
