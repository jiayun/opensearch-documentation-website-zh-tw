---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指令碼指標"
parent: Metric aggregations
nav_order: 100
redirect_from:
  - /query-dsl/aggregations/metric/scripted-metric/
---

# 指令碼指標彙總

`scripted_metric` 彙總是一種多值指標彙總，會傳回由您提供的指令碼計算出的指標。此彙總會執行四個指令碼，分別對應各個階段：`init`、`map`、`combine` 和 `reduce`。這些階段會依序執行，並共同合併文件的結果。指令碼以 [Painless]({{site.url}}{{site.baseurl}}/scripting/painless/) 撰寫，您可以將每個指令碼以內嵌方式提供，或以[預存指令碼]({{site.url}}{{site.baseurl}}/api-reference/script-apis/create-stored-script/)提供。

這四個指令碼共用一個由您定義、名為 `state` 的可變物件。在 `init`、`map` 和 `combine` 階段，`state` 僅存在於各自的分片中。結果會傳入 `states` 陣列，供 `reduce` 階段使用。因此，在 `reduce` 步驟合併分片之前，每個分片的 `state` 都是獨立的。每個指令碼都可以指定為包含指令碼原始碼的字串，或指定為指令碼物件。如需指定指令碼的詳細資訊，請參閱[如何使用指令碼]({{site.url}}{{site.baseurl}}/scripting/using-scripts/)。

## 參數

`scripted_metric` 彙總接受下列參數。

| 參數        | 資料類型 | 必要／選用 | 說明                                                                                        |
| ---------------- | --------- | ----------------- | -------------------------------------------------------------------------------------------------- |
| `init_script`    | 字串或物件 | 選用          | 在處理任何文件之前，於每個分片執行一次的指令碼。用於設定初始 `state`（例如，初始化 `state` 物件中的計數器或清單）。若未提供，則每個分片上的 `state` 起初都是空物件。 |
| `map_script`     | 字串或物件 | 必要          | 針對彙總收集的每份文件執行的指令碼。此指令碼會根據文件的資料更新 `state`。例如，您可以檢查欄位的值，然後遞增計數器，或在 `state` 中計算累加總和。                                                  |
| `combine_script` | 字串或物件 | 必要          | 在分片上的所有文件都經過 `map_script` 處理後，於該分片執行一次的指令碼。此指令碼會將分片的 `state` 彙總成單一結果，以傳回協調節點。此指令碼用於完成單一分片的計算（例如，加總儲存在 `state` 中的計數器或總計）。指令碼應傳回其分片的整合值或結構。  |
| `reduce_script`  | 字串或物件 | 必要          | 在收到所有分片的合併結果後，於協調節點執行一次的指令碼。此指令碼會接收特殊變數 `states`，這是一個陣列，包含各分片由 `combine_script` 產生的輸出。`reduce_script` 會逐一處理各個狀態，並產生最終彙總輸出（例如，加總分片總和或合併計數的映射）。`reduce_script` 傳回的值就是彙總結果中回報的值。 |
| `params`         | 物件    | 選用          | 使用者定義的參數，四個指令碼皆可存取。                        |

## 允許的傳回類型

指令碼內部可以使用任何有效的運算和物件。不過，您儲存在 `state` 中或從任何指令碼傳回的資料，都必須屬於允許的類型之一。之所以有此限制，是因為中間的 `state` 需要在節點之間傳送。允許的類型如下：

- 基本類型：`int`、`long`、`float`、`double`、`boolean`
- 字串
- 映射（鍵和值僅能使用允許的類型：基本類型、字串、映射或陣列）
- 陣列（僅包含允許的類型：基本類型、字串、映射或陣列）

`state` 可以是數字、字串、`map`（物件）或陣列（清單），也可以是這些類型的組合。例如，您可以使用 `map` 累積多個計數器、使用陣列收集值，或使用單一數字記錄累加總和。如果您需要傳回多個指標，可以將它們儲存在 `map` 或陣列中。如果您從 `reduce_script` 傳回 `map` 作為最終值，彙總結果就會包含一個物件。如果您傳回單一數字或字串，結果就會是單一值。

