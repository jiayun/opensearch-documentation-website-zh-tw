---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用相關性圖表"
parent: Using Security Analytics
nav_order: 45
---

# 使用相關性圖表

相關性圖表是一個安全發現知識圖譜。它將相關性引擎產生的資訊以視覺化方式呈現，讓您能專注於特定相關性並更深入地檢視。圖表上的資訊包括依記錄類型分類的發現、發現的嚴重性等級、發現之間繪製的相關性，以及相關性的相關程度等詳細資料。您也可以操作圖表，以進一步了解感興趣的特定事件，包括依日期與時間篩選發現、放大檢視特定發現與其相關性之間的關係，以及依記錄類型與嚴重性等級篩選。請使用本節進一步了解圖表的使用方式。

---
## 存取圖表

首先在 OpenSearch Dashboards 主選單中選取 **Security Analytics**。接著在畫面左側的 Security Analytics 選單中選取 **Correlations**。畫面會顯示 **Correlations** 頁面，如下圖所示。

![相關性圖表]({{site.url}}{{site.baseurl}}/images/Security/sec-analytics/corr-graph.png){: width="85%" }

---
## 解讀圖表

圖表將發現顯示為節點，並以彩色邊框表示其嚴重性等級。節點內的三個字母縮寫代表記錄類型。連接各發現的線條代表它們之間的相關性。粗線表示強相關性，細線則表示較弱的關聯。

![相關性圖表]({{site.url}}{{site.baseurl}}/images/Security/sec-analytics/corr-graph-detail.png){: width="40%" }

---
## 使用圖表

您可以透過依嚴重性等級、記錄類型與時間篩選器篩選，控制圖表上顯示哪些發現。時間篩選器透過設定發現產生的日期範圍，控制出現在圖表上的發現。
* 使用 **Severity** 下拉式清單，依嚴重性等級選取要在圖表上顯示的發現。清單名稱旁的數字表示圖表上目前顯示的嚴重性等級數量。
* 使用 **Log types** 下拉式清單，選取要在圖表上顯示的記錄類型。清單名稱旁的數字表示圖表上目前顯示的記錄類型數量。
* 選取 **Reset filters** 可將下拉式清單恢復為預設設定，顯示所有項目。
* 使用時間篩選器設定日期範圍，僅顯示在該時間範圍內產生的發現。選取 **Refresh** 可將發現的目前數量更新至最新狀態。

您可以專注於圖表的特定區域，檢視與特定發現相關的相關性，方法是在圖表上選取該發現。圖表隨後會變更為僅顯示所選發現，以及與其相關的發現群組，如下圖所示。

![放大檢視圖表上的特定發現]({{site.url}}{{site.baseurl}}/images/Security/sec-analytics/corr-drill-dn.png){: width="40%" }

縮小圖表的焦點後，畫面右側會出現每個發現的資訊卡片。所選發現會顯示在卡片最上方，相關的發現則依其相關性程度列於下方，並以相關性分數表示，如下圖所示。

![放大檢視圖表上的特定發現]({{site.url}}{{site.baseurl}}/images/Security/sec-analytics/corr-cards.png){: width="30%" }

您可以在圖表上選取其中一個相關的發現，以變更相關性關係的視角。這會將新選取的發現移至資訊卡片的最上方，並將其他發現顯示為相對相關性。

卡片會顯示每個發現的下列詳細資料：
* 發現的嚴重性等級：1 為 critical（重大）、2 為 high（高）、3 為 medium（中）、4 為 low（低）、5 為 informational（資訊）。
* 相關發現的相關性分數。此分數是根據相關性規則所定義的威脅情境中，相關發現之間的接近程度計算。
* 產生該發現的偵測規則。
* 對於相關發現，則顯示用來將其與所選發現建立關聯的相關性規則。

