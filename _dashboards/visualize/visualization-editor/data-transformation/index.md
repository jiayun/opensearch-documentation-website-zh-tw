---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "資料轉換"
parent: Creating visualizations using queries
grand_parent: Building data visualizations
nav_order: 95
redirect_from:
  - /dashboards/visualize/visualization-editor/data-transformation/
---

# 資料轉換

資料轉換會在視覺化呈現之前修改查詢結果。您可以使用轉換來重新調整、篩選、排序、計算或摘要資料，而不需變更原始查詢。

轉換會以管線的方式套用。每個轉換都會接收前一個轉換的輸出作為輸入，因此轉換的順序可能會改變最終結果。

在下列情況下，請使用轉換：

- 在查詢傳回結果後篩選資料列。
- 在結果表格中保留或移除特定欄位。
- 在進行視覺化之前排序資料列。
- 限制視覺化中顯示的資料列數量。
- 將欄位值轉換為其他類型，例如數字、字串、布林值或日期。
- 從物件或 JSON 字串中擷取欄位，成為最上層的資料欄。
- 根據現有的數值欄位新增計算欄位。
- 依某個欄位將資料列分組，並彙總其餘欄位。

當查詢傳回的資料正確，但其形式不完全符合視覺化的需求時，轉換就很實用。如果能在查詢中更有效率地篩選或彙總資料，請先更新查詢。

## 支援的轉換

下表列出可用的轉換。

| 轉換 | 說明 |
| --- | --- |
| **Limit** | 僅保留指定數量的資料列。 |
| **Sort by** | 依單一欄位以遞增或遞減順序排序資料列。 |
| **Filter** | 保留符合欄位、運算子與值條件的資料列。 |
| **Filter fields** | 包含或排除所選的欄位。 |
| **Convert field type** | 將欄位值轉換為字串、數字、布林值或日期。 |
| **Group by** | 依單一欄位將資料列分組，並彙總其餘欄位。 |
| **Extract fields** | 將巢狀物件或 JSON 字串欄位擷取為最上層欄位。 |
| **Add field** | 根據現有的數值欄位或常數建立計算數值欄位。 |

## 新增與管理轉換

若要新增轉換，請前往 **Transform** 索引標籤，選取 **Add**，然後在 **Add transformation** 浮出視窗中選擇轉換。系統會將轉換卡片新增至管線。

下圖顯示列出可用轉換的 **Add transformation** 浮出視窗。

![Transform 索引標籤旁列出可用轉換的 Add transformation 浮出視窗]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/data-transformation/open-transformation-table.png){: width="100%" }

您可以透過下列方式管理管線中的轉換：

- 更新轉換卡片中的控制項以進行編輯。
- 選取眼睛圖示以隱藏或顯示轉換。隱藏的轉換仍會保留在管線中，但會被略過。
- 選取刪除圖示以移除轉換。
- 拖曳轉換卡片以變更管線順序。

## 轉換順序

轉換的順序很重要。管線會由上而下執行，每個步驟都會使用前一個步驟產生的結果。某個轉換所建立或移除的欄位，會影響後續轉換可用的欄位。

例如，下列管線會篩選成功的請求，依位元組數排序，並僅保留最大的結果：

1. **Filter**：`response` 等於 `200`。
1. **Sort by**：`bytes`，遞減。
1. **Limit**：`1`。

下表顯示輸入資料。

| `extension` | `response` | `bytes` |
| --- | --- | --- |
| `css` | `200` | `14074` |
| `png` | `404` | `7911` |
| `js` | `200` | `1024` |
| `css` | `503` | `2048` |

下表顯示結果。

| `extension` | `response` | `bytes` |
| --- | --- | --- |
| `css` | `200` | `14074` |

## 範例資料

下列範例使用以 `opensearch_dashboards_sample_data_logs` 範例索引為基礎的小型結果表格。

| `@timestamp` | `extension` | `response` | `bytes` | `machine.os` | `geo` |
| --- | --- | --- | --- | --- | --- |
| `2026-09-20T10:00:00Z` | `css` | `200` | `14074` | `win 8` | `{"src":"US","dest":"CN"}` |
| `2026-09-20T10:01:00Z` | `png` | `404` | `7911` | `osx` | `{"src":"IN","dest":"US"}` |
| `2026-09-20T10:02:00Z` | `js` | `200` | `1024` | `win xp` | `{"src":"US","dest":"GB"}` |
| `2026-09-20T10:03:00Z` | `css` | `503` | `2048` | `ios` | `{"src":"CN","dest":"US"}` |

## 轉換類型

下列各節將說明每種轉換，並顯示將其套用至範例資料的結果。

### Limit

使用 **Limit** 從結果開頭僅保留指定數量的資料列。

此轉換使用下列組態：

- **Number of rows**：`2`

下表顯示輸入資料。

| `extension` | `response` | `bytes` |
| --- | --- | --- |
| `css` | `200` | `14074` |
| `png` | `404` | `7911` |
| `js` | `200` | `1024` |
| `css` | `503` | `2048` |

