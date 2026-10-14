---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "顯著文字"
parent: Bucket aggregations
nav_order: 190
redirect_from:
  - /query-dsl/aggregations/bucket/significant-text/
---

# 顯著文字彙總

`significant_text` 彙總會比較前景集合（您的查詢結果）與背景集合（完整索引）中的詞彙頻率，藉此找出自由文字欄位中不尋常或有趣的詞彙。與 [`significant_terms`]({{site.url}}{{site.baseurl}}/aggregations/bucket/significant-terms/) 不同（後者運作於已編製索引的關鍵字欄位），`significant_text` 會即時重新分析來源文字，並可篩除會扭曲結果的重複內容。

在下列情境中使用 `significant_text` 彙總：

- 建議使用者可加入搜尋的相關詞彙。例如，搜尋「bird flu」時可能會建議「H5N1」。
- 找出可描述一組文件特性的關鍵字，例如用來建立文件分類器。

一組搜尋結果中最常見的詞彙通常沒什麼意思，因為它們到處都很常見（例如「and」、「of」或「the」）。當某個詞彙的頻率在前景與背景之間有明顯變化時，該詞彙即具顯著性。例如，某個詞彙出現在您結果的 100 份文件中的 4 份，但在索引的 1,000 萬份文件中只出現於 5 份，則該詞彙與您的搜尋高度相關。

重新分析大型結果集會耗用大量 CPU。請在 [`sampler`]({{site.url}}{{site.baseurl}}/aggregations/bucket/sampler/) 或 [`diversified_sampler`]({{site.url}}{{site.baseurl}}/aggregations/bucket/diversified-sampler/) 彙總內使用 `significant_text`，將分析限制在少量最相符的文件（例如 100--200 份）。
{: .note}

## 參數

