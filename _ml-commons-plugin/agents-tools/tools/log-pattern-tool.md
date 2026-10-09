---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Log Pattern 工具"
has_children: false
has_toc: false
nav_order: 37
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# Log Pattern 工具
**2.19 版引入**
{: .label .label-purple }
<!-- vale on -->

`LogPatternTool` 會分析透過[查詢特定領域語言 (DSL)]({{site.url}}{{site.baseurl}}/query-dsl/) 或[管道處理語言 (PPL)]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/) 查詢所擷取的記錄資料，以擷取並識別記錄訊息中反覆出現的結構模式。此工具會依據共用範本將相似的記錄分組，然後傳回最常見的模式。每個模式都包含具代表性的範例記錄，以及資料集中符合該模式的記錄項目總數。

OpenSearch 會根據請求中是否存在 `input` 或 `ppl` 參數，判斷您使用的是 DSL 還是 PPL 查詢：

- 如果存在 `input` 參數 (以字串表示的 DSL 查詢 JSON)，工具會將請求解讀為 DSL 查詢。

- 如果存在 `ppl` 參數而不存在 `input`，工具會將請求解讀為 PPL 查詢。

- 如果兩者都有提供，工具會優先使用 DSL 查詢。

為避免混淆，執行代理程式時，請在請求中只提供兩者之一：DSL 使用 `input`，PPL 使用 `ppl`。

## 步驟 1：註冊將執行 LogPatternTool 的流程代理程式

流程代理程式會依序執行一系列工具，並傳回最後一個工具的輸出。若要建立流程代理程式，請傳送下列註冊代理程式請求：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_Log_Pattern_Tool",
  "type": "flow",
  "description": "this is a test agent for the LogPatternTool",
  "memory": {
    "type": "demo"
  },
  "tools": [
      {
      "type": "LogPatternTool",
      "parameters": {
        "sample_log_size": 1
      }
    }
  ]
}
```
{% include copy-curl.html %}

如需參數說明，請參閱[註冊參數](#register-parameters)。

OpenSearch 會以代理程式 ID 回應：

```json
{
  "agent_id": "OQutgJYBAc35E4_KvI1q"
}
```

## 步驟 2：執行代理程式

傳送下列請求以執行代理程式：

```json
POST /_plugins/_ml/agents/OQutgJYBAc35E4_KvI1q/_execute
{
  "parameters": {
    "input": "{\"query\":{\"bool\":{\"filter\":[{\"range\":{\"bytes\":{\"from\":10,\"to\":null,\"include_lower\":true,\"include_upper\":true,\"boost\":1}}}],\"adjust_pure_negative\":true,\"boost\":1}}}",
    "index": "opensearch_dashboards_sample_data_logs"
  }
}
```
{% include copy-curl.html %}

OpenSearch 會傳回 JSON 回應，其中包含在您的資料中找到的最常見記錄模式，數量最多為指定的上限。每個識別出的模式都以 JSON 物件表示，包含三個關鍵元件：模式範本、一組符合該模式的代表性範例記錄，以及表示該模式在資料集中出現頻率的計數。其結構遵循 `{"pattern": "...", "sample logs": [...], "total count": N}` 格式，如下列範例回應所示：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result":"""[{"pattern":"<*IP*> - - [<*DATETIME*>] "GET <*> HTTP/<*><*>\" 200 <*> \"-\" \"Mozilla/<*><*> (<*>; Linux <*>_<*>; rv:<*><*><*>) Gecko/<*> Firefox/<*><*><*>\"","sample logs":["223.87.60.27 - - [2018-07-22T00:39:02.912Z] \"GET /opensearch/opensearch-1.0.0.deb_1 HTTP/1.1\" 200 6219 \"-\" \"Mozilla/5.0 (X11; Linux x86_64; rv:6.0a1) Gecko/20110421 Firefox/6.0a1\""],"total count":367},{"pattern":"<*IP*> - - [<*DATETIME*>] \"GET <*> HTTP/<*><*>\" 200 <*> \"-\" \"Mozilla/<*><*> (<*>; Linux <*>) AppleWebKit/<*><*> (KHTML like Gecko) Chrome<*IP*> Safari/<*><*>\"","sample logs":["216.9.22.134 - - [2018-07-22T05:27:11.939Z] \"GET /beats/metricbeat_1 HTTP/1.1\" 200 3629 \"-\" \"Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.50 Safari/534.24\""],"total count":311},{"pattern":"<*IP*> - - [<*DATETIME*>] \"GET <*> HTTP/<*><*>\" 200 <*> \"-\" \"Mozilla/<*><*> (compatible; MSIE 6<*>; Windows NT 5<*>; <*>; .NET CLR 1<*><*>)\"","sample logs":["99.74.118.237 - - [2018-07-22T03:34:43.399Z] \"GET /beats/metricbeat/metricbeat-6.3.2-amd64.deb_1 HTTP/1.1\" 200 14113 \"-\" \"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)\""],"total count":269}]"""
        }
      ]
    }
  ]
}
```

## 註冊參數

下表列出註冊代理程式時可用的工具參數。

| 參數         | 類型     | 必要/選用                                | 說明 |
|:-----------------|:---------|:-------------------------------------------------|:------------|
| `index`          | 字串   | DSL 查詢必要                         | 要搜尋以進行模式分析的索引。 |
| `input`          | 字串   | DSL 查詢必要                         | 以字串表示的 DSL 查詢 JSON。如果同時提供 `input` 和 `ppl`，則會使用 `input` (DSL)。 |
| `ppl`            | 字串   | PPL 查詢必要                         | PPL 查詢字串。如果也提供了 `input`，則會忽略此參數。 |
| `source_field`   | 字串   | 選用                                         | 要在結果中傳回的欄位。可以是單一欄位或陣列 (例如 `["field1", "field2"]`)。 |
| `doc_size`       | 整數  | 選用                                         | 要擷取的文件數量。預設為 `2`。 |
| `top_n_pattern`  | 整數  | 選用                                         | 將輸出限制為指定數量的最常見模式。預設為 `3`。 |
| `sample_log_size`| 整數  | 選用                                         | 每個模式要包含的範例記錄數量。預設為 `20`。 |
| `pattern_field`  | 字串   | 選用                                         | 要分析以偵測模式的欄位。如果未指定，工具會從第一份文件中選取最長的文字欄位。 |


## 執行參數

下表列出執行代理程式時可用的工具參數。

參數	| 類型 | 必要/選用      | 說明	
:--- | :--- |:-----------------------| :---
| `index`   | 字串 | DSL 查詢必要 | 要搜尋以進行模式分析的索引。 |
| `input`   | 字串 | DSL 查詢必要 | 以字串表示的 DSL 查詢 JSON。如果同時提供 `input` 和 `ppl`，則以 `input` (DSL) 為優先。 |
| `ppl`     | 字串 | PPL 查詢必要 | PPL 查詢字串。如果也提供了 `input`，則會忽略此參數。 |

## 測試工具

您可以將此工具作為代理程式工作流程的一部分執行，也可以使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 單獨執行。Execute Tool API 適合用來測試個別工具或執行獨立作業。