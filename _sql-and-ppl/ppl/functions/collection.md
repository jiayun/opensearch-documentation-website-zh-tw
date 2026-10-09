---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "集合函式"
parent: Functions
grand_parent: PPL
nav_order: 2
---

# 集合函式

集合函式會建立、操作及分析資料中的陣列與多值欄位。這些函式對於處理複雜的資料結構，以及執行篩選、轉換和分析陣列元素等作業至關重要。

PPL 支援下列集合函式。

## ARRAY

**用法**：`array(value1, value2, value3...)`

建立包含輸入值的陣列。混合類型會自動轉換為限制最少的類型。例如，`array(1, "demo")` 會傳回 `["1", "demo"]`，其中整數會轉換為字串。

**參數**：

- `value1` (必要)：要包含在陣列中的任意類型值。
- `value2`、`value3` (選用)：要包含在陣列中的其他任意類型值。

**傳回類型**：`ARRAY`

#### 範例

下列範例會建立包含數值的陣列：

```sql
source=people
| eval array = array(1, 2, 3)
| fields array
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| array |
| --- |
| [1,2,3] |

<!-- vale on -->

下列範例示範混合類型轉換：

```sql
source=people
| eval array = array(1, "demo")
| fields array
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：
  
<!-- vale off -->

| array |
| --- |
| [1,demo] |

<!-- vale on -->
  
## ARRAY_LENGTH

**用法**：`array_length(array)`

傳回輸入 `array` 的長度。

**參數**：

- `array` (必要)：要傳回長度的陣列。

**傳回類型**：`INTEGER`

#### 範例

```sql
source=people
| eval array = array(1, 2, 3)
| eval length = array_length(array)
| fields length
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：
  
<!-- vale off -->

| length |
| --- |
| 3 |

<!-- vale on -->
  
## FORALL

**用法**：`forall(array, function)`

檢查陣列中的所有元素是否都符合 lambda 函式條件。lambda 函式必須接受單一輸入參數並傳回布林值。

**參數**：

- `array` (必要)：要檢查的陣列。
- `function` (必要)：傳回布林值並接受單一輸入參數的 lambda 函式。

**傳回類型**：`BOOLEAN`

#### 範例

```sql
source=people
| eval array = array(1, 2, 3), result = forall(array, x -> x > 0)
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：
  
<!-- vale off -->

| result |
| --- |
| True |

<!-- vale on -->
  
## EXISTS

**用法**：`exists(array, function)`

檢查陣列中是否至少有一個元素符合 lambda 函式條件。lambda 函式必須接受單一輸入參數並傳回布林值。

**參數**：

- `array` (必要)：要檢查的陣列。
- `function` (必要)：傳回布林值並接受單一輸入參數的 lambda 函式。

**傳回類型**：`BOOLEAN`

#### 範例

```sql
source=people
| eval array = array(-1, -2, 3), result = exists(array, x -> x > 0)
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：
  
<!-- vale off -->

| result |
| --- |
| True |

<!-- vale on -->
  
## FILTER

**用法**：`filter(array, function)`

使用 lambda 函式篩選陣列中的元素。lambda 函式必須接受單一輸入參數並傳回布林值。

**參數**：

- `array` (必要)：要篩選的陣列。
- `function` (必要)：傳回布林值並接受單一輸入參數的 lambda 函式。

**傳回類型**：`ARRAY`

#### 範例

```sql
source=people
| eval array = array(1, -2, 3), result = filter(array, x -> x > 0)
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：
  
<!-- vale off -->

| result |
| --- |
| [1,3] |

<!-- vale on -->
  
## TRANSFORM

**用法**：`transform(array, function)`

使用 lambda 函式逐一轉換 `array` 的元素。lambda 函式可以接受一或兩個輸入。如果 lambda 函式接受兩個參數，第二個參數是元素在 `array` 中的索引。

**參數**：

