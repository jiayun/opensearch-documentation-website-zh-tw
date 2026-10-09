---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: multisearch
parent: Commands
grand_parent: PPL
nav_order: 29
---

<!-- vale off -->

# multisearch 命令

<!-- vale on -->


`multisearch` 命令會執行多個子搜尋並合併其結果。它可讓您在相同或不同來源上合併來自不同查詢的資料。您可以選擇性地對合併後的結果套用後續處理，例如彙總或排序。每個子搜尋可以有不同的篩選條件、資料轉換和欄位選取。

`multisearch` 命令對於比較分析、聯集運算，以及從多個搜尋條件建立完整資料集特別有用。處理時間序列資料時，此命令支援依時間戳記交錯排列結果。

`multisearch` 適用於：

* **比較分析**：比較不同區隔、地區或時間週期的指標。
* **成功率監控**：透過比較成功與總運算次數來計算成功率。
* **多來源資料合併**：合併來自不同索引的資料，或對相同來源套用不同的篩選條件。
* **A/B 測試分析**：合併不同測試群組的結果以進行比較。
* **時間序列資料合併**：依時間戳記交錯排列來自多個來源的事件。
 
  

## 語法

`multisearch` 命令的語法如下：

```sql
multisearch <subsearch1> <subsearch2> [<subsearch3> ...]
```

以下為 `multisearch` 命令語法的範例：

```sql
| multisearch [search source=table | where condition1] [search source=table | where condition2]
| multisearch [search source=index1 | fields field1, field2] [search source=index2 | fields field1, field2]
| multisearch [search source=table | where status="success"] [search source=table | where status="error"]
```

## 參數

`multisearch` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<subsearchN>` | 必要 | 至少需要兩個子搜尋。每個子搜尋必須以方括號括住，並以 `search` 關鍵字 (`[search source=index | <commands>]`) 開頭。子搜尋內支援所有 PPL 命令。 |
| `<result-processing>` | 選用 | 在 `multisearch` 運算之後套用至合併結果的命令 (例如 `stats`、`sort` 或 `head`)。 |  

## 範例 1：比較錯誤記錄檔與偵錯記錄檔

此範例將錯誤記錄檔與偵錯記錄檔並排合併。當您調查相同服務的偵錯層級記錄檔是否提供錯誤根本原因的線索時，這非常有用：
  
```sql
| multisearch [search source=otellogs
| where severityText = 'ERROR'
| eval env = 'errors'
| fields env, `resource.attributes.service.name`, body] [search source=otellogs
| where severityText = 'DEBUG'
| eval env = 'debug'
| fields env, `resource.attributes.service.name`, body]
| sort env, `resource.attributes.service.name`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| env | resource.attributes.service.name | body |
| --- | --- | --- |
| debug | cart | Cache miss for key user:session:U200 in Valkey cluster |
| debug | cart | Valkey SETEX user:session:U300 3600 - session refreshed |
| debug | product-catalog | gRPC call /ProductCatalogService/GetProduct completed in 12ms |
| errors | checkout | NullPointerException in CheckoutService.placeOrder at line 142 |
| errors | checkout | Kafka producer delivery failed: message too large for topic order-events (max 1048576 bytes) |
| errors | frontend-proxy | [2024-02-01T09:20:00.456Z] "POST /api/checkout HTTP/1.1" 503 - 0 30000 checkout-8d4f7b-mk2p9 |
| errors | payment | Payment failed: connection timeout to payment gateway after 30000ms |
| errors | payment | Out of memory: Java heap space - shutting down pod payment-6f8d4b-ht7q3 |
| errors | product-catalog | Database primary node unreachable: connection refused to db-primary-01:5432 |
| errors | recommendation | Failed to process recommendation request: invalid product ID from 203.0.113.50 |

<!-- vale on -->
  

## 範例 2：依嚴重性層級分割記錄檔

此範例將嚴重與非嚴重的記錄檔分開，以進行比較分析：
  
```sql
| multisearch [search source=otellogs
| where severityNumber >= 17
| eval tier = "critical"
| fields severityText, severityNumber, tier] [search source=otellogs
| where severityNumber < 17 AND severityNumber >= 13
| eval tier = "warning"
| fields severityText, severityNumber, tier]
| sort - severityNumber
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | severityNumber | tier |
| --- | --- | --- |
| ERROR | 17 | critical |
| ERROR | 17 | critical |
| ERROR | 17 | critical |
| ERROR | 17 | critical |
| ERROR | 17 | critical |
| ERROR | 17 | critical |
| ERROR | 17 | critical |
| WARN | 13 | warning |
| WARN | 13 | warning |
| WARN | 13 | warning |
| WARN | 13 | warning |

<!-- vale on -->
  

## 範例 3：合併來自多個來源的時間序列資料

此範例示範如何在維持時間先後順序的情況下，合併來自不同來源的時間序列資料。結果會自動依時間戳記排序，以建立統一的時間軸：
  
```sql
| multisearch [search source=time_data
| where category IN ("A", "B")] [search source=time_data2
| where category IN ("E", "F")]
| fields @timestamp, category, value, timestamp
| head 5
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| @timestamp | category | value | timestamp |
| --- | --- | --- | --- |
| 2025-08-01 04:00:00 | E | 2001 | 2025-08-01 04:00:00 |
| 2025-08-01 03:47:41 | A | 8762 | 2025-08-01 03:47:41 |
| 2025-08-01 02:30:00 | F | 2002 | 2025-08-01 02:30:00 |
| 2025-08-01 01:14:11 | B | 9015 | 2025-08-01 01:14:11 |
| 2025-08-01 01:00:00 | E | 2003 | 2025-08-01 01:00:00 |

<!-- vale on -->
  

## 範例 4：處理子搜尋之間缺少的欄位

此範例示範 `multisearch` 如何在子搜尋傳回不同欄位時處理結構描述差異。當某個子搜尋包含其他子搜尋沒有的欄位時，缺少的值會自動以 null 填入：
  
```sql
| multisearch [search source=otellogs
| where severityText = 'ERROR'
| eval needs_page = "yes"
| fields severityText, `resource.attributes.service.name`, needs_page] [search source=otellogs
| where severityText = 'WARN'
| fields severityText, `resource.attributes.service.name`]
| sort `resource.attributes.service.name`
| head 5
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | resource.attributes.service.name | needs_page |
| --- | --- | --- |
| ERROR | checkout | yes |
| ERROR | checkout | yes |
| ERROR | frontend-proxy | yes |
| WARN | frontend-proxy | null |
| WARN | frontend-proxy | null |

<!-- vale on -->
  

## 限制

`multisearch` 命令有下列限制：

* 至少必須指定兩個子搜尋。
* 當子搜尋之間存在名稱相同但類型不相容的欄位時，系統會透過重新命名衝突的欄位自動解決衝突。第一次出現的欄位保留原始名稱，後續衝突的欄位則會以數字後綴重新命名 (例如 `age` 會變成 `age0`、`age1`，依此類推)。這可確保在維持結構描述一致性的同時保留所有資料。  