---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Wildcard
nav_order: 45
has_children: false
parent: String field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/wildcard/
---

# Wildcard 欄位類型
**於 2.15 版推出**
{: .label .label-purple }

`wildcard` 欄位是 `keyword` 欄位的一種變體，專為任意子字串與正規表示式比對而設計。

當您需要以前置萬用字元或任意子字串搜尋值時，例如非結構化的記錄行與電腦程式碼，請使用 `wildcard` 欄位。在 `keyword` 欄位上，這類搜尋必須掃描欄位中的每個詞元，隨著不同值數量增加，速度會變慢。在 `text` 欄位上，斷詞會將每個值拆解成單字，因此跨越單字邊界的子字串便無法比對。`wildcard` 欄位會直接為子字串本身編製索引，因此能直接支援這類搜尋。

`wildcard` 欄位類型的索引方式與 `keyword` 欄位類型不同。`keyword` 欄位會將原始欄位值寫入索引，而 `wildcard` 欄位類型則會將欄位值拆解成長度小於或等於 3 的子字串，並將這些子字串寫入索引。例如，字串 `test` 會被拆解成 `t`、`te`、`tes`、`e`、`es` 與 `est`。 

在搜尋時，系統會以查詢模式中所需的子字串對索引進行比對，產生候選文件，再依查詢中的模式加以篩選。例如，對於搜尋詞 `test`，OpenSearch 會對 `tes AND est` 執行索引搜尋。如果搜尋詞少於三個字元，OpenSearch 會使用長度為一或兩個字元的子字串。對每個符合的文件而言，如果來源值為 `test`，該文件就會出現在結果中。這樣可排除 `nikola tesla felt alternating current was best` 之類的誤判值。

一般而言，精確比對查詢（例如 [`term`]({{site.url}}{{site.baseurl}}/query-dsl/term/term/) 或 [`terms`]({{site.url}}{{site.baseurl}}/query-dsl/term/term/) 查詢）在 `wildcard` 欄位上的效果不如在 `keyword` 欄位上，而 [`wildcard`]({{site.url}}{{site.baseurl}}/query-dsl/term/wildcard/)、[`prefix`]({{site.url}}{{site.baseurl}}/query-dsl/term/prefix/) 與 [`regexp`]({{site.url}}{{site.baseurl}}/query-dsl/term/regexp/) 查詢在 `wildcard` 欄位上則有較佳的表現。
{: .tip}

Wildcard 欄位不支援醒目提示。
{: .note}

## 範例

建立一個包含 `wildcard` 欄位的對應：

```json
PUT logs
{
  "mappings" : {
    "properties" : {
      "log_line" : {
        "type" :  "wildcard"
      }
    }
  }
}
```
{% include copy-curl.html %}

所有對 wildcard 欄位的查詢都具有固定分數，通常為 `1`。若要變更分數，請在查詢中設定 `boost` 參數。欄位對應中的 `boost` 不會產生任何作用。
{: .note}

## 參數

下表列出 `wildcard` 欄位可用的所有參數。

| 參數 | 說明 | 預設值 | 可動態更新 |
| :--- | :--- | :--- | :--- |
| `copy_to` | 一或多個其他欄位的名稱，在編製索引時會將此欄位的值複製到這些欄位。 | 無 | 是 |
| `doc_values` | 布林值，指定是否應將欄位儲存在磁碟上，以便用於彙總、排序或指令碼。 | `true` | 否 |
| `fields` | 一或多個子欄位，使用不同的欄位類型為相同的值編製索引。使用子欄位可支援 `wildcard` 類型不支援的操作，例如在 `keyword` 子欄位上進行範圍查詢。 | 無 | 是 |
| `ignore_above` | 整數值，指定最大字串長度。較長的字串既不會編製索引，也不會寫入 doc values，因此不會符合任何查詢，也不會出現在彙總中。該值仍保留在 `_source` 中。 | `2147483647` | 是 |
| `meta` | 欄位的中繼資料。OpenSearch 會儲存此中繼資料並在對應中回傳，但不會使用它。 | 無 | 是 |
| [`normalizer`]({{site.url}}{{site.baseurl}}/analyzers/normalizers/) | 用於在編製索引與搜尋前處理值的正規化器。OpenSearch 會將其同時套用至索引值與查詢，doc values 儲存正規化後的形式，而 `_source` 則保留原始值。使用 `lowercase` 正規化器可對欄位執行不區分大小寫的比對。 | `default`（無正規化） | 否 |
| `null_value` | 用來取代 `null` 進行索引的值。請以字串指定；其他 JSON 類型會轉換為其字串形式。若未指定此參數，`null` 值會被視為遺漏，且 `exists` 查詢不會符合該文件。 | `null` | 否 |

## 儲存空間需求

`wildcard` 欄位比包含相同值的 `keyword` 欄位使用更多磁碟空間。兩種欄位類型都寫入相同的 doc values，因此額外空間完全來自索引：`keyword` 欄位為每個值索引一個詞元，而 `wildcard` 欄位則為值中的每個字元位置索引一個子字串。因此，索引的子字串數量會隨著每個值的長度增加，而非隨著不同值的數量增加。

索引子字串的數量並不是大小差異的良好預測指標，因為兩種欄位類型使用空間的方式不同。`keyword` 欄位索引少量長詞元：每個不同值一個，每個都完整儲存在詞元字典中。`wildcard` 欄位則索引大量出現的少量短詞元，因為任何資料集中出現的不同三字元組合數量有限。在 20,000 筆各約 116 個字元的不同記錄行樣本中，`keyword` 欄位索引了 20,000 個詞元，佔 2.3 MB 的詞元文字，而 `wildcard` 欄位索引了 5,431 個不同詞元，僅佔 16 KB。因此，索引 116 倍的子字串只產生了 13% 較大的索引。

