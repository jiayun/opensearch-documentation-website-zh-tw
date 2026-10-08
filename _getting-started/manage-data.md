---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "新增與管理您的資料"
nav_order: 35
---

# 新增與管理您的資料

OpenSearch 將資料儲存為 JSON _文件_，並將相關文件歸入一個 _索引_。將文件新增至不存在的索引時，會建立該索引並推斷每個欄位的類型，因此您無需定義任何欄位即可開始儲存資料。將文件編製索引後，您就可以從索引中擷取、更新及刪除這些文件。

## 將文件編製索引

若要將 JSON 文件新增至 OpenSearch 索引（也就是將文件 _編製索引_），請傳送包含下列標頭的 HTTP 請求：

```json
PUT /{index-name}/_doc/{document-id}
```

例如，若要將代表一名學生的文件編製索引，請傳送下列請求：

```json
PUT /students/_doc/1
{
  "name": "John Doe",
  "gpa": 3.89,
  "grad_year": 2022
}
```
{% include copy-curl.html %}

傳送上述請求後，OpenSearch 會建立名為 `students` 的索引，並將文件儲存在該索引中。如果您未提供文件 ID，OpenSearch 會產生文件 ID。在上述請求中，文件 ID 指定為學生 ID（`1`）。

若要進一步了解編製索引，請參閱[管理索引]({{site.url}}{{site.baseurl}}/im-plugin/)。

## 動態對應

