---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引層級搜尋剪除"
parent: Improving search performance
nav_order: 35
has_children: false
---

# 索引層級搜尋剪除
**於 3.9 版推出**
{: .label .label-purple }

索引層級搜尋剪除可讓 OpenSearch 在將請求傳送至分片之前，先排除整個索引。

假設有一個時間序列工作負載，其中 `logs-*` 會擴展為 90 個每日索引，而某個儀表板查詢最近 5 分鐘的資料。OpenSearch 一開始會考量全部 90 個索引的分片。`can_match` 階段會篩除無法包含相符文件的分片，但它是藉由將請求傳送至每個分片來判斷，因此即使這 90 個索引中只有一個能包含相符文件，搜尋仍需要對每個分片進行一次來回傳輸。

索引層級搜尋剪除會在協調節點上進行這項判斷。如果某個索引針對所查詢的欄位有已記錄的範圍 (例如 `logs-2026-06-01` 只包含 6 月 1 日的時間戳記)，OpenSearch 就會將該索引從最近 5 分鐘的查詢中排除，而不會將請求傳送至其任何分片。

剪除取決於已記錄的範圍，稱為 _欄位定義域_（field domain）。欄位定義域包含索引中某個 `date` 或 `date_nanos` 欄位的最小值和最大值，因此它一律是時間範圍。對於每日索引中的 `@timestamp`，欄位定義域就是該索引中最早與最晚的時間戳記。OpenSearch 會將每個欄位定義域儲存在叢集狀態中，而協調節點已將其保留在記憶體中，因此可以在本機比較範圍。

由於欄位定義域是索引值的快照，因此只有在索引維持寫入封鎖時才有效。如果索引仍接受寫入，新文件可能會落在欄位定義域之外，剪除就會略過包含相符文件的索引，而無聲地從搜尋結果中捨棄資料。這使得剪除特別適用於時間序列資料，因為較舊的索引在輪替後通常會處於寫入封鎖狀態。

_分片群組_（shard group）是指一次搜尋可做為目標的單一分片副本集合，包括主要分片及其副本。一次搜尋會從每個群組中的一個副本讀取。例如，一個具有 5 個主要分片且每個分片有 1 個副本的索引，會有 10 個分片副本，但只有 5 個分片群組。剪除會略過欄位定義域完全落在查詢範圍之外之索引的分片群組。當索引沒有欄位定義域，或其欄位定義域無法使用時，OpenSearch 會搜尋該分片群組。


## 設定搜尋剪除

若要使用剪除，請先啟用叢集設定。接著為您想要剪除的索引發佈欄位定義域。

### 啟用搜尋剪除

索引層級搜尋剪除預設為停用。若要啟用，請使用 Cluster Settings API 設定剪除設定：

```json
PUT _cluster/settings
{
  "persistent": {
    "search.index_pruning.enabled": true,
    "search.index_pruning.min_shards": 32,
    "search.index_pruning.fields": ["@timestamp"]
  }
}
```
{% include copy-curl.html %}

如需剪除設定的詳細資訊，請參閱[搜尋設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/search-settings/#index-pruning-settings)。

### 發佈欄位定義域

您想要 OpenSearch 剪除的每個索引，都必須為您查詢所篩選的欄位具有欄位定義域，而且該欄位必須列在 `search.index_pruning.fields` 中。若要發佈欄位定義域，請在 `read_only` 動作之後，將 Index State Management (ISM) [`publish_field_domains`]({{site.url}}{{site.baseurl}}/im-plugin/ism/policies-operations/#publish-field-domains) 動作新增至原則狀態。ISM 接著會計算該索引中該欄位的最小值和最大值並加以儲存。

請只為維持寫入封鎖的索引發佈欄位定義域。
{: .important}

## 限制

剪除不適用於使用 Point in Time (PIT) 的搜尋，也不適用於遠端叢集上的分片群組。因此，剪除不會減少跨叢集搜尋中所搜尋的遠端分片群組數量。

如果剪除會排除每個分片群組，OpenSearch 會改為搜尋所有分片群組。

## 查詢限制

剪除適用於所設定欄位上 `must` 和 `filter` 子句中的 `range` 查詢。選用和否定子句 (例如 `should` 和 `must_not`) 不會觸發剪除，因為相符文件不需要滿足這些子句。

當 `@timestamp` 設定於 `search.index_pruning.fields` 中時，下列查詢符合剪除的資格。OpenSearch 會解析日期數學運算式 (例如 `now-2m`) 一次 (在請求開始時間)，並針對其評估的每個索引使用該值：

```json
GET logs-*/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "range": {
            "@timestamp": {
              "gte": "now-2m",
              "lte": "now"
            }
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}
