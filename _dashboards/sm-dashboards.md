---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "快照管理"
nav_order: 90
redirect_from:
  - /dashboards/admin-ui-index/sm-dashboards/
---

# OpenSearch Dashboards 中的快照管理

[快照]({{site.url}}{{site.baseurl}}/opensearch/snapshots/index/)是叢集索引與狀態的備份。狀態包括叢集設定、節點資訊、索引中繼資料（對應、設定、範本）以及分片配置。OpenSearch Dashboards 中的 Snapshot Management (SM) 介面提供建立與還原快照的整合式解決方案。

下圖顯示此介面的範例。

![Snapshot Management 使用者介面]({{site.url}}{{site.baseurl}}/images/dashboards/snapshots-UI.png)

## 快照使用案例

快照有兩個主要用途：

1. 從故障中復原

    例如，若叢集健康狀態變成紅色，您可以從快照還原紅色狀態的索引。

2. 從一個叢集遷移到另一個叢集

    例如，若您要從概念驗證環境移轉到生產叢集，可以為前者建立快照，然後在後者上還原。

## 建立儲存庫

在建立 SM 政策之前，請先為快照設定儲存庫。

1. 在 OpenSearch Dashboards 主選單中，選取 **Management** > **Snapshot Management**。
2. 在左側面板的 **Snapshot Management** 下，選取 **Repositories**。
3. 選擇 **Create Repository** 按鈕。
4. 輸入儲存庫名稱、類型與位置。
5. （選用）選取 **Advanced Settings**，並以 JSON 物件的形式輸入此儲存庫的其他設定。
#### 範例
```json
    {
        "chunk_size": null,
        "compress": false,
        "max_restore_bytes_per_sec": "40m",
        "max_snapshot_bytes_per_sec": "40m",
        "readonly": false
    }
```
6. 選擇 **Add** 按鈕。

