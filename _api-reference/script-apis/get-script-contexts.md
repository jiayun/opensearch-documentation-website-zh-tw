---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得指令碼執行環境"
parent: Script APIs
nav_order: 70
---

# Get Script Contexts API
**於 1.0 版推出**
{: .label .label-purple }

擷取所有可使用指令碼的執行環境，例如搜尋、更新或彙總執行環境。

## 請求範例

<!-- spec_insert_start
component: example_code
rest: GET /_script_context
-->
{% capture step1_rest %}
GET /_script_context
{% endcapture %}

{% capture step1_python %}

response = client.get_script_context()
{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

`GET _script_context` 請求會傳回下列欄位：

````json
{
  "contexts" : [
    {
      "name" : "aggregation_selector",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "boolean",
          "params" : [ ]
        },
        {
          "name" : "getParams",
          "return_type" : "java.util.Map",
          "params" : [ ]
        }
      ]
    },
    {
      "name" : "aggs",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "java.lang.Object",
          "params" : [ ]
        },
        {
          "name" : "getDoc",
          "return_type" : "java.util.Map",
          "params" : [ ]
        },
        {
          "name" : "getParams",
          "return_type" : "java.util.Map",
          "params" : [ ]
        },
        {
          "name" : "get_score",
          "return_type" : "java.lang.Number",
          "params" : [ ]
        },
        {
          "name" : "get_value",
          "return_type" : "java.lang.Object",
          "params" : [ ]
        }
      ]
    },
    {
      "name" : "aggs_combine",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "java.lang.Object",
          "params" : [ ]
        },
        {
          "name" : "getParams",
          "return_type" : "java.util.Map",
          "params" : [ ]
        },
        {
          "name" : "getState",
          "return_type" : "java.util.Map",
          "params" : [ ]
        }
      ]
    },
    {
      "name" : "aggs_init",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "void",
          "params" : [ ]
        },
        {
          "name" : "getParams",
          "return_type" : "java.util.Map",
          "params" : [ ]
        },
        {
          "name" : "getState",
          "return_type" : "java.lang.Object",
          "params" : [ ]
        }
      ]
    },
    {
      "name" : "aggs_map",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "void",
          "params" : [ ]
        },
        {
          "name" : "getDoc",
          "return_type" : "java.util.Map",
          "params" : [ ]
        },
        {
          "name" : "getParams",
          "return_type" : "java.util.Map",
          "params" : [ ]
        },
        {
          "name" : "getState",
          "return_type" : "java.util.Map",
          "params" : [ ]
        },
        {
          "name" : "get_score",
          "return_type" : "double",
          "params" : [ ]
        }
      ]
    },
    {
      "name" : "aggs_reduce",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "java.lang.Object",
          "params" : [ ]
        },
        {
          "name" : "getParams",
          "return_type" : "java.util.Map",
          "params" : [ ]
        },
        {
          "name" : "getStates",
          "return_type" : "java.util.List",
          "params" : [ ]
        }
      ]
    },
    {
      "name" : "analysis",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "boolean",
          "params" : [
            {
              "type" : "org.opensearch.analysis.common.AnalysisPredicateScript$Token",
              "name" : "token"
            }
          ]
        }
      ]
    },
    {
      "name" : "bucket_aggregation",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "java.lang.Number",
          "params" : [ ]
        },
        {
          "name" : "getParams",
          "return_type" : "java.util.Map",
          "params" : [ ]
        }
      ]
    },
    {
      "name" : "field",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "java.lang.Object",
          "params" : [ ]
        },
        {
          "name" : "getDoc",
          "return_type" : "java.util.Map",
          "params" : [ ]
        },
        {
          "name" : "getParams",
          "return_type" : "java.util.Map",
          "params" : [ ]
        }
      ]
    },
    {
      "name" : "filter",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "boolean",
          "params" : [ ]
        },
        {
          "name" : "getDoc",
          "return_type" : "java.util.Map",
          "params" : [ ]
        },
        {
          "name" : "getParams",
          "return_type" : "java.util.Map",
          "params" : [ ]
        }
      ]
    },
    {
      "name" : "ingest",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "void",
          "params" : [
            {
              "type" : "java.util.Map",
              "name" : "ctx"
            }
          ]
        },
        {
          "name" : "getParams",
          "return_type" : "java.util.Map",
          "params" : [ ]
        }
      ]
    },
    {
      "name" : "interval",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "boolean",
          "params" : [
            {
              "type" : "org.opensearch.index.query.IntervalFilterScript$Interval",
              "name" : "interval"
            }
          ]
        }
      ]
    },
    {
      "name" : "moving-function",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "double",
          "params" : [
            {
              "type" : "java.util.Map",
              "name" : "params"
            },
            {
              "type" : "double[]",
              "name" : "values"
            }
          ]
        }
      ]
    },
    {
      "name" : "number_sort",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "double",
          "params" : [ ]
        },
        {
          "name" : "getDoc",
          "return_type" : "java.util.Map",
          "params" : [ ]
        },
        {
          "name" : "getParams",
          "return_type" : "java.util.Map",
          "params" : [ ]
        },
        {
          "name" : "get_score",
          "return_type" : "double",
          "params" : [ ]
        }
      ]
    },
    {
      "name" : "painless_test",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "java.lang.Object",
          "params" : [ ]
        },
        {
          "name" : "getParams",
          "return_type" : "java.util.Map",
          "params" : [ ]
        }
      ]
    },
    {
      "name" : "processor_conditional",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "boolean",
          "params" : [
            {
              "type" : "java.util.Map",
              "name" : "ctx"
            }
          ]
        },
        {
          "name" : "getParams",
          "return_type" : "java.util.Map",
          "params" : [ ]
        }
      ]
    },
    {
      "name" : "score",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "double",
          "params" : [
            {
              "type" : "org.opensearch.script.ScoreScript$ExplanationHolder",
              "name" : "explanation"
            }
          ]
        },
        {
          "name" : "getDoc",
          "return_type" : "java.util.Map",
          "params" : [ ]
        },
        {
          "name" : "getParams",
          "return_type" : "java.util.Map",
          "params" : [ ]
        },
        {
          "name" : "get_score",
          "return_type" : "double",
          "params" : [ ]
        }
      ]
    },
    {
      "name" : "script_heuristic",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "double",
          "params" : [
            {
              "type" : "java.util.Map",
              "name" : "params"
            }
          ]
        }
      ]
    },
    {
      "name" : "similarity",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "double",
          "params" : [
            {
              "type" : "double",
              "name" : "weight"
            },
            {
              "type" : "org.opensearch.index.similarity.ScriptedSimilarity$Query",
              "name" : "query"
            },
            {
              "type" : "org.opensearch.index.similarity.ScriptedSimilarity$Field",
              "name" : "field"
            },
            {
              "type" : "org.opensearch.index.similarity.ScriptedSimilarity$Term",
              "name" : "term"
            },
            {
              "type" : "org.opensearch.index.similarity.ScriptedSimilarity$Doc",
              "name" : "doc"
            }
          ]
        }
      ]
    },
    {
      "name" : "similarity_weight",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "double",
          "params" : [
            {
              "type" : "org.opensearch.index.similarity.ScriptedSimilarity$Query",
              "name" : "query"
            },
            {
              "type" : "org.opensearch.index.similarity.ScriptedSimilarity$Field",
              "name" : "field"
            },
            {
              "type" : "org.opensearch.index.similarity.ScriptedSimilarity$Term",
              "name" : "term"
            }
          ]
        }
      ]
    },
    {
      "name" : "string_sort",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "java.lang.String",
          "params" : [ ]
        },
        {
          "name" : "getDoc",
          "return_type" : "java.util.Map",
          "params" : [ ]
        },
        {
          "name" : "getParams",
          "return_type" : "java.util.Map",
          "params" : [ ]
        },
        {
          "name" : "get_score",
          "return_type" : "double",
          "params" : [ ]
        }
      ]
    },
    {
      "name" : "template",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "java.lang.String",
          "params" : [ ]
        },
        {
          "name" : "getParams",
          "return_type" : "java.util.Map",
          "params" : [ ]
        }
      ]
    },
    {
      "name" : "terms_set",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "java.lang.Number",
          "params" : [ ]
        },
        {
          "name" : "getDoc",
          "return_type" : "java.util.Map",
          "params" : [ ]
        },
        {
          "name" : "getParams",
          "return_type" : "java.util.Map",
          "params" : [ ]
        }
      ]
    },
    {
      "name" : "trigger",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "boolean",
          "params" : [
            {
              "type" : "org.opensearch.alerting.script.QueryLevelTriggerExecutionContext",
              "name" : "ctx"
            }
          ]
        },
        {
          "name" : "getParams",
          "return_type" : "java.util.Map",
          "params" : [ ]
        }
      ]
    },
    {
      "name" : "update",
      "methods" : [
        {
          "name" : "execute",
          "return_type" : "void",
          "params" : [ ]
        },
        {
          "name" : "getCtx",
          "return_type" : "java.util.Map",
          "params" : [ ]
        },
        {
          "name" : "getParams",
          "return_type" : "java.util.Map",
          "params" : [ ]
        }
      ]
    }
  ]
}
````

## 回應本文欄位

`GET _script_context` 請求會傳回下列回應欄位：

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `contexts` | 清單 | 所有情境的清單。請參閱[指令碼物件](#script-context)。  |

#### 指令碼情境

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `name` | 字串 | 情境名稱。 |
| `methods` | 清單 | 情境允許使用的方法清單。請參閱[指令碼物件](#context-methods)。 |

#### 情境方法

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `name` | 字串 | 方法名稱。 |
| `name` | 字串 | 方法傳回的類型（`boolean`、`object`、`number` 等）。 |
| `params` | 清單 | 方法接受的參數清單。請參閱[指令碼物件](#method-parameters)。 |

#### 方法參數 

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `type` | 字串 | 參數資料類型。 | 
| `name` | 字串 | 參數名稱。 |