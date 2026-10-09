---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "特徵工程"
nav_order: 40
parent: Learning to Rank
grand_parent: Optimizing search quality
has_children: false
---

# 特徵工程

以下各節說明在開發學習排序 (LTR) 解決方案時可能遇到的常見特徵工程工作。

## 取得原始詞彙統計資料

許多 LTR 解決方案在訓練時會使用原始詞彙統計資料，例如：
- **總詞彙頻率 (`raw_ttf`)：**某個詞彙在整個索引中出現的總次數。
- **文件頻率 (`raw_df`)：**某個詞彙出現的文件數量。
- **詞彙頻率 (`raw_tf`)：**某個詞彙在特定文件中出現的次數。
- **Classic IDF (`classic_idf`)：**反向文件頻率 (IDF) 計算 `log((NUM_DOCS+1)/(raw_df+1)) + 1`。

Learning to Rank 外掛程式提供 `match_explorer` 查詢原語，可為您擷取這些統計資料，如下列範例所示：

```json
POST tmdb/_search
{
    "query": {
        "match_explorer": {
            "type": "max_raw_df",
            "query": {
                "match": {
                    "title": "rambo rocky"
                }
            }
        }
    }
}
```
{% include copy-curl.html %}

此查詢會傳回詞彙 `rambo ` 與 `rocky` 之間最高的文件頻率。

您可以對這些統計資料使用 `max`、`min`、`sum` 和 `stddev` 等運算，以取得所需的資訊。

### 詞彙位置統計資料

您可以在 `type` 前面加上所需的運算 (`min`、`max`、`avg`)，以計算跨詞彙位置的對應統計資料。如果文件中不存在這些詞彙，則結果將為 `0`。

可用的統計資料包括：

- `min_raw_tp` (最小原始詞彙位置)：此統計資料會找出任何搜尋詞彙在文件中最早出現的位置。例如，使用查詢 `dance monkey` 時，如果 `dance` 出現在位置 [2, 5, 9]，而 `monkey` 出現在 [1, 4]，則最小值為 1。
- `max_raw_tp` (最大原始詞彙位置)：此統計資料會找出任何搜尋詞彙在文件中最晚出現的位置。以上述範例而言，最大值為 9。
- `avg_raw_tp` (平均原始詞彙位置)：此統計資料會計算任何查詢詞彙的平均詞彙位置。以上述範例而言，`dance` 的平均值為 5.33 [(2+5+9)/3)]，`monkey` 的平均值為 2.5 [(1+4)/2]，整體平均值為 3.91。
- `unique_terms_count`：提供查詢中不重複搜尋詞彙的數量。

## 文件專屬特徵

在開發 LTR 解決方案時，您可能需要納入文件專屬的特徵，而非查詢與文件之間關係的特徵。這些文件專屬特徵可包括與熱門程度或時效性相關的指標。

`function_score` 查詢提供擷取這些文件專屬特徵的功能。下列範例查詢示範如何使用它將 `vote_average` 欄位納入為特徵：

```json
{
    "query": {
        "function_score": {
            "functions": [{
                "field_value_factor": {
                    "field": "vote_average",
                    "missing": 0
                }
            }],
            "query": {
                "match_all": {}
            }
        }
    }
}
```
{% include copy-curl.html %}

在此範例中，查詢的分數由 `vote_average` 欄位的值決定，該值可以是文件熱門程度或品質的衡量指標。

## 索引漂移

在使用定期更新的索引時，務必考量您觀察到的趨勢與模式可能不會隨時間保持不變。隨著使用者行為、內容及其他因素的變化，您的索引可能會發生漂移。例如，在電子商務商店中，您可能會發現涼鞋在夏季很受歡迎，但在冬季幾乎找不到。同樣地，在某個期間內驅動購買或互動的特徵，在另一個期間可能就不再那麼重要。

## 後續步驟

了解[記錄特徵分數]({{site.url}}{{site.baseurl}}/search-plugins/ltr/logging-features/)。
