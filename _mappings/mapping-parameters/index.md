---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "對應參數"
nav_order: 100
has_children: true
has_toc: false
redirect_from:
  - /field-types/mapping-parameters/
  - /field-types/mapping-parameters/index/
  - /mappings/mapping-parameters/
---

# 對應參數

對應參數用於設定索引欄位的行為。如需參數的使用案例，請參閱各對應參數的頁面。

下表列出 OpenSearch 對應參數。

參數 | 說明
:--- | :---
[`analyzer`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/analyzer/) | 指定在編製索引或搜尋文字欄位時，用於文字分析的分析器。除非由 search_analyzer 覆寫，否則此分析器會同時處理編製索引時與搜尋時的分析。
[`boost`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/boost/) | 對欄位貢獻的分數套用乘數，以提高或降低搜尋查詢期間欄位的相關性分數。
[`coerce`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/coerce/) | 控制 OpenSearch 是否在編製索引期間嘗試正規化並轉換值，以符合欄位的資料類型（例如，將字串轉換為數字，或將浮點數截斷為整數）。
[`copy_to`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/copy-to/) | 將多個欄位的值複製到群組欄位，之後即可將其當作單一欄位查詢，而不修改原始 `_source`。
[`disable_objects`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/disable-objects/) | 控制含有點號的欄位名稱是展開為巢狀物件結構，還是視為字面上的扁平欄位識別字，以確保指標與分析工作負載的匯入行為具有確定性。
[`doc_values`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/doc-values/) | 控制是否在編製索引時建立儲存於磁碟上的欄式資料結構，以支援快速排序、彙總及指令碼中的欄位存取。
[`dynamic`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/dynamic/) | 指定是否可將新偵測到的欄位動態新增至對應（選項包括 true、false、strict、strict_allow_templates 和 false_allow_templates）。
[`eager_global_ordinals`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/eager_global_ordinals/) | 控制何時為欄位建立全域序數；預先載入會在索引重新整理期間計算全域序數，而非在查詢執行期間計算，以提升彙總與排序效能。
[`enabled`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/enabled/) | 控制 OpenSearch 是否解析欄位內容並為其編製索引；設為 false 時，欄位會儲存在 `_source` 中，但無法搜尋。
[`fielddata`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/field-data/) | 允許將 `text` 欄位中經過分析的詞元載入記憶體，以供排序、彙總及指令碼使用。由於記憶體成本高，預設為停用。
[`fields`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/fields/) | 透過定義採用其他對應的額外子欄位（例如，不同的資料類型或分析器），允許以多種方式為同一欄位編製索引，以支援不同的搜尋與彙總需求。
[`format`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/format/) | 指定日期欄位在編製索引期間可接受的內建日期格式，以確保正確解析與儲存日期值。
[`ignore_above`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/ignore-above/) | 限制已編製索引字串的字元數上限；超過門檻的值會被儲存，但不會編製索引，以避免索引膨脹。
[`ignore_malformed`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/ignore-malformed/) | 指示索引引擎忽略不符合欄位預期格式的值，即使部分欄位含有無法解析的資料，仍會儲存文件。
[`index`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/index-parameter/) | 控制欄位是否包含在倒排索引中；設為 false 時，欄位會被儲存，但無法搜尋（除非已啟用 doc_values）。
[`index_options`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/index-options/) | 控制文字欄位在倒排索引中儲存的詳細程度（選項包括 `docs`、`freqs`、`positions` 和 `offsets`），進而影響索引大小，以及評分、片語比對和醒目提示的功能。
[`index_phrases`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/index-phrases/) | 決定是否額外處理欄位的文字，以產生片語詞元（雙詞組），藉此提升片語查詢的效能與準確度，但會增加索引大小。
[`index_prefixes`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/index-prefixes/) | 為文字欄位中詞彙的開頭部分產生額外的索引項目，以大幅提升自動完成或隨輸入即搜尋等前綴查詢的效能。
[`meta`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/meta/) | 允許您將中繼資料附加至對應定義，並與對應一同儲存，作為背景資訊，而不影響編製索引或搜尋作業。
[`normalizer`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/normalizer/) | 為 keyword 欄位定義自訂的正規化程序，使用詞元篩選器將整個欄位值轉換為單一詞元，同時保持 `_source` 不變。
[`norms`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/norms/) | 控制是否為欄位計算並儲存正規化因子，以調整相關性評分；儲存這些因子會增加索引大小與記憶體用量。
[`null_value`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/null-value/) | 在編製索引期間，以預先定義的替代值取代明確指定的 `null` 值，允許對原本為 null 的欄位進行查詢與彙總，而不修改文件的 `_source`。
[`position_increment_gap`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/position-increment-gap/) | 定義編製索引期間多值欄位的詞元之間的位置距離，影響 match_phrase 與 span 查詢在跨多個值搜尋時的行為（預設為 100 個位置）。
[`properties`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/properties/) | 定義物件或文件根層級內欄位的結構與資料類型，作為所有對應定義的核心，以控制編製索引、儲存、搜尋行為及資料驗證。
[`search_analyzer`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/search-analyzer/) | 指定文字欄位在搜尋時使用的分析器，允許編製索引時使用的分析器與搜尋時使用的分析器不同，以更精確地控制詞彙比對。
[`similarity`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/similarity/) | 透過定義評分演算法，自訂搜尋期間文字欄位的相關性分數計算方式（選項包括 BM25 和 `boolean`）。
[`store`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/store/) | 決定是否應將欄位值與 `_source` 分開儲存，並允許使用搜尋請求中的 stored_fields 選項直接擷取。
[`term_vector`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/term-vector/) | 控制是否在編製索引期間為文字欄位儲存詞彙層級的資訊（詞頻、位置及字元位移），以供自訂評分與醒目提示等進階功能使用。