## 在指令碼中使用參數

您可以選擇使用 `params` 欄位，將自訂參數傳遞給指令碼。這是一個使用者定義的物件，其內容在四個指令碼中皆可透過 `params` 取得。如果您未指定任何 `params`，`params` 物件就會是空的。您也可以在個別指令碼物件上定義 `params`，例如 `"reduce_script": {"source": "...", "params": {...}}`。OpenSearch 會將這些參數與最上層的 `params` 合併。同一個參數名稱不能同時出現在這兩個位置；如果出現，請求就會失敗。 

例如，您可以在 `params` 中提供 `threshold` 或 `field` 名稱，然後在指令碼中參照 `params.threshold` 或 `params.field`：

```json
"scripted_metric": {
  "params": {
    "threshold": 100,
    "field": "amount"
  },
  "init_script": "...",
  "map_script": "...",
  "combine_script": "...",
  "reduce_script": "..."
}
```

## 範例

下列範例示範使用 `scripted_metric` 的不同方式。

### 從交易計算淨利

下列範例示範如何使用 `scripted_metric` 彙總，計算內建彙總未直接支援的自訂指標。此資料集代表財務交易，其中每份文件都分類為 `sale`（收入）或 `cost`（支出），並包含 `amount` 欄位。目標是將所有文件的銷售總額減去成本總額，以計算總淨利。 

建立索引：

```json
PUT transactions
{
  "mappings": {
    "properties": {
      "type":   { "type": "keyword" }, 
      "amount": { "type": "double" }
    }
  }
}
```
{% include copy-curl.html %}

將四筆交易編製索引，包含兩筆銷售（金額為 `80` 和 `130`）與兩筆成本（`10` 和 `30`）：

```json
PUT transactions/_bulk?refresh=true
{ "index": {} }
{ "type": "sale", "amount": 80 }
{ "index": {} }
{ "type": "cost", "amount": 10 }
{ "index": {} }
{ "type": "cost", "amount": 30 }
{ "index": {} }
{ "type": "sale", "amount": 130 }
```
{% include copy-curl.html %}

若要執行包含 `scripted_metric` 彙總的搜尋來計算利潤，請使用下列指令碼：

- `init_script` 會建立空清單，用於儲存每個分片的交易值。 
- `map_script` 會將每份文件的金額加入 `state.transactions` 清單；若類型為 `sale`，則以正數加入，若類型為 `cost`，則以負數加入。到 `map` 階段結束時，每個分片都有一份代表其收入與支出的 `state.transactions` 清單。 
- `combine_script` 會處理 `state.transactions` 清單，並為該分片計算單一 `shardProfit` 值。接著會傳回 `shardProfit` 作為分片的輸出。 
- `reduce_script` 會在協調節點上執行，接收 `states` 陣列，其中包含每個分片的 `shardProfit` 值。它會檢查是否有 null 項目，將這些值加總以計算整體利潤，並傳回最終結果。

下列請求包含上述所有指令碼：

```json
GET transactions/_search
{
  "size": 0, 
  "aggs": {
    "total_profit": {
      "scripted_metric": {
        "init_script": "state.transactions = []",
        "map_script": "state.transactions.add(doc['type'].value == 'sale' ? doc['amount'].value : -1 * doc['amount'].value)",
        "combine_script": "double shardProfit = 0; for (t in state.transactions) { shardProfit += t; } return shardProfit;",
        "reduce_script": "double totalProfit = 0; for (p in states) { if (p != null) { totalProfit += p; }} return totalProfit;"
      }
    }
  }
}
```
{% include copy-curl.html %}


回應會傳回 `total_profit`：

```json
{
  ...
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "total_profit": {
      "value": 170.0
    }
  }
}
```

