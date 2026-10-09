---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "字串函式"
parent: Functions
grand_parent: PPL
nav_order: 13
---

# 字串函式

PPL 支援下列字串函式。

## CONCAT

**用法**：`CONCAT(str1, str2, ...., str_9)`

將最多 9 個字串串接起來。

**參數**：

- `str1, str2, ..., str_9` (必要)：最多 9 個要串接的字串。

**傳回類型**：`STRING`

### 範例
  
```sql
source=people
| eval `CONCAT('hello', 'world')` = CONCAT('hello', 'world'), `CONCAT('hello ', 'whole ', 'world', '!')` = CONCAT('hello ', 'whole ', 'world', '!')
| fields `CONCAT('hello', 'world')`, `CONCAT('hello ', 'whole ', 'world', '!')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| CONCAT('hello', 'world') | CONCAT('hello ', 'whole ', 'world', '!') |
| --- | --- |
| helloworld | hello whole world! |

<!-- vale on -->
  
## CONCAT_WS

**用法**：`CONCAT_WS(sep, str1, str2)`

傳回以 `sep` 作為分隔符號串接的 `str1` 與 `str2`。

**參數**：

- `sep` (必要)：要放在串接字串之間的分隔字串。
- `str1` (必要)：要串接的第一個字串。
- `str2` (必要)：要串接的第二個字串。

**傳回類型**：`STRING`

### 範例
  
```sql
source=people
| eval `CONCAT_WS(',', 'hello', 'world')` = CONCAT_WS(',', 'hello', 'world')
| fields `CONCAT_WS(',', 'hello', 'world')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| CONCAT_WS(',', 'hello', 'world') |
| --- |
| hello,world |

<!-- vale on -->
  
## LENGTH

**用法**：`length(str)`

傳回以位元組為單位測量的字串長度。

**參數**：

- `str` (必要)：要計算長度的字串。

**傳回類型**：`INTEGER`

### 範例
  
```sql
source=people
| eval `LENGTH('helloworld')` = LENGTH('helloworld')
| fields `LENGTH('helloworld')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| LENGTH('helloworld') |
| --- |
| 10 |

<!-- vale on -->
  
## LIKE

**用法**：`like(string, PATTERN[, case_sensitive])`

若字串符合模式則傳回 `TRUE`，否則傳回 `FALSE`。

**參數**：

- `string` (必要)：要與模式比對的字串。
- `PATTERN` (必要)：要比對的模式，支援萬用字元。
- `case_sensitive` (選用)：模式比對是否區分大小寫。預設值由 `plugins.ppl.syntax.legacy.preferred` 決定。

**萬用字元**：
- `%` - 代表零個、一個或多個字元。
- `_` - 代表單一字元。

**組態**：
- 當 `plugins.ppl.syntax.legacy.preferred=true` 時，`case_sensitive` 預設為 `false`。
- 當 `plugins.ppl.syntax.legacy.preferred=false` 時，`case_sensitive` 預設為 `true`。

**傳回類型**：`BOOLEAN`

### 範例
  
