---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Significant terms
parent: Bucket aggregations
nav_order: 180
redirect_from:
  - /query-dsl/aggregations/bucket/significant-terms/
---

# Significant terms 彙總

`significant_terms` 彙總用於識別在文件子集（前景集）中出現頻率異常高，且與較廣泛的參考集（背景集）相比具有顯著差異的詞元。預設情況下，背景集針對目標索引中的所有文件。您可以使用 `background_filter` 來縮小範圍。使用此彙總來檢索 *最過度代表* 的值，對於這種需求，僅顯示 *最常見* 值的普通 `terms` 彙總是不夠的。

每個結果桶包含：

- `key`：詞元值。
- `doc_count`：包含該詞元的前景文件數量。
- `bg_count`：包含該詞元的背景文件數量。
- `score`：指定該詞元在前景中相對於背景的突出程度。如需更多資訊，請參閱 [啟發式演算法與評分](#heuristics-and-scoring)。

如果彙總沒有回傳任何桶，通常表示前景未經過篩選（例如，您使用了 `match_all` 查詢），或者前景中的詞元分佈與背景相同。
{: .note}

## 基本範例：識別電子商務應用程式中高價值退貨的特徵詞元

建立一個包含客戶訂單的索引：

```json
PUT /retail_orders
{
  "mappings": {
    "properties": {
      "status":         { "type": "keyword" },
      "order_total":    { "type": "double" },
      "payment_method": { "type": "keyword" }
    }
  }
}
```
{% include copy-curl.html %}

將範例文件匯入索引：

```json
POST _bulk
{ "index": { "_index": "retail_orders" } }
{ "status":"RETURNED", "order_total": 950, "payment_method":"gift_card" }
{ "index": { "_index": "retail_orders" } }
{ "status":"RETURNED", "order_total": 720, "payment_method":"gift_card" }
{ "index": { "_index": "retail_orders" } }
{ "status":"RETURNED", "order_total": 540, "payment_method":"gift_card" }
{ "index": { "_index": "retail_orders" } }
{ "status":"RETURNED", "order_total": 820, "payment_method":"credit_card" }
{ "index": { "_index": "retail_orders" } }
{ "status":"RETURNED", "order_total": 500, "payment_method":"paypal" }
{ "index": { "_index": "retail_orders" } }
{ "status":"DELIVERED", "order_total": 130, "payment_method":"credit_card" }
{ "index": { "_index": "retail_orders" } }
{ "status":"DELIVERED", "order_total": 75,  "payment_method":"paypal" }
{ "index": { "_index": "retail_orders" } }
{ "status":"DELIVERED", "order_total": 260, "payment_method":"paypal" }
{ "index": { "_index": "retail_orders" } }
{ "status":"DELIVERED", "order_total": 45,  "payment_method":"credit_card" }
{ "index": { "_index": "retail_orders" } }
{ "status":"DELIVERED", "order_total": 310, "payment_method":"credit_card" }
{ "index": { "_index": "retail_orders" } }
{ "status":"DELIVERED", "order_total": 220, "payment_method":"credit_card" }
{ "index": { "_index": "retail_orders" } }
{ "status":"DELIVERED", "order_total": 410, "payment_method":"paypal" }
```
{% include copy-curl.html %}

執行以下查詢，以識別與整個索引相比，在退貨且金額超過 500 美元的訂單中異常常見的 `payment_method` 值：

```json
GET /retail_orders/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        { "term":  { "status": "RETURNED" } },
        { "range": { "order_total": { "gte": 500 } } }
      ]
    }
  },
  "aggs": {
    "payment_signals": {
      "significant_terms": {
        "field": "payment_method"
      }
    }
  }
}
```
{% include copy-curl.html %}

回傳的彙總顯示，在五筆高價值退貨中，`gift_card` 出現了 3 次 (60%)，而整個索引中 12 次僅出現 3 次 (25%)。因此，它被標記為最過度代表的付款方式：

```json
{
  ...
  "hits": {
    "total": {
      "value": 5,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "payment_signals": {
      "doc_count": 5,
      "bg_count": 12,
      "buckets": [
        {
          "key": "gift_card",
          "doc_count": 3,
          "score": 0.84,
          "bg_count": 3
        }
      ]
    }
  }
}
```

## 多集分析

您可以先將文件分組到桶中，然後在每個桶內執行 `significant_terms` 彙總，以此確定每個類別的異常值。

### 範例：每個區域的異常 `cancel_reason`

以下範例使用 terms 彙總按區域分組，並在每個桶內執行 `significant_terms`，以識別在該區域中不成比例地常見的取消原因：

```json
GET /rides/_search
{
  "size": 0,
  "aggs": {
    "by_region": {
      "terms": { "field": "region.keyword", "size": 5 },
      "aggs": {
        "odd_cancellations": {
          "significant_terms": { "field": "cancel_reason.keyword" }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 範例：地圖上的熱點

假設您有一組全國各個站點的現場事故資料集。每份文件包含一個 `geo_point` 類型的點位置 `site.location` 和一個類別欄位 `issue.keyword`（例如 `POWER_OUTAGE`、`FIBER_CUT` 或 `VANDALISM`）。您想要識別與較廣泛的參考集相比，在特定地圖圖塊中過度代表的問題類型。您可以使用 `geotile_grid` 將地圖劃分為縮放層級圖塊。較高的 `precision` 會產生較小的圖塊（例如街道或城市街區），而較低的 `precision` 則會產生較大的圖塊（例如城市或區域）。在每個圖塊內執行 `significant_terms` 彙總以識別局部離群值。

按地圖圖塊對資料進行分段，並識別在這些圖塊中異常頻繁的 `issue.keyword` 值：

```json
GET field_ops/_search
{
  "size": 0,
  "aggs": {
    "tiles": {
      "geotile_grid": { "field": "site.location", "precision": 6 },
      "aggs": {
        "odd_issues": {
          "significant_terms": { "field": "issue.keyword" }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 使用 `background_filter` 縮小背景集

預設情況下，背景包含整個索引。使用 `background_filter` 限制背景文件以獲得更精確的結果。

### 範例：將多倫多與加拿大其他地區進行比較

以下範例將前景篩選為「Toronto」，並為「Canada」設定 `background_filter`。`significant_terms` 會突出顯示相對於其他加拿大城市在多倫多異常頻繁的主題：

```json
GET /news/_search
{
  "size": 0,
  "query": { "term": { "city.keyword": "Toronto" } },
  "aggs": {
    "unusual_topics": {
      "significant_terms": {
        "field": "topic.keyword",
        "background_filter": {
          "term": { "country.keyword": "Canada" }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用自訂背景需要額外的處理，因為必須透過套用篩選器來計算每個候選詞元的背景頻率。這可能比使用預設的索引範圍計數速度較慢。
{: .warning}

## 欄位類型考量

`significant_terms` 彙總在精確值欄位（例如 `keyword` 或 `numeric`）上效果最好。在經過大量斷詞的文字上執行 `significant_terms` 彙總可能會消耗大量記憶體。對於經過分析的文字，請考慮使用 [`significant_text` 彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/significant-text/)，這些彙總專為全文欄位設計，並支援相同的顯著性啟發式演算法。

## 啟發式演算法與評分

`score` 根據前景頻率與背景頻率的差異程度對詞元進行排名。它沒有單位，僅在同一請求和啟發式演算法內進行比較時才有意義。

您可以在每個請求中透過在 `significant_terms` 下指定來選擇一種啟發式演算法。支援以下啟發式演算法：

### JLH

Jensen–Shannon Lift Heuristic (JLH) 適用於大多數通用場景。它平衡了詞元的絕對頻率及其相對於背景集的相對過度代表程度，傾向於在 *絕對* 和 *相對* 方面都增加的詞元。

```json
"significant_terms": {
  "field": "payment_method.keyword",
  "jlh": {}
}
```

#### JLH 評分

JLH 分數的計算方式如下：

`fg_pct = doc_count / foreground_total` 和 `bg_pct = bg_count / background_total`。JLH ≈ `(fg_pct − bg_pct) * (fg_pct / bg_pct)`。 

頻率從較大基準線略微增加的詞元，其得分將高於從極小背景份額中具有相同絕對增量的詞元。

#### 使用 JLH 的評分範例計算

假設您的前景集（高價值退貨）包含 `2,000` 筆訂單，而背景集（所有訂單）包含 `120,000` 筆訂單。考慮 `significant_terms` 彙總中的單個詞元，其計數如下：

- `doc_count = 160`
- `bg_count = 3,200`

包含該詞元的文件百分比計算方式如下：

- `fg_pct = 160 / 2000 = 0.08`
- `bg_pct = 3200 / 120000 ≈ 0.026666…`

JLH ≈ `(0.08 − 0.026666…) * (0.08 / 0.026666…) ≈ 0.053333… * 3 ≈ 0.16`

這個正分表示搜尋的詞元在高價值退貨中比在整體中更為普遍。分數是相對的：請將其用於對詞元進行排名，而非作為絕對機率。

### 互資訊

互資訊 (Mutual information, MI) 傾向於頻繁出現的詞元，並識別流行但仍具特徵的詞元。設定 `include_negatives: false` 以忽略在前景中比背景中更不常見的詞元。如果您的背景不是前景的超集，請設定 `background_is_superset: false`：

```json
"significant_terms": {
  "field": "product.keyword",
  "mutual_information": {
    "include_negatives": false,
    "background_is_superset": true
  }
}
```

### 卡方檢定

卡方檢定 (Chi-square) 是一種統計檢定，用於衡量子集（前景）中詞元的觀察頻率與基於參考集（背景）的預期頻率之間的偏差程度。與 [MI](#mutual-information) 類似，卡方檢定支援 `include_negatives` 和 `background_is_superset`：

```json
"significant_terms": {
  "field": "error.keyword",
  "chi_square": { "include_negatives": false }
}
```

### Google 正規化距離

Google 正規化距離 (Google Normalized Distance, GND) 傾向於強共現。它對於同義詞發現或傾向於共同出現的項目非常有用：

```json
"significant_terms": {
  "field": "tag.keyword",
  "gnd": {}
}
```

### 百分比

百分比 (Percentage) 根據 `doc_count`/`bg_count` 比例對詞元進行排序，並識別詞元相對於其背景命中數的前景命中數。它不考慮兩個集的整體大小，因此極其罕見的詞元可能會佔主導地位：

```json
"significant_terms": {
  "field": "sku.keyword",
  "percentage": {}
}
```

### 指令碼啟發式演算法

若要提供自訂的啟發式公式，請使用以下變數：

- `_subset_freq`：前景集中包含該詞元的文件數量。
- `_superset_freq`：背景集中包含該詞元的文件數量。
- `_subset_size`：前景集中的文件總數。
- `_superset_size`：背景集中的文件總數。

以下請求在 `field.keyword` 上執行 `significant_terms` 彙總，使用自訂指令碼啟發式演算法根據詞元在前景相對於背景的頻率來對其評分：

```json
"significant_terms": {
  "field": "field.keyword",
  "script_heuristic": {
    "script": {
      "lang": "painless",
      "source": "params._subset_freq / (params._superset_freq - params._subset_freq + 1)"
    }
  }
}
```


