---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: dedup
parent: Commands
grand_parent: PPL
nav_order: 11
---

<!-- vale off -->

# dedup 命令

<!-- vale on -->

`dedup` 命令會從搜尋結果中移除由指定欄位所定義的重複文件。


## 語法

`dedup` 命令的語法如下：

```sql
dedup [int] <field-list> [keepempty=<bool>] [consecutive=<bool>]
```

## 參數

`dedup` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<field-list>` | 必要 | 用於去除重複的欄位清單，以逗號分隔。至少需要一個欄位。 |
| `<int>` | 選用 | 每種組合要保留的重複文件數量。必須大於 `0`。預設為 `1`。 |
| `keepempty` | 選用 | 設定為 `true` 時，會保留欄位清單中任一欄位具有 `NULL` 值或缺少值的文件。預設為 `false`。 |
| `consecutive` | 選用 | 設定為 `true` 時，只會移除連續的重複文件。預設為 `false`。需要舊版 SQL 引擎 (`plugins.calcite.enabled=false`)。 |
  

## 範例 1：根據單一欄位去除重複  

下列查詢依服務名稱去除重複，以取得每個服務的一筆錯誤範例，讓您快速掌握系統中哪些地方發生故障：
  
```sql
source=otellogs
| where severityText IN ('ERROR', 'WARN')
| dedup `resource.attributes.service.name`
| sort `resource.attributes.service.name`
| fields `resource.attributes.service.name`, severityText, body
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| resource.attributes.service.name | severityText | body |
| --- | --- | --- |
| checkout | ERROR | NullPointerException in CheckoutService.placeOrder at line 142 |
| frontend-proxy | ERROR | [2024-02-01T09:20:00.456Z] "POST /api/checkout HTTP/1.1" 503 - 0 30000 checkout-8d4f7b-mk2p9 |
| payment | ERROR | Payment failed: connection timeout to payment gateway after 30000ms |
| product-catalog | WARN | Slow query detected: SELECT \* FROM products WHERE category = 'electronics' took 3200ms |
| recommendation | ERROR | Failed to process recommendation request: invalid product ID from 203.0.113.50 |

<!-- vale on -->
  

## 範例 2：保留多筆重複文件  

下列查詢為每個嚴重性等級最多保留兩筆記錄，提供每個等級更廣泛的樣本，協助您了解問題的多樣性：
  
```sql
source=otellogs
| dedup 2 severityText
| sort severityNumber
| fields severityText, severityNumber
| head 6
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | severityNumber |
| --- | --- |
| DEBUG | 5 |
| DEBUG | 5 |
| INFO | 9 |
| INFO | 9 |
| WARN | 13 |
| WARN | 13 |

<!-- vale on -->
  

## 範例 3：處理欄位值為空的文件  

下列查詢依檢測範圍名稱去除重複，以查看哪些 OTel SDK 正在回報。預設情況下，具有 null 值的記錄會被捨棄：
  
```sql
source=otellogs
| dedup instrumentationScope.name
| fields instrumentationScope.name
| sort instrumentationScope.name
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| instrumentationScope.name |
| --- |
| @opentelemetry/instrumentation-http |
| Microsoft.Extensions.Hosting |
| go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc |

<!-- vale on -->
  
下列查詢在去除重複時，會忽略指定欄位值為空的文件：
  
```sql
source=otellogs
| dedup instrumentationScope.name
| fields instrumentationScope.name
| sort instrumentationScope.name
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| instrumentationScope.name |
| --- |
| @opentelemetry/instrumentation-http |
| Microsoft.Extensions.Hosting |
| go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc |

<!-- vale on -->
  

## 範例 4：去除連續文件的重複  

下列查詢會移除重複的連續文件。當記錄檔依嚴重性排序時，這會顯示嚴重性等級之間的轉換，協助您看出升溫的模式：
  
```sql
source=otellogs
| sort severityNumber, `resource.attributes.service.name`
| dedup severityText consecutive=true
| fields severityText, `resource.attributes.service.name`
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | resource.attributes.service.name |
| --- | --- |
| DEBUG | cart |
| INFO | cart |
| WARN | frontend-proxy |
| ERROR | checkout |

<!-- vale on -->
  