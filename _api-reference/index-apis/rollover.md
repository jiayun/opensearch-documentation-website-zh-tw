---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "滾動更新索引"
parent: Index operations
grand_parent: Index APIs
nav_order: 70
---

# Roll Over Index API
**1.0 版引入**
{: .label .label-purple }

Roll Over Index API 操作會根據 `wait_for_active_shards` 設定，為資料串流或索引別名建立新的索引。

## 端點

```json
POST /{rollover-target}/_rollover/
POST /{rollover-target}/_rollover/{target-index}
```

## 滾動更新類型

您可以滾動更新資料串流、只有一個索引的索引別名，或具有寫入索引的索引別名。

### 資料串流

當您對資料串流執行滾動更新操作時，API 會為該串流產生新的寫入索引。同時，該串流先前的寫入索引會轉換為一般的支援索引 (backing index)。此外，滾動更新程序會遞增資料串流的世代計數。資料串流的滾動更新不支援在請求本文中指定索引設定。

### 只有一個索引的索引別名

當您對關聯單一索引的索引別名啟動滾動更新時，API 會產生新的索引，並解除原始索引與該別名的關聯。

### 具有寫入索引的索引別名

當索引別名參照多個索引時，必須將其中一個索引指定為寫入索引。在滾動更新期間，API 會建立新的寫入索引，並將其 `is_write_index` 屬性設為 `true`，同時將先前寫入索引的 `is_write_index property` 設為 `false.` 以更新該索引。

## 遞增別名的索引名稱

在索引別名滾動更新過程中，如果您未指定自訂名稱，且目前索引的名稱以連字號加上數字結尾 (例如 `my-index-000001` 或 `my-index-3`)，則滾動更新操作會自動遞增該數字作為新索引的名稱。例如，滾動更新 `my-index-000001` 會產生 `my-index-000002`。數字部分一律會以前置零補齊，以確保長度固定為六個字元。

## 在索引滾動更新中使用日期運算