```sql
source=people
| eval `LIKE('hello world', '_ello%')` = LIKE('hello world', '_ello%'), `LIKE('hello world', '_ELLo%', true)` = LIKE('hello world', '_ELLo%', true), `LIKE('hello world', '_ELLo%', false)` = LIKE('hello world', '_ELLo%', false)
| fields `LIKE('hello world', '_ello%')`, `LIKE('hello world', '_ELLo%', true)`, `LIKE('hello world', '_ELLo%', false)`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| LIKE('hello world', '_ello%') | LIKE('hello world', '_ELLo%', true) | LIKE('hello world', '_ELLo%', false) |
| --- | --- | --- |
| True | False | True |

<!-- vale on -->
  
限制：將 `LIKE` 函式下推至 DSL wildcard 查詢僅支援 keyword 欄位。

## ILIKE

**用法**：`ilike(string, PATTERN)`

若字串符合模式（不區分大小寫）則傳回 `TRUE`，否則傳回 `FALSE`。

**參數**：

- `string` (必要)：要與模式比對的字串。
- `PATTERN` (必要)：要不區分大小寫比對的模式，支援萬用字元。

**萬用字元**：
- `%` - 代表零個、一個或多個字元。
- `_` - 代表單一字元。

**傳回類型**：`BOOLEAN`

### 範例
  
```sql
source=people
| eval `ILIKE('hello world', '_ELLo%')` = ILIKE('hello world', '_ELLo%')
| fields `ILIKE('hello world', '_ELLo%')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| ILIKE('hello world', '_ELLo%') |
| --- |
| True |

<!-- vale on -->
  
限制：將 `ILIKE` 函式下推至 DSL wildcard 查詢僅支援 keyword 欄位。

## LOCATE

**用法**：`locate(substr, str[, start])`

傳回 `substr` 在 `str` 中第一次出現的位置，從位置 `start` 開始。若未指定 `start`，搜尋會從位置 1 開始。若找不到 `substr` 則傳回 0。若任何引數為 `NULL`，函式會傳回 `NULL`。

**參數**：

- `substr` (必要)：要搜尋的子字串。
- `str` (必要)：要在其中搜尋的字串。
- `start` (選用)：開始搜尋的位置。預設為 1。

**傳回類型**：`INTEGER`

### 範例
  
```sql
source=people
| eval `LOCATE('world', 'helloworld')` = LOCATE('world', 'helloworld'), `LOCATE('invalid', 'helloworld')` = LOCATE('invalid', 'helloworld'), `LOCATE('world', 'helloworld', 6)` = LOCATE('world', 'helloworld', 6)
| fields `LOCATE('world', 'helloworld')`, `LOCATE('invalid', 'helloworld')`, `LOCATE('world', 'helloworld', 6)`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| LOCATE('world', 'helloworld') | LOCATE('invalid', 'helloworld') | LOCATE('world', 'helloworld', 6) |
| --- | --- | --- |
| 6 | 0 | 6 |

<!-- vale on -->
  
## LOWER

**用法**：`lower(string)`

將字串轉換為小寫。

**參數**：

- `string` (必要)：要轉換為小寫的字串。

**傳回類型**：`STRING`

### 範例
  
```sql
source=people
| eval `LOWER('helloworld')` = LOWER('helloworld'), `LOWER('HELLOWORLD')` = LOWER('HELLOWORLD')
| fields `LOWER('helloworld')`, `LOWER('HELLOWORLD')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| LOWER('helloworld') | LOWER('HELLOWORLD') |
| --- | --- |
| helloworld | helloworld |

<!-- vale on -->
  
## LTRIM

**用法**：`ltrim(str)`

移除字串開頭的空格字元。

**參數**：

- `str` (必要)：要移除開頭空格的字串。

**傳回類型**：`STRING`

### 範例
  
```sql
source=people
| eval `LTRIM('   hello')` = LTRIM('   hello'), `LTRIM('hello   ')` = LTRIM('hello   ')
| fields `LTRIM('   hello')`, `LTRIM('hello   ')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| LTRIM('   hello') | LTRIM('hello   ') |
| --- | --- |
| hello | hello |

<!-- vale on -->
  
## POSITION

**用法**：`POSITION(substr IN str)`

傳回 `substr` 在 `str` 中第一次出現的位置。若找不到 `substr` 則傳回 0。若任何引數為 `NULL` 則傳回 `NULL`。

**參數**：

- `substr` (必要)：要搜尋的子字串。
- `str` (必要)：要在其中搜尋的字串。

**傳回類型**：`INTEGER`

### 範例
  
