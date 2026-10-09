---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: where
parent: Commands
grand_parent: PPL
nav_order: 53
---

<!-- vale off -->

# where 命令

<!-- vale on -->

`where` 命令用於篩選搜尋結果，只會傳回符合指定條件的結果。

## 語法

`where` 命令的語法如下：

```sql
where <boolean-expression>
```

## 參數

`where` 命令支援下列參數。

| 參數 | 必要／選用 | 說明 |
| --- | --- | --- |
| `<boolean-expression>` | 必要 | 用於篩選結果的條件。只會傳回此條件評估為 `true` 的資料列。 |

## 範例 1：依嚴重性等級篩選

下列查詢會找出所有嚴重性等級高於 `INFO` (severityNumber > 9) 的記錄項目，篩除例行記錄檔，以聚焦於警告與錯誤：

```sql
source=otellogs
| where severityNumber > 9
| sort severityNumber, `resource.attributes.service.name`
| fields severityText, severityNumber, `resource.attributes.service.name`
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| severityText | severityNumber | resource.attributes.service.name |
| --- | --- | --- |
| WARN | 13 | frontend-proxy |
| WARN | 13 | frontend-proxy |
| WARN | 13 | product-catalog |
| WARN | 13 | product-catalog |
| ERROR | 17 | checkout |
| ERROR | 17 | checkout |
| ERROR | 17 | frontend-proxy |
| ERROR | 17 | payment |
| ERROR | 17 | payment |
| ERROR | 17 | product-catalog |
| ERROR | 17 | recommendation |

<!-- vale on -->

## 範例 2：使用組合條件篩選

下列查詢在事件調查期間，使用 `AND` 結合嚴重性與服務名稱條件，將錯誤縮小至特定服務：

```sql
source=otellogs
| where severityNumber >= 17 AND `resource.attributes.service.name` = 'payment'
| fields severityText, severityNumber, `resource.attributes.service.name`
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| severityText | severityNumber | resource.attributes.service.name |
| --- | --- | --- |
| ERROR | 17 | payment |
| ERROR | 17 | payment |

<!-- vale on -->


## 範例 3：以多個可能值篩選

下列查詢使用 `OR` 同時比對任一條件，擷取所有警告與錯誤：

```sql
source=otellogs
| where severityText = 'WARN' or severityText = 'ERROR'
| fields severityText, `resource.attributes.service.name`, body
| head 5
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| severityText | resource.attributes.service.name | body |
| --- | --- | --- |
| WARN | product-catalog | Slow query detected: SELECT \* FROM products WHERE category = 'electronics' took 3200ms |
| ERROR | payment | Payment failed: connection timeout to payment gateway after 30000ms |
| ERROR | checkout | NullPointerException in CheckoutService.placeOrder at line 142 |
| ERROR | payment | Out of memory: Java heap space - shutting down pod payment-6f8d4b-ht7q3 |
| WARN | product-catalog | Connection pool 80% utilized on database replica db-replica-02 |

<!-- vale on -->
  

## 範例 4：依文字模式篩選 

`LIKE` 運算子可使用萬用字元對字串欄位進行模式比對。

### 以字首模式比對

下列查詢使用百分比符號 (`%`) 找出所有以 `frontend` 開頭的服務：

```sql
source=otellogs
| where LIKE(`resource.attributes.service.name`, 'frontend%')
| fields severityText, `resource.attributes.service.name`, body
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}

### 以萬用字元模式比對

下列查詢會找出名稱中包含 `product` 的所有服務記錄檔：

