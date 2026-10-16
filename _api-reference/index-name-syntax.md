---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引名稱語法"
nav_order: 155
---

# 索引名稱語法

許多 OpenSearch REST API 在請求路徑中接受一或多個索引名稱。您可以在一個請求中指定多個索引、使用日期數學依日期選取索引，並防止請求在請求本文中指定索引。

## 指定多個索引

大多數在路徑中接受索引名稱的 API 可以同時在多個索引上執行。請以下列其中一種方式指定目標索引：

- 以逗號分隔的名稱清單，例如 `app-logs-2026.10.12,app-logs-2026.10.13`。
- 萬用字元模式，例如 `app-logs-*` 或 `*-logs-*`。
- `_all` 或 `*` 以指定所有索引。
- 排除項，會從前面的模式中移除索引。在名稱或模式前加上 `-`，例如 `app-logs-*,-app-logs-2026.10.11`。排除項必須至少接在一個包含性的名稱或模式之後。只包含 `-app-logs-2026.10.11` 的路徑會被解譯為字面索引名稱 `-app-logs-2026.10.11`。

下列請求會計算 2026 年建立的所有 `app-logs-` 索引中的文件數，但 `app-logs-2026.10.11` 除外：

```json
GET /app-logs-2026*,-app-logs-2026.10.11/_count
```
{% include copy-curl.html %}

針對單一文件或單一索引運作的 API，例如 [Index Document API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/index-document/)，不接受多個索引。這些 API 路徑中以逗號分隔的清單會被視為無效的索引名稱而遭拒絕。

支援多個索引的 API 接受下列查詢參數，這些參數控制 OpenSearch 如何解析目標索引。預設值取決於個別 API。

參數 | 資料類型 | 說明
:--- | :--- | :---
`ignore_unavailable` | 布林值 | 若為 `true`，OpenSearch 會忽略以名稱列出的遺失或已關閉索引。若為 `false`，指定遺失或已關閉索引的請求會失敗。
`allow_no_indices` | 布林值 | 若為 `true`，當萬用字元模式、別名或 `_all` 未符合任何索引時，請求仍會成功。若為 `false`，請求會失敗。例如，在預設的 `true` 下，針對 `nomatch-*` 的 Count API 請求會傳回 `0` 的計數。
`expand_wildcards` | 字串 | 萬用字元模式可比對的索引類型。接受以下值的逗號分隔清單：<br> - `open`：開啟的索引。<br> - `closed`：關閉的索引。<br> - `hidden`：隱藏索引，即啟用 [`index.hidden`]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/) 設定的索引。必須與 `open`、`closed` 或兩者合併使用。<br> - `all`：所有索引，包括隱藏索引。<br> - `none`：無索引。萬用字元模式不會展開。<br><br>對大多數 API 而言，預設值為 `open`，因此萬用字元模式不會比對隱藏索引，例如名稱以 `.` 開頭的索引。請指定 `expand_wildcards=open,hidden` 以包含它們。

## 索引名稱中的日期數學