- `array` (必要)：要轉換的陣列。
- `function` (必要)：接受一或兩個輸入參數並傳回轉換後值的 lambda 函式。

**傳回類型**：`ARRAY`

#### 範例

下列範例會將每個元素加上 2 來進行轉換：

```sql
source=people
| eval array = array(1, -2, 3), result = transform(array, x -> x + 2)
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [3,0,5] |

<!-- vale on -->

下列範例在轉換中同時使用元素值和索引：

```sql
source=people
| eval array = array(1, -2, 3), result = transform(array, (x, i) -> x + i)
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：
  
<!-- vale off -->

| result |
| --- |
| [1,-1,5] |

<!-- vale on -->
  
## REDUCE

**用法**：`reduce(array, acc_base, function, <reduce_function>)`

使用 lambda 函式逐一查看所有元素，並與累加器基礎值互動。lambda 函式接受兩個參數：累加器和陣列元素。提供選用的 `reduce_function` 時，會套用至最終的累加器值。reduce 函式接受累加器作為單一參數。

**參數**：

- `array` (必要)：要縮減的陣列。
- `acc_base` (必要)：初始累加器值。
- `function` (必要)：接受累加器和陣列元素作為參數的 lambda 函式。
- `reduce_function` (選用)：要套用至最終累加器值的 lambda 函式。

**傳回類型**：與累加器類型相同 (由 `acc_base` 和 `reduce_function` 決定)

#### 範例

下列範例會使用初始值加總所有元素來縮減陣列：

```sql
source=people
| eval array = array(1, -2, 3), result = reduce(array, 10, (acc, x) -> acc + x)
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| 12 |

<!-- vale on -->

下列範例使用額外的 reduce 函式來轉換最終結果：

```sql
source=people
| eval array = array(1, -2, 3), result = reduce(array, 10, (acc, x) -> acc + x, acc -> acc * 10)
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：
  
<!-- vale off -->

| result |
| --- |
| 120 |

<!-- vale on -->
  
## MVJOIN

**用法**：`mvjoin(array, delimiter)`

將字串陣列元素聯結成單一字串，並以指定的分隔符號分隔。`NULL` 元素會從輸出中排除。僅支援字串陣列。

**參數**：

- `array` (必要)：要聯結的字串陣列。
- `delimiter` (必要)：用來作為陣列元素之間分隔符號的字串。

**傳回類型**：`STRING`

#### 範例

下列範例會以逗號分隔符號聯結字串陣列：

```sql
source=people
| eval result = mvjoin(array('a', 'b', 'c'), ',')
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| a,b,c |

<!-- vale on -->

下列範例會將欄位值聯結成單一字串：

```sql
source=accounts
| eval names_array = array(firstname, lastname)
| eval result = mvjoin(names_array, ', ')
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：
  
<!-- vale off -->

| result |
| --- |
| Amber, Duke |

<!-- vale on -->
  
## MVAPPEND

**用法**: `mvappend(value1, value2, value3...)`

附加參數中的所有元素以建立陣列。將陣列參數攤平，並收集所有個別元素。一律傳回陣列或 `NULL`，以維持一致的類型行為。

**參數**:

- `value1`（必要）：要附加至陣列的任意類型值。
- `value2`（選用）：要附加至陣列的其他任意類型值。
- `...`（選用）：任意數量的其他值。

**傳回類型**: `ARRAY`

#### 範例

下列範例附加多個值以建立陣列：

```sql
source=people
| eval result = mvappend(1, 1, 3)
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：
  
<!-- vale off -->

| result |
| --- |
| [1,1,3] |

<!-- vale on -->

下列範例示範如何攤平陣列：

```sql
source=people
| eval result = mvappend(1, array(2, 3))
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：
  
<!-- vale off -->

| result |
| --- |
| [1,2,3] |

<!-- vale on -->

下列範例顯示巢狀的 `mvappend` 呼叫：

