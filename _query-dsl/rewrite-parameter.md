---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "重寫"
nav_order: 85
---

# Rewrite 參數

多詞元查詢（例如 `wildcard`、`prefix`、`regexp`、`fuzzy` 和 `range`）會在內部展開為一組詞元。`rewrite` 參數可讓您控制這些詞元展開的執行與評分方式。

當多詞元查詢展開為大量詞元時（例如 `prefix: "error*"` 符合數百個詞元），它們會在內部被轉換為 `term` 查詢。此過程可能有以下缺點：

* 超過 `indices.query.bool.max_clause_count` 限制（預設為 `1024`）。
* 影響符合文件的分數計算方式。
* 依所使用的 rewrite 方法而影響記憶體與延遲。

`rewrite` 參數可讓您控制多詞元查詢在內部的行為。

| 模式                        | 分數                                 | 效能 | 備註                                         |
| --------------------------- | -------------------------------------- | ----------- | --------------------------------------------- |
| `constant_score`            | 所有符合項目分數相同             | 最佳        | 預設模式，適合篩選用途               |
| `scoring_boolean`           | 以 TF/IDF 為基礎                           | 中等    | 完整相關性評分                        |
| `constant_score_boolean`    | 分數相同但具有布林結構 | 中等    | 搭配 `must_not` 或 `minimum_should_match` 使用 |
| `top_terms_N`               | 前 N 個詞元使用 TF/IDF                  | 高效   | 截斷展開                           |
| `top_terms_boost_N`         | 靜態加權值                          | 快速        | 精確度較低                                 |
| `top_terms_blended_freqs_N` | 混合分數                          | 均衡    | 評分與效能之間的最佳權衡              |


## 可用的 rewrite 方法

下表摘要說明可用的 rewrite 方法。

