---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "數值計算"
parent: Configuring visualizations
grand_parent: Creating visualizations using queries
great_grand_parent: Building data visualizations
nav_order: 20
---

# 數值計算

當視覺化接收到數值欄位時，資料通常包含一系列數值，而不是單一數字。請使用 **Calculation** 設定選取一個歸約函式，將該系列彙總為一個具代表性的數值以供顯示。

## 支援的圖表類型

數值計算設定適用於下列圖表類型。只有這些圖表類型會為每個系列顯示單一彙總值。

- 長條量表 (Bar gauge)
- 量表 (Gauge)
- 指標 (Metric)

## 遺漏值

資料系列可能包含 `NaN` 或 `null` 項目。標有星號 (\*) 的計算方法會略過這些無效項目，僅對有效的數值進行運算。未標星號的方法則使用原始位置上的值，不論其是否為有效數字。

## 可用的計算

下表列出所有可用的計算方法。

| 計算 | 說明 | 需要有效值 |
| --- | --- | --- |
| **First** | 欄位中的第一個值。 | 否 |
| **First \*** | 欄位中第一個有效 (非 `null`、非 `NaN`) 的值。 | 是 |
| **Last** | 欄位中的最後一個值。 | 否 |
| **Last \*** | 欄位中最後一個有效 (非 `null`、非 `NaN`) 的值。 | 是 |
| **Min** | 所有有效值中的最小值。 | 是 |
| **Max** | 所有有效值中的最大值。 | 是 |
| **Mean** | 所有有效值的算術平均數。 | 是 |
| **Median** | 將所有有效值排序後位於中間的值。 | 是 |
| **Total** | 所有有效值的總和。 | 是 |
| **Count** | 欄位中值的總數 (包含 `null`/`NaN`)。 | 否 |
| **Distinct count** | 欄位中不重複值的數量 (包含 `null`/`NaN`)。 | 否 |
| **Variance** | 所有有效值的統計變異數。 | 是 |

