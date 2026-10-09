---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: mvexpand
parent: Commands
grand_parent: PPL
nav_order: 31
---

<!-- vale off -->

# mvexpand 命令

<!-- vale on -->

`mvexpand` 命令會將多值（陣列）欄位中的每個值展開為個別的資料列。對於每份文件，指定陣列欄位中的每個元素都會各自以一個資料列傳回。

## 語法

`mvexpand` 命令的語法如下：

```sql
mvexpand <field> [limit=<int>]
```

## 參數

`mvexpand` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<field>` | 必要 | 要展開的多值（陣列）欄位。 |
| `limit` | 選用 | 每份文件要展開的值數量上限。若未指定，則會展開所有陣列元素。 |

## 範例 1：使用基本展開

下列查詢會建立一個陣列，並將其展開為個別的資料列：

```sql
source=people
| eval tags = array('error', 'warning', 'info')
| fields tags
| head 1
| mvexpand tags
| fields tags
```
{% include copy.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| tags |
| --- |
| error |
| warning |
| info |

<!-- vale on -->

## 範例 2：限制展開的資料列數量

下列查詢會展開陣列，同時限制展開的資料列數量：

```sql
source=people
| eval ids = array(1, 2, 3, 4, 5)
| fields ids
| head 1
| mvexpand ids limit=3
| fields ids
```
{% include copy.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| ids |
| --- |
| 1 |
| 2 |
| 3 |

<!-- vale on -->

## 範例 3：展開巢狀欄位

下列查詢會將多值 `projects` 欄位展開為每個專案一個資料列：

```sql
source=people
| head 1
| fields projects
| mvexpand projects
| fields projects.name
```
{% include copy.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| projects.name |
| --- |
| AWS Redshift Spectrum querying |
| AWS Redshift security |
| AWS Aurora security |

<!-- vale on -->

## 範例 4：單值陣列

只有單一元素的陣列會展開為一個資料列：

```sql
source=people
| eval tags = array('error')
| fields tags
| head 1
| mvexpand tags
| fields tags
```
{% include copy.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| tags |
| --- |
| error |

<!-- vale on -->

## 範例 5：缺少的欄位

下列查詢嘗試展開輸入結構描述中不存在的欄位：

```sql
source=people
| eval some_field = 'x'
| fields some_field
| head 1
| mvexpand tags
| fields tags
```
{% include copy.html %}

此查詢會擲回下列語意檢查例外狀況：

```text
{'reason': 'Invalid Query', 'details': "Field 'tags' not found in the schema", 'type': 'SemanticCheckException'}
```

## 相關命令

- [`nomv`]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/nomv/) -- 將多值欄位轉換為單值字串
- [`mvcombine`]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/mvcombine/) -- 將多個資料列合併為一個含有多值欄位的資料列