```sql
source=people
| eval result = mvappend(mvappend(1, 2), 3)
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [1,2,3] |

<!-- vale on -->

下列範例從單一值建立陣列：

```sql
source=people
| eval result = mvappend(42)
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [42] |

<!-- vale on -->

下列範例示範如何篩除 `NULL` 值：

```sql
source=people
| eval result = mvappend(nullif(1, 1), 2)
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [2] |

<!-- vale on -->

下列範例顯示僅有 `NULL` 值時的行為：

```sql
source=people
| eval result = mvappend(nullif(1, 1))
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| null |

<!-- vale on -->

下列範例串接多個陣列：

```sql
source=people
| eval arr1 = array(1, 2), arr2 = array(3, 4), result = mvappend(arr1, arr2)
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [1,2,3,4] |

<!-- vale on -->

下列範例附加欄位值：

```sql
source=accounts
| eval result = mvappend(firstname, lastname)
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [Amber,Duke] |

<!-- vale on -->

下列範例示範混合資料類型：

```sql
source=people
| eval result = mvappend(1, 'text', 2.5)
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [1,text,2.5] |

<!-- vale on -->
  
## SPLIT

**用法**: `split(str, delimiter)`

依分隔符號分割字串值，並以多值欄位（陣列）傳回字串值。使用空字串（`""`）可將原始字串分割成每個字元各為一個值。若找不到分隔符號，函式會傳回包含原始字串的陣列。若輸入字串為空，函式會傳回空陣列。

**參數**:

- `str`（必要）：要分割的字串。
- `delimiter`（必要）：分割時要用作分隔符號的字串。

**傳回類型**: `ARRAY`

#### 範例

下列範例使用分號作為分隔符號來分割字串：

```sql
source=people
| eval test = 'buttercup;rarity;tenderhoof;dash', result = split(test, ';')
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [buttercup,rarity,tenderhoof,dash] |

<!-- vale on -->

下列範例使用多字元分隔符號：

```sql
source=people
| eval test = '1a2b3c4def567890', result = split(test, 'def')
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [1a2b3c4,567890] |

<!-- vale on -->

下列範例使用空分隔符號將字串分割成個別字元：

```sql
source=people
| eval test = 'abcd', result = split(test, '')
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [a,b,c,d] |

<!-- vale on -->

下列範例使用雙冒號作為分隔符號進行分割：

```sql
source=people
| eval test = 'name::value', result = split(test, '::')
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [name,value] |

<!-- vale on -->

下列範例顯示找不到分隔符號時的行為：

```sql
source=people
| eval test = 'hello', result = split(test, ',')
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [hello] |

<!-- vale on -->
  
## MVDEDUP

**用法**: `mvdedup(array)`

移除多值陣列中的重複值，同時保留各值首次出現的順序。`NULL` 元素會被篩除。傳回移除重複值後的陣列；若輸入為 `NULL`，則傳回 `NULL`。

**參數**:

- `array`（必要）：要移除重複值的陣列。

**傳回類型**: `ARRAY`

#### 範例

下列範例移除重複的數字，同時保留順序：

```sql
source=people
| eval array = array(1, 2, 2, 3, 1, 4), result = mvdedup(array)
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [1,2,3,4] |

<!-- vale on -->

下列範例移除重複的字串值：

```sql
source=people
| eval array = array('z', 'a', 'z', 'b', 'a', 'c'), result = mvdedup(array)
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [z,a,b,c] |

<!-- vale on -->

下列範例顯示使用空陣列時的行為：

