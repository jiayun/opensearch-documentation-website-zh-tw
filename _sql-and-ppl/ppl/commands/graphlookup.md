---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: graphLookup
parent: Commands
grand_parent: PPL
nav_order: 21
---

<!-- vale off -->

# graphLookup 命令

<!-- vale on -->

這是一項實驗性功能，不建議在正式環境中使用。若要了解此功能的進度或提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/) 的討論。
{: .warning}

`graphLookup` 命令使用廣度優先搜尋 (BFS) 演算法對集合執行遞迴圖形走訪。它會找出符合起始值的文件，並根據指定的欄位遞迴走訪文件之間的關聯。這對於組織架構圖、社交網路或路由圖等階層式資料非常有用。

`graphLookup` 命令執行廣度優先搜尋 (BFS) 走訪：

1. 對每個來源文件，擷取 `start` 的值
2. 查詢 lookup 索引，找出 `toField` 符合起始值的文件
3. 將符合的文件加入結果陣列
4. 從符合的文件中擷取 `fromField` 值以繼續走訪
5. 重複步驟 2--4，直到找不到新文件或達到 `maxDepth` 為止

對於雙向走訪 (`<->`)，演算法還會透過額外比對 `fromField` 值，沿反方向追蹤邊。

## 語法

`graphLookup` 命令的語法如下：

```sql
graphLookup <lookupIndex> start=<startField> edge=<fromField><operator><toField> [maxDepth=<maxDepth>] [depthField=<depthField>] [supportArray=(true | false)] [batchMode=(true | false)] [usePIT=(true | false)] [filter=(<condition>)] as <outputField>
```

以下是 `graphLookup` 命令語法的範例：

```sql
source = employees | graphLookup employees start=reportsTo edge=reportsTo-->name as reportingHierarchy
source = employees | graphLookup employees start=reportsTo edge=reportsTo-->name maxDepth=2 as reportingHierarchy
source = employees | graphLookup employees start=reportsTo edge=reportsTo-->name depthField=level as reportingHierarchy
source = employees | graphLookup employees start=reportsTo edge=reportsTo<->name as connections
source = travelers | graphLookup airports start=nearestAirport edge=connects-->airport supportArray=true as reachableAirports
source = airports | graphLookup airports start=airport edge=connects-->airport supportArray=true as reachableAirports
source = employees | graphLookup employees start=reportsTo edge=reportsTo-->name filter=(status = 'active' AND age > 18) as reportingHierarchy
```

## 參數


