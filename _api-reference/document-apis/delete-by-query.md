---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "依查詢刪除"
parent: Document APIs
nav_order: 50
redirect_from:
 - /opensearch/rest-api/document-apis/delete-by-query/
---

# Delete by Query API
**於 1.0 版導入**
{: .label .label-purple}

Delete by Query API 會從索引中移除所有符合指定查詢的文件。此 API 讓您不必逐一刪除文件，而是能依據搜尋條件在單一請求中刪除多份文件。

請在下列情境使用此 API：

- 依日期範圍或其他條件，從時間序列索引中移除過期資料。
- 清理符合特定模式的測試資料或無效文件。
- 透過刪除超過一定時間的文件來實作資料保留政策。
- 刪除包含敏感資訊的文件。

當您提交依查詢刪除的請求時，OpenSearch 會在操作開始時建立索引的 scroll context，並使用內部版本控制（序號與主要分片任期）刪除符合的文件。此操作會依序執行多個搜尋請求以找出所有符合的文件，然後對每一批執行大量刪除請求。如果文件在擷取快照與刪除操作處理之間發生變更，就會發生版本衝突，除非您將 `conflicts` 參數設為 `proceed`，否則該文件的刪除會失敗。即使批次中後續操作失敗，已成功刪除的文件也不會復原。

OpenSearch 會以指數退避方式重試被拒絕的搜尋或大量請求，最多 10 次。若達到重試上限，操作會停止，並在回應中傳回所有失敗的請求。

**注意：** OpenSearch 無法使用此 API 刪除版本為 `0` 的文件。內部版本控制系統要求版本號必須大於 0，才能正確追蹤與處理刪除操作。
{: .note}

