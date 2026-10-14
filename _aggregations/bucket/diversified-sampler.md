---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "多樣化取樣器"
parent: Bucket aggregations
nav_order: 40
redirect_from:
  - /query-dsl/aggregations/bucket/diversified-sampler/
---

# 多樣化取樣器彙總

`diversified_sampler` 彙總是一種篩選彙總，會將子彙總的處理限制在評分最高的文件樣本上，同時確保樣本包含多樣的內容。它擴充了 [`sampler` 彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/sampler/)，方法是對共用相同欄位值的文件進行去除重複，避免任何單一類別主導整個樣本。

由於樣本只包含評分最高的文件，子彙總結果會聚焦於最相關的相符項目，不會被大量較弱的相符項目稀釋。當您需要確保不同群組之間有公平的呈現時，此彙總也很有用——例如，避免單一多產的作者扭曲分析結果，或確保以地點為基礎的分析具有地理多樣性。它也能透過從更小、更具代表性的樣本產生有用的結果，來降低像是 `significant_terms` 這類高成本子彙總的開銷。

## 參數

`diversified_sampler` 彙總採用下列參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `field` | 選用 | 字串 | 用於去除重複的欄位。每個文件必須產生單一值。必須指定 `field` 或 `script` 其中之一。 |
| `script` | 選用 | 物件 | 產生去除重複值的指令碼。必須指定 `field` 或 `script` 其中之一。若同時指定兩者，指令碼會作為值指令碼，並以 `_value` 接收欄位值。 |
| `shard_size` | 選用 | 整數 | 在每個分片上收集之評分最高文件的最大數量。預設為 `100`。 |
| `max_docs_per_value` | 選用 | 整數 | 在每個分片上，共用相同去除重複值的文件可進入樣本的上限。預設為 `1`，因此樣本中每個值最多只包含一份文件。 |
| `execution_hint` | 選用 | 字串 | 控制去除重複值在記憶體中的管理方式。請參閱[執行提示](#execution-hint)。 |

### 執行提示

下表列出有效的 `execution_hint` 值。

| 值 | 說明 |
| :--- | :--- |
| `map` | 直接將欄位值保存在記憶體中。 |
| `global_ordinals` | 使用 Lucene 針對該欄位的序數對應，在高基數欄位上提供更好的記憶體效率。 |
| `bytes_hash` | 儲存每個值的雜湊，而非值本身。在某些情境下可提升速度，但若兩個不同的值具有相同的雜湊，OpenSearch 會將它們視為同一個值，這可能會縮小樣本。 |

根據預設，若欄位有序數，OpenSearch 會使用 `global_ordinals`，否則使用 `map`。除非 `bytes_hash` 因為雜湊碰撞而將兩個不同的值視為重複，否則這三個選項會產生相同的樣本。它們的差異只在於保存在記憶體中的值類型，且每個選項最多可保存 `shard_size` 個值。若所選選項不適用於該欄位類型，OpenSearch 會忽略 `execution_hint`，而無法辨識的值會導致請求失敗。


`diversified_sampler` 彙總可以巢狀置於 `terms` 彙總之下。若 `terms` 彙總使用 `breadth_first` 收集模式，OpenSearch 會重播延後文件的相關性分數，因此樣本仍以評分最高的文件為基礎。
{: .note}

## 範例：依欄位去除重複

評分最高文件的樣本可能會被少數多產的來源主導，例如一位下了許多相似訂單的客戶。在範例電子商務資料中，有一位客戶在 646 筆包含洋裝的訂單中下了 103 筆。單純的 `sampler` 搭配 `shard_size` 為 `100` 時，只包含來自 16 位客戶的訂單。

下列範例會對包含洋裝的評分最高訂單進行取樣，但每個 `customer_id` 只允許一筆訂單，讓子彙總能平均反映許多客戶：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "query": {
    "match": {
      "products.product_name": "dress"
    }
  },
  "aggs": {
    "unbiased_sample": {
      "diversified_sampler": {
        "shard_size": 100,
        "field": "customer_id"
      },
      "aggs": {
        "customers": {
          "cardinality": {
            "field": "customer_id"
          }
        },
        "top_manufacturers": {
          "terms": {
            "field": "manufacturer.keyword",
            "size": 3
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

樣本包含 22 筆訂單，來自 22 位訂購洋裝的客戶各一筆：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "aggregations": {
    "unbiased_sample": {
      "doc_count": 22,
      "top_manufacturers": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 17,
        "buckets": [
          {
            "key": "Tigress Enterprises",
            "doc_count": 7
          },
          {
            "key": "Low Tide Media",
            "doc_count": 6
          },
          {
            "key": "Oceanavigations",
            "doc_count": 6
          }
        ]
      },
      "customers": {
        "value": 22
      }
    }
  }
}
```
</details>

## 範例：依指令碼去除重複

使用指令碼依值的組合進行多樣化。下列範例針對每個 `customer_gender` 與 `day_of_week` 的組合最多允許三筆訂單：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "query": {
    "match": {
      "products.product_name": "dress"
    }
  },
  "aggs": {
    "unbiased_sample": {
      "diversified_sampler": {
        "shard_size": 100,
        "max_docs_per_value": 3,
        "script": {
          "lang": "painless",
          "source": "doc['customer_gender'].value + '-' + doc['day_of_week'].value"
        }
      },
      "aggs": {
        "by_day": {
          "terms": {
            "field": "day_of_week",
            "size": 7
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

樣本包含 27 筆訂單：每個性別與星期幾的組合最多三筆。由於每一天都可能包含女性與男性客戶的訂單，有些天會包含超過三筆訂單：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "aggregations": {
    "unbiased_sample": {
      "doc_count": 27,
      "by_day": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
          {
            "key": "Thursday",
            "doc_count": 5
          },
          {
            "key": "Friday",
            "doc_count": 4
          },
          {
            "key": "Sunday",
            "doc_count": 4
          },
          {
            "key": "Tuesday",
            "doc_count": 4
          },
          {
            "key": "Wednesday",
            "doc_count": 4
          },
          {
            "key": "Monday",
            "doc_count": 3
          },
          {
            "key": "Saturday",
            "doc_count": 3
          }
        ]
      }
    }
  }
}
```
</details>

## 回應本文欄位

下表列出回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `doc_count` | 整數 | 多樣化樣本中的文件總數。 |

## 限制

`diversified_sampler` 彙總有下列限制：

- `field` 或 `script` 必須為每個文件產生單一值。使用多值欄位（例如範例電子商務資料中的 `manufacturer.keyword`）會導致請求失敗。若要依多值欄位的所有值進行多樣化，請使用將它們合併為單一值的指令碼，例如 `doc['manufacturer.keyword'].hashCode()`。
- 去除重複會分別套用於每個分片，因此不同分片上具有相同值的文件不會彼此去除重複。
- 沒有針對地理或日期多樣性值（例如 `7d` 或 `10km`）的專用語法。若要依地理區域或時間間隔進行多樣化，請撰寫將原始值分桶的指令碼——例如，緯度帶使用 `(int)(doc['geoip.location'].lat / 10)`，或按星期幾分組使用 `doc['order_date'].value.dayOfWeek`。