```sql
source=people
| eval array = array(), result = mvdedup(array)
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [] |

<!-- vale on -->

## MVFIND

**用法**: `mvfind(array, regex)`

搜尋多值陣列，並傳回第一個符合規則運算式的元素以 `0` 為起點的索引。若找不到相符項目，則傳回 `NULL`。

**參數**:

- `array`（必要）：要搜尋的陣列。
- `regex`（必要）：用來比對陣列元素的規則運算式模式。

**傳回類型**: `INTEGER`（若找不到相符項目，則為 `NULL`）

#### 範例

下列範例搜尋第一個符合規則運算式的元素：

```sql
source=people
| eval array = array('apple', 'banana', 'apricot'), result = mvfind(array, 'ban.*')
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| 1 |

<!-- vale on -->

下列範例顯示找不到相符項目時的行為：

```sql
source=people
| eval array = array('cat', 'dog', 'bird'), result = mvfind(array, 'fish')
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| null |

<!-- vale on -->

下列範例使用含有字元類別的規則運算式模式：

```sql
source=people
| eval array = array('error123', 'info', 'error456'), result = mvfind(array, 'error[0-9]+')
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| 0 |

<!-- vale on -->

下列範例示範不區分大小寫的比對：

```sql
source=people
| eval array = array('Apple', 'Banana', 'Cherry'), result = mvfind(array, '(?i)banana')
| fields result
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| result |
| --- |
| 1 |

<!-- vale on -->

## MVINDEX

**用法**：`mvindex(array, start, [end])`

使用起始索引值與選用的結束索引值，傳回多值陣列的子集。索引以 `0` 為起點（第一個元素位於索引 `0`）。支援負數索引，其中 `-1` 代表最後一個元素。若只提供 start，函式會傳回單一元素。若同時提供 start 與 end，函式會傳回從 start 到 end（含）的元素陣列。

**參數**：

- `array`（必要）：要從中擷取元素的陣列。
- `start`（必要）：起始索引（以 `0` 為起點）。
- `end`（選用）：結束索引（以 `0` 為起點，包含該索引）。

**傳回類型**：只提供 `start` 時為單一元素的類型；同時提供 `start` 與 `end` 時為 `ARRAY`

#### 範例

下列範例取得索引 1 的單一元素：

```sql
source=people
| eval array = array('a', 'b', 'c', 'd', 'e'), result = mvindex(array, 1)
| fields result
| head 1
```
{% include copy.html %}

此查詢傳回下列結果：

<!-- vale off -->

| result |
| --- |
| b |

<!-- vale on -->

下列範例使用負數索引取得最後一個元素：

```sql
source=people
| eval array = array('a', 'b', 'c', 'd', 'e'), result = mvindex(array, -1)
| fields result
| head 1
```
{% include copy.html %}

此查詢傳回下列結果：

<!-- vale off -->

| result |
| --- |
| e |

<!-- vale on -->

下列範例擷取一個範圍內的元素：

```sql
source=people
| eval array = array(1, 2, 3, 4, 5), result = mvindex(array, 1, 3)
| fields result
| head 1
```
{% include copy.html %}

此查詢傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [2,3,4] |

<!-- vale on -->

下列範例使用負數索引指定範圍：

```sql
source=people
| eval array = array(1, 2, 3, 4, 5), result = mvindex(array, -3, -1)
| fields result
| head 1
```
{% include copy.html %}

此查詢傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [3,4,5] |

<!-- vale on -->

下列範例從陣列開頭擷取元素：

```sql
source=people
| eval array = array('alex', 'celestino', 'claudia', 'david'), result = mvindex(array, 0, 2)
| fields result
| head 1
```
{% include copy.html %}

此查詢傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [alex,celestino,claudia] |

<!-- vale on -->

## MVMAP

**用法**：`mvmap(array, expression)`

逐一走訪多值陣列的每個元素，將運算式套用至每個元素，並傳回包含轉換結果的多值陣列。運算式中的欄位名稱會隱含繫結至每個元素值。

**參數**：

- `array`（必要）：要對應處理的陣列。
- `expression`（必要）：要套用至每個元素的運算式。

**傳回類型**：`ARRAY`

#### 範例

下列範例對陣列的每個元素套用數學運算：

```sql
source=people
| eval array = array(1, 2, 3), result = mvmap(array, array * 10)
| fields result
| head 1
```
{% include copy.html %}

此查詢傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [10,20,30] |

<!-- vale on -->

下列範例套用另一種數學運算：

```sql
source=people
| eval array = array(1, 2, 3), result = mvmap(array, array + 5)
| fields result
| head 1
```
{% include copy.html %}

此查詢傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [6,7,8] |

<!-- vale on -->

對於 `mvmap(mvindex(arr, 1, 3), arr * 2)` 這類巢狀運算式，欄位名稱（`arr`）會從第一個引數中擷取，且必須與運算式中參照的欄位相符。
{: .note}

下列範例說明運算式如何參照其他單值欄位：

```sql
source=people
| eval array = array(1, 2, 3), multiplier = 10, result = mvmap(array, array * multiplier)
| fields result
| head 1
```
{% include copy.html %}

此查詢傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [10,20,30] |

<!-- vale on -->


## MVZIP

**用法**：`mvzip(mv_left, mv_right, [delim])`

將兩個多值陣列中對應的元素配對並連接成字串，藉此合併兩個陣列的值。分隔符號用於指定連接兩個值所用的字元或字串。這與 Python 的 zip 命令類似。

合併方式是將 `mv_left` 的第一個值與 `mv_right` 的第一個值配對，接著第二個與第二個配對，依此類推。每一組配對會使用分隔符號串接成一個字串。函式會在較短陣列的長度處停止。

分隔符號為選用。若有指定，必須以引號括住。預設分隔符號為逗號。

若任一輸入為 `NULL`，則傳回 `NULL`。若任一輸入陣列為空，則傳回空陣列。

**參數**：

- `mv_left`（必要）：要合併的第一個陣列。
- `mv_right`（必要）：要合併的第二個陣列。
- `delim`（選用）：用於連接配對的分隔符號。預設為逗號。

**傳回類型**：`ARRAY`

#### 範例

下列範例使用冒號分隔符號合併主機與連接埠陣列：

```sql
source=people
| eval hosts = array('host1', 'host2'), ports = array('80', '443'), nserver = mvzip(hosts, ports, ':')
| fields nserver
| head 1
```
{% include copy.html %}

此查詢傳回下列結果：

<!-- vale off -->

| nserver |
| --- |
| [host1:80,host2:443] |

<!-- vale on -->

下列範例對長度相同的陣列使用管線符號分隔符號：

```sql
source=people
| eval arr1 = array('a', 'b', 'c'), arr2 = array('x', 'y', 'z'), result = mvzip(arr1, arr2, '|')
| fields result
| head 1
```
{% include copy.html %}

此查詢傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [a|x,b|y,c|z] |

<!-- vale on -->

下列範例示範陣列長度不同時的行為：

```sql
source=people
| eval arr1 = array('1', '2', '3'), arr2 = array('a', 'b'), result = mvzip(arr1, arr2, '-')
| fields result
| head 1
```
{% include copy.html %}

此查詢傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [1-a,2-b] |

<!-- vale on -->

下列範例示範巢狀的 `mvzip` 呼叫：

```sql
source=people
| eval arr1 = array('a', 'b', 'c'), arr2 = array('x', 'y', 'z'), arr3 = array('1', '2', '3'), result = mvzip(mvzip(arr1, arr2, '-'), arr3, ':')
| fields result
| head 1
```
{% include copy.html %}

此查詢傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [a-x:1,b-y:2,c-z:3] |

<!-- vale on -->

下列範例示範空陣列時的行為：

```sql
source=people
| eval arr1 = array('a', 'b'), arr2 = array(), result = mvzip(arr1, arr2)
| fields result
| head 1
```
{% include copy.html %}

此查詢傳回下列結果：

<!-- vale off -->

| result |
| --- |
| [] |

<!-- vale on -->
