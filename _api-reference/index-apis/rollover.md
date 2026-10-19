---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "輪替索引"
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

## 輪替類型

您可以輪替資料串流、只有一個索引的索引別名，或具有寫入索引的索引別名。

### 資料串流

當您對資料串流執行輪替操作時，API 會為該串流產生新的寫入索引。同時，該串流先前的寫入索引會轉換為一般的後端索引（backing index）。此外，輪替程序會遞增資料串流的世代計數。資料串流的輪替不支援在請求本文中指定索引設定。

### 只有一個索引的索引別名

當您對關聯單一索引的索引別名啟動輪替時，API 會產生新的索引，並解除原始索引與該別名的關聯。

### 具有寫入索引的索引別名

當索引別名參照多個索引時，必須將其中一個索引指定為寫入索引。在輪替期間，API 會建立新的寫入索引，並將其 `is_write_index` 屬性設為 `true`，同時將先前寫入索引的 `is_write_index property` 設為 `false.` 以更新該索引。

## 遞增別名的索引名稱

在索引別名輪替過程中，如果您未指定自訂名稱，且目前索引的名稱以連字號加上數字結尾（例如 `my-index-000001` 或 `my-index-3`），則輪替操作會自動遞增該數字作為新索引的名稱。例如，輪替 `my-index-000001` 會產生 `my-index-000002`。數字部分一律會以前置零補齊，以確保長度固定為六個字元。

## 在索引輪替中使用日期數學

當您使用索引別名來處理時間序列資料時，可以在索引名稱中使用[日期數學]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/)來追蹤輪替日期。例如，您可以建立一個指向 `my-index-{now/d}-000001` 的別名。如果您在 2029 年 6 月 11 日建立別名，則索引名稱會是 `my-index-2029.06.11-000001`。若在 2029 年 6 月 12 日進行輪替，新索引將命名為 `my-index-2029.06.12-000002`。實際範例請參閱[使用寫入索引輪替索引別名](#rolling-over-an-index-alias-with-a-write-index)。如需完整的日期數學索引名稱語法，以及必須在請求 URL 中編碼的字元，請參閱[索引名稱中的日期數學]({{site.url}}{{site.baseurl}}/api-reference/index-name-syntax/#date-math-in-index-names)。

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明 
:--- | :--- | :--- 
`rollover-target` | 字串 | 要輪替的資料串流或索引別名名稱。必要。 |
`target-index` | 字串 | 要建立的索引名稱。支援日期運算。資料串流不支援此參數。如果別名目前寫入索引的名稱不是以 `-` 加上數字結尾（例如 `my-index-000001` 或 `my-index-2`），則此參數為必要。 

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 資料類型 | 說明 
:--- | :--- | :--- 
`cluster_manager_timeout` | 時間 | 等待連線至叢集管理員節點的時間量。預設為 `30s`。
`dry_run` | 布林值 | 若為 `true`，OpenSearch 會檢查目前索引是否符合輪替條件，並傳回將建立的索引名稱，但不會執行輪替。預設為 `false`。
`timeout` | 時間 | 等待回應的時間量。預設為 `30s`。
`wait_for_active_shards` | 字串 | OpenSearch 處理請求前必須可用的作用中分片數量。預設為 `1`（僅主要分片）。您也可以設為 `all` 或正整數。大於 `1` 的值需要副本。例如，若您指定值為 `3`，則該索引必須有兩個副本分散於另外兩個節點上，操作才能成功。

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
`routing` | 字串 | 用於將編製索引與搜尋操作路由至特定分片的值。
`search_routing` | 字串 | 將搜尋操作路由至特定分片。指定時，會覆寫搜尋操作的 `routing`。

### `mappings`

`mappings` 參數指定索引欄位對應。此參數為選用。如需詳細資訊，請參閱[對應與欄位類型]({{site.url}}{{site.baseurl}}/mappings/)。

### `conditions`

`conditions` 參數是選用的物件，用於定義觸發輪替的條件。若有提供，OpenSearch 只會在目前索引符合一或多個指定條件時才執行輪替。若省略，則會在沒有任何前置條件的情況下無條件執行輪替。

此物件本文支援下列參數。

參數 | 資料類型 | 說明 
:--- | :--- | :--- 
`max_age` | 時間單位 | 在自索引建立起算的最大經過時間達到後觸發輪替。選用。 |
`max_docs` | 整數 | 在達到指定的最大文件數後觸發輪替，不包括上次重新整理後新增的文件以及副本分片中的文件。選用。 
`max_size` | 位元組單位  | 在索引達到指定大小時觸發輪替，該大小計算為所有主要分片的總大小。副本不計入。請使用 `_cat indices` API 並檢查 `pri.store.size` 值，以查看目前的索引大小。選用。

### `settings`

`settings` 參數指定索引組態選項。如需詳細資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。

## 範例請求

下列範例說明如何使用 Rollover Index API。當符合一個或多個指定條件時，就會進行輪替：

- 索引建立已滿 5 天或以上。
- 索引包含 500 份或以上的文件。
- 索引大小為 100 GB 或以上。

### 輪替資料串流

如果目前的寫入索引符合任一指定條件，下列請求會輪替資料串流：

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

### 輪替具有寫入索引的索引別名

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

下一個請求會使用別名執行輪替：

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

### 在輪替期間指定設定

在大多數情況下，您可以使用索引範本自動設定在輪替操作期間建立的索引。不過，輪替索引別名時，您可以傳送下列請求，使用 Rollover Index API 加入額外的索引設定，或覆寫範本中定義的設定：

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
