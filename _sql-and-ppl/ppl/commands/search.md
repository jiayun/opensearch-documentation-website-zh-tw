---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: search
parent: Commands
grand_parent: PPL
nav_order: 41
---

<!-- vale off -->

# search 命令

<!-- vale on -->

`search` 命令會從索引擷取文件。`search` 命令只能作為 PPL 查詢中的第一個命令使用。

## 語法

`search` 命令具有下列語法：

```sql
search source=[<remote-cluster>:]<index> [<search-expression>]
```

## 參數

`search` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<index>` | 必要 | 要查詢的索引。索引名稱可加上 `<remote-cluster>:` (遠端叢集名稱) 前置詞，以進行跨叢集搜尋。 |
| `<search-expression>` | 選用 | 會轉換為 OpenSearch [查詢字串]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/)查詢的搜尋運算式。 |
  

## 搜尋運算式  

搜尋運算式語法支援：
* **全文搜尋**：`error` 或 `"error message"` -- 搜尋 `index.query.default_field` 設定中所設定的預設欄位 (預設為 `*`，其指定所有欄位)。如需詳細資訊，請參閱[預設欄位組態](#default-field-configuration)。 
* **欄位值比較**：`field=value`、`field!=value`、`field>value`、`field>=value`、`field<value` 或 `field<=value`。  
* **時間修飾詞**：`earliest=timeModifier`、`latest=timeModifier` -- 使用隱含的 `@timestamp` 欄位依時間範圍篩選結果。如需詳細資訊，請參閱[時間修飾詞](#time-modifiers)。 
* **布林運算子**：`AND`、`OR` 或 `NOT`。預設為 `AND`。  
* **使用括號分組**：`(expression)`。  
* **用於多個值的 `IN` 運算子**：`field IN (value1, value2, value3)`。  
* **萬用字元**：`*` (零個或多個字元)、`?` (恰好一個字元)。  
  
### 全文搜尋

與其他 PPL 命令不同，`search` 命令同時支援加上引號與未加引號的字串。未加引號的詞彙僅限於英數字元、連字號、底線與萬用字元。任何其他字元都需要加上雙引號。

下列查詢顯示這兩種語法類型：

* **未加引號**：`search error`、`search user-123`、`search log_*`
* **加上引號**：`search "error message"`、`search "user@example.com"`
  
### 欄位值

欄位值遵循與搜尋文字相同的引號規則。

欄位值語法的範例：

* **未加引號**：`status=active`、`code=ERR-401`
* **加上引號**：`email="user@example.com"`、`message="server error"`  
  
### 時間修飾詞

時間修飾詞會使用隱含的 `@timestamp` 欄位，依時間範圍篩選搜尋結果。時間修飾詞支援下列格式。

| 格式 | 語法 | 說明 | 範例 |
| --- | --- | --- | --- |
| 目前時間 | `now` 或 `now()` | 目前時間 | `earliest=now` |
| 絕對時間 | `MM/dd/yyyy:HH:mm:ss` 或 `yyyy-MM-dd HH:mm:ss` | 特定日期與時間 | `latest='2024-12-31 23:59:59'` |
| Unix 時間戳記 | 數值 | 自 epoch 起算的秒數 | `latest=1754020060.123` |
| 相對時間 | `[(+/-)<time_integer><time_unit>][@<round_to_unit>]` | 相對於目前時間的時間位移。請參閱[相對時間元件](#relative-time-components)。 | `earliest=-7d`、`latest='+1d@d'` |

#### 相對時間元件

相對時間修飾詞使用多個可合併的元件。下表說明每個元件。

| 元件 | 語法 | 說明 | 範例 |
| --- | --- | --- | --- |
| 時間位移 | `+` 或 `-` | 方向：`+` (未來) 或 `-` (過去) | `+7d`、`-1h` |
| 時間量 | `<time_integer><time_unit>` | 數值 + 時間單位 | `7d`、`1h`、`30m` |
| 捨入至單位 | `@<round_to_unit>` | 捨入至最接近的單位 | `@d` (日)、`@h` (小時)、`@m` (分鐘) | 
  
下列是常見時間修飾詞模式的範例：

* `earliest=now` -- 從目前時間開始。
* `latest='2024-12-31 23:59:59'` -- 結束於特定日期與時間。
* `earliest=-7d` -- 從 7 天前開始。
* `latest='+1d@d'` -- 結束於明天的開始時間。
* `earliest='-1month@month'` -- 從上個月的開始時間開始。
* `latest=1754020061` -- 結束於 Unix 時間戳記 `1754020061` (2025 年 8 月 1 日 03:47:41 UTC)。

在 `search` 命令中使用時間修飾詞時，適用下列考量事項：

* **欄位名稱衝突**：如果您的資料包含名為 `earliest` 或 `latest` 的欄位，請使用反引號將它們作為一般欄位存取 (例如 `` `earliest`="value"``)，以避免與時間修飾詞語法衝突。  
* **時間捨入語法**：具有連鎖時間位移的時間修飾詞必須以引號括住 (例如 `latest='+1d@month-10h'`)，才能正確剖析查詢。  

## 預設欄位組態  

在未指定欄位的情況下執行搜尋時，會使用 `index.query.default_field` 索引設定所設定的預設欄位。根據預設，此設定為 `*`，其會搜尋所有欄位。

若要擷取預設欄位設定，請使用下列請求：

```json
GET /accounts/_settings/index.query.default_field
```
{% include copy-curl.html %}

若要修改預設欄位設定，請使用下列請求：

```json
PUT /accounts/_settings
{
  "index.query.default_field": "firstname,lastname,email"
}
```
{% include copy-curl.html %}

## 依欄位類型區分的搜尋行為

不同的欄位類型具有特定的搜尋功能與限制。下表摘要說明搜尋運算式如何與各欄位類型搭配運作。

| 欄位類型 | 支援的操作 | 範例 | 限制 |
| --- | --- | --- | --- |
| 文字 | 全文搜尋、片語搜尋 | `search message="error occurred" source=logs` | 萬用字元套用於分析後的詞元，而非整個欄位值 |
| 關鍵字 | 完全相符、萬用字元模式 | `search status="ACTIVE" source=logs` | 無文字分析；比對區分大小寫 |
| 數值 | 範圍查詢、完全相符、`IN` 運算子 | `search age>=18 AND balance<50000 source=accounts` | 不支援萬用字元或文字搜尋 |
| 日期 | 範圍查詢、完全相符、`IN` 運算子 | `search timestamp>="2024-01-01" source=logs` | 必須遵循索引對應的日期格式；不支援萬用字元 |
| 布林值 | 完全相符、`true` 與 `false` 值、`IN` 運算子 | `search active=true source=users` | 不支援萬用字元或範圍查詢 |
| IP | 完全相符、CIDR 標記法 | `search client_ip="192.168.1.0/24" source=logs` | 不支援部分 IP 萬用字元比對。如需萬用字元搜尋，請使用 keyword 的多欄位：`search ip_address.keyword='1*' source=logs` 或 WHERE 子句：`source=logs | where cast(ip_address as string) like '1%'` |

處理不同欄位類型時，請考量下列效能最佳化：

* 每個欄位類型都有特定的搜尋功能與限制。在匯入期間選擇不適當的欄位類型，可能會對效能與查詢準確度造成負面影響。
* 若要在非 keyword 欄位上進行萬用字元搜尋，請建立 `keyword` 子欄位以改善效能。例如，若要在類型為 `text` 的 `message` 欄位上進行萬用字元搜尋，請新增 `message.keyword` 欄位。

<!-- temporarily commented out because the admin section is not ported
## Cross-cluster search  

Cross-cluster search lets any node in a cluster execute search requests against other clusters. Refer to [Cross-cluster search]({{site.url}}{{site.baseurl}}/search-plugins/cross-cluster-search/) for configuration.
-->

## 範例 1：擷取所有資料

從索引擷取所有文件：

```sql
source=otellogs
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| spanId | traceId | @timestamp | instrumentationScope | severityText | resource | flags | attributes | droppedAttributesCount | severityNumber | time | body |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| span0001 | abcd1234efgh5678 | 2024-02-01 09:10:00 | {'name': '@opentelemetry/instrumentation-http', 'droppedAttributesCount': 0, 'version': '0.57.0'} | INFO | {'attributes': {'service': {'name': 'frontend'}, 'host': {'name': 'frontend-6b7b4c9f-x2kl9'}}, 'droppedAttributesCount': 0} | 0 | {} | 0 | 9 | 2024-02-01 09:10:00 | [2024-02-01T09:10:00.123Z] "GET /api/products HTTP/1.1" 200 - 1024 45 frontend-6b7b4c9f-x2kl9 |
| span0002 | abcd1234efgh5678 | 2024-02-01 09:11:00 | {'name': 'Microsoft.Extensions.Hosting', 'droppedAttributesCount': 0, 'version': '9.0.0'} | INFO | {'attributes': {'service': {'name': 'cart'}, 'host': {'name': 'cart-5d8f7b-mk29s'}}, 'droppedAttributesCount': 0} | 0 | {} | 0 | 9 | 2024-02-01 09:11:00 | Order #1234 placed successfully by user U100 |
| span0003 | abcd1234efgh5678 | 2024-02-01 09:12:00 | {'name': 'go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc', 'droppedAttributesCount': 0, 'version': '0.49.0'} | WARN | {'attributes': {'service': {'name': 'product-catalog'}, 'host': {'name': 'productcatalog-7c9d-zn4p2'}}, 'droppedAttributesCount': 0} | 0 | {} | 0 | 13 | 2024-02-01 09:12:00 | Slow query detected: SELECT \* FROM products WHERE category = 'electronics' took 3200ms |

