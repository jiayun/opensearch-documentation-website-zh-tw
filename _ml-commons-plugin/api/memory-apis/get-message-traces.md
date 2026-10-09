---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得訊息追蹤"
parent: Memory APIs
grand_parent: ML Commons APIs
nav_order: 70
---

# Get Message Traces API
**2.12 版推出**
{: .label .label-purple }

使用此 API 擷取[對話式搜尋]({{site.url}}{{site.baseurl}}/search-plugins/conversational-search/)的訊息追蹤資訊。這對偵錯很有幫助。

對於每則訊息，代理程式可能需要執行不同的工具。您可以使用 Get Traces API 取得某則訊息的所有追蹤資料。追蹤資料包含訊息執行的詳細步驟。

啟用 Security 外掛程式時，所有記憶都存在於 `private` 安全性模式中。只有建立記憶的使用者才能與該記憶及其訊息互動。
{: .important}


## 端點

```json
GET /_plugins/_ml/memory/message/{message_id}/traces
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`message_id` | 字串 | 要追蹤的訊息 ID。

## 回應本文欄位

下表列出可用的回應欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `memory_id` | 字串 | 記憶 ID。 |
| `message_id` | 字串 | 訊息 ID。 |
| `create_time` | 字串 | 訊息的建立時間。 |
| `updated_time` | 字串 | 訊息的最後更新時間。 |
| `input` | 字串 | 訊息中的問題（人類輸入）。 |
| `prompt_template` | 字串 | 訊息所使用的提示範本。 |
| `response` | 字串 | 問題的答案（生成式 AI 輸出）。 |
| `origin` | 字串 | 產生回應的 AI 或其他系統名稱。 |
| `additional_info` | 物件 | 傳送至 `origin` 的任何其他資訊。 |
| `parent_message_id` | 字串 | 父訊息的 ID（適用於追蹤訊息）。 |
| `trace_number` | 整數 | 追蹤編號（適用於追蹤訊息）。 |

## 範例請求

```json
GET /_plugins/_ml/memory/message/TAuCZY0BT2tRrkdmCPqZ/traces
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "traces": [
    {
      "memory_id": "7Qt4ZY0BT2tRrkdmSPlo",
      "message_id": "TQuCZY0BT2tRrkdmEvpp",
      "create_time": "2024-02-01T16:30:39.719968032Z",
      "updated_time": "2024-02-01T16:30:39.719968032Z",
      "input": "Which index has most documents",
      "prompt_template": null,
      "response": "Let me check the document counts of each index",
      "origin": null,
      "additional_info": {},
      "parent_message_id": "TAuCZY0BT2tRrkdmCPqZ",
      "trace_number": 1
    },
    {
      "memory_id": "7Qt4ZY0BT2tRrkdmSPlo",
      "message_id": "TguCZY0BT2tRrkdmEvp7",
      "create_time": "2024-02-01T16:30:39.732979687Z",
      "updated_time": "2024-02-01T16:30:39.732979687Z",
      "input": "",
      "prompt_template": null,
      "response": """health    status    index    uuid    pri    rep    docs.count    docs.deleted    store.size    pri.store.size
green    open    .plugins-ml-model-group    lHgGEgJhT_mpADyOZoXl2g    1    1    9    2    33.4kb    16.7kb
green    open    .plugins-ml-memory-meta    b2LEpv0QS8K60QBjXtRm6g    1    1    13    0    117.5kb    58.7kb
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
green    open    security-auditlog-2024.02.01    2VD1ieDGS5m-TfjIdfT8Eg    1    1    36386    0    37mb    18.2mb
green    open    opensearch_dashboards_sample_data_ecommerce    wnE6r7OvSPqc5YHj8wHSLA    1    1    4675    0    8.8mb    4.4mb
green    open    security-auditlog-2024.01.31    cNRK5-2eTwes0SRlXTl0RQ    1    1    34520    0    20.5mb    9.8mb
green    open    .plugins-ml-memory-message    wTNBU4BBQVSFcFhNlUdfBQ    1    1    88    1    399.7kb    205kb
green    open    .plugins-flow-framework-state    dJUNDv9MSJ2jjwKbzXPlrw    1    1    39    0    114.1kb    57kb
green    open    .plugins-ml-agent    7X1IzoLuSGmIujOh9i5mmg    1    1    27    0    146.6kb    73.3kb
green    open    .plugins-flow-framework-templates    _ecC0KahTlmG_3tFUst7Uw    1    1    18    0    175.8kb    87.9kb
green    open    .plugins-ml-connector    q45iJfVjQ5KgxeNC65DLSw    1    1    11    0    313.1kb    156.5kb
green    open    .kibana_1    vRjXK4bHSUueB_4iXiQ8yw    1    1    257    0    264kb    132kb
green    open    .plugins-ml-config    G7gxGQB7TZeQzBasHd5PUg    1    1    1    0    7.8kb    3.9kb
green    open    .plugins-ml-controller    NQTZPREZRhWoDdjCglRLFg    1    1    0    0    50.1kb    49.9kb
green    open    opensearch_dashboards_sample_data_logs    9gpOTB3rRgqBLvqis_k5LQ    1    1    14074    0    18mb    9mb
green    open    .plugins-flow-framework-config    JlKPsCh6SEq-Jh6rPL_x9Q    1    1    1    0    7.8kb    3.9kb
green    open    opensearch_dashboards_sample_data_flights    pJde0irnTce4-uobHwYmMQ    1    1    13059    0    11.9mb    5.9mb
green    open    my_test_data    T4hwNs7CTJGIfw2QpCqQ_Q    1    1    6    0    91.7kb    45.8kb
green    open    .opendistro-job-scheduler-lock    XjgmXAVKQ4e8Y-ac54VBzg    1    1    3    0    38.7kb    19.4kb
""",
      "origin": "ListIndexTool",
      "additional_info": {},
      "parent_message_id": "TAuCZY0BT2tRrkdmCPqZ",
      "trace_number": 2
    },
    {
      "memory_id": "7Qt4ZY0BT2tRrkdmSPlo",
      "message_id": "UwuCZY0BT2tRrkdmHPos",
      "create_time": "2024-02-01T16:30:42.217897656Z",
      "updated_time": "2024-02-01T16:30:42.217897656Z",
      "input": "Which index has most documents",
      "prompt_template": null,
      "response": "Based on the cluster health information provided, the index with the most documents is .plugins-ml-model with 191 documents",
      "origin": null,
      "additional_info": {},
      "parent_message_id": "TAuCZY0BT2tRrkdmCPqZ",
      "trace_number": 3
    },
    {
      "memory_id": "7Qt4ZY0BT2tRrkdmSPlo",
      "message_id": "UQuCZY0BT2tRrkdmHPos",
      "create_time": "2024-02-01T16:30:42.218120716Z",
      "updated_time": "2024-02-01T16:30:42.218120716Z",
      "input": "Which index has most documents",
      "prompt_template": null,
      "response": "The index with the most documents is the .plugins-ml-model index, which contains 191 documents based on the cluster health information provided.",
      "origin": null,
      "additional_info": {},
      "parent_message_id": "TAuCZY0BT2tRrkdmCPqZ",
      "trace_number": 4
    },
    {
      "memory_id": "7Qt4ZY0BT2tRrkdmSPlo",
      "message_id": "UguCZY0BT2tRrkdmHPos",
      "create_time": "2024-02-01T16:30:42.218240713Z",
      "updated_time": "2024-02-01T16:30:42.218240713Z",
      "input": "Which index has most documents",
      "prompt_template": null,
      "response": "The index with the most documents is the .plugins-ml-model index, which contains 191 documents based on the cluster health information provided.",
      "origin": null,
      "additional_info": {},
      "parent_message_id": "TAuCZY0BT2tRrkdmCPqZ",
      "trace_number": 5
    }
  ]
}
```