{::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/star-icon.png" class="inline-icon" alt="star icon"/>{:/} **注意：**若您需要自動建立快照，可以使用快照政策。
{: .note purple}

## 刪除儲存庫

若要刪除快照儲存庫組態，請從 **Repositories** 清單中選取該儲存庫，然後選擇 **Delete** 按鈕。

## 建立 SM 政策

建立 SM 政策以設定自動快照。SM 政策會定義自動建立快照的排程，以及選用的自動刪除排程。

1. 在 OpenSearch Dashboards 主選單中，選取 **Management** > **Snapshot Management**。
1. 在左側面板的 **Snapshot Management** 下，選取 **Snapshot Policies**。
1. 選取 **Create Policy** 按鈕。
1. 在 **Policy settings** 區段中：
    1. 輸入政策名稱。
    1. （選用）輸入政策說明。
1. 在 **Source and destination** 區段中：
    1. 以清單或索引模式的形式選取或輸入來源索引。
    1. 選取快照的儲存庫。若要[建立新的儲存庫](#creating-a-repository)，請選取 **Create** 按鈕。
1. 在 **Snapshot schedule** 區段中：
    1. 選取所需的快照頻率，或輸入自訂的 cron 運算式作為快照頻率。
    1. 選取開始時間與時區。
1. 在 **Retention period** 區段中：
    1. 選擇保留所有快照，或指定保留條件（保留快照的最長存在時間）。
    1. （選用）在 **Additional settings** 中，選取保留快照的最小與最大數量、刪除頻率以及刪除開始時間。
1. 在 **Notifications** 區段中，選取您希望收到通知的快照活動。
1. （選用）在 **Advanced settings** 區段中，選取所需的選項：
    - **Include cluster state in snapshots**
    - **Ignore unavailable indices**
    - **Allow partial snapshots**
1. 選取 **Create** 按鈕。

## 檢視、編輯或刪除 SM 政策

您可以在政策詳細資料頁面上檢視、編輯或刪除 SM 政策。

1. 在 OpenSearch Dashboards 主選單中，選取 **Management** > **Snapshot Management**。
1. 在左側面板的 **Snapshot Management** 下，選取 **Snapshot Policies**。
1. 按一下您要檢視、編輯或刪除之政策的 **Policy name**。<br>
政策詳細資料頁面會顯示政策設定、快照排程、快照保留期間、通知，以及最近一次的建立與刪除。<br> 若快照建立或刪除失敗，您可以在 **Last Creation/Deletion** 區段中檢視有關失敗的資訊。若要檢視失敗訊息，請按一下 **Info** 欄中的 **cause**。
1. 若要編輯或刪除 SM 政策，請選取 **Edit** 或 **Delete** 按鈕。

## 啟用、停用或刪除 SM 政策

1. 在 OpenSearch Dashboards 主選單中，選取 **Management** > **Snapshot Management**。
1. 在左側面板的 **Snapshot Management** 下，選取 **Snapshot Policies**。
1. 在清單中選取一或多個政策。
1. 若要啟用或停用所選的 SM 政策，請選取 **Enable** 或 **Disable** 按鈕。若要刪除所選的 SM 政策，請在 **Actions** 清單中選取 **Delete** 選項。

## 檢視快照

1. 在 OpenSearch Dashboards 主選單中，選取 **Management** > **Snapshot Management**。
1. 在左側面板的 **Snapshot Management** 下，選取 **Snapshots**。
所有自動或手動建立的快照都會顯示在清單中。
1. 若要檢視快照，請按一下其 **Name**。

## 建立快照

請依照下列步驟手動建立快照：

1. 在 OpenSearch Dashboards 主選單中，選取 **Management** > **Snapshot Management**。
1. 在左側面板的 **Snapshot Management** 下，選取 **Snapshots**。
1. 選取 **Take snapshot** 按鈕。
1. 輸入快照名稱。
1. 以清單或索引模式的形式選取或輸入來源索引。
1. 選取快照的儲存庫。
1. （選用）在 **Advanced options** 區段中，選取所需的選項：
    - **Include cluster state in snapshots**
    - **Ignore unavailable indices**
    - **Allow partial snapshots**
1. 選擇 **Add** 按鈕。

## 刪除快照

**Delete** 按鈕會從儲存庫中[刪除]({{site.url}}{{site.baseurl}}/api-reference/snapshots/delete-snapshot/)快照。

1. 若要檢視您的儲存庫清單，請選擇 **Snapshot Management** 區段下的 **Repositories**。
2. 若要檢視您的快照清單，請選擇 **Snapshot Management** 區段下的 **Snapshots**。

## 還原快照

1. 在 OpenSearch Dashboards 主選單中，選取 **Management** > **Snapshot Management**。
1. 在左側面板的 **Snapshot Management** 下，選取 **Snapshots**。預設會選取 **Snapshots** 索引標籤。
1. 選取您要還原之快照旁的核取方塊。下圖顯示範例：
    ![快照]({{site.url}}{{site.baseurl}}/images/restore-snapshot/restore-snapshot-main.png)

    {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/star-icon.png" class="inline-icon" alt="star icon"/>{:/} **注意：**您只能還原狀態為 `Success` 或 `Partial` 的快照。快照的狀態會顯示在 **Snapshot status** 欄中。
    {: .note purple}
1. 在 **Restore snapshot** 飛出視窗中，選取還原快照的選項。

    **Restore snapshot** 飛出視窗會列出快照名稱與狀態。若要檢視快照中的索引清單，請選取 **Indices** 下的數字（例如下圖中的 `27`）。此數字代表快照中的索引數量。

    ![還原快照]({{site.url}}{{site.baseurl}}/images/restore-snapshot/restore-snapshot.png){: width="450" }

    如需有關 **Restore snapshot** 飛出視窗中選項的詳細資訊，請參閱[還原快照]({{site.url}}{{site.baseurl}}/opensearch/snapshots/snapshot-restore#restore-snapshots)。

    **忽略遺失的索引**

    若您指定要從快照還原哪些索引，並選取 **Ignore unavailable indices** 選項，還原作業會忽略快照中遺失的索引。例如，若您要還原 `log1` 與 `log2` 索引，但 `log2` 不在快照中，則會還原 `log1` 並忽略 `log2`。若您未選取 **Ignore unavailable indices**，當要還原的索引在快照中遺失時，整個還原作業都會失敗。

    **自訂索引設定**

    您可以選擇為從快照還原的索引自訂部分設定：<br>
        &emsp;&#x2022; 選取 **Customize index settings** 核取方塊，為指定的索引設定提供新值。所有新還原的索引都會使用這些值，而不是快照中的值。<br>
        &emsp;&#x2022; 選取 **Ignore index settings** 核取方塊，指定要忽略的快照中設定。所有新還原的索引都會對這些設定使用叢集預設值。

    下圖中的範例會為所有新還原的索引將 `index.number_of_replicas` 設為 `0`、將 `index.auto_expand_replicas` 設為 `true`，並將 `index.refresh_interval` 與 `index.max_script_fields` 設為叢集預設值。

    ![自訂設定]({{site.url}}{{site.baseurl}}/images/restore-snapshot/restore-snapshot-custom.png){: width="450" }

    如需有關索引設定的詳細資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/im-plugin/index-settings/)。

    如需無法變更或忽略的設定清單，請參閱[還原快照]({{site.url}}{{site.baseurl}}/opensearch/snapshots/snapshot-restore#restore-snapshots)。

    選擇選項後，請選取 **Restore snapshot** 按鈕。
1. （選用）若要監控還原進度，請在確認對話方塊中選取 **View restore activities**。您也可以隨時選取 **Restore activities in progress** 索引標籤來監控還原進度，如下圖所示。

    ![還原活動]({{site.url}}{{site.baseurl}}/images/restore-snapshot/restore-snapshot-activities.png)

    您可以在 **Status** 欄中檢視工作已完成的百分比。快照還原完成後，**Status** 會變更為 `Completed (100%)`。

    {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/star-icon.png" class="inline-icon" alt="star icon"/>{:/} **注意：****Restore activities in progress** 面板不會持續保留。它只會顯示目前還原作業的進度。若有多個還原作業正在執行，面板會顯示最近的一個。
    {: .note purple}
    若要檢視每個正在還原之索引的狀態，請選取 **Indices being restored** 欄中的連結（在上圖中為 `27 Indices` 連結）。**Indices being restored** 飛出視窗（如下圖所示）會顯示每個索引及其還原狀態。

    ![還原索引]({{site.url}}{{site.baseurl}}/images/restore-snapshot/restore-snapshot-indices.png)

 還原作業完成後，已還原的索引會列在 **Indices** 面板中。若要檢視這些索引，請在左側面板的 **Index Management** 下，選擇 **Indices**。

![檢視索引]({{site.url}}{{site.baseurl}}/images/restore-snapshot/restore-snapshot-indices-panel.png)
