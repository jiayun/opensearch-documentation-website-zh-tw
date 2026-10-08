---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Parent
parent: Bucket aggregations
nav_order: 145
---

# Parent 彙總

`parent` 彙總是一種桶 (bucket) 彙總，它會根據您索引中定義的父子關係，建立一個包含父文件的單一桶。此彙總使您能夠對具有相同匹配子文件的父文件執行分析，從而實現強大的階層式資料分析。

`parent` 彙總與 [`join` 欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/join/) 配合使用，該類型可在同一索引的文件之間建立父子關係。

`parent` 彙總會識別具有匹配子文件的父文件，而 [`children` 彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/children/) 則會識別匹配特定子關係的子文件。這兩種彙總都將子關係名稱作為輸入。


## 參數

`parent` 彙總使用以下參數：

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :-- | :-- | :-- | :-- |
| `type` | 必要 | String | 來自 `join` 欄位的子類型名稱。 |

## 範例

以下範例建立了一個包含三名員工的小型公司資料庫。每筆員工記錄都與父部門記錄具有子 `join` 關係。

首先，建立一個 `company` 索引，其中包含一個將部門 (父) 對應到員工 (子) 的 `join` 欄位：

```json
PUT /company
{
  "mappings": {
    "properties": {
      "join_field": {
        "type": "join",
        "relations": {
          "department": "employee"
        }
      },
      "department_name": {
        "type": "keyword"
      },
      "employee_name": {
        "type": "keyword"
      },
      "salary": {
        "type": "double"
      },
      "hire_date": {
        "type": "date"
      }
    }
  }
}
```
{% include copy-curl.html %}

接下來，填入三個部門和三名員工的資料。父子分配情況如下表所示。

| 部門 (父) | 員工 (子) |
| :-- | :-- |
| `Accounting` | `Abel Anderson`, `Betty Billings` |
| `Engineering` | `Carl Carter` |
| `HR` | 無 |

`routing` 參數可確保父文件和子文件都儲存在同一分片中，這是 OpenSearch 中父子關係能正確運作的必要條件：

```json
POST _bulk?routing=1
{ "create": { "_index": "company", "_id": "1" } }
{ "type": "department", "department_name": "Accounting", "join_field": "department" }
{ "create": { "_index": "company", "_id": "2" } }
{ "type": "department", "department_name": "Engineering", "join_field": "department" }
{ "create": { "_index": "company", "_id": "3" } }
{ "type": "department", "department_name": "HR", "join_field": "department" }
{ "create": { "_index": "company", "_id": "4" } }
{ "type": "employee", "employee_name": "Abel Anderson", "salary": 120000, "hire_date": "2024-04-04", "join_field": { "name": "employee",  "parent": "1" } }
{ "create": { "_index": "company", "_id": "5" } }
{ "type": "employee", "employee_name": "Betty Billings", "salary": 140000, "hire_date": "2023-05-05", "join_field": { "name": "employee",  "parent": "1" } }
{ "create": { "_index": "company", "_id": "6" } }
{ "type": "employee", "employee_name": "Carl Carter", "salary": 140000, "hire_date": "2020-06-06",  "join_field": { "name": "employee",  "parent": "2" } }
```
{% include copy-curl.html %}

最後，對所有與一名或多名員工具有父關係的部門執行彙總：

```json
GET /company/_search
{
  "size": 0,
  "aggs": {
    "all_departments": {
      "parent": {
        "type": "employee"
      },
      "aggs": {
        "departments": {
          "terms": {
            "field": "department_name"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

`all_departments` 父彙總會回傳所有具有員工子文件的部門。請注意，HR 部門未被列出：

```json
{
  "took": 3,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 6,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "all_departments": {
      "doc_count": 2,
      "departments": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
          {
            "key": "Accounting",
            "doc_count": 1
          },
          {
            "key": "Engineering",
            "doc_count": 1
          }
        ]
      }
    }
  }
}
```