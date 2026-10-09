---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "欄位資料"
parent: Mapping parameters
nav_order: 50
has_children: false
has_toc: false
---

# 欄位資料對應參數

預設情況下，`text` 欄位無法用於排序、彙總或指令碼處理。支援全文搜尋的倒排索引會將詞彙對應至文件，但不會提供排序與彙總所需的個別文件欄位值。嘗試對 `text` 欄位進行彙總或排序時，會傳回錯誤，建議您改用 `keyword` 欄位。

`fielddata` 對應參數會將分析後的詞元載入常駐堆積記憶體的資料結構，讓 `text` 欄位可用於排序、彙總與指令碼處理。當首次為了執行其中一項操作而存取欄位時，OpenSearch 會依需求建構此結構。

由於欄位資料會針對分析後的詞元進行操作，對文字欄位進行彙總會為個別詞彙（例如「open」和「source」）產生桶，而非原始的多字詞值（例如「Open Source」）。如果您需要對未經分析的精確值進行彙總，請改用 `keyword` 欄位。
{: .note}

欄位資料可能耗用大量堆積記憶體，因為它會載入分段中所有文件在該欄位的所有不重複詞元，並在該分段的整個存續期間保留於記憶體中。在大多數情況下，使用[多重欄位]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/fields/)中的 [`keyword`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/keyword/) 子欄位，比啟用欄位資料更合適。
{: .warning}

## 範例

下列範例會建立索引，並在文字欄位上啟用 `fielddata`：

```json
PUT /fielddata_test
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "fielddata": true
      }
    }
  }
}
```
{% include copy-curl.html %}

將一些文件編製索引：

```json
POST /fielddata_test/_bulk?refresh=true
{"index":{}}
{"title":"OpenSearch performance tuning"}
{"index":{}}
{"title":"OpenSearch security configuration"}
{"index":{}}
{"title":"OpenSearch index management"}
```
{% include copy-curl.html %}

啟用 `fielddata` 後，您可以對 `title` 欄位中分析後的詞元進行彙總：

```json
GET /fielddata_test/_search
{
  "size": 0,
  "aggs": {
    "top_terms": {
      "terms": {
        "field": "title",
        "size": 5
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會傳回個別分析後詞元的桶（而非完整的欄位值）：

```json
{
  "took" : 3,
  "timed_out" : false,
  "terminated_early" : true,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 3,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "top_terms" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 2,
      "buckets" : [
        {
          "key" : "opensearch",
          "doc_count" : 3
        },
        {
          "key" : "configuration",
          "doc_count" : 1
        },
        {
          "key" : "index",
          "doc_count" : 1
        },
        {
          "key" : "management",
          "doc_count" : 1
        },
        {
          "key" : "performance",
          "doc_count" : 1
        }
      ]
    }
  }
}
```

`fielddata` 設定可動態更新。您可以在現有欄位上啟用此設定，無須重新編製索引：

```json
PUT /fielddata_test/_mapping
{
  "properties": {
    "title": {
      "type": "text",
      "fielddata": true
    }
  }
}
```
{% include copy-curl.html %}

## 欄位資料頻率篩選器

`fielddata_frequency_filter` 參數僅載入文件頻率落在指定範圍內的詞元，以減少記憶體用量。極為常見的詞元（例如停用詞）或極為罕見的詞元（例如拼字錯誤）會從欄位資料中排除，藉此降低堆積記憶體耗用量，同時仍支援大多數彙總使用案例。

下表列出 `fielddata_frequency_filter` 參數。

| 參數 | 必要／選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `min` | 必要 | 浮點數 | 載入詞元所需的最低文件頻率（以 0 到 1 之間的比率表示）。出現於文件中的頻率低於此門檻的詞元會被排除。 |
| `max` | 必要 | 浮點數 | 載入詞元所允許的最高文件頻率（以 0 到 1 之間的比率表示）。出現於文件中的頻率高於此門檻的詞元會被排除。 |
| `min_segment_size` | 選用 | 整數 | 分段必須包含的最低文件數量，達到此數量才會套用頻率篩選器。較小的分段會載入所有詞元，不受頻率影響。預設為 `0`。 |

下列範例僅載入出現於 1% 到 50% 文件中的詞元，並且僅對至少包含 100 份文件的分段套用此篩選器：

```json
PUT /my-index
{
  "mappings": {
    "properties": {
      "description": {
        "type": "text",
        "fielddata": true,
        "fielddata_frequency_filter": {
          "min": 0.01,
          "max": 0.5,
          "min_segment_size": 100
        }
      }
    }
  }
}
```
{% include copy-curl.html %}
