---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分割索引"
parent: Index operations
grand_parent: Index APIs
nav_order: 110
redirect_from:
  - /opensearch/rest-api/index-apis/split/
---

# 分割索引 API
**於 1.0 版推出**
{: .label .label-purple }

分割索引 API 會建立新的目標索引，將每個原始主要分片分割成兩個或多個主要分片，藉此增加現有索引中的主要分片數量。當索引的成長已超出其原始分片數量，且需要額外容量來處理增加的資料量或查詢負載時，這項功能便十分實用。

目標索引中的主要分片數量必須是來源索引主要分片數量的倍數。舉例來說，具有 2 個主要分片的索引可以分割成 4、6、8 或任何其他 2 的倍數。具有單一主要分片的索引則可以分割成任意數量的分片。

索引支援的分割次數上限取決於 `index.number_of_routing_shards` 設定。此設定會定義使用一致性雜湊來分散文件的總雜湊空間。由於一致性雜湊要求每個新分片都必須對應到原始雜湊空間中完整且連續的子集，因此僅支援倍數因子；增量重新分片 (N 到 N+1) 需要重新平衡所有分片中的文件，對於搜尋導向的資料結構而言成本過高。舉例來說，具有 2 個分片且 `number_of_routing_shards` 設為 12 (2 x 2 x 3) 的索引支援下列分割路徑：

- `2` -> `4` -> `12` (先以 2 倍分割，再以 3 倍分割)
- `2` -> `6` -> `12` (先以 3 倍分割，再以 2 倍分割)
- `2` -> `12` (以 6 倍分割)

若未明確設定，`number_of_routing_shards` 會預設為允許重複加倍、最多達 1,024 個分片的值。

## 先決條件

您必須先讓索引符合下列條件，才能分割索引：

- 索引必須為唯讀。若要將索引設為唯讀，請將[動態索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#dynamic-index-settings) `index.blocks.write` 設為 `true`。
- 叢集健康狀態必須為綠色。

此外，分割作業會強制執行下列限制：

- 目標索引不得已存在。
- 來源索引的主要分片數量必須少於目標索引。
- 目標索引中的主要分片數量必須是來源索引主要分片數量的倍數。
- 處理分割程序的節點必須有足夠的可用磁碟空間，以容納現有索引的第二份複本。

下列請求會將 `catalog-logs` 索引設為唯讀，以準備進行分割：

```json
PUT /catalog-logs/_settings
{
  "settings": {
    "index.blocks.write": true
  }
}
```
{% include copy-curl.html %}

分割請求中無法指定對應。目標索引會繼承來源索引的所有對應。
{: .important}

分割作業會執行下列步驟：

1. 配置具有相同對應與組態但主要分片數量更多的新目標索引。
1. 從來源區段建立指向目標索引目錄的硬式連結。如果檔案系統不支援硬式連結，則會改為執行完整的位元組層級複製，這會耗費明顯更長的時間。
1. 執行重新雜湊階段，根據新的路由配置將每份文件重新指派至正確的目標分片，並移除不再屬於該分片的文件。
1. 在目標索引上啟動分片復原，類似於重新開啟已關閉索引時所執行的程序。

## 監控分割程序

分割 API 在目標索引新增至叢集狀態後便會立即傳回，不會等待分割作業完成。分割程序會依序經歷下列分片狀態：

1. **未指派** -- 目標索引中的所有分片在 API 傳回後會立即從此狀態開始。
1. **初始化中** -- 主要分片配置至節點後，便會轉換為此狀態並開始重新分散資料。
1. **作用中** -- 分割完成時，分片會變成作用中。OpenSearch 接著會嘗試配置任何已設定的副本，並可能將主要分片重新配置至其他節點以進行平衡。

您可以使用 [CAT recovery API]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-recovery/) 追蹤分片復原的進度，或搭配 `wait_for_status=yellow` 使用 [Cluster Health API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-health/)，等待所有主要分片完成配置。

建立目標索引時，請記得 OpenSearch 索引名稱有下列限制：

- 所有字母必須為小寫。
- 索引名稱不能以底線 (`_`) 或連字號 (`-`) 開頭。
- 索引名稱不能包含空格、逗號或下列字元：

  `:`, `"`, `*`, `+`, `/`, `\`, `|`, `?`, `#`, `>`, 或 `<`

