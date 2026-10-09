---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "受管理索引"
nav_order: 20
parent: Index State Management
has_children: false
redirect_from: 
 - /im-plugin/ism/managedindices/
---

# 受管理索引

受管理索引是指已附加 Index State Management (ISM) 政策的索引。本頁面說明如何將受管理索引從一項政策移至另一項政策。

## 變更政策

受管理索引的政策變更受到限制，以確保變更不會使索引處於新政策未定義的狀態。

如果新政策包含與目前狀態完全相同的狀態——名稱相同、動作相同且順序相同——ISM 會立即套用新政策，即使動作正在執行中也一樣。當索引卡在目前狀態且您需要變更立即生效時，請使用此方式。

如果新政策不包含完全相同的狀態，ISM 只會在目前狀態中的所有動作完成後才套用新政策。您也可以指定目前政策中的某個狀態，讓新政策在該狀態之後生效。

若要變更政策，請使用 [Update Managed Index Policy API]({{site.url}}{{site.baseurl}}/im-plugin/ism/api/#update-managed-index-policy) 或 [變更索引的政策](#changing-the-policy-of-an-index) 中的步驟。

## 變更政策參數

下表列出 Change Policy 作業的參數。

參數 | 說明 | 類型 | 必要 | 唯讀
:--- | :--- |:--- |:--- |
`name` |  受管理索引政策的名稱。 | 字串 | 是 | 否
`index` | 此政策所管理的受管理索引名稱。 | 字串 | 是 | 否
`index_uuid`  |  索引的 UUID。 | 字串 | 是 | 否
`enabled` |  當值為 `true` 時，受管理索引由排程器排程並執行。 | 布林值 | 是 | 否
`enabled_time` | 受管理索引上次啟用的時間。如果受管理索引處理程序已停用，則此值為 null。 | 時間戳記 | 是 | 是
`last_updated_time` | 受管理索引上次更新的時間。  | 時間戳記 | 是 | 是
`schedule` | 受管理索引作業的排程。 | 物件 | 是 | 否
`policy_id` | 此受管理索引所使用政策的名稱。 | 字串 | 是 | 否
`policy_seq_no` | 此受管理索引所使用政策的序號。 | 數值 | 是 | 否
`policy_primary_term` | 此受管理索引所使用政策的主要分片任期。 | 數值 | 是 | 否
`policy_version` | 此受管理索引所使用政策的版本。 | 數值 | 是 | 是
`policy` | 供執行時使用、對應於 `policy_version` 的政策快取 JSON。如果政策為 null，表示這是該作業的第一次執行，並會讀入/儲存最新的政策文件。 | 物件 | 否 | 否
`change_policy` | 有關要變更至哪個政策和狀態的資訊。 | 物件 | 否 | 否
`policy_name` | 要更新至的政策名稱。若要更新至最新版本，請將此值設定為與目前的 `policy_name` 相同。 | 字串 | 否 | 是
`state` | 受管理索引完成更新後的狀態。如果未指定狀態，則假設政策結構未變更。 | 字串 | 否 | 是

以下範例顯示受管理索引政策：

```json
{
  "managed_index": {
    "name": "my_index",
    "index": "my_index",
    "index_uuid": "sOKSOfkdsoSKeofjIS",
    "enabled": true,
    "enabled_time": 1553112384,
    "last_updated_time": 1553112384,
    "schedule": {
      "interval": {
        "period": 1,
        "unit": "MINUTES",
        "start_time": 1553112384
      }
    },
    "policy_id": "log_rotation",
    "policy_version": 1,
    "policy": {...},
    "change_policy": null
  }
}
```

## OpenSearch Dashboards 中的受管理索引

若要前往 **Index Management** 頁面，請在頂端選單中前往 **Management > Index Management**。選取 **Policy managed indexes** 以列出由政策管理的索引，以及政策、目前狀態和上一個動作的狀態。

下圖顯示 **Policy managed indexes** 頁面。

![政策管理的索引頁面]({{site.url}}{{site.baseurl}}/images/admin-ui-index/policy-managed-indexes.png)

若要將政策附加至尚未受管理的索引，請參閱 [套用政策]({{site.url}}{{site.baseurl}}/im-plugin/index-operations/#applying-a-policy)。

### 檢視受管理索引的狀態

**Policy managed indexes** 表格會顯示每個索引所處的狀態，以及其上一個動作的狀態。選取失敗索引在 **Info** 欄位中的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/arrow-right-icon.png" class="inline-icon" alt="expand icon"/>{:/} (展開) 圖示，即可檢視失敗原因。若要將表格縮小至特定索引，請在搜尋方塊中輸入名稱。

### 變更索引的政策

1. 在 **Index Management** 中，選取 **Policy managed indexes**。
1. 選取要變更政策的每個索引旁的核取方塊，然後選取 **Change policy**。
1. 在 **Choose managed indexes** 中確認索引。若要將變更限制於特定狀態的索引，請在 **State filters** 中選取那些狀態。
1. 在 **Choose new policy** 中，選取要變更至的政策。
1. 選取新政策生效的時機：

   - **Keep indexes in their current state after the policy takes effect** 會以每個索引目前所處的狀態啟動新政策。
   - **Start from a chosen state after changing policies** 會以您選取的狀態啟動新政策。

1. 選取 **Change**。

有關變更生效時機的限制，請參閱 [變更政策](#change-policy)。

### 新增輪替別名

包含 `rollover` 動作的政策需要一個別名才能進行輪替。如果索引建立時沒有別名，請依下列方式新增：

1. 在 **Index Management** 中，選取 **Policy managed indexes**。
1. 選取索引旁的核取方塊。**Edit rollover alias** 僅在恰好選取一個索引時才可用。
1. 選取 **Edit rollover alias**。
1. 輸入現有別名的名稱，然後選取 **Edit**。

### 移除政策

1. 在 **Index Management** 中，選取 **Policy managed indexes**。
1. 選取要停止管理的每個索引旁的核取方塊。
1. 選取 **Remove policy**。
1. 在確認對話方塊中選取 **Remove**。

移除政策會讓索引及其資料保持原狀。政策最後套用至索引的狀態 (例如 `read_only`) 仍然有效。

### 重試政策

當動作失敗且重試次數用盡時，受管理索引會停在失敗狀態。修正原因，例如缺少輪替別名或快照儲存庫不存在，然後重試：

1. 在 **Index Management** 中，選取 **Policy managed indexes**。
1. 選取每個失敗索引旁的核取方塊。**Retry policy** 僅在選取的索引已失敗時才可用。
1. 選取 **Retry policy**。
1. 選取 **Retry from the failed action**，或選取 **Retry policy from a specific state** 並選取要從中重新開始的狀態。
1. 選取 **Retry**。

## 相關文件

- [政策]({{site.url}}{{site.baseurl}}/im-plugin/ism/policies/)
- [ISM API]({{site.url}}{{site.baseurl}}/im-plugin/ism/api/)
- [ISM 錯誤預防]({{site.url}}{{site.baseurl}}/im-plugin/ism/error-prevention/index/)

