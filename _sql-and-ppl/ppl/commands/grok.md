---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: grok
parent: Commands
grand_parent: PPL
nav_order: 22
---

<!-- vale off -->

# grok 命令

<!-- vale on -->

`grok` 命令會使用 Grok 模式剖析文字欄位，並將擷取的結果附加到搜尋結果中。

## 語法

`grok` 命令的語法如下：

```sql
grok <field> <pattern>
```

## 參數

`grok` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<field>` | 必要 | 要剖析的文字欄位。 |
| `<pattern>` | 必要 | 用於從指定文字欄位擷取新欄位的 Grok 模式。如果新欄位名稱已存在，則會覆寫原始欄位。 |  
  

## 範例 1：剖析 Apache 存取記錄檔  

下列查詢使用內建的 `COMMONAPACHELOG` grok 模式剖析原始 Apache 存取記錄檔：
  
```sql
source=apache
| grok message '%{COMMONAPACHELOG}'
| fields COMMONAPACHELOG, timestamp, response, bytes
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| COMMONAPACHELOG | timestamp | response | bytes |
| --- | --- | --- | --- |
| 177.95.8.74 - upton5450 [28/Sep/2022:10:15:57 -0700] "HEAD /e-business/mindshare HTTP/1.0" 404 19927 | 28/Sep/2022:10:15:57 -0700 | 404 | 19927 |
| 127.45.152.6 - pouros8756 [28/Sep/2022:10:15:57 -0700] "GET /architectures/convergence/niches/mindshare HTTP/1.0" 100 28722 | 28/Sep/2022:10:15:57 -0700 | 100 | 28722 |
| 118.223.210.105 - - [28/Sep/2022:10:15:57 -0700] "PATCH /strategize/out-of-the-box HTTP/1.0" 401 27439 | 28/Sep/2022:10:15:57 -0700 | 401 | 27439 |
| 210.204.15.104 - - [28/Sep/2022:10:15:57 -0700] "POST /users HTTP/1.1" 301 9481 | 28/Sep/2022:10:15:57 -0700 | 301 | 9481 |

<!-- vale on -->

## 範例 2：從 Envoy 存取記錄檔擷取欄位

下列查詢剖析 Envoy 存取記錄項目，擷取 HTTP 方法、路徑與狀態碼：

```sql
source=otellogs
| where LIKE(body, '%HTTP/1.1%')
| grok body '\[%{DATA:ts}\] \"%{WORD:method} %{DATA:path} HTTP/%{DATA:ver}\" %{POSINT:status}'
| fields method, path, status
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| method | path | status |
| --- | --- | --- |
| GET | /api/products | 200 |
| POST | /api/checkout | 503 |

<!-- vale on -->

## 範例 3：從記錄訊息擷取持續時間

下列查詢使用 grok 從記錄訊息中擷取數值持續時間：

```sql
source=otellogs
| where LIKE(body, '%ms%')
| grok body '%{NUMBER:duration}ms'
| fields body, duration
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| body | duration |
| --- | --- |
| Slow query detected: SELECT \* FROM products WHERE category = 'electronics' took 3200ms | 3200 |
| Payment failed: connection timeout to payment gateway after 30000ms | 30000 |
| gRPC call /ProductCatalogService/GetProduct completed in 12ms | 12 |

<!-- vale on -->

## 限制

`grok` 命令有下列限制：

* `grok` 命令與 `parse` 命令具有相同的[限制]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/parse#limitations)。 