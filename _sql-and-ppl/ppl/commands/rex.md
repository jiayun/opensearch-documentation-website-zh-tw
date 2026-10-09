---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: rex
parent: Commands
grand_parent: PPL
nav_order: 40
---

<!-- vale off -->

# rex 命令

<!-- vale on -->

`rex` 命令使用正規表示式的具名擷取群組，從原始文字欄位中擷取欄位。它使用 Java regex 模式。如需更多資訊，請參閱 [Java 正規表示式文件](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html)。

<!-- vale off -->

## rex 與 parse 命令的比較

<!-- vale on -->

`rex` 與 [`parse`]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/parse/) 命令都使用帶有具名擷取群組的 Java 正規表示式，從文字欄位中擷取資訊。下表比較了 `rex` 與 `parse` 命令的功能。

| 功能 | `rex` | `parse` |
| --- | --- | --- |
| 模式類型 | Java regex | Java regex |
| 需要具名群組 | 是 | 是 |
| 多個具名群組 | 是 | 否 |
| 多重比對 | 是 | 否 |
| 文字替換 | 是 | 否 |
| 偏移量追蹤 | 是 | 否 |
| 群組名稱中的特殊字元 | 否 | 否 |

## 語法

`rex` 命令的語法如下：

```sql
rex [mode=<mode>] field=<field> <pattern> [max_match=<int>] [offset_field=<string>]
```

## 參數

`rex` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `field` | 必要 | 要從中擷取資料的欄位。該欄位必須是字串。 |
| `<pattern>` | 必要 | 用來擷取新欄位、帶有具名擷取群組的正規表示式模式。模式必須至少包含一個使用 `(?<name>pattern)` 語法的具名擷取群組。群組名稱必須以字母開頭，且只能包含字母與數字。 |
| `mode` | 選用 | 比對模式。有效值為 `extract` 與 `sed`。`extract` 模式會從正規表示式的具名擷取群組建立新欄位。`sed` 模式會使用 sed 風格的模式執行文字替換（支援帶旗標的 `s/pattern/replacement/`、`y/from_chars/to_chars/` 字元轉換，以及回參照）。 |
| `max_match` | 選用 | 要擷取的最大比對次數。如果該值大於 `1`，擷取的欄位會以陣列形式回傳。值為 `0` 表示比對次數無上限；不過，實際比對次數會自動受設定的最大值限制。預設最大值為 `10`，可透過 `plugins.ppl.rex.max_match.limit` 進行設定（請參閱[注意]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/rex/#note)）。預設值為 `1`。 |
| `offset_field` | 選用 | 僅在 `extract` 模式下有效。用來儲存比對結果字元偏移位置的欄位名稱。 |

<p id="note"></p>

您可以在 `plugins.ppl.rex.max_match.limit` 叢集設定中設定 `max_match` 限制。如需更多資訊，請參閱 [SQL 設定]({{site.url}}{{site.baseurl}}/sql-and-ppl/settings/)。不建議將此限制設定為過大的值，因為這可能導致過度的記憶體消耗，尤其是當模式會比對空字串時（例如 `\d*` 或 `\w*`）。
{: .note}


## 範例 1：從記錄檔訊息中擷取服務名稱與錯誤類型  

下列查詢會從 Java 例外狀況記錄檔訊息中擷取錯誤類型。未比對到的資料列在擷取的欄位中會回傳 `null`：
  
```sql
source=otellogs
| where severityText = 'ERROR'
| rex field=body "(?<errtype>[A-Z][a-zA-Z]+Exception)"
| fields body, errtype
| head 3
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會回傳下列結果：
  
<!-- vale off -->

| body | errtype |
| --- | --- |
| Payment failed: connection timeout to payment gateway after 30000ms | null |
| NullPointerException in CheckoutService.placeOrder at line 142 | NullPointerException |
| Out of memory: Java heap space - shutting down pod payment-6f8d4b-ht7q3 | null |

<!-- vale on -->
  

## 範例 2：使用 max_match 擷取多個單字  

下列查詢使用 `rex` 命令搭配 `max_match` 參數，從 `body` 欄位中擷取多個單字。擷取的欄位會以字串陣列的形式回傳：
  
```sql
source=otellogs
| where severityText = 'WARN'
| rex field=body "(?<word>[A-Za-z]+)" max_match=3
| fields body, word
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會回傳下列結果：
  
<!-- vale off -->

| body | word |
| --- | --- |
| Slow query detected: SELECT \* FROM products WHERE category = 'electronics' took 3200ms | [Slow,query,detected] |
| Connection pool 80% utilized on database replica db-replica-02 | [Connection,pool,utilized] |
| SSL certificate for api.example.com expires in 14 days | [SSL,certificate,for] |
| Rate limit threshold reached: 450/500 requests per minute for API key ending in ...abc789 | [Rate,limit,threshold] |

<!-- vale on -->
  

<!-- vale off -->

## 範例 3：使用 sed 模式替換文字  

<!-- vale on -->

下列查詢使用 `sed` 模式來遮罩記錄檔訊息中的 IP 位址，以符合隱私合規要求：

```sql
source=otellogs
| where LIKE(body, '%authenticated%') OR LIKE(body, '%credentials%')
| rex field=body mode=sed "s/[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+/xxx.xxx.xxx.xxx/"
| fields body
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會回傳下列結果：

<!-- vale off -->

| body |
| --- |
| User U300 authenticated via OAuth2 from xxx.xxx.xxx.xxx |

<!-- vale on -->

## 範例 4：使用 offset_field 追蹤比對位置  

下列查詢會追蹤比對發生的字元位置，適合用於在使用者介面中突顯比對結果：
  
```sql
source=otellogs
| where severityText = 'ERROR'
| rex field=body "(?<errtype>[A-Z][a-zA-Z]+Exception)" offset_field=pos
| where NOT ISNULL(errtype)
| fields body, errtype, pos
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會回傳下列結果：
  
<!-- vale off -->

| body | errtype | pos |
| --- | --- | --- |
| NullPointerException in CheckoutService.placeOrder at line 142 | NullPointerException | errtype=0-19 |

<!-- vale on -->
  

由於 [Java regex](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html) 的限制，擷取群組名稱不能包含底線。例如，`(?<error_type>\w+)` 是無效的；請改用 `(?<errortype>\w+)`。
{: .note}

如需詳細的 Java regex 模式語法與用法，請參閱官方 [Java Pattern 文件](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html)。
