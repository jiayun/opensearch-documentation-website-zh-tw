---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: fields
parent: Commands
grand_parent: PPL
nav_order: 18
---

<!-- vale off -->

# fields 命令

<!-- vale on -->

`fields` 命令指定搜尋結果應包含或排除的欄位。

## 語法

`fields` 命令的語法如下：

```sql
fields [+|-] <field-list>
```

## 參數

`fields` 命令支援下列參數。

| 參數 | 必要／選用 | 說明 |
| --- | --- | --- |
| `<field-list>` | 必要 | 要保留或移除的欄位清單，以逗號或空格分隔。支援萬用字元模式。 |
| `[+|-]` | 選用 | 若使用加號（`+`），則僅包含 `field-list` 中指定的欄位。若使用減號（`-`），則排除 `field-list` 中指定的所有欄位。預設為 `+`。 |
  

## 範例 1：選取您進行問題分流所需的欄位

下列查詢會從搜尋結果中選取特定欄位：
  
```sql
source=otellogs
| where severityText IN ('ERROR', 'WARN')
| sort severityNumber, `resource.attributes.service.name`
| fields severityText, `resource.attributes.service.name`, body
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | resource.attributes.service.name | body |
| --- | --- | --- |
| WARN | frontend-proxy | SSL certificate for api.example.com expires in 14 days |
| WARN | frontend-proxy | Rate limit threshold reached: 450/500 requests per minute for API key ending in ...abc789 |
| WARN | product-catalog | Slow query detected: SELECT \* FROM products WHERE category = 'electronics' took 3200ms |

<!-- vale on -->
  

## 範例 2：從結果中移除雜訊欄位 

下列查詢會在擷取您所需的內容後，移除原始的 `body` 欄位，讓輸出保持簡潔：
  
```sql
source=otellogs
| where severityText IN ('ERROR', 'WARN')
| sort severityNumber, `resource.attributes.service.name`
| fields severityText, `resource.attributes.service.name`, severityNumber, body
| fields - body, severityNumber
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | resource.attributes.service.name |
| --- | --- |
| WARN | frontend-proxy |
| WARN | frontend-proxy |
| WARN | product-catalog |

<!-- vale on -->
  

## 範例 3：使用前綴萬用字元選取所有與嚴重程度相關的欄位

當您不確定確切的欄位名稱時，可使用萬用字元取得所有以共同前綴開頭的欄位。這會同時選取 `severityText` 和 `severityNumber`：
  
```sql
source=otellogs
| where severityText IN ('ERROR', 'WARN')
| sort severityNumber, `resource.attributes.service.name`
| fields severity*
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | severityNumber |
| --- | --- |
| WARN | 13 |
| WARN | 13 |
| WARN | 13 |

<!-- vale on -->
  

## 範例 4：使用後綴萬用字元選取追蹤關聯欄位

下列查詢會取得所有以 `Id` 結尾的欄位，適合在偵錯分散式請求時擷取追蹤關聯識別碼：
  
```sql
source=otellogs
| where LENGTH(traceId) > 0
| fields *Id
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| spanId | traceId |
| --- | --- |
| span0001 | abcd1234efgh5678 |
| span0002 | abcd1234efgh5678 |
| span0003 | abcd1234efgh5678 |

<!-- vale on -->
  

## 範例 5：結合明確指定的欄位與萬用字元

下列查詢會同時選取特定欄位與符合萬用字元的欄位。這會在一次查詢中取得嚴重程度文字及所有追蹤識別碼：
  
```sql
source=otellogs
| where LENGTH(traceId) > 0
| fields severityText, *Id
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | spanId | traceId |
| --- | --- | --- |
| INFO | span0001 | abcd1234efgh5678 |
| INFO | span0002 | abcd1234efgh5678 |
| WARN | span0003 | abcd1234efgh5678 |

<!-- vale on -->
  

## 範例 6：使用萬用字元排除方式移除追蹤欄位

下列查詢會從輸出中移除所有識別碼欄位，適合在您只想取得記錄檔內容而不需要追蹤中繼資料時使用：
  
```sql
source=otellogs
| where severityText = 'ERROR'
| sort `resource.attributes.service.name`
| fields - *Id
| head 1
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| @timestamp | instrumentationScope | severityText | resource | flags | attributes | droppedAttributesCount | severityNumber | time | body |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024-02-01 09:15:00 | {} | ERROR | {'attributes': {'service': {'name': 'checkout'}, 'host': {'name': 'checkout-8b4c2d-jp5r7'}}, 'droppedAttributesCount': 0} | 0 | {} | 0 | 17 | 2024-02-01 09:15:00 | NullPointerException in CheckoutService.placeOrder at line 142 |

<!-- vale on -->

## 範例 7：移除重複欄位

當萬用字元展開後包含已指定的欄位時，下列查詢會自動避免產生重複的資料欄：

```sql
source=otellogs
| fields severityText, severity*
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢會傳回下列結果。即使 `severityText` 已明確指定，而且也符合 `severity*`，由於會自動移除重複項目，因此只會出現一次：

<!-- vale off -->

| severityText | severityNumber |
| --- | --- |
| INFO | 9 |
| INFO | 9 |
| WARN | 13 |

<!-- vale on -->

## 範例 8：選取所有欄位  

下列查詢會使用 `` `*` `` 選取索引結構描述中定義的所有欄位。值為 null 的欄位也會包含在此查詢傳回的下列結果中：
  
```sql
source=otellogs
| where severityText = 'WARN'
| fields `*`
| head 1
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| spanId | traceId | @timestamp | instrumentationScope | severityText | resource | flags | attributes | droppedAttributesCount | severityNumber | time | body |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| span0003 | abcd1234efgh5678 | 2024-02-01 09:12:00 | {'name': 'go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc', 'droppedAttributesCount': 0, 'version': '0.49.0'} | WARN | {'attributes': {'service': {'name': 'product-catalog'}, 'host': {'name': 'productcatalog-7c9d-zn4p2'}}, 'droppedAttributesCount': 0} | 0 | {} | 0 | 13 | 2024-02-01 09:12:00 | Slow query detected: SELECT \* FROM products WHERE category = 'electronics' took 3200ms |

<!-- vale on -->
  

## 相關文件 

- [`table`]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/table/) -- 功能相同的別名命令  