<!-- vale on -->


## 範例 2：搜尋文字

若要進行基本文字搜尋，請使用不加引號的單一詞彙：
  
```sql
search ERROR source=otellogs
| sort `resource.attributes.service.name`
| fields severityText, body
| head 1
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | body |
| --- | --- |
| ERROR | NullPointerException in CheckoutService.placeOrder at line 142 |

<!-- vale on -->
  
片語搜尋需要使用引號，才能對多個單字進行精確比對：
  
```sql
search "Payment failed" source=otellogs
| sort `resource.attributes.service.name` | fields body | head 1
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| body |
| --- |
| Payment failed: connection timeout to payment gateway after 30000ms |

<!-- vale on -->

多個搜尋詞彙（不加引號的字串字面值）會自動使用 `AND` 運算子合併：
  
```sql
search connection timeout source=otellogs
| fields body
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| body |
| --- |
| Payment failed: connection timeout to payment gateway after 30000ms |

<!-- vale on -->
  
`search connection timeout` 等同於 `search connection AND timeout`。
{: .note}

### 結合片語與布林搜尋

將加引號的片語與布林運算子結合，可進行更精確的搜尋：

```sql
search "connection timeout" OR "heap space" source=otellogs
| sort `resource.attributes.service.name`
| fields body
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| body |
| --- |
| Payment failed: connection timeout to payment gateway after 30000ms |
| Out of memory: Java heap space - shutting down pod payment-6f8d4b-ht7q3 |

