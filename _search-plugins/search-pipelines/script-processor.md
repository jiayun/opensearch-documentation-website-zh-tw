---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指令碼"
nav_order: 120
has_children: false
parent: User-defined search processors
grand_parent: Search pipelines
---

# 指令碼搜尋處理器
於 2.8 版推出
{: .label .label-purple }

`script` 搜尋請求處理器會攔截搜尋請求，並加入在傳入請求上執行的內嵌 [Painless]({{site.url}}{{site.baseurl}}/scripting/painless/) 指令碼。此指令碼只能對下列請求欄位執行：

- `from` 
- `size` 
- `explain` 
- `version` 
- `seq_no_primary_term` 
- `track_scores`  
- `track_total_hits` 
- `min_score` 
- `terminate_after` 
- `profile` 

如需請求欄位的定義，請參閱[搜尋請求欄位]({{site.url}}{{site.baseurl}}/api-reference/search#request-body)。

## 請求本文欄位

下表列出所有可用的請求欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`source` | 內嵌指令碼 | 要執行的指令碼。必要。
`lang` | 字串 | 指令碼語言。選用。僅支援 `painless`。
`tag` | 字串 | 處理器的識別碼。選用。
`description` | 字串 | 處理器的說明。選用。
`ignore_failure` | 布林值 | 若為 `true`，OpenSearch 會[忽略此處理器的任何失敗]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/creating-search-pipeline/#ignoring-processor-failures)，並繼續執行搜尋管線中的其餘處理器。選用。預設為 `false`。

## 範例 

下列請求會建立包含 `script` 請求處理器的搜尋管線。此指令碼將分數解釋限制為僅針對一份文件，因為 `explain` 是一項耗費資源的作業：

```json
PUT /_search/pipeline/explain_one_result
{
  "description": "A pipeline to limit the explain operation to one result only",
  "request_processors": [
    {
      "script": {
        "lang": "painless",
        "source": "if (ctx._source['size'] > 1) { ctx._source['explain'] = false } else { ctx._source['explain'] = true }"
      }
    }
  ]
} 
```
{% include copy-curl.html %}
