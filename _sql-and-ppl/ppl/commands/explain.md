---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: explain
parent: Commands
grand_parent: PPL
nav_order: 16
---

<!-- vale off -->

# explain 命令

<!-- vale on -->

`explain` 命令會顯示查詢的執行計畫，常用於查詢轉換與疑難排解。`explain` 命令只能作為 PPL 查詢中的第一個命令。

## 語法

`explain` 命令具有下列語法：

```sql
explain <mode> queryStatement
```

## 參數

`explain` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<queryStatement>` | 必要 | 要解釋的 PPL 查詢。 |
| `<mode>` | 選用 | 解釋模式。有效值為：<br> - `standard`：顯示邏輯與實體計畫以及下推資訊（查詢領域特定語言 [DSL]）。v2 與 v3 引擎皆可使用。<br> - `simple`：顯示不含屬性的邏輯計畫樹。需要 v3 引擎（`plugins.calcite.enabled` = `true`）。<br> - `cost`：顯示標準資訊加上計畫成本屬性。需要 v3 引擎（`plugins.calcite.enabled` = `true`）。<br> - `extended`：顯示標準資訊加上產生的程式碼。如果整個計畫都能下推，則等同於標準模式。需要 v3 引擎（`plugins.calcite.enabled` = `true`）。<br><br> 預設為 `standard`。 |

## 範例 1：在 v2 引擎中解釋 PPL 查詢  

當 Apache Calcite 停用時（`plugins.calcite.enabled` 設為 `false`），`explain` 會從 v2 引擎取得其實體計畫與下推資訊：
  
```sql
explain source=state_country
| where country = 'USA' OR country = 'England'
| stats count() by country
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
```json
{
  "root": {
    "name": "ProjectOperator",
    "description": {
      "fields": "[count(), country]"
    },
    "children": [
      {
        "name": "OpenSearchIndexScan",
        "description": {
          "request": """OpenSearchQueryRequest(indexName=state_country, sourceBuilder={"from":0,"size":10000,"timeout":"1m","query":{"bool":{"should":[{"term":{"country":{"value":"USA","boost":1.0}}},{"term":{"country":{"value":"England","boost":1.0}}}],"adjust_pure_negative":true,"boost":1.0}},"aggregations":{"composite_buckets":{"composite":{"size":1000,"sources":[{"country":{"terms":{"field":"country","missing_bucket":true,"missing_order":"first","order":"asc"}}}]},"aggregations":{"count()":{"value_count":{"field":"_index"}}}}}}, pitId=null, cursorKeepAlive=null, searchAfter=null, searchResponse=null)"""
        },
        "children": []
      }
    ]
  }
}
```
  

## 範例 2：在 v3 引擎中解釋 PPL 查詢  

當 Apache Calcite 啟用時（`plugins.calcite.enabled` 設為 `true`），`explain` 會從 v3 引擎取得其邏輯與實體計畫以及下推資訊：  
  
```sql
explain source=state_country
| where country = 'USA' OR country = 'England'
| stats count() by country
```
{% include copy.html %}
  
查詢會傳回下列結果：

```json
{
  "calcite": {
    "logical": """LogicalProject(count()=[$1], country=[$0])
  LogicalAggregate(group=[{1}], count()=[COUNT()])
    LogicalFilter(condition=[SEARCH($1, Sarg['England', 'USA':CHAR(7)]:CHAR(7))])
      CalciteLogicalIndexScan(table=[[OpenSearch, state_country]])
""",
    "physical": """EnumerableCalc(expr#0..1=[{inputs}], count()=[$t1], country=[$t0])
  CalciteEnumerableIndexScan(table=[[OpenSearch, state_country]], PushDownContext=[[FILTER->SEARCH($1, Sarg['England', 'USA':CHAR(7)]:CHAR(7)), AGGREGATION->rel#53:LogicalAggregate.NONE.[]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/input=RelSubset#43,group={1},count()=COUNT())], OpenSearchRequestBuilder(sourceBuilder={"from":0,"size":0,"timeout":"1m","query":{"terms":{"country":["England","USA"],"boost":1.0}},"aggregations":{"composite_buckets":{"composite":{"size":1000,"sources":[{"country":{"terms":{"field":"country","missing_bucket":true,"missing_order":"first","order":"asc"}}}]},"aggregations":{"count()":{"value_count":{"field":"_index"}}}}}}, requestedTotalSize=2147483647, pageSize=null, startFrom=0)])
"""
  }
}
```
  

## 範例 3：以 simple 模式解釋 PPL 查詢  

下列查詢以 `simple` 模式使用 `explain` 命令來顯示簡化的邏輯計畫樹： 
  
```sql
explain simple source=state_country
| where country = 'USA' OR country = 'England'
| stats count() by country
```
{% include copy.html %}
  
查詢會傳回下列結果： 
  
```json
{
  "calcite": {
    "logical": """LogicalProject
  LogicalAggregate
    LogicalFilter
      CalciteLogicalIndexScan
"""
  }
}
```
  

## 範例 4：以 cost 模式解釋 PPL 查詢  

下列查詢以 `cost` 模式使用 `explain` 命令來顯示計畫成本屬性：
  
