---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: top
parent: Commands
grand_parent: PPL
nav_order: 50
---

<!-- vale off -->

# top 命令

<!-- vale on -->

`top` 命令會找出欄位清單中所有指定欄位裡最常見的值組合。

`top` 命令不會改寫為 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/)。它只會在協調節點上執行。
{: .note}

## 語法

`top` 命令的語法如下：

```sql
top [N] [top-options] <field-list> [by-clause]
```

## 參數

`top` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<N>` | 選用 | 要傳回的結果數量。預設為 `10`。 |
| `top-options` | 選用 | `showcount`：是否在輸出中建立一個代表值元組計數的欄位。預設為 `true`。<br>`countfield`：包含計數的欄位名稱。預設為 `count`。<br>`usenull`：是否輸出 `null` 值。預設為 `plugins.ppl.syntax.legacy.preferred` 的值。 |
| `<field-list>` | 必要 | 以逗號分隔的欄位名稱清單。  |
| `<by-clause>` | 選用 | 用來分組結果的一或多個欄位。 |

## 範例 1：在預設的 count 欄位中顯示計數

下列查詢會找出最常見的嚴重性層級：

```sql
source=otellogs
| top severityText
```
{% include copy.html %}
{% include try-in-playground.html %}

預設情況下，`top` 命令會自動包含一個 `count` 欄位，顯示每個值出現的頻率：

<!-- vale off -->

| severityText | count |
| --- | --- |
| ERROR | 7 |
| INFO | 6 |
| WARN | 4 |
| DEBUG | 3 |

<!-- vale on -->

## 範例 2：不顯示計數欄位，找出最常見的值

下列查詢使用 `showcount=false` 在結果中隱藏 `count` 欄位：

```sql
source=otellogs
| top showcount=false severityText
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| severityText |
| --- |
| ERROR |
| INFO |
| WARN |
| DEBUG |

<!-- vale on -->

## 範例 3：重新命名計數欄位

下列查詢使用 `countfield` 參數為計數欄位指定自訂名稱 (`cnt`)，而非預設的 `count`：
  
```sql
source=otellogs
| top countfield='cnt' severityText
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| severityText | cnt |
| --- | --- |
| ERROR | 7 |
| INFO | 6 |
| WARN | 4 |
| DEBUG | 3 |

<!-- vale on -->

## 範例 4：限制傳回的結果數量

下列查詢會傳回最常見的前 1 個嚴重性層級：

```sql
source=otellogs
| top 1 showcount=false severityText
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| severityText |
| --- |
| ERROR |

<!-- vale on -->

## 範例 5：分組結果

下列查詢會找出每個服務中最常見的嚴重性層級：

```sql
source=otellogs
| top 1 showcount=false severityText by `resource.attributes.service.name`
```
{% include copy.html %}
{% include try-in-playground.html %}

查詢會傳回下列結果：

<!-- vale off -->

| resource.attributes.service.name | severityText |
| --- | --- |
| product-catalog | WARN |
| frontend-proxy | WARN |
| recommendation | ERROR |
| payment | ERROR |
| checkout | ERROR |
| cart | DEBUG |
| frontend | INFO |

<!-- vale on -->

## 範例 6：指定 null 值的處理方式

下列查詢指定 `usenull=false` 以排除 null 值：

```sql
source=otellogs
| top usenull=false instrumentationScope.name
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| instrumentationScope.name | count |
| --- | --- |
| @opentelemetry/instrumentation-http | 2 |
| Microsoft.Extensions.Hosting | 1 |
| go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc | 1 |

<!-- vale on -->

下列查詢指定 `usenull=true` 以在結果中包含 null 值：

```sql
source=otellogs
| top usenull=true instrumentationScope.name
```
{% include copy.html %}
{% include try-in-playground.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| instrumentationScope.name | count |
| --- | --- |
| null | 16 |
| @opentelemetry/instrumentation-http | 2 |
| Microsoft.Extensions.Hosting | 1 |
| go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc | 1 |

<!-- vale on -->