為時間序列資料使用索引別名時，您可以在索引名稱中使用[日期運算]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/)來追蹤滾動更新日期。例如，您可以建立指向 `my-index-{now/d}-000001` 的別名。如果您在 2029 年 6 月 11 日建立別名，則索引名稱會是 `my-index-2029.06.11-000001`。若在 2029 年 6 月 12 日進行滾動更新，新索引的名稱會是 `my-index-2029.06.12-000002`。如需實際範例，請參閱[滾動更新具有寫入索引的索引別名](#rolling-over-an-index-alias-with-a-write-index)。

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明 
:--- | :--- | :--- 
`rollover-target` | 字串 | 要滾動更新的資料串流或索引別名名稱。必要。 |
`target-index` | 字串 | 要建立的索引名稱。支援日期運算。資料串流不支援此參數。如果別名目前寫入索引的名稱不是以 `-` 加上數字結尾 (例如 `my-index-000001` 或 `my-index-2`)，則此參數為必要。 

## 查詢參數

下表列出可用的查詢參數。

參數 | 資料類型 | 說明 
:--- | :--- | :--- 
`cluster_manager_timeout` | 時間 | 等待連線至叢集管理員節點的時間長度。預設為 `30s`。
`timeout` | 時間 | 等待回應的時間長度。預設為 `30s`。
`wait_for_active_shards` | 字串 | OpenSearch 處理請求前必須可用的作用中分片數量。預設為 `1` (僅主要分片)。您也可以設為 `all` 或正整數。大於 `1` 的值需要副本。例如，如果您指定的值為 `3`，則索引必須有兩個副本分散在另外兩個節點上，操作才會成功。

## 請求本文欄位

支援下列請求本文欄位。

### `alias`

`alias` 參數以別名名稱作為鍵。當請求本文中存在 `template` 選項時，此參數為必要。物件本文包含下列選用參數。


參數 | 類型 | 說明
:--- | :--- | :---
`filter` | Query DSL 物件 | 限制別名可存取文件數量的查詢。
`index_routing` | 字串 | 將編製索引操作路由至特定分片的值。指定時，會覆寫編製索引操作的 `routing` 值。
`is_hidden` | 布林值 | 隱藏或顯示別名。當值為 `true` 時，別名會隱藏。預設為 `false`。該別名的所有索引在此設定上的值必須一致。
`is_write_index` | 布林值 | 指定寫入索引。當值為 `true` 時，該索引即為別名的寫入索引。預設為 `false`。
`routing` | 字串 | 用於將索引與搜尋操作路由至特定分片的值。
`search_routing` | 字串 | 將搜尋操作路由至特定分片。指定時，會覆寫搜尋操作的 `routing`。

### `mappings`

`mappings` 參數指定索引欄位對應。此參數為選用。如需詳細資訊，請參閱[對應與欄位類型]({{site.url}}{{site.baseurl}}/mappings/)。

### `conditions`

`conditions` 參數是選用物件，用於定義觸發滾動更新的條件。提供此參數時，OpenSearch 只會在目前索引符合一個或多個指定條件時進行滾動更新。若省略此參數，則滾動更新會無條件執行，不需任何先決條件。

物件本文支援下列參數。

參數 | 資料類型 | 說明 
:--- | :--- | :--- 
`max_age` | 時間單位 | 自索引建立起經過的時間達到上限後觸發滾動更新。經過時間一律從索引建立時間開始計算，即使索引起始日期已設定為自訂日期 (例如使用 `index.lifecycle.parse_origination_date` 或 `index.lifecycle.origination_date` 設定時) 也是如此。選用。 |
`max_docs` | 整數 | 達到指定的文件數量上限後觸發滾動更新，不包含上次重新整理後新增的文件及副本分片中的文件。選用。 
`max_size` | 位元組單位  | 當索引達到指定大小時觸發滾動更新，大小以所有主要分片的總大小計算，不計入副本。使用 `_cat indices` API 並查看 `pri.store.size` 值，即可得知目前的索引大小。選用。

### `settings`

`settings` 參數指定索引組態選項。如需詳細資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。

## 範例請求

下列範例說明如何使用 Rollover Index API。當符合一個或多個指定條件時，就會進行滾動更新：

- 索引建立已滿 5 天或以上。
- 索引包含 500 份或以上的文件。
- 索引大小為 100 GB 或以上。

### 滾動更新資料串流

如果目前的寫入索引符合任一指定條件，下列請求會滾動更新資料串流：

<!-- spec_insert_start
component: example_code
rest: POST /my-alias/_rollover
body: |
{
  "conditions": {
    "max_age": "5d",
    "max_docs": 500,
    "max_size": "100gb"
  }
}
-->
{% capture step1_rest %}
POST /my-alias/_rollover
{
  "conditions": {
    "max_age": "5d",
    "max_docs": 500,
    "max_size": "100gb"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.rollover(
  alias = "my-alias",
  body =   {
    "conditions": {
      "max_age": "5d",
      "max_docs": 500,
      "max_size": "100gb"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 滾動更新具有寫入索引的索引別名

下列請求會建立日期時間索引，並將其設為 `my-alias` 的寫入索引。索引名稱必須經過 URL 編碼：`%3Cmy-index-%7Bnow%2Fd%7D-000001%3E` 是 `<my-index-{now/d}-000001>` 的編碼形式，而 `{now/d}` 會解析為目前日期：

```json
PUT %3Cmy-index-%7Bnow%2Fd%7D-000001%3E
{
  "aliases": {
    "my-alias": {
      "is_write_index": true
    }
  }
}
```
{% include copy-curl.html %}

下一個請求會使用別名執行滾動更新：

<!-- spec_insert_start
component: example_code
rest: POST /my-data-stream/_rollover
body: |
{
  "conditions": {
    "max_age": "5d",
    "max_docs": 500,
    "max_size": "100gb"
  }
}
-->
{% capture step1_rest %}
POST /my-data-stream/_rollover
{
  "conditions": {
    "max_age": "5d",
    "max_docs": 500,
    "max_size": "100gb"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.rollover(
  alias = "my-data-stream",
  body =   {
    "conditions": {
      "max_age": "5d",
      "max_docs": 500,
      "max_size": "100gb"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 在滾動更新期間指定設定

在大多數情況下，您可以使用索引範本自動設定在滾動更新操作期間建立的索引。不過，滾動更新索引別名時，您可以傳送下列請求，使用 Rollover Index API 加入額外的索引設定，或覆寫範本中定義的設定：

<!-- spec_insert_start
component: example_code
rest: POST /my-alias/_rollover
body: |
{
  "settings": {
    "index.number_of_shards": 4
  }
}
-->
{% capture step1_rest %}
POST /my-alias/_rollover
{
  "settings": {
    "index.number_of_shards": 4
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.rollover(
  alias = "my-alias",
  body =   {
    "settings": {
      "index.number_of_shards": 4
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 範例回應

OpenSearch 會傳回下列回應，確認除了 `max_size` 以外的所有條件皆已符合：

```json
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "old_index": ".ds-my-data-stream-2029.06.11-000001",
  "new_index": ".ds-my-data-stream-2029.06.12-000002",
  "rolled_over": true,
  "dry_run": false,
  "conditions": {
    "[max_age: 5d]": true,
    "[max_docs: 500]": true,
    "[max_size: 100gb]": false
  }
}
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`indices:admin/rollover`。