```sql
source=people
| eval `POSITION('world' IN 'helloworld')` = POSITION('world' IN 'helloworld'), `POSITION('invalid' IN 'helloworld')` = POSITION('invalid' IN 'helloworld')
| fields `POSITION('world' IN 'helloworld')`, `POSITION('invalid' IN 'helloworld')`
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| POSITION('world' IN 'helloworld') | POSITION('invalid' IN 'helloworld') |
| --- | --- |
| 6 | 0 |

<!-- vale on -->
  
## REPLACE

**用法**：`replace(str, pattern, replacement)`

傳回一個字串，其中 `str` 中所有符合模式的部分都會被替換為替換字串。若任何引數為 `NULL`，則傳回 `NULL`。

**參數**：

- `str`（必要）：要執行替換的輸入字串。
- `pattern`（必要）：要比對的正規表示式模式（支援 Java 正規表示式語法）。
- `replacement`（必要）：替換字串。

**回傳類型**：`STRING`

**正規表示式支援**：pattern 參數支援 Java 正規表示式語法。

**正規表示式特殊字元**：模式會被解譯為正規表示式（regex）。下列字元在正規表示式中具有特殊意義：`.`、`*`、`+`、`[`、`]`、`(`、`)`、`{`、`}`、`^`、`$`、`|`、`?` 與 `\`。若要以字面方式比對這些字元，請使用反斜線跳脫：
- `example.com` 會變成 `'example\\.com'`（跳脫的句點）。
- `value*` 會變成 `'value\\*'`（跳脫的星號）。
- `price+tax` 會變成 `'price\\+tax'`（跳脫的加號）。

包含多個特殊字元的字串可以使用 `\\Q...\\E` 加上引號，將整個字串視為字面文字。例如，`'\\Qhttps://example.com/path?id=123\\E'` 會將整個 URL 視為字面字串。

### 範例：字面字串替換
  
```sql
source=people
| eval `REPLACE('helloworld', 'world', 'universe')` = REPLACE('helloworld', 'world', 'universe'), `REPLACE('helloworld', 'invalid', 'universe')` = REPLACE('helloworld', 'invalid', 'universe')
| fields `REPLACE('helloworld', 'world', 'universe')`, `REPLACE('helloworld', 'invalid', 'universe')`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| REPLACE('helloworld', 'world', 'universe') | REPLACE('helloworld', 'invalid', 'universe') |
| --- | --- |
| hellouniverse | helloworld |

<!-- vale on -->

### 範例：跳脫特殊字元
  
```sql
source=people
| eval `Replace domain` = REPLACE('api.example.com', 'example\\.com', 'newsite.org'), `Replace with quote` = REPLACE('https://api.example.com/v1', '\\Qhttps://api.example.com\\E', 'http://localhost:8080')
| fields `Replace domain`, `Replace with quote`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| Replace domain | Replace with quote |
| --- | --- |
| api.newsite.org | http://localhost:8080/v1 |

<!-- vale on -->

### 範例：正規表示式模式
  
```sql
source=people
| eval `Remove digits` = REPLACE('test123', '\\d+', ''), `Collapse spaces` = REPLACE('hello  world', ' +', ' '), `Remove special` = REPLACE('hello@world!', '[^a-zA-Z]', '')
| fields `Remove digits`, `Collapse spaces`, `Remove special`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| Remove digits | Collapse spaces | Remove special |
| --- | --- | --- |
| test | hello world | helloworld |

<!-- vale on -->

### 範例：擷取群組與反向參照
  
```sql
source=people
| eval `Swap date` = REPLACE('1/14/2023', '^(\\d{1,2})/(\\d{1,2})/', '$2/$1/'), `Reverse words` = REPLACE('Hello World', '(\\w+) (\\w+)', '$2 $1'), `Extract domain` = REPLACE('user@example.com', '.*@(.+)', '$1')
| fields `Swap date`, `Reverse words`, `Extract domain`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| Swap date | Reverse words | Extract domain |
| --- | --- | --- |
| 14/1/2023 | World Hello | example.com |

<!-- vale on -->

### 範例：進階正規表示式
  
```sql
source=people
| eval `Clean phone` = REPLACE('(555) 123-4567', '[^0-9]', ''), `Remove vowels` = REPLACE('hello world', '[aeiou]', ''), `Add prefix` = REPLACE('test', '^', 'pre_')
| fields `Clean phone`, `Remove vowels`, `Add prefix`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| Clean phone | Remove vowels | Add prefix |
| --- | --- | --- |
| 5551234567 | hll wrld | pre_test |

<!-- vale on -->
  
**PPL 查詢中正規表示式模式的注意事項**：
* 反斜線必須重複兩次以進行跳脫：使用 `\\` 而非 `\`。範例：`\\d` 用於數字模式，`\\w+` 用於單字字元。
* 反向參照同時支援 PCRE 風格（`\1`、`\2`）與 Java 風格（`$1`、`$2`）語法。PCRE 風格的反向參照會在內部自動轉換為 Java 風格。  
  
## REVERSE

**用法**：`REVERSE(str)`

傳回所提供字串的反轉結果。

**參數**：

- `str`（必要）：要反轉的字串。

**回傳類型**：`STRING`

### 範例
  
```sql
source=people
| eval `REVERSE('abcde')` = REVERSE('abcde')
| fields `REVERSE('abcde')`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| REVERSE('abcde') |
| --- |
| edcba |

<!-- vale on -->
  
## RIGHT

**用法**：`right(str, len)`

傳回 `str` 最後 `len` 個字元。若任何引數為 `NULL`，則傳回 `NULL`。

