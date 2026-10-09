---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: head
parent: Commands
grand_parent: PPL
nav_order: 23
---

<!-- vale off -->

# head 命令

<!-- vale on -->

`head` 命令會從搜尋結果傳回前 N 行。

`head` 命令不會改寫為 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/index/)。它只會在協調節點上執行。
{: .note}

## 語法

`head` 命令的語法如下：

```sql
head [<size>] [from <offset>]
```

## 參數

`head` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<size>` | 選用 | 要傳回的結果數。必須是整數。預設為 `10`。 |
| `<offset>` | 選用 | 要略過的結果數 (與 `from` 關鍵字搭配使用)。必須是整數。預設為 `0`。 |
  

## 範例 1：使用預設大小擷取第一組結果

下列查詢會擷取最新的錯誤，並限制為預設的 10 筆結果。這是調查事件時常見的第一步：
  
```sql
source=otellogs
| where severityText IN ('ERROR', 'WARN')
| sort - severityNumber, `resource.attributes.service.name`
| fields severityText, `resource.attributes.service.name`, body
| head
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | resource.attributes.service.name | body |
| --- | --- | --- |
| ERROR | checkout | NullPointerException in CheckoutService.placeOrder at line 142 |
| ERROR | checkout | Kafka producer delivery failed: message too large for topic order-events (max 1048576 bytes) |
| ERROR | frontend-proxy | [2024-02-01T09:20:00.456Z] "POST /api/checkout HTTP/1.1" 503 - 0 30000 checkout-8d4f7b-mk2p9 |
| ERROR | payment | Payment failed: connection timeout to payment gateway after 30000ms |
| ERROR | payment | Out of memory: Java heap space - shutting down pod payment-6f8d4b-ht7q3 |
| ERROR | product-catalog | Database primary node unreachable: connection refused to db-primary-01:5432 |
| ERROR | recommendation | Failed to process recommendation request: invalid product ID from 203.0.113.50 |
| WARN | frontend-proxy | SSL certificate for api.example.com expires in 14 days |
| WARN | frontend-proxy | Rate limit threshold reached: 450/500 requests per minute for API key ending in ...abc789 |
| WARN | product-catalog | Slow query detected: SELECT \* FROM products WHERE category = 'electronics' took 3200ms |

<!-- vale on -->
  

## 範例 2：擷取指定數量的結果

下列查詢會傳回前 3 筆最嚴重的記錄檔項目，以便快速檢查嚴重性：
  
```sql
source=otellogs
| where severityText IN ('ERROR', 'WARN')
| sort - severityNumber, `resource.attributes.service.name`
| fields severityText, `resource.attributes.service.name`, body
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | resource.attributes.service.name | body |
| --- | --- | --- |
| ERROR | checkout | NullPointerException in CheckoutService.placeOrder at line 142 |
| ERROR | checkout | Kafka producer delivery failed: message too large for topic order-events (max 1048576 bytes) |
| ERROR | frontend-proxy | [2024-02-01T09:20:00.456Z] "POST /api/checkout HTTP/1.1" 503 - 0 30000 checkout-8d4f7b-mk2p9 |

<!-- vale on -->
  

## 範例 3：在位移 M 之後擷取前 N 筆結果

下列查詢會略過 2 筆最嚴重的項目，並傳回接下來的 3 筆，適合在檢閱最嚴重的問題後分頁瀏覽結果：
  
```sql
source=otellogs
| where severityText IN ('ERROR', 'WARN')
| sort - severityNumber, `resource.attributes.service.name`
| fields severityText, `resource.attributes.service.name`, body
| head 3 from 2
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | resource.attributes.service.name | body |
| --- | --- | --- |
| ERROR | frontend-proxy | [2024-02-01T09:20:00.456Z] "POST /api/checkout HTTP/1.1" 503 - 0 30000 checkout-8d4f7b-mk2p9 |
| ERROR | payment | Payment failed: connection timeout to payment gateway after 30000ms |
| ERROR | payment | Out of memory: Java heap space - shutting down pod payment-6f8d4b-ht7q3 |

<!-- vale on -->
  