```sql
explain cost source=state_country
| where country = 'USA' OR country = 'England'
| stats count() by country
```
{% include copy.html %}
  
查詢會傳回下列結果：

```json
{
  "calcite": {
    "logical": """LogicalProject(count()=[$1], country=[$0]): rowcount = 2.5, cumulative cost = {130.3125 rows, 206.0 cpu, 0.0 io}, id = 75
  LogicalAggregate(group=[{1}], count()=[COUNT()]): rowcount = 2.5, cumulative cost = {127.8125 rows, 201.0 cpu, 0.0 io}, id = 74
    LogicalFilter(condition=[SEARCH($1, Sarg['England', 'USA':CHAR(7)]:CHAR(7))]): rowcount = 25.0, cumulative cost = {125.0 rows, 201.0 cpu, 0.0 io}, id = 73
      CalciteLogicalIndexScan(table=[[OpenSearch, state_country]]): rowcount = 100.0, cumulative cost = {100.0 rows, 101.0 cpu, 0.0 io}, id = 72
""",
    "physical": """EnumerableCalc(expr#0..1=[{inputs}], count()=[$t1], country=[$t0]): rowcount = 100.0, cumulative cost = {200.0 rows, 501.0 cpu, 0.0 io}, id = 138
  CalciteEnumerableIndexScan(table=[[OpenSearch, state_country]], PushDownContext=[[FILTER->SEARCH($1, Sarg['England', 'USA':CHAR(7)]:CHAR(7)), AGGREGATION->rel#125:LogicalAggregate.NONE.[]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/input=RelSubset#115,group={1},count()=COUNT())], OpenSearchRequestBuilder(sourceBuilder={"from":0,"size":0,"timeout":"1m","query":{"terms":{"country":["England","USA"],"boost":1.0}},"aggregations":{"composite_buckets":{"composite":{"size":1000,"sources":[{"country":{"terms":{"field":"country","missing_bucket":true,"missing_order":"first","order":"asc"}}}]},"aggregations":{"count()":{"value_count":{"field":"_index"}}}}}}, requestedTotalSize=2147483647, pageSize=null, startFrom=0)]): rowcount = 100.0, cumulative cost = {100.0 rows, 101.0 cpu, 0.0 io}, id = 133
"""
  }
}
```
  

## 範例 5：以 extended 模式解釋 PPL 查詢

下列查詢以 `extended` 模式使用 `explain` 命令來顯示產生的程式碼：

```sql
explain extended source=state_country
| where country = 'USA' OR country = 'England'
| stats count() by country
```
{% include copy.html %}
  
查詢會傳回下列結果：

```json
{
  "calcite": {
    "logical": """LogicalProject(count()=[$1], country=[$0])
  LogicalAggregate(group=[{1}], count()=[COUNT()])
    LogicalFilter(condition=[SEARCH($1, Sarg['England', 'USA':CHAR(7)]:CHAR(7))])
      CalciteLogicalIndexScan(table=[[OpenSearch, state_country]])
""",
    "physical": """EnumerableCalc(expr#0..1=[{inputs}], count()=[$t1], country=[$t0])
  CalciteEnumerableIndexScan(table=[[OpenSearch, state_country]], PushDownContext=[[FILTER->SEARCH($1, Sarg['England', 'USA':CHAR(7)]:CHAR(7)), AGGREGATION->rel#193:LogicalAggregate.NONE.[]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/input=RelSubset#183,group={1},count()=COUNT())], OpenSearchRequestBuilder(sourceBuilder={"from":0,"size":0,"timeout":"1m","query":{"terms":{"country":["England","USA"],"boost":1.0}},"aggregations":{"composite_buckets":{"composite":{"size":1000,"sources":[{"country":{"terms":{"field":"country","missing_bucket":true,"missing_order":"first","order":"asc"}}}]},"aggregations":{"count()":{"value_count":{"field":"_index"}}}}}}, requestedTotalSize=2147483647, pageSize=null, startFrom=0)])
""",
    "extended": """public org.apache.calcite.linq4j.Enumerable bind(final org.apache.calcite.DataContext root) {
  final org.opensearch.sql.opensearch.storage.scan.CalciteEnumerableIndexScan v1stashed = (org.opensearch.sql.opensearch.storage.scan.CalciteEnumerableIndexScan) root.get("v1stashed");
  final org.apache.calcite.linq4j.Enumerable _inputEnumerable = v1stashed.scan();
  return new org.apache.calcite.linq4j.AbstractEnumerable(){
      public org.apache.calcite.linq4j.Enumerator enumerator() {
        return new org.apache.calcite.linq4j.Enumerator(){
            public final org.apache.calcite.linq4j.Enumerator inputEnumerator = _inputEnumerable.enumerator();
            public void reset() {
              inputEnumerator.reset();
            }
            public boolean moveNext() {
              return inputEnumerator.moveNext();
            }
            public void close() {
              inputEnumerator.close();
            }
            public Object current() {
              final Object[] current = (Object[]) inputEnumerator.current();
              final Object input_value = current[1];
              final Object input_value0 = current[0];
              return new Object[] {
                  input_value,
                  input_value0};
            }
          };
      }
    };
}
public Class getElementType() {
  return java.lang.Object[].class;
}
"""
  }
}
```