大小增加取決於您的資料，因此沒有固定的倍數。較長的值會為每份文件產生更多子字串。字元集的寬度影響更大：來自窄字元集的值（例如十六進位識別碼）產生的不同子字串遠少於來自寬字元集的值（例如 Base64 負載）。在兩組各 20,000 個不同 64 字元值、僅字元集不同的樣本中，十六進位值的 `wildcard` 索引比對應的 `keyword` 索引大 6%，但 Base64 值則大 55%。

若要估算對您自身資料的影響，請將代表性樣本編製索引兩次，一次作為 `keyword` 欄位，一次作為 `wildcard` 欄位，然後比較產生的索引大小。

為每種欄位類型各建立一個索引，兩者使用相同數量的分片與副本，以免比較結果失真：

```json
PUT wildcard-sample
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "log_line": {
        "type": "wildcard"
      }
    }
  }
}
```
{% include copy-curl.html %}

```json
PUT keyword-sample
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "log_line": {
        "type": "keyword"
      }
    }
  }
}
```
{% include copy-curl.html %}

使用 [Bulk API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) 將相同的樣本文件編製索引到兩個索引中。請使用足夠的文件填滿至少一個分段；通常數萬個代表性值即已足夠。

將每個索引合併為單一分段，以免已刪除的文件與部分填滿的分段扭曲測量結果：

```json
POST wildcard-sample,keyword-sample/_forcemerge?max_num_segments=1
```
{% include copy-curl.html %}

強制合併是耗用大量資源的操作。請在測試索引而非正式環境索引上執行。
{: .warning}

排清兩個索引，使合併後的分段寫入磁碟。回報的儲存大小只計入已排清的分段，因此在排清完成前測量會得到無法反映合併後索引的大小：

```json
POST wildcard-sample,keyword-sample/_flush
```
{% include copy-curl.html %}

測量前，請確認每個索引都回報一個分段且沒有已刪除的文件：

```json
GET _cat/segments/wildcard-sample,keyword-sample?v&h=index,segment,docs.count,docs.deleted,size
```
{% include copy-curl.html %}

使用 [Index Stats API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/stats/) 比較大小：

```json
GET wildcard-sample,keyword-sample/_stats/store
```
{% include copy-curl.html %}

`primaries` 下的 `size_in_bytes` 值會回報每個索引在磁碟上的大小。以下節錄的回應顯示相關欄位：

```json
{
  "indices": {
    "wildcard-sample": {
      "primaries": {
        "store": {
          "size_in_bytes": 4600819
        }
      }
    },
    "keyword-sample": {
      "primaries": {
        "store": {
          "size_in_bytes": 4052054
        }
      }
    }
  }
}
```

兩個值之間的比率，就是當欄位對應為 `wildcard` 而非 `keyword` 時，整個索引會變大多少。這不是欄位本身儲存空間的比率，後者更高：`_source` 與其他每份文件的結構在兩個索引中完全相同，因此會稀釋差異。在上述回應中，整個索引的比率為 1.14，但單就欄位而言為 1.22。請使用整個索引的比率進行容量規劃，並將結果乘以 1 加上副本數量。

由於索引已合併為單一分段，這些大小是下限：正式環境索引包含多個分段與已刪除的文件，兩者都會為任一種欄位類型增加額外負擔。比率會隨文件數量增加而略微下降，因此小樣本會產生略為保守的估計。

若要減少儲存空間，請使用 `ignore_above` 防止超過指定長度的值被編製索引。如果您不需要對欄位進行彙總、排序或指令碼操作，也可以將 `doc_values` 設為 `false` 以停用 doc values。當欄位停用 doc values 時，您無法將該欄位從 `_source` 中排除，且對該欄位的查詢可能會明顯變慢。這兩種設定都會使欄位不符合 [衍生來源](#derived-source) 的資格。

## 限制

下列查詢不支援在 `wildcard` 欄位上使用：

- [`fuzzy`]({{site.url}}{{site.baseurl}}/query-dsl/term/fuzzy/) 查詢：請改在 `keyword` 或 `text` 欄位上執行。
- [`range`]({{site.url}}{{site.baseurl}}/query-dsl/term/range/) 查詢：範圍比對不適用於此欄位類型。

## 衍生來源

當索引使用 [衍生來源]({{site.url}}{{site.baseurl}}/field-types/metadata-fields/source/#derived-source) 時，OpenSearch 在重建來源時可能會排序多值萬用字元欄位中的值並移除重複項。 

若要在搭配衍生來源使用萬用字元值時支援 `wildcard` 欄位，必須啟用 `doc_values`。設定 `ignore_above` 或 `normalizer` 的 `wildcard` 欄位不支援衍生來源，因為 OpenSearch 無法從索引值重建原始值。
{: .note}

建立一個啟用衍生來源並設定啟用 `doc_values` 的 `name` 欄位的索引：

```json
PUT sample-index1
{
  "settings": {
    "index": {
      "derived_source": {
        "enabled": true
      }
    }
  },
  "mappings": {
    "properties": {
      "name": {
        "type": "wildcard",
        "doc_values": true
      }
    }
  }
}
```

將一份包含多個萬用字元值（包括重複值）的文件編製索引到該索引中：

```json
PUT sample-index1/_doc/1
{
  "name": ["ba", "ab", "ac", "ba"]
}
```

在 OpenSearch 重建 `_source` 後，衍生的 `_source` 會移除重複值並按字母順序排序：

```json
{
  "name": ["ab", "ac", "ba"]
}
```
