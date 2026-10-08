---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Children
parent: Bucket aggregations
nav_order: 15
---

# Children 彙總

`children` 彙總是一種桶 (bucket) 彙總，會根據索引中定義的父子關係，建立一個包含子文件的單一桶。

`children` 彙總搭配 [join 欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/join/) 使用，用於彙總與父文件相關聯的子文件。

`children` 彙總會識別符合特定子關係名稱的子文件，而 [`parent` 彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/parent/) 則會識別具有相符子文件的父文件。這兩種彙總都以子關係名稱作為輸入。

## 參數

`children` 彙總接受下列參數。

| 參數             | 必要/選用 | 資料類型       | 說明 |
| :--                   | :--               | :--             | :--         |
| `type`                | 必要          | 字串          | join 欄位中子類型的名稱。用於識別要使用的父子關係。 |


## 範例

下列範例會建立一個包含三名員工的小型公司資料庫。每筆員工記錄都與一筆父部門記錄具有子 `join` 關係。

首先，建立一個 `company` 索引，其中包含一個將部門 (父) 對應至員工 (子) 的 `join` 欄位：

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

接著，填入三個部門和三名員工的資料。父子指派關係如下表所示。

| 部門 (父) | 員工 (子) |
| :-- | :-- |
| `Accounting` | `Abel Anderson`、`Betty Billings` |
| `Engineering` | `Carl Carter` |
| `HR` | 無 |

`routing` 參數可確保父文件和子文件都儲存在同一個分片上，這是 OpenSearch 中父子關係正常運作的必要條件：

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

下列請求會查詢所有部門，然後篩選出名為 `Accounting` 的部門。接著使用 `children` 彙總，選取與 `Accounting` 部門具有子關係的兩份文件。最後，`avg` 子彙總會傳回 `Accounting` 員工薪資的平均值：

```json
GET /company/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "join_field": "department"
          }
        },
        {
          "term": {
            "department_name": "Accounting"
          }
        }
      ]
    }
  },
  "aggs": {
    "acc_employees": {
      "children": {
        "type": "employee"
      },
      "aggs": {
        "avg_salary": {
          "avg": {
            "field": "salary"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

回應會傳回所選取的部門桶，找出該部門的 `employee` 類型子項，並計算其薪資的 `avg`：

```json
{
  "took": 379,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "acc_employees": {
      "doc_count": 2,
      "avg_salary": {
        "value": 110000
      }
    }
  }
}
```