`graphLookup` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
|---|---|---|
| `<lookupIndex>` | 必要 | 要執行圖形走訪的索引名稱。對於自我參照的圖形，可以與來源索引相同。 |
| `start=<startField>` | 必要 | 來源文件中用於啟動遞迴搜尋的欄位。該值會與 lookup 索引中的 `toField` 進行比對。支援單一值與陣列。 |
| `edge=<fromField><operator><toField>` | 必要 | 定義節點之間的走訪路徑，指定文件如何連接以及走訪方向。請參閱[邊參數](#edge-parameters)。 |
| `maxDepth=<maxDepth>` | 選用 | 最大遞迴深度 (跳躍次數)。預設為 `0`。值為 `0` 時僅傳回直接連接；較高的值會相應擴大走訪範圍。 |
| `depthField=<depthField>` | 選用 | 加入每個結果文件中以表示遞迴深度的欄位名稱。若省略，則不會加入深度資訊。第一層的深度從 `0` 開始。 |
| `supportArray=(true \| false)` | 選用 | 當為 `true` 時，停用將已造訪節點篩選條件提前下推至 OpenSearch。預設為 `false`。當 `fromField` 或 `toField` 包含陣列值時，請啟用此選項以確保正確的走訪行為。請參閱[陣列欄位](#array-fields)。 |
| `batchMode=(true \| false)` | 選用 | 當為 `true` 時，會收集所有起始值並執行單一統一的 BFS 走訪。預設為 `false`。輸出會變成兩個陣列：`[Array<sourceRows>, Array<lookupResults>]`。請參閱[批次模式](#batch-mode)。 |
| `usePIT=(true \| false)` | 選用 | 當為 `true` 時，會為 lookup 索引啟用 Point in Time (PIT) 搜尋，允許超出 `max_result_window` 限制的完整分頁走訪。預設為 `false`。請參閱[PIT 搜尋](#pit-search)。 |
| `filter=(<condition>)` | 選用 | 限制哪些 lookup 索引文件參與走訪的篩選條件。BFS 期間僅考慮符合條件的文件。必須使用括號。範例：`filter=(status = 'active' AND age > 18)`。 |
| `as <outputField>` | 必要 | 儲存走訪期間發現之所有文件的輸出欄位名稱。 |

### 邊參數


`edge` 參數使用語法 `edge=<fromField><operator><toField>`，由下列元件組成。

| 元件 | 說明 |
|---|---|
| `fromField` | lookup 索引文件中用作走訪來源的欄位。文件被比對成功後，此欄位的值會用來尋找下一組連接的文件。支援單一值與陣列。 |
| `toField` | lookup 索引文件中用於比對的欄位。`toField` 等於目前走訪值的文件會包含在結果中。 |
| `operator` | 指定走訪方向：<br>- `-->` 僅執行從 `fromField` 到 `toField` 的**單向**走訪 (例如，`edge=reportsTo-->name` 僅以單一方向從 `reportsTo` 走訪到 `name`)。<br>- `<->` 在 `fromField` 與 `toField` 之間執行**雙向**走訪 (例如，`edge=reportsTo<->name` 在 `reportsTo` 與 `name` 之間以雙向走訪)。 |

## 範例 1：走訪員工階層

假設有一個包含下列文件的 `employees` 索引。

<!-- vale off -->

| id | name | reportsTo |
|----|------|-----------|
| 1 | Dev | Eliot |
| 2 | Eliot | Ron |
| 3 | Ron | Andrew |
| 4 | Andrew | null |
| 5 | Asya | Ron |
| 6 | Dan | Andrew |
<!-- vale on -->

下列查詢會找出每位員工的回報鏈：

```sql
source = employees
  | graphLookup employees
    start=reportsTo
    edge=reportsTo-->name
    as reportingHierarchy
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| name | reportsTo | id | reportingHierarchy |
| --- | --- | --- | --- |
| Dev | Eliot | 1 | [{name:Eliot, reportsTo:Ron, id:2}] |
| Eliot | Ron | 2 | [{name:Ron, reportsTo:Andrew, id:3}] |
| Ron | Andrew | 3 | [{name:Andrew, reportsTo:null, id:4}] |
| Andrew | null | 4 | [] |
| Asya | Ron | 5 | [{name:Ron, reportsTo:Andrew, id:3}] |
| Dan | Andrew | 6 | [{name:Andrew, reportsTo:null, id:4}] |

<!-- vale on -->

`reportingHierarchy` 陣列中的每個元素都是一個 `struct`，包含來自 lookup 索引的具名欄位。對於名為 `Dev` 的員工，走訪從 `reportsTo="Eliot"` 開始，找出 `Eliot` 的記錄，並將其包含在 `reportingHierarchy` 陣列中。

## 範例 2：加入深度追蹤

下列查詢加入一個名為 `level` 的 `depthField`，以追蹤每位主管與員工之間的層級數：

```sql
source = employees
  | graphLookup employees
    start=reportsTo
    edge=reportsTo-->name
    depthField=level
    as reportingHierarchy
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| name | reportsTo | id | reportingHierarchy |
| --- | --- | --- | --- |
| Dev | Eliot | 1 | [{name:Eliot, reportsTo:Ron, id:2, level:0}] |
| Eliot | Ron | 2 | [{name:Ron, reportsTo:Andrew, id:3, level:0}] |
| Ron | Andrew | 3 | [{name:Andrew, reportsTo:null, id:4, level:0}] |
| Andrew | null | 4 | [] |
| Asya | Ron | 5 | [{name:Ron, reportsTo:Andrew, id:3, level:0}] |
| Dan | Andrew | 6 | [{name:Andrew, reportsTo:null, id:4, level:0}] |

<!-- vale on -->

`level` 欄位會加入結果陣列中的每個 struct。值為 `0` 表示第一層比對結果。


## 範例 3：限制走訪深度

下列查詢使用 `maxDepth=1` 將走訪限制為兩層（深度 `0` 與 `1`）：

```sql
source = employees
  | graphLookup employees
    start=reportsTo
    edge=reportsTo-->name
    maxDepth=1
    as reportingHierarchy
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| name | reportsTo | id | reportingHierarchy |
| --- | --- | --- | --- |
| Dev | Eliot | 1 | [{name:Eliot, reportsTo:Ron, id:2}, {name:Ron, reportsTo:Andrew, id:3}] |
| Eliot | Ron | 2 | [{name:Ron, reportsTo:Andrew, id:3}, {name:Andrew, reportsTo:null, id:4}] |
| Ron | Andrew | 3 | [{name:Andrew, reportsTo:null, id:4}] |
| Andrew | null | 4 | [] |
| Asya | Ron | 5 | [{name:Ron, reportsTo:Andrew, id:3}, {name:Andrew, reportsTo:null, id:4}] |
| Dan | Andrew | 6 | [{name:Andrew, reportsTo:null, id:4}] |

<!-- vale on -->

## 範例 4：尋找可到達的機場

假設有一個 `airports` 索引包含下列文件。

<!-- vale off -->

| airport | connects |
|---------|----------|
| JFK | [BOS, ORD] |
| BOS | [JFK, PWM] |
| ORD | [JFK] |
| PWM | [BOS, LHR] |
| LHR | [PWM] |
<!-- vale on -->

下列查詢會找出可從每個機場到達的所有機場：

```sql
source = airports
  | graphLookup airports
    start=airport
    edge=connects-->airport
    as reachableAirports
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| airport | connects | reachableAirports |
| --- | --- | --- |
| JFK | [BOS, ORD] | [{airport:JFK, connects:[BOS, ORD]}] |
| BOS | [JFK, PWM] | [{airport:BOS, connects:[JFK, PWM]}] |
| ORD | [JFK] | [{airport:ORD, connects:[JFK]}] |
| PWM | [BOS, LHR] | [{airport:PWM, connects:[BOS, LHR]}] |
| LHR | [PWM] | [{airport:LHR, connects:[PWM]}] |

<!-- vale on -->

## 範例 5：使用不同的來源與 lookup 索引

`graphLookup` 命令可以使用不同的來源與 lookup 索引。

假設有一個 `travelers` 索引包含下列文件。

<!-- vale off -->

| name | nearestAirport |
|------|----------------|
| Dev | JFK |
| Eliot | JFK |
| Jeff | BOS |
<!-- vale on -->

下列查詢會找出每位旅客可到達的機場：

```sql
source = travelers
  | graphLookup airports
    start=nearestAirport
    edge=connects-->airport
    as reachableAirports
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| name | nearestAirport | reachableAirports |
| --- | --- | --- |
| Dev | JFK | [{airport:JFK, connects:[BOS, ORD]}] |
| Eliot | JFK | [{airport:JFK, connects:[BOS, ORD]}] |
| Jeff | BOS | [{airport:BOS, connects:[JFK, PWM]}] |

<!-- vale on -->

## 範例 6：雙向走訪圖形

下列查詢會執行雙向走訪，以找出直屬主管以及共用同一位主管的同事：

```sql
source = employees
  | where name = 'Ron'
  | graphLookup employees
    start=reportsTo
    edge=reportsTo<->name
    as connections
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| name | reportsTo | id | connections |
| --- | --- | --- | --- |
| Ron | Andrew | 3 | [{name:Ron, reportsTo:Andrew, id:3}, {name:Andrew, reportsTo:null, id:4}, {name:Dan, reportsTo:Andrew, id:6}] |

<!-- vale on -->

使用雙向走訪時，Ron 的 connections 包含下列記錄：

- 他自己的記錄（Ron 向 Andrew 報告）。
- 他的主管（Andrew）。
- 他的同儕（Dan，他也向 Andrew 報告）。

## 批次模式

當 `batchMode=true` 時，`graphLookup` 命令會收集所有來源資料列中的所有起始值，並執行單一統一的 BFS 走訪，而不是分別走訪每個資料列。

在下列情況使用 `batchMode=true`：

- 您想找出可從**任何**來源起始值到達的所有節點。
- 您需要從多個起始點檢視圖形連線性的全域檢視。
- 當多個來源資料列共用重疊路徑時，您想避免重複走訪。

在批次模式中，輸出是包含兩個陣列的**單一資料列**：
1. 收集到的所有來源資料列。
2. 統一 BFS 走訪的所有 lookup 結果。

下列查詢會找出可從每位旅客最近機場到達的所有機場：

```sql
source = travelers
  | graphLookup airports
    start=nearestAirport
    edge=connects-->airport
    batchMode=true
    maxDepth=2
    as reachableAirports
```
{% include copy.html %}

**標準模式**（預設）：每位旅客會獲指派一份可到達機場的清單：

```text
| name  | nearestAirport | reachableAirports                    |
|-------|----------------|--------------------------------------|
| Dev   | JFK            | [{airport:JFK, connects:[BOS, ORD]}] |
| Jeff  | BOS            | [{airport:BOS, connects:[JFK, PWM]}] |
```

**批次模式**：所有旅客與所有可到達機場會合併成單一結果：

```text
| travelers                                                          | reachableAirports                                           |
|--------------------------------------------------------------------|-------------------------------------------------------------|
| [{name:Dev, nearestAirport:JFK}, {name:Jeff, nearestAirport:BOS}] | [{airport:JFK, connects:[BOS, ORD]}, {airport:BOS, ...}]   |
```

## 陣列欄位

當 `fromField` 或 `toField` 包含陣列值時，請設定 `supportArray=true` 以確保正確的走訪行為。

## PIT 搜尋


根據預設，BFS 走訪的每一層會將傳回的文件數限制為 lookup 索引的 `max_result_window` 設定 (通常為 10,000)。這可避免 Point in Time (PIT) 搜尋的額外負荷，但當單一走訪層符合的文件數超過限制時，可能會傳回不完整的結果。

當 `usePIT=true` 時，會移除此限制，且 lookup 表會使用以 PIT 為基礎的分頁，以確保在每個走訪層擷取所有符合的文件。這會提供完整且準確的結果，但會增加搜尋的額外負荷。

在下列情況使用 `usePIT=true`：

- 圖形包含連接數多的節點，單一走訪層可能會傳回超過 `max_result_window` 份文件。
- 結果完整性比查詢效能更重要。
- 您使用預設設定時觀察到不完整或缺少的結果。

下列查詢會啟用 PIT 搜尋，以確保完整的走訪結果：

```sql
source = employees
  | graphLookup employees
    start=reportsTo
    edge=reportsTo-->name
    usePIT=true
    as reportingHierarchy
```
{% include copy.html %}

## 篩選後的圖形走訪

`filter` 參數會限制 BFS 走訪期間納入考量的 lookup 索引文件。在每個走訪層中，只有符合篩選條件的文件會納入做為候選項。

下列查詢只會走訪報告階層中的在職員工：

```sql
source = employees
  | graphLookup employees
    start=reportsTo
    edge=reportsTo-->name
    filter=(status = 'active')
    as reportingHierarchy
```
{% include copy.html %}

篩選條件會在 OpenSearch 查詢層級套用，因此能有效率地與 BFS 走訪查詢結合。在每個 BFS 層級，傳送至 OpenSearch 的查詢為  `bool { filter: [user_filter, bfs_terms_query] }`。

## 限制

請注意 `graphLookup` 命令的下列限制：

- 來源輸入提供走訪的起始點，為避免效能問題，其上限為 100 份文件。
- 當 `usePIT=false`（預設）時，每個走訪層級傳回的結果最多只會達到 lookup 索引的 `max_result_window`，因此結果可能不完整。請設定 `usePIT=true` 以取得完整結果。
