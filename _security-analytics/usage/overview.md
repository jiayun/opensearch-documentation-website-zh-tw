---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "總覽頁面"
parent: Using Security Analytics
nav_order: 25
---

<!-- vale off -->
# 總覽頁面
<!-- vale on -->

當您從頂端選單選取 **Security Analytics** 時，就會顯示 **Overview** 頁面。**Overview** 頁面由五個區段組成：
* Findings 與警示數量
* 最近的警示
* 最近的 findings
* 最常觸發的偵測規則
* 偵測器

每個區段都提供 Security Analytics 各項元素的摘要說明，並附上可讓您對每個項目採取行動的控制項。

---
## 總覽與入門

**Overview** 頁面的上半部包含兩個控制按鈕，分別用於重新整理資訊以及開始使用 Security Analytics。您可以選取 **Refresh** 按鈕來重新整理頁面上的所有資訊。

您也可以選取 **Getting started** 連結來展開 Get started with Security Analytics 視窗，其中包含設定步驟的摘要，以及可讓您跳至任何步驟的控制按鈕。

![總覽頁面與入門快速啟動視窗]({{site.url}}{{site.baseurl}}/images/Security/overview.png){: width="85%" }

* 在設定的步驟 1 中，選取 **Create detector** 來定義偵測器。
* 在步驟 2 中，選取 **View findings** 前往 Findings 頁面。有關此頁面的詳細資訊，請參閱[使用 findings]({{site.url}}{{site.baseurl}}/security-analytics/usage/findings/)。
* 在步驟 3 中，選取 **View alerts** 前往 Security alerts 頁面。有關此頁面的詳細資訊，請參閱[使用警示]({{site.url}}{{site.baseurl}}/security-analytics/usage/alerts/)。
* 在步驟 4 中，選取 **Manage rules** 前往 Rules 頁面。有關規則的更多資訊，請參閱[使用規則]({{site.url}}{{site.baseurl}}/security-analytics/usage/rules/)。

---
## Findings 與警示數量

Findings 與警示數量區段提供一個圖表，顯示最新 findings 的資料。使用 **Group by** 下拉式清單選取 **All findings** 或 **Log type**。

![顯示 findings 與警示數量的圖表。]({{site.url}}{{site.baseurl}}/images/Security/count.png){: width="75%" }

---
## 最近的警示

Recent alerts 表格依時間、觸發條件名稱與警示嚴重性顯示最近的警示。選取 **View alerts** 前往 Alerts 頁面。

![顯示最近警示的表格。]({{site.url}}{{site.baseurl}}/images/Security/recent-alerts.png){: width="50%" }

---
## 最近的 findings

Recent findings 表格依時間、規則名稱、規則嚴重性與偵測器顯示最近的 findings。選取 **View all findings** 前往 Findings 頁面。

![顯示最近 findings 的表格。]({{site.url}}{{site.baseurl}}/images/Security/recent-findings.png){: width="50%" }

---
## 最常觸發的偵測規則

此區段以圖形方式呈現最常觸發 findings 的偵測規則，以及它們佔整體百分比與其他規則的比較。圖表所代表的規則名稱列於右側。您可以將滑鼠游標停留在圖表上的每個顏色，以查看其所代表偵測規則的詳細資訊。

![Overview 頁面上的偵測規則圖表]({{site.url}}{{site.baseurl}}/images/Security/rule_graph.png){: width="50%" }

---
## 偵測器

Detectors 區段依偵測器名稱、狀態 (啟用/停用) 與記錄類型顯示可用偵測器的清單。選取 **View all detectors** 前往 Detectors 頁面。選取 **Create detector** 可直接前往 Define detector 頁面。

![顯示可用偵測器的表格。]({{site.url}}{{site.baseurl}}/images/Security/detector-overview.png){: width="50%" }