<!-- vale on -->
  

## 範例 3：布林邏輯與運算子優先順序  

下列查詢示範布林運算子及其優先順序。

### 布林運算子

使用 `OR` 比對包含任一指定條件的文件：

```sql
search severityText="ERROR" OR severityText="WARN" source=otellogs
| sort severityNumber, `resource.attributes.service.name`
| fields severityText, `resource.attributes.service.name`
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | resource.attributes.service.name |
| --- | --- |
| WARN | frontend-proxy |
| WARN | frontend-proxy |
| WARN | product-catalog |
| WARN | product-catalog |
| ERROR | checkout |
| ERROR | checkout |
| ERROR | frontend-proxy |
| ERROR | payment |
| ERROR | payment |
| ERROR | product-catalog |
| ERROR | recommendation |

<!-- vale on -->

使用 `AND` 結合條件，要求所有條件都必須符合：

```sql
search severityText="INFO" AND `resource.attributes.service.name`="cart-service" source=otellogs
| fields body
| head 1
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| body |
| --- |
| Order #1234 placed successfully by user U100 |

<!-- vale on -->
  
### 運算子優先順序

運算子會依照下列優先順序求值：

```
Parentheses > NOT > OR > AND
```

下列查詢示範運算子優先順序：

```sql
search severityText="ERROR" OR severityText="WARN" AND severityNumber>15 source=otellogs
| sort @timestamp
| fields severityText, severityNumber
| head 2
```
{% include copy.html %}