下表顯示結果。

| `extension` | `response` | `bytes` |
| --- | --- | --- |
| `css` | `200` | `14074` |
| `png` | `404` | `7911` |

### Sort by

使用 **Sort by** 依所選欄位排序資料列。

此轉換使用下列組態：

- **Field**：`bytes`
- **Order**：**Descending**

下表顯示輸入資料。

| `extension` | `response` | `bytes` |
| --- | --- | --- |
| `css` | `200` | `14074` |
| `png` | `404` | `7911` |
| `js` | `200` | `1024` |
| `css` | `503` | `2048` |

下表顯示結果。

| `extension` | `response` | `bytes` |
| --- | --- | --- |
| `css` | `200` | `14074` |
| `png` | `404` | `7911` |
| `css` | `503` | `2048` |
| `js` | `200` | `1024` |

### Filter

使用 **Filter** 保留符合條件的資料列。可用的運算子取決於所選欄位的類型。

此轉換使用下列組態：

- **Field**：`response`
- **Operator**：**Equals**
- **Value**：`200`

下表顯示輸入資料。

| `extension` | `response` | `bytes` |
| --- | --- | --- |
| `css` | `200` | `14074` |
| `png` | `404` | `7911` |
| `js` | `200` | `1024` |
| `css` | `503` | `2048` |

下表顯示結果。

| `extension` | `response` | `bytes` |
| --- | --- | --- |
| `css` | `200` | `14074` |
| `js` | `200` | `1024` |

### Filter fields

使用 **Filter fields** 包含或排除所選的欄位。

此轉換使用下列組態：

- **Mode**：**Include**
- **Fields**：`extension`、`response`、`bytes`

下表顯示輸入資料。

| `@timestamp` | `extension` | `response` | `bytes` | `machine.os` |
| --- | --- | --- | --- | --- |
| `2026-09-20T10:00:00Z` | `css` | `200` | `14074` | `win 8` |
| `2026-09-20T10:01:00Z` | `png` | `404` | `7911` | `osx` |

下表顯示結果。

| `extension` | `response` | `bytes` |
| --- | --- | --- |
| `css` | `200` | `14074` |
| `png` | `404` | `7911` |

### Convert field type

使用 **Convert field type** 將所選的欄位值轉型為其他類型。支援的目標類型為字串、數字、布林值和日期。

此轉換使用下列組態：

- **Field**：`response`
- **Target type**：**Number**

下表顯示輸入資料。

| `extension` | `response` | `bytes` |
| --- | --- | --- |
| `css` | `"200"` | `14074` |
| `png` | `"404"` | `7911` |

下表顯示結果。

| `extension` | `response` | `bytes` |
| --- | --- | --- |
| `css` | `200` | `14074` |
| `png` | `404` | `7911` |

### Group by

使用 **Group by** 依欄位值將資料列分組，並針對每個群組彙總其他欄位。

此轉換使用下列組態：

- **Field**：`extension`
- **Aggregations**：`bytes` 使用 **Total**，`response` 使用 **Count**

下表顯示輸入資料。

| `extension` | `response` | `bytes` |
| --- | --- | --- |
| `css` | `200` | `14074` |
| `png` | `404` | `7911` |
| `js` | `200` | `1024` |
| `css` | `503` | `2048` |

下表顯示結果。

| `extension` | `total_bytes` | `count_response` |
| --- | --- | --- |
| `css` | `16122` | `2` |
| `png` | `7911` | `1` |
| `js` | `1024` | `1` |

### Extract fields

使用 **Extract fields** 將巢狀物件或 JSON 字串欄位展開為最上層欄位。

此轉換使用下列組態：

- **Field**：`geo`
- **Format**：**Object**
- **Column prefix**：`geo_`

下表顯示輸入資料。

| `extension` | `geo` |
| --- | --- |
| `css` | `{"src":"US","dest":"CN"}` |
| `png` | `{"src":"IN","dest":"US"}` |

下表顯示結果。

| `extension` | `geo` | `geo_src` | `geo_dest` |
| --- | --- | --- | --- |
| `css` | `{"src":"US","dest":"CN"}` | `US` | `CN` |
| `png` | `{"src":"IN","dest":"US"}` | `IN` | `US` |

### Add field

使用 **Add field** 建立計算數值欄位。**Add field** 支援二元計算、一元計算和跨欄位計算。

此轉換使用下列組態：

- **Mode**：**Binary**
- **Field 1**：`bytes`
- **Operator**：`+`
- **Field 2**：自訂值 `100`
- **Alias**：`bytes_with_overhead`

下表顯示輸入資料。

| `extension` | `bytes` |
| --- | --- |
| `css` | `14074` |
| `png` | `7911` |
| `js` | `1024` |

下表顯示結果。

| `extension` | `bytes` | `bytes_with_overhead` |
| --- | --- | --- |
| `css` | `14074` | `14174` |
| `png` | `7911` | `8011` |
| `js` | `1024` | `1124` |
