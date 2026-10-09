---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: parse
parent: Commands
grand_parent: PPL
nav_order: 33
---

<!-- vale off -->

# parse 命令

<!-- vale on -->

`parse` 命令會使用規則表達式從文字欄位擷取資訊，並將擷取到的資訊加入搜尋結果。此命令使用 Java 規則表達式模式。如需詳細資訊，請參閱 [Java 規則表達式文件](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html)。

<!-- vale off -->

## rex 與 parse 命令的比較

<!-- vale on -->

`rex` 與 `parse` 命令都會使用帶有具名擷取群組的 Java 規則表達式，從文字欄位擷取資訊。若要比較 `rex` 與 `parse` 命令的功能，請參閱 [`rex` 命令文件]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/rex/)。

## 語法

`parse` 命令的語法如下：

```sql
parse <field> <pattern>
```

## 參數

`parse` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<field>` | 必要 | 要剖析的文字欄位。 |
| `<pattern>` | 必要 | 用來從指定文字欄位擷取新欄位的規則表達式模式。若已存在同名欄位，其值會被取代。 |

## 規則表達式

規則表達式模式會根據 [Java 規則表達式語法](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html)，用來比對每份文件的整個文字欄位。運算式中的每個具名擷取群組都會成為新的 `STRING` 欄位。  

## 範例 1：從記錄訊息擷取錯誤詳細資料  

下列查詢會從錯誤記錄訊息擷取錯誤摘要與詳細資料。這在事件分級期間分類錯誤時很有用：
  
```sql
source=otellogs
| where severityText = 'ERROR'
| parse body '(?<errmsg>[^:]+): (?<detail>.+)'
| fields errmsg, detail
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| errmsg | detail |
| --- | --- |
| Payment failed | connection timeout to payment gateway after 30000ms |
|  |  |
| Out of memory | Java heap space - shutting down pod payment-6f8d4b-ht7q3 |

<!-- vale on -->
  

## 範例 2：從記錄訊息擷取 IP 位址  

下列查詢會從特定服務的記錄訊息擷取 IP 位址：
  
```sql
source=otellogs
| where `resource.attributes.service.name` = 'frontend'
| parse body '.+from (?<sourceip>[0-9.]+)'
| fields body, sourceip
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| body | sourceip |
| --- | --- |
| [2024-02-01T09:10:00.123Z] "GET /api/products HTTP/1.1" 200 - 1024 45 frontend-6b7b4c9f-x2kl9 |  |
| User U300 authenticated via OAuth2 from 10.0.0.5 | 10.0.0.5 |
| Deployment frontend-v2.2.0 rolled out successfully to 3/3 replicas |  |

<!-- vale on -->
  

## 限制

`parse` 命令有下列限制：

- 由 `parse` 命令建立的欄位無法再次剖析。例如，下列命令無法如預期運作：

    ```sql
    source=otellogs | parse body '(?<errmsg>[^:]+): (?<detail>.+)' | parse detail '\\w+ (?<word>\\w+)'
    ```

- 由 `parse` 命令建立的欄位無法被其他命令覆寫。例如，在下列查詢中，`where` 子句不會比對到任何文件，因為 `errmsg` 無法被覆寫：

    ```sql
    source=otellogs | parse body '(?<errmsg>[^:]+): (?<detail>.+)' | eval errmsg='1' | where errmsg='1'
    ```

- `parse` 命令所使用的來源文字欄位無法被覆寫。例如，在下列查詢中，`errmsg` 欄位無法正確剖析，因為 `body` 被覆寫：

    ```sql
    source=otellogs | parse body '(?<errmsg>[^:]+): (?<detail>.+)' | eval body='1'
    ```

- 由 `parse` 命令建立的欄位在 `stats` 命令中使用後，就無法加以篩選或排序。例如，在下列查詢中，`where` 子句無法如預期運作：

    ```sql
    source=otellogs | parse body '(?<errmsg>[^:]+): (?<detail>.+)' | stats count() by errmsg | where errmsg='Payment failed'
    ```
