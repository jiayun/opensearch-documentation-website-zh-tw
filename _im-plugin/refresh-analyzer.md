---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "重新整理搜尋分析器"
parent: Tuning indexes
nav_order: 10
has_toc: false
redirect_from: 
  - /query-dsl/analyzers/refresh-analyzer/
  - /im-plugin/refresh-analyzer/index/
---

# 重新整理搜尋分析器

使用 Refresh Search Analyzer API 即時套用對搜尋分析器資源檔案的變更。例如，如果您變更了分析器中的同義詞清單，該變更會立即生效，無需關閉再重新開啟索引：

```json
POST /_plugins/_refresh_search_analyzers/{index}
```
{% include copy-curl.html %}

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為必要。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `index` | 字串 | 要套用此操作的索引、資料串流或索引別名的逗號分隔清單。支援萬用字元運算式 (`*`)。使用 `_all` 或 `*` 來指定叢集中的所有索引與資料串流。 |

## 查詢參數

下表列出支援的查詢參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`reload_cached_resources` | 布林值 | 設定為 `true` 時，會從磁碟重新載入快取的資源，而不會為從磁碟載入檔案的詞元篩選器 (例如 [`hunspell`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/hunspell/) 篩選器的字典檔案) 重建快取。當為 `false` (預設值) 時，會重建分析器工廠，但重複使用快取的資源。

## 讓詞元篩選器可更新

只有當詞元篩選器的 `updateable` 旗標為 `true` 時，才會被重新整理。可更新的篩選器只能用於搜尋分析器，不能用於索引分析器，因為現有的文件不會重新分析。以下請求會建立一個帶有可更新同義詞篩選器的索引，並將其套用為 `desc` 欄位的搜尋分析器：

```json
PUT /synonym_index
{
  "settings": {
    "index": {
      "analysis": {
        "analyzer": {
          "my_synonyms": {
            "tokenizer": "whitespace",
            "filter": [
              "synonym"
            ]
          }
        },
        "filter": {
          "synonym": {
            "type": "synonym_graph",
            "synonyms_path": "analysis/synonyms.txt",
            "updateable": true
          }
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "desc": {
        "type": "text",
        "analyzer": "standard",
        "search_analyzer": "my_synonyms"
      }
    }
  }
}
```
{% include copy-curl.html %}

`synonyms_path` 是相對於每個節點的 `config` 目錄。編輯檔案後，請重新整理分析器：

```json
POST /_plugins/_refresh_search_analyzers/synonym_index
```
{% include copy-curl.html %}

## 回應範例

回應會列出每個索引中已重新整理的分析器：

```json
{
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "successful_refresh_details": [
    {
      "index": "synonym_index",
      "refreshed_analyzers": [
        "my_synonyms"
      ]
    }
  ]
}
```

針對 `desc` 的搜尋現在會使用更新後的同義詞清單。

