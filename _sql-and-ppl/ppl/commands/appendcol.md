---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: appendcol
parent: Commands
grand_parent: PPL
nav_order: 6
---

<!-- vale off -->

# appendcol 命令

<!-- vale on -->

`appendcol` 命令會將子搜尋的結果以額外欄位的形式附加到輸入的搜尋結果（主搜尋）中。

## 語法

`appendcol` 命令的語法如下：

```sql
appendcol [override=<boolean>] <subsearch>
```

## 參數

`appendcol` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<subsearch>` | 必要 | 以次要搜尋的方式執行 PPL 命令。`subsearch` 會使用主搜尋結果中 `source` 子句所指定的資料作為其輸入。 |
| `override` | 選用 | 指定當欄位名稱衝突時，是否應覆寫主搜尋的結果。預設為 `false`。 |
  

## 範例 1：在現有結果旁附加不同的彙總

此範例同時顯示每個服務的記錄筆數與錯誤筆數。由於兩個查詢都依服務名稱分組，並使用相同的排序順序，因此資料列會正確對齊：

```sql
source=otellogs
| stats count() as total_logs by `resource.attributes.service.name`
| sort `resource.attributes.service.name`
| appendcol [ where severityText = 'ERROR' | stats count() as error_count by `resource.attributes.service.name` | sort `resource.attributes.service.name` ]
| fields `resource.attributes.service.name`, total_logs, error_count
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| resource.attributes.service.name | total_logs | error_count |
| --- | --- | --- |
| cart | 3 | 2 |
| checkout | 3 | 1 |
| frontend | 4 | 2 |
| frontend-proxy | 3 | 1 |
| payment | 2 | 1 |
| product-catalog | 4 | null |
| recommendation | 1 | null |

<!-- vale on -->

## 範例 2：附加多個子搜尋結果

下列查詢串連多個 `appendcol` 命令，在明細資料列旁加入摘要統計。第一個 `appendcol` 加入錯誤總數，第二個加入受影響的服務數量：

```sql
source=otellogs
| where severityText = 'ERROR'
| fields `resource.attributes.service.name`, severityText, body
| sort `resource.attributes.service.name`
| appendcol [ where severityText = 'ERROR' | stats count() as total_errors ]
| appendcol [ where severityText = 'ERROR' | stats distinct_count(`resource.attributes.service.name`) as services_affected ]
| head 4
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| resource.attributes.service.name | severityText | body | total_errors | services_affected |
| --- | --- | --- | --- | --- |
| checkout | ERROR | NullPointerException in CheckoutService.placeOrder at line 142 | 7 | 5 |
| checkout | ERROR | Kafka producer delivery failed: message too large for topic order-events (max 1048576 bytes) | null | null |
| frontend-proxy | ERROR | [2024-02-01T09:20:00.456Z] "POST /api/checkout HTTP/1.1" 503 - 0 30000 checkout-8d4f7b-mk2p9 | null | null |
| payment | ERROR | Payment failed: connection timeout to payment gateway after 30000ms | null | null |

<!-- vale on -->

## 範例 3：使用 override 參數解決欄位名稱衝突

當主搜尋與子搜尋共用同一個欄位名稱時，`override=true` 會以子搜尋的值取代主搜尋的值。在此範例中，兩者都會產生名為 `agg` 的欄位——主搜尋用它表示記錄總數，子搜尋用它表示僅錯誤的數量。使用 override 時，錯誤數量會取代總數：

```sql
source=otellogs
| stats count() as agg by severityText
| sort severityText
| appendcol override=true [ where severityText IN ('ERROR', 'WARN') | stats count() as agg by severityText | sort severityText ]
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| agg | severityText |
| --- | --- |
| 7 | ERROR |
| 4 | WARN |
| 6 | INFO |
| 4 | WARN |

<!-- vale on -->

## 限制

`appendcol` 命令有下列限制：

* **資料列對齊**：子搜尋結果會依位置（逐列）附加。如果主搜尋與子搜尋傳回的資料列數量不同，較短的結果集會以 `NULL` 值填補。
* **結構描述相容性**：當主搜尋與子搜尋中存在名稱相同但資料類型不相容的欄位時，查詢會失敗並產生錯誤。
