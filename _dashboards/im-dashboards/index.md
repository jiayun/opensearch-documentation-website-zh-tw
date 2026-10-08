---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引管理"
nav_order: 80
has_children: false
redirect_from:
  - /dashboards/im-dashboards/
  - /dashboards/admin-ui-index/
---

# OpenSearch Dashboards 中的索引管理

OpenSearch Dashboards 中的 **Index Management** 頁面提供一個介面，讓您執行原本可使用 [Index API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/index/) 進行的索引作業：建立索引並定義其對應、開啟與關閉索引、合併與分割索引，以及使用狀態管理政策將這些作業自動化。

若要前往 **Index Management** 頁面，請在頂端選單中前往 **Management > Index Management**。下圖顯示 **Index Management** 頁面。

![Index Management 頁面]({{site.url}}{{site.baseurl}}/images/dashboards/index-management-UI.png)

索引管理不包含對索引中文件的作業。若要將資料新增至索引，請參閱[將您的資料匯入 OpenSearch]({{site.url}}{{site.baseurl}}/getting-started/ingest-data/)。若要查詢資料，請參閱 [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/dashboards/)。

## Index Management 頁面

**Index Management** 頁面的左側面板包含下列頁面。

| 頁面 | 說明 | 文件 |
| :--- | :--- | :--- |
| **State management policies** | 建立、編輯及刪除可自動管理索引的政策。 | [政策]({{site.url}}{{site.baseurl}}/im-plugin/ism/policies/#policies-in-opensearch-dashboards) |
| **Policy managed indexes** | 檢視由政策管理的每個索引的狀態、變更其政策，或停止管理該索引。 | [受管理的索引]({{site.url}}{{site.baseurl}}/im-plugin/ism/managedindexes/#managed-indexes-in-opensearch-dashboards) |
| **Indexes** | 建立索引，並檢視其設定、對應與統計資料。開啟、關閉、重新編製索引及刪除索引、對索引套用政策，並透過重新整理、排清、強制合併、縮減、分割及滾動更新來維護索引。 | [索引作業]({{site.url}}{{site.baseurl}}/im-plugin/index-operations/#index-operations-in-opensearch-dashboards)、[索引維護]({{site.url}}{{site.baseurl}}/im-plugin/index-maintenance/#index-maintenance-in-opensearch-dashboards) |
| **Data streams** | 建立資料串流、檢視其支援索引，以及對其進行滾動更新。 | [資料串流]({{site.url}}{{site.baseurl}}/im-plugin/data-streams/#data-streams-in-opensearch-dashboards) |
| **Templates** | 建立用於設定新索引與資料串流的索引範本與元件範本。 | [索引範本]({{site.url}}{{site.baseurl}}/im-plugin/index-templates/#index-templates-in-opensearch-dashboards) |
| **Aliases** | 建立別名、將索引新增至別名，以及設定寫入索引。 | [索引別名]({{site.url}}{{site.baseurl}}/im-plugin/index-alias/#index-aliases-in-opensearch-dashboards) |
| **Rollup jobs** | 建立將舊資料彙總至較小索引的作業。 | [索引彙整]({{site.url}}{{site.baseurl}}/im-plugin/index-rollups/index/#index-rollups-in-opensearch-dashboards) |
| **Transform jobs** | 建立將索引的彙總檢視寫入第二個索引的作業。 | [索引轉換]({{site.url}}{{site.baseurl}}/im-plugin/index-transforms/index/#index-transforms-in-opensearch-dashboards) |
| **Notification settings** | 選擇在完成或失敗時傳送通知的索引作業，以及接收通知的管道。 | [長時間執行作業的通知]({{site.url}}{{site.baseurl}}/im-plugin/notifications-settings/#notifications-in-opensearch-dashboards) |

## 相關文件

- [管理索引]({{site.url}}{{site.baseurl}}/im-plugin/)
- [Index API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/index/)
- [Index State Management]({{site.url}}{{site.baseurl}}/im-plugin/ism/index/)
