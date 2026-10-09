---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "僅附加索引"
nav_order: 30
---

# 僅附加索引

僅附加索引 (append-only index) 是一種不可變的索引，僅允許文件匯入 (附加)，並在文件初次建立後封鎖所有更新或刪除作業。當您為索引啟用僅附加設定時，OpenSearch 會防止對現有文件進行任何修改。您只能在索引中新增文件。

當您將索引設定為僅附加時，下列作業會回傳錯誤：

- 文件更新呼叫 (Update API)
- 文件刪除呼叫 (Delete API)
- Update by query 呼叫
- Delete by query 呼叫
- 使用 update、delete 或 upsert 動作的 Bulk API 呼叫
- 包含帶有自訂文件 ID 之 index 動作的 Bulk API 呼叫

由於僅附加索引不執行任何更新或刪除作業，因此會略過軟刪除與版本追蹤，從而減少儲存空間用量以及分段合併期間的工作量。請將僅附加索引用於匯入後不會修改的資料，例如記錄檔、指標、可觀測性資料或安全性事件。

## 建立僅附加索引

下列請求會建立一個名為 `my-append-only-index` 的新索引，並停用所有更新：

```json
PUT /my-append-only-index
{
  "settings": {
    "index.append_only.enabled": true
  }
}
```
{% include copy-curl.html %}

索引一旦設定為僅附加，就無法變更為其他索引類型。
{: .warning}


若要將現有索引的資料附加到新的僅附加索引，請使用 Reindex API。由於僅附加索引不支援自訂文件 ID，您需要將來源索引的 `ctx._id` 設定為 `null`。這樣文件就能透過重新索引加入。

下列範例將文件從來源索引 (`my-source-index`) 重新索引到新的僅附加索引。請先建立來源索引：

```json
POST /my-source-index/_doc?refresh=true
{
  "message": "login attempt"
}
```
{% include copy-curl.html %}

然後將其文件重新索引到僅附加索引：

```json
POST /_reindex
{
  "source": {
    "index": "my-source-index"
  },
  "dest": {
    "index": "my-append-only-index"
  },
  "script": {
    "source": "ctx._id = null",
    "lang": "painless"
  }
}

```
{% include copy-curl.html %}

## 批次編製索引的適應性分片選擇
**3.5 版新增**
{: .label .label-purple }

對於僅附加索引，當您未明確指定時，OpenSearch 會自動產生隨機的 `_id` 進行寫入路由。在批次寫入時，單一批次項目可能會被拆分成數十個子批次並分派到不同的分片，這會導致顯著的長尾延遲，並大幅降低寫入效能。

適應性分片選擇可確保單一批次項目的所有子批次都路由到同一個分片，從而大幅提升批次寫入效能。

`index.bulk.adaptive_shard_selection.enabled` 設定是動態的，因此您可以在現有的僅附加索引上啟用它：

```json
PUT /my-append-only-index/_settings
{
  "index.bulk.adaptive_shard_selection.enabled": "true"
}
```
{% include copy-curl.html %}

您也可以在建立索引時設定它：

```json
PUT /my-new-append-only-index
{
  "settings": {
    "index.append_only.enabled": "true",
    "index.bulk.adaptive_shard_selection.enabled": "true"
  }
}
```
{% include copy-curl.html %}

如需更多資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。