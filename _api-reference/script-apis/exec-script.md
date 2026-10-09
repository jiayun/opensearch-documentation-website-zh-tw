---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "執行行內指令碼"
parent: Script APIs
nav_order: 7
---

# Execute Inline Script API
**於 1.0 版推出**
{: .label .label-purple }

Execute Inline Script API 可讓您直接執行指令碼，無須將其儲存在叢集狀態中。每次呼叫此 API 時，都會編譯並執行指令碼。如需詳細資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

## 端點

```json
GET /_scripts/painless/_execute
POST /_scripts/painless/_execute
```

## 請求本文欄位

| 欄位 | 說明 | 
:--- | :---
| `script` | 要執行的指令碼。必要 |
| `context` | 指令碼的執行環境。選用。預設為 `painless_test`。 |
| `context_setup` | 指定執行環境的其他參數。選用。 | 

## 請求範例
<!-- spec_insert_start
component: example_code
rest: POST /_scripts/painless/_execute
body: |
{
  "script": {
    "source": "doc['gpa_4_0'].value * params.max_gpa / 4.0",
    "params": {
      "max_gpa": 5.0
    }
  },
  "context": "score",
  "context_setup": {
    "index": "testindex1",
    "document": {
      "gpa_4_0": 3.5
    }
  }
}
-->
{% capture step1_rest %}
POST /_scripts/painless/_execute
{
  "script": {
    "source": "doc['gpa_4_0'].value * params.max_gpa / 4.0",
    "params": {
      "max_gpa": 5.0
    }
  },
  "context": "score",
  "context_setup": {
    "index": "testindex1",
    "document": {
      "gpa_4_0": 3.5
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.put_script(
  id = "painless",
  context = "_execute",
  body =   {
    "script": {
      "source": "doc['gpa_4_0'].value * params.max_gpa / 4.0",
      "params": {
        "max_gpa": 5.0
      }
    },
    "context": "score",
    "context_setup": {
      "index": "testindex1",
      "document": {
        "gpa_4_0": 3.5
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

下列請求使用指令碼的預設 `painless_context`：

<!-- spec_insert_start
component: example_code
rest: GET /_scripts/painless/_execute
body: |
{
  "script": {
    "source": "(params.x + params.y)/ 2",
    "params": {
      "x": 80,
      "y": 100
    }
  }
}
-->
{% capture step1_rest %}
GET /_scripts/painless/_execute
{
  "script": {
    "source": "(params.x + params.y)/ 2",
    "params": {
      "x": 80,
      "y": 100
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.scripts_painless_execute(
  body =   {
    "script": {
      "source": "(params.x + params.y)/ 2",
      "params": {
        "x": 80,
        "y": 100
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

回應包含兩個指令碼參數的平均值：

```json
{
  "result" : "90"
}
```

## 回應本文欄位

| 欄位 | 說明 | 
:--- | :--- 
| `result` | 指令碼結果。 |


## 指令碼執行環境

選擇不同的執行環境，以控制指令碼可使用的變數，以及結果的回傳類型。預設執行環境為 `painless_test`。

## Painless 測試執行環境

`painless_test` 執行環境是預設的指令碼執行環境，僅提供 `params` 變數給指令碼。回傳的結果一律會轉換為字串。如需使用範例，請參閱前面的請求範例。

## 篩選執行環境

`filter` 執行環境會執行指令碼，就如同指令碼位於指令碼查詢中一樣。您必須在執行環境中提供測試文件。指令碼可使用 `_source`、儲存欄位及 `_doc` 變數。

您可以在 `context_setup` 中為篩選執行環境指定下列參數。

參數 | 說明
:--- | :---
`document` | 暫時在記憶體中編製索引且可供指令碼使用的文件。
`index` | 包含該文件對應的索引名稱。

例如，先建立具有測試文件對應的索引：

```json
PUT /testindex1
{
  "mappings": {
    "properties": {
      "grad": {
        "type": "boolean"
      },
      "gpa": {
        "type": "float"
      }
    }
  }
}
```
{% include copy-curl.html %}

執行指令碼，判斷學生是否符合以優異成績畢業的資格：

<!-- spec_insert_start
component: example_code
rest: POST /_scripts/painless/_execute
body: |
{
  "script": {
    "source": "doc['grad'].value == true && doc['gpa'].value >= params.min_honors_gpa",
    "params": {
      "min_honors_gpa": 3.5
    }
  },
  "context": "filter",
  "context_setup": {
    "index": "testindex1",
    "document": {
      "grad": true,
      "gpa": 3.79
    }
  }
}
-->
{% capture step1_rest %}
POST /_scripts/painless/_execute
{
  "script": {
    "source": "doc['grad'].value == true && doc['gpa'].value >= params.min_honors_gpa",
    "params": {
      "min_honors_gpa": 3.5
    }
  },
  "context": "filter",
  "context_setup": {
    "index": "testindex1",
    "document": {
      "grad": true,
      "gpa": 3.79
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.put_script(
  id = "painless",
  context = "_execute",
  body =   {
    "script": {
      "source": "doc['grad'].value == true && doc['gpa'].value >= params.min_honors_gpa",
      "params": {
        "min_honors_gpa": 3.5
      }
    },
    "context": "filter",
    "context_setup": {
      "index": "testindex1",
      "document": {
        "grad": true,
        "gpa": 3.79
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應包含結果：

```json
{
  "result" : true
}
```

## 評分執行環境

`score` 執行環境會執行指令碼，就如同指令碼位於 `function_score` 查詢中的 `script_score` 函式內一樣。

您可以在 `context_setup` 中為評分執行環境指定下列參數。

參數 | 說明
:--- | :---
`document` | 暫時在記憶體中編製索引且可供指令碼使用的文件。
`index` | 包含該文件對應的索引名稱。
`query` | 如果指令碼使用 `_score` 參數，查詢可以指定使用 `_score` 欄位來計算分數。

例如，先建立具有測試文件對應的索引：

```json
PUT /testindex1
{
  "mappings": {
    "properties": {
      "gpa_4_0": {
        "type": "float"
      }
    }
  }
}
```
{% include copy-curl.html %}

執行指令碼，將採用 4.0 分制的 GPA 轉換為透過參數提供的另一種分制：

<!-- spec_insert_start
component: example_code
rest: POST /_scripts/painless/_execute
body: |
{
  "script": {
    "source": "doc['gpa_4_0'].value * params.max_gpa / 4.0",
    "params": {
      "max_gpa": 5.0
    }
  },
  "context": "score",
  "context_setup": {
    "index": "testindex1",
    "document": {
      "gpa_4_0": 3.5
    }
  }
}
-->
{% capture step1_rest %}
POST /_scripts/painless/_execute
{
  "script": {
    "source": "doc['gpa_4_0'].value * params.max_gpa / 4.0",
    "params": {
      "max_gpa": 5.0
    }
  },
  "context": "score",
  "context_setup": {
    "index": "testindex1",
    "document": {
      "gpa_4_0": 3.5
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.put_script(
  id = "painless",
  context = "_execute",
  body =   {
    "script": {
      "source": "doc['gpa_4_0'].value * params.max_gpa / 4.0",
      "params": {
        "max_gpa": 5.0
      }
    },
    "context": "score",
    "context_setup": {
      "index": "testindex1",
      "document": {
        "gpa_4_0": 3.5
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應包含結果：

```json
{
  "result" : 4.375
}
```