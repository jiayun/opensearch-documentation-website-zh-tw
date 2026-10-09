---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "JSON 函式"
parent: Functions
grand_parent: PPL
nav_order: 9
---

# JSON 函式

PPL 支援下列 JSON 函式，用於建立、剖析及操作 JSON 資料。

## JSON path

JSON 函式中使用的所有 JSON 路徑都遵循 `<key1>{<index1>}.<key2>{<index2>}...` 格式。
每個 `<key>` 代表一個欄位名稱。`{<index>}` 部分為選用，僅在對應的鍵指向陣列時使用。
例如：

```bash
a{2}.b{0}
```
{% include copy.html %}

此路徑存取 `b` 陣列中索引 `0` 處的元素，而該陣列位於 `a` 陣列中索引 `2` 處的元素內。

**注意**：
1. `{<index>}` 標記法僅在相關的鍵指向陣列時適用。
2. `{}` (不含特定索引) 會被解讀為萬用字元，等同於 `{*}`，表示該層級陣列中的 `all elements`。

## JSON

**用法**：`JSON(value)`

驗證並剖析 JSON 字串。若字串是有效的 JSON，則傳回剖析後的 JSON 值；若無效，則傳回 `NULL`。

**參數**：

- `value` (必要)：要驗證並剖析為 JSON 的字串。

**回傳類型**：`STRING`

#### 範例

```sql
source=json_test
| where json_valid(json_string)
| eval json=json(json_string)
| fields test_name, json_string, json
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| test_name | json_string | json |
| --- | --- | --- |
| json nested object | {"a":"1","b":{"c":"2","d":"3"}} | {"a":"1","b":{"c":"2","d":"3"}} |
| json object | {"a":"1","b":"2"} | {"a":"1","b":"2"} |
| json array | [1, 2, 3, 4] | [1, 2, 3, 4] |
| json scalar string | "abc" | "abc" |

<!-- vale on -->

## JSON_VALID

**用法**：`JSON_VALID(value)`

評估字串是否使用有效的 JSON 語法。若有效則傳回 `TRUE`，若無效則傳回 `FALSE`。`NULL` 輸入會傳回 `NULL`。

**版本**：3.1.0
**限制**：僅在 `plugins.calcite.enabled=true` 時有效

**參數**：

- `value` (必要)：要驗證為 JSON 的字串。

**回傳類型**：`BOOLEAN`

#### 範例

```sql
source=people
| eval is_valid_json = json_valid('[1,2,3,4]'), is_invalid_json = json_valid('{invalid}')
| fields is_valid_json, is_invalid_json
| head 1
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| is_valid_json | is_invalid_json |
| --- | --- |
| True | False |

<!-- vale on -->

## JSON_OBJECT

**用法**：`JSON_OBJECT(key1, value1, key2, value2, ...)`

從指定的鍵值對建立 JSON 物件字串。所有鍵都必須是字串。

**參數**：

- `key1`, `value1` (必要)：第一個鍵值對。鍵必須是字串。
- `key2`, `value2`, `...` (選用)：其他鍵值對。

**回傳類型**：`STRING`

#### 範例

```sql
source=json_test
| eval test_json = json_object('key', 123.45)
| head 1
| fields test_json
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| test_json |
| --- |
| {"key":123.45} |

<!-- vale on -->

## JSON_ARRAY

**用法**：`JSON_ARRAY(element1, element2, ...)`

從指定的元素建立 JSON 陣列字串。

**參數**：

- `element1`, `element2`, `...` (選用)：要包含在陣列中的元素。可以是任何資料類型。

**回傳類型**：`STRING`

#### 範例

```sql
source=json_test
| eval test_json_array = json_array('key', 123.45)
| head 1
| fields test_json_array
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| test_json_array |
| --- |
| ["key",123.45] |

<!-- vale on -->

## JSON_ARRAY_LENGTH

**用法**：`JSON_ARRAY_LENGTH(value)`

傳回 JSON 陣列中的元素數量。若輸入不是有效的 JSON 陣列、為 `NULL`，或包含無效的 JSON，則傳回 `NULL`。

**參數**：

- `value` (必要)：包含 JSON 陣列的字串。

**回傳類型**：`INTEGER`

#### 範例

下列範例傳回有效 JSON 陣列的長度：

```sql
source=json_test
| eval array_length = json_array_length("[1,2,3]")
| head 1
| fields array_length
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| array_length |
| --- |
| 3 |

<!-- vale on -->

下列範例針對非陣列的 JSON 值傳回 `NULL`：

```sql
source=json_test
| eval array_length = json_array_length("{\"1\": 2}")
| head 1
| fields array_length
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| array_length |
| --- |
| null |

