---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Painless 指令碼語言"
nav_order: 30
has_children: true
has_toc: false
---

# Painless 指令碼語言

Painless 是 OpenSearch 的預設指令碼語言，也是唯一能在所有指令碼情境中執行的語言。它的語法擴充了 Java 的子集，其編譯器會產生 JVM 位元組碼，因此編譯後的 Painless 指令碼能以接近編譯後 Java 的速度執行。

Painless 是沙箱化的，因此無論是內嵌指令碼還是儲存的指令碼，使用起來都很安全。指令碼只能呼叫 OpenSearch 所提供允許清單中的類別與方法，而此允許清單排除了任何寫入檔案、開啟通訊端、產生執行緒或讀取系統時鐘的類別或方法。呼叫允許清單未列出的方法會在編譯時失敗並擲回 `compile error`，因此這類指令碼永遠不會對您的資料執行。

允許清單定義於 OpenSearch 儲存庫的 [`painless/spi` 目錄](https://github.com/opensearch-project/OpenSearch/tree/main/modules/lang-painless/src/main/resources/org/opensearch/painless/spi)。其中十二個檔案涵蓋 Java 標準函式庫中允許使用的部分，每個檔案對應一個套件---`java.lang`、`java.math`、`java.text`、`java.util`、`java.util.function`、`java.util.regex`、`java.util.stream`、`java.time`，以及其 `chrono`、`format`、`temporal` 與 `zone` 子套件。其餘六個檔案則加入特定情境所需的類別，例如資料匯入、更新與評分情境。每個允許的類別都以 `class` 區塊呈現，列出可在其上呼叫的欄位、建構子與方法，因此當您需要確認某個特定方法是否可用時，請查閱這些定義。如需其涵蓋範圍的概覽，請參閱 [可用的函式庫]({{site.url}}{{site.baseurl}}/scripting/painless-language/#available-libraries)。

## 語言特性

Painless 提供下列功能：

- 選用型別：當型別已知時，以明確型別（例如 `int count = 0`）宣告變數；當型別會變動時，則以 `def` 宣告。明確型別會編譯成更快的位元組碼，因為它們避免了執行時期的型別解析。
- Java 語法的子集，包括控制流程、運算子、轉型與方法呼叫，外加 Java 所沒有的指令碼便利功能，例如 `?:` 空值合併運算子，以及映射與清單字面值。
- Java 的集合與字串函式庫。`HashMap`、`ArrayList`、`String`、`Math` 以及 `java.time` 類別皆可使用，因此指令碼可以建立並回傳結構化的值。
- 正規表示式，但受複雜度預算限制。請參閱 [控制正規表示式](#controlling-regular-expressions)。

如需完整語法---型別、轉型、運算子、陳述式、函式、lambda 與正規表示式---請參閱 [Painless 語言參考文件]({{site.url}}{{site.baseurl}}/scripting/painless-language/)。

Painless 與 Java 有所不同。反射、類別定義、泛型型別參數與 `finally` 區塊皆不可使用；`catch` 子句只能命名允許清單中列出的例外類型；而且指令碼由一個陳述式區塊組成，前面可加上所需的函式宣告。
{: .note}

## 測試指令碼

在將 Painless 指令碼加入搜尋請求之前，請先使用 [Execute Inline Script API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/exec-script/) 加以開發。此 API 會隔離編譯並執行指令碼，然後回傳其結果，因此編譯錯誤會立即回傳，並附上錯誤在指令碼本文中的位置。

下列請求計算一份產品清單的含稅價格：

```json
POST _scripts/painless/_execute
{
  "script": {
    "source": "def totals = new HashMap(); for (int i = 0; i < params.skus.length; i++) { totals.put(params.skus[i], Math.round(params.prices[i] * params.tax_rate * 100) / 100.0) } return totals",
    "params": {
      "skus": ["AUD-1001", "ACC-2001"],
      "prices": [249.99, 89.0],
      "tax_rate": 1.08
    }
  }
}
```
{% include copy-curl.html %}

預設的 `painless_test` 情境會將回傳的映射轉換為字串：

```json
{
  "result": "{AUD-1001=269.99, ACC-2001=96.12}"
}
```

若要測試讀取文件欄位或相關性分數的指令碼，請將 `context` 設為 `filter` 或 `score`，並在 `context_setup` 中提供測試文件。相關範例請參閱 [Execute Inline Script API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/exec-script/)。

## 處理日期

透過 doc values 讀取的日期欄位在 Painless 中以 `ZonedDateTime` 呈現，因此其組成部分可透過標準的 `java.time` 存取子方法取得。下列搜尋從 `scripting-products` 索引中擷取產品的發行年份與月份，該索引建立於 [測試設定]({{site.url}}{{site.baseurl}}/scripting/using-scripts/#test-setup)：

```json
GET scripting-products/_search
{
  "_source": false,
  "query": { "term": { "sku": "AUD-1001" } },
  "script_fields": {
    "release_year": {
      "script": {
        "lang": "painless",
        "source": "doc['release_date'].value.getYear()"
      }
    },
    "release_month": {
      "script": {
        "lang": "painless",
        "source": "doc['release_date'].value.getMonthValue()"
      }
    }
  }
}
```
{% include copy-curl.html %}

兩個組成部分都以整數回傳：

<details open markdown="block">
<summary>
  回應
</summary>

```json
{
  "took": 26,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "scripting-products",
        "_id": "1",
        "_score": 1.0,
        "fields": {
          "release_month": [
            3
          ],
          "release_year": [
            2024
          ]
        }
      }
    ]
  }
}
```
</details>

回報目前時間的方法（例如 `ZonedDateTime.now()`）不在允許清單中，因為輸出在不同分片或不同重試之間會變化的指令碼會產生不一致的結果，並使快取失效。請改為將參考時間以參數傳入。
{: .note}

## 控制正規表示式

某些正規表示式在輸入僅比測試時略長的情況下，可能執行非常久的時間。包含這類表示式的指令碼，只要表示式持續執行，就會在執行它的節點上消耗 CPU。為了限制這種 CPU 消耗，OpenSearch 限制了 Painless 正規表示式可讀取的字元數：`script.painless.regex.enabled` 預設為 `limited`，`script.painless.regex.limit-factor` 預設為 `6`，因此，輸入中的每個字元最多允許表示式讀取六個字元。超出限制會觸發 `circuit_breaking_exception`，其中會回報模式、字元限制與已讀取的字元數。

下表列出 `script.painless.regex.enabled` 的值。此設定與 `script.painless.regex.limit-factor` 皆為靜態設定，因此請在每個節點的 `opensearch.yml` 中設定，並重新啟動節點。

值 | 說明
:--- | :---
`limited` | 允許正規表示式，並受 `script.painless.regex.limit-factor` 限制。這是預設值。
`true` | 允許正規表示式且無字元限制。表示式此時可以執行直到完成，期間持續在節點上消耗 CPU。
`false` | 正規表示式語法無法編譯。

## 外掛程式新增的方法

已安裝的外掛程式可以將類別與方法加入 Painless 允許清單。每項新增都限定於特定情境，因此外掛程式為 `score` 情境提供的方法在其他情境中無法使用。

k-NN 外掛程式新增了可對 `knn_vector` 欄位運作的向量距離函式。它們是一般的 Painless 呼叫，因此使用這些函式的指令碼可將 `lang` 保持為 `painless`：

```json
"source": "cosineSimilarity(params.query_value, doc[params.field])"
```

如需可用函式及其限制，請參閱 [Painless 指令碼擴充功能]({{site.url}}{{site.baseurl}}/vector-search/vector-search-techniques/painless-functions/)。

同樣的呼叫在 `painless_test` 情境中會編譯失敗並擲回 `Unknown call [cosineSimilarity]`，因為 k-NN 允許清單並未延伸至該情境。請在外掛程式註冊方法的情境中測試依賴該外掛程式方法的指令碼。
{: .note}

## Painless 的使用場景

Painless 可在 OpenSearch 的所有指令碼情境中執行，包括下列各項：

- 在搜尋時運算 [指令碼欄位]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#using-scripted-fields) 與 [衍生欄位]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/derived/)
- 使用 [`script_score` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/script-score/) 自訂相關性，或使用 [`script` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/script/) 進行篩選
- 依運算出的值進行 [排序]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/sort/)
- 透過 [Update Document]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-document/) 與 [Update By Query]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-by-query/) API 修改文件
- 在匯入期間使用 [`script` 處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/script/) 轉換文件
- 建立 [指令碼指標]({{site.url}}{{site.baseurl}}/aggregations/metric/scripted-metric/) 與 [桶指令碼]({{site.url}}{{site.baseurl}}/aggregations/pipeline/bucket-script/) 彙總

如需各情境提供的變數與回傳型別，請參閱 [指令碼情境]({{site.url}}{{site.baseurl}}/scripting/script-contexts/)。

## 相關文件

- [Painless 語言參考文件]({{site.url}}{{site.baseurl}}/scripting/painless-language/)
- [指令碼情境]({{site.url}}{{site.baseurl}}/scripting/script-contexts/)
- [Execute Inline Script API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/exec-script/)