前述運算式會被求值為 `(severityText="ERROR" OR severityText="WARN") AND severityNumber>15`。查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | severityNumber |
| --- | --- |
| ERROR | 17 |
| ERROR | 17 |

<!-- vale on -->

## 範例 4：比較 NOT 與 != 的語意

`!=` 與 `NOT` 運算子都能找出欄位值不等於指定值的文件。不過，`!=` 運算子會排除包含 null 或缺少欄位的文件，而 `NOT` 運算子則會包含這些文件。下列查詢使用 `instrumentationScope.name`（在大多數記錄中為 null）來說明這項差異。

**!= 運算子**

排除 null 值---只傳回欄位存在且不等於指定值的資料列：

```sql
search instrumentationScope.name!="@opentelemetry/instrumentation-http" source=otellogs
| fields instrumentationScope.name
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| instrumentationScope.name |
| --- |
| Microsoft.Extensions.Hosting |

<!-- vale on -->

**`NOT` 運算子**

包含 null 值---傳回欄位為 null 或不等於指定值的資料列：

```sql
search NOT instrumentationScope.name="@opentelemetry/instrumentation-http" source=otellogs
| fields instrumentationScope.name
| head 5
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| instrumentationScope.name |
| --- |
| Microsoft.Extensions.Hosting |
| null |
| null |
| null |
| null |

<!-- vale on -->

## 範例 5：查詢範圍

使用比較運算子（`>,` `<,` `>=` 與 `<=`）篩選特定範圍內的數值與日期欄位。範圍查詢特別適合用來依年齡、價格、時間戳記或任何數值指標進行篩選：

```sql
search severityNumber>13 AND severityNumber<=21 source=otellogs
| sort severityNumber, `resource.attributes.service.name`
| fields severityNumber
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| severityNumber |
| --- |
| 17 |
| 17 |
| 17 |

<!-- vale on -->



## 範例 6：使用萬用字元

以下查詢示範萬用字元模式比對。在萬用字元模式中，`*` 比對零個或多個字元，而 `?` 則比對恰好一個字元。

使用 `*` 比對詞彙結尾的任意數量字元：

```sql
search severityText=ERR* source=otellogs
| sort severityNumber, `resource.attributes.service.name`
| fields severityText
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| severityText |
| --- |
| ERROR |
| ERROR |
| ERROR |

<!-- vale on -->

萬用字元搜尋也可用於文字欄位內，以尋找部分相符的內容：

