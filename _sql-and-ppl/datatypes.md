---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "資料類型"
nav_order: 7
redirect_from:
  - /search-plugins/sql/datatypes/
---

# SQL 與 PPL 資料類型

下表顯示 SQL 外掛程式支援的資料類型，以及每個類型如何對應至 SQL 與 OpenSearch 資料類型。

| OpenSearch SQL 類型 | OpenSearch 類型 | SQL 類型
:--- | :--- | :---
`boolean` |	布林值 |	`BOOLEAN`
`byte` |	Byte |	`TINYINT`
`short` |	Byte |	`SMALLINT`
`integer` |	整數 |	`INTEGER`
`long` | Long |	`BIGINT`
`float` |	Float |	`REAL`
`half_float` | Float | `FLOAT`
`scaled_float` | Float | `DOUBLE`
`double` | Double | `DOUBLE`
`keyword` |	字串 | `VARCHAR`
`text` | Text | `VARCHAR`
`date` | Timestamp | `TIMESTAMP`
`date_nanos` | Timestamp | `TIMESTAMP`
`ip` | IP | `VARCHAR`
`binary` | Binary | `VARBINARY`
`object` | Struct | `STRUCT`
`nested` | 陣列 | `STRUCT`

除了此清單之外，SQL 外掛程式也支援 `datetime` 類型，不過它沒有對應至 OpenSearch 或 SQL 的對應關係。
若要使用沒有對應關係的函式，您必須明確地將資料類型轉換為有對應關係的類型。


## 日期與時間類型

日期與時間類型代表一段時間：`DATE`、`TIME`、`DATETIME`、`TIMESTAMP` 及 `INTERVAL`。根據預設，OpenSearch DSL 使用 `date` 類型作為唯一與日期時間相關的類型，其中包含絕對時間點的所有資訊。

為了與 SQL 整合，除了 `timestamp` 類型之外，每個類型都只保留部分時間資訊。若要使用日期時間函式，請參閱[日期與時間]({{site.url}}{{site.baseurl}}/sql-and-ppl/functions#date-and-time)。部分函式可能對輸入引數類型有所限制。


### 日期

`date` 類型代表日曆日期，與時區無關。指定的日期值是一段 24 小時的期間，但此期間在不同時區會有所不同，且在日光節約時間期間可能會有彈性的時數。`date` 類型不包含時間資訊，且僅支援 `1000-01-01` 至 `9999-12-31` 的範圍。

| 類型 | 語法 | 範圍
:--- | :--- | :---
`date` | `yyyy-MM-dd` | `0001-01-01` 至 `9999-12-31`

### 時間

`time` 類型代表時鐘時間，與其時區無關。`time` 類型不包含日期資訊。

| 類型 | 語法 | 範圍
:--- | :--- | :---
`time` | `hh:mm:ss[.fraction]` | `00:00:00.0000000000` 至 `23:59:59.9999999999`

### 日期與時間

`datetime` 類型是日期與時間的組合。它不包含時區資訊。若需要包含日期、時間與時區資訊的絕對時間點，請參閱[時間戳記](#timestamp)。

| 類型 | 語法 | 範圍
:--- | :--- | :---
`datetime` | `yyyy-MM-dd hh:mm:ss[.fraction]` | `0001-01-01 00:00:00.0000000000` 至 `9999-12-31 23:59:59.9999999999`

### 時間戳記

`timestamp` 類型是獨立於時區或慣例的絕對時刻。例如，對於指定的時間點，如果您將時間戳記變更為不同的時區，其值也會隨之改變。

`timestamp` 類型的儲存方式與其他類型不同。儲存時會從其目前時區轉換為 UTC，擷取時則會從 UTC 轉換回其設定的時區。

| 類型 | 語法 | 範圍
:--- | :--- | :---
`timestamp` | `yyyy-MM-dd hh:mm:ss[.fraction]` | `0001-01-01 00:00:01.9999999999` UTC 至 `9999-12-31 23:59:59.9999999999`

### 時間間隔

`interval` 類型代表一段時間長度或期間。

| 類型 | 語法
:--- | :---
`interval` | `INTERVAL expr unit`

`expr` 可以是最終求得數量值的任何運算式。單位是用來解讀該數量的單位，包括 `MICROSECOND`、`SECOND`、`MINUTE`、`HOUR`、`DAY`、`WEEK`、`MONTH`、`QUARTER` 及 `YEAR`。`INTERVAL` 關鍵字與單位指定元沒有大小寫之分。

`interval` 類型有兩類間隔：年週間隔與日時間隔。

- 年週間隔儲存年、季、月與週。
- 日時間隔儲存日、時、分、秒與微秒。


### 在日期與時間類型之間轉換

除了 `interval` 類型之外，所有日期與時間類型都可以互相轉換。轉換可能會改變值或造成部分資訊遺失。例如，從 `datetime` 值擷取 `time` 值，或將 `date` 值轉換為 `datetime` 值等等。

SQL 外掛程式支援下列每種類型的轉換規則：

**從 date 轉換**

- 因為 `date` 值沒有任何時間資訊，轉換為 `time` 類型沒有用處，且一律會傳回 `00:00:00` 的零時間值。
- 從 `date` 轉換為 `datetime` 時，由於缺少時間資訊，會進行資料填補。根據預設，它會將時間 `00:00:00` 附加至原始日期，並形成 `datetime` 執行個體。例如，將 `2020-08-17` 轉換為 `datetime` 類型會得到 `2020-08-17 00:00:00`。
- 轉換為 `timestamp` 類型會同時變更 `time` 值與時區資訊。它會將零時間值 `00:00:00` 與工作階段時區（預設為 UTC）附加至日期。例如，將 `2020-08-17` 轉換為工作階段時區為 UTC 的 `datetime` 類型會得到 `2020-08-17 00:00:00 UTC`。

**從 time 轉換**

- 您無法將 `time` 類型轉換為任何其他日期與時間類型，因為它不包含任何日期資訊。

**從 `datetime` 轉換**

- 將 `datetime` 轉換為 `date` 會從 `datetime` 值擷取日期值。例如，將 `2020-08-17 14:09:00` 轉換為 `date` 類型會得到 `2020-08-08`。
- 將 `datetime` 轉換為 `time` 會從 `datetime` 值擷取時間值。例如，將 `2020-08-17 14:09:00` 轉換為 `time` 類型會得到 `14:09:00`。
- 因為 `datetime` 類型不包含時區資訊，轉換為 `timestamp` 類型時會以工作階段時區填補時區值。例如，將 `2020-08-17 14:09:00` (UTC) 轉換為 `timestamp` 類型會得到 `2020-08-17 14:09:00 UTC`。

**從 timestamp 轉換**

- 從 `timestamp` 類型轉換為 `date` 類型會擷取日期值，轉換為 `time` 類型則會擷取時間值。從 `timestamp` 類型轉換為 `datetime` 類型只會擷取 `datetime` 值，並省略時區值。例如，將 `2020-08-17 14:09:00` UTC 轉換為 `date` 類型會得到 `2020-08-17`，轉換為 `time` 類型會得到 `14:09:00`，而轉換為 `datetime` 類型會得到 `2020-08-17 14:09:00`。