### 逐分片逐步解說

若要了解這四個階段如何處理資料，請在具有兩個分片的索引上執行淨利計算。建立索引：

```json
PUT transactions_2shards
{
  "settings": {
    "number_of_shards": 2
  },
  "mappings": {
    "properties": {
      "type":   { "type": "keyword" },
      "amount": { "type": "double" }
    }
  }
}
```
{% include copy-curl.html %}

將這四筆交易編製索引。`routing` 值會將文件 1 和 3 放在分片 0，並將文件 2 和 4 放在分片 1：

```json
POST transactions_2shards/_bulk?refresh
{ "index": { "_id": "1", "routing": "a" } }
{ "type": "sale", "amount": 80 }
{ "index": { "_id": "2", "routing": "b" } }
{ "type": "cost", "amount": 10 }
{ "index": { "_id": "3", "routing": "a" } }
{ "type": "cost", "amount": 30 }
{ "index": { "_id": "4", "routing": "b" } }
{ "type": "sale", "amount": 130 }
```
{% include copy-curl.html %}

下表顯示每個分片上淨利計算各階段的結果。

| 階段 | 分片 0（文件 1 和 3） | 分片 1（文件 2 和 4） |
| :--- | :--- | :--- |
| `init_script` 之前 | `{}` | `{}` |
| `init_script` 之後 | `{"transactions": []}` | `{"transactions": []}` |
| `map_script` 之後 | `{"transactions": [80.0, -30.0]}` | `{"transactions": [-10.0, 130.0]}` |
| `combine_script` 之後 | `50.0` | `120.0` |

接著 `reduce_script` 會在協調節點上執行一次。它會接收 `states` 陣列 `[50.0, 120.0]` 並傳回其總和 `170.0`。

`states` 中項目的順序並不保證，因此您可能會看到 `[120.0, 50.0]`。請撰寫 `reduce_script`，使其結果不依賴分片結果的順序。
{: .note}

若要自行檢查中間結果，請讓後續的指令碼原樣傳回其輸入。例如，下列請求會透過從 `combine_script` 傳回 `state` 並從 `reduce_script` 傳回 `states`，來傳回每個分片在 `map_script` 之後的 `state`：

