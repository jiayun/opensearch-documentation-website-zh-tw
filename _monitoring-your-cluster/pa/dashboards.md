---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "PerfTop 儀表板"
parent: Performance Analyzer
nav_order: 2
redirect_from:
  - /monitoring-plugins/pa/dashboards/
---

# PerfTop 儀表板

您可以在 PerfTop 儀表板中檢視衍生自 Performance Analyzer 的指標。PerfTop 儀表板是一種用於顯示指標的命令列介面 (CLI)。PerfTop 儀表板由三個主要元素組成：表格、折線圖和長條圖。您可以使用 JSON 定義由列和欄組成的格線，然後將元素放入該格線中，每個元素會跨越您指定的列數和欄數。

開始建立自訂儀表板的最佳方式，是複製並修改 `dashboards` 目錄中現有的 JSON 檔案。
{: .tip }

下圖顯示一個範例儀表板。
![PerfTop 儀表板]({{site.url}}{{site.baseurl}}/images/perftop.jpg)

---

#### 目錄
1. TOC
{:toc}

---


## 元素摘要

- 表格會顯示各維度的指標。例如，如果您的指標是 `CPU_Utilization`，而您的維度是 `ShardID`，PerfTop 表格會為每個節點上的每個分片顯示一列。
- 除非您在儀表板中新增 `nodeName`，否則長條圖會針對叢集進行彙總。請參閱[所有元素的選項](#all-elements)。
- 折線圖會針對每個節點進行彙總。每條線代表一個節點。


## 定位元素

PerfTop 會將元素定位於格線中。例如，請看這個 12 * 12 的格線。

![儀表板格線]({{site.url}}{{site.baseurl}}/images/perftop-grid.png)

格線的左上角代表第 0 列、第 0 欄，因此這三個方塊的起始位置為：

- 橘色：第 0 列、第 0 欄
- 紫色：第 2 列、第 2 欄
- 綠色：第 1 列、第 6 欄

這些方塊會跨越若干列和欄。在此例中：

- 橘色：2 列、4 欄
- 紫色：1 列、4 欄
- 綠色：3 列、2 欄

以 JSON 形式表示，我們會有以下內容：

```json
{
  "gridOptions": {
    "rows": 12,
    "cols": 12
  },
  "graphs": {
    "tables": [{
        "options": {
          "gridPosition": {
            "row": 0,
            "col": 0,
            "rowSpan": 2,
            "colSpan": 4
          }
        }
      },
      {
        "options": {
          "gridPosition": {
            "row": 2,
            "col": 2,
            "rowSpan": 1,
            "colSpan": 4
          }
        }
      },
      {
        "options": {
          "gridPosition": {
            "row": 1,
            "col": 6,
            "rowSpan": 3,
            "colSpan": 2
          }
        }
      }
    ]
  }
}
```

不過，此時這段 JSON 只是定義三個表格的大小和位置。若要將資料填入元素，您需要指定查詢。


## 新增查詢

查詢使用與 [REST API]({{site.url}}{{site.baseurl}}/monitoring-plugins/pa/api/) 相同的元素，只是以 JSON 形式呈現：

```json
{
  "queryParams": {
    "metrics": "estimated,limitConfigured",
    "aggregates": "avg,avg",
    "dimensions": "type",
    "sortBy": "estimated"
  }
}
```

如需可用指標的詳細資訊，請參閱[指標參考]({{site.url}}{{site.baseurl}}/monitoring-plugins/pa/reference/)。


## 新增選項

選項包括標籤、顏色和重新整理間隔。不同的元素類型有不同的選項。

儀表板支援 16 種 ANSI 色彩：黑色、紅色、綠色、黃色、藍色、洋紅色、青色和白色。若要使用這些顏色的「亮色」變體，請使用數字 8--15。如果您的終端機支援 256 色，您也可以使用十六進位色碼 (例如 `#6D40ED`)。
{: .note }


### 所有元素

選項 | 類型 | 說明
:--- | :--- | :---
`label` | 字串或整數 | 方塊左上角的文字。
`labelColor` | 字串或整數 | 標籤的顏色。
`refreshInterval` | 整數 | 呼叫 Performance Analyzer API 取得新資料之間的毫秒數。最小值為 5000。
`dimensionFilters` | 字串陣列 | 要為圖表顯示的維度值。例如，如果您查詢 `metric=Net_Throughput&agg=sum&dim=Direction`，而可能的維度值為 `in` 和 `out`，您可以定義 `dimensionFilters: ["in"]` 以只顯示 `in` 維度的指標資料
`nodeName` | 字串 | 若非 null，可讓您將元素限制為個別節點。您可以直接在儀表板檔案中指定節點名稱，但更好的做法是在儀表板中使用 `"nodeName": "#nodeName"`，並在啟動 PerfTop 時加入 `--nodename <node_name>` 引數。


### 表格

選項 | 類型 | 說明
:--- | :--- | :---
`bg` | 字串或整數 | 背景顏色。
`fg` | 字串或整數 | 文字顏色。
`selectedFg` | 字串或整數 | 聚焦文字的顏色。
`selectedBg` | 字串或整數 | 聚焦文字的背景顏色。
`columnSpacing` | 整數 | 欄之間的間距 (以字元為單位)。
`keys` | 布林值 | 目前沒有任何影響。


### 長條

選項 | 類型 | 說明
:--- | :--- | :---
`barWidth` | 整數 | 圖表中每個長條的寬度 (以字元為單位)。
`xOffset` | 整數 | 圖表中 y 軸與第一個長條之間的間距 (以字元為單位)。
`maxHeight` | 整數 | 圖表中每個長條的最大高度 (以字元為單位)。


### 折線

選項 | 類型 | 說明
:--- | :--- | :---
`showNthLabel` | 整數 | 指定要顯示哪些 `xAxis` 標籤。例如，`"showNthLabel": 2` 會每隔一個標籤顯示一次。
`showLegend` | 布林值 | 是否顯示折線圖的圖例。
`legend.width` | 整數 | 圖表中圖例的寬度 (以字元為單位)。
`xAxis` | 字串陣列 | x 軸的標籤陣列。例如，`["0:00", "0:10", "0:20", "0:30", "0:40", "0:50"]`。
`colors` | 字串陣列 | 可選擇的線條顏色陣列。例如，`["magenta", "cyan"]`。如果您未提供此值，PerfTop 會為每條線隨機選擇顏色。
