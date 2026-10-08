---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "縮減索引"
parent: Index operations
grand_parent: Index APIs
nav_order: 100
redirect_from:
  - /opensearch/rest-api/index-apis/shrink-index/
---

# Shrink Index API
**1.0 版引入**
{: .label .label-purple }

Shrink Index API 會建立一個分片數較少的新目標索引，藉此減少現有索引中的主要分片數量。當索引最初的分片數過多，而您想要合併分片以回收資源或提升搜尋效能時，這項 API 就很實用。

目標索引的主要分片數必須是來源索引主要分片數的因數。例如，具有 8 個主要分片的索引可以縮減為 4 個、2 個或 1 個主要分片。分片數為質數（例如 7）的索引只能縮減為 1 個主要分片。

## 先決條件

在縮減索引之前，索引必須符合下列條件：

- 索引必須為唯讀。若要將索引設為唯讀，請將[動態索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#dynamic-index-settings) `index.blocks.write` 設為 `true`。
- 索引中每個分片（主要分片或副本分片皆可）都必須有一份複本位於同一個節點上。您可以使用[分片配置篩選]({{site.url}}{{site.baseurl}}/api-reference/index-apis/shard-allocation/)將分片移至同一個節點。
- 叢集健康狀態必須為綠色。

此外，縮減作業會強制執行下列限制：

- 目標索引必須尚未存在。
- 來源索引的主要分片數必須多於目標索引。
- 目標索引的主要分片數必須是來源索引主要分片數的因數。
- 在所有將合併至單一目標分片的分片中，來源索引的文件總數不得超過 2,147,483,519 個，因為這是單一 Lucene 分片可容納的文件數上限。
- 處理縮減程序的節點必須有足夠的可用磁碟空間，以容納現有索引的第二份複本。

下列請求會將所有分片路由至單一節點並封鎖寫入作業，藉此滿足前三項條件：

```json
PUT /catalog-archive/_settings
{
  "settings": {
    "index.routing.allocation.require._name": "opensearch-node1",
    "index.blocks.write": true
  }
}
```
{% include copy-curl.html %}

分片重新配置可能需要一些時間，視索引大小而定。您可以使用 [CAT recovery API]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-recovery/) 追蹤進度，或使用 [Cluster Health API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-health/) 搭配 `wait_for_no_relocating_shards` 參數等待作業完成。
{: .note}

縮減請求中無法指定對應。目標索引會繼承來源索引的所有對應。
{: .important}

縮減作業會執行下列三個步驟：

1. 建立新的目標索引，其定義與來源索引相同，但主要分片數較少。
1. 從來源索引區段建立指向目標索引的硬連結。若檔案系統不支援硬連結，則會將區段實際複製到新索引中，這個過程會耗費更多時間。
1. 使用與重新開啟已關閉索引時相同的程序來復原目標索引。

建立目標索引時，請記得 OpenSearch 索引名稱有下列限制：

- 所有字母都必須為小寫。
- 索引名稱不能以底線（`_`）或連字號（`-`）開頭。
- 索引名稱不能包含空格、逗號或下列字元：

  `:`、`"`、`*`、`+`、`/`、`\`、`|`、`?`、`#`、`>` 或 `<`

