---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: lookup
parent: Commands
grand_parent: PPL
nav_order: 27
---

<!-- vale off -->

# lookup 命令

<!-- vale on -->

`lookup` 命令會使用第二個索引（稱為 _lookup 索引_ 或 _維度表_）中的欄位來擴充搜尋結果。對於搜尋結果中的每一列，`lookup` 命令會在 lookup 索引中尋找相符的列，並將該列的欄位複製到結果中。

`lookup` 命令的運作方式類似左聯結：搜尋結果中的每一列都會保留，並新增或覆寫來自 lookup 索引的相符欄位。如果某一列沒有相符項目，`replace` 會將複製的欄位設為 `null`，而 `append` 會保留任何現有的值。與 `join` 命令相比，`lookup` 更簡單，也更適合將靜態參考資料（例如地區名稱、使用者部門或產品類別）新增至搜尋結果。

## 語法

`lookup` 命令具有下列語法：

```sql
lookup <lookupIndex> (<lookupMappingField> [as <sourceMappingField>])... [(replace | append | output) (<inputField> [as <outputField>])...]
```

下表說明範例 `lookup` 命令。

| 命令 | 說明 |
| --- | --- |
| `source = table1 | lookup table2 id` | 將 `table2.id` 與 `table1.id` 進行比對，並從 `table2` 複製所有其他欄位。 |
| `source = table1 | lookup table2 id, name` | 同時依 `id` 和 `name` 進行比對。 |
| `source = table1 | lookup table2 id as cid` | 將 `table2.id` 與 `table1.cid` 進行比對。 |
| `source = table1 | lookup table2 id as cid replace dept as department` | 將 `table2.id` 與 `table1.cid` 進行比對，並將 `table2.dept` 複製到 `department` 欄位，覆寫現有的值。 |
| `source = table1 | lookup table2 id as cid append dept as department` | 將 `table2.id` 與 `table1.cid` 進行比對，並僅在 `department` 為 `null` 或缺少時，將 `table2.dept` 複製到 `department` 欄位。 |

## 參數

