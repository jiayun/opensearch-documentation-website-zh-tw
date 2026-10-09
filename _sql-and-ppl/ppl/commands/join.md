---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: join
parent: Commands
grand_parent: PPL
nav_order: 25
---

<!-- vale off -->

# join 命令

<!-- vale on -->

`join` 命令會合併兩個資料集。左側可以是索引或管線命令的結果，而右側可以是索引或子搜尋。

## 語法

`join` 命令支援基本與擴充語法選項。

### 基本語法

```sql
[joinType] join [left = <leftAlias>] [right = <rightAlias>] (on | where) <joinCriteria> <right-dataset>
```

使用別名時，`left` 必須出現在 `right` 之前。
{: .note}

以下是基本 `join` 命令語法的範例：

```sql
source = table1 | inner join left = l right = r on l.a = r.a table2 | fields l.a, r.a, b, c
source = table1 | inner join left = l right = r where l.a = r.a table2 | fields l.a, r.a, b, c
source = table1 | left join left = l right = r on l.a = r.a table2 | fields l.a, r.a, b, c
source = table1 | right join left = l right = r on l.a = r.a table2 | fields l.a, r.a, b, c
source = table1 | full left = l right = r on l.a = r.a table2 | fields l.a, r.a, b, c
source = table1 | cross join left = l right = r on 1=1 table2
source = table1 | left semi join left = l right = r on l.a = r.a table2
source = table1 | left anti join left = l right = r on l.a = r.a table2
source = table1 | join left = l right = r [ source = table2 | where d > 10 | head 5 ]
source = table1 | inner join on table1.a = table2.a table2 | fields table1.a, table2.a, table1.b, table1.c
source = table1 | inner join on a = c table2 | fields a, b, c, d
source = table1 as t1 | join left = l right = r on l.a = r.a table2 as t2 | fields l.a, r.a
source = table1 as t1 | join left = l right = r on l.a = r.a table2 as t2 | fields t1.a, t2.a
source = table1 | join left = l right = r on l.a = r.a [ source = table2 ] as s | fields l.a, s.a
```

#### 基本語法參數

基本 `join` 語法支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<joinCriteria>` | 必要 | 比較運算式，指定如何合併資料集。必須放在查詢中的 `on` 或 `where` 關鍵字之後。 |
| `<right-dataset>` | 必要 | 右側資料集，可以是索引或子搜尋，可含或不含別名。 |
| `joinType` | 選用 | 要執行的 join 類型。有效值為 `left`、`semi`、`anti`，以及效能敏感類型（`right`、`full` 和 `cross`）。預設為 `inner`。 |
| `left` | 選用 | 左側資料集（通常是子搜尋）的別名，用於避免欄位名稱不明確。指定為 `left = <leftAlias>`。 |
| `right` | 選用 | 右側資料集（通常是子搜尋）的別名，用於避免欄位名稱不明確。指定為 `right = <rightAlias>`。 |

### 擴充語法

```sql
join [type=<joinType>] [overwrite=<bool>] [max=n] (<join-field-list> | [left = <leftAlias>] [right = <rightAlias>] (on | where) <joinCriteria>) <right-dataset>
```

以下是擴充 `join` 命令語法的範例：

```sql
source = table1 | join type=outer left = l right = r on l.a = r.a table2 | fields l.a, r.a, b, c
source = table1 | join type=left left = l right = r where l.a = r.a table2 | fields l.a, r.a, b, c
source = table1 | join type=inner max=1 left = l right = r where l.a = r.a table2 | fields l.a, r.a, b, c
source = table1 | join a table2 | fields a, b, c
source = table1 | join a, b table2 | fields a, b, c
source = table1 | join type=outer a b table2 | fields a, b, c
source = table1 | join type=inner max=1 a, b table2 | fields a, b, c
source = table1 | join type=left overwrite=false max=0 a, b [source=table2 | rename d as b] | fields a, b, c
```

#### 擴充語法參數

擴充 `join` 語法支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<joinCriteria>` | 必要 | 比較運算式，指定如何合併資料集。必須放在查詢中的 `on` 或 `where` 關鍵字之後。 |
| `<right-dataset>` | 必要 | 右側資料集，可以是索引或子搜尋，可含或不含別名。 |  
| `type` | 選用 | 使用擴充語法時的 join 類型。有效值為 `left`、`outer`（與 `left` 相同）、`semi`、`anti`，以及效能敏感類型（`right`、`full` 和 `cross`）。預設為 `inner`。 |
| `<join-field-list>` | 選用 | 用於建立 join 準則的欄位清單。這些欄位必須同時存在於兩個資料集中。若未指定，則會使用兩個資料集共有的所有欄位作為 join 鍵。 |
| `overwrite` | 選用 | 僅在指定 `join-field-list` 時適用。指定右側資料集中名稱重複的欄位是否應取代主搜尋結果中的對應欄位。預設為 `true`。 |
| `max` | 選用 | 要與主搜尋中每一列合併的子搜尋結果數上限。當 plugins.ppl.syntax.legacy.preferred 為 `true` 時，預設為 `0`（無限制）。當設定為 `false` 時，預設值為 `1`。 |
| `left` | 選用 | 左側資料集（通常是子搜尋）的別名，用於避免欄位名稱不明確。指定為 `left = <leftAlias>`。 |
| `right` | 選用 | 右側資料集（通常是子搜尋）的別名，用於避免欄位名稱不明確。指定為 `right = <rightAlias>`。 |
  

