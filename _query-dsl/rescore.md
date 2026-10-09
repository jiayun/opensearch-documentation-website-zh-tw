---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "重新評分"
nav_order: 90
---

# 重新評分參數

`rescore` 參數僅重新排序初始查詢傳回的排名最高的文件，藉此提高搜尋精確度。重新評分不會將耗費運算資源的演算法套用至索引中的所有文件，而是將運算資源集中於排名靠前的較小結果範圍，使用第二種評分方法重新排名。

當您在搜尋請求中包含 `rescore` 參數時，OpenSearch 會依下列順序處理結果：

1. **初始搜尋**：針對所有相關文件執行主要查詢及任何後置篩選器。
2. **分片層級重新評分**：每個分片將重新評分演算法套用至其排名靠前的結果。
3. **最終協調**：協調節點合併所有分片中重新評分後的結果。

此方法可提高相關性，同時維持可接受的效能。

使用 `rescore` 參數時，請注意下列重要事項：

- 您無法在重新評分時使用明確指定的排序方式（依 `_score` 遞減排序除外）。如果您嘗試將自訂排序與重新評分查詢搭配使用，OpenSearch 會傳回錯誤。

- 實作分頁時，請在所有頁面維持相同的 `window_size`。在頁面之間變更視窗大小，可能導致使用者瀏覽搜尋結果時出現結果不一致的情況。

- 將重新評分與[混合查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/hybrid/#rescoring-hybrid-queries)搭配使用時，重新評分查詢會在正規化與合併之前，於分片層級獨立套用至每個子查詢的結果，而非套用至協調節點上最終合併的結果。

## 查詢重新評分

查詢重新評分會套用第二個查詢，以調整排名靠前的文件分數。您可以使用 `window_size` 參數（預設為 `10`）控制每個分片檢查的文件數量。

### 基本重新評分語法

```json
POST /_search
{
  "query": {
    "match": {
      "content": {
        "query": "OpenSearch query optimization",
        "operator": "or"
      }
    }
  },
  "rescore": {
    "window_size": 100,
    "query": {
      "rescore_query": {
        "match_phrase": {
          "content": {
            "query": "OpenSearch query optimization",
            "slop": 1
          }
        }
      },
      "query_weight": 0.8,
      "rescore_query_weight": 1.3
    }
  }
}
```
{% include copy-curl.html %}

### 重新評分參數

`rescore` 物件支援下列參數。

參數 | 類型 | 說明
--- | --- | ---
`window_size` | 整數 | 每個分片中要重新評分的排名靠前文件數量。預設為 `10`。
`query_weight` | 浮點數 | 套用至原始查詢分數的權重。預設為 `1.0`。
`rescore_query_weight` | 浮點數 | 套用至重新評分查詢分數的權重。預設為 `1.0`。
`score_mode` | 字串 | 合併原始查詢分數與重新評分查詢分數的方法。預設為 `total`。請參閱[分數合併模式](#score-combination-modes)。

### 分數合併模式

`score_mode` 參數決定 OpenSearch 如何合併原始分數與重新評分查詢分數。此參數接受下列值。

模式 | 說明 | 使用情境
--- | --- | ---
`total` | 將原始分數 + 重新評分分數相加 | 一般相關性改善（預設）
`multiply` | 將原始分數 × 重新評分分數相乘 | 適合搭配傳回 0 到 1 之間數值的函式查詢
`avg` | 計算兩個分數的平均值 | 當兩個分數同等重要時採用的平衡方法
`max` | 使用兩個分數中較高的分數 | 確保在任一查詢中獲得高分的文件具有良好排名
`min` | 使用兩個分數中較低的分數 | 要求文件在兩個查詢中都獲得高分的保守方法

## 多個重新評分階段

您可以串接多個重新評分作業，以套用越來越精細的排名演算法：

```json
POST /_search
{
  "query": {
    "match": {
      "title": {
        "query": "search engine technology",
        "operator": "or"
      }
    }
  },
  "rescore": [
    {
      "window_size": 200,
      "query": {
        "rescore_query": {
          "match_phrase": {
            "title": {
              "query": "search engine technology",
              "slop": 2
            }
          }
        },
        "query_weight": 0.6,
        "rescore_query_weight": 1.4
      }
    },
    {
      "window_size": 50,
      "query": {
        "score_mode": "multiply",
        "rescore_query": {
          "function_score": {
            "script_score": {
              "script": {
                "source": "Math.log10(doc['popularity'].value + 2)"
              }
            }
          }
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

在此多階段範例中：
1. **第一個重新評分階段**檢查每個分片中的 200 份文件，套用片語比對以提高相關性。
2. **第二個重新評分階段**取用第一階段排名前 50 的結果，並使用對數函式套用以熱門程度為依據的評分。

每個階段都會處理前一階段的結果，形成逐步調整的管線，讓耗費運算資源的作業僅針對最有潛力的候選文件執行。
