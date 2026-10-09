---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "監控搜尋品質"
nav_order: 70
parent: Search Relevance Workbench
grand_parent: Optimizing search quality
has_children: false
---

# 監控搜尋品質
**於 3.4 版推出**
{: .label .label-purple }

搜尋品質並非一成不變。即使您的排名演算法維持不變，已編製索引的資料仍會持續演進，諸如熱門程度與新近程度等訊號會有所波動，使用者的查詢也會隨時間改變。

為了偵測並避免相關性出現非預期的變化，您應該持續監控搜尋品質。您可以設定 cron 排程，定期執行搜尋評估實驗。


每個作業只能有一個排程。若要修改排程，請刪除現有排程並建立新的排程。刪除排程也會一併移除其相關的歷史資料。

## 使用 Search Relevance Workbench 排定搜尋評估

在您首次成功執行搜尋評估後，會出現一個時鐘圖示，讓您排定該實驗，如下圖所示。

![排定實驗執行時間]({{site.url}}{{site.baseurl}}/images/search-relevance-workbench/experiment_scheduled_icon.png)

在排程頁面上，設定您希望實驗執行的頻率，如下圖所示。

![設定執行頻率的排程]({{site.url}}{{site.baseurl}}/images/search-relevance-workbench/experiment_scheduled_modal.png)

### 評估搜尋品質

排定實驗後，會出現一個新的儀表板圖示，讓您隨時間監控搜尋結果。由於儀表板每天評估結果，資料最多可能需要 24 小時才會填入並顯示有意義的洞察。

![隨時間檢視搜尋品質]({{site.url}}{{site.baseurl}}/images/search-relevance-workbench/experiment_scheduled_dashboard.png)


## 使用 API 排定搜尋評估

您可以使用 API 建立定期排定的實驗。您要排定的實驗必須已經存在。

### 端點

```json
POST _plugins/_search_relevance/experiments/schedule
```

### 請求本文欄位

下表列出可用的輸入參數。

欄位 | 資料類型 |  說明
:---  | :--- | :---
`experimentId` | 字串 | 要重新執行的實驗 ID。
`cronExpression` | 字串 | 以 UTC 執行評估的 cron 排程。

### 範例請求

下列請求會排定該實驗每天凌晨 1 點執行：

```json
POST _plugins/_search_relevance/experiments/schedule
{
  "experimentId": "6282afa6-fa14-49c8-a627-ac1d5204d357",
  "cronExpression": "0 1 * * *"
}
```
{% include copy-curl.html %}

## 管理已排定的實驗

您可以使用下列 API 擷取或刪除已排定的實驗。

### 擷取已排定的實驗

此 API 會擷取可用的已排定實驗。

#### 端點

```json
GET _plugins/_search_relevance/experiments/schedule
GET _plugins/_search_relevance/experiments/schedule/{experiment_id}
```

#### 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `experiment_id` | 字串 | 要擷取的已排定實驗 ID。若未提供，則擷取所有已排定的實驗。 |

#### 範例請求

```json
GET _plugins/_search_relevance/experiments/schedule/6282afa6-fa14-49c8-a627-ac1d5204d357
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "took": 17,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": null,
    "hits": [
      {
        "_index": ".search-relevance-scheduled-experiment-jobs",
        "_id": "6282afa6-fa14-49c8-a627-ac1d5204d357",
        "_score": null,
        "_source": {
          "id": "6282afa6-fa14-49c8-a627-ac1d5204d357",
          "enabled": true,
          "schedule": {
            "cron": {
              "expression": "0 0 * * *",
              "timezone": "America/Los_Angeles"
            }
          },
          "enabledTime": 1758320475601,
          "lastUpdateTime": 1758320475601,
          "timestamp": "2025-09-19T00:00:00.602Z"
        },
        "sort": [
          "2025-09-19T00:00:00.602Z"
        ]
      }
    ]
  }
}
```

### 刪除已排定的實驗

您可以使用已排定的實驗 ID 刪除已排定的實驗。

#### 端點

```json
DELETE _plugins/_search_relevance/experiments/schedule/<experiment_id>
```

### 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `experiment_id` | 字串 | 要刪除的已排定實驗 ID。  |


#### 範例請求

```json
DELETE _plugins/_search_relevance/experiments/schedule/6282afa6-fa14-49c8-a627-ac1d5204d357
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "_index": ".search-relevance-scheduled-experiment-jobs",
  "_id": "6282afa6-fa14-49c8-a627-ac1d5204d357",
  "_version": 2,
  "result": "deleted",
  "forced_refresh": true,
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 17,
  "_primary_term": 1
}
```
