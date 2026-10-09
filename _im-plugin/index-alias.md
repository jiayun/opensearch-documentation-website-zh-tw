---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引別名"
nav_order: 20
redirect_from:
  - /opensearch/index-alias/
---

# 索引別名

別名是指向一或多個索引的虛擬索引名稱。查詢別名時，OpenSearch 會將它解析為背後的索引，因此即使別名涵蓋的索引有所變動，您的用戶端仍可持續使用同一個穩定的名稱。

例如，如果您將記錄檔儲存在每月建立的索引中，而且通常查詢最近兩個月的資料，可以建立一個 `last_2_months` 別名，並在每個月更新它所指向的索引。應用程式中的查詢永遠不需要改變。

別名也可用於執行下列操作：

- 在不停機的情況下從一個索引切換到另一個索引，例如將資料重新編製索引至採用新對應的索引，並在複製完成後切換。
- 在別名上附加篩選器，以提供相同資料的不同檢視。
- 保留環境專屬名稱，例如 `production-data` 和 `staging-data`，使其與解析到的索引互相獨立。
- 將經由別名的請求路由到特定分片，讓搜尋讀取較少的分片。如需更多資訊，請參閱[管理別名]({{site.url}}{{site.baseurl}}/api-reference/alias/aliases-api/#example-basic-routing)。
- 對單一寫入目標背後的時間序列索引執行輪替。請參閱[輪替索引]({{site.url}}{{site.baseurl}}/im-plugin/index-maintenance/#rolling-over-an-index)。

別名具有下列特性：

- 別名變更是原子性的。別名永遠不會指向非預期的索引集合，即使只有一瞬間也不會。
- 萬用字元模式會在建立別名時解析。之後建立且符合該模式的索引不會自動加入。
- 若要寫入指向多個索引的別名，必須將其中一個索引指定為寫入索引。
- 篩選別名上的篩選器適用於透過該別名執行的所有搜尋、計數與依查詢刪除操作。

## 建立別名

本節的範例使用兩個索引，您可以使用下列請求建立它們：

```json
PUT /logs-2024-01
```
{% include copy-curl.html %}

```json
PUT /logs-2024-02
```
{% include copy-curl.html %}

最基本的別名指向單一索引：

```json
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "logs-2024-01",
        "alias": "current-logs"
      }
    }
  ]
}
```
{% include copy-curl.html %}

您也可以在建立索引時附加別名：

```json
PUT /logs-2024-03
{
  "aliases": {
    "current-logs": {},
    "all-logs": {}
  }
}
```
{% include copy-curl.html %}

## 將別名切換到不同的索引

在同一個請求中結合 `remove` 與 `add`，讓別名在單一原子性步驟中於索引之間移動：

```json
POST /_aliases
{
  "actions": [
    {
      "remove": {
        "index": "logs-2024-01",
        "alias": "current-logs"
      }
    },
    {
      "add": {
        "index": "logs-2024-02",
        "alias": "current-logs"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 將別名指向多個索引

使用 `indices` 欄位，讓一個別名涵蓋多個索引：

```json
POST /_aliases
{
  "actions": [
    {
      "add": {
        "indices": ["logs-2024-01", "logs-2024-02"],
        "alias": "recent-logs"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 指定寫入索引

指向多個索引的別名會拒絕編製索引的請求，直到其中一個索引被標記為寫入索引：

```json
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "logs-2024-02",
        "alias": "active-logs",
        "is_write_index": true
      }
    },
    {
      "add": {
        "index": "logs-2024-01",
        "alias": "active-logs"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 篩選別名

在別名上附加篩選器，即可用別名自己的名稱公開索引的子集。建立一個帶有 `level` 欄位以供篩選的索引：

```json
PUT /application-logs
{
  "mappings": {
    "properties": {
      "level": {
        "type": "keyword"
      }
    }
  }
}
```
{% include copy-curl.html %}

下列別名只會傳回 `application-logs` 中 `level` 欄位為 `ERROR` 的文件：

```json
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "application-logs",
        "alias": "error-logs",
        "filter": {
          "term": {
            "level": "ERROR"
          }
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 檢視與查詢別名

下表列出常見的別名請求。

| 任務 | 請求 |
| :--- | :--- |
| 列出所有別名 | `GET /_cat/aliases?v` |
| 取得單一別名 | `GET /_alias/current-logs` |
| 檢查別名是否存在 | `HEAD /_alias/current-logs` |
| 透過別名搜尋 | `GET /current-logs/_search` |

如需所有別名操作及其參數，請參閱[別名 API]({{site.url}}{{site.baseurl}}/api-reference/alias/)。

## OpenSearch Dashboards 中的索引別名

若要前往 **Index Management** 頁面，請在頂端選單中前往 **Management > Index Management**。選取 **Aliases** 以列出叢集中的別名，以及每個別名的寫入索引與所屬索引。

下圖顯示 **Aliases** 頁面。

![Aliases 頁面]({{site.url}}{{site.baseurl}}/images/admin-ui-index/aliases-list.png)

### 建立別名

別名至少涵蓋一個索引，因此請先建立索引再建立別名。若要建立索引，請參閱[建立索引]({{site.url}}{{site.baseurl}}/im-plugin/index-operations/#creating-an-index-1)。

1. 在 **Index Management** 中，選取 **Aliases**，然後選取 **Create alias**。
1. 輸入別名的名稱。
1. 在 **Indexes or index patterns** 中，選取或輸入別名涵蓋的索引與索引模式。
1. 選取 **Create alias**。

### 編輯別名

1. 在 **Index Management** 中，選取 **Aliases**。
1. 在 **Alias name** 欄中選取別名名稱。
1. 在 **Indexes or index patterns** 中，新增或移除索引與索引模式。您無法重新命名現有的別名。
1. 選取 **Save changes**。

### 刪除別名

1. 在 **Index Management** 中，選取 **Aliases**。
1. 勾選每個要刪除之別名旁的核取方塊。
1. 選取 **Actions**，然後選取 **Delete**。
1. 在確認對話方塊中輸入 `delete`，然後選取 **Delete**。

刪除別名不會刪除其背後的索引。

### 輪替別名

1. 在 **Index Management** 中，選取 **Aliases**。
1. 選取 **Actions**，然後選取 **Roll over**。
1. 在 **Configure source** 中，選取要輪替的別名。其目前的寫入索引會顯示為 **Assigned source index**。
1. 在 **Configure new rollover index** 中，輸入新寫入索引的名稱，然後輸入其定義、設定與對應。若要重複使用目前寫入索引的組態，請選取 **Import from old write index**。
1. 選取 **Roll over**。

**Write index** 欄會顯示新的寫入索引，而 **Index name** 欄會列出別名中的所有索引。

重新整理、排清、清除快取與強制合併也可以從 **Aliases** 頁面執行，並套用至所選別名的開啟後端索引。相關程序請參閱[OpenSearch Dashboards 中的索引維護]({{site.url}}{{site.baseurl}}/im-plugin/index-maintenance/#index-maintenance-in-opensearch-dashboards)。

## 相關文件

- [別名 API]({{site.url}}{{site.baseurl}}/api-reference/alias/)
- [資料串流]({{site.url}}{{site.baseurl}}/im-plugin/data-streams/)
- [索引維護]({{site.url}}{{site.baseurl}}/im-plugin/index-maintenance/)
