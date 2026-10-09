---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "僅比對文字"
nav_order: 20
has_children: false
parent: String field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/match-only-text/
---

# 僅比對文字欄位類型
**於 2.12 版推出**
{: .label .label-purple }

`match_only_text` 欄位是 `text` 欄位的變體，專為全文搜尋所設計，適用於文件中詞元的評分與位置資訊不重要的情境。

`match_only_text` 欄位與 `text` 欄位有下列差異：

 - 省略儲存位置、頻率與正規化資訊（norms），降低儲存空間需求。
 - 停用評分，讓所有符合的文件都獲得固定的分數 1.0。
 - 支援所有查詢類型，但 interval 與 span 查詢除外。

當您需要優先考量高效率的全文搜尋，而非複雜的排名與位置查詢，同時又想最佳化儲存成本時，請選擇 `match_only_text` 欄位類型。使用 `match_only_text` 會建立明顯較小的索引，進而降低儲存成本，尤其是在大型資料集上。

當您需要快速找出包含特定詞元的文件，而不想負擔儲存頻率與位置的額外開銷時，請使用 `match_only_text` 欄位。`match_only_text` 欄位類型並非根據相關性排序結果，或執行依賴詞元鄰近度或順序的查詢（例如 interval 或 span 查詢）的最佳選擇。雖然此欄位類型確實支援詞組查詢，但其效能不如使用 `text` 欄位類型時來得高。如果您必須辨識確切的詞組或其文件中的位置，請改用 `text` 欄位類型。

## 範例

建立含有 `match_only_text` 欄位的對應：

```json
PUT movies
{
  "mappings" : {
    "properties" : {
      "title" : {
        "type" :  "match_only_text"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 參數

雖然 `match_only_text` 支援 `text` 欄位可用的大部分參數，但修改其中大多數參數可能適得其反。此欄位類型旨在簡單且有效率，盡量減少索引中儲存的資料，以最佳化儲存成本。因此，維持預設設定通常是最好的做法。任何超出分析器設定的修改，都可能重新引入額外開銷，並抵銷 `match_only_text` 的效率優勢。

下表列出 `match_text_only` 欄位可用的所有參數。

參數 | 說明
:--- | :---
`analyzer` | 要用於此欄位的分析器。根據預設，它會在索引時與搜尋時使用。若要在搜尋時覆寫它，請設定 `search_analyzer` 參數。預設為 `standard` 分析器，其使用以文法為基礎的斷詞，並以 [Unicode 文字分段](https://unicode.org/reports/tr29/) 演算法為基礎。
`boost` |  所有命中都會被指派分數 1，並乘以 `boost`，以產生查詢子句的最終分數。
`eager_global_ordinals` | 指定是否應在重新整理時預先載入全域序數。如果此欄位經常用於彙總，則應將此參數設為 `true`。預設為 `false`。
`fielddata` | 布林值，指定是否要存取已分析的詞元，以進行排序、彙總與指令碼。預設為 `false`。
`fielddata_frequency_filter` | JSON 物件，指定只將文件頻率介於 `min` 與 `max` 值之間（以絕對數字或百分比提供）的已分析詞元載入記憶體。頻率會依分段計算。參數：`min`、`max`、`min_segment_size`。預設為載入所有已分析的詞元。
`fields` | 若要以多種方式為同一個字串編製索引（例如同時作為 keyword 與 text），請提供 `fields` 參數。您可以指定欄位的其中一個版本用於搜尋，另一個版本用於排序與彙總。
`index` | 布林值，指定此欄位是否應可供搜尋。預設為 `true`。
`index_options` | 您無法修改此參數。
`index_phrases` | 不支援。
`index_prefixes` | 不支援。
`meta` | 接受此欄位的中繼資料。
`norms` | 正規化資訊已停用，且無法啟用。
`position_increment_gap` | 雖然位置已停用，但 `position_increment_gap` 用於詞組查詢時的行為與 `text` 欄位類似。這類查詢可能較慢，但仍可運作。
`similarity` | 設定相似度沒有任何影響。`match_only_text` 欄位類型不支援像 `more_like_this` 這類依賴相似度的查詢。若查詢依賴相似度，請使用 `keyword` 或 `text` 欄位。
`term_vector` | 支援詞元向量，但不建議使用，因為這與此欄位的主要目的（最佳化儲存空間）相違背。

## 將欄位從 `text` 遷移至 `match_only_text`

您可以使用 [Reindex API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/reindex/)，在目的地索引中更新正確的對應，將 `text` 欄位遷移至 `match_only_text`。

在下列範例中，`source` 索引包含類型為 `text` 的 `title` 欄位。

建立目的地索引，並將 `title` 欄位對應為 `text`：

```json
PUT destination
{
  "mappings" : {
    "properties" : {
      "title" : {
        "type" :  "match_only_text"
      }
    }
  }
}
```
{% include copy-curl.html %}

重新編製資料索引：

```json
POST _reindex
{
   "source": {
      "index":"source"
   },
   "dest": {
      "index":"destination"
   }
}
```
{% include copy-curl.html %}
