---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "List Index 工具"
has_children: false
has_toc: false
nav_order: 35
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# List Index 工具
**3.0 版新增**
{: .label .label-purple }
<!-- vale on -->

`ListIndexTool` 會擷取 OpenSearch 叢集的索引資訊，類似於 [List Indices API]({{site.url}}{{site.baseurl}}/api-reference/list/list-indices/)。

從 OpenSearch 3.0 版開始，`ListIndexTool` 取代了 `CatIndexTool`。
{: .note}

## 步驟 1：註冊將執行 ListIndexTool 的流程代理程式

流程代理程式會依序執行一連串工具，並傳回最後一個工具的輸出。若要建立流程代理程式，請傳送下列註冊代理程式請求：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Test_Agent_For_ListIndex_tool",
  "type": "flow",
  "description": "this is a test agent for the ListIndexTool",
  "tools": [
    {
      "type": "ListIndexTool",
      "name": "DemoListIndexTool",
      "parameters": {
        "input": "${parameters.question}"
      }
    }
  ]
}
```
{% include copy-curl.html %} 

參數說明請參閱 [Register parameters](#register-parameters)。

OpenSearch 會回應代理程式 ID：

```json
{
  "agent_id": "9X7xWI0Bpc3sThaJdY9i"
}
```

## 步驟 2：執行代理程式

在執行代理程式之前，請確認您已新增 OpenSearch Dashboards 的 `Sample eCommerce orders` 範例資料集。若要了解更多，請參閱 [Adding sample data]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。

接著，傳送下列請求來執行代理程式：

```json
POST /_plugins/_ml/agents/9X7xWI0Bpc3sThaJdY9i/_execute
{
  "parameters": {
    "question": "How many indices do I have?"
  }
}
```
{% include copy-curl.html %} 

OpenSearch 會傳回索引資訊：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": """health    status    index    uuid    pri    rep    docs.count    docs.deleted    store.size    pri.store.size
green    open    .plugins-ml-model-group    lHgGEgJhT_mpADyOZoXl2g    1    1    9    2    33.4kb    16.7kb
green    open    .plugins-ml-memory-meta    b2LEpv0QS8K60QBjXtRm6g    1    1    13    0    95.1kb    47.5kb
green    open    .ql-datasources    9NXm_tMXQc6s_4uRToSNkQ    1    1    0    0    416b    208b
green    open    sample-ecommerce    UPYOQcAfRGqFAlSxcZlRjw    1    1    40320    0    4.1mb    2mb
green    open    .plugins-ml-task    xYTlprYCQnaaYici69SOjA    1    1    117    0    115.5kb    57.6kb
green    open    .opendistro_security    7DAqhm9QQmeEsQYhA40cJg    1    1    10    0    117kb    58.5kb
green    open    sample-host-health    Na5tq6UiTt6r_qYME1vV-w    1    1    40320    0    2.6mb    1.3mb
green    open    .opensearch-observability    6PthtLluSKyYCdZR3Mw0iw    1    1    0    0    416b    208b
green    open    .plugins-ml-model    WYcjBHcnRuSDHeVWPVupoA    1    1    191    45    4.2gb    2.1gb
green    open    index_for_neural_sparse    GQswGabQRIazM_trnqaDrw    1    1    5    0    28.4kb    14.2kb
green    open    security-auditlog-2024.01.30    BhXR7Nd3QVOVGxJNpR0-jw    1    1    27768    0    13.8mb    7mb
green    open    sample-http-responses    0gmYYYdOTiCbVUvl_uDL0w    1    1    40320    0    2.5mb    1.2mb
green    open    security-auditlog-2024.02.01    2VD1ieDGS5m-TfjIdfT8Eg    1    1    39305    0    39mb    18.6mb
green    open    opensearch_dashboards_sample_data_ecommerce    wnE6r7OvSPqc5YHj8wHSLA    1    1    4675    0    8.8mb    4.4mb
green    open    security-auditlog-2024.01.31    cNRK5-2eTwes0SRlXTl0RQ    1    1    34520    0    20.5mb    9.8mb
green    open    .plugins-ml-memory-message    wTNBU4BBQVSFcFhNlUdfBQ    1    1    93    0    358.2kb    181.9kb
green    open    .plugins-flow-framework-state    dJUNDv9MSJ2jjwKbzXPlrw    1    1    39    0    114.1kb    57kb
green    open    .plugins-ml-agent    7X1IzoLuSGmIujOh9i5mmg    1    1    30    0    170.7kb    85.3kb
green    open    .plugins-flow-framework-templates    _ecC0KahTlmG_3tFUst7Uw    1    1    18    0    175.8kb    87.9kb
green    open    .plugins-ml-connector    q45iJfVjQ5KgxeNC65DLSw    1    1    11    0    313.1kb    156.5kb
green    open    .kibana_1    vRjXK4bHSUueB_4iXiQ8yw    1    1    257    0    264kb    132kb
green    open    .plugins-ml-config    G7gxGQB7TZeQzBasHd5PUg    1    1    1    0    7.8kb    3.9kb
green    open    .plugins-ml-controller    NQTZPREZRhWoDdjCglRLFg    1    1    0    0    50.1kb    49.9kb
green    open    opensearch_dashboards_sample_data_logs    9gpOTB3rRgqBLvqis_k5LQ    1    1    14074    0    18mb    9mb
green    open    .plugins-flow-framework-config    JlKPsCh6SEq-Jh6rPL_x9Q    1    1    1    0    7.8kb    3.9kb
green    open    opensearch_dashboards_sample_data_flights    pJde0irnTce4-uobHwYmMQ    1    1    13059    0    11.9mb    5.9mb
green    open    my_test_data    T4hwNs7CTJGIfw2QpCqQ_Q    1    1    6    0    91.7kb    45.8kb
green    open    .opendistro-job-scheduler-lock    XjgmXAVKQ4e8Y-ac54VBzg    1    1    3    3    36.2kb    21.3kb
"""
        }
      ]
    }
  ]
}
```

## 註冊參數

下表列出註冊代理程式時可用的所有工具參數。

<!-- vale off -->
參數 | 類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`indices` | 字串 | 選用 | 以逗號分隔的一或多個索引清單，用於執行列出索引操作。預設為空清單，表示所有索引。
`local` | 布林值 | 選用 | 當為 `true` 時，僅從本機節點擷取資訊，而不是從叢集管理員節點擷取。預設為 `false`。
`page_size` | 整數 | 選用 | 指定使用 List Indices API 時每頁傳回的索引結果數量。此 API 以分頁方式擷取索引狀態。預設為 `100`。
<!-- vale on -->

## 執行參數

下表列出執行代理程式時可用的所有工具參數。

參數	| 類型 | 必要/選用 | 說明	
:--- | :--- | :--- | :---
`question` | 字串 | 必要 | 要傳送給 LLM 的自然語言問題。

## 測試工具

您可以將此工具作為代理程式工作流程的一部分執行，也可以使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適用於測試個別工具或執行獨立操作。