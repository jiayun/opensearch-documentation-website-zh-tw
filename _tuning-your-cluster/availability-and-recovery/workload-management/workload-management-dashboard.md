---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
title: "在 OpenSearch Dashboards 中管理工作負載"
layout: default
parent: Workload management
grand_parent: Availability and recovery
nav_order: 60
---

# 在 OpenSearch Dashboards 中管理工作負載

您可以在 OpenSearch Dashboards 中監視和控制叢集內的資源使用量：

- 依工作負載群組檢視即時 CPU 與記憶體使用量。
- 識別超出資源閾值的群組。
- 設定工作負載群組與自動標籤規則。
- 設定拒絕閾值，以進行資源型查詢控制。

## 必要條件

開始之前，請先安裝 Workload Management 外掛程式。如需更多資訊，請參閱[安裝工作負載管理]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/workload-management/wlm-feature-overview#installing-workload-management)。

## 監視工作負載使用量

若要監視叢集中工作負載的資源使用量，請在頂端功能表列前往 **OpenSearch Plugins** > **Workload management**。工作負載管理的登陸頁面如下圖所示。

![工作負載管理的登陸頁面]({{site.url}}{{site.baseurl}}/images/Workload-Management/Overview.png)

**Total workload groups** 面板顯示已定義的工作負載群組數量。**Total groups exceeding limits** 面板顯示超出閾值的工作負載群組數量。


主面板在概觀表格中提供工作負載資訊，包含下列欄位。

| 欄位                   | 說明                                                                                                                                                            |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Workload group name**  | 若要檢視節點層級的工作負載群組詳細資訊並更新組態設定，請選取工作負載群組連結。如需更多資訊，請參閱[檢視工作負載群組詳細資訊](#viewing-workload-group-details)。                                                                                                                                 |
| **CPU usage**、**Memory usage** | 盒鬚圖，顯示各群組跨節點的即時 CPU 與記憶體使用量。閾值以紅色顯示。                                                                                              |
| **Total completions**    | 與該工作負載群組相關聯的已完成任務總數。單一查詢可能產生多個已完成任務，例如協調器與分片層級的任務。 |
| **Total rejections**     | 因資源限制而遭拒絕的任務總數。                                                                                                                                 |
| **Total cancellations**  | 在完成前被取消的任務總數。                                                                                                                                      |

使用搜尋列依工作負載群組名稱篩選表格。
{: .tip}

若要檢視最小值、Q1、中位數、Q3 與最大值，請將滑鼠游標停留在 CPU 或記憶體盒鬚圖上。資訊會顯示在工具提示中，如下圖所示。

![盒鬚圖工具提示]({{site.url}}{{site.baseurl}}/images/Workload-Management/BoxplotTooltip.png){: width="240px" }

## 檢視工作負載群組詳細資訊

若要檢視特定工作負載群組的詳細資訊，請執行下列步驟：

1. 在概觀表格中，選取群組名稱。
1. 若要檢視工作負載群組統計資料，請選取 **Resources** 索引標籤（預設選取）。在此索引標籤中，您可以依節點檢視工作負載群組的即時使用量與查詢統計資料。 
1. 若要檢視工作負載群組的設定，請選取 **Settings** 索引標籤。

## 建立工作負載群組

若要建立新的工作負載群組，請執行下列步驟：

1. 在工作負載管理登陸頁面上，選取 **Create workload group**。
1. 在 **Overview** 區段中，輸入下列資訊：
  - **Name**：唯一且具描述性的名稱。
  - **Description (Optional)**：簡短說明群組的用途。
      
      只有在定義了規則時，描述才會被儲存。
      {: .note}
1. 在 **Rules** 區段中，執行下列動作：
    1. 選取 **Resiliency mode**。在 **Soft** 模式下，若資源可用，查詢可以超出限制。在 **Enforced** 模式下，當使用量超出限制時，查詢會被拒絕。
    1. 新增一或多個 **Index wildcard** 模式，以定義哪些查詢會自動標記到此群組。任何目標索引名稱以這些模式之一開頭的查詢，都會自動指派到此群組。多個模式之間以逗號分隔（例如 `logs-,metrics-`）。
    1. 若要定義多條規則，請選取 **Add another rule**。使用垃圾桶圖示刪除規則。
1. 在 **Resource thresholds** 區段中，輸入下列資訊：
  - **Reject queries when CPU usage exceeds**：設定 CPU 使用量百分比限制。例如，輸入 `10` 表示 10%。所有工作負載群組的 CPU 總使用量不得超過 **100%**。
  - **Reject queries when memory usage exceeds**：設定記憶體使用量百分比限制。所有工作負載群組的記憶體總使用量不得超過 **100%**。 
  
    您必須至少定義一個閾值（CPU 使用量或記憶體使用量）。閾值一經設定即無法清除。 
    {: .note}

    如果您最初設定了 CPU 閾值，但之後只想依賴記憶體限制（反之亦然），可以將群組切換為 **soft** 韌性模式來達成。在 soft 模式下，即使定義了限制，只要節點資源可用，系統仍允許查詢繼續執行。
    {: .tip}
1. 選取 **Create workload group**。

## 修改工作負載群組設定

若要修改特定工作負載群組的設定，請執行下列步驟：

1. 在概觀表格中，選取群組名稱。
1. 選取 **Settings** 索引標籤。 
1. 修改工作負載群組的組態。如需設定的更多資訊，請參閱[建立工作負載群組](#creating-a-workload-group)。  
1. 若要更新設定，請選取 **Apply Changes**。

### 預設工作負載群組

`DEFAULT_WORKLOAD_GROUP` 無法編輯。其 CPU 與記憶體限制固定為 100%。對此群組而言，**Settings** 索引標籤為停用狀態。

## 相關文件

- [工作負載群組]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/workload-management/workload-groups/)
- [工作負載群組規則]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/workload-management/workload-group-rules/)