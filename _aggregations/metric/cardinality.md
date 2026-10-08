---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Cardinality
parent: Metric aggregations
nav_order: 20
redirect_from:
  - /query-dsl/aggregations/metric/cardinality/
---

# Cardinality 彙總

`cardinality` 彙總是一種單值指標彙總，用於計算某個欄位中唯一或不重複值的數量。


基數計數是近似值。更多資訊請參閱[控制精確度](#controlling-precision)。

## 參數

`cardinality` 彙總接受下列參數。

| 參數             | 必要/選用 | 資料類型       | 說明 |
| :--                   | :--               |  :--            | :--         |
| `field`               | 必要          | 字串          | 要估算基數的欄位。 |
| `precision_threshold` | 選用          | 數值         | 低於此閾值時，計數預期會接近準確。更多資訊請參閱[控制精確度](#controlling-precision)。     |
| `execution_hint`      | 選用          | 字串          | 彙總的執行方式。有效值為 `ordinals` 與 `direct`。 |
| `missing`             | 選用          | 與 `field` 的類型相同 | 用於儲存欄位缺失實例的桶。若未提供，缺失值將被忽略。 |

## 範例

下列範例請求會找出 OpenSearch Dashboards 範例電子商務資料中不重複產品 ID 的數量：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "unique_products": {
      "cardinality": {
        "field": "products.product_id"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 回應範例

如下列範例回應所示，彙總會在 `unique_products` 變數中傳回基數計數：

```json
{
  "took": 176,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "unique_products": {
      "value": 7033
    }
  }
}
```

## 控制精確度

精確的基數計算需要將所有值載入雜湊集並傳回其大小。這種方法的擴充性不佳；可能需要大量記憶體並造成高延遲。

您可以使用 `precision_threshold` 設定來控制記憶體與精確度之間的權衡。此參數會設定一個閾值，低於此閾值時，計數預期會接近準確。高於此值的計數可能較不準確。

`precision_threshold` 的預設值為 3,000。支援的最大值為 40,000。

基數彙總使用 [HyperLogLog++ 演算法](https://static.googleusercontent.com/media/research.google.com/fr//pubs/archive/40671.pdf)。基數計數在精確度閾值內通常非常準確，在大多數其他情況下，即使閾值低至 100，誤差也在真實計數的 6% 以內。

### 預先計算雜湊值

對於高基數字串欄位，為索引欄位儲存雜湊值並計算雜湊的基數，可以節省運算與記憶體資源。請謹慎使用此方法；它僅對包含長字串和/或高基數的集合更有效率。數值欄位以及耗用記憶體較少的字串集合，直接處理反而更好。

### 範例：控制精確度

將精確度閾值設為 `10000` 個唯一值：

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "unique_products": {
      "cardinality": {
        "field": "products.product_id",
        "precision_threshold": 10000
      }
    }
  }
}
```
{% include copy-curl.html %}

回應與使用預設閾值的結果類似，但傳回的值略有不同。調整 `precision_threshold` 參數，觀察它如何影響基數估算。

## 設定彙總執行方式  

您可以使用 `execution_hint` 設定來控制彙總的執行方式。此設定支援兩個選項：  

- `direct` – 直接使用欄位值。  
- `ordinals` – 使用欄位的序數。 

若未指定 `execution_hint`，OpenSearch 會透過混合收集器（預設啟用）自動為該欄位選擇最佳選項。

在非序數欄位上設定 `ordinals` 不會產生任何效果。同樣地，`direct` 對序數欄位也沒有效果。  
{: .note}

這是專家級設定。序數使用位元組陣列，陣列大小取決於欄位的基數。高基數欄位可能耗用大量堆積記憶體，增加發生記憶體不足錯誤的風險。  
{: .warning}

### 範例：控制執行方式

下列請求使用序數執行基數彙總： 

```json
GET opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "unique_products": {
      "cardinality": {
        "field": "products.product_id",
        "execution_hint": "ordinals"
      }
    }
  }
}
```  
{% include copy-curl.html %}

## 混合收集器
**3.4 版新增**
{: .label .label-purple }

預設情況下，OpenSearch 會對基數彙總使用 _混合收集器_ ，以提升速度並管理記憶體。混合收集器從較快的序數收集器開始，並在執行期間監控記憶體使用量。若使用量超過可設定的閾值，它會自動切換至直接收集器，並從已計算的資料繼續。

這種方法在記憶體可用時提供更快的效能，同時確保高基數欄位的安全性。它會動態適應實際記憶體狀況，並避免切換收集器時重新啟動彙總的額外負擔。

若要設定混合收集器，請使用下列叢集設定：
- `search.aggregations.cardinality.hybrid_collector.enabled` (Dynamic, 布林值)：啟用混合收集器。停用時，OpenSearch 會使用傳統邏輯在序數收集器與直接收集器之間進行選擇。預設為 `true`。
- `search.aggregations.cardinality.hybrid_collector.memory_threshold` (Dynamic, 百分比或位元組大小)：設定從序數收集器切換至直接收集器的記憶體閾值。您可以將此設定指定為 JVM 堆積的百分比（例如 `1%`）或絕對值（例如 `10mb` 或 `1gb`）。預設為 `1%`。

## 缺失值

您可以為彙總欄位的缺失實例指定一個值。更多資訊請參閱[缺失彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/missing/)。

在基數彙總中替換缺失值，會將替換值加入唯一值清單，使實際基數增加一。
