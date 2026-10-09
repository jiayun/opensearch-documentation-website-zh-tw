---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用警示"
parent: Using Security Analytics
nav_order: 46
---

# 使用警示

**Alerts** 視窗提供檢視和管理警示的功能。其包含：

- 顯示警示數量、日期，以及狀態或嚴重性等級的長條圖。
- 兩個索引標籤：
  - **Findings**：列出偵測器產生的警示，顯示警示時間、觸發條件名稱，以及觸發警示的偵測器等詳細資訊。
  - **Correlations**：列出關聯規則產生的警示，顯示警示時間、觸發條件名稱，以及觸發警示的關聯規則等詳細資訊。

您可以選取 **Refresh** 按鈕，重新整理 **Alerts** 頁面上的資訊。

---

## 警示圖表

**Alerts** 圖表依警示的狀態或嚴重性顯示警示。使用 **Group by** 下拉式選單，指定 **Alert status** 或 **Alert severity**。

若要指定日期範圍，請選取日曆圖示以開啟下拉式選單。日期選擇器視窗隨即開啟。下圖顯示視窗範例。

![發現項目圖表的日期選擇器]({{site.url}}{{site.baseurl}}/images/Security/find-date-pick.png){: width="55%" }

您可以使用 **Quick select** 設定來指定日期範圍：
* 從第一個下拉式選單中選取 **Last** 或 **Next**，將日期範圍設為目前設定之前或之後。
* 從第二個下拉式選單中選取數字，以定義範圍的數值。
* 從第三個下拉式選單中選取時間單位。可用選項為秒、分鐘、小時、天、週、月和年。
* 選取 **Apply** 按鈕，將時間範圍套用至圖表。圖表會立即更新。

下圖顯示視窗範例。

![Quick select 設定範例]({{site.url}}{{site.baseurl}}/images/Security/quickset.png){: width="40%" }

您可以使用左上角的向左和向右箭頭，分別將時間範圍往前或往後移動。使用這些箭頭時，開始日期和結束日期會顯示在日期範圍欄位中。接著，您可以分別選取這兩個日期，以設定絕對、相對或目前的日期與時間。若變更絕對或相對日期與時間，請選取 **Update** 按鈕以套用變更。 

下圖顯示視窗範例。

![變更日期範圍]({{site.url}}{{site.baseurl}}/images/Security/date-pick.png){: width="55%" }

您也可以選取 **Commonly used** 區段中的選項（請參閱前面的日曆下拉式選單圖片），方便地設定日期範圍。選項包括 **Today**、**Yesterday**、**this week** 和 **week to date**。 

選取常用日期範圍後，您可以選取日期範圍欄位中的 **Show dates** 標籤，以填入範圍。接著，您可以選取開始日期或結束日期，指定絕對、相對或目前的日期與時間設定。若變更絕對或相對日期與時間，請選取 **Update** 按鈕以套用變更。

您也可以從 **Recently used date ranges** 區段中選取選項，以還原為先前的設定。

---

## 警示清單

**Alerts list** 顯示所有警示，並提供兩個索引標籤以顯示不同類型的警示：

- **Findings**：**Alerts list** 依警示觸發時間、警示的觸發條件名稱、觸發警示的偵測器、警示狀態和警示嚴重性顯示所有發現項目。
- **Correlations**：  **Alerts list** 顯示所有關聯，包括關聯規則與時間區間、警示的觸發條件名稱、觸發警示的關聯規則名稱、警示狀態和警示嚴重性。

使用 **Alert severity** 下拉式選單，依嚴重性篩選警示清單。使用 **Status** 下拉式選單，依警示狀態篩選清單。