`lookup` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<lookupIndex>` | 必要 | 要從中複製欄位的 lookup 索引（維度表）。 |
| `<lookupMappingField>` | 必要 | lookup 索引中用於比對的欄位。如果您未指定 `<sourceMappingField>`，搜尋結果必須包含名稱相同的欄位。請以逗號分隔的清單指定多個欄位。只有當所有欄位都相等時，某一列才會相符。請參閱[依欄位比對列](#matching-rows-by-field)。 |
| `<sourceMappingField>` | 選用 | 搜尋結果中與 `<lookupMappingField>` 進行比對的欄位。預設為 `<lookupMappingField>` 名稱。請參閱[依欄位比對列](#matching-rows-by-field)。 |
| `<inputField>` | 選用 | lookup 索引中其相符值會複製到搜尋結果的欄位。請以逗號分隔的清單指定多個欄位。如果未指定，則會複製 lookup 索引中除了比對欄位以外的所有欄位。請參閱[選取要複製的欄位](#selecting-fields-to-copy)。 |
| `<outputField>` | 選用 | 搜尋結果中要放置複製值的欄位名稱。預設為 `<inputField>` 名稱。如果該欄位不存在，則會新增至搜尋結果。請參閱[選取要複製的欄位](#selecting-fields-to-copy)。 |
| `(replace | append | output)` | 選用 | 指定複製值的套用方式。`replace` 會覆寫現有的值。`append` 只會設定為 `null` 或缺少的值。`output` 是 `replace` 的同義詞。預設為 `replace`。請參閱[處理現有欄位](#handling-existing-fields)。 |

## 依欄位比對列

`<lookupMappingField>` 和 `<sourceMappingField>` 參數使用 `<lookupMappingField> AS <sourceMappingField>` 格式。`AS` 左側的欄位位於 lookup 索引中，而 `AS` 右側的欄位位於搜尋結果中。

例如，`lookup work_information uid AS id` 會比對搜尋結果中其 `id` 等於 `work_information` 中某一列的 `uid` 的每一列。如果兩個索引使用相同的欄位名稱，請省略 `AS`。例如，`lookup work_information id` 會將搜尋結果中的 `id` 與 lookup 索引中的 `id` 進行比對。

若要依多個欄位進行比對，請以逗號分隔的清單指定它們。只有當所有欄位都相等時，某一列才會相符。您可以在同一個清單中合併重新命名和同名的欄位。例如，當 `uid` 等於 `id` 且 `name` 值相等時，`lookup work_information uid AS id, name` 會相符。

## 選取要複製的欄位

`<inputField>` 和 `<outputField>` 參數接在比對欄位之後，並使用 `<inputField> AS <outputField>` 格式。`AS` 左側的欄位位於 lookup 索引中，並提供值。`AS` 右側的欄位是搜尋結果中的欄位名稱。例如，`replace department AS dept` 會將 lookup 索引中的 `department` 複製到搜尋結果中名為 `dept` 的欄位。

如果您省略 `AS`，該欄位會保留其在 lookup 索引中的名稱。如果您省略 `<inputField>`，`lookup` 會複製 lookup 索引中除了比對欄位以外的所有欄位。

## 處理現有欄位

`replace`、`append` 和 `output` 關鍵字會指定取代策略，這會決定當輸出欄位已存在於結果列時，複製值要如何套用。下表比較 `replace` 和 `append` 策略。

| 關鍵字 | 如果輸出欄位有值 | 如果輸出欄位為 `null` 或缺少 |
| --- | --- | --- |
| `replace` (預設) | 以 lookup 索引中的值覆寫該值。如果該列沒有相符項目，則會以 `null` 覆寫該值。 | 設定 lookup 索引中的值。 |
| `append` | 保留現有的值。 | 設定 lookup 索引中的值。 |

如果輸出欄位不存在於搜尋結果中，這兩種策略都會新增它。`output` 關鍵字是 `replace` 的同義詞。

## 範例

下列範例使用 `work_information` lookup 索引來擴充 `worker` 索引。

`worker` 索引包含下列文件。

<!-- vale off -->

| id | name | occupation | country | salary |
| --- | --- | --- | --- | --- |
| 1000 | Jake | Engineer | England | 100000 |
| 1001 | Hello | Artist | USA | 70000 |
| 1002 | John | Doctor | Canada | 120000 |
| 1003 | David | Doctor | null | 120000 |
| 1004 | David | null | Canada | 0 |
| 1005 | Jane | Scientist | Canada | 90000 |

<!-- vale on -->

`work_information` 索引包含下列文件。其鍵欄位為 `uid`，且不包含工作者 `1001` 和 `1004` 的資料列。

<!-- vale off -->

| uid | name | department | occupation |
| --- | --- | --- | --- |
| 1000 | Jake | IT | Engineer |
| 1002 | John | DATA | Scientist |
| 1003 | David | HR | Doctor |
| 1005 | Jane | DATA | Engineer |
| 1006 | Tom | SALES | Artist |

<!-- vale on -->

### 範例 1：使用不同名稱的比對欄位複製單一欄位

下列查詢會比對每個其 `id` 等於 `work_information` 中某個 `uid` 的工作者，並將 `department` 複製到結果中。因為 `worker` 不包含 `department` 欄位，`replace` 會新增它。沒有相符項目的資料列會包含 `null`：

```sql
source = worker
  | lookup work_information uid AS id REPLACE department
  | fields id, name, occupation, country, salary, department
  | sort id
```
{% include copy.html %}

該查詢會傳回下列結果：

<!-- vale off -->

| id | name | occupation | country | salary | department |
| --- | --- | --- | --- | --- | --- |
| 1000 | Jake | Engineer | England | 100000 | IT |
| 1001 | Hello | Artist | USA | 70000 | null |
| 1002 | John | Doctor | Canada | 120000 | DATA |
| 1003 | David | Doctor | null | 120000 | HR |
| 1004 | David | null | Canada | 0 | null |
| 1005 | Jane | Scientist | Canada | 90000 | DATA |

<!-- vale on -->

### 範例 2：比較現有欄位的 replace 與 append

只有當輸出欄位已經包含值時，`replace` 與 `append` 策略才會產生不同的結果。下列查詢將 lookup 索引中的 `department` 複製到既有的 `country` 欄位。

使用 `replace` 時，lookup 值會覆寫每個相符列中的 `country`。在沒有相符項目的列中，`country` 會被覆寫為 `null`：

```sql
source = worker
  | lookup work_information uid AS id REPLACE department AS country
  | fields id, name, occupation, salary, country
  | sort id
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| id | name | occupation | salary | country |
| --- | --- | --- | --- | --- |
| 1000 | Jake | Engineer | 100000 | IT |
| 1001 | Hello | Artist | 70000 | null |
| 1002 | John | Doctor | 120000 | DATA |
| 1003 | David | Doctor | 120000 | HR |
| 1004 | David | null | 0 | null |
| 1005 | Jane | Scientist | 90000 | DATA |

