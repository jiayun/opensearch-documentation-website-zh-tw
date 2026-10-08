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

`scripted_metric` 彙總是一種多值指標彙總，會傳回根據指定指令碼計算出的指標。指令碼有四個階段：`init`、`map`、`combine` 和 `reduce`。每個彙總會依序執行這些階段，讓您能夠合併來自文件的結果。

這四個指令碼都共用一個由您定義、名為 `state` 的可變物件。在 `init`、`map` 和 `combine` 階段期間，`state` 僅存在於各個分片本機。其結果會傳入 `states` 陣列，供 `reduce` 階段使用。因此，在 `reduce` 步驟合併各分片之前，每個分片的 `state` 都是獨立的。

## 參數

`scripted_metric` 彙總接受下列參數。

| 參數        | 資料類型 | 必要/選用 | 說明                                                                                        |
| ---------------- | --------- | ----------------- | -------------------------------------------------------------------------------------------------- |
| `init_script`    | 字串    | 選用          | 在處理任何文件之前，於每個分片上執行一次的指令碼。用於設定初始的 `state`（例如，在 `state` 物件中初始化計數器或清單）。若未提供，`state` 在每個分片上都會從空物件開始。       |
| `map_script`     | 字串    | 必要          | 針對彙總所收集的每份文件執行的指令碼。此指令碼會根據文件的資料更新 `state`。例如，您可以檢查欄位的值，然後在 `state` 中遞增計數器或計算累計總和。                                                  |
| `combine_script` | 字串    | 必要          | 在 `map_script` 處理完該分片上的所有文件之後，於每個分片上執行一次的指令碼。此指令碼會將該分片的 `state` 彙總為單一結果，並傳回協調節點。此指令碼用於完成單一分片的計算（例如，加總儲存在 `state` 中的計數器或總計）。指令碼應傳回其分片經合併後的值或結構。  |
| `reduce_script`  | 字串    | 必要          | 在收到所有分片的合併結果後，於協調節點上執行一次的指令碼。此指令碼會收到一個特殊變數 `states`，這是一個陣列，包含每個分片來自 `combine_script` 的輸出。`reduce_script` 會逐一處理這些狀態並產生最終的彙總輸出（例如，將各分片的總和相加，或合併計數的對應表）。`reduce_script` 傳回的值即為彙總結果中回報的值。 |
| `params`         | 物件    | 選用          | 使用者定義的參數，除了 `reduce_script` 之外的所有指令碼皆可存取。                        |

## 允許的傳回類型

指令碼內部可以使用任何有效的運算和物件。不過，您儲存在 `state` 中或從任何指令碼傳回的資料，都必須屬於允許的類型之一。之所以有此限制，是因為中間的 `state` 需要在節點之間傳送。允許的類型如下：

- 基本類型：`int`、`long`、`float`、`double`、`boolean`
- 字串
- 對應表（鍵和值僅能是允許的類型：基本類型、字串、對應表或陣列）
- 陣列（僅包含允許的類型：基本類型、字串、對應表或陣列）

`state` 可以是數字、字串、`map`（物件）或陣列（清單），也可以是這些類型的組合。例如，您可以使用 `map` 累積多個計數器、使用陣列收集值，或使用單一數字保存累計總和。若需要傳回多個指標，可以將它們儲存在 `map` 或陣列中。若您從 `reduce_script` 傳回 `map` 作為最終值，彙總結果會包含一個物件。若傳回單一數字或字串，結果則為單一值。

## 在指令碼中使用參數

您可以選擇使用 `params` 欄位將自訂參數傳遞給指令碼。這是一個使用者定義的物件，其內容會成為 `init_script`、`map_script` 和 `combine_script` 中可用的變數。`reduce_script` 不會直接收到 `params`，因為到了 `reduce` 階段，所有需要的資料都必須已在 `states` 陣列中。若您在 `reduce` 階段需要常數，可以將其納入每個分片的 `state` 中，或使用預存指令碼。所有參數都必須定義在全域的 `params` 物件內，以確保它們能在不同的指令碼階段之間共用。若您未指定任何 `params`，`params` 物件即為空。 

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