| Rewrite 方法 | 說明 |
| [`constant_score`](#constant-score) | （預設）所有展開的詞元會作為單一單位一起評估，並為每個符合項目指派相同分數。符合的文件不會個別評分，因此在篩選使用情境中非常高效。 |
| [`scoring_boolean`](#scoring-boolean) | 將查詢拆解為布林 `should` 子句，每個符合項目各有一個 term 查詢。每個結果會依相關性個別評分。 |
| [`constant_score_boolean`](#constant-score-boolean) | 與 `scoring_boolean` 類似，但所有文件都會收到固定分數，不論詞元頻率為何。保留布林結構但不使用 TF/IDF 加權。 |
| [`top_terms_N`](#top-terms-n) | 將評分與執行限制在頻率最高的 N 個詞元。減少資源用量並防止子句過載。 |
| [`top_terms_boost_N`](#top-terms-boost-n) | 與 `top_terms_N` 類似，但使用靜態加權而非完整評分。以簡化的相關性提供效能改善。 |
| [`top_terms_blended_freqs_N`](#top-terms-blended-frequencies-n) | 選取前 N 個符合的詞元，並平均其文件頻率以進行評分。在不造成詞元全面爆炸的情況下產生均衡的分數。 |

## 布林型 rewrite 的限制

所有布林型 rewrite（例如 `scoring_boolean`、`constant_score_boolean` 和 `top_terms_*`）都受到下列索引的動態[叢集設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/cluster-settings-for-indexes/#dynamic-settings)約束：

```json
indices.query.bool.max_clause_count
```

此設定控制允許的布林 `should` 子句數量上限（預設為 `1024`）。如果您的查詢展開後的子句數量超過此限制，將會被拒絕，並以 HTTP 400 Bad Request 回應傳回 `too_many_clauses` 錯誤。同樣地，如果您的查詢 _及其所有子查詢累計_ 展開後的子句總數超過此限制，也會被拒絕，並以 HTTP 400 Bad Request 回應傳回 `too_many_nested_clauses` 錯誤。

例如，像 "error*" 這樣的萬用字元可能會展開為數百或數千個符合的詞元，其中可能包括 "error"、"errors"、"error_log"、"error404" 等。每個詞元都會變成獨立的 `term` 查詢。如果詞元數量超過 `indices.query.bool.max_clause_count` 限制，查詢就會失敗：

```json
POST /logs/_search
{
  "query": {
    "wildcard": {
      "message": {
        "value": "error*",
        "rewrite": "scoring_boolean"
      }
    }
  }
}
```
{% include copy-curl.html %}

查詢會在內部展開如下：

```json
{
  "bool": {
    "should": [
      { "term": { "message": "error" } },
      { "term": { "message": "errors" } },
      { "term": { "message": "error_log" } },
      { "term": { "message": "error404" } },
      ...
    ]
  }
}
```

## 固定分數

預設的 `constant_score` rewrite 方法會將所有展開的詞元包裝成單一查詢，並完全略過評分階段。此方法具有以下特性：

* 將所有詞元符合項目以單一[位元陣列](https://en.wikipedia.org/wiki/Bit_array)查詢執行。
* 完全忽略評分；每個文件都會得到 `1.0` 的 `_score`。
* 最快的選項；適合篩選用途。

以下範例使用預設的 `constant_score` rewrite 方法執行 `wildcard` 查詢，以高效篩選 `message` 欄位中符合 `warning*` 模式的文件：

```json
POST /logs/_search
{
  "query": {
    "wildcard": {
      "message": {
        "value": "warning*"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 布林評分

`scoring_boolean` rewrite 方法會將展開的詞元拆分為多個獨立的 `term` 查詢，並在布林 `should` 子句下合併。此方法的運作方式如下：

* 將萬用字元展開為布林 `should` 子句內的個別 `term` 查詢。
* 每個文件的分數反映它符合多少詞元，以及這些詞元的頻率。

以下範例使用 `scoring_boolean` rewrite 組態：

```json
POST /logs/_search
{
  "query": {
    "wildcard": {
      "message": {
        "value": "warning*",
        "rewrite": "scoring_boolean"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 固定分數布林查詢

`constant_score_boolean` rewrite 方法使用與 `scoring_boolean` 相同的布林結構，但停用評分，因此在需要子句邏輯但不需要相關性排名時非常實用。此方法具有以下特性：

* 結構與 `scoring_boolean` 類似，但不對文件進行排名。
* 所有符合的文件都會得到相同分數。
* 保留布林子句的彈性，例如使用 `must_not`，但不進行排名。

以下範例查詢使用 `must_not` 布林子句：

```json
POST /logs/_search
{
  "query": {
    "bool": {
      "must_not": {
        "wildcard": {
          "message": {
            "value": "error*",
            "rewrite": "constant_score_boolean"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

此查詢會在內部展開如下：

```json
{
  "bool": {
    "must_not": {
      "bool": {
        "should": [
          { "term": { "message": "error" } },
          { "term": { "message": "errors" } },
          { "term": { "message": "error_log" } },
          ...
        ]
      }
    }
  }
}
```

## 前 N 個詞元

`top_terms_N` 方法是多種 rewrite 選項之一，旨在展開多詞元查詢時平衡評分精確度與效能。其運作方式如下：

* 只選取並評分最常符合的前 N 個詞元。
* 當您預期會有大量詞元展開並希望限制負載時非常實用。
* 其他有效詞元會被忽略以維持效能。

以下查詢使用 `top_terms_2` rewrite 方法，只對 `message` 欄位中符合 `warning*` 模式且最常出現的兩個詞元進行評分：

```json
POST /logs/_search
{
  "query": {
    "wildcard": {
      "message": {
        "value": "warning*",
        "rewrite": "top_terms_2"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 前 N 個詞元的加權值

`top_terms_boost_N` rewrite 方法會選取前 N 個符合的詞元，並套用靜態 `boost` 值，而不是計算完整的相關性分數。其運作方式如下：

* 與 `top_terms_N` 一樣，將展開限制在前 N 個詞元。
* 不計算 TF/IDF，而是為每個詞元指派預設的加權值。
* 以可預測的相關性權重提供更快的執行速度。

以下範例使用 `top_terms_boost_2` rewrite 參數：

```json
POST /logs/_search
{
  "query": {
    "wildcard": {
      "message": {
        "value": "warning*",
        "rewrite": "top_terms_boost_2"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 前 N 個詞元的混合頻率

`top_terms_blended_freqs_N` rewrite 方法會選取前 N 個符合的詞元，並混合其文件頻率以產生更均衡的相關性分數。此方法具有以下特性：

* 選取前 N 個符合的詞元，並對所有詞元套用混合頻率。
* 混合可讓頻率不同的詞元之間的評分更加平滑。
* 當您想要兼顧效能與真實評分時，這是很好的權衡選擇。

以下範例使用 `top_terms_blended_freqs_2` rewrite 參數：

```json
POST /logs/_search
{
  "query": {
    "wildcard": {
      "message": {
        "value": "warning*",
        "rewrite": "top_terms_blended_freqs_2"
      }
    }
  }
}
```
{% include copy-curl.html %}