將文件編製索引時，OpenSearch 會根據文件中提交的 JSON 類型推斷欄位類型。此程序稱為 _動態對應_。如需詳細資訊，請參閱[動態對應]({{site.url}}{{site.baseurl}}/mappings/#dynamic-mapping)。

若要檢視推斷出的欄位類型，請向 `_mapping` 端點傳送請求：

```json
GET /students/_mapping
```
{% include copy-curl.html %}

OpenSearch 會在回應中為每個欄位提供 `type` 欄位：

```json
{
  "students": {
    "mappings": {
      "properties": {
        "gpa": {
          "type": "float"
        },
        "grad_year": {
          "type": "long"
        },
        "name": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        }
      }
    }
  }
}
```

OpenSearch 將數值欄位對應至 `float` 與 `long` 類型。請注意，OpenSearch 將 `name` 文字欄位對應至 `text`，並新增一個對應至 `keyword` 的 `name.keyword` 子欄位。對應至 `text` 的欄位會經過分析（轉為小寫並切分為詞彙），可用於全文搜尋。對應至 `keyword` 的欄位則用於精確詞彙搜尋。

## 索引對應與設定

OpenSearch 索引透過對應與設定進行組態：

- _對應_ 是欄位及其類型的集合。如需詳細資訊，請參閱[對應與欄位類型]({{site.url}}{{site.baseurl}}/mappings/)。
- _設定_ 包含索引資料，例如索引名稱、建立日期和分片數量。如需詳細資訊，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

欄位建立後，便無法變更其類型。若要變更欄位類型，必須刪除索引，再使用新的對應重新建立索引。若要控制欄位類型，請在建立索引時自行指定對應。
{: .note}

在上述範例中，OpenSearch 將 `grad_year` 對應至 `long`，但畢業年份是日期。若要將 `grad_year` 對應至 `date`，請先刪除動態對應所建立的索引：

```json
DELETE /students
```
{% include copy-curl.html %}

您可以在單一請求中指定對應與設定。下列請求會重新建立索引，指定索引分片數量，並將 `name` 欄位對應至 `text`、將 `grad_year` 欄位對應至 `date`。由於畢業年份沒有月份或日期，`format` 參數會告知 OpenSearch 將該欄位解讀為四位數的年份：

```json
PUT /students
{
  "settings": {
    "index.number_of_shards": 1
  }, 
  "mappings": {
    "properties": {
      "name": {
        "type": "text"
      },
      "grad_year": {
        "type": "date",
        "format": "yyyy"
      }
    }
  }
}
```
{% include copy-curl.html %}

現在再次將同一份文件編製索引：

```json
PUT /students/_doc/1
{
  "name": "John Doe",
  "gpa": 3.89,
  "grad_year": 2022
}
```
{% include copy-curl.html %}

OpenSearch 會將 `grad_year` 儲存為日期 `2022-01-01`，因此您現在可以對其使用日期範圍查詢。`_source` 仍包含原始值 `2022`。

若要檢視索引欄位的對應，請傳送下列請求：

```json
GET /students/_mapping
```
{% include copy-curl.html %}

OpenSearch 依照指定的類型對應 `name` 與 `grad_year` 欄位，並推斷 `gpa` 欄位的欄位類型：

```json
{
  "students": {
    "mappings": {
      "properties": {
        "gpa": {
          "type": "float"
        },
        "grad_year": {
          "type": "date",
          "format": "yyyy"
        },
        "name": {
          "type": "text"
        }
      }
    }
  }
}
```

請注意，`name` 不再有 `name.keyword` 子欄位。明確的對應會取代動態預設值，因此只會使用您指定的類型。

## 搜尋文件

若要搜尋文件，請指定要搜尋的索引，以及用來比對文件的查詢。最簡單的查詢是 `match_all` 查詢，它會比對索引中的所有文件：

```json
GET /students/_search
{
  "query": {
    "match_all": {}
  }
}
```
{% include copy-curl.html %}

OpenSearch 會傳回已編製索引的文件：

```json
{
  "took": 12,
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
    "max_score": 1,
    "hits": [
      {
        "_index": "students",
        "_id": "1",
        "_score": 1,
        "_source": {
          "name": "John Doe",
          "gpa": 3.89,
          "grad_year": 2022
        }
      }
    ]
  }
}
```

如需搜尋的詳細資訊，請參閱[搜尋您的資料]({{site.url}}{{site.baseurl}}/getting-started/search-data/)。

## 更新文件

在 OpenSearch 中，已儲存的文件是不可變的，因此更新會取代文件，而不是就地修改。OpenSearch 會擷取目前的文件、套用您的變更，並將結果編製索引為新版本。您可以使用 Index Document API 取代整份文件，並為文件中所有現有及新增的欄位提供值。例如，若要更新先前已編製索引之文件的 `gpa` 欄位並新增 `address` 欄位，請傳送下列請求：

```json
PUT /students/_doc/1
{
  "name": "John Doe",
  "gpa": 3.91,
  "grad_year": 2022,
  "address": "123 Main St."
}
```
{% include copy-curl.html %}

或者，您可以呼叫 Update Document API 來更新文件的部分內容：

```json
POST /students/_update/1/
{
  "doc": {
    "gpa": 3.91,
    "address": "123 Main St."
  }
}
```
{% include copy-curl.html %}

此請求只會更新您提供的欄位，文件的其餘部分則維持不變。文件必須已存在；更新不在索引中的文件會傳回錯誤。如需部分文件更新的詳細資訊，請參閱 [Update Document API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-document/)。

若要在文件存在時更新文件，或在文件不存在時將新文件編製索引，請使用 _upsert_ 操作。在請求中加入 `doc_as_upsert` 並將其設為 `true`：

```json
POST /students/_update/2/
{
  "doc": {
    "name": "Jonathan Powers",
    "gpa": 3.85,
    "grad_year": 2025
  },
  "doc_as_upsert": true
}
```
{% include copy-curl.html %}

由於不存在 ID 為 `2` 的文件，OpenSearch 會將新文件編製索引。如果該文件已存在，同一個請求就會更新該文件，而不會傳回錯誤。

如需 upsert 操作的詳細資訊，請參閱 [Upsert]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-document/#upsert)。

## 刪除文件

若要刪除文件，請傳送刪除請求並提供文件 ID：

```json
DELETE /students/_doc/1
```
{% include copy-curl.html %}

## 刪除索引

若要永久刪除索引及其中的所有文件，請傳送下列請求：

```json
DELETE /students
```
{% include copy-curl.html %}

## 延伸閱讀

- 如需文件 API 的相關資訊，請參閱[文件 API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/)。
- 如需對應的相關資訊，請參閱[對應與欄位類型]({{site.url}}{{site.baseurl}}/mappings/)。
- 如需設定的相關資訊，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

## 後續步驟

- 若要在單一請求中將多份文件編製索引，請參閱[將資料匯入 OpenSearch]({{site.url}}{{site.baseurl}}/getting-started/ingest-data/)。
- 若要了解搜尋選項，請參閱[搜尋您的資料]({{site.url}}{{site.baseurl}}/getting-started/search-data/)。
