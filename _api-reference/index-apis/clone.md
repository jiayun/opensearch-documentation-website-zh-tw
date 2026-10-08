---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "複製索引"
parent: Index operations
grand_parent: Index APIs
nav_order: 20
redirect_from:
  - /opensearch/rest-api/index-apis/clone/
---

# 複製索引 API
**於 1.0 版推出**
{: .label .label-purple }

複製索引 API 會將現有索引複製到新索引，其中每個原始主要分片都會複製成目標索引中的新主要分片。

在下列情境中使用此 API：

- 在進行破壞性變更之前，建立分片數相同的索引備份。
- 在保留原始索引的同時，於複製的副本上測試組態變更。
- 複製索引，以供使用不同設定或別名的平行處理工作流程使用。

複製作業遵循三個步驟，以有效率地複製索引資料：

1. OpenSearch 會建立與來源索引具有相同定義的目標索引，包括對應與設定。
2. 系統會建立從來源索引區段到目標索引的硬連結。如果檔案系統不支援硬連結，OpenSearch 會將所有區段複製到目標索引，這需要更多時間與磁碟空間。
3. OpenSearch 會復原目標索引，如同復原已關閉後重新開啟的索引，使其可供使用。

## 先決條件

在複製索引之前，您必須將來源索引標記為唯讀，並確保叢集狀態良好，以完成準備：

- 來源索引必須將 `index.blocks.write` 設定設為 `true`，以防止在複製過程中進行寫入作業。仍允許變更中繼資料，例如刪除索引。
- 叢集健康狀態必須為 `green`，以確保所有主要分片與副本分片皆可用。

下列範例請求會將 `products` 索引設為唯讀模式，以便複製：

