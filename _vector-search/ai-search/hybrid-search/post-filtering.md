---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用後置篩選的混合搜尋"
parent: Hybrid search
grand_parent: AI search
has_children: false
nav_order: 40
---

# 使用後置篩選的混合搜尋
**於 2.13 版推出**
{: .label .label-purple }

您可以在查詢中提供 `post_filter` 參數，對混合搜尋結果執行後置篩選。

`post_filter` 子句會在擷取搜尋結果之後套用。後置篩選適合用來對搜尋結果套用額外的篩選條件，而不影響評分或結果的順序。

後置篩選不會影響彙總結果。
{: .note}

若要在查詢執行期間篩選所有子查詢，而不是篩選最終結果，請使用通用篩選。如需詳細資訊，請參閱[使用前置篩選的混合搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/pre-filtering/)。

## 範例：使用後置篩選的分面搜尋

後置篩選常用於分面搜尋，此類搜尋的 UI 會將彙總計數 (例如品牌、顏色和尺寸篩選條件) 與搜尋結果一併顯示。使用 `post_filter` 可讓彙總計數以未篩選的完整查詢為依據，同時只篩選顯示的命中結果。

假設有一個包含產品文件的索引：

```json
{
  "name": "Nike Air Max",
  "brand": "Nike",
  "color": "Red",
  "size": 10,
  "price": 120,
  "category": "Running Shoes"
}
```

使用者搜尋「running shoes」，應用程式建構的查詢包含品牌、顏色和尺寸的彙總：

```json
POST /products/_search
{
  "query": {
    "match": {
      "category": "running shoes"
    }
  },
  "aggs": {
    "brands": {
      "terms": { "field": "brand.keyword" }
    },
    "colors": {
      "terms": { "field": "color.keyword" }
    },
    "sizes": {
      "terms": { "field": "size" }
    }
  }
}
```
{% include copy-curl.html %}

回應會傳回所有品牌的命中結果：

```
Nike Air Max
Nike Pegasus
Adidas Adizero
Puma Velocity
...
```

回應也會傳回彙總，其中包含每個品牌、顏色和尺寸的計數：

```
Brands:  Nike (120), Adidas (80), Puma (45)
Colors:  Black (90), White (70), Red (55)
Sizes:   8 (40), 9 (60), 10 (85)
```

彙總通常會以分面篩選的形式顯示在 UI 中。當使用者選取特定品牌 (例如 `Nike`) 來篩選結果時，使用前置篩選會在計算彙總之前排除非 Nike 的文件，導致其他品牌從分面計數中消失。

使用 `post_filter` 時，查詢和彙總會在完整結果集上執行。篩選只會套用至顯示的命中結果：

```json
POST /products/_search
{
  "query": {
    "match": {
      "category": "running shoes"
    }
  },
  "aggs": {
    "brands": {
      "terms": { "field": "brand.keyword" }
    },
    "colors": {
      "terms": { "field": "color.keyword" }
    }
  },
  "post_filter": {
    "term": { "brand.keyword": "Nike" }
  }
}
```
{% include copy-curl.html %}

命中結果只包含 Nike 產品，但彙總仍反映未篩選的完整查詢：

```
Brands:  Nike (120), Adidas (80), Puma (45)
Colors:  Black (90), White (70), Red (55)
```

所有品牌選項仍會顯示在分面中，讓使用者可以切換品牌或比較計數，而不需移除篩選條件。

## 後置篩選對搜尋結果和評分的影響

後置篩選可能會大幅改變最終搜尋結果和文件分數。請考慮下列情境。

### 單一查詢情境

假設有一個查詢會傳回下列結果：
- 正規化前的查詢結果：`[d2: 5.0, d4: 3.0, d1: 2.0]`
- 正規化分數：`[d2: 1.0, d4: 0.33, d1: 0.0]`

對初始查詢結果套用後置篩選後，結果如下：
- 後置篩選相符項目 `[d2, d4]`
- 產生的分數：`[d2: 1.0, d4: 0.0]`

請注意，套用後置篩選後，文件 `d4` 的分數如何從 `0.33` 變成 `0.0`。

### 多重查詢情境

假設有一個包含兩個子查詢的查詢：
- 查詢 1 結果：`[d2: 5.0, d4: 3.0, d1: 2.0]`
- 查詢 2 結果：`[d1: 1.0, d5: 0.5, d4: 0.25]`
- 正規化分數：
  - 查詢 1：`[d2: 1.0, d4: 0.33, d1: 0.0]`
  - 查詢 2：`[d1: 1.0, d5: 0.33, d4: 0.0]`
- 合併的初始分數：`[d2: 1.0, d1: 0.5, d5: 0.33, d4: 0.165]`

對初始查詢結果套用後置篩選後，結果如下：
- 後置篩選相符項目 `[d2, d4]`
- 產生的分數：
  - 查詢 1：`[d2: 5.0, d4: 3.0]`
  - 查詢 2：`[d4: 0.25]`
- 正規化分數：
  - 查詢 1：`[d2: 1.0, d4: 0.0]`
  - 查詢 2：`[d4: 1.0]`
- 合併的最終分數：`[d2: 1.0, d4: 0.5]`

請注意：
- 文件 `d2` 的分數維持不變。
- 文件 `d4` 的分數已變更。