```sql
search body=connection* source=otellogs
| sort `resource.attributes.service.name`
| fields body
| head 2
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| body |
| --- |
| Payment failed: connection timeout to payment gateway after 30000ms |
| Connection pool 80% utilized on database replica db-replica-02 |

<!-- vale on -->

使用 `?` 比對特定位置的恰好一個字元：

```sql
search severityText="ERR?R" source=otellogs
| fields severityText, `resource.attributes.service.name`
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| severityText | resource.attributes.service.name |
| --- | --- |
| ERROR | payment |
| ERROR | checkout |
| ERROR | payment |

<!-- vale on -->


## 範例 7：服務名稱搜尋中的萬用字元模式

在 text 或 keyword 欄位中搜尋時，萬用字元可啟用部分相符，當您只知道服務名稱的一部分時相當實用。萬用字元在 keyword 欄位上效果最佳，因為它們會使用模式比對確切值。在 text 欄位上使用萬用字元可能會產生非預期的結果，因為它們會套用至分析後的個別詞元，而非整個欄位值。除非在編製索引時進行正規化，否則 keyword 欄位中的萬用字元會區分大小寫。

前置萬用字元（例如 `*-service`）相較於尾端萬用字元，可能會降低查詢速度。
{: .note}

當您只知道服務名稱的開頭時，尋找服務的記錄檔：

```sql
search `resource.attributes.service.name`=payment* source=otellogs
| fields severityText, `resource.attributes.service.name`, body
| head 2
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| severityText | resource.attributes.service.name | body |
| --- | --- | --- |
| ERROR | payment | Payment failed: connection timeout to payment gateway after 30000ms |
| ERROR | payment | Out of memory: Java heap space - shutting down pod payment-6f8d4b-ht7q3 |

<!-- vale on -->

將萬用字元模式與其他條件結合，以進行更精確的篩選：

```sql
search firstname=A* AND age>30 source=accounts
| fields firstname, age, city
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| firstname | age | city |
| --- | --- | --- |
| Amber | 32 | Brogan |

<!-- vale on -->

## 範例 8：欄位值比對  

`IN` 運算子可有效率地檢查欄位是否符合清單中的任何值，提供比在同一欄位上串接多個 `OR` 條件更簡潔且效能更好的替代方案。

檢查欄位是否符合預先定義清單中的任何值：

```sql
search severityText IN ("ERROR", "WARN") source=otellogs
| fields severityText, `resource.attributes.service.name`
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | resource.attributes.service.name |
| --- | --- |
| WARN | product-catalog |
| WARN | product-catalog |
| WARN | frontend-proxy |
| WARN | frontend-proxy |
| ERROR | payment |
| ERROR | checkout |
| ERROR | payment |
| ERROR | frontend-proxy |
| ERROR | recommendation |
| ERROR | product-catalog |
| ERROR | checkout |

<!-- vale on -->


依 `severityNumber` 篩選記錄檔，以尋找具有特定數值嚴重性層級的錯誤：

```sql
search severityNumber=17 source=otellogs
| fields body, `resource.attributes.service.name`
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| body | resource.attributes.service.name |
| --- | --- |
| Payment failed: connection timeout to payment gateway after 30000ms | payment |
| NullPointerException in CheckoutService.placeOrder at line 142 | checkout |
| Out of memory: Java heap space - shutting down pod payment-6f8d4b-ht7q3 | payment |
| [2024-02-01T09:20:00.456Z] "POST /api/checkout HTTP/1.1" 503 - 0 30000 checkout-8d4f7b-mk2p9 | frontend-proxy |
| Failed to process recommendation request: invalid product ID from 203.0.113.50 | recommendation |
| Database primary node unreachable: connection refused to db-primary-01:5432 | product-catalog |
| Kafka producer delivery failed: message too large for topic order-events (max 1048576 bytes) | checkout |

<!-- vale on -->

## 範例 9：使用複雜運算式  

若要建立精密的搜尋查詢，請使用布林運算子和括號結合多個條件：
  
