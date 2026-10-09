---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: chart
parent: Commands
grand_parent: PPL
nav_order: 9
---

<!-- vale off -->

# chart 命令

<!-- vale on -->

`chart` 命令透過套用統計彙總函式來轉換搜尋結果，並可選擇性地依一或兩個欄位分組資料。當依兩個欄位分組時，結果適合用於二維圖表視覺化，第二個分組鍵的唯一值會樞紐為欄位名稱。

## 語法

`chart` 命令的語法如下：

```sql
chart [limit=(top|bottom) <number>] [useother=<boolean>] [usenull=<boolean>] [nullstr=<string>] [otherstr=<string>] <aggregation_function> [ by <row_split> <column_split> ] | [over <row_split> ] [ by <column_split>]
```

## 參數

`chart` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 | 預設 |
| --- | --- | --- | --- |
| `<aggregation_function>` | 必要 | 要套用至資料的彙總函式。僅支援單一彙總函式。可用的函式為 [`stats`]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/stats/) 命令支援的彙總函式。 | N/A |
| `<by>` | 選用 | 依單一欄位（列分割）或兩個欄位（列分割與欄分割）分組結果。參數 `limit`、`useother` 與 `usenull` 適用於欄分割。結果會以每個組合的個別列傳回。 | 對所有文件彙總 |
| `over [] by []` | 選用 | 依多個欄位分組的另一種語法。`over <row_split> by <column_split>` 會依兩個欄位分組結果。單獨對一個欄位使用 `over` 等同於 `by <row_split>`。 | N/A |
| `limit` | 選用 | 使用欄分割時要顯示的類別數量。`limit=N` 或 `limit=topN` 會傳回前 N 個類別。`limit=bottomN` 會傳回後 N 個類別。當超過限制時，其餘類別會分組為一個 `OTHER` 類別（除非 `useother=false`）。設為 `0` 可顯示所有類別而不受限制。排名依據是每個欄類別的彙總值總和。例如，`limit=top3` 會保留總值最高的三個類別。僅在依兩個欄位分組時適用。 | `top10` |
| `useother` | 選用 | 控制是否為超出 `limit` 的類別建立 `OTHER` 類別。設為 `false` 時，僅顯示前 N 或後 N 個類別（依據 `limit`），不會有 `OTHER` 類別。設為 `true` 時，超出 `limit` 的類別會分組為一個 `OTHER` 類別。此參數僅在使用欄分割且類別數量超過 `limit` 時適用。 | `true` |
| `usenull` | 選用 | 控制是否將欄分割欄位中具有 null 值的文件分組為一個獨立的 `NULL` 類別。此參數僅適用於欄分割。列分割欄位中具有 null 值的文件會被忽略；只有列分割欄位中具有非 null 值的文件才會納入結果。當 `usenull=false` 時，欄分割欄位中具有 null 值的文件會從結果中排除。當 `usenull=true` 時，欄分割欄位中具有 null 值的文件會分組為一個獨立的 `NULL` 類別。 | `true` |
| `nullstr` | 選用 | 指定欄分割欄位中具有 null 值之文件的類別名稱。此參數僅在 `usenull` 為 `true` 時適用。 | `"NULL"` |
| `otherstr` | 選用 | 指定 `OTHER` 類別的類別名稱。此參數僅在 `useother` 為 `true` 且有超出 `limit` 的值時適用。 | `OTHER` |


## 注意事項

使用 `chart` 命令時，請注意下列事項：

* 由欄分割產生的欄位會轉換為字串。這可確保與 `nullstr` 和 `otherstr` 的相容性，並允許這些欄位在樞紐後作為欄位名稱使用。
* 彙總函式所用欄位中具有 null 值的文件會從彙總中排除。例如，在 `chart avg(balance) over deptno, group` 中，`balance` 為 null 的文件會從平均值計算中排除。
* 彙總指標會顯示為結果中的最後一欄。結果欄位的排序如下：`[row split] [column split] [aggregation metrics]`。

## 範例 1：不進行分組的基本彙總  

此範例計算記錄項目的總數：
  