<!-- spec_insert_start
api: indices.split
component: endpoints
-->
## 端點
```json
POST /{index}/_split/{target}
PUT  /{index}/_split/{target}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `index` | **必要** | 字串 | 要分割的來源索引名稱。 |
| `target` | **必要** | 字串 | 要建立的目標索引名稱。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數均為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `wait_for_active_shards` | 字串 | OpenSearch 傳回回應之前必須可用的作用中分片複本數量。由於分割作業會建立新索引，因此建立索引時的[等待作用中分片]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/#wait-for-active-shards)設定也會在此適用。請設為 `all` 或正整數。大於 1 的值需要副本。舉例來說，如果您指定值 3，索引就必須有兩個副本分散於另外兩個節點，請求才會成功。 | `1` |
| `cluster_manager_timeout` | 字串 | 等待連線至叢集管理員節點的時間長度。 | `30s` |
| `timeout` | 字串 | 等待回應的時間長度。若在逾時前未收到回應，請求會失敗並傳回錯誤。 | `30s` |
| `wait_for_completion` | 布林值 | 設為 `false` 時，請求會立即傳回，而非等到作業完成後才傳回。若要監控作業狀態，請搭配請求傳回的工作 ID 使用 [Tasks API]({{site.url}}{{site.baseurl}}/api-reference/tasks/)。 | `true` |
| `task_execution_timeout` | 字串 | 等待工作完成的時間長度。僅適用於 `wait_for_completion` 設為 `false` 時。 | `1h` |

## 請求本文欄位

下表列出可用的請求本文欄位。所有欄位均為選用。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `settings` | 物件 | 要套用至目標索引的索引設定。請參閱[索引設定]({{site.url}}{{site.baseurl}}/im-plugin/index-settings/)。 |
| `aliases` | 物件 | 要與目標索引建立關聯的別名。請參閱[別名 API]({{site.url}}{{site.baseurl}}/api-reference/alias/)。 |

## 索引轉碼器考量

如需索引轉碼器考量，請參閱[索引轉碼器]({{site.url}}{{site.baseurl}}/im-plugin/index-codecs/#splits-and-shrinks)。

## 範例：分割索引

下列範例會將 `catalog-logs` 索引從 2 個主要分片分割成 4 個、解除寫入封鎖，並附加別名：

<!-- spec_insert_start
component: example_code
rest: POST /catalog-logs/_split/catalog-logs-split
body: |
{
  "settings": {
    "index.number_of_shards": 4,
    "index.number_of_replicas": 0,
    "index.blocks.write": null
  },
  "aliases": {
    "catalog-logs-current": {}
  }
}
-->
{% capture step1_rest %}
POST /catalog-logs/_split/catalog-logs-split
{
  "settings": {
    "index.number_of_shards": 4,
    "index.number_of_replicas": 0,
    "index.blocks.write": null
  },
  "aliases": {
    "catalog-logs-current": {}
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.split(
  index = "catalog-logs",
  target = "catalog-logs-split",
  body =   {
    "settings": {
      "index.number_of_shards": 4,
      "index.number_of_replicas": 0,
      "index.blocks.write": null
    },
    "aliases": {
      "catalog-logs-current": {}
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：分割單一分片索引

具有單一主要分片的索引可以分割成任意數量的分片。下列範例會將 `catalog-events` 索引從 1 個分片分割成 3 個：

<!-- spec_insert_start
component: example_code
rest: POST /catalog-events/_split/catalog-events-expanded
body: |
{
  "settings": {
    "index.number_of_shards": 3,
    "index.number_of_replicas": 0,
    "index.blocks.write": null
  }
}
-->
{% capture step1_rest %}
POST /catalog-events/_split/catalog-events-expanded
{
  "settings": {
    "index.number_of_shards": 3,
    "index.number_of_replicas": 0,
    "index.blocks.write": null
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.split(
  index = "catalog-events",
  target = "catalog-events-expanded",
  body =   {
    "settings": {
      "index.number_of_shards": 3,
      "index.number_of_replicas": 0,
      "index.blocks.write": null
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

```json
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "catalog-logs-split"
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `acknowledged` | 布林值 | 指出請求是否已由叢集中所有相關節點確認。 |
| `shards_acknowledged` | 布林值 | 指出在請求逾時前，是否已啟動所需數量的分片複本。 |
| `index` | 字串 | 已建立的目標索引名稱。 |

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`indices:admin/resize`。