```sql
search (severityText="ERROR" OR severityText="WARN") AND severityNumber>13 source=otellogs
| sort severityNumber, `resource.attributes.service.name`
| fields severityText
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| severityText |
| --- |
| ERROR |
| ERROR |
| ERROR |

<!-- vale on -->

## 範例 10：使用時間修飾詞  

時間修飾詞會使用隱含的 `@timestamp` 欄位，依時間範圍篩選搜尋結果。它們支援各種時間格式，以進行精確的時間篩選。

### 絕對時間篩選

使用絕對時間戳記，篩選特定時間範圍內的記錄檔：

```sql
search earliest='2024-02-01 09:13:00' latest='2024-02-01 09:16:00' source=otellogs
| sort severityNumber
| fields `@timestamp`, severityText
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| @timestamp | severityText |
| --- | --- |
| 2024-02-01 09:14:00 | DEBUG |
| 2024-02-01 09:16:00 | INFO |
| 2024-02-01 09:13:00 | ERROR |
| 2024-02-01 09:15:00 | ERROR |

<!-- vale on -->
  
### 相對時間篩選

使用相對時間運算式篩選記錄檔，例如 30 秒前之前發生的記錄檔：

```sql
search latest=-30s source=otellogs
| sort severityNumber
| fields `@timestamp`, severityText
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| @timestamp | severityText |
| --- | --- |
| 2024-02-01 09:14:00 | DEBUG |
| 2024-02-01 09:21:00 | DEBUG |
| 2024-02-01 09:28:00 | DEBUG |

<!-- vale on -->
  
### 時間捨入

使用時間捨入運算式，依時間邊界篩選事件，例如目前分鐘開始之前的事件：

```sql
search latest='@m' source=otellogs
| sort severityNumber
| fields `@timestamp`, severityText
| head 2
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| @timestamp | severityText |
| --- | --- |
| 2024-02-01 09:14:00 | DEBUG |
| 2024-02-01 09:21:00 | DEBUG |

<!-- vale on -->
  
### Unix 時間戳記篩選

使用 Unix 紀元時間戳記篩選記錄檔，以指定精確的時間範圍：

```sql
search earliest=1706778600 latest=1706778960 source=otellogs
| sort severityNumber
| fields `@timestamp`, severityText
```
{% include copy.html %}
{% include try-in-playground.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| @timestamp | severityText |
| --- | --- |
| 2024-02-01 09:14:00 | DEBUG |
| 2024-02-01 09:10:00 | INFO |
| 2024-02-01 09:11:00 | INFO |
| 2024-02-01 09:16:00 | INFO |
| 2024-02-01 09:12:00 | WARN |
| 2024-02-01 09:13:00 | ERROR |
| 2024-02-01 09:15:00 | ERROR |

<!-- vale on -->
  

## 特殊字元的跳脫處理

特殊字元分為兩類，取決於它們是否必須一律跳脫，或僅在您想搜尋其字面值時才需要跳脫：

- 下列字元必須一律跳脫，才能按字面值解讀：
    * **反斜線（`\`）**：跳脫為 `\\`。
    * **引號（`"`）**：在以引號括住的字串內使用時，跳脫為 `\"`。

- 這些字元預設作為萬用字元，只有在您想比對其字面值時才應跳脫：
    * **星號（`*`）**：使用 `*` 進行萬用字元比對；若要比對星號的字面值，則跳脫為 `\\*`。
    * **問號（`?`）**：使用 `?` 進行萬用字元比對；若要比對問號的字面值，則跳脫為 `\\?`。

下表比較萬用字元比對與字元字面值比對。

| 目的 | PPL 語法 | 結果 |
| ---| --- | --- |
| 萬用字元搜尋 | `field=user*` | 比對 `user`、`user123`、`userABC` |
| 字面值 `user*` | `field="user\\*"` | 僅比對 `user*` |
| 萬用字元搜尋 | `field=log?` | 比對 `log1`、`logA`、`logs` |
| 字面值 `log?` | `field="log\\?"`  | 僅比對 `log?`|