**參數**：

- `str`（必要）：輸入字串。
- `len`（必要）：從右側傳回的字元數。

**回傳類型**：`STRING`

### 範例
  
```sql
source=people
| eval `RIGHT('helloworld', 5)` = RIGHT('helloworld', 5), `RIGHT('HELLOWORLD', 0)` = RIGHT('HELLOWORLD', 0)
| fields `RIGHT('helloworld', 5)`, `RIGHT('HELLOWORLD', 0)`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| RIGHT('helloworld', 5) | RIGHT('HELLOWORLD', 0) |
| --- | --- |
| world |  |

<!-- vale on -->
  
## RTRIM

**用法**：`rtrim(str)`

移除字串尾端的空格字元。

**參數**：

- `str`（必要）：要移除尾端空格的字串。

**回傳類型**：`STRING`

### 範例
  
```sql
source=people
| eval `RTRIM('   hello')` = RTRIM('   hello'), `RTRIM('hello   ')` = RTRIM('hello   ')
| fields `RTRIM('   hello')`, `RTRIM('hello   ')`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| RTRIM('   hello') | RTRIM('hello   ') |
| --- | --- |
| hello | hello |

<!-- vale on -->
  
## SUBSTRING

**用法**：`substring(str, start[, length])`

傳回 `str` 的子字串，從 `start` 開始，長度為 `length` 個字元。若未指定 `length`，則傳回從 `start` 到字串結尾的子字串。

**參數**：

- `str`（必要）：輸入字串。
- `start`（必要）：子字串的起始位置。
- `length`（選用）：子字串的長度。若未指定，則從 `start` 傳回至結尾。

**回傳類型**：`STRING`

**同義詞**：`SUBSTR`

### 範例
  
```sql
source=people
| eval `SUBSTRING('helloworld', 5)` = SUBSTRING('helloworld', 5), `SUBSTRING('helloworld', 5, 3)` = SUBSTRING('helloworld', 5, 3)
| fields `SUBSTRING('helloworld', 5)`, `SUBSTRING('helloworld', 5, 3)`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| SUBSTRING('helloworld', 5) | SUBSTRING('helloworld', 5, 3) |
| --- | --- |
| oworld | owo |

<!-- vale on -->
  
## TRIM

**用法**：`trim(str)`

移除字串開頭與尾端的空格字元。

**參數**：

- `str`（必要）：要移除開頭與尾端空格的字串。

**回傳類型**：`STRING`

### 範例
  
```sql
source=people
| eval `TRIM('   hello')` = TRIM('   hello'), `TRIM('hello   ')` = TRIM('hello   ')
| fields `TRIM('   hello')`, `TRIM('hello   ')`
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| TRIM('   hello') | TRIM('hello   ') |
| --- | --- |
| hello | hello |

<!-- vale on -->
  
## UPPER

**用法**：`upper(string)`

將字串轉換為大寫。

**參數**：

- `string` (必要)：要轉換為大寫的字串。

**傳回類型**：`STRING`

### 範例
  
```sql
source=people
| eval `UPPER('helloworld')` = UPPER('helloworld'), `UPPER('HELLOWORLD')` = UPPER('HELLOWORLD')
| fields `UPPER('helloworld')`, `UPPER('HELLOWORLD')`
```
{% include copy.html %}
  
此查詢傳回下列結果：
  
<!-- vale off -->

| UPPER('helloworld') | UPPER('HELLOWORLD') |
| --- | --- |
| HELLOWORLD | HELLOWORLD |

<!-- vale on -->
  
## REGEXP_REPLACE

**用法**：`regexp_replace(str, pattern, replacement)`

將 `str` 中所有符合 `pattern` 的子字串取代為 `replacement`，並傳回產生的字串。

**參數**：

- `str` (必要)：要執行取代的輸入字串。
- `pattern` (必要)：要比對的正規表示式模式。
- `replacement` (必要)：取代字串。

**傳回類型**：`STRING`

**同義詞**：[REPLACE](#replace)

### 範例
  
```sql
source=people
| eval `DOMAIN` = REGEXP_REPLACE('https://opensearch.org/downloads/', '^https?://(?:www\.)?([^/]+)/.*$', '\1')
| fields `DOMAIN`
```
{% include copy.html %}
  
此查詢傳回下列結果：
  
<!-- vale off -->

| DOMAIN |
| --- |
| opensearch.org |

<!-- vale on -->