```json
GET transactions_2shards/_search
{
  "size": 0,
  "aggs": {
    "profit": {
      "scripted_metric": {
        "init_script": "state.transactions = []",
        "map_script": "state.transactions.add(doc['type'].value == 'sale' ? doc['amount'].value : -1 * doc['amount'].value)",
        "combine_script": "return state",
        "reduce_script": "return states"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會為每個分片包含一個 `state` 物件：

```json
{
  ...
  "aggregations": {
    "profit": {
      "value": [
        {
          "transactions": [
            80.0,
            -30.0
          ]
        },
        {
          "transactions": [
            -10.0,
            130.0
          ]
        }
      ]
    }
  }
}
```

同樣地，若要查看每個分片上 `combine_script` 的結果，請保留原始的 `combine_script` 並從 `reduce_script` 傳回 `states`：

```json
GET transactions_2shards/_search
{
  "size": 0,
  "aggs": {
    "profit": {
      "scripted_metric": {
        "init_script": "state.transactions = []",
        "map_script": "state.transactions.add(doc['type'].value == 'sale' ? doc['amount'].value : -1 * doc['amount'].value)",
        "combine_script": "double p = 0; for (t in state.transactions) { p += t } return p",
        "reduce_script": "return states"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會包含在每個分片上計算出的利潤：

```json
{
  ...
  "aggregations": {
    "profit": {
      "value": [
        50.0,
        120.0
      ]
    }
  }
}
```


### 使用已儲存的指令碼

您可以使用 [Create or Update Stored Script API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/create-stored-script/) 儲存每個指令碼，並透過 `id` 加以參照。下列請求會儲存前述範例中的四個指令碼。`map_script` 會從 `params.field` 讀取金額欄位的名稱：

```json
PUT _scripts/profit_init
{
  "script": {
    "lang": "painless",
    "source": "state.transactions = []"
  }
}
```
{% include copy-curl.html %}

```json
PUT _scripts/profit_map
{
  "script": {
    "lang": "painless",
    "source": "double v = doc[params.field].value; state.transactions.add(doc['type'].value == 'sale' ? v : -1 * v)"
  }
}
```
{% include copy-curl.html %}

```json
PUT _scripts/profit_combine
{
  "script": {
    "lang": "painless",
    "source": "double p = 0; for (t in state.transactions) { p += t } return p"
  }
}
```
{% include copy-curl.html %}

```json
PUT _scripts/profit_reduce
{
  "script": {
    "lang": "painless",
    "source": "double p = 0; for (s in states) { if (s != null) { p += s } } return p"
  }
}
```
{% include copy-curl.html %}

下列請求會透過 `id` 參照已儲存的指令碼。請在最上層的 `params` 物件中定義參數，使其可供所有指令碼使用：

```json
GET transactions/_search
{
  "size": 0,
  "aggs": {
    "total_profit": {
      "scripted_metric": {
        "init_script": { "id": "profit_init" },
        "map_script": { "id": "profit_map" },
        "combine_script": { "id": "profit_combine" },
        "reduce_script": { "id": "profit_reduce" },
        "params": {
          "field": "amount"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會包含與前述範例相同的 `total_profit`：

```json
{
  ...
  "aggregations": {
    "total_profit": {
      "value": 170.0
    }
  }
}
```

### 將 HTTP 回應碼分類

下列範例示範 `scripted_metric` 彙總的更進階用法，可在單一彙總中傳回多個值。資料集由網頁伺服器記錄檔項目組成，每個項目都包含一個 HTTP 回應碼。目標是將回應分類為三個類別：成功回應（2xx 狀態碼）、用戶端或伺服器錯誤（4xx 或 5xx 狀態碼），以及其他回應（1xx 或 3xx 狀態碼）。此分類是透過在以 map 為基礎的彙總 `state` 中維護計數器來實作。

建立範例索引：

```json
PUT logs
{
  "mappings": {
    "properties": {
      "response": { "type": "keyword" }
    }
  }
}
```
{% include copy-curl.html %}

新增包含各種回應碼的範例文件：

```json
PUT logs/_bulk?refresh=true
{ "index": {} }
{ "response": "200" }
{ "index": {} }
{ "response": "201" }
{ "index": {} }
{ "response": "404" }
{ "index": {} }
{ "response": "500" }
{ "index": {} }
{ "response": "304" }
```
{% include copy-curl.html %}

`state`（在每個分片上）是一個 `map`，其中包含三個計數器：`error`、`success` 和 `other`。

若要執行可計數各類別的指令碼指標彙總，請使用下列指令碼：

- `init_script` 會將 `error`、`success` 和 `other` 的計數器初始化為 `0`。
- `map_script` 會檢查每個文件的回應碼，並根據回應碼遞增相關的計數器。
- `combine_script` 會傳回該分片的 `state.responses` map。
- `reduce_script` 會合併來自所有分片的 map 陣列（`states`）。因此，它會建立新的合併 `map`，並加入每個分片 `map` 中的 `error`、`success` 和 `other` 計數。此合併的 `map` 會作為最終結果傳回。

下列請求包含所有所述的指令碼：

```json
GET logs/_search
{
  "size": 0,
  "aggs": {
    "responses_by_type": {
      "scripted_metric": {
        "init_script": "state.responses = new HashMap(); state.responses.put('success', 0); state.responses.put('error', 0); state.responses.put('other', 0);",
        "map_script": """
          String code = doc['response'].value;
          if (code.startsWith("5") || code.startsWith("4")) {
            // 4xx or 5xx -> count as error
            state.responses.error += 1;
          } else if (code.startsWith("2")) {
            // 2xx -> count as success
            state.responses.success += 1;
          } else {
            // anything else (e.g., 1xx, 3xx, etc.) -> count as other
            state.responses.other += 1;
          }
        """,
        "combine_script": "return state.responses;",
        "reduce_script": """
          Map combined = new HashMap();
          combined.error = 0;
          combined.success = 0;
          combined.other = 0;
          for (state in states) {
            if (state != null) {
              combined.error += state.error;
              combined.success += state.success;
              combined.other += state.other;
            }
          }
          return combined;
        """
      }
    }
  }
}
```
{% include copy-curl.html %}


回應會在 `value` 物件中傳回三個值，示範指令碼指標如何透過在 `state` 中使用 `map`，一次傳回多個指標：

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
    "responses_by_type": {
      "value": {
        "other": 1,
        "success": 2,
        "error": 2
      }
    }
  }
}
```

## 管理空桶

沒有相符文件的分片仍會執行 `init_script` 和 `combine_script`，因此會將 `combine_script` 的結果加入 `states` 陣列。然而，某些桶彙總會建立未在任何分片上收集的空桶 (bucket)。例如，`histogram` 或 `date_histogram` 彙總會在第一個與最後一個包含文件的桶之間傳回空桶。對於這些桶，`states` 陣列會包含 `null`。

下列請求會將交易分組至間隔為 25 的直方圖桶中，並計算每個桶的利潤。這些交易的金額分別為 10、30、80 和 130，因此 50 和 100 的桶是空的。`reduce_script` 會在加入每個狀態之前檢查 `null`：

```json
GET transactions/_search
{
  "size": 0,
  "aggs": {
    "by_amount": {
      "histogram": {
        "field": "amount",
        "interval": 25
      },
      "aggs": {
        "profit": {
          "scripted_metric": {
            "init_script": "state.transactions = []",
            "map_script": "state.transactions.add(doc['type'].value == 'sale' ? doc['amount'].value : -1 * doc['amount'].value)",
            "combine_script": "double s = 0; for (t in state.transactions) { s += t } return s",
            "reduce_script": "double total = 0; for (s in states) { if (s != null) { total += s } } return total"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

空桶回報的利潤為 `0`：

```json
{
  ...
  "aggregations": {
    "by_amount": {
      "buckets": [
        {
          "key": 0.0,
          "doc_count": 1,
          "profit": {
            "value": -10.0
          }
        },
        {
          "key": 25.0,
          "doc_count": 1,
          "profit": {
            "value": -30.0
          }
        },
        {
          "key": 50.0,
          "doc_count": 0,
          "profit": {
            "value": 0.0
          }
        },
        {
          "key": 75.0,
          "doc_count": 1,
          "profit": {
            "value": 80.0
          }
        },
        {
          "key": 100.0,
          "doc_count": 0,
          "profit": {
            "value": 0.0
          }
        },
        {
          "key": 125.0,
          "doc_count": 1,
          "profit": {
            "value": 130.0
          }
        }
      ]
    }
  }
}
```

若沒有 `if (s != null)` 檢查，`reduce_script` 會針對空桶發生 `null_pointer_exception` 而失敗。請務必檢查 `states` 陣列中的 `null` 項目。
{: .important}

## 效能考量

由於指令碼指標會針對每份文件執行自訂程式碼，因此可能在記憶體中累積大型的 `state`，所以可能比內建彙總更慢。每個分片的中間 `state` 必須經過序列化，才能傳送至協調節點。因此，如果您的 `state` 非常大，可能會耗用大量記憶體與網路頻寬。為了維持搜尋效率，請盡可能讓指令碼保持輕量，並避免在 `state` 中累積不必要的資料。請使用合併階段在傳送前縮減 `state` 資料，如[計算交易的淨利](#calculating-net-profit-from-transactions)中所示範，並且只收集產生最終指標真正需要的值。