## 組態

`join` 命令的行為是使用 `plugins.ppl.join.subsearch_maxout` 設定來設定，該設定指定要合併的子搜尋列數上限。預設為 `50000`。值為 `0` 表示無限制。

若要更新設定，請傳送下列請求：
  
```json
PUT /_plugins/_query/settings
{
  "persistent": {
    "plugins.ppl.join.subsearch_maxout": "5000"
  }
}
```
{% include copy-curl.html %}

## 範例 1：合併兩個索引  

下列查詢使用基本 `join` 語法來合併兩個索引：
  
```sql
source = state_country
| inner join left=a right=b ON a.name = b.name occupation
| stats avg(salary) by span(age, 10) as age_span, b.country
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| avg(salary) | age_span | b.country |
| --- | --- | --- |
| 120000.0 | 40 | USA |
| 105000.0 | 20 | Canada |
| 0.0 | 40 | Canada |
| 70000.0 | 30 | USA |
| 100000.0 | 70 | England |

<!-- vale on -->
  

## 範例 2：與子搜尋合併  

下列查詢使用基本 `join` 語法將資料集與子搜尋合併：
  
```sql
source = state_country as a
| where country = 'USA' OR country = 'England'
| left join ON a.name = b.name [ source = occupation
| where salary > 0
| fields name, country, salary
| sort salary
| head 3 ] as b
| stats avg(salary) by span(age, 10) as age_span, b.country
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| avg(salary) | age_span | b.country |
| --- | --- | --- |
| null | 40 | null |
| 70000.0 | 30 | USA |
| 100000.0 | 70 | England |

<!-- vale on -->
  

## 範例 3：使用欄位清單合併  

下列查詢使用擴充語法，並為 join 準則指定欄位清單：
  
```sql
source = state_country
| where country = 'USA' OR country = 'England'
| join type=left overwrite=true name [ source = occupation
| where salary > 0
| fields name, country, salary
| sort salary
| head 3 ]
| stats avg(salary) by span(age, 10) as age_span, country
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| avg(salary) | age_span | country |
| --- | --- | --- |
| null | 40 | null |
| 70000.0 | 30 | USA |
| 100000.0 | 70 | England |

<!-- vale on -->
  

## 範例 4：使用其他選項合併  

下列查詢使用擴充語法與選用參數，以進一步控制 join 作業：
  
```sql
source = state_country
| join type=inner overwrite=false max=1 name occupation
| stats avg(salary) by span(age, 10) as age_span, country
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| avg(salary) | age_span | country |
| --- | --- | --- |
| 120000.0 | 40 | USA |
| 100000.0 | 70 | USA |
| 105000.0 | 20 | Canada |
| 70000.0 | 30 | USA |

<!-- vale on -->
  

## 限制

`join` 命令有下列限制：

* **基本語法中的欄位名稱不明確** – 當左側與右側資料集的欄位名稱相同時，輸出中的欄位名稱會不明確。為了解決此問題，衝突的欄位會重新命名為 `<alias>.id`（若未指定別名則為 `<tableName>.id`）。

  下表示範當 `table1` 與 `table2` 都包含名為 `id` 的欄位時，如何解決欄位名稱衝突。

  | 查詢 | 輸出 |
  | --- | --- |
  | `source=table1 \| join left=t1 right=t2 on t1.id=t2.id table2 \| eval a = 1` | `t1.id, t2.id, a` |
  | `source=table1 \| join on table1.id=table2.id table2 \| eval a = 1` | `table1.id, table2.id, a` |
  | `source=table1 \| join on table1.id=t2.id table2 as t2 \| eval a = 1` | `table1.id, t2.id, a` |
  | `source=table1 \| join right=tt on table1.id=t2.id [ source=table2 as t2 \| eval b = id ] \| eval a = 1` | `table1.id, tt.id, tt.b, a` |

* **擴充語法中的欄位去重** – 使用擴充語法搭配欄位清單時，輸出中重複的欄位名稱會根據 `overwrite` 選項進行去重。

* **join 類型可用性** – join 類型 `inner`、`left`、`outer`（`left` 的別名）、`semi` 和 `anti` 預設為啟用。效能敏感的 join 類型 `right`、`full` 和 `cross` 預設為停用。若要啟用這些類型，請將 `plugins.calcite.all_join_types.allowed` 設定為 `true`。
