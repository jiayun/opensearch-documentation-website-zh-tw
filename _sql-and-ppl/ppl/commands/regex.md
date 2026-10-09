---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: regex
parent: Commands
grand_parent: PPL
nav_order: 36
---

<!-- vale off -->

# regex 命令

<!-- vale on -->

`regex` 命令透過將欄位值與正規表示式模式比對來篩選搜尋結果。只有指定欄位符合該模式的文件才會包含在結果中。

## 語法

`regex` 命令的語法如下：

```sql
regex <field> = <pattern>
regex <field> != <pattern>
```

支援下列運算子：

* `=` -- 正向比對（包含符合的結果）
* `!=` -- 反向比對（排除符合的結果）

`regex` 命令使用 Java 內建的正規表示式引擎，支援：

* **標準正規表示式功能**：字元類別、量詞、錨點。  
* **具名擷取群組**：`(?<name>pattern)` 語法。  
* **先行斷言／後顧斷言**：`(?=...)` 與 `(?<=...)` 斷言。  
* **行內旗標**：不分大小寫 `(?i)`、多行 `(?m)`、點號可比對換行字元的模式 `(?s)` 及其他模式。  

## 參數

`regex` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<field>` | 必要 |要比對的欄位名稱。 |
| `<pattern>` | 必要 |要比對的正規表示式模式。支援 [Java 正規表示式語法](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html)。 |

## 範例 1：尋找符合模式的記錄檔  

下列查詢會找出提及連線逾時的錯誤記錄檔：
  
```sql
source=otellogs
| where severityText = 'ERROR'
| regex body=".*timeout.*"
| fields severityText, `resource.attributes.service.name`, body
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | resource.attributes.service.name | body |
| --- | --- | --- |
| ERROR | payment | Payment failed: connection timeout to payment gateway after 30000ms |

<!-- vale on -->
  

## 範例 2：排除符合模式的記錄檔  

下列查詢會找出所有錯誤，但與逾時相關的錯誤除外：
  
```sql
source=otellogs
| where severityText = 'ERROR'
| regex body!=".*timeout.*"
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
| ERROR | payment | Out of memory: Java heap space - shutting down pod payment-6f8d4b-ht7q3 |
| ERROR | frontend-proxy | [2024-02-01T09:20:00.456Z] "POST /api/checkout HTTP/1.1" 503 - 0 30000 checkout-8d4f7b-mk2p9 |

<!-- vale on -->
  

## 範例 3：依服務名稱模式篩選  

下列查詢會找出名稱以 "catalog" 結尾之服務的警告記錄檔：
  
```sql
source=otellogs
| where severityText = 'WARN'
| regex `resource.attributes.service.name`=".*catalog$"
| fields severityText, `resource.attributes.service.name`, body
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | resource.attributes.service.name | body |
| --- | --- | --- |
| WARN | product-catalog | Slow query detected: SELECT \* FROM products WHERE category = 'electronics' took 3200ms |
| WARN | product-catalog | Connection pool 80% utilized on database replica db-replica-02 |

<!-- vale on -->
  

## 範例 4：使用字元類別的複雜模式

下列查詢使用包含字元類別與量詞的複雜正規表示式模式，比對包含服務方法呼叫的記錄訊息：

```sql
source=otellogs
| where severityText = 'ERROR'
| regex body="[A-Z][a-zA-Z]+\\.[a-zA-Z]+"
| fields severityText, body
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| severityText | body |
| --- | --- |
| ERROR | NullPointerException in CheckoutService.placeOrder at line 142 |

<!-- vale on -->

## 範例 5：區分大小寫的比對

預設情況下，regex 比對會區分大小寫。下列查詢會搜尋小寫的 `error`：

```sql
source=otellogs
| regex severityText="error"
| fields severityText
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢沒有傳回任何結果，因為正規表示式模式 `error`（小寫）不符合 `ERROR`（大寫）：

## 限制

`regex` 命令有下列限制：

* 必須在 `regex` 命令中指定欄位名稱。不支援僅使用模式的語法（例如 `regex "pattern"`）。
* `regex` 命令僅支援字串欄位。對數值或布林值欄位使用會導致錯誤。  
