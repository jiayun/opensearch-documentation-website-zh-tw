---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "相關性函式"
parent: Functions
grand_parent: PPL
nav_order: 11
---

# 相關性函式

以相關性為基礎的函式可讓使用者根據查詢相關性，在索引中搜尋文件。這些函式建構於 OpenSearch 引擎搜尋查詢之上，但不支援在外掛程式內以記憶體執行。

您可以使用這些函式進行全域查詢篩選，例如在 `WHERE` 或 `HAVING` 子句中的條件運算式。如需以相關性為基礎之搜尋的詳細資訊，請參閱[使用 SQL/PPL 查詢引擎進行相關性搜尋](https://github.com/opensearch-project/sql/issues/182)。

## MATCH

**用法**：`MATCH(<field_expression>, <query_expression>[, <option>=<option_value>]*)`

對應至 OpenSearch 引擎中的 `match` 查詢。傳回指定欄位符合所提供文字、數字、日期或布林值的文件。

**參數**：

- `<field_expression>` (必要)：要搜尋的欄位。
- `<query_expression>` (必要)：要符合的文字、數字、日期或布林值。
- `<option>` (選用)：以 `<option>=<option_value>` 配對指定的其他選項。

  可用的選項如下：

  - `analyzer`：指定查詢要使用的分析器。
  - `auto_generate_synonyms_phrase`：是否自動產生同義詞片語查詢。
  - `fuzziness`：控制模糊比對行為。
  - `max_expansions`：查詢可擴充的詞元數量上限。
  - `prefix_length`：模糊比對時保持不變的開頭字元數。
  - `fuzzy_transpositions`：模糊比對是否包含兩個相鄰字元的調換。
  - `fuzzy_rewrite`：用於重寫查詢的方法。
  - `lenient`：是否忽略格式相關的失敗。
  - `operator`：用於解譯查詢值中文字的布林邏輯。
  - `minimum_should_match`：必須符合的子句數量下限。
  - `zero_terms_query`：當分析器移除所有詞元時要傳回的內容。
  - `boost`：用於降低或提高相關性分數的浮點值。

**傳回類型**：`BOOLEAN`

#### 範例

下列範例僅使用必要參數，所有選用參數皆設為預設值：
  
```sql
source=accounts
| where match(address, 'Street')
| fields lastname, address
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| lastname | address |
| --- | --- |
| Bond | 671 Bristol Street |
| Bates | 789 Madison Street |

<!-- vale on -->
  
下列範例顯示如何為選用參數設定自訂值：
  
```sql
source=accounts
| where match(firstname, 'Hattie', operator='AND', boost=2.0)
| fields lastname
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| lastname |
| --- |
| Bond |

<!-- vale on -->
  
## MATCH_PHRASE

**用法**：`MATCH_PHRASE(<field_expression>, <query_expression>[, <option>=<option_value>]*)`

對應至 OpenSearch 引擎中的 `match_phrase` 查詢。傳回指定欄位以片語形式符合所提供文字的文件。

**參數**：

- `<field_expression>` (必要)：要搜尋的欄位。
- `<query_expression>` (必要)：要以片語形式符合的文字。
- `<option>` (選用)：以 `<option>=<option_value>` 配對指定的其他選項。

  可用的選項如下：

  - `analyzer`：指定查詢要使用的分析器。
  - `slop`：相符詞元之間的位置數量上限。
  - `zero_terms_query`：當分析器移除所有詞元時要傳回的內容。

**傳回類型**：`BOOLEAN`

為回溯相容性，亦支援 `matchphrase`，並對應至 `match_phrase` 查詢。

#### 範例

下列範例僅使用必要參數，所有選用參數皆設為預設值：
  
```sql
source=books
| where match_phrase(author, 'Alexander Milne')
| fields author, title
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| author | title |
| --- | --- |
| Alan Alexander Milne | The House at Pooh Corner |
| Alan Alexander Milne | Winnie-the-Pooh |

<!-- vale on -->
  
下列範例顯示如何為選用參數設定自訂值：
  
```sql
source=books
| where match_phrase(author, 'Alan Milne', slop = 2)
| fields author, title
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| author | title |
| --- | --- |
| Alan Alexander Milne | The House at Pooh Corner |
| Alan Alexander Milne | Winnie-the-Pooh |

<!-- vale on -->
  
## MATCH_PHRASE_PREFIX

**用法**：`MATCH_PHRASE_PREFIX(<field_expression>, <query_expression>[, <option>=<option_value>]*)`

對應至 OpenSearch 引擎中的 `match_phrase_prefix` 查詢。傳回指定欄位使用最後一個詞元的前置字元比對來符合所提供文字的文件。

**參數**：

- `<field_expression>` (必要)：要搜尋的欄位。
- `<query_expression>` (必要)：使用最後一個詞元的前置字元比對來符合的文字。
- `<option>` (選用)：以 `<option>=<option_value>` 配對指定的其他選項。

  可用的選項如下：

  - `analyzer`：指定查詢要使用的分析器。
  - `slop`：相符詞元之間的位置數量上限。
  - `max_expansions`：所提供最後一個詞元可擴充的詞元數量上限。
  - `boost`：用於降低或提高相關性分數的浮點值。
  - `zero_terms_query`：當分析器移除所有詞元時要傳回的內容。

**傳回類型**：`BOOLEAN`

#### 範例

下列範例僅使用必要參數，所有選用參數皆設為預設值：
  
```sql
source=books
| where match_phrase_prefix(author, 'Alexander Mil')
| fields author, title
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| author | title |
| --- | --- |
| Alan Alexander Milne | The House at Pooh Corner |
| Alan Alexander Milne | Winnie-the-Pooh |

<!-- vale on -->
  
下列範例顯示如何為選用參數設定自訂值：
  
```sql
source=books
| where match_phrase_prefix(author, 'Alan Mil', slop = 2)
| fields author, title
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| author | title |
| --- | --- |
| Alan Alexander Milne | The House at Pooh Corner |
| Alan Alexander Milne | Winnie-the-Pooh |

<!-- vale on -->
  
## MULTI_MATCH

**用法**：
- `MULTI_MATCH([<field_expression+>], <query_expression>[, <option>=<option_value>]*)`。
- `MULTI_MATCH(<query_expression>[, <option>=<option_value>]*)`。

對應至 OpenSearch 引擎中的 `multi_match query`。傳回一或多個指定欄位符合所提供文字、數字、日期或布林值的文件。

**支援兩種語法形式**：
1. **含明確欄位** (傳統語法)：`multi_match([field_list], query, ...)`
2. **不含欄位** (搜尋預設欄位)：`multi_match(query, ...)`

省略欄位時，查詢會搜尋 `index.query.default_field` 設定所指定的欄位。

您可以使用 `^` 符號提升特定欄位的權重。提升值是乘數，可讓某個欄位的相符結果比其他欄位的相符結果更具權重。您可以使用雙引號、單引號、反引號或不加引號來指定欄位。您也可以使用 `"*"` 搜尋所有欄位 (星號符號必須以引號括住)。提升值為選用，且應指定於欄位名稱之後，並以 `^` 字元或空白分隔：
- `multi_match(["Tags" ^ 2, 'Title' 3.4, `Body`, Comments ^ 0.3], ...)`。
- `multi_match(["*"], ...)`。
- `multi_match("search text", ...)` (搜尋預設欄位)。

**參數**：

- `<field_expression+>` (選用)：要搜尋的欄位清單，可包含選用的提升值。
- `<query_expression>` (必要)：要符合的文字、數字、日期或布林值。
- `<option>` (選用)：以 `<option>=<option_value>` 配對指定的其他選項。

  可用的選項如下：

  - `analyzer`：指定查詢要使用的分析器。
  - `auto_generate_synonyms_phrase`：是否自動產生同義詞片語查詢。
  - `cutoff_frequency`：允許將高頻詞元放入查詢中。
  - `fuzziness`：控制模糊比對行為。
  - `fuzzy_transpositions`：模糊比對是否包含兩個相鄰字元的調換。
  - `lenient`：是否忽略格式相關的失敗。
  - `max_expansions`：查詢可擴充的詞元數量上限。
  - `minimum_should_match`：必須符合的子句數量下限。
  - `operator`：用於解譯查詢值中文字的布林邏輯。
  - `prefix_length`：模糊比對時保持不變的開頭字元數。
  - `tie_breaker`：介於 0.0 與 1.0 之間的值，用於在相關性相同的欄位之間做為決勝依據。
  - `type`：multi_match 查詢在內部應如何執行。
  - `slop`：相符詞元之間的位置數量上限 (適用於片語查詢)。
  - `boost`：用於降低或提高相關性分數的浮點值。

**傳回類型**：`BOOLEAN`

#### 範例

下列範例明確指定欄位，且僅使用必要參數：
  
```sql
source=books
| where multi_match(['title'], 'Pooh House')
| fields id, title, author
```
{% include copy.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| id | title | author |
| --- | --- | --- |
| 1 | The House at Pooh Corner | Alan Alexander Milne |
| 2 | Winnie-the-Pooh | Alan Alexander Milne |

<!-- vale on -->

下列範例示範明確指定欄位並搭配選用參數：
  
```sql
source=books
| where multi_match(['title'], 'Pooh House', operator='AND', analyzer=default)
| fields id, title, author
```
{% include copy.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| id | title | author |
| --- | --- | --- |
| 1 | The House at Pooh Corner | Alan Alexander Milne |

<!-- vale on -->

下列範例使用預設欄位語法，未明確指定欄位：
  
```sql
source=books
| where multi_match('Pooh House')
| fields id, title, author
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| id | title | author |
| --- | --- | --- |
| 1 | The House at Pooh Corner | Alan Alexander Milne |
| 2 | Winnie-the-Pooh | Alan Alexander Milne |

<!-- vale on -->
  
## SIMPLE_QUERY_STRING

**用法**：
- `SIMPLE_QUERY_STRING([<field_expression+>], <query_expression>[, <option>=<option_value>]*)`。
- `SIMPLE_QUERY_STRING(<query_expression>[, <option>=<option_value>]*)`。

對應至 OpenSearch 引擎中的 `simple_query_string` 查詢。傳回一或多個指定欄位符合所提供之文字、數字、日期或布林值的文件。

**支援兩種語法形式**：
1. **明確指定欄位**（傳統語法）：`simple_query_string([field_list], query, ...)`
2. **不指定欄位**（搜尋預設欄位）：`simple_query_string(query, ...)`

省略欄位時，查詢會在 `index.query.default_field` 設定所指定的欄位中搜尋。

您可以使用 `^` 符號提升特定欄位的權重。提升值是乘數，可讓某個欄位中的相符項目比其他欄位中的相符項目具有更高的權重。您可以使用雙引號、單引號、反引號或不加引號來指定欄位。您也可以使用 `"*"` 搜尋所有欄位（星號必須以引號括住）。提升值為選用，應指定於欄位名稱之後，並以 `^` 字元或空白分隔：
- `simple_query_string(["Tags" ^ 2, 'Title' 3.4, `Body`, Comments ^ 0.3], ...)`。
- `simple_query_string(["*"], ...)`。
- `simple_query_string("search text", ...)`（搜尋預設欄位）。

**參數**：

- `<field_expression+>`（選用）：要搜尋的欄位清單，可附帶選用的提升值。
- `<query_expression>`（必要）：要比對的文字、數字、日期或布林值。
- `<option>`（選用）：以 `<option>=<option_value>` 配對指定的其他選項。

  可用的選項如下：

  - `analyze_wildcard`：是否分析萬用字元查詢與前綴查詢。
  - `analyzer`：指定查詢要使用的分析器。
  - `auto_generate_synonyms_phrase`：是否自動產生同義詞片語查詢。
  - `flags`：用於啟用簡易查詢字串運算子的旗標。
  - `fuzziness`：控制模糊比對行為。
  - `fuzzy_max_expansions`：模糊查詢可展開的最大詞彙數。
  - `fuzzy_prefix_length`：模糊比對時保持不變的開頭字元數。
  - `fuzzy_transpositions`：模糊比對是否包含兩個相鄰字元的換位。
  - `lenient`：是否忽略因格式造成的失敗。
  - `default_operator`：用於解譯查詢中文字的預設布林邏輯。
  - `minimum_should_match`：必須符合的最少子句數。
  - `quote_field_suffix`：附加至查詢字串中引號內文字的後綴。
  - `boost`：用於降低或提高相關性分數的浮點數值。

**傳回類型**：`BOOLEAN`

#### 範例

下列範例明確指定欄位，且僅使用必要參數：
  
```sql
source=books
| where simple_query_string(['title'], 'Pooh House')
| fields id, title, author
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| id | title | author |
| --- | --- | --- |
| 1 | The House at Pooh Corner | Alan Alexander Milne |
| 2 | Winnie-the-Pooh | Alan Alexander Milne |

<!-- vale on -->

下列範例示範明確指定欄位並搭配選用參數：

```sql
source=books
| where simple_query_string(['title'], 'Pooh House', flags='ALL', default_operator='AND')
| fields id, title, author
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| id | title | author |
| --- | --- | --- |
| 1 | The House at Pooh Corner | Alan Alexander Milne |

<!-- vale on -->

下列範例使用預設欄位語法，未明確指定欄位：

```sql
source=books
| where simple_query_string('Pooh House')
| fields id, title, author
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| id | title | author |
| --- | --- | --- |
| 1 | The House at Pooh Corner | Alan Alexander Milne |
| 2 | Winnie-the-Pooh | Alan Alexander Milne |

<!-- vale on -->
  
## MATCH_BOOL_PREFIX

**用法**：`MATCH_BOOL_PREFIX(<field_expression>, <query_expression>[, <option>=<option_value>]*)`

對應至 OpenSearch 引擎中的 `match_bool_prefix` 查詢。傳回指定欄位符合所提供文字的文件，其中除了最後一個詞彙之外，所有詞彙都必須完全相符，而最後一個詞彙則視為前綴。

**參數**：

- `<field_expression>`（必要）：要搜尋的欄位。
- `<query_expression>`（必要）：要比對的文字，其中最後一個詞彙會視為前綴。
- `<option>`（選用）：以 `<option>=<option_value>` 配對指定的其他選項。

  可用的選項如下：

  - `analyzer`：指定查詢要使用的分析器。
  - `fuzziness`：控制模糊比對行為。
  - `max_expansions`：查詢可展開的最大詞彙數。
  - `prefix_length`：模糊比對時保持不變的開頭字元數。
  - `fuzzy_transpositions`：模糊比對是否包含兩個相鄰字元的換位。
  - `operator`：用於解譯查詢值中文字的布林邏輯。
  - `fuzzy_rewrite`：用於重寫查詢的方法。
  - `minimum_should_match`：必須符合的最少子句數。
  - `boost`：用於降低或提高相關性分數的浮點數值。

**傳回類型**：`BOOLEAN`

#### 範例

下列範例僅使用必要參數，所有選用參數皆設為預設值：
  
```sql
source=accounts
| where match_bool_prefix(address, 'Bristol Stre')
| fields firstname, address
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| firstname | address |
| --- | --- |
| Hattie | 671 Bristol Street |
| Nanette | 789 Madison Street |

<!-- vale on -->

下列範例示範如何設定選用參數：
  
```sql
source=accounts
| where match_bool_prefix(address, 'Bristol Stre', minimum_should_match = 2)
| fields firstname, address
```
{% include copy.html %}
  
此查詢會傳回下列結果：
  
<!-- vale off -->

| firstname | address |
| --- | --- |
| Hattie | 671 Bristol Street |

<!-- vale on -->
  
## QUERY_STRING

**用法**：
- `QUERY_STRING([<field_expression+>], <query_expression>[, <option>=<option_value>]*)`。
- `QUERY_STRING(<query_expression>[, <option>=<option_value>]*)`。

對應至 OpenSearch 引擎中的 `query_string` 查詢。回傳一或多個指定欄位符合所提供文字、數字、日期或布林值的文件。

**支援兩種語法形式**：
1. **明確指定欄位**（傳統語法）：`query_string([field_list], query, ...)`
2. **不指定欄位**（搜尋預設欄位）：`query_string(query, ...)`

省略欄位時，查詢會在 `index.query.default_field` 設定所指定的欄位中搜尋。

您可以使用 `^` 符號提高特定欄位的權重。提升值是乘數，會讓某個欄位中的相符結果比其他欄位中的相符結果獲得更高的權重。您可以使用雙引號、單引號、反引號或不加引號來指定欄位。您也可以使用 `"*"` 搜尋所有欄位（星號必須以引號包住）。提升值為選用，應在欄位名稱之後指定，並以 `^` 字元或空白分隔：
- `query_string(["Tags" ^ 2, 'Title' 3.4, `Body`, Comments ^ 0.3], ...)`。
- `query_string(["*"], ...)`。
- `query_string("search text", ...)`（搜尋預設欄位）。

**參數**：

- `<field_expression+>`（選用）：要搜尋的欄位清單，可附帶提升值。
- `<query_expression>`（必要）：要比對的文字、數字、日期或布林值。
- `<option>`（選用）：以 `<option>=<option_value>` 成對指定的其他選項。

  可用的選項如下：

  - `analyzer`：指定查詢要使用的分析器。
  - `escape`：是否跳脫查詢字串中的特殊字元。
  - `allow_leading_wildcard`：是否允許前置萬用字元。
  - `analyze_wildcard`：是否分析萬用字元與前置詞查詢。
  - `auto_generate_synonyms_phrase_query`：是否自動產生同義詞片語查詢。
  - `boost`：用於降低或提高相關性分數的浮點數值。
  - `default_operator`：用於解讀查詢文字的預設布林邏輯。
  - `enable_position_increments`：是否在結果查詢中啟用位置增量。
  - `fuzziness`：控制模糊比對行為。
  - `fuzzy_max_expansions`：模糊查詢可擴展的最大詞彙數。
  - `fuzzy_prefix_length`：模糊比對時保持不變的開頭字元數。
  - `fuzzy_transpositions`：模糊比對是否包含兩個相鄰字元的調換。
  - `fuzzy_rewrite`：用於改寫模糊查詢的方法。
  - `tie_breaker`：介於 0.0 與 1.0 之間的數值，用於在相關性相同的欄位之間進行平手裁決。
  - `lenient`：是否忽略格式相關的失敗。
  - `type`：query_string 查詢在內部的執行方式。
  - `max_determinized_states`：regexp 或模糊查詢的自動機狀態數上限。
  - `minimum_should_match`：必須符合的最小子句數。
  - `quote_analyzer`：查詢字串中引號內文字要使用的分析器。
  - `phrase_slop`：由查詢字串建立的片語查詢的預設 slop 值。
  - `quote_field_suffix`：附加至查詢字串中引號內文字的後綴。
  - `rewrite`：用於改寫查詢的方法。
  - `time_zone`：日期範圍查詢要使用的時區。

**回傳類型**：`BOOLEAN`

#### 範例

下列範例僅使用必要參數並明確指定欄位：
  
```sql
source=books
| where query_string(['title'], 'Pooh House')
| fields id, title, author
```
{% include copy.html %}
  
查詢回傳下列結果：
  
<!-- vale off -->

| id | title | author |
| --- | --- | --- |
| 1 | The House at Pooh Corner | Alan Alexander Milne |
| 2 | Winnie-the-Pooh | Alan Alexander Milne |

<!-- vale on -->

下列範例示範明確指定欄位並使用選用參數：

```sql
source=books
| where query_string(['title'], 'Pooh House', default_operator='AND')
| fields id, title, author
```
{% include copy.html %}
  
查詢回傳下列結果：
  
<!-- vale off -->

| id | title | author |
| --- | --- | --- |
| 1 | The House at Pooh Corner | Alan Alexander Milne |

<!-- vale on -->
  
下列範例使用預設欄位語法，未明確指定欄位：
  
```sql
source=books
| where query_string('Pooh House')
| fields id, title, author
```
{% include copy.html %}
  
查詢回傳下列結果：
  
<!-- vale off -->

| id | title | author |
| --- | --- | --- |
| 1 | The House at Pooh Corner | Alan Alexander Milne |
| 2 | Winnie-the-Pooh | Alan Alexander Milne |

<!-- vale on -->
  
## 限制

相關性函式只能在 OpenSearch Query DSL 中執行，無法在記憶體中執行。如果查詢過於複雜而無法轉譯為 DSL，相關性搜尋可能會失敗，尤其是當相關性函式位於複雜的 PPL 操作之後時。

為確保正確執行，請將相關性函式盡量放在靠近 `search` 命令的位置。這樣可提高函式符合下推最佳化資格的可能性。

**有問題的查詢結構範例**：
```sql
search source = people
| rename firstname as name
| dedup account_number
| fields name, account_number, balance, employer
| where match(employer, 'Open Search')
| stats count() by city
```

請將包含相關性函式的 `where` 命令緊接在 `search` 命令之後，讓函式能夠被最佳化並在 OpenSearch DSL 中執行。

**建議的查詢結構**：
```sql
search source = people
| where match(employer, 'Open Search')
| rename firstname as name
| dedup account_number
| fields name, account_number, balance, employer
| stats count() by city
```

<!-- temporarily commented out because the optimization section is not ported
See [Optimization]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/optimization/optimization/) to get more details about the query engine optimization.

-->