<!-- vale on -->

## JSON_EXTRACT

**用法**：`JSON_EXTRACT(json_string, path1, path2, ...)`

使用指定的 JSON 路徑從 JSON 字串中擷取值。

**行為**：
- **單一路徑**：直接傳回擷取的值。
- **多個路徑**：傳回一個 JSON 陣列，其中依路徑順序包含擷取的值。
- **無效路徑**：結果中該路徑傳回 `NULL`。

有關路徑語法的詳細資訊，請參閱 [JSON path](#json-path) 章節。

**參數**：

- `json_string` (必要)：要從中擷取值的 JSON 字串。
- `path1`, `path2`, `...` (必要)：一或多個 JSON 路徑，指定要擷取哪些值。

**回傳類型**：`STRING`

#### 範例

下列範例使用單一 JSON 路徑擷取值：

```sql
source=json_test
| eval extract = json_extract('{"a": [{"b": 1}, {"b": 2}]}', 'a{}.b')
| head 1
| fields extract
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| extract |
| --- |
| [1,2] |

<!-- vale on -->

下列範例使用多個 JSON 路徑擷取值：

```sql
source=json_test
| eval extract = json_extract('{"a": [{"b": 1}, {"b": 2}]}', 'a{}.b', 'a{}')
| head 1
| fields extract
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| extract |
| --- |
| [[1,2],[{"b":1},{"b":2}]] |

<!-- vale on -->

## JSON_DELETE

**用法**：`JSON_DELETE(json_string, path1, path2, ...)`

從 JSON 字串中指定的 JSON 路徑刪除值。傳回修改後的 JSON 字串。若某個路徑找不到值，則該路徑不會進行任何變更。

**參數**：

- `json_string` (必要)：要從中刪除值的 JSON 字串。
- `path1`, `path2`, `...` (必要)：一或多個 JSON 路徑，指定要刪除哪些值。

**回傳類型**：`STRING`

#### 範例

下列範例使用單一 JSON 路徑刪除值：

```sql
source=json_test
| eval delete = json_delete('{"a": [{"b": 1}, {"b": 2}]}', 'a{0}.b')
| head 1
| fields delete
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| delete |
| --- |
| {"a":[{"b":2}]} |

<!-- vale on -->

下列範例使用多個 JSON 路徑刪除值：

```sql
source=json_test
| eval delete = json_delete('{"a": [{"b": 1}, {"b": 2}]}', 'a{0}.b', 'a{1}.b')
| head 1
| fields delete
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| delete |
| --- |
| {"a":[{},{}]} |

<!-- vale on -->

下列範例顯示嘗試刪除不存在的路徑時不會發生任何變更：

```sql
source=json_test
| eval delete = json_delete('{"a": [{"b": 1}, {"b": 2}]}', 'a{2}.b')
| head 1
| fields delete
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| delete |
| --- |
| {"a":[{"b":1},{"b":2}]} |

<!-- vale on -->

## JSON_SET

**用法**：`JSON_SET(json_string, path1, value1, path2, value2, ...)`

在 JSON 字串中指定的 JSON 路徑設定值。回傳修改後的 JSON 字串。如果某個路徑的父節點不是 JSON 物件，則略過該路徑。

**參數**：

- `json_string` (必要)：要修改的 JSON 字串。
- `path1`、`value1` (必要)：要設定的第一組路徑-值配對。
- `path2`、`value2`、`...` (選用)：其他路徑-值配對。

**回傳類型**：`STRING`

#### 範例

以下範例在 JSON 路徑設定單一值：

```sql
source=json_test
| eval jsonSet = json_set('{"a": [{"b": 1}]}', 'a{0}.b', 3)
| head 1
| fields jsonSet
```
{% include copy.html %}

查詢回傳以下結果：

<!-- vale off -->

| jsonSet |
| --- |
| {"a":[{"b":3}]} |

<!-- vale on -->

以下範例使用多組路徑-值配對設定多個值：

```sql
source=json_test
| eval jsonSet = json_set('{"a": [{"b": 1}, {"b": 2}]}', 'a{0}.b', 3, 'a{1}.b', 4)
| head 1
| fields jsonSet
```
{% include copy.html %}

查詢回傳以下結果：

<!-- vale off -->

| jsonSet |
| --- |
| {"a":[{"b":3},{"b":4}]} |

<!-- vale on -->

## JSON_APPEND

**用法**：`JSON_APPEND(json_string, path1, value1, path2, value2, ...)`

在 JSON 字串中指定的 JSON 路徑將值附加至陣列。回傳修改後的 JSON 字串。如果某個路徑的目標節點不是陣列，則略過該路徑。

**參數**：

- `json_string` (必要)：要修改的 JSON 字串。
- `path1`、`value1` (必要)：要附加的第一組路徑-值配對。
- `path2`、`value2`、`...` (選用)：其他路徑-值配對。

**回傳類型**：`STRING`

#### 範例

以下範例將一個值附加至陣列：

```sql
source=json_test
| eval jsonAppend = json_append('{"a": [{"b": 1}]}', 'a', 3)
| head 1
| fields jsonAppend
```
{% include copy.html %}

查詢回傳以下結果：

<!-- vale off -->

| jsonAppend |
| --- |
| {"a":3} |

<!-- vale on -->

以下範例顯示目標不是陣列的路徑會被略過：

```sql
source=json_test
| eval jsonAppend = json_append('{"a": [{"b": 1}, {"b": 2}]}', 'a{0}.b', 3, 'a{1}.b', 4)
| head 1
| fields jsonAppend
```
{% include copy.html %}

查詢回傳以下結果：

<!-- vale off -->

| jsonAppend |
| --- |
| {"a":[{"b":1},{"b":2}]} |

<!-- vale on -->

以下範例使用混合路徑類型附加值：

```sql
source=json_test
| eval jsonAppend = json_append('{"a": [{"b": 1}]}', 'a', '[1,2]', 'a{1}.b', 4)
| head 1
| fields jsonAppend
```
{% include copy.html %}

查詢回傳以下結果：

<!-- vale off -->

| jsonAppend |
| --- |
| {"a":[{"b":1},"[1,2]"]} |

<!-- vale on -->

## JSON_EXTEND

**用法**：`JSON_EXTEND(json_string, path1, value1, path2, value2, ...)`

在 JSON 字串中指定的 JSON 路徑以新值擴充陣列。回傳修改後的 JSON 字串。如果某個路徑的目標節點不是陣列，則略過該路徑。

此函式會嘗試將每個值剖析為陣列：
- 如果剖析成功：剖析出的陣列元素會加入目標陣列。
- 如果剖析失敗：該值會視為單一元素並加入目標陣列。

**參數**：

- `json_string` (必要)：要修改的 JSON 字串。
- `path1`、`value1` (必要)：要擴充的第一組路徑-值配對。
- `path2`、`value2`、`...` (選用)：其他路徑-值配對。

**回傳類型**：`STRING`

#### 範例

以下範例以單一值擴充陣列：

```sql
source=json_test
| eval jsonExtend = json_extend('{"a": [{"b": 1}]}', 'a', 3)
| head 1
| fields jsonExtend
```
{% include copy.html %}

查詢回傳以下結果：

<!-- vale off -->

| jsonExtend |
| --- |
| {"a":[{"b":1},3]} |

<!-- vale on -->

以下範例顯示目標不是陣列的路徑會被略過：

```sql
source=json_test
| eval jsonExtend = json_extend('{"a": [{"b": 1}, {"b": 2}]}', 'a{0}.b', 3, 'a{1}.b', 4)
| head 1
| fields jsonExtend
```
{% include copy.html %}

查詢回傳以下結果：

<!-- vale off -->

| jsonExtend |
| --- |
| {"a":[{"b":1},{"b":2}]} |

<!-- vale on -->

以下範例將值剖析為陣列來擴充陣列：

```sql
source=json_test
| eval jsonExtend = json_extend('{"a": [{"b": 1}]}', 'a', '[1,2]')
| head 1
| fields jsonExtend
```
{% include copy.html %}

查詢回傳以下結果：

<!-- vale off -->

| jsonExtend |
| --- |
| {"a":[{"b":1},1.0,2.0]} |

<!-- vale on -->

## JSON_KEYS

**用法**：`JSON_KEYS(json_string)`

以 JSON 陣列回傳 JSON 物件的鍵。如果輸入不是有效的 JSON 物件，則回傳 `NULL`。

**參數**：

- `json_string` (必要)：包含 JSON 物件的字串。

**回傳類型**：`STRING`

#### 範例

以下範例從簡單的 JSON 物件取得鍵：

```sql
source=json_test
| eval jsonKeys = json_keys('{"a": 1, "b": 2}')
| head 1
| fields jsonKeys
```
{% include copy.html %}

查詢回傳以下結果：

<!-- vale off -->

| jsonKeys |
| --- |
| ["a","b"] |

<!-- vale on -->

以下範例從巢狀 JSON 物件取得鍵：

```sql
source=json_test
| eval jsonKeys = json_keys('{"a": {"c": 1}, "b": 2}')
| head 1
| fields jsonKeys
```
{% include copy.html %}

查詢回傳以下結果：

<!-- vale off -->

| jsonKeys |
| --- |
| ["a","b"] |

<!-- vale on -->
