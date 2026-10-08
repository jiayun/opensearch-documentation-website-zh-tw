---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "將查詢隨機化"
nav_order: 65
has_math: true
redirect_from:
  - /benchmark/user-guide/optimizing-benchmarks/randomizing-queries/
---

# 將查詢隨機化

預設情況下，OpenSearch Benchmark 會在多次基準測試迭代中執行相同的查詢。然而，反覆執行相同的查詢並非在每種測試情境下都適合。例如，使用多次相同查詢的迭代來模擬實際環境中的快取行為，會造成一次快取未命中，接著多次命中。OpenSearch Benchmark 可讓您以可設定的方式將查詢隨機化。 

例如，變更下列 `nyc_taxis` 作業中的 `"gte"` 和 `"lt"` 會建立不同的查詢，產生各自獨立的快取項目：

```json
{
    "name": "range",
    "operation-type": "search",
    "body": {
    "query": {
        "range": {
        "total_amount": {
            "gte": 5,
            "lte": 15
        }
        }
    }
    }
}
```

您無法將值完全隨機化，因為這樣快取就不會有任何命中。若要讓快取命中，快取必須偶爾遇到相同的值。為了在隨機化的同時納入相同的值，OpenSearch Benchmark 會在基準測試開始時，為每個隨機化作業產生 $$N$$ 組值配對。OpenSearch Benchmark 會將這些值儲存在已儲存的清單中，並為每組配對指派從 $$1$$ 到 $$N$$ 的索引。

每次 OpenSearch 傳送查詢時，OpenSearch Benchmark 都會決定是否在查詢中使用這份已儲存清單中的一組值配對。它會依可設定的比例這樣做，此比例稱為 _重複頻率_（`rf`）。如果 OpenSearch 先前遇過該值配對，就可能造成快取命中。例如，如果 `rf` = 0.7，快取命中率最高可達 70%。此比例是否能造成命中，取決於基準測試的持續時間與快取大小。 

OpenSearch Benchmark 使用 Zipf 機率分布來選取已儲存的值配對，其中選取配對 $$i$$ 的機率與 $$1 \over i^\alpha$$ 成正比。在此公式中，$$i$$ 代表已儲存值配對的索引，而 $$\alpha$$ 控制分布的集中程度。此分布反映了在實際快取中觀察到的使用模式。$$i$$ 值較低（較接近 $$1$$）的配對會更常被選取，而 $$i$$ 值較高（較接近 $$N$$）的配對則較少被選取。

在其餘 $$1 -$$ `rf` 比例的時間內，會產生一組新的隨機值配對。由於 OpenSearch Benchmark 先前未遇過這些值配對，因此這些配對應該不會命中快取。

## 使用方式

若要在工作負載中使用此功能，您必須對 `workload.py` 做一些變更，並在執行 OpenSearch Benchmark 時提供一些 CLI 旗標。

### 修改 `workload.py`

為每個作業註冊「標準值來源」，以指定如何產生該作業的已儲存值配對。這個 Python 函式不接受任何引數，並傳回一個字典。其鍵與輸入查詢中的鍵相同，但值會隨機化。最後，變更 `register()` 方法，讓它以要隨機化的作業名稱和欄位名稱註冊此函式。

例如，用於將前述 `"range"` 作業中的 `"total_amount"` 欄位隨機化的標準值來源，可能類似下列函式： 

```py
def random_money_values(max_value):
    gte_cents = random.randrange(0, max_value*100)
    lte_cents = random.randrange(gte_cents, max_value*100)
    return {
        "gte":gte_cents/100,
        "lte":lte_cents/100
    }

def range_query_standard_value_source():
    return random_money_values(120.00)
```

同樣地，您可以使用下列函式將註冊行為隨機化：

```py
def register(registry):
    registry.register_standard_value_source("range", "total_amount", range_query_standard_value_source)
```

此函式可能已包含程式碼。若有，請保留。如果 `workload.py` 不存在或缺少 `register(registry)` 函式，您可以建立它們。 

#### 將非範圍查詢隨機化

預設情況下，OpenSearch Benchmark 假設要隨機化的查詢是 `"range"` 查詢，具有 `"gte"`/`"gt"`、`"lte"`/`"lt"` 值，以及選用的 `"format"`。如果情況並非如此，您可以設定它使用不同的查詢類型名稱和不同的值。 

例如，若要將下列工作負載作業隨機化： 

```json
{
  "name": "bbox", 
  "operation-type": "search", 
  "index": "nyc_taxis",
  "body": { 
    "size": 0,
    "query": {
      "geo_bounding_box": {
        "pickup_location": {
          "top_left": [-74.27, 40.92],
          "bottom_right": [-73.68, 40.49]
        }
      }
    }
  }
}
```

您會在 `workload.py` 中註冊下列函式： 

```py
registry.register_query_randomization_info("bbox", "geo_bounding_box", [["top_left"], ["bottom_right"]], [])
```

第一個引數 `"bbox"` 是作業的名稱。 

第二個引數 `"geo_bounding_box"` 是查詢類型名稱。

第三個引數是由多個清單組成的清單：`[[“top_left”], [“bottom_right”]]`。外層清單的項目指定要隨機化的參數，因為同一個名稱可能有不同版本，代表大致相同的參數，例如 `"gte"` 或 `"gt"`。此處每個參數名稱都只有一個選項。每個參數名稱至少必須有一個版本出現在原始查詢中，才能將該參數隨機化。

最後一個引數是選用參數的清單。如果隨機標準值來源中存在某個選用參數，OpenSearch Benchmark 就會將該參數插入隨機化版本的查詢中。如果來源中沒有該參數，就會忽略它。下列範例沒有選用參數，但典型的使用案例是範圍查詢中的 `"format"`。

如果沒有註冊，就會使用預設註冊：`registry.register_query_randomization_info(<operation_name>, “range”, [[“gte”, “gt”], [“lte”, “lt”]], [“format”])`。


標準值來源傳回的 `dict` 應與您要隨機化的參數名稱相符。例如，下列是前述範例的標準值來源：

```py
def bounding_box_source(): 
    top_longitude = random.uniform(-74.27, -73.68)
    top_latitude = random.uniform(40.49, 40.92)

    bottom_longitude = random.uniform(top_longitude, -73.68)
    bottom_latitude = random.uniform(40.49, top_latitude)

    return { 
        "top_left":[top_longitude, top_latitude],
        "bottom_right":[bottom_longitude, bottom_latitude]
    }
```



### CLI 旗標

使用下列 CLI 旗標來自訂隨機化：

- `--randomization-enabled` 可啟用或停用隨機化。如果未啟用隨機化，就不會套用任何隨機化旗標。

- `--randomization-repeat-frequency` 或 `-rf` 設定從基準測試開始時產生的已儲存值配對中抽取配對的比例。此值應介於 `0.0` 和 `1.0` 之間。預設值為 `0.3`。 

- `--randomization-n` 設定為每個作業產生的值配對數量 `N`。預設值為 `5000`。 

- `--randomization-alpha` 設定 `alpha` 參數，用來控制 `Zipf` 分布的分散程度。此值應為 `>=0`。較低的值會增加分布的分散程度。預設值為 `1.0`。 
