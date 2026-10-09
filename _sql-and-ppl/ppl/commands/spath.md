---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: spath
parent: Commands
grand_parent: PPL
nav_order: 44
---

<!-- vale off -->

# spath 命令

<!-- vale on -->

`spath` 命令可從結構化的 JSON 資料中擷取欄位。它有兩種運作模式：

- **路徑模式**：當指定 `path` 時，會擷取指定 JSON 路徑上的單一值。
- **自動擷取模式** (實驗性)：當省略 `path` 時，會將 JSON 中的所有欄位擷取成一個 map。

`spath` 命令不會在 OpenSearch 資料節點上執行。它是在資料回傳至協調節點之後才擷取欄位，因此在大型資料集上速度較慢。建議直接為篩選所需的欄位編製索引，而不要使用 `spath` 來篩選巢狀欄位。
{: .note}

## 語法

`spath` 命令的語法如下：

```sql
spath input=<field> [output=<field>] [[path=]<path>]
```

## 參數

`spath` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `input` | 必要 | 包含要剖析之 JSON 資料的欄位。 |
| `output` | 選用 | 儲存擷取資料的目標欄位。預設值在路徑模式下為 `path` 的值，在自動擷取模式下為 `input` 的值。 |
| `path` | 選用 | 識別要擷取資料的 JSON 路徑。省略時，所有欄位都會擷取成一個 map (自動擷取模式)。 |  

如需路徑語法的詳細資訊，請參閱 [json_extract]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/functions/json#json_extract)。

## 自動擷取模式 (實驗性)

當省略 `path` 時，`spath` 命令會以自動擷取模式執行。它不會擷取單一值，而是依照下列規則將整個 JSON 攤平成 `map<string, string>` 欄：

- 巢狀物件使用點號鍵：`user.name`、`user.age`
- 陣列使用 `{}` 後綴：`tags{}`、`users{}.name`
- 重複的邏輯鍵會合併成陣列：`c{}.b = [2, 3]`
- Null 值會保留：JSON 中的 `null` 會變成 map 中的字串 `"null"`
- 所有值都會字串化：數值與布林值會轉換為其字串表示 (例如 `30` 變成 `"30"`、`true` 變成 `"true"`，而陣列變成 `"[a, b, c]"`)

自動擷取模式會處理整個輸入欄位，沒有字元數限制。對於大型 JSON 負載，建議使用路徑擷取來針對特定欄位。
{: .note}
>
> 無效或格式錯誤的 JSON 會回傳部分結果，其中包含在錯誤發生前成功剖析的所有欄位。空的 JSON 物件 (`{}`) 會回傳空的 map。

## 範例 1：擷取基本欄位

`spath` 的基本用法是從 JSON 資料中擷取單一欄位。下列查詢會從 `doc_n` 欄位中的 JSON 物件擷取 `n` 欄位：
  
```sql
source=structured
| spath input=doc_n n
| fields doc_n n
```
{% include copy.html %}
  
查詢回傳下列結果：
  
<!-- vale off -->

| doc_n | n |
| --- | --- |
| {"n": 1} | 1 |
| {"n": 2} | 2 |
| {"n": 3} | 3 |

<!-- vale on -->
  

## 範例 2：清單與巢狀結構  

下列查詢示範如何走訪巢狀欄位並擷取清單元素：
  
```sql
source=structured
| spath input=doc_list output=first_element list{0}
| spath input=doc_list output=all_elements list{}
| spath input=doc_list output=nested nest_out.nest_in
| fields doc_list first_element all_elements nested
```
{% include copy.html %}
  
查詢回傳下列結果：
  
<!-- vale off -->

| doc_list | first_element | all_elements | nested |
| --- | --- | --- | --- |
| {"list": [1, 2, 3, 4], "nest_out": {"nest_in": "a"}} | 1 | [1,2,3,4] | a |
| {"list": [], "nest_out": {"nest_in": "a"}} | null | [] | a |
| {"list": [5, 6], "nest_out": {"nest_in": "a"}} | 5 | [5,6] | a |

<!-- vale on -->
  

## 範例 3：加總內部元素  

下列查詢示範如何使用 `spath` 從 JSON 資料中擷取 `n` 欄位，並計算所有擷取值的總和： 
  
```sql
source=structured
| spath input=doc_n n
| eval n=cast(n as int)
| stats sum(n)
| fields `sum(n)`
```
{% include copy.html %}
  
查詢回傳下列結果。`spath` 命令一律以字串回傳內部值：
  
<!-- vale off -->

| sum(n) |
| --- |
| 6 |

<!-- vale on -->
  

## 範例 4：使用逸出路徑  

使用引號字串語法來存取包含空格、點號或其他特殊字元的 JSON 欄位名稱：
  
```sql
source=structured
| spath output=a input=doc_escape "['a fancy field name']"
| spath output=b input=doc_escape "['a.b.c']"
| fields a b
```
{% include copy.html %}
  
查詢回傳下列結果：
  
<!-- vale off -->

| a | b |
| --- | --- |
| true | 0 |
| true | 1 |
| false | 2 |

<!-- vale on -->
  

## 範例 5：使用自動擷取模式  

當省略 `path` 時，`spath` 會將 JSON 中的所有欄位擷取成一個 map。您可以使用點號路徑導覽來存取個別值，其中 `doc.user.name` 會解析為 map 鍵 `user.name`。對於包含 `{}` 等特殊字元的鍵，請使用反引號括住：
  
```sql
source=structured
| spath input=doc_auto output=doc
| fields doc_auto, doc.user.name, doc.user.age, doc.`tags{}`, doc.active
```
{% include copy.html %}
  
查詢回傳下列結果：
  
<!-- vale off -->

| doc_auto | doc.user.name | doc.user.age | doc.tags{} | doc.active |
| --- | --- | --- | --- | --- |
| {"user":{"name":"John","age":30},"tags":["java","sql"],"active":true} | John | 30 | [java, sql] | true |
| {"user":{"name":"Jane","age":25},"tags":["python"],"active":null} | Jane | 25 | python | null |
| {"user":{"name":"Bob","age":35},"tags":["go","rust","sql"],"user.name":"Bobby"} | [Bob, Bobby] | 35 | [go, rust, sql] | null |

<!-- vale on -->
  
此範例示範的攤平規則：

- 巢狀物件使用點號鍵：`user.name` 與 `user.age` 是從 `{"user": {"name": "John", "age": 30}}` 擷取
- 陣列使用 `{}` 後綴：`tags{}` 是從 `{"tags": ["java", "sql"]}` 擷取
- 重複的邏輯鍵會合併成陣列：在第三列中，`"user": {"name": "Bob"}` (巢狀) 與 `"user.name": "Bobby"` (直接點號鍵) 都解析為同一個鍵 `user.name`，因此它們的值合併成 `'[Bob, Bobby]'`
- 所有值都是字串：數值 `30` 變成 `'30'`、布林值 `true` 變成 `'true'`，而陣列變成 `'[java, sql]'` 之類的字串
- Null 值會保留：在第二列中，`"active": null` 在 map 中保留為 `'active': 'null'`
