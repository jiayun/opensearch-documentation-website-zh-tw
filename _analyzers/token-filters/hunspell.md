---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Hunspell
parent: Token filters
nav_order: 160
---

# Hunspell 詞元篩選器

`hunspell` 詞元篩選器用於對特定語言的單字進行詞幹提取與詞形分析。此篩選器會套用 Hunspell 字典，這類字典廣泛用於拼字檢查器。它的運作方式是將單字拆解為其字根形式（詞幹提取）。

Hunspell 字典檔案會在啟動時自動從 `<OS_PATH_CONF>/hunspell/<locale>` 目錄載入。例如，`en_GB` 地區設定在 `<OS_PATH_CONF>/hunspell/en_GB/` 目錄中必須至少有一個 `.aff` 檔案，以及一個或多個 `.dic` 檔案。

您也可以使用 `ref_path` 參數從自訂目錄載入字典，以便為同一個地區設定維護多組獨立的字典。如需詳細資訊，請參閱[使用 ref_path 載入自訂字典](#custom-dictionary-loading)。

您也可以在執行階段熱重新載入 Hunspell 字典，而不需要重新啟動節點。如需詳細資訊，請參閱[熱重新載入 Hunspell 字典](#hot-reloading-hunspell-dictionaries)。

您可以從 [LibreOffice 字典](https://github.com/LibreOffice/dictionaries)下載這些檔案。

## 參數

`hunspell` 詞元篩選器可使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`language/lang/locale` | 三者至少須提供其一 | 字串 | 指定 Hunspell 字典的語言。只能包含英數字元、連字號和底線（例如 `en_US`、`de_DE`）。
`ref_path` | 選用 | 字串 | 指定用於從 `<OS_PATH_CONF>/<ref_path>/hunspell/<locale>/` 目錄載入字典的相對路徑，而非從預設的 `<OS_PATH_CONF>/hunspell/<locale>/` 目錄載入。指定此參數時，`locale` 參數為必要。`ref_path` 值可包含英數字元、連字號、底線和正斜線（用於巢狀路徑，例如 `analyzers/my-dict`）。`locale` 值只能包含英數字元、連字號和底線。請參閱[使用 ref_path 載入自訂字典](#custom-dictionary-loading)。**注意**：`ref_path` 會直接解析至 `<OS_PATH_CONF>` 底下。在 OpenSearch 3.6 及更早版本中，它會解析至 `<OS_PATH_CONF>/analyzers/` 底下。若要保留先前的配置，請在您的 `ref_path` 值前面加上 `analyzers/`（例如 `analyzers/my-dict`）。
`dedup` | 選用 | 布林值 | 決定是否移除同一個詞元的多個重複詞幹詞彙。預設值為 `true`。
`dictionary` | 選用 | 字串陣列 | 設定 Hunspell 字典要使用的字典檔案。若未指定 `ref_path`，預設為 `<OS_PATH_CONF>/hunspell/<locale>` 目錄中的所有檔案；若已指定 `ref_path`，則預設為 `<OS_PATH_CONF>/<ref_path>/hunspell/<locale>/` 目錄中的所有檔案。請參閱[使用 ref_path 載入自訂字典](#custom-dictionary-loading)。
`longest_only` | 選用 | 布林值 | 指定是否只傳回詞元最長的詞幹版本。預設值為 `false`。
`updateable` | 選用 | 布林值 | 設為 `true` 時，篩選器會以搜尋時分析模式運作，讓您可以使用 [Refresh search analyzer]({{site.url}}{{site.baseurl}}/im-plugin/refresh-analyzer/) API 熱重新載入字典，而不需要重新啟動節點。預設值為 `false`。**於 3.7 版推出。**

## 範例

下列範例請求會建立名為 `my_index` 的新索引，並設定一個使用 `hunspell` 篩選器的分析器：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_hunspell_filter": {
          "type": "hunspell",
          "lang": "en_GB",
          "dedup": true,
          "longest_only": true
        }
      },
      "analyzer": {
        "my_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_hunspell_filter"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 載入自訂字典

當您指定 `ref_path` 參數時，字典會從自訂目錄載入，而非從預設目錄載入。當您需要為同一個地區設定使用多組獨立的字典時，這項功能非常實用，例如不同的索引需要不同的自訂字典時。

`ref_path` 值會相對於 `<OS_PATH_CONF>` 進行解析，且可包含正斜線以表示巢狀路徑。在 OpenSearch 3.6 及更早版本中，`ref_path` 是相對於 `<OS_PATH_CONF>/analyzers/` 進行解析。從 3.6 或更早版本升級時，若要保留先前的目錄配置，請在您現有的 `ref_path` 值前面加上 `analyzers/`。
{: .note}

請將字典檔案放在下列目錄結構中：

```xml
<OS_PATH_CONF>/<ref_path>/hunspell/<locale>/
├── <locale>.aff       (exactly one .aff file required)
├── <locale>.dic       (one or more .dic files)
└── <locale>_custom.dic
```

下列範例會從 `<OS_PATH_CONF>/analyzers/my-dict/hunspell/en_US/` 載入 Hunspell 字典：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_custom_hunspell": {
          "type": "hunspell",
          "ref_path": "analyzers/my-dict",
          "locale": "en_US"
        }
      },
      "analyzer": {
        "my_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_custom_hunspell"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

多個索引可以針對同一個地區設定使用不同的 `ref_path` 目錄。每個 `ref_path` 都會維護各自獨立的字典快取：

```json
PUT /index_medical
{
  "settings": {
    "analysis": {
      "filter": {
        "medical_hunspell": {
          "type": "hunspell",
          "ref_path": "analyzers/medical-dict",
          "locale": "en_US"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

```json
PUT /index_legal
{
  "settings": {
    "analysis": {
      "filter": {
        "legal_hunspell": {
          "type": "hunspell",
          "ref_path": "analyzers/legal-dict",
          "locale": "en_US"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 熱重新載入 Hunspell 字典
**於 3.7 版推出**
{: .label .label-purple }

您可以在執行階段更新 Hunspell 字典，而不需要重新啟動節點。若要啟用此功能，請在 Hunspell 詞元篩選器上將 `updateable` 參數設為 `true`。這會以搜尋時分析模式註冊此篩選器，因此它只能在搜尋時使用（例如在 `search_analyzer` 中），而不能在編製索引時使用。

若要熱重新載入 Hunspell 字典，請依照下列步驟操作：

1. 設定 Hunspell 詞元篩選器，並將 `updateable` 設為 `true`。下列範例會建立一個索引，並使用可熱重新載入的 Hunspell 篩選器作為 `search_analyzer`：

   ```json
   PUT /my_index
   {
     "settings": {
       "analysis": {
         "filter": {
           "my_reloadable_hunspell": {
             "type": "hunspell",
             "ref_path": "analyzers/my-dict",
             "locale": "en_US",
             "updateable": true
           }
         },
         "analyzer": {
           "my_search_analyzer": {
             "type": "custom",
             "tokenizer": "standard",
             "filter": [
               "lowercase",
               "my_reloadable_hunspell"
             ]
           }
         }
       }
     },
     "mappings": {
       "properties": {
         "content": {
           "type": "text",
           "analyzer": "standard",
           "search_analyzer": "my_search_analyzer"
         }
       }
     }
   }
   ```
   {% include copy-curl.html %}

1. 在每個持有該索引分片的節點上，替換磁碟上的 `.aff` 和 `.dic` 檔案。

1. 呼叫 [Refresh Search Analyzer API]({{site.url}}{{site.baseurl}}/im-plugin/refresh-analyzer/)。當 `reload_cached_resources` 為 `false`（預設值）時，此 API 會重建分析器工廠，但會重複使用先前快取的 Hunspell 字典。請指定 `reload_cached_resources=true` 以強制從磁碟重新載入字典：

   ```json
   POST /_plugins/_refresh_search_analyzers/my_index?reload_cached_resources=true
   ```
   {% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器產生的詞元：

```json
POST /my_index/_analyze
{
  "analyzer": "my_analyzer",
  "text": "the turtle moves slowly"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "the",
      "start_offset": 0,
      "end_offset": 3,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "turtle",
      "start_offset": 4,
      "end_offset": 10,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "move",
      "start_offset": 11,
      "end_offset": 16,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "slow",
      "start_offset": 17,
      "end_offset": 23,
      "type": "<ALPHANUM>",
      "position": 3
    }
  ]
}
```