<!-- vale on -->

使用 `append` 時，既有的 `country` 值會保留，只有在 `country` 為 `null` 的列中才會設定 lookup 值：

```sql
source = worker
  | lookup work_information uid AS id APPEND department AS country
  | fields id, name, occupation, salary, country
  | sort id
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| id | name | occupation | salary | country |
| --- | --- | --- | --- | --- |
| 1000 | Jake | Engineer | 100000 | England |
| 1001 | Hello | Artist | 70000 | USA |
| 1002 | John | Doctor | 120000 | Canada |
| 1003 | David | Doctor | 120000 | HR |
| 1004 | David | null | 0 | Canada |
| 1005 | Jane | Scientist | 90000 | Canada |

<!-- vale on -->

只有工作者 `1003` 的列發生變化：其 `country` 原本為 `null`，因此 `append` 將其設定為 `HR`。

### 範例 3：複製所有欄位

若省略 `<inputField>`，`lookup` 會複製 lookup 索引中除比對欄位以外的所有欄位。下列查詢同時以 `uid AS id` 與 `name` 進行比對，因此 `department` 與 `occupation` 都會被複製：

```sql
source = worker
  | lookup work_information uid AS id, name
  | fields id, name, occupation, country, salary, department
  | sort id
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| id | name | occupation | country | salary | department |
| --- | --- | --- | --- | --- | --- |
| 1000 | Jake | Engineer | England | 100000 | IT |
| 1001 | Hello | null | USA | 70000 | null |
| 1002 | John | Scientist | Canada | 120000 | DATA |
| 1003 | David | Doctor | null | 120000 | HR |
| 1004 | David | null | Canada | 0 | null |
| 1005 | Jane | Engineer | Canada | 90000 | DATA |

<!-- vale on -->

因為 `worker` 已包含 `occupation` 欄位，且預設策略為 `replace`，所以 lookup 索引中的 `occupation` 值會覆寫它。例如，工作者 `1002` 的 `Doctor` 變成 `Scientist`，工作者 `1001` 的 `Artist` 變成 `null`。

### 範例 4：將欄位複製到新欄位

若輸出欄位不存在於搜尋結果中，`lookup` 會新增該欄位，並保持既有欄位不變。下列查詢以 `name` 進行比對，並將 lookup 索引中的 `occupation` 複製到新的 `new_col` 欄位：

```sql
source = worker
  | lookup work_information name REPLACE occupation AS new_col
  | fields id, name, occupation, country, salary, new_col
  | sort id
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| id | name | occupation | country | salary | new_col |
| --- | --- | --- | --- | --- | --- |
| 1000 | Jake | Engineer | England | 100000 | Engineer |
| 1001 | Hello | Artist | USA | 70000 | null |
| 1002 | John | Doctor | Canada | 120000 | Scientist |
| 1003 | David | Doctor | null | 120000 | Doctor |
| 1004 | David | null | Canada | 0 | Doctor |
| 1005 | Jane | Scientist | Canada | 90000 | Engineer |

<!-- vale on -->

David 的兩列（`1003` 與 `1004`）在 `new_col` 中都包含 `Doctor`，因為兩者透過 `name` 與同一個 lookup 列相符。

### 範例 5：使用 output 關鍵字

`output` 關鍵字是 `replace` 的同義詞。下列查詢會傳回與範例 1 相同的結果：

```sql
source = worker
  | lookup work_information uid AS id OUTPUT department
  | fields id, name, occupation, country, salary, department
  | sort id
```
{% include copy.html %}