<!-- spec_insert_start
api: delete_by_query
component: endpoints
-->
## 端點
```json
POST /{index}/_delete_by_query
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: delete_by_query
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `index` | **必要** | 清單或字串 | 要搜尋的資料串流、索引與別名，以逗號分隔的清單。支援萬用字元（`*`）。若要搜尋所有資料串流或索引，請省略此參數，或使用 `*` 或 `_all`。 |

<!-- spec_insert_end -->

<!-- spec_insert_start
api: delete_by_query
component: query_parameters
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `_source` | 布林值或清單或字串 | 設為 `true` 或 `false` 以決定是否傳回 `_source` 欄位，或提供要傳回的欄位清單。 | N/A |
| `_source_excludes` | 清單 | 要從傳回的 `_source` 欄位中排除的欄位清單。 | N/A |
| `_source_includes` | 清單 | 要從 `_source` 欄位中擷取並傳回的欄位清單。 | N/A |
| `allow_no_indices` | 布林值 | 若為 `false`，當任何萬用字元運算式、索引別名或 `_all` 值只指向不存在或已關閉的索引時，請求會傳回錯誤。即使請求同時指向其他開啟的索引，此行為仍然適用。例如，指向 `foo*,bar*` 的請求，若某索引以 `foo` 開頭但沒有索引以 `bar` 開頭，則會傳回錯誤。 | N/A |
| `analyze_wildcard` | 布林值 | 若為 `true`，萬用字元與前置詞查詢會經過分析。 | `false` |
| `analyzer` | 字串 | 用於查詢字串的分析器。 | N/A |
| `conflicts` | 字串 | 依查詢刪除遇到版本衝突時的處理方式：`abort` 或 `proceed`。<br> 有效值為：<br> - `abort`：遇到版本衝突時中止操作。<br> - `proceed`：遇到版本衝突時繼續操作。 | N/A |
| `default_operator` | 字串 | 查詢字串查詢的預設運算子：`AND` 或 `OR`。<br> 有效值為：`and`、`AND`、`or` 與 `OR`。 | N/A |
| `df` | 字串 | 當查詢字串中未指定欄位前置詞時，所使用的預設欄位。 | N/A |
| `expand_wildcards` | 清單或字串 | 萬用字元模式可比對的索引類型。若請求可指向資料串流，此引數會決定萬用字元運算式是否符合隱藏的資料串流。支援以逗號分隔的值，例如 `open,hidden`。有效值為：`all`、`open`、`closed`、`hidden`、`none`。<br> 有效值為：<br> - `all`：比對所有索引，包括隱藏的索引。<br> - `closed`：比對已關閉且非隱藏的索引。<br> - `hidden`：比對隱藏的索引。必須與 `open`、`closed` 或兩者合併使用。<br> - `none`：不接受萬用字元運算式。<br> - `open`：比對開啟且非隱藏的索引。 | N/A |
| `from` | 整數 | 起始位移。 | `0` |
| `ignore_unavailable` | 布林值 | 若為 `false`，當請求指向不存在或已關閉的索引時會傳回錯誤。 | N/A |
| `lenient` | 布林值 | 若為 `true`，查詢字串中格式錯誤造成的查詢失敗（例如對數值欄位提供文字）將被忽略。 | N/A |
| `max_docs` | 整數 | 要處理的文件數上限。預設為所有文件。 | N/A |
| `preference` | 字串 | 指定應在其上執行操作的節點或分片。預設為隨機。 | `random` |
| `q` | 字串 | 使用 Lucene 查詢字串語法的查詢。 | N/A |
| `refresh` | 布林值或字串 | 若為 `true`，OpenSearch 會在請求完成後重新整理依查詢刪除所涉及的所有分片。<br> 有效值為：<br> - `false`：不重新整理受影響的分片。<br> - `true`：立即重新整理受影響的分片。<br> - `wait_for`：等待變更可見後再回覆。 | N/A |
| `request_cache` | 布林值 | 若為 `true`，此請求會使用請求快取。預設為索引層級的設定。 | N/A |
| `requests_per_second` | 浮點數 | 此請求的節流限制，單位為每秒子請求數。 | `0` |
| `routing` | 清單或字串 | 用於將操作路由至特定分片的自訂值。 | N/A |
| `scroll` | 字串 | 保留捲動搜尋內容的期間。 | N/A |
| `scroll_size` | 整數 | 驅動此操作的捲動請求大小。 | `100` |
| `search_timeout` | 字串 | 每個搜尋請求的明確逾時時間。預設為不逾時。 | N/A |
| `search_type` | 字串 | 搜尋操作的類型。可用選項：`query_then_fetch`、`dfs_query_then_fetch`。<br> 有效值為：<br> - `dfs_query_then_fetch`：使用所有分片的全域詞彙與文件頻率為文件評分。通常較慢但較準確。<br> - `query_then_fetch`：使用該分片的本機詞彙與文件頻率為文件評分。通常較快但較不準確。 | N/A |
| `size` | 整數 | 已淘汰，請改用 `max_docs`。 | N/A |
| `slices` | 整數或字串 | 此任務應分割成的切片數。<br> 有效值為：<br> - `auto`：自動決定切片數。 | N/A |
| `sort` | 清單 | 以逗號分隔的 <field>:<direction> 配對清單。 | N/A |
| `stats` | 清單 | 用於記錄與統計目的的請求特定 `tag`。 | N/A |
| `terminate_after` | 整數 | 每個分片可收集的文件數上限。若查詢達到此上限，OpenSearch 會提前終止查詢。OpenSearch 會在排序前收集文件。請謹慎使用。OpenSearch 會將此參數套用至處理該請求的每個分片。請盡可能讓 OpenSearch 自動執行提前終止。對於目標為橫跨多個資料層且具有後端索引的資料串流的請求，請避免指定此參數。 | N/A |
| `timeout` | 字串 | 每個刪除請求等待作用中分片的期間。 | N/A |
| `version` | 布林值 | 若為 `true`，會在命中結果中傳回文件版本。 | N/A |
| `wait_for_active_shards` | 整數或字串或 NULL 或字串 | 繼續操作前必須處於作用狀態的分片複本數。可設為 all，或任何不超過索引中分片總數的正整數（`number_of_replicas+1`）。<br> 有效值為：<br> - `all`：等待所有分片皆為作用中。 | N/A |
| `wait_for_completion` | 布林值 | 若為 `true`，請求會封鎖直到操作完成。 | `true` |

<!-- spec_insert_end -->


## 請求本文欄位

請求本文為選用，但通常會包含查詢，用以指定要刪除哪些文件。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`query` | 物件 | 用來選取要刪除之文件的查詢。若未指定，此操作會刪除目標索引中的所有文件。如需查詢類型的詳細資訊，請參閱 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/)。
`slice` | 物件 | 手動指定用於平行處理的分割 ID 與分割數上限。包含 `id` (整數，分割編號) 與 `max` (整數，分割總數)。選用。
`max_docs` | 整數 | 要處理的文件數上限。選用。

## 重新整理分片

指定 `refresh` 參數會在請求完成後，重新整理 delete by query 操作涉及的所有分片。此行為與 Delete Document API 的 `refresh` 參數不同，後者只會重新整理收到刪除請求的那個分片。Delete by Query API 不支援 `refresh` 參數使用 `wait_for` 值。

## 以非同步方式執行 delete by query

若要以非同步方式執行 delete by query 操作，請將 `wait_for_completion` 查詢參數設為 `false`。OpenSearch 會執行預先檢查、啟動請求，並傳回任務 ID，您可用來監控進度或取消操作。以非同步方式執行時，OpenSearch 會將任務的記錄建立為 `.tasks/task/${taskId}` 上的文件。任務完成後，請刪除該任務文件，讓 OpenSearch 回收空間。

## 等待作用中的分片

`wait_for_active_shards` 參數控制處理請求前必須有多少個分片複本處於作用中狀態。`timeout` 參數控制每個寫入請求等待無法使用之分片變為可用的時間長度。這些參數的運作方式與 Bulk API 中相同。由於 Delete by Query 使用捲動搜尋，您可以指定 `scroll` 參數來控制搜尋內容維持作用中的時間長度。預設的捲動時間為 5 分鐘。

## 節流刪除請求

若要控制 delete by query 發出批次刪除操作的速率，請將 `requests_per_second` 設為任意正十進位數。這會為每個批次加上等待時間，以節流該速率。將 `requests_per_second` 設為 `-1` 可停用節流。

節流會在批次之間使用等待時間，讓內部捲動請求能取得考量請求填補的逾時。填補時間是批次大小除以 `requests_per_second` 與寫入所花時間之間的差異。根據預設，批次大小為 1,000，因此若 `requests_per_second` 設為 500：

```
target_time = 1,000 / 500 per second = 2 seconds
wait_time = target_time - write_time = 2 seconds - 0.5 seconds = 1.5 seconds
```

由於每個批次都是以單一大量請求發出，批次大小過大會導致 OpenSearch 建立許多請求，然後在開始下一個批次前等待。這會造成處理模式不均，出現高活動期間後接著閒置等待的情況。

## 分割以進行平行處理

您可以使用分割，跨多個執行緒平行執行刪除操作。此做法會將刪除操作分成獨立的分段，提升大規模刪除的效能。

將 `slices` 設為 `auto` 可讓 OpenSearch 為大多數索引選擇合理的數值。使用自動分割或手動調整時，請考量下列因素：

- 當分割數與分片數相符時，可達到最佳查詢效能。不過，對於分片數眾多 (500 個以上) 的索引，請使用較少的分割，以避免過度平行化造成的額外負擔導致效能降低。將分割數設得高於分片數通常不會提升效率，反而會增加額外負擔。
- 刪除效能會隨分割數，在可用資源上呈線性擴展。
- 執行時間主要由查詢效能還是刪除效能主導，取決於要刪除的文件與可用的叢集資源。

## 範例：刪除符合查詢的文件

下列範例請求會從 `movies` 索引中刪除所有 `year` 欄位小於 2000 的文件：

<!-- spec_insert_start
component: example_code
rest: POST /movies/_delete_by_query
body: |
{
  "query": {
    "range": {
      "year": {
        "lt": 2000
      }
    }
  }
}
-->
{% capture step1_rest %}
POST /movies/_delete_by_query
{
  "query": {
    "range": {
      "year": {
        "lt": 2000
      }
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.delete_by_query(
  index = "movies",
  body =   {
    "query": {
      "range": {
        "year": {
          "lt": 2000
        }
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：設定為繼續處理的衝突刪除

下列範例請求會刪除符合查詢的文件，並在發生版本衝突時繼續處理：

<!-- spec_insert_start
component: example_code
rest: POST /movies/_delete_by_query?conflicts=proceed
body: |
{
  "query": {
    "match": {
      "status": "archived"
    }
  }
}
-->
{% capture step1_rest %}
POST /movies/_delete_by_query?conflicts=proceed
{
  "query": {
    "match": {
      "status": "archived"
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.delete_by_query(
  index = "movies",
  params = { "conflicts": "proceed" },
  body =   {
    "query": {
      "match": {
        "status": "archived"
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：從多個索引刪除

下列範例請求會從多個符合查詢的索引中刪除文件：

<!-- spec_insert_start
component: example_code
rest: POST /movies,tv-shows/_delete_by_query
body: |
{
  "query": {
    "match_all": {}
  }
}
-->
{% capture step1_rest %}
POST /movies,tv-shows/_delete_by_query
{
  "query": {
    "match_all": {}
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.delete_by_query(
  index = "movies,tv-shows",
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

## 範例：使用路由進行目標式刪除

下列範例請求會將刪除操作限制在具有特定路由值的分片：

<!-- spec_insert_start
component: example_code
rest: POST /movies/_delete_by_query?routing=user123
body: |
{
  "query": {
    "term": {
      "user_id": "user123"
    }
  }
}
-->
{% capture step1_rest %}
POST /movies/_delete_by_query?routing=user123
{
  "query": {
    "term": {
      "user_id": "user123"
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.delete_by_query(
  index = "movies",
  params = { "routing": "user123" },
  body =   {
    "query": {
      "term": {
        "user_id": "user123"
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：使用 scroll_size 控制批次大小

下列範例請求使用自訂的捲動批次大小 5,000 份文件：

<!-- spec_insert_start
component: example_code
rest: POST /movies/_delete_by_query?scroll_size=5000
body: |
{
  "query": {
    "term": {
      "genre": "documentary"
    }
  }
}
-->
{% capture step1_rest %}
POST /movies/_delete_by_query?scroll_size=5000
{
  "query": {
    "term": {
      "genre": "documentary"
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.delete_by_query(
  index = "movies",
  params = { "scroll_size": "5000" },
  body =   {
    "query": {
      "term": {
        "genre": "documentary"
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：手動切片以進行平行處理

下列範例請求手動將刪除操作分成兩個切片以進行平行處理：

<!-- spec_insert_start
component: example_code
rest: POST /movies/_delete_by_query
body: |
{
  "slice": {
    "id": 0,
    "max": 2
  },
  "query": {
    "range": {
      "rating": {
        "lt": 5
      }
    }
  }
}
-->
{% capture step1_rest %}
POST /movies/_delete_by_query
{
  "slice": {
    "id": 0,
    "max": 2
  },
  "query": {
    "range": {
      "rating": {
        "lt": 5
      }
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.delete_by_query(
  index = "movies",
  body =   {
    "slice": {
      "id": 0,
      "max": 2
    },
    "query": {
      "range": {
        "rating": {
          "lt": 5
        }
      }
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
rest: POST /movies/_delete_by_query
body: |
{
  "slice": {
    "id": 1,
    "max": 2
  },
  "query": {
    "range": {
      "rating": {
        "lt": 5
      }
    }
  }
}
-->
{% capture step1_rest %}
POST /movies/_delete_by_query
{
  "slice": {
    "id": 1,
    "max": 2
  },
  "query": {
    "range": {
      "rating": {
        "lt": 5
      }
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.delete_by_query(
  index = "movies",
  body =   {
    "slice": {
      "id": 1,
      "max": 2
    },
    "query": {
      "range": {
        "rating": {
          "lt": 5
        }
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：自動切片

下列範例請求使用自動切片，將刪除操作平行化為 5 個切片：

<!-- spec_insert_start
component: example_code
rest: POST /movies/_delete_by_query?slices=5&refresh=true
body: |
{
  "query": {
    "range": {
      "views": {
        "lt": 100
      }
    }
  }
}
-->
{% capture step1_rest %}
POST /movies/_delete_by_query?slices=5&refresh=true
{
  "query": {
    "range": {
      "views": {
        "lt": 100
      }
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.delete_by_query(
  index = "movies",
  params = { "slices": "5", "refresh": "true" },
  body =   {
    "query": {
      "range": {
        "views": {
          "lt": 100
        }
      }
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
rest: POST /movies/_delete_by_query?slices=auto
body: |
{
  "query": {
    "match": {
      "category": "test"
    }
  }
}
-->
{% capture step1_rest %}
POST /movies/_delete_by_query?slices=auto
{
  "query": {
    "match": {
      "category": "test"
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.delete_by_query(
  index = "movies",
  params = { "slices": "auto" },
  body =   {
    "query": {
      "match": {
        "category": "test"
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 範例回應

下列範例回應顯示成功的 delete by query 操作，共刪除了 8 份文件：

```json
{
  "took": 88,
  "timed_out": false,
  "total": 8,
  "deleted": 8,
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

使用手動切片時，回應包含 `slice_id` 欄位，指出處理的是哪個切片：

```json
{
  "took": 13,
  "timed_out": false,
  "slice_id": 0,
  "total": 9,
  "deleted": 9,
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

使用自動切片並指定切片數量時，回應包含 `slices` 陣列，顯示每個切片的結果：

```json
{
  "took": 52,
  "timed_out": false,
  "total": 9,
  "deleted": 9,
  "batches": 4,
  "version_conflicts": 0,
  "noops": 0,
  "retries": {
    "bulk": 0,
    "search": 0
  },
  "throttled_millis": 0,
  "requests_per_second": -1.0,
  "throttled_until_millis": 0,
  "slices": [
    {
      "slice_id": 0,
      "total": 3,
      "deleted": 3,
      "batches": 1,
      "version_conflicts": 0,
      "noops": 0,
      "retries": {
        "bulk": 0,
        "search": 0
      },
      "throttled_millis": 0,
      "requests_per_second": -1.0,
      "throttled_until_millis": 0
    },
    {
      "slice_id": 1,
      "total": 2,
      "deleted": 2,
      "batches": 1,
      "version_conflicts": 0,
      "noops": 0,
      "retries": {
        "bulk": 0,
        "search": 0
      },
      "throttled_millis": 0,
      "requests_per_second": -1.0,
      "throttled_until_millis": 0
    },
    {
      "slice_id": 2,
      "total": 0,
      "deleted": 0,
      "batches": 0,
      "version_conflicts": 0,
      "noops": 0,
      "retries": {
        "bulk": 0,
        "search": 0
      },
      "throttled_millis": 0,
      "requests_per_second": -1.0,
      "throttled_until_millis": 0
    },
    {
      "slice_id": 3,
      "total": 1,
      "deleted": 1,
      "batches": 1,
      "version_conflicts": 0,
      "noops": 0,
      "retries": {
        "bulk": 0,
        "search": 0
      },
      "throttled_millis": 0,
      "requests_per_second": -1.0,
      "throttled_until_millis": 0
    },
    {
      "slice_id": 4,
      "total": 3,
      "deleted": 3,
      "batches": 1,
      "version_conflicts": 0,
      "noops": 0,
      "retries": {
        "bulk": 0,
        "search": 0
      },
      "throttled_millis": 0,
      "requests_per_second": -1.0,
      "throttled_until_millis": 0
    }
  ],
  "failures": []
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`took` | 整數 | 整個操作從開始到結束所花的時間，單位為毫秒。
`timed_out` | 布林值 | delete by query 操作期間執行的任何請求是否逾時。設為 `true` 時，已成功完成的刪除仍會保留，不會復原。
`total` | 整數 | 成功處理的文件總數。
`deleted` | 整數 | 成功刪除的文件數。
`batches` | 整數 | delete by query 操作處理的捲動批次數。
`version_conflicts` | 整數 | delete by query 操作遇到的版本衝突數。當文件在擷取快照與處理刪除操作之間發生變更時，就會發生此情況。
`noops` | 整數 | 無操作請求的數量。此欄位在 delete by query 中一律傳回 0。它的存在是為了與 Update by Query 及 Reindex API 維持一致的回應結構。
`retries` | 物件 | delete by query 操作嘗試的重試次數。包含 `bulk` (大量操作重試次數) 與 `search` (搜尋操作重試次數)。
`throttled_millis` | 整數 | 為符合 `requests_per_second` 而對請求進行節流的時間，單位為毫秒。
`requests_per_second` | 浮點數 | delete by query 操作期間實際執行的每秒請求數。
`throttled_until_millis` | 整數 | 距離下一個被節流請求執行的時間，單位為毫秒。在已完成的 delete by query 回應中一律等於 0。此欄位僅在使用 Tasks API 監視進行中的操作時才有意義，此時它表示下一個被節流請求將執行的時間。
`slice_id` | 整數 | 此回應的切片編號。僅在使用手動切片時出現。表示此回應代表操作的哪個切片。
`slices` | 陣列 | 使用自動切片並指定數量時的切片結果陣列。每個元素包含與主要回應相同的回應欄位，顯示該個別切片的結果。
`failures` | 陣列 | 操作期間若發生任何無法復原的錯誤，則為失敗項目的陣列。若此陣列不為空，表示請求因這些失敗而中止。Delete by query 是以批次方式實作，任何失敗都會導致整個程序中止，但目前批次中的所有失敗都會收集在此陣列中。您可以將 `conflicts` 參數設為 `proceed`，以防止操作在發生版本衝突時中止。

## 管理依查詢刪除工作

當您透過設定 `wait_for_completion=false` 以非同步方式執行依查詢刪除操作時，OpenSearch 會傳回一個工作 ID，您可以使用該 ID 來監視、修改或取消該操作。

### 擷取依查詢刪除操作的狀態

若要擷取依查詢刪除操作的狀態，請使用 [Tasks API]({{site.url}}{{site.baseurl}}/api-reference/tasks/)：

```json
GET _tasks?detailed=true&actions=*/delete/byquery
```
{% include copy-curl.html %}

回應會包含所有執行中依查詢刪除操作的狀態。若要擷取特定工作的狀態，請使用工作 ID：

```json
GET _tasks/{task_id}
```
{% include copy-curl.html %}

回應會包含該操作進度的詳細資訊：

```json
{
  "nodes": {
    "node_id": {
      "tasks": {
        "task_id": {
          "status": {
            "total": 1000,
            "updated": 0,
            "created": 0,
            "deleted": 450,
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

`total` 欄位代表依查詢刪除操作預期執行的操作總數。您可以比較 `deleted` 欄位與 `total` 欄位來估算進度。當 `deleted` 等於 `total` 時，表示操作已完成。

### 變更執行中操作的節流

若要變更執行中依查詢刪除操作的節流，請使用 Rethrottle Task API 並搭配工作 ID：

```json
POST _delete_by_query/{task_id}/_rethrottle?requests_per_second=100
```
{% include copy-curl.html %}

將 `requests_per_second` 設為任何正的小數值，或將 `-1` 設為停用節流。加速操作的重新節流會立即生效。減慢操作的重新節流會在完成目前批次後生效，以避免捲動逾時。

### 取消依查詢刪除操作

若要取消執行中的依查詢刪除操作，請使用工作取消 API：

```json
POST _tasks/{task_id}/_cancel
```
{% include copy-curl.html %}

取消作業應會迅速完成，但可能需要幾秒鐘。Tasks API 會持續列出依查詢刪除工作，直到確認該工作已取消並自行終止為止。當您取消具有分割的依查詢刪除操作時，OpenSearch 會取消每個子請求。

## 必要權限

如果您使用 Security 外掛程式，請確定您具有適當的權限：`indices:data/write/delete/byquery`。