`significant_text` 彙總採用下列參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `field` | 必要 | 字串 | 要分析的文字欄位。 |
| `size` | 選用 | 整數 | 要傳回的詞彙桶數。預設為 `10`。 |
| `shard_size` | 選用 | 整數 | 從每個分片收集的候選詞彙數。較高的值可提升準確度，但會犧牲效能。預設為 `-1`，會根據 `size` 設定分片大小。如需更多資訊，請參閱[大小與分片大小](#size-and-shard-size)。 |
| `min_doc_count` | 選用 | 整數 | 詞彙必須出現於其中才能納入的最少文件數。預設為 `3`。設為 `1` 通常會傳回錯字與拼字錯誤。 |
| `shard_min_doc_count` | 選用 | 整數 | 詞彙被視為候選詞彙所需的最小本機分片頻率。預設為 `0`。 |
| `background_filter` | 選用 | 物件 | 縮小用於比較之背景集合的查詢。預設會使用整個索引作為背景。 |
| `filter_duplicate_text` | 選用 | 布林值 | 設為 `true` 時，會篩除已出現過、長度為 6 個以上詞元的序列，以減少剪貼內容造成的雜訊。預設為 `false`。如需更多資訊，請參閱[篩除重複文字](#filtering-duplicate-text)。 |
| `source_fields` | 選用 | 陣列 | 要從中分析文字的 JSON 來源欄位名稱清單。當已編製索引的欄位名稱與來源欄位不同時使用（例如使用 `copy_to` 時）。如需更多資訊，請參閱[分析使用 copy_to 建立的欄位](#analyzing-fields-created-using-copy_to)。 |
| `include` | 選用 | 字串或陣列 | 要包含的規則表達式模式或確切詞彙清單。 |
| `exclude` | 選用 | 字串或陣列 | 要從結果中排除的規則表達式模式或確切詞彙清單。 |

## 範例

下列範例假設有一個 `shakespeare` 索引，內含莎士比亞全集，並有一個 `text_entry` 文字欄位。此查詢會搜尋包含「breathe」的文件，然後在 `sampler` 內使用 `significant_text`，找出與這些段落最相關（相較於完整語料庫）的詞彙：

```json
GET /shakespeare/_search
{
  "size": 0,
  "query": {
    "match": {
      "text_entry": "breathe"
    }
  },
  "aggs": {
    "sample": {
      "sampler": {
        "shard_size": 100
      },
      "aggs": {
        "keywords": {
          "significant_text": {
            "field": "text_entry",
            "min_doc_count": 4
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會指出「air」、「dead」和「life」等詞彙與關於呼吸的段落顯著相關：

```json
{
  ...
  "aggregations" : {
    "sample" : {
      "doc_count" : 59,
      "keywords" : {
        "doc_count" : 59,
        "bg_count" : 111396,
        "buckets" : [
          {
            "key" : "breathe",
            "doc_count" : 59,
            "score" : 1887.0677966101694,
            "bg_count" : 59
          },
          {
            "key" : "air",
            "doc_count" : 4,
            "score" : 2.641295376716233,
            "bg_count" : 189
          },
          {
            "key" : "dead",
            "doc_count" : 4,
            "score" : 0.9665839666414213,
            "bg_count" : 495
          },
          {
            "key" : "life",
            "doc_count" : 5,
            "score" : 0.9090787433467572,
            "bg_count" : 805
          }
        ]
      }
    }
  }
}
```

## 範例：使用篩選器縮小背景

根據預設，詞彙頻率會與整個索引比較。`background_filter` 參數會縮小比較集合，這可找出在特定情境中具顯著性的詞彙。下列範例會將所有劇作中關於「breathe」的段落，與僅來自《亨利四世》的台詞（而非完整語料庫）進行比較。

大多數顯著性啟發式方法都假設背景集合包含前景集合。在此範例中，前景包含每部劇作的台詞，但背景只包含《亨利四世》，因此詞彙 `breathe` 出現於 59 份前景文件，但只出現於 6 份背景文件。若要在這種情況下正確為詞彙評分，請將 `background_is_superset` 設為 `false`。`jlh` 啟發式方法不支援此設定，因此下列請求使用 `chi_square`。使用 `chi_square` 時，省略 `background_is_superset: false` 會導致請求失敗。使用預設的 `jlh` 啟發式方法時，請求會成功，但分數會計算錯誤：

```json
GET /shakespeare/_search
{
  "size": 0,
  "query": {
    "match": {
      "text_entry": "breathe"
    }
  },
  "aggs": {
    "sample": {
      "sampler": {
        "shard_size": 100
      },
      "aggs": {
        "keywords": {
          "significant_text": {
            "field": "text_entry",
            "min_doc_count": 3,
            "background_filter": {
              "term": {
                "play_name": "Henry IV"
              }
            },
            "chi_square": {
              "background_is_superset": false
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

將背景縮小至《亨利四世》的 3,205 行台詞後，`bg_count` 值會變小，且也會傳回 `awhile` 和 `life` 等詞彙：

```json
{
  ...
  "aggregations": {
    "sample": {
      "doc_count": 59,
      "keywords": {
        "doc_count": 59,
        "bg_count": 3205,
        "buckets": [
          {
            "key": "breathe",
            "doc_count": 59,
            "score": 2957.161281651266,
            "bg_count": 6
          },
          {
            "key": "air",
            "doc_count": 4,
            "score": 121.01928476442328,
            "bg_count": 3
          },
          {
            "key": "dead",
            "doc_count": 4,
            "score": 45.42858478985534,
            "bg_count": 13
          },
          {
            "key": "awhile",
            "doc_count": 3,
            "score": 36.49997548041267,
            "bg_count": 9
          },
          {
            "key": "life",
            "doc_count": 5,
            "score": 29.934089933945792,
            "bg_count": 31
          }
        ]
      }
    }
  }
}
```

## 回應本文欄位

下表列出回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `doc_count` | 整數 | 樣本中的文件數量（在 sampler 層級）或前景集合中的文件數量（在 significant_text 層級）。 |
| `bg_count` | 整數 | 用於比較的背景集合中的文件總數。 |
| `buckets` | 陣列 | 顯著詞彙的桶，依 `score` 遞減排序。 |
| `buckets.key` | 字串 | 顯著詞彙。 |
| `buckets.doc_count` | 整數 | 前景集合中包含此詞彙的文件數量。 |
| `buckets.score` | 雙精度浮點數 | 顯著性分數，表示此詞彙在前景中出現的頻率比背景高出多少。 |
| `buckets.bg_count` | 整數 | 背景集合中包含此詞彙的文件數量。 |

## 顯著性啟發式方法

預設情況下，顯著性分數使用 JLH 啟發式方法。您可以在 `field` 旁加入其他評分演算法的名稱作為參數，以選用該演算法。支援下列啟發式方法。

| 啟發式方法 | 參數 | 說明 |
| :--- | :--- | :--- |
| JLH | `jlh: {}` | 預設方法。衡量詞彙在前景與背景之間的普及程度相對變化。 |
| 互資訊 | `mutual_information: {}` | 衡量詞彙的出現對於判斷是否屬於前景集合提供多少資訊。支援 `include_negatives` 和 `background_is_superset` 選項。 |
| 卡方 | `chi_square: {}` | 檢定詞彙與前景集合之間獨立性的標準統計檢定。支援 `include_negatives` 和 `background_is_superset` 選項。 |
| GND | `gnd: {}` | Google 正規化距離。使用共同出現的比率衡量統計關聯性。支援 `background_is_superset` 選項。 |
| 百分比 | `percentage: {}` | 包含該詞彙的前景文件數與背景文件數的比率。極罕見的詞彙可能主導結果，因此請考慮提高 `min_doc_count`。 |
| 指令碼 | `script_heuristic: {}` | 由指令碼計算的自訂分數。指令碼可以使用 `_subset_freq`、`_superset_freq`、`_subset_size` 和 `_superset_size` 參數。 |

如需比較各啟發式方法的差異，請參閱[選擇啟發式方法]({{site.url}}{{site.baseurl}}/aggregations/bucket/significant-terms/#choosing-a-heuristic)。

下列範例使用卡方評分，取代預設的 JLH：

```json
GET /shakespeare/_search
{
  "size": 0,
  "query": {
    "match": {
      "text_entry": "breathe"
    }
  },
  "aggs": {
    "sample": {
      "sampler": {
        "shard_size": 100
      },
      "aggs": {
        "keywords": {
          "significant_text": {
            "field": "text_entry",
            "min_doc_count": 4,
            "chi_square": {}
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應顯示，識別出的詞彙相同，但分數尺度不同：

```json
{
  ...
  "aggregations" : {
    "sample" : {
      "doc_count" : 59,
      "keywords" : {
        "doc_count" : 59,
        "bg_count" : 111396,
        "buckets" : [
          {
            "key" : "breathe",
            "doc_count" : 59,
            "score" : 111396.0,
            "bg_count" : 59
          },
          {
            "key" : "air",
            "doc_count" : 4,
            "score" : 152.27540220402065,
            "bg_count" : 189
          },
          {
            "key" : "dead",
            "doc_count" : 4,
            "score" : 53.556852313941825,
            "bg_count" : 495
          },
          {
            "key" : "life",
            "doc_count" : 5,
            "score" : 49.44532193700098,
            "bg_count" : 805
          }
        ]
      }
    }
  }
}
```

## 篩除重複文字

自由文字欄位通常包含複製的文字，例如多個網站轉載的新聞稿、電子郵件回覆串、制式免責聲明或導覽選單。複製文字中的罕見詞彙，例如姓名或產品代號，會在每份副本中與您的搜尋詞彙一起出現，因此即使它們沒有實質意義，也可能主導結果。

若要在查詢時移除此雜訊，請將 `filter_duplicate_text` 設為 `true`。彙總分析最符合的文件時，會忽略先前已出現過、長度為 6 個以上詞元的任何序列。由於相似文件的排名往往接近，因此這能移除大部分複製的段落。

下列範例使用 `tech_news` 索引，其中數篇關於可觀測性的文章包含相同的制式段落，內容是關於獎項評審團。請建立索引。`all_text` 欄位將用於[下一節](#analyzing-fields-created-using-copy_to)：

```json
PUT tech_news
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "copy_to": "all_text"
      },
      "content": {
        "type": "text",
        "copy_to": "all_text"
      },
      "all_text": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

將下列文件編製索引：

```json
POST _bulk?refresh
{ "index": { "_index": "tech_news", "_id": "1" } }
{ "title": "Tracing comes to the edge", "content": "New observability agents collect traces from edge devices and forward spans to a central collector." }
{ "index": { "_index": "tech_news", "_id": "2" } }
{ "title": "Startup ships open telemetry pipeline", "content": "The observability startup released a pipeline that converts logs into metrics and traces for dashboards." }
{ "index": { "_index": "tech_news", "_id": "3" } }
{ "title": "Awards shortlist announced", "content": "The observability category of the cloud awards includes three tracing platforms. The awards jury includes Priya Ramaswamy, program director at Northwind Labs, and other industry experts." }
{ "index": { "_index": "tech_news", "_id": "4" } }
{ "title": "Finalists named for cloud awards", "content": "Judges selected observability finalists focused on traces and metrics. The awards jury includes Priya Ramaswamy, program director at Northwind Labs, and other industry experts." }
{ "index": { "_index": "tech_news", "_id": "5" } }
{ "title": "Cloud awards finalists revealed", "content": "Observability vendors with tracing dashboards lead the finalist list. The awards jury includes Priya Ramaswamy, program director at Northwind Labs, and other industry experts." }
{ "index": { "_index": "tech_news", "_id": "6" } }
{ "title": "Award nominees in observability", "content": "Several observability nominees offer metrics and tracing for containers. The awards jury includes Priya Ramaswamy, program director at Northwind Labs, and other industry experts." }
{ "index": { "_index": "tech_news", "_id": "7" } }
{ "title": "Metrics at scale", "content": "An observability team explains how it stores billions of metrics and traces per day." }
{ "index": { "_index": "tech_news", "_id": "8" } }
{ "title": "Quarterly earnings beat estimates", "content": "The retailer reported higher revenue and raised its forecast for the year." }
{ "index": { "_index": "tech_news", "_id": "9" } }
{ "title": "New phone launches", "content": "The manufacturer released a phone with a larger battery and a faster camera." }
{ "index": { "_index": "tech_news", "_id": "10" } }
{ "title": "City approves bike lanes", "content": "The council voted to add protected bike lanes downtown." }
{ "index": { "_index": "tech_news", "_id": "11" } }
{ "title": "Chip shortage eases", "content": "Suppliers report shorter lead times for processors and memory." }
{ "index": { "_index": "tech_news", "_id": "12" } }
{ "title": "Streaming service raises prices", "content": "Subscribers will pay more for the ad-free plan starting next month." }
{ "index": { "_index": "tech_news", "_id": "13" } }
{ "title": "Database release adds vector search", "content": "The new database version adds vector search and faster joins." }
{ "index": { "_index": "tech_news", "_id": "14" } }
{ "title": "Electric trucks enter service", "content": "A logistics company added electric trucks to its delivery fleet." }
{ "index": { "_index": "tech_news", "_id": "15" } }
{ "title": "Weather disrupts flights", "content": "Storms delayed hundreds of flights across the region." }
{ "index": { "_index": "tech_news", "_id": "16" } }
{ "title": "Robotics firm raises funding", "content": "The company will use the funding to expand warehouse automation." }
{ "index": { "_index": "tech_news", "_id": "17" } }
{ "title": "Programming language update", "content": "The release improves compile times and adds pattern matching." }
```
{% include copy-curl.html %}

下列請求會找出可觀測性相關文章中的顯著詞彙，且不篩除重複文字：

```json
GET tech_news/_search
{
  "size": 0,
  "query": {
    "match": {
      "content": "observability"
    }
  },
  "aggs": {
    "sample": {
      "sampler": {
        "shard_size": 100
      },
      "aggs": {
        "keywords": {
          "significant_text": {
            "field": "content"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

傳回的大部分詞彙，例如 `priya`、`ramaswamy`、`labs` 和 `director`，都來自複製的評審團段落：

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

```json
{
  "aggregations": {
    "sample": {
      "doc_count": 7,
      "keywords": {
        "doc_count": 7,
        "bg_count": 17,
        "buckets": [
          {
            "key": "observability",
            "doc_count": 7,
            "score": 1.4285714285714288,
            "bg_count": 7
          },
          {
            "key": "ramaswamy",
            "doc_count": 4,
            "score": 0.8163265306122448,
            "bg_count": 4
          },
          {
            "key": "priya",
            "doc_count": 4,
            "score": 0.8163265306122448,
            "bg_count": 4
          },
          {
            "key": "director",
            "doc_count": 4,
            "score": 0.8163265306122448,
            "bg_count": 4
          },
          {
            "key": "traces",
            "doc_count": 4,
            "score": 0.8163265306122448,
            "bg_count": 4
          },
          {
            "key": "includes",
            "doc_count": 4,
            "score": 0.8163265306122448,
            "bg_count": 4
          },
          {
            "key": "program",
            "doc_count": 4,
            "score": 0.8163265306122448,
            "bg_count": 4
          },
          {
            "key": "at",
            "doc_count": 4,
            "score": 0.8163265306122448,
            "bg_count": 4
          },
          {
            "key": "labs",
            "doc_count": 4,
            "score": 0.8163265306122448,
            "bg_count": 4
          },
          {
            "key": "metrics",
            "doc_count": 4,
            "score": 0.8163265306122448,
            "bg_count": 4
          }
        ]
      }
    }
  }
}
```
</details>

下列請求將 `filter_duplicate_text` 設為 `true`：

```json
GET tech_news/_search
{
  "size": 0,
  "query": {
    "match": {
      "content": "observability"
    }
  },
  "aggs": {
    "sample": {
      "sampler": {
        "shard_size": 100
      },
      "aggs": {
        "keywords": {
          "significant_text": {
            "field": "content",
            "filter_duplicate_text": true
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

複製的段落只計算一次，因此其中的詞彙不再達到 `min_doc_count` 的預設值 `3`。其餘詞彙，例如 `traces`、`metrics` 和 `tracing`，則描述文章的主題：

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

```json
{
  "aggregations": {
    "sample": {
      "doc_count": 7,
      "keywords": {
        "doc_count": 7,
        "bg_count": 17,
        "buckets": [
          {
            "key": "observability",
            "doc_count": 7,
            "score": 1.4285714285714288,
            "bg_count": 7
          },
          {
            "key": "traces",
            "doc_count": 4,
            "score": 0.8163265306122448,
            "bg_count": 4
          },
          {
            "key": "metrics",
            "doc_count": 4,
            "score": 0.8163265306122448,
            "bg_count": 4
          },
          {
            "key": "tracing",
            "doc_count": 3,
            "score": 0.6122448979591836,
            "bg_count": 3
          },
          {
            "key": "and",
            "doc_count": 6,
            "score": 0.18367346938775497,
            "bg_count": 12
          }
        ]
      }
    }
  }
}
```
</details>

如果您可以使用單值欄位（例如文章內文的雜湊值或原始新聞稿的 URL）來識別重複的文件，請改用 [`diversified_sampler`]({{site.url}}{{site.baseurl}}/aggregations/bucket/diversified-sampler/) 父彙總來從樣本中移除重複項目。在分析前移除重複文件，比在分析期間篩選重複文字更有效率。

## 分析使用 copy_to 建立的欄位

`significant_text` 彙總會從文件 `_source` 讀取文字。通常，索引欄位與來源欄位名稱相同。如果該欄位是使用 [`copy_to`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/copy-to/) 填入的，它就不存在於 `_source` 中，因此彙總不會傳回任何桶。若要分析這類欄位，請在 `source_fields` 中列出包含其文字的來源欄位。

在 `tech_news` 索引中，`title` 與 `content` 欄位會被複製到 `all_text`。下列請求會搜尋 `all_text`，並分析 `title` 與 `content` 來源欄位的文字：

```json
GET tech_news/_search
{
  "size": 0,
  "query": {
    "match": {
      "all_text": "observability"
    }
  },
  "aggs": {
    "sample": {
      "sampler": {
        "shard_size": 100
      },
      "aggs": {
        "keywords": {
          "significant_text": {
            "field": "all_text",
            "source_fields": [
              "title",
              "content"
            ]
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含來自標題與內容的重要詞彙：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "aggregations": {
    "sample": {
      "doc_count": 7,
      "keywords": {
        "doc_count": 7,
        "bg_count": 17,
        "buckets": [
          {
            "key": "observability",
            "doc_count": 7,
            "score": 1.4285714285714288,
            "bg_count": 7
          },
          {
            "key": "at",
            "doc_count": 5,
            "score": 1.0204081632653061,
            "bg_count": 5
          },
          {
            "key": "director",
            "doc_count": 4,
            "score": 0.8163265306122448,
            "bg_count": 4
          },
          {
            "key": "tracing",
            "doc_count": 4,
            "score": 0.8163265306122448,
            "bg_count": 4
          },
          {
            "key": "includes",
            "doc_count": 4,
            "score": 0.8163265306122448,
            "bg_count": 4
          },
          {
            "key": "traces",
            "doc_count": 4,
            "score": 0.8163265306122448,
            "bg_count": 4
          },
          {
            "key": "ramaswamy",
            "doc_count": 4,
            "score": 0.8163265306122448,
            "bg_count": 4
          },
          {
            "key": "priya",
            "doc_count": 4,
            "score": 0.8163265306122448,
            "bg_count": 4
          },
          {
            "key": "program",
            "doc_count": 4,
            "score": 0.8163265306122448,
            "bg_count": 4
          },
          {
            "key": "labs",
            "doc_count": 4,
            "score": 0.8163265306122448,
            "bg_count": 4
          }
        ]
      }
    }
  }
}
```
</details>

## size 與 shard_size

`size` 參數控制彙總傳回多少個桶。每個分片會先使用本機統計資料選出候選詞彙，再由協調節點將候選項目合併為最終清單。由於分片無法得知詞彙的全域頻率，合併後的清單可能遺漏某些詞彙，或包含稍微不準確的計數。

預設情況下（`shard_size` 為 `-1`），每個分片會傳回 `2 * (size * 1.5 + 10)` 個候選詞彙。低頻詞彙在所有結果合併後可能反而是最重要的，因此將 `shard_size` 設定得遠高於 `size` 可以改善結果，但代價是使用更多記憶體與網路流量。

## 最小文件數

`min_doc_count` 參數會排除出現在少於指定數量之前景文件中的詞彙。`3` 的預設值要求必須有一些證據證明詞彙是有意義的：只出現在一個文件中的詞彙通常是錯字或其他一次性出現。

`min_doc_count` 閾值只會在分片結果合併之後套用。每個分片會根據其本機分數選出候選項目，因此本機分數高的低頻詞彙可能會取代原本在全域能符合 `min_doc_count` 的詞彙。若要傳回這些詞彙，請提高 `shard_size`。

`shard_min_doc_count` 參數會在候選項目傳送至協調節點之前，於每個分片上進行篩選。您可以用它來捨棄不太可能達到 `min_doc_count` 的詞彙，例如拼字錯誤。請將 `shard_min_doc_count` 設定為遠低於 `min_doc_count` 除以分片數量的值。否則，重要詞彙可能會在個別分片上被篩除。

## 使用顯著文字彙總結果

來自自由文字的顯著詞彙，最常見的用途是作為另一個查詢的輸入。以下模式很常見：

- 尋找分類錯誤的文件：在結構化欄位中搜尋某個類別，在自由文字欄位上執行 `significant_text`，然後搜尋不屬於該類別但包含顯著詞彙的文件。結果就是可能屬於原始類別的文件。
- 為符合的文件排名：在搜尋這些詞彙時，使用每個顯著詞彙的分數作為 `boost` 值。若要平衡精確度與召回率，請在後續查詢中設定 `minimum_should_match`。高值會傳回較少但包含多數詞彙的文件，而 `1` 值則會傳回包含任一詞彙的所有文件。
- 在上下文中顯示詞彙：當讀者能看到詞彙出現的位置時，顯著詞彙會更容易解讀。在相同欄位中搜尋這些詞彙，並加入 [`highlight`]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/highlight/) 子句，以傳回顯示每個詞彙及其周圍文字的片段。

## 限制

`significant_text` 彙總有下列限制：

- 由於記憶體成本過高，不支援子彙總。若要進一步分析特定詞彙，請使用 `terms` 彙總與包含初始結果中重要詞彙的 `include` 子句，執行另一個查詢。
- 因為它處理的是文件的 JSON 來源，所以不支援巢狀物件。
- 文件計數是近似值。`doc_count` 值可能過低，因為某些分片未在其候選項目中傳回該詞彙；`bg_count` 值可能過高，因為背景計數可能包含已刪除的文件。若要提高準確度，請提高 `shard_size`。如需更多資訊，請參閱[大小與分片大小](#size-and-shard-size)。