下列範例示範了使用 `scripted_metric` 的不同方式。

### 從交易計算淨利

下列範例示範如何使用 `scripted_metric` 彙總來計算內建彙總未直接支援的自訂指標。此資料集代表財務交易，其中每份文件都會被歸類為 `sale`（收入）或 `cost`（支出），並包含 `amount` 欄位。目標是將所有文件的總銷售額減去總成本，以計算總淨利。 

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

將四筆交易編製索引，其中包含兩筆銷售（金額為 `80` 和 `130`）和兩筆成本（`10` 和 `30`）：

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

若要執行帶有 `scripted_metric` 彙總的搜尋來計算利潤，請使用下列指令碼：

- `init_script` 會建立一個空清單，用於儲存每個分片的交易值。 
- `map_script` 會將每份文件的金額加入 `state.transactions` 清單：若類型為 `sale`，則以正數加入；若類型為 `cost`，則以負數加入。到 `map` 階段結束時，每個分片都會有一個代表其收入和支出的 `state.transactions` 清單。 
- `combine_script` 會處理 `state.transactions` 清單，並為該分片計算出單一的 `shardProfit` 值。接著，`shardProfit` 會作為該分片的輸出傳回。 
- `reduce_script` 在協調節點上執行，會收到 `states` 陣列，其中保存了來自每個分片的 `shardProfit` 值。它會檢查是否有 null 項目，將這些值相加以計算整體利潤，並傳回最終結果。

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
      "value": 170
    }
  }
}
```

### 將 HTTP 回應碼分類

下列範例示範 `scripted_metric` 彙總的進階用法，可在單一彙總中傳回多個值。資料集由網頁伺服器記錄檔項目組成，每個項目都包含一個 HTTP 回應碼。目標是將回應分為三類：成功回應（2xx 狀態碼）、用戶端或伺服器錯誤（4xx 或 5xx 狀態碼），以及其他回應（1xx 或 3xx 狀態碼）。此分類的實作方式是在以對應表為基礎的彙總 `state` 中維護計數器。

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

（每個分片上的）`state` 是一個 `map`，其中包含三個計數器：`error`、`success` 和 `other`。

若要執行計算各類別數量的指令碼指標彙總，請使用下列指令碼：

- `init_script` 會將 `error`、`success` 和 `other` 的計數器初始化為 `0`。
- `map_script` 會檢查每份文件的回應碼，並根據回應碼遞增對應的計數器。
- `combine_script` 會傳回該分片的 `state.responses map`。
- `reduce_script` 會合併來自所有分片的對應表陣列（`states`）。因此，它會建立一個新的合併 `map`，並加總每個分片 `map` 中的 `error`、`success` 和 `other` 計數。此合併後的 `map` 會作為最終結果傳回。

下列請求包含上述所有指令碼：

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

## 處理空的桶 (bucket)（沒有文件）

在桶彙總（例如 `terms`）中將 `scripted_metric` 彙總作為子彙總使用時，務必考量在某些分片上不含任何文件的桶。在這種情況下，這些分片會針對彙總 `state` 傳回 `null` 值。因此，在 `reduce_script` 階段，`states` 陣列可能會包含對應這些分片的 `null` 項目。為確保執行穩定可靠，`reduce_script` 的設計必須能妥善處理 `null` 值。常見的做法是在存取或操作每個 `state` 之前，加入條件檢查，例如 `if (state != null)`。若未實作此類檢查，在跨分片處理空的桶時可能會導致執行階段錯誤。


## 效能考量

由於指令碼指標會針對每份文件執行自訂程式碼，因此可能會在記憶體中累積大型的 `state`，所以速度可能比內建彙總慢。每個分片的中間 `state` 都必須經過序列化，才能傳送至協調節點。因此，如果您的 `state` 非常大，可能會耗用大量記憶體和網路頻寬。為了讓搜尋保持有效率，請盡可能讓指令碼保持輕量，並避免在 `state` 中累積不必要的資料。請使用 combine 階段在傳送前縮減 `state` 資料（如[計算交易淨利](#calculating-net-profit-from-transactions)中所示），並且只收集產生最終指標真正需要的值。

