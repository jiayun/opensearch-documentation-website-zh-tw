---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "日期直方圖"
parent: Bucket aggregations
nav_order: 20
redirect_from:
  - /query-dsl/aggregations/bucket/date-histogram/
---

# 日期直方圖彙總

`date_histogram` 彙總會將 [date]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/) 欄位中的文件分組為以時間為基礎的桶。您可以用它來按小時、天或月彙總指標、繪製流量趨勢圖，或填入時間序列儀表板。

## 選擇間隔

`date_histogram` 彙總支援兩種間隔樣式：

- `calendar_interval` 參數會將桶對齊日曆邊界，例如天、月或年。當您關注真實世界的日曆期間時使用，例如 `day`、`1M` 或 `year`。
- `fixed_interval` 參數使用以 [SI 單位](https://en.wikipedia.org/wiki/International_System_of_Units) 測量的確切持續時間。桶的長度一律相同，不受日光節約時間或月份長度影響，例如 `5m`、`12h` 或 `30d`。

### 日曆間隔

日曆間隔會考量長度不同的月份，以及因日光節約時間變更而變短或變長的天。下表中的每個間隔都有兩個等效名稱。日曆間隔不能是倍數。例如，`2d` 會傳回錯誤。若要多天的桶，請使用 `fixed_interval`。

| 間隔 | 說明 |
| :--- | :--- |
| `minute`、`1m` | 從每分鐘的第 00 秒開始。 |
| `hour`、`1h` | 從每小時的第 00 分 00 秒開始。 |
| `day`、`1d` | 從指定時區中每一天的開始（通常是午夜）開始。 |
| `week`、`1w` | 從每週的星期一開始。 |
| `month`、`1M` | 從每個月的第一天開始。 |
| `quarter`、`1q` | 從每一季的第一天開始：1 月 1 日、4 月 1 日、7 月 1 日或 10 月 1 日。 |
| `year`、`1y` | 從每年的 1 月 1 日開始。 |

### 固定間隔

固定間隔一律是相同的毫秒數，因此您可以指定單位的任意倍數，例如 `90m` 或 `12h`。由於月或季的長度會變動，這些單位不接受做為固定間隔。不支援小數值，例如 `2.5d`。若要指定小數間隔，請使用較小的單位，例如 `60h`。關於間隔中可使用的縮寫，請參閱[單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。

下表列出固定間隔可接受的單位。

| 單位 | 說明 |
| :--- | :--- |
| `ms` | 毫秒。 |
| `s` | 秒。每秒為 1,000 毫秒。 |
| `m` | 分。每分為 60 秒。 |
| `h` | 小時。每小時為 60 分。 |
| `d` | 天。每天正好是 24 小時，不受日光節約時間變更影響。 |

固定間隔的桶會對齊 Unix 紀元的開始，而不是一天的開始。例如，當 `fixed_interval` 為 `90m` 時，桶會從 07:30 和 09:00 UTC 等時間開始。若要位移桶的開始時間，請使用 [`offset`](#example-shift-bucket-start-times-using-an-offset) 參數。

### 桶索引鍵

每個桶都包含一個 `key`，這是桶的開始時間，以自 Unix 紀元以來的毫秒數表示，以及一個 `key_as_string`，這是格式化為日期字串的相同時間。`key_as_string` 會使用 `format` 參數中指定的日期格式。如果您未指定 `format`，OpenSearch 會使用欄位對應中的日期格式。

OpenSearch 會將每份文件的日期值向下捨入至間隔的開始，藉此將文件放入桶中。如果您指定 `time_zone`，OpenSearch 會將值轉換為當地時間、向下捨入，再將結果轉換回 UTC。`key` 一律為 UTC 毫秒，而 `key_as_string` 則以要求的時區顯示。

`date_histogram` 彙總也適用於 [`date_range`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/range/) 欄位。文件會在其範圍重疊的每個桶中各計一次。例如，從 3 月 31 日到 4 月 2 日的預訂會計入 3 月 31 日、4 月 1 日和 4 月 2 日的每日桶中。

舊版 `interval` 欄位為了相容性而保留，但已棄用。請改用 `calendar_interval` 或 `fixed_interval`。
{: .note}


## 參數

`date_histogram` 彙總支援下列參數。

| 參數 | 必要 | 類型 | 說明 |
|:--|:--|:--|:--|
| `field` | 下列其中一項為必要：`field` 或 `script`。 | 字串 | 要建立桶的日期欄位。 |
| `calendar_interval` | 下列其中一項為必要：`calendar_interval`、`fixed_interval` 或舊版 `interval`。 | 字串 | 日曆感知間隔（例如 `day`、`1M`、`year`）。僅支援單數日曆單位。 |
| `fixed_interval` | 下列其中一項為必要：`calendar_interval`、`fixed_interval` 或舊版 `interval`。 | 字串 | 固定間隔，例如 `5m`、`12h`、`30d`。不適用於月或季等日曆單位。 |
| `time_zone` | 選用 | 字串 | 用於建立桶及格式化的時區。接受時區，例如 `Europe/Dublin`，或 UTC 位移，例如 `-07:00`。 |
| `format` | 選用 | 字串 | 用於 `key_as_string` 的輸出日期格式，例如 `yyyy-MM-dd`。若省略，則套用對應預設值。 |
| `offset` | 選用 | 字串 | 以正或負間隔位移桶邊界，例如 `+8h`、`-30m`。在套用 `time_zone` 之後計算。 |
| `min_doc_count` | 選用 | 整數 | 傳回桶所需的最少文件數。預設為 `0`，會包含第一份與最後一份文件之間的空桶。若要在資料範圍之外包含空桶，請使用 `extended_bounds`。 |
| `extended_bounds` | 選用 | 物件 | 將桶的範圍延伸到您的資料之外：`{"min": "<date>", "max": "<date>"}`。 |
| `hard_bounds` | 選用 | 物件 | 嚴格將桶限制在某個範圍內：`{"min": "<date>", "max": "<date>"}`。範圍外的桶一律不會建立。 |
| `missing` | 選用 | 日期字串 | 將缺少該欄位的文件視為具有此日期值。 |
| `keyed` | 選用 | 布林值 | 當設為 `true` 時，會以格式化日期字串為索引鍵的物件形式傳回桶。 |
| `order` | 選用 | 物件 | 依 `_key` 或 `_count` 以遞增或遞減順序排序桶。 |
| `script` | 下列其中一項為必要：`field` 或 `script`。 | 物件 | 為每份文件產生日期值的指令碼，或與 `field` 搭配使用時修改每個欄位值的指令碼。指令碼會在每份相符的文件上執行，因此會增加額外負荷。如需詳細資訊，請參閱[範例：使用指令碼](#example-use-a-script)。 |

## 範例設定

本頁的範例使用一個 `my-logs` 索引，其中包含 2025 年 3 月 30 日歐洲日光節約時間開始前後的時間戳記。建立索引：

```json
PUT my-logs
{
  "mappings": {
    "properties": {
      "timestamp": { "type": "date" }
    }
  }
}
```
{% include copy-curl.html %}

將下列文件編製索引：

```json
POST my-logs/_bulk?refresh
{ "index": { "_id": "1" } }
{ "timestamp": "2025-03-31T08:10:00Z" }
{ "index": { "_id": "2" } }
{ "timestamp": "2025-03-31T08:40:00Z" }
{ "index": { "_id": "3" } }
{ "timestamp": "2025-03-31T10:05:00Z" }
{ "index": { "_id": "4" } }
{ "timestamp": "2025-03-31T23:30:00Z" }
{ "index": { "_id": "5" } }
{ "timestamp": "2025-04-01T05:15:00Z" }
{ "index": { "_id": "6" } }
{ "timestamp": "2025-04-01T14:20:00Z" }
{ "index": { "_id": "7" } }
{ "timestamp": "2025-04-02T09:00:00Z" }
```
{% include copy-curl.html %}

## 範例：每月桶（日曆間隔）

下列請求會計算每個日曆月份的文件數量：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "logs_per_month": {
      "date_histogram": {
        "field": "timestamp",
        "calendar_interval": "1M"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應中會包含一個三月的桶和一個四月的桶：

```json
{
  "aggregations": {
    "logs_per_month": {
      "buckets": [
        {
          "key_as_string": "2025-03-01T00:00:00.000Z",
          "key": 1740787200000,
          "doc_count": 4
        },
        {
          "key_as_string": "2025-04-01T00:00:00.000Z",
          "key": 1743465600000,
          "doc_count": 3
        }
      ]
    }
  }
}
```

## 範例：統一的每小時桶（固定間隔）

下列請求會擷取固定間隔正好為 1 小時的桶，不受日光節約時間變更影響：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "by_hour": {
      "date_histogram": {
        "field": "timestamp",
        "fixed_interval": "1h"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應中包含 50 個每小時桶，從 `2025-03-31T08:00:00.000Z` 到 `2025-04-02T09:00:00.000Z`。因為 `min_doc_count` 預設為 `0`，回應會包含第一份與最後一份文件之間各小時的空桶。

## 範例：使用時區

根據預設，分桶會以 UTC 進行。設定 `time_zone` 可將桶的邊界對齊特定時區。

下列請求會使用 `Europe/Dublin` 擷取每日桶：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "by_day_ie": {
      "date_histogram": {
        "field": "timestamp",
        "calendar_interval": "day",
        "time_zone": "Europe/Dublin"
      }
    }
  }
}
```
{% include copy-curl.html %}

2025 年 3 月 30 日之後，都柏林比 UTC 快一小時，因此文件 4（`2025-03-31T23:30:00Z`）在都柏林時間會落在 4 月 1 日。在 UTC 中，這三個每日桶分別包含 4、2 和 1 份文件。在都柏林時間中，則分別包含 3、3 和 1 份文件。每個 `key_as_string` 會顯示都柏林的午夜（`+01:00`），而每個 `key` 則是同一時刻的 UTC 毫秒數：

```json
{
  "aggregations": {
    "by_day_ie": {
      "buckets": [
        {
          "key_as_string": "2025-03-31T00:00:00.000+01:00",
          "key": 1743375600000,
          "doc_count": 3
        },
        {
          "key_as_string": "2025-04-01T00:00:00.000+01:00",
          "key": 1743462000000,
          "doc_count": 3
        },
        {
          "key_as_string": "2025-04-02T00:00:00.000+01:00",
          "key": 1743548400000,
          "doc_count": 1
        }
      ]
    }
  }
}
```

>   在採用日光節約時間的時區中，包含時間變更的桶可能會比要求的間隔更短或更長。例如，在 `Europe/Dublin` 時區中：
>
>   - 2025 年 3 月 30 日的每日桶，在時鐘往前撥時，只涵蓋 23 小時；而 2025 年 10 月 26 日的每日桶，在時鐘往後撥時，則涵蓋 25 小時。
>   - 時鐘往後撥時，每小時桶不會被延長。相反地，重複的那一小時會以兩個獨立的桶呈現，具有相同的當地時間但不同的位移，例如 `2025-10-26T01:00:00.000+01:00` 和 `2025-10-26T01:00:00.000Z`。
>   - 如果桶的邊界落在因時鐘往前撥而不存在的當地時間，該邊界會移到下一個有效時間。例如，當 `offset` 為 `+1h` 時，3 月 30 日的桶會從 02:00 開始，而不是 01:00。
{: .warning}

請在時間變更前後測試您的彙總，以確保桶符合您的預期，並讓所有伺服器和用戶端與可靠的時間來源（例如 NTP）保持同步。
{: .tip}

## 範例：使用位移調整桶的開始時間

使用 `offset` 參數可將桶的邊界往前或往後移動，例如定義一個從 08:00 到 08:00（而非午夜到午夜）的「報告日」：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "by_day_shifted": {
      "date_histogram": {
        "field": "timestamp",
        "calendar_interval": "day",
        "offset": "+8h"
      }
    }
  }
}
```
{% include copy-curl.html %}

文件 1--5 是在 3 月 31 日 08:00 到 4 月 1 日 08:00 之間記錄的，因此它們全都計入從 3 月 31 日開始的報告日：

```json
{
  "aggregations": {
    "by_day_shifted": {
      "buckets": [
        {
          "key_as_string": "2025-03-31T08:00:00.000Z",
          "key": 1743408000000,
          "doc_count": 5
        },
        {
          "key_as_string": "2025-04-01T08:00:00.000Z",
          "key": 1743494400000,
          "doc_count": 1
        },
        {
          "key_as_string": "2025-04-02T08:00:00.000Z",
          "key": 1743580800000,
          "doc_count": 1
        }
      ]
    }
  }
}
```

## 範例：在固定時間範圍內包含空桶

根據預設，`min_doc_count` 為 `0`，因此直方圖會包含第一份與最後一份相符文件之間的空桶。若要為整個時間範圍（包括範圍開頭和結尾沒有文件的時段）傳回空桶，請在 `extended_bounds` 中提供該範圍。`extended_bounds` 參數只會新增桶，不會篩選文件，因此請使用 `range` 查詢將文件限制在相同的範圍內。

下列請求會擷取 2025 年 3 月 31 日 06:00–12:00 的每小時桶，包括沒有資料的時段：

```json
GET my-logs/_search
{
  "size": 0,
  "query": {
    "range": {
      "timestamp": {
        "gte": "2025-03-31T06:00:00Z",
        "lt": "2025-03-31T12:00:00Z"
      }
    }
  },
  "aggs": {
    "morning": {
      "date_histogram": {
        "field": "timestamp",
        "fixed_interval": "1h",
        "extended_bounds": {
          "min": "2025-03-31T06:00:00Z",
          "max": "2025-03-31T11:00:00Z"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應中會包含該範圍內每個小時的桶，包括 06:00、07:00、09:00 和 11:00 的空桶：

```json
{
  "aggregations": {
    "morning": {
      "buckets": [
        {
          "key_as_string": "2025-03-31T06:00:00.000Z",
          "key": 1743400800000,
          "doc_count": 0
        },
        {
          "key_as_string": "2025-03-31T07:00:00.000Z",
          "key": 1743404400000,
          "doc_count": 0
        },
        {
          "key_as_string": "2025-03-31T08:00:00.000Z",
          "key": 1743408000000,
          "doc_count": 2
        },
        {
          "key_as_string": "2025-03-31T09:00:00.000Z",
          "key": 1743411600000,
          "doc_count": 0
        },
        {
          "key_as_string": "2025-03-31T10:00:00.000Z",
          "key": 1743415200000,
          "doc_count": 1
        },
        {
          "key_as_string": "2025-03-31T11:00:00.000Z",
          "key": 1743418800000,
          "doc_count": 0
        }
      ]
    }
  }
}
```

## 範例：嚴格限制範圍

`hard_bounds` 會將直方圖嚴格限制在指定的最小與最大時間範圍內。即使資料落在這些界限之外，也不會在界限外建立任何桶。

下列請求會擷取 `2025-03-31T08:00:00Z` 到 `2025-03-31T11:00:00Z` 期間、固定間隔為 30 分鐘的桶：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "strict_range": {
      "date_histogram": {
        "field": "timestamp",
        "fixed_interval": "30m",
        "hard_bounds": {
          "min": "2025-03-31T08:00:00Z",
          "max": "2025-03-31T11:00:00Z"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應中只會包含界限內的桶。界限外的文件（例如文件 4）不會被計入：

```json
{
  "aggregations": {
    "strict_range": {
      "buckets": [
        {
          "key_as_string": "2025-03-31T08:00:00.000Z",
          "key": 1743408000000,
          "doc_count": 1
        },
        {
          "key_as_string": "2025-03-31T08:30:00.000Z",
          "key": 1743409800000,
          "doc_count": 1
        },
        {
          "key_as_string": "2025-03-31T09:00:00.000Z",
          "key": 1743411600000,
          "doc_count": 0
        },
        {
          "key_as_string": "2025-03-31T09:30:00.000Z",
          "key": 1743413400000,
          "doc_count": 0
        },
        {
          "key_as_string": "2025-03-31T10:00:00.000Z",
          "key": 1743415200000,
          "doc_count": 1
        }
      ]
    }
  }
}
```

## 範例：傳回桶的對應表

設定 `keyed: true`，以格式化的日期字串作為鍵，將桶以物件形式傳回：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "per_month": {
      "date_histogram": {
        "field": "timestamp",
        "calendar_interval": "1M",
        "format": "yyyy-MM-dd",
        "keyed": true
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含以月份作為鍵的物件：

```json
{
  "aggregations": {
    "per_month": {
      "buckets": {
        "2025-03-01": {
          "key_as_string": "2025-03-01",
          "key": 1740787200000,
          "doc_count": 4
        },
        "2025-04-01": {
          "key_as_string": "2025-04-01",
          "key": 1743465600000,
          "doc_count": 3
        }
      }
    }
  }
}
```

## 範例：將缺少的日期視為固定值

使用 `missing` 參數，將沒有值的文件指派到指定日期的桶。這些文件會與具有該日期的文件計入同一個桶。下列範例使用 `news-articles` 索引，其中一篇文章沒有 `published_on`。建立索引並新增文件：

```json
PUT news-articles
{
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "published_on": { "type": "date" }
    }
  }
}
```
{% include copy-curl.html %}

```json
POST news-articles/_bulk?refresh
{ "index": { "_id": "1" } }
{ "title": "Cluster sizing basics", "published_on": "2023-06-12" }
{ "index": { "_id": "2" } }
{ "title": "Tuning shard allocation", "published_on": "2024-02-20" }
{ "index": { "_id": "3" } }
{ "title": "Snapshot strategies", "published_on": "2024-09-05" }
{ "index": { "_id": "4" } }
{ "title": "Draft: Upgrading to OpenSearch 3" }
```
{% include copy-curl.html %}

下列請求會計算每年的文章數，並將沒有 `published_on` 值的文章歸入 2022 年：

```json
GET news-articles/_search
{
  "size": 0,
  "aggs": {
    "published_per_year": {
      "date_histogram": {
        "field": "published_on",
        "calendar_interval": "year",
        "missing": "2022-01-01"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含一個 2022 年的桶，其中含有未標示日期的文章：

```json
{
  "aggregations": {
    "published_per_year": {
      "buckets": [
        {
          "key_as_string": "2022-01-01T00:00:00.000Z",
          "key": 1640995200000,
          "doc_count": 1
        },
        {
          "key_as_string": "2023-01-01T00:00:00.000Z",
          "key": 1672531200000,
          "doc_count": 1
        },
        {
          "key_as_string": "2024-01-01T00:00:00.000Z",
          "key": 1704067200000,
          "doc_count": 2
        }
      ]
    }
  }
}
```

## 範例：排序桶

依預設，傳回的桶會依 `_key` 遞增排序。如有需要，使用 `order` 參數改為遞減排序。`order` 參數也接受子彙總路徑，方式與 `terms` 彙總相同。如需詳細資訊，請參閱[排序順序]({{site.url}}{{site.baseurl}}/aggregations/bucket/terms/#sort-order)。

下列請求會擷取桶，並將最近的月份排在最前面：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "recent_months": {
      "date_histogram": {
        "field": "timestamp",
        "calendar_interval": "1M",
        "order": {
          "_key": "desc"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

下列請求會依文件數排序每小時的桶，將文件數最多的桶排在最前面。此請求將 `min_doc_count` 設為 `1`，以排除沒有文件的小時：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "busiest_hours": {
      "date_histogram": {
        "field": "timestamp",
        "fixed_interval": "1h",
        "min_doc_count": 1,
        "order": {
          "_count": "desc"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應中的第一個桶為 `2025-03-31T08:00:00.000Z`，其中包含兩份文件。

## 範例：使用指令碼

您可以使用 Painless 指令碼，產生或修改用於分桶的日期值。如需詳細資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。指令碼會針對每份符合條件的文件執行，因此會增加額外負擔。

`date_histogram` 彙總支援兩種指令碼：

- 文件層級指令碼在 `script` 中指定，且不指定 `field`，會根據文件計算日期值。指令碼可以傳回日期物件或自紀元起算的毫秒數。
- 值指令碼在 `script` 中指定，並同時指定 `field`，會修改欄位的每個值。指令碼可透過 `_value` 取得欄位值，其單位為自紀元起算的毫秒數。

下列請求使用文件層級指令碼，傳回 `timestamp` 值，產生的桶與指定 `"field": "timestamp"` 時相同：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "by_hour_script": {
      "date_histogram": {
        "script": {
          "lang": "painless",
          "source": "doc['timestamp'].value"
        },
        "fixed_interval": "1h"
      }
    }
  }
}
```
{% include copy-curl.html %}

下列請求使用值指令碼，在分桶之前將每個 `timestamp` 值往後移一小時（3,600,000 毫秒）。因此，文件 4（`2025-03-31T23:30:00Z`）會計入 4 月 1 日：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "by_day_plus_one_hour": {
      "date_histogram": {
        "field": "timestamp",
        "script": {
          "lang": "painless",
          "source": "_value + 3600000"
        },
        "calendar_interval": "day"
      }
    }
  }
}
```
{% include copy-curl.html %}

每日的桶分別包含 3、3 和 1 份文件，而未使用指令碼時則分別為 4、2 和 1 份：

```json
{
  "aggregations": {
    "by_day_plus_one_hour": {
      "buckets": [
        {
          "key_as_string": "2025-03-31T00:00:00.000Z",
          "key": 1743379200000,
          "doc_count": 3
        },
        {
          "key_as_string": "2025-04-01T00:00:00.000Z",
          "key": 1743465600000,
          "doc_count": 3
        },
        {
          "key_as_string": "2025-04-02T00:00:00.000Z",
          "key": 1743552000000,
          "doc_count": 1
        }
      ]
    }
  }
}
```

## 範例：依星期幾彙總

若要依星期幾計算文件數，而不考慮日期，請使用 `terms` 彙總，搭配傳回星期幾的指令碼：

```json
GET my-logs/_search
{
  "size": 0,
  "aggs": {
    "day_of_week": {
      "terms": {
        "script": {
          "lang": "painless",
          "source": "doc['timestamp'].value.dayOfWeekEnum.value"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

桶的鍵為代表星期幾的數字，其中 `1` 為星期一，`7` 為星期日。回應顯示星期一（3 月 31 日）有四份文件，星期二有兩份，星期三有一份：

```json
{
  "aggregations": {
    "day_of_week": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "1",
          "doc_count": 4
        },
        {
          "key": "2",
          "doc_count": 2
        },
        {
          "key": "3",
          "doc_count": 1
        }
      ]
    }
  }
}
```
