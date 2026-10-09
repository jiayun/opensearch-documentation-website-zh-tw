---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "依查詢更新"
parent: Document APIs
nav_order: 40
redirect_from: 
 - /opensearch/rest-api/document-apis/update-by-query/
---

# Update By Query API
**於 1.0 版推出**
{: .label .label-purple}

Update by Query API 會更新索引中符合指定查詢的所有文件。您可以在不變更文件來源的情況下更新文件，以套用對應變更，或使用指令碼根據自訂邏輯修改欄位值。

在下列情境中使用此 API：

- 新增欄位或變更欄位類型後，將對應變更套用至現有文件。
- 根據計算邏輯或條件更新多份文件中的欄位值。
- 對符合特定條件的文件遞增計數器或執行大量計算。
- 在指令碼中設定 `ctx.op = "delete"`，依條件刪除文件。
- 在不符合條件時設定 `ctx.op = "noop"`，執行不進行任何操作的更新。

當您提交依查詢更新請求時，OpenSearch 會在操作開始時建立索引快照，並使用內部版本控制更新符合條件的文件。如果文件在建立快照之後、更新操作處理該文件之前發生變更，就會發生版本衝突，且該文件的更新會失敗，除非您將 `conflicts` 參數設為 `proceed`。當版本衝突未導致操作中止時，文件會更新，且其版本號碼會遞增。即使批次中的後續操作失敗，已成功更新的文件也不會回復。

所有更新與查詢失敗都會導致操作中止，並傳回於回應的 `failures` 陣列中。即使操作中止，成功的更新仍會保留。雖然第一個失敗會觸發中止，但遭拒絕的大量請求中的所有失敗都會出現在 `failures` 元素中，因此可能會回報多個失敗的實體。

OpenSearch 會採用指數退避，對遭拒絕的搜尋或大量請求最多重試 10 次。如果達到重試次數上限，操作就會停止，並在回應中傳回所有失敗的請求。

**注意：** OpenSearch 無法使用此 API 更新版本為 `0` 的文件。內部版本控制系統要求版本號碼必須大於 0，才能正確追蹤與處理更新操作。
{: .note}