<!-- spec_insert_start
component: example_code
rest: PUT /products/_settings
body: |
{
  "settings": {
    "index.blocks.write": true
  }
}
-->
{% capture step1_rest %}
PUT /products/_settings
{
  "settings": {
    "index.blocks.write": true
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.put_settings(
  index = "products",
  body =   {
    "settings": {
      "index.blocks.write": true
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->



<!-- spec_insert_start
api: indices.clone
component: endpoints
-->
## 端點
```json
POST /{index}/_clone/{target}
PUT  /{index}/_clone/{target}
```
<!-- spec_insert_end -->

## 需求

索引必須符合下列需求才能複製：

- 目標索引必須尚未存在。
- 來源索引的主要分片數必須與目標索引相同。
- 來源索引必須透過將 `index.blocks.write` 設為 `true`，標記為唯讀。
- 叢集健康狀態必須為 `green`。
- 如果檔案系統不支援硬連結，處理複製程序的節點必須有足夠的可用磁碟空間，以容納索引的第二份副本。

## 索引命名限制

OpenSearch 索引有下列命名限制：

- 所有字母都必須為小寫。
- 索引名稱不能以底線（`_`）或連字號（`-`）開頭。
- 索引名稱不能包含空格、逗號或下列字元：

  `:`、`"`、`*`、`+`、`/`、`\`、`|`、`?`、`#`、`>` 或 `<`

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `index` | **必要** | 字串 | 要複製的來源索引名稱。 |
| `target` | **必要** | 字串 | 要建立的目標索引名稱。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `cluster_manager_timeout` | 字串 | 等待連線至叢集管理員節點的時間。 | `30s` |
| `task_execution_timeout` | 字串 | 等待工作完成的時間。僅在 `wait_for_completion` 設為 `false` 時適用。 | `1h` |
| `timeout` | 字串 | 等待回應的時間。如果在逾時期限前未收到回應，請求會失敗並傳回錯誤。 | `30s` |
| `wait_for_active_shards` | 字串 | 作業繼續進行所需的作用中分片副本數。指定 `all`，或不超過索引分片總數（`number_of_replicas+1`）的任意正整數。 | `1`（僅主要分片） |
| `wait_for_completion` | 布林值 | 指定是否在傳回回應之前等待作業完成。 | `true` |

## 請求本文欄位

複製索引 API 會建立新的目標索引，因此您可以在請求本文中指定要套用至目標索引的索引設定與別名。請求本文為選用。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`settings` | 物件 | 目標索引的組態選項。如需索引設定清單，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。選用。
`settings.index.number_of_shards` | 整數 | 目標索引中的主要分片數。此值必須等於來源索引中的主要分片數。選用。預設與來源索引相同。
`settings.index.number_of_replicas` | 整數 | 目標索引中每個主要分片的副本分片數。選用。預設與來源索引相同。
`aliases` | 物件 | 要套用至目標索引的索引別名。每個鍵都是別名名稱，而值則是別名組態物件。如需詳細資訊，請參閱[索引別名]({{site.url}}{{site.baseurl}}/im-plugin/index-alias/)。選用。

**注意**：您無法在複製請求中指定對應。來源索引的對應會自動用於目標索引。
{: .note}

## 範例：複製索引

下列範例請求會將 `products` 索引複製到名為 `products-clone` 的新索引：

<!-- spec_insert_start
component: example_code
rest: POST /products/_clone/products-clone
body: {}
-->
{% capture step1_rest %}
POST /products/_clone/products-clone
{}
{% endcapture %}

{% capture step1_python %}


response = client.indices.clone(
  index = "products",
  target = "products-clone",
  body =   {}
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：使用設定與別名複製索引

下列範例請求會將 `products` 索引複製到名為 `products-clone-configured` 的新索引，並使用自訂設定與別名：

<!-- spec_insert_start
component: example_code
rest: POST /products/_clone/products-clone-configured
body: |
{
  "settings": {
    "index": {
      "number_of_shards": 2,
      "number_of_replicas": 1
    }
  },
  "aliases": {
    "products-search": {}
  }
}
-->
{% capture step1_rest %}
POST /products/_clone/products-clone-configured
{
  "settings": {
    "index": {
      "number_of_shards": 2,
      "number_of_replicas": 1
    }
  },
  "aliases": {
    "products-search": {}
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.clone(
  index = "products",
  target = "products-clone-configured",
  body =   {
    "settings": {
      "index": {
        "number_of_shards": 2,
        "number_of_replicas": 1
      }
    },
    "aliases": {
      "products-search": {}
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

複製請求成功時，OpenSearch 會傳回下列回應。`index` 欄位包含已建立的目標索引名稱：

```json
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "products-clone"
}
```

目標索引加入叢集狀態後，便會立即傳回回應。它不會等待複製作業完成。

## 回應本文欄位

下表列出所有回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`acknowledged` | 布林值 | 表示叢集是否已收到複製請求。值為 `true` 表示已收到請求。
`shards_acknowledged` | 布林值 | 表示 `wait_for_active_shards` 設定所指定數量的分片副本是否在作業逾時之前進入作用中狀態。值為 `true` 表示目標數量的分片副本已進入作用中狀態。值為 `false` 表示作業在目標數量的分片副本進入作用中狀態之前已逾時。
`index` | 字串 | 新建立的目標索引名稱。

## 監控複製程序

複製 API 會在將目標索引加入叢集狀態後立即傳回，此時尚未配置任何分片。此時，所有分片都處於 `unassigned` 狀態。如果目標索引因任何原因而無法配置，其主要分片會維持 `unassigned` 狀態，直到可以將它們配置到節點上。

主要分片配置完成後，會轉為 `initializing` 狀態，並開始複製作業。複製作業完成後，分片會變成 `active`。接著，OpenSearch 會嘗試配置所有副本，並可能將主要分片重新配置到另一個節點。

您可以使用下列其中一種方法監控複製程序：

- 若要檢視分片復原與複製的進度，請使用 [CAT recovery API]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-recovery/)。
- 若要等待所有主要分片完成配置，請使用 [Cluster health API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-health/)，並將 `wait_for_status` 參數設為 `yellow`。

下列範例請求會監控複製索引的復原程序：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/recovery/products-clone?v
-->
{% capture step1_rest %}
GET /_cat/recovery/products-clone?v
{% endcapture %}

{% capture step1_python %}


response = client.cat.recovery(
  index = "products-clone",
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 等待作用中分片

由於複製作業會建立新索引，因此用於索引建立的 `wait_for_active_shards` 設定也適用於複製作業。此設定決定作業傳回回應之前，必須有多少個分片副本處於作用中狀態。如需詳細資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`indices:admin/resize`。
