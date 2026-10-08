---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "數值計數"
parent: Metric aggregations
nav_order: 140
redirect_from:
  - /query-dsl/aggregations/metric/value-count/
---

# 數值計數彙總

`value_count` 指標是一種單值指標彙總，用於計算從彙總文件中擷取的值的數量。這些值可以從文件中的特定欄位擷取，或由指令碼產生。此彙總通常會與 `avg` 等彙總搭配使用，以判斷有多少個值參與了計算結果。

`value_count` 彙總不會對值進行去重複。如果欄位包含重複值，或指令碼為單一文件產生多個相同的值，則每個值都會分別計數。

## 參數

`value_count` 彙總接受下列參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `field` | 字串 | 要計算值數量的欄位。 |
| `script` | 物件 | 產生要計數之值的指令碼。可用來取代 `field`，或與其搭配使用。 |
| `missing` | 數字或字串 | 指派給缺少目標欄位之文件的預設值。 |

## 範例

下列範例會計算電子商務索引中包含 `taxful_total_price` 值的文件數量：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "number_of_values": {
      "value_count": {
        "field": "taxful_total_price"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應顯示有 4,675 份文件包含指定欄位的值：

```json
{
  ...
  "hits": {
    "total": {
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "number_of_values": {
      "value": 4675
    }
  }
}
```

彙總名稱（`number_of_values`）同時也是從回應中擷取彙總結果時所使用的鍵。

### 使用指令碼

您可以提供指令碼來產生要計數的值，而不必指定欄位。如需更多資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。下列範例使用內嵌的 Painless 指令碼，根據計算出的值進行計數：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "type_count": {
      "value_count": {
        "script": {
          "source": "doc['taxful_total_price'].value"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會傳回指令碼所產生之值的數量：

```json
{
  ...
  "hits": {
    "total": {
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "type_count": {
      "value": 4675
    }
  }
}
```

### 使用預存指令碼

若要在多個查詢中重複使用指令碼，您可以將其儲存，並透過 ID 參照該指令碼。下列範例使用一個接受欄位名稱作為參數的預存指令碼：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "type_count": {
      "value_count": {
        "script": {
          "id": "my_value_count_script",
          "params": {
            "field": "taxful_total_price"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

由於 `value_count` 在內部將所有值表示為位元組序列，因此使用 `_value` 指令碼變數存取欄位值時，會以字串形式傳回該值，而非其原生格式。
{: .note}