<!-- spec_insert_start
api: update_by_query
component: endpoints
-->
## 端點
```json
POST /{index}/_update_by_query
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: update_by_query
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `index` | **必要** | 清單或字串 | 要搜尋的資料串流、索引與別名清單，以逗號分隔。支援萬用字元（`*`）。若要搜尋所有資料串流或索引，請省略此參數，或使用 `*` 或 `_all`。 |

<!-- spec_insert_end -->

<!-- spec_insert_start
api: update_by_query
component: query_parameters
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `_source` | 布林值或清單或字串 | 設為 `true` 或 `false`，以決定是否傳回 `_source` 欄位，或設為要傳回的欄位清單。 | 不適用 |
| `_source_excludes` | 清單 | 要從傳回的 `_source` 欄位中排除的欄位清單。 | 不適用 |
| `_source_includes` | 清單 | 要從 `_source` 欄位擷取並傳回的欄位清單。 | 不適用 |
| `allow_no_indices` | 布林值 | 若為 `false`，當任何萬用字元運算式、索引別名或 `_all` 值僅指向不存在或已關閉的索引時，請求會傳回錯誤。即使請求也指向其他開啟的索引，此行為仍適用。例如，指向 `foo*,bar*` 的請求，如果存在以 `foo` 開頭的索引，但沒有以 `bar` 開頭的索引，就會傳回錯誤。 | 不適用 |
| `analyze_wildcard` | 布林值 | 若為 `true`，會分析萬用字元與前綴查詢。 | `false` |
| `analyzer` | 字串 | 查詢字串使用的分析器。 | 不適用 |
| `conflicts` | 字串 | 依查詢更新遇到版本衝突時要採取的動作：`abort` 或 `proceed`。<br> 有效值為：<br> - `abort`：發生版本衝突時中止操作。<br> - `proceed`：發生版本衝突時繼續操作。 | 不適用 |
| `default_operator` | 字串 | 查詢字串查詢的預設運算子：`AND` 或 `OR`。<br> 有效值為：`and`、`AND`、`or` 與 `OR`。 | 不適用 |
| `df` | 字串 | 查詢字串未提供欄位前綴時，使用的預設欄位。 | 不適用 |
| `expand_wildcards` | 清單或字串 | 萬用字元模式可以比對的索引類型。如果請求可以指向資料串流，此引數會決定萬用字元運算式是否比對隱藏的資料串流。支援以逗號分隔的值，例如 `open,hidden`。有效值為：`all`、`open`、`closed`、`hidden`、`none`。<br> 有效值為：<br> - `all`：比對任何索引，包括隱藏的索引。<br> - `closed`：比對已關閉且未隱藏的索引。<br> - `hidden`：比對隱藏的索引。必須搭配 `open`、`closed` 或兩者使用。<br> - `none`：不接受萬用字元運算式。<br> - `open`：比對開啟且未隱藏的索引。 | 不適用 |
| `from` | 整數 | 起始位移。 | `0` |
| `ignore_unavailable` | 布林值 | 若為 `false`，當請求指向不存在或已關閉的索引時，會傳回錯誤。 | 不適用 |
| `lenient` | 布林值 | 若為 `true`，會忽略查詢字串中因格式造成的查詢失敗（例如將文字提供給數值欄位）。 | 不適用 |
| `max_docs` | 整數 | 要處理的文件數量上限。預設為所有文件。 | 不適用 |
| `pipeline` | 字串 | 用於預先處理傳入文件的管線 ID。如果索引已指定預設資料匯入管線，將此值設為 `_none` 會停用此請求的預設資料匯入管線。如果已設定最終管線，則無論此參數的值為何，最終管線都會執行。 | 不適用 |
| `preference` | 字串 | 指定應執行操作的節點或分片。預設為隨機選擇。 | `random` |
| `q` | 字串 | 使用 Lucene 查詢字串語法的查詢。 | 不適用 |
| `refresh` | 布林值或字串 | 若為 `true`，OpenSearch 會重新整理受影響的分片，讓搜尋可以看見此操作的結果。<br> 有效值為：<br> - `false`：不重新整理受影響的分片。<br> - `true`：立即重新整理受影響的分片。<br> - `wait_for`：等待變更可見後再回覆。 | 不適用 |
| `request_cache` | 布林值 | 若為 `true`，此請求會使用請求快取。 | 不適用 |
| `requests_per_second` | 浮點數 | 此請求的節流限制，以每秒子請求數表示。 | `0` |
| `routing` | 清單或字串 | 用於將操作路由至特定分片的自訂值。 | 不適用 |
| `scroll` | 字串 | 捲動搜尋情境的保留時間。 | 不適用 |
| `scroll_size` | 整數 | 用於執行此操作的捲動請求大小。 | `100` |
| `search_timeout` | 字串 | 每個搜尋請求的明確逾時時間。 | 不適用 |
| `search_type` | 字串 | 搜尋操作的類型。可用選項：`query_then_fetch`、`dfs_query_then_fetch`。<br> 有效值為：<br> - `dfs_query_then_fetch`：使用所有分片的全域詞彙頻率與文件頻率為文件評分。這通常較慢，但更準確。<br> - `query_then_fetch`：使用該分片的本機詞彙頻率與文件頻率為文件評分。這通常較快，但較不準確。 | 不適用 |
| `size` | 整數 | 已棄用，請改用 `max_docs`。 | 不適用 |
| `slices` | 整數或字串 | 此工作應分割成的切片數量。<br> 有效值為：<br> - `auto`：自動決定切片數量。 | 不適用 |
| `sort` | 清單 | 以逗號分隔的 <field>:<direction> 配對清單。 | 不適用 |
| `stats` | 清單 | 請求的特定 `tag`，用於記錄與統計。 | 不適用 |
| `terminate_after` | 整數 | 每個分片要收集的文件數量上限。如果查詢達到此上限，OpenSearch 會提前終止查詢。OpenSearch 會在排序前收集文件。請謹慎使用。OpenSearch 會將此參數套用至處理請求的每個分片。盡可能讓 OpenSearch 自動執行提前終止。對於指向資料串流，且其後端索引橫跨多個資料層級的請求，請避免指定此參數。 | 不適用 |
| `timeout` | 字串 | 每個更新請求等待下列操作的時間：動態對應更新、等待作用中分片。 | 不適用 |
| `version` | 布林值 | 若為 `true`，會將文件版本作為命中結果的一部分傳回。 | 不適用 |
| `wait_for_active_shards` | 整數或字串或 NULL 或字串 | 繼續執行操作前必須處於作用中狀態的分片副本數量。設為 `all`，或不超過索引分片總數（`number_of_replicas+1`）的任何正整數。<br> 有效值為：<br> - `all`：等待所有分片處於作用中狀態。 | 不適用 |
| `wait_for_completion` | 布林值 | 若為 `true`，請求會封鎖直到操作完成。 | `true` |

<!-- spec_insert_end -->

**重要：** 在依查詢更新請求中使用 `_source`、`_source_includes` 或 `_source_excludes` 時，這些設定不僅會影響回應，也會影響更新指令碼可使用的欄位。如果某個欄位從 `_source` 中排除，且未在指令碼中明確處理，該欄位可能會在更新操作期間從文件中移除。若要保留排除的欄位，請確保指令碼會視需要讀取並重新指派這些欄位。
{: .important}

## 請求本文欄位

請求本文是選用的，但通常包含一個用於指定要更新哪些文件的查詢，以及一個用於定義更新邏輯的指令碼。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`query` | 物件 | 用於選取要更新之文件的查詢。若未指定，此操作會更新目標索引中的所有文件。如需查詢類型的更多資訊，請參閱 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/)。
`script` | 物件 | 在每個符合條件的文件上執行的指令碼。包含 `source` (指令碼程式碼)、`lang` (指令碼語言，通常為 `painless`)，以及選用的 `params` (傳遞給指令碼的參數)。指令碼可透過 `ctx._source` 存取文件，並透過設定 `ctx.op` 來控制操作。如需更多資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。
`slice` | 物件 | 手動指定切片 ID 與平行處理的最大切片數。包含 `id` (整數，切片編號) 與 `max` (整數，切片總數)。選用。
`max_docs` | 整數 | 要處理的最大文件數量。選用。
`conflicts` | 字串 | 當依查詢更新操作遇到版本衝突時的處理方式。設為 `proceed` 以繼續，或設為 `abort` 以停止。可在請求本文中指定，或作為查詢參數指定。選用。

## 指令碼操作

在更新指令碼中，您可以透過設定 `ctx.op` 來控制每個文件的處理方式：

操作 | 說明
:--- | :---
不執行任何操作（`noop`） | 當指令碼判斷文件無需變更時，設定 `ctx.op = "noop"` 以跳過更新該文件。OpenSearch 會在回應的 `noops` 計數器中回報被跳過的文件。
刪除（`delete`） | 設定 `ctx.op = "delete"`，根據指令碼邏輯刪除文件。OpenSearch 會在回應的 `deleted` 計數器中回報被刪除的文件。

將 `ctx.op` 設定為任何其他值都會導致錯誤。修改 `ctx` 中 `ctx._source` 與 `ctx.op` 以外的其他欄位也會導致錯誤。

## 重新整理分片

指定 `refresh` 參數會在請求完成後重新整理依查詢更新操作所涉及的所有分片。此行為與 Update API 的 `refresh` 參數不同，後者只會重新整理接收更新請求的分片。Update by Query API 不支援 `refresh` 參數使用 `wait_for` 值。

## 以非同步方式執行依查詢更新

若要以非同步方式執行依查詢更新操作，請將 `wait_for_completion` 查詢參數設為 `false`。OpenSearch 會執行預先檢查、啟動請求，並傳回一個工作 ID，您可以用它來監控進度或取消操作。以非同步方式執行時，OpenSearch 會在 `.tasks/task/${taskId}` 建立一份以文件形式記錄的工作。工作完成後，請刪除該工作文件，讓 OpenSearch 能夠回收儲存空間。

## 等待作用中的分片

`wait_for_active_shards` 參數控制在處理請求之前必須有多少分片副本處於作用中狀態。`timeout` 參數控制每個寫入請求等待無法使用的分片變成可用的時間長度。這些參數的運作方式與 Bulk API 相同。由於 Update by Query 使用捲動式搜尋，您可以指定 `scroll` 參數，控制搜尋情境保持作用中的時間長度。預設捲動時間為 5 分鐘。

## 節流更新請求

若要控制依查詢更新操作發出更新批次的速率，請將 `requests_per_second` 設為任何正的十進位數。這會在每個批次之間加入等待時間，以節流速率。將 `requests_per_second` 設為 `-1` 可停用節流。

節流使用批次之間的等待時間，讓內部捲動請求可以取得一個將請求填充時間納入考量的逾時設定。填充時間是批次大小除以 `requests_per_second` 的結果與寫入所花費時間之間的差值。預設批次大小為 1,000，因此若 `requests_per_second` 設為 500：

```
target_time = 1,000 / 500 per second = 2 seconds
wait_time = target_time - write_time = 2 seconds - 0.5 seconds = 1.5 seconds
```

由於每個批次都是以單一大量請求的形式發出，較大的批次大小會導致 OpenSearch 建立許多請求，然後在開始下一個批次之前等待。這會造成不均勻的處理模式，出現高活動量時期之後接著閒置等待。

## 切片以進行平行處理

您可以使用切片在多個執行緒之間平行執行更新操作。這種方式會將更新操作劃分為獨立的區段，提升大規模更新的效能。

將 `slices` 設為 `auto` 可讓 OpenSearch 為大多數索引選擇合理的數量。使用自動切片或手動調整時，請考量下列因素：

- 當切片數量與分片數量相符時，查詢效能最佳。然而，對於具有許多分片 (500 個以上) 的索引，請使用較少的切片，以避免過度平行化造成的額外負擔導致效能下降。將切片數設定得高於分片數通常不會提升效率，反而會增加負擔。
- 更新效能會隨著可用資源與切片數量呈線性擴展。
- 查詢效能或更新效能何者主導執行時間，取決於正在更新的文件以及可用的叢集資源。

## 範例：更新所有文件而不變更來源

下列範例請求會更新索引中的所有文件，而不修改其來源。這對於套用新的對應屬性或其他對應變更非常有用：

<!-- spec_insert_start
component: example_code
rest: POST /products/_update_by_query?conflicts=proceed
-->
{% capture step1_rest %}
POST /products/_update_by_query?conflicts=proceed
{% endcapture %}

{% capture step1_python %}


response = client.update_by_query(
  index = "products",
  params = { "conflicts": "proceed" },
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：使用查詢篩選條件更新文件

下列範例請求會透過新增 10% 的折扣，僅更新電子產品：

<!-- spec_insert_start
component: example_code
rest: POST /products/_update_by_query
body: |
{
  "query": {
    "term": {
      "category": "electronics"
    }
  },
  "script": {
    "source": "ctx._source.discount = params.discountPercent",
    "lang": "painless",
    "params": {
      "discountPercent": 0.10
    }
  }
}
-->
{% capture step1_rest %}
POST /products/_update_by_query
{
  "query": {
    "term": {
      "category": "electronics"
    }
  },
  "script": {
    "source": "ctx._source.discount = params.discountPercent",
    "lang": "painless",
    "params": {
      "discountPercent": 0.1
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.update_by_query(
  index = "products",
  body =   {
    "query": {
      "term": {
        "category": "electronics"
      }
    },
    "script": {
      "source": "ctx._source.discount = params.discountPercent",
      "lang": "painless",
      "params": {
        "discountPercent": 0.1
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：遞增欄位值

下列範例請求會針對特定使用者的所有產品遞增 likes 計數器：

<!-- spec_insert_start
component: example_code
rest: POST /products/_update_by_query
body: |
{
  "query": {
    "term": {
      "user_id": "user1"
    }
  },
  "script": {
    "source": "ctx._source.likes++",
    "lang": "painless"
  }
}
-->
{% capture step1_rest %}
POST /products/_update_by_query
{
  "query": {
    "term": {
      "user_id": "user1"
    }
  },
  "script": {
    "source": "ctx._source.likes++",
    "lang": "painless"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.update_by_query(
  index = "products",
  body =   {
    "query": {
      "term": {
        "user_id": "user1"
      }
    },
    "script": {
      "source": "ctx._source.likes++",
      "lang": "painless"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：有條件地刪除文件

下列範例請求會刪除 likes 為零的缺貨產品：

<!-- spec_insert_start
component: example_code
rest: POST /products/_update_by_query
body: |
{
  "query": {
    "bool": {
      "must": [
        { "term": { "in_stock": false } },
        { "term": { "likes": 0 } }
      ]
    }
  },
  "script": {
    "source": "ctx.op = 'delete'",
    "lang": "painless"
  }
}
-->
{% capture step1_rest %}
POST /products/_update_by_query
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "in_stock": false
          }
        },
        {
          "term": {
            "likes": 0
          }
        }
      ]
    }
  },
  "script": {
    "source": "ctx.op = 'delete'",
    "lang": "painless"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.update_by_query(
  index = "products",
  body =   {
    "query": {
      "bool": {
        "must": [
          {
            "term": {
              "in_stock": false
            }
          },
          {
            "term": {
              "likes": 0
            }
          }
        ]
      }
    },
    "script": {
      "source": "ctx.op = 'delete'",
      "lang": "painless"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

<!-- vale off -->
## 範例：使用 noop 進行有條件的更新
<!-- vale on -->

下列範例請求只會針對價格高於 $100 的產品增加折扣，否則不執行任何操作：

<!-- spec_insert_start
component: example_code
rest: POST /products/_update_by_query
body: |
{
  "script": {
    "source": "if (ctx._source.price > 100) { ctx._source.discount = 0.15 } else { ctx.op = 'noop' }",
    "lang": "painless"
  }
}
-->
{% capture step1_rest %}
POST /products/_update_by_query
{
  "script": {
    "source": "if (ctx._source.price > 100) { ctx._source.discount = 0.15 } else { ctx.op = 'noop' }",
    "lang": "painless"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.update_by_query(
  index = "products",
  body =   {
    "script": {
      "source": "if (ctx._source.price > 100) { ctx._source.discount = 0.15 } else { ctx.op = 'noop' }",
      "lang": "painless"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：從多個索引更新

下列範例請求會跨多個索引更新文件：

<!-- spec_insert_start
component: example_code
rest: POST /products,inventory/_update_by_query
body: |
{
  "query": {
    "match_all": {}
  }
}
-->
{% capture step1_rest %}
POST /products,inventory/_update_by_query
{
  "query": {
    "match_all": {}
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.update_by_query(
  index = "products,inventory",
  body =   {
    "query": {
      "match_all": {}
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：使用路由進行目標式更新

下列範例請求會將更新操作限制在具有特定路由值的分片：

<!-- spec_insert_start
component: example_code
rest: POST /products/_update_by_query?routing=user1
body: |
{
  "query": {
    "term": {
      "user_id": "user1"
    }
  },
  "script": {
    "source": "ctx._source.likes += 5",
    "lang": "painless"
  }
}
-->
{% capture step1_rest %}
POST /products/_update_by_query?routing=user1
{
  "query": {
    "term": {
      "user_id": "user1"
    }
  },
  "script": {
    "source": "ctx._source.likes += 5",
    "lang": "painless"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.update_by_query(
  index = "products",
  params = { "routing": "user1" },
  body =   {
    "query": {
      "term": {
        "user_id": "user1"
      }
    },
    "script": {
      "source": "ctx._source.likes += 5",
      "lang": "painless"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：使用 scroll_size 控制批次大小

下列範例請求使用自訂的 100 份文件 scroll 批次大小：

<!-- spec_insert_start
component: example_code
rest: POST /products/_update_by_query?scroll_size=100
body: |
{
  "query": {
    "range": {
      "price": {
        "gte": 50
      }
    }
  },
  "script": {
    "source": "ctx._source.discount = 0.05",
    "lang": "painless"
  }
}
-->
{% capture step1_rest %}
POST /products/_update_by_query?scroll_size=100
{
  "query": {
    "range": {
      "price": {
        "gte": 50
      }
    }
  },
  "script": {
    "source": "ctx._source.discount = 0.05",
    "lang": "painless"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.update_by_query(
  index = "products",
  params = { "scroll_size": "100" },
  body =   {
    "query": {
      "range": {
        "price": {
          "gte": 50
        }
      }
    },
    "script": {
      "source": "ctx._source.discount = 0.05",
      "lang": "painless"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：手動切片以進行平行處理

下列範例請求會手動將更新操作分成兩個切片以進行平行處理：

<!-- spec_insert_start
component: example_code
rest: POST /products/_update_by_query
body: |
{
  "slice": {
    "id": 0,
    "max": 2
  },
  "script": {
    "source": "ctx._source.discount = 0.20",
    "lang": "painless"
  }
}
-->
{% capture step1_rest %}
POST /products/_update_by_query
{
  "slice": {
    "id": 0,
    "max": 2
  },
  "script": {
    "source": "ctx._source.discount = 0.20",
    "lang": "painless"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.update_by_query(
  index = "products",
  body =   {
    "slice": {
      "id": 0,
      "max": 2
    },
    "script": {
      "source": "ctx._source.discount = 0.20",
      "lang": "painless"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

在另一個請求中，處理第二個切片：

<!-- spec_insert_start
component: example_code
rest: POST /products/_update_by_query
body: |
{
  "slice": {
    "id": 1,
    "max": 2
  },
  "script": {
    "source": "ctx._source.discount = 0.20",
    "lang": "painless"
  }
}
-->
{% capture step1_rest %}
POST /products/_update_by_query
{
  "slice": {
    "id": 1,
    "max": 2
  },
  "script": {
    "source": "ctx._source.discount = 0.20",
    "lang": "painless"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.update_by_query(
  index = "products",
  body =   {
    "slice": {
      "id": 1,
      "max": 2
    },
    "script": {
      "source": "ctx._source.discount = 0.20",
      "lang": "painless"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：自動切片

下列範例請求使用自動切片，將更新作業平行化為 5 個切片執行：

<!-- spec_insert_start
component: example_code
rest: POST /products/_update_by_query?slices=5&refresh=true
body: |
{
  "script": {
    "source": "ctx._source.discount = 0.25",
    "lang": "painless"
  }
}
-->
{% capture step1_rest %}
POST /products/_update_by_query?slices=5&refresh=true
{
  "script": {
    "source": "ctx._source.discount = 0.25",
    "lang": "painless"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.update_by_query(
  index = "products",
  params = { "slices": "5", "refresh": "true" },
  body =   {
    "script": {
      "source": "ctx._source.discount = 0.25",
      "lang": "painless"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要讓 OpenSearch 自動判斷最佳切片數量，請使用 `slices=auto`：

<!-- spec_insert_start
component: example_code
rest: POST /products/_update_by_query?slices=auto
body: |
{
  "query": {
    "term": {
      "category": "furniture"
    }
  },
  "script": {
    "source": "ctx._source.discount = 0.30",
    "lang": "painless"
  }
}
-->
{% capture step1_rest %}
POST /products/_update_by_query?slices=auto
{
  "query": {
    "term": {
      "category": "furniture"
    }
  },
  "script": {
    "source": "ctx._source.discount = 0.30",
    "lang": "painless"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.update_by_query(
  index = "products",
  params = { "slices": "auto" },
  body =   {
    "query": {
      "term": {
        "category": "furniture"
      }
    },
    "script": {
      "source": "ctx._source.discount = 0.30",
      "lang": "painless"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

下列範例回應顯示一次成功的依查詢更新作業，共更新了 8 份文件：

```json
{
  "took": 39,
  "timed_out": false,
  "total": 8,
  "updated": 8,
  "deleted": 0,
  "batches": 1,
  "version_conflicts": 0,
  "noops": 0,
  "retries": {
    "bulk": 0,
    "search": 0
  },
  "throttled_millis": 0,
  "requests_per_second": -1.0,
  "throttled_until_millis": 0,
  "failures": []
}
```

當指令碼使用條件式 `noop` 作業時，回應會包含 `noops` 計數，顯示有多少文件被略過：

```json
{
  "took": 55,
  "timed_out": false,
  "total": 8,
  "updated": 4,
  "deleted": 0,
  "batches": 1,
  "version_conflicts": 0,
  "noops": 4,
  "retries": {
    "bulk": 0,
    "search": 0
  },
  "throttled_millis": 0,
  "requests_per_second": -1.0,
  "throttled_until_millis": 0,
  "failures": []
}
```

當使用手動切片時，回應會包含 `slice_id` 欄位，指出處理的是哪一個切片：

```json
{
  "took": 12,
  "timed_out": false,
  "slice_id": 0,
  "total": 4,
  "updated": 4,
  "deleted": 0,
  "batches": 1,
  "version_conflicts": 0,
  "noops": 0,
  "retries": {
    "bulk": 0,
    "search": 0
  },
  "throttled_millis": 0,
  "requests_per_second": -1.0,
  "throttled_until_millis": 0,
  "failures": []
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`took` | 整數 | 整個作業從開始到結束所花費的時間，單位為毫秒。
`timed_out` | 布林值 | 依查詢更新作業期間執行的任何請求是否逾時。當設為 `true` 時，已成功完成的更新仍會保存，不會復原。
`total` | 整數 | 成功處理的文件總數。
`updated` | 整數 | 成功更新的文件數。
`deleted` | 整數 | 刪除的文件數。當指令碼設定 `ctx.op = "delete"` 時會發生此情況。
`batches` | 整數 | 依查詢更新作業處理的捲動批次數。
`version_conflicts` | 整數 | 依查詢更新作業遇到的版本衝突數。當文件在建立快照與處理更新作業之間發生變更時，就會發生此情況。
`noops` | 整數 | 因指令碼設定 `ctx.op = "noop"` 而被忽略的文件數。與依查詢刪除不同，當指令碼有條件地略過更新時，此欄位可能包含非零值。
`retries` | 物件 | 依查詢更新作業嘗試的重試次數。包含 `bulk` (大量操作動作重試次數) 與 `search` (搜尋動作重試次數)。
`throttled_millis` | 整數 | 為符合 `requests_per_second` 而對請求進行節流的時間，單位為毫秒。
`requests_per_second` | 浮點數 | 依查詢更新作業期間每秒實際執行的請求數。
`throttled_until_millis` | 整數 | 下一個被節流的請求將執行前的等待時間，單位為毫秒。在已完成的依查詢更新回應中一律為 0。此欄位僅在使用 Tasks API 監視進行中的作業時才有意義，此時它表示下一個被節流的請求將執行的時間。
`slice_id` | 整數 | 此回應的切片編號。僅在使用手動切片時出現。指出此回應代表作業的哪一個切片。
`slices` | 陣列 | 使用自動切片並指定特定數量時的切片結果陣列。每個元素包含與主要回應相同的回應欄位，顯示該個別切片的結果。
`failures` | 陣列 | 作業期間發生任何無法復原的錯誤時的失敗陣列。若此陣列不為空，表示請求因這些失敗而中止。依查詢更新是以批次方式實作，任何失敗都會導致整個程序中止，但目前批次中的所有失敗都會收集在此陣列中。您可以將 `conflicts` 參數設為 `proceed`，以防止作業在發生版本衝突時中止。

## 管理依查詢更新任務

當您透過設定 `wait_for_completion=false` 以非同步方式執行依查詢更新作業時，OpenSearch 會傳回一個任務 ID，您可以用它來監視、修改或取消該作業。

### 擷取依查詢更新作業的狀態

若要擷取依查詢更新作業的狀態，請使用 [Tasks API]({{site.url}}{{site.baseurl}}/api-reference/tasks/)：

```json
GET _tasks?detailed=true&actions=*/update/byquery
```
{% include copy-curl.html %}

回應包含所有執行中的依查詢更新作業狀態。若要擷取特定任務的狀態，請使用任務 ID：

```json
GET _tasks/<task_id>
```
{% include copy-curl.html %}

回應包含作業進度的詳細資訊：

```json
{
  "nodes": {
    "node_id": {
      "tasks": {
        "task_id": {
          "status": {
            "total": 1000,
            "updated": 450,
            "created": 0,
            "deleted": 0,
            "batches": 5,
            "version_conflicts": 0,
            "noops": 0,
            "retries": 0,
            "throttled_millis": 0
          }
        }
      }
    }
  }
}
```

`total` 欄位代表依查詢更新作業預期執行的作業總數。您可以將 `updated`、`deleted` 與 `noops` 欄位相加，並將總和與 `total` 欄位比較，以估算進度。當總和等於 `total` 欄位時，作業即完成。

### 變更執行中作業的節流設定

若要變更執行中依查詢更新作業的節流設定，請使用 Rethrottle Task API 並指定工作 ID：

```json
POST _update_by_query/<task_id>/_rethrottle?requests_per_second=100
```
{% include copy-curl.html %}

將 `requests_per_second` 設為任何正的十進位數值，或設為 `-1` 以停用節流。提高作業速度的節流調整會立即生效。降低作業速度的節流調整會在目前批次完成後生效，以避免捲動逾時。

### 取消依查詢更新作業

若要取消執行中的依查詢更新作業，請使用工作取消 API：

```json
POST _tasks/<task_id>/_cancel
```
{% include copy-curl.html %}

取消作業應會迅速完成，但可能需要幾秒鐘。Tasks API 會持續列出依查詢更新工作，直到該工作確認已被取消並自行終止。當您取消使用切片的依查詢更新作業時，OpenSearch 會取消每個子請求。

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`indices:data/write/update/byquery`。