```sql
source=otellogs
| chart count() as total_logs
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| total_logs |
| --- |
| 20 |

<!-- vale on -->
  

## 範例 2：依單一欄位分組  

此範例依嚴重性層級計算記錄數，適用於嚴重性分布圓餅圖：
  
```sql
source=otellogs
| chart count() by severityText
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | count() |
| --- | --- |
| DEBUG | 3 |
| ERROR | 7 |
| INFO | 6 |
| WARN | 4 |

<!-- vale on -->
  

## 範例 3：使用 over [] by [] 依多個欄位分組  

下列查詢建立一個二維圖表，顯示依嚴重性層級與服務分類的記錄數量，適合用於熱力圖視覺化：
  
```sql
source=otellogs
| chart limit=2 count() over severityText by `resource.attributes.service.name`
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果。超出前 2 名的服務會分組為 `OTHER`：
  
<!-- vale off -->

| severityText | `resource.attributes.service.name` | count() |
| --- | --- | --- |
| DEBUG | OTHER | 2 |
| DEBUG | product-catalog | 1 |
| ERROR | OTHER | 6 |
| ERROR | product-catalog | 1 |
| INFO | OTHER | 2 |
| INFO | frontend | 4 |
| WARN | OTHER | 2 |
| WARN | product-catalog | 2 |

<!-- vale on -->
  

## 範例 4：使用 limit 與自訂 other 標籤  

下列查詢限制每個嚴重性層級僅顯示前 1 個服務，並將其餘服務標記為 `other_services`：
  
```sql
source=otellogs
| chart limit=top1 useother=true otherstr='other_services' count() over severityText by `resource.attributes.service.name`
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | `resource.attributes.service.name` | count() |
| --- | --- | --- |
| DEBUG | other_services | 3 |
| ERROR | other_services | 7 |
| INFO | frontend | 4 |
| INFO | other_services | 2 |
| WARN | other_services | 4 |

<!-- vale on -->
  

## 範例 5：使用 null 參數  

下列查詢顯示依命名空間分類的每個服務記錄數量，並將沒有命名空間的服務標記為 `no namespace`：
  
```sql
source=otellogs
| chart usenull=true nullstr='not instrumented' count() over `resource.attributes.service.name` by instrumentationScope.name
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| `resource.attributes.service.name` | instrumentationScope.name | count() |
| --- | --- | --- |
| cart | Microsoft.Extensions.Hosting | 1 |
| cart | not instrumented | 2 |
| checkout | not instrumented | 3 |
| frontend | @opentelemetry/instrumentation-http | 1 |
| frontend | not instrumented | 3 |
| frontend-proxy | not instrumented | 3 |
| payment | @opentelemetry/instrumentation-http | 1 |
| payment | not instrumented | 1 |
| product-catalog | go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc | 1 |
| product-catalog | not instrumented | 3 |
| recommendation | not instrumented | 1 |

<!-- vale on -->
  

## 範例 6：使用 span  

下列查詢繪製每個嚴重性範圍與主機的最大嚴重性圖表，有助於識別哪些主機發生最嚴重的問題：
  
```sql
source=otellogs
| chart max(severityNumber) by severityNumber span=10, `resource.attributes.host.name`
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityNumber | `resource.attributes.host.name` | max(severityNumber) |
| --- | --- | --- |
| 0 | cart-5d8f7b-mk29s | 9 |
| 0 | checkout-8b4c2d-jp5r7 | 9 |
| 0 | frontend-6b7b4c9f-x2kl9 | 9 |
| 0 | productcatalog-7c9d-zn4p2 | 5 |
| 10 | checkout-8b4c2d-jp5r7 | 17 |
| 10 | frontendproxy-envoy-7d4b8c-xk2q9 | 17 |
| 10 | payment-6f8d4b-ht7q3 | 17 |
| 10 | productcatalog-7c9d-zn4p2 | 17 |
| 10 | recommendation-5f7c-bn3k8 | 17 |

<!-- vale on -->
  

## 限制

`chart` 命令有下列限制：

* 每個 `chart` 命令僅支援單一彙總函式。