<!-- spec_insert_start
api: indices.shrink
component: endpoints
-->
## 端點
```json
POST /{index}/_shrink/{target}
PUT  /{index}/_shrink/{target}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `index` | **必要** | 字串 | 要縮減的來源索引名稱。 |
| `target` | **必要** | 字串 | 要建立的目標索引名稱。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設值 |
| :--- | :--- | :--- | :--- |
| `wait_for_active_shards` | 字串 | 在 OpenSearch 傳回回應之前，必須可用的作用中分片複本數量。由於縮減作業會建立新索引，因此建立索引時的[等待作用中分片]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/#wait-for-active-shards)設定在此同樣適用。可設為 `all` 或正整數。大於 1 的值需要副本。例如，若您指定的值為 3，索引必須有兩個副本分散在另外兩個節點上，請求才會成功。 | `1` |
| `cluster_manager_timeout` | 字串 | 等待連線至叢集管理員節點的時間長度。 | `30s` |
| `timeout` | 字串 | 等待回應的時間長度。若在逾時之前未收到回應，請求就會失敗並傳回錯誤。 | `30s` |
| `wait_for_completion` | 布林值 | 設為 `false` 時，請求會立即傳回，而不是在作業完成後才傳回。若要監視作業狀態，請使用 [Tasks API]({{site.url}}{{site.baseurl}}/api-reference/tasks/) 搭配請求所傳回的任務 ID。 | `true` |
| `task_execution_timeout` | 字串 | 等待任務完成的時間長度。僅在 `wait_for_completion` 設為 `false` 時適用。 | `1h` |

## 請求本文欄位

下表列出可用的請求本文欄位。所有欄位皆為選用。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `settings` | 物件 | 要套用至目標索引的索引設定。請參閱[索引設定]({{site.url}}{{site.baseurl}}/im-plugin/index-settings/)。 |
| `aliases` | 物件 | 要與目標索引建立關聯的別名。請參閱 [Alias API]({{site.url}}{{site.baseurl}}/api-reference/alias/)。 |
| `max_shard_size` | 字串 | 目標索引中主要分片的大小上限。OpenSearch 會根據總儲存空間與此限制計算最佳分片數。不能與 `index.number_of_shards` 同時使用。請參閱 [`max_shard_size` 參數](#the-max_shard_size-parameter)。 |

### `max_shard_size` 參數

`max_shard_size` 參數指定目標索引中主要分片的大小上限。OpenSearch 會使用 `max_shard_size` 與來源索引中所有主要分片的總儲存空間，計算目標索引的主要分片數量及其大小。

目標索引的主要分片數，是來源索引主要分片數的因數中，能使分片大小不超過 `max_shard_size` 的最小因數。例如，若來源索引有 8 個主要分片，總共占用 400 GB 的儲存空間，且 `max_shard_size` 為 150 GB，OpenSearch 會依照下列步驟計算主要分片數量：

1. 以 400/150 計算主要分片數的最小值，並四捨五入至最接近的整數。主要分片數的最小值為 3。
1. 找出 8 的因數中大於或等於 3 的最小值。主要分片數為 4。

目標索引的主要分片數上限等於來源索引的主要分片數。例如，若來源索引有 5 個主要分片，占用 600 GB，且 `max_shard_size` 為 100 GB，則最小值為 600/100 = 6。由於 6 超過來源分片數 5，目標索引會保留 5 個主要分片。

目標索引的主要分片數最小值為 1。
{: .note}

## 監視縮減程序

Shrink Index API 會在目標索引加入叢集狀態後立即傳回，不會等待縮減作業完成。縮減程序會依序經過下列分片狀態：

1. **Unassigned**：API 傳回後，目標索引中的所有分片會立即處於此狀態。
1. **Initializing**：主要分片配置到執行縮減的節點後，會轉換為此狀態，並開始整併資料。
1. **Active**：縮減完成後，分片會變為作用中。接著，OpenSearch 會嘗試配置所有已設定的副本，並可能將主要分片重新配置到其他節點以達成平衡。

您可以使用 [CAT recovery API]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-recovery/) 追蹤分片復原的進度，或搭配 `wait_for_status=yellow` 使用 [Cluster Health API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-health/)，等待所有主要分片完成配置。

## 索引編解碼器注意事項

如需索引編解碼器的注意事項，請參閱[索引編解碼器]({{site.url}}{{site.baseurl}}/im-plugin/index-codecs/#splits-and-shrinks)。

## 範例：縮減索引

下列範例將 `catalog-archive` 索引從 4 個主要分片縮減為 2 個，清除從來源複製的配置需求和寫入封鎖，並附加別名：

<!-- spec_insert_start
component: example_code
rest: POST /catalog-archive/_shrink/catalog-archive-shrunk
body: |
{
  "settings": {
    "index.number_of_shards": 2,
    "index.number_of_replicas": 0,
    "index.routing.allocation.require._name": null,
    "index.blocks.write": null
  },
  "aliases": {
    "catalog-current": {}
  }
}
-->
{% capture step1_rest %}
POST /catalog-archive/_shrink/catalog-archive-shrunk
{
  "settings": {
    "index.number_of_shards": 2,
    "index.number_of_replicas": 0,
    "index.routing.allocation.require._name": null,
    "index.blocks.write": null
  },
  "aliases": {
    "catalog-current": {}
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.shrink(
  index = "catalog-archive",
  target = "catalog-archive-shrunk",
  body =   {
    "settings": {
      "index.number_of_shards": 2,
      "index.number_of_replicas": 0,
      "index.routing.allocation.require._name": null,
      "index.blocks.write": null
    },
    "aliases": {
      "catalog-current": {}
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：使用 `max_shard_size` 縮減索引

您可以不指定確切的分片數量，而是讓 OpenSearch 根據最大分片大小決定最佳的分片數量。下列範例縮減 `catalog-source` 索引，使每個主要分片都不超過 100 MB：

<!-- spec_insert_start
component: example_code
rest: POST /catalog-source/_shrink/catalog-source-compact
body: |
{
  "max_shard_size": "100mb",
  "settings": {
    "index.number_of_replicas": 0,
    "index.routing.allocation.require._name": null,
    "index.blocks.write": null
  }
}
-->
{% capture step1_rest %}
POST /catalog-source/_shrink/catalog-source-compact
{
  "max_shard_size": "100mb",
  "settings": {
    "index.number_of_replicas": 0,
    "index.routing.allocation.require._name": null,
    "index.blocks.write": null
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.shrink(
  index = "catalog-source",
  target = "catalog-source-compact",
  body =   {
    "max_shard_size": "100mb",
    "settings": {
      "index.number_of_replicas": 0,
      "index.routing.allocation.require._name": null,
      "index.blocks.write": null
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

```json
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "catalog-archive-shrunk"
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `acknowledged` | 布林值 | 表示請求是否已獲得叢集中所有相關節點的確認。 |
| `shards_acknowledged` | 布林值 | 表示在請求逾時之前，是否已啟動所需數量的分片複本。 |
| `index` | 字串 | 所建立之目標索引的名稱。 |

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`indices:admin/resize`。
