---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: rare
parent: Commands
grand_parent: PPL
nav_order: 35
---

<!-- vale off -->

# rare 命令

<!-- vale on -->

`rare` 命令會找出欄位清單中所有欄位裡最不常見的值組合。

此命令會針對 group-by 欄位中每個不同的值組合，最多傳回 10 筆結果。
{: .note}

`rare` 命令不會改寫為 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/)。它只會在協調節點上執行。
{: .note}

## 語法

`rare` 命令的語法如下：

```sql
rare [rare-options] <field-list> [by-clause]
```

## 參數

`rare` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<field-list>` | 必要 | 以逗號分隔的欄位名稱清單。 |
| `<by-clause>` | 選用 | 用來將結果分組的一或多個欄位。 |
| `rare-options` | 選用 | 控制輸出的其他選項：<br> - `showcount`：是否在輸出中建立包含每個值組合出現次數的欄位。預設為 `true`。<br> - `countfield`：包含計數的欄位名稱。預設為 `count`。<br> - `usenull`：是否輸出 null 值。預設為 `plugins.ppl.syntax.legacy.preferred` 的值。 |

## 範例 1：找出最不常見的值而不顯示計數

下列查詢使用 `showcount=false` 找出最不常見的嚴重性層級，而不顯示出現次數：

```sql
source=otellogs
| rare showcount=false severityText
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| severityText |
| --- |
| DEBUG |
| WARN |
| INFO |
| ERROR |

<!-- vale on -->

## 範例 2：依欄位分組找出最不常見的值

下列查詢會依服務分組，找出最不常見的嚴重性層級：

```sql
source=otellogs
| rare showcount=false severityText by `resource.attributes.service.name`
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| resource.attributes.service.name | severityText |
| --- | --- |
| product-catalog | DEBUG |
| product-catalog | ERROR |
| product-catalog | WARN |
| frontend-proxy | ERROR |
| frontend-proxy | WARN |
| recommendation | ERROR |
| payment | ERROR |
| checkout | INFO |
| checkout | ERROR |
| cart | INFO |
| cart | DEBUG |
| frontend | INFO |

<!-- vale on -->

## 範例 3：找出最不常見的值並顯示出現次數

下列查詢會找出最不常見的嚴重性層級及其出現次數：

```sql
source=otellogs
| rare severityText
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| severityText | count |
| --- | --- |
| DEBUG | 3 |
| WARN | 4 |
| INFO | 6 |
| ERROR | 7 |

<!-- vale on -->

## 範例 4：自訂計數欄位名稱

下列查詢使用 `countfield` 為出現次數欄位指定自訂名稱：

```sql
source=otellogs
| rare countfield='cnt' severityText
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| severityText | cnt |
| --- | --- |
| DEBUG | 3 |
| WARN | 4 |
| INFO | 6 |
| ERROR | 7 |

<!-- vale on -->

## 範例 5：指定 null 值的處理方式

下列查詢使用 `usenull=false` 排除 null 值：

```sql
source=otellogs
| rare usenull=false instrumentationScope.name
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| instrumentationScope.name | count |
| --- | --- |
| Microsoft.Extensions.Hosting | 1 |
| go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc | 1 |
| @opentelemetry/instrumentation-http | 2 |

<!-- vale on -->

下列查詢使用 `usenull=true` 將 null 值納入結果中：

```sql
source=otellogs
| rare usenull=true instrumentationScope.name
```
{% include copy.html %}
{% include try-in-playground.html %}

此查詢會傳回下列結果：

<!-- vale off -->

| instrumentationScope.name | count |
| --- | --- |
| Microsoft.Extensions.Hosting | 1 |
| go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc | 1 |
| @opentelemetry/instrumentation-http | 2 |
| null | 16 |<!-- vale on -->