```sql
source=otellogs
| where LIKE(`resource.attributes.service.name`, '%product%')
| fields severityText, `resource.attributes.service.name`, body
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| severityText | resource.attributes.service.name | body |
| --- | --- | --- |
| WARN | product-catalog | Slow query detected: SELECT \* FROM products WHERE category = 'electronics' took 3200ms |
| WARN | product-catalog | Connection pool 80% utilized on database replica db-replica-02 |
| DEBUG | product-catalog | gRPC call /ProductCatalogService/GetProduct completed in 12ms |

<!-- vale on -->

## 範例 5：排除特定值進行篩選  

下列查詢使用 `NOT` 運算子排除例行的資訊與偵錯記錄檔，聚焦於需要留意的警告與錯誤：
  
```sql
source=otellogs
| where NOT severityText IN ('INFO', 'DEBUG')
| sort severityNumber, `resource.attributes.service.name`
| fields severityText, `resource.attributes.service.name`, body
| head 4
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | resource.attributes.service.name | body |
| --- | --- | --- |
| WARN | frontend-proxy | SSL certificate for api.example.com expires in 14 days |
| WARN | frontend-proxy | Rate limit threshold reached: 450/500 requests per minute for API key ending in ...abc789 |
| WARN | product-catalog | Slow query detected: SELECT \* FROM products WHERE category = 'electronics' took 3200ms |
| WARN | product-catalog | Connection pool 80% utilized on database replica db-replica-02 |

<!-- vale on -->
  

## 範例 6：使用值清單篩選  

下列查詢使用 `IN` 運算子一次比對多個嚴重性等級，擷取事件回應所需的所有錯誤與警告：
  
```sql
source=otellogs
| where severityText IN ('ERROR', 'WARN')
| sort severityNumber, `resource.attributes.service.name`
| fields severityText, `resource.attributes.service.name`, body
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | resource.attributes.service.name | body |
| --- | --- | --- |
| WARN | frontend-proxy | SSL certificate for api.example.com expires in 14 days |
| WARN | frontend-proxy | Rate limit threshold reached: 450/500 requests per minute for API key ending in ...abc789 |
| WARN | product-catalog | Slow query detected: SELECT \* FROM products WHERE category = 'electronics' took 3200ms |
| WARN | product-catalog | Connection pool 80% utilized on database replica db-replica-02 |
| ERROR | checkout | NullPointerException in CheckoutService.placeOrder at line 142 |
| ERROR | checkout | Kafka producer delivery failed: message too large for topic order-events (max 1048576 bytes) |
| ERROR | frontend-proxy | [2024-02-01T09:20:00.456Z] "POST /api/checkout HTTP/1.1" 503 - 0 30000 checkout-8d4f7b-mk2p9 |
| ERROR | payment | Payment failed: connection timeout to payment gateway after 30000ms |
| ERROR | payment | Out of memory: Java heap space - shutting down pod payment-6f8d4b-ht7q3 |
| ERROR | product-catalog | Database primary node unreachable: connection refused to db-primary-01:5432 |
| ERROR | recommendation | Failed to process recommendation request: invalid product ID from 203.0.113.50 |

<!-- vale on -->
  

## 範例 7：篩選缺少資料的記錄  

下列查詢會找出具有儀表化範圍中繼資料的記錄檔：
  
```sql
source=otellogs
| where NOT ISNULL(instrumentationScope.name)
| fields severityText, instrumentationScope.name
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | instrumentationScope.name |
| --- | --- |
| INFO | @opentelemetry/instrumentation-http |
| INFO | Microsoft.Extensions.Hosting |
| WARN | go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc |
| ERROR | @opentelemetry/instrumentation-http |

<!-- vale on -->
  

## 範例 8：使用分組條件篩選  

下列查詢透過結合嚴重性條件與服務篩選條件來調查特定服務的錯誤，並使用括號控制評估順序：
  
```sql
source=otellogs
| where (severityText = 'ERROR' OR severityText = 'WARN') AND `resource.attributes.service.name` = 'payment'
| sort severityNumber
| fields severityText, `resource.attributes.service.name`, body
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | resource.attributes.service.name | body |
| --- | --- | --- |
| ERROR | payment | Payment failed: connection timeout to payment gateway after 30000ms |
| ERROR | payment | Out of memory: Java heap space - shutting down pod payment-6f8d4b-ht7q3 |

<!-- vale on -->
  