如果您為時間序列資料每天或每月建立一個索引，可以在請求路徑中使用日期數學，依日期選取索引。例如，請求可以只指定本月與上個月的銷售索引，而不需要您的用戶端計算索引名稱，OpenSearch 也只會讀取這些索引。大多數在路徑中接受索引名稱的 API 都支援日期數學。例如，您可以使用日期數學為輪替所建立的索引命名。如需詳細資訊，請參閱[在索引輪替中使用日期數學]({{site.url}}{{site.baseurl}}/api-reference/index-apis/rollover/#using-date-math-with-index-rollovers)。

日期數學索引名稱具有下列格式：

```
<static_name{date_math_expression{date_format|time_zone}}>
```

下表說明日期數學索引名稱的組成部分。

組成部分 | 說明
:--- | :---
`static_name` | 名稱的固定部分，例如 `app-logs-`。
`date_math_expression` | 相對於 `now` 計算日期的運算式，例如 `now/d`（今天捨入至當日開始）或 `now/d-1d`（昨天）。運算式語法請參閱[日期數學]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/#date-math)。
`date_format` | 選用。計算出的日期寫入索引名稱時使用的格式。預設為 `yyyy.MM.dd`。格式模式區分大小寫：`MM` 是月份，`mm` 是分鐘，而 `HH` 是 24 小時制的小時，`hh` 是 12 小時制的小時。如需詳細資訊，請參閱[自訂格式]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/#custom-formats)。
`time_zone` | 選用。用來計算日期的時區，可以是位移值，例如 `+12:00`，或是 ID，例如 `America/Los_Angeles`。預設為 UTC。

整個運算式必須以角括號括住。若要在名稱的靜態部分使用 `{` 或 `}`，請使用反斜線（`\`）逸出該字元。

下表顯示當目前時間為 2026 年 10 月 13 日 18:00 UTC 時，各運算式的解析結果。

運算式 | 解析結果
:--- | :---
`<app-logs-{now/d}>` | `app-logs-2026.10.13`
`<app-logs-{now/d-1d}>` | `app-logs-2026.10.12`
`<app-logs-{now/w}>` | `app-logs-2026.10.12`（一週從星期一開始）
`<app-logs-{now-1h/h{yyyy.MM.dd.HH}}>` | `app-logs-2026.10.13.17`
`<app-logs-{now/d{yyyy.MM.dd\|Asia/Tokyo}}>` | `app-logs-2026.10.14`
`<sales-{now/M{yyyy-MM}}>` | `sales-2026-10`
`<app\{prod\}-{now/M}>` | `app{prod}-2026.10.01`

OpenSearch 使用格里曆（Gregorian calendar）解析日期數學，不受地區設定影響。

在請求 URL 中，您必須對日期數學運算式中的特殊字元進行百分比編碼。OpenSearch 會拒絕包含這些字元但未編碼的 URL。下表列出每個字元的編碼值。

字元 | 編碼值
:--- | :---
`<` | `%3C`
`>` | `%3E`
`/` | `%2F`
`{` | `%7B`
`}` | `%7D`
`\|` | `%7C`
`+` | `%2B`
`:` | `%3A`
`,` | `%2C`

下列請求會從當月與上個月的每月 `sales-` 索引計算 `west` 區域的總銷售額。編碼前，路徑的索引部分為 `<sales-{now/M-1M{yyyy-MM}}>,<sales-{now/M{yyyy-MM}}>`：

```json
GET /%3Csales-%7Bnow%2FM-1M%7Byyyy-MM%7D%7D%3E%2C%3Csales-%7Bnow%2FM%7Byyyy-MM%7D%7D%3E/_search
{
  "size": 0,
  "query": {
    "term": {
      "region": "west"
    }
  },
  "aggs": {
    "total_sales": {
      "sum": {
        "field": "amount"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 限制請求本文中的索引

Bulk、Multi-get 與 Multi-search API 允許請求本文中的每個項目指定自己的目標索引，覆寫請求路徑中的索引。如果您是根據請求 URL 控制索引的存取權，例如使用代理伺服器，使用者可能會透過在請求本文中指定不同的索引來繞過該控制。

若要防止這種情況，請在每個節點的 `opensearch.yml` 中將 `rest.action.multi.allow_explicit_index` 設為 `false`。這是靜態設定，因此必須重新啟動節點才會生效。預設為 `true`。當此設定為 `false` 時，這些 API 會拒絕任何本文指定索引的請求，即使該索引與路徑中的索引相符也一樣。請在請求路徑中指定目標索引：

```json
POST /orders/_bulk
{ "index": {} }
{ "product": "Trail running shoes" }
```
{% include copy-curl.html %}

## 相關文件

- [常用 REST 參數]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/)
- [支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)
- [Cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/cron-expressions/)
