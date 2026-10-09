---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "監控"
nav_order: 95
redirect_from:
  - /search-plugins/sql/monitoring/
---

# SQL 與 PPL 監控

OpenSearch 提供一個 stats 端點，會在設定的間隔內收集 SQL 與 PPL 查詢處理的指標。統計資料是在節點層級收集，因此您只會收到您正在存取之節點的指標。

## 節點統計

回應包含下列欄位。

|                 欄位名稱|                                                    說明|
| ------------------------- | ------------------------------------------------------------- |
|              `request_total`|                                         請求總數。|
|              `request_count`|                     間隔內的請求總數。|
|`failed_request_count_syserr`|間隔內因系統錯誤而失敗的請求數量。|
|`failed_request_count_cuserr`| 間隔內因錯誤請求而失敗的請求數量。|
|    `failed_request_count_cb`| 表示外掛程式在間隔內是否觸發斷路器。|


### 範例

SQL 查詢：

```console
>> curl -H 'Content-Type: application/json' -X GET localhost:9200/_plugins/_sql/stats
```
{% include copy.html %}


查詢會傳回下列結果：

```json
{
  "failed_request_count_cb": 0,
  "failed_request_count_cuserr": 0,
  "circuit_breaker": 0,
  "request_total": 0,
  "request_count": 0,
  "failed_request_count_syserr": 0
}
```
