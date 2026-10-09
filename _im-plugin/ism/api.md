---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: ISM API
parent: Index State Management
nav_order: 30
---

# ISM API

使用 Index State Management (ISM) API 以程式設計方式管理政策與受管理的索引。

---

#### 目錄
- TOC
{:toc}


---


## 建立政策
**於 1.0 版推出**
{: .label .label-purple }

建立政策。

#### 端點

```json
PUT _plugins/_ism/policies/{policy_id}
```

#### 範例請求

```json
PUT _plugins/_ism/policies/policy_1
{
  "policy": {
    "description": "ingesting logs",
    "default_state": "ingest",
    "states": [
      {
        "name": "ingest",
        "actions": [
          {
            "rollover": {
              "min_doc_count": 5
            }
          }
        ],
        "transitions": [
          {
            "state_name": "search"
          }
        ]
      },
      {
        "name": "search",
        "actions": [],
        "transitions": [
          {
            "state_name": "delete",
            "conditions": {
              "min_index_age": "5m"
            }
          }
        ]
      },
      {
        "name": "delete",
        "actions": [
          {
            "delete": {}
          }
        ],
        "transitions": []
      }
    ]
  }
}
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "_id": "policy_1",
  "_version": 1,
  "_primary_term": 1,
  "_seq_no": 7,
  "policy": {
    "policy": {
      "policy_id": "policy_1",
      "description": "ingesting logs",
      "last_updated_time": 1577990761311,
      "schema_version": 1,
      "error_notification": null,
      "default_state": "ingest",
      "states": [
        {
          "name": "ingest",
          "actions": [
            {
              "retry": {
                "count": 3,
                "backoff": "exponential",
                "delay": "1m"
              },
              "rollover": {
                "min_doc_count": 5,
                "copy_alias": false
              }
            }
          ],
          "transitions": [
            {
              "state_name": "search"
            }
          ]
        },
        {
          "name": "search",
          "actions": [],
          "transitions": [
            {
              "state_name": "delete",
              "conditions": {
                "min_index_age": "5m"
              }
            }
          ]
        },
        {
          "name": "delete",
          "actions": [
            {
              "retry": {
                "count": 3,
                "backoff": "exponential",
                "delay": "1m"
              },
              "delete": {}
            }
          ],
          "transitions": []
        }
      ],
      "ism_template": null
    }
  }
}
```

回應會傳回由 ISM 填入預設值的政策，因此每個動作都會獲得一個 `retry` 物件，而每個操作都會獲得您未設定的參數。

---

## 新增政策
**於 1.0 版推出**
{: .label .label-purple }

將政策新增至索引。若要變更已有政策的索引之政策，請改用 [更新受管理索引政策](#update-managed-index-policy)。

#### 端點

```json
POST _plugins/_ism/add/{index}
```

#### 範例請求

先建立索引：

```json
PUT index_1
```
{% include copy-curl.html %}

然後將政策新增至索引：

```json
POST _plugins/_ism/add/index_1
{
  "policy_id": "policy_1"
}
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "updated_indices": 1,
  "failures": false,
  "failed_indices": []
}
```

對已有政策的索引新增政策並不會覆寫原有政策。請求會傳回 `200`，但該索引會出現在 `failed_indices` 中，且 `failures` 為 `true`：

```json
{
  "updated_indices": 0,
  "failures": true,
  "failed_indices": [
    {
      "index_name": "index_1",
      "index_uuid": "t6a6I5YDQTiXY9c7cymI_w",
      "reason": "This index already has a policy, use the update policy API to update index policies"
    }
  ]
}
```

如果您在為索引新增政策時使用萬用字元 `*`，ISM 外掛程式會將 `*` 解譯為所有索引，包括儲存使用者、角色與租用戶的系統索引 `.opendistro-security`。政策中的刪除動作可能會意外刪除叢集中的所有使用者角色與租用戶。
請勿使用過於寬泛的 `*` 萬用字元，而是在使用 `_ism/add` API 指定索引時加上前置詞，例如 `my-logs*`。
{: .warning }

---


## 更新政策
**於 1.0 版推出**
{: .label .label-purple }

更新政策。使用 `seq_no` 與 `primary_term` 參數來更新現有政策。如果這些數字與現有政策不符，或政策不存在，ISM 會擲回錯誤。

目前套用至您索引的政策可能不是最新的政策版本。若要檢視目前套用至索引的政策，請參閱 [說明索引]({{site.url}}{{site.baseurl}}/im-plugin/ism/api/#explain-index)。若要取得政策的最新版本，請參閱 [取得政策]({{site.url}}{{site.baseurl}}/im-plugin/ism/api/#get-policy)。

#### 端點

```json
PUT _plugins/_ism/policies/{policy_id}?if_seq_no={seq_no}&if_primary_term={primary_term}
```

#### 範例請求

```json
PUT _plugins/_ism/policies/policy_1?if_seq_no=7&if_primary_term=1
{
  "policy": {
    "description": "ingesting logs",
    "default_state": "ingest",
    "states": [
      {
        "name": "ingest",
        "actions": [
          {
            "rollover": {
              "min_doc_count": 5
            }
          }
        ],
        "transitions": [
          {
            "state_name": "search"
          }
        ]
      },
      {
        "name": "search",
        "actions": [],
        "transitions": [
          {
            "state_name": "delete",
            "conditions": {
              "min_index_age": "5m"
            }
          }
        ]
      },
      {
        "name": "delete",
        "actions": [
          {
            "delete": {}
          }
        ],
        "transitions": []
      }
    ]
  }
}
```
{% include copy-curl.html %}


#### 範例回應

```json
{
  "_id": "policy_1",
  "_version": 2,
  "_primary_term": 1,
  "_seq_no": 10,
  "policy": {
    "policy": {
      "policy_id": "policy_1",
      "description": "ingesting logs",
      "last_updated_time": 1577990934044,
      "schema_version": 1,
      "error_notification": null,
      "default_state": "ingest",
      "states": [
        {
          "name": "ingest",
          "actions": [
            {
              "retry": {
                "count": 3,
                "backoff": "exponential",
                "delay": "1m"
              },
              "rollover": {
                "min_doc_count": 5,
                "copy_alias": false
              }
            }
          ],
          "transitions": [
            {
              "state_name": "search"
            }
          ]
        },
        {
          "name": "search",
          "actions": [],
          "transitions": [
            {
              "state_name": "delete",
              "conditions": {
                "min_index_age": "5m"
              }
            }
          ]
        },
        {
          "name": "delete",
          "actions": [
            {
              "retry": {
                "count": 3,
                "backoff": "exponential",
                "delay": "1m"
              },
              "delete": {}
            }
          ],
          "transitions": []
        }
      ],
      "ism_template": null
    }
  }
}
```


---

## 取得政策
**於 1.0 版推出**
{: .label .label-purple }

依 `policy_id` 取得政策。

#### 端點

```json
GET _plugins/_ism/policies/{policy_id}
```

#### 範例請求

```json
GET _plugins/_ism/policies/policy_1
```
{% include copy-curl.html %}


#### 範例回應

```json
{
  "_id": "policy_1",
  "_version": 2,
  "_seq_no": 10,
  "_primary_term": 1,
  "policy": {
    "policy_id": "policy_1",
    "description": "ingesting logs",
    "last_updated_time": 1577990934044,
    "schema_version": 30,
    "error_notification": null,
    "default_state": "ingest",
    "states": [
      {
        "name": "ingest",
        "actions": [
          {
            "retry": {
              "count": 3,
              "backoff": "exponential",
              "delay": "1m"
            },
            "rollover": {
              "min_doc_count": 5,
              "copy_alias": false
            }
          }
        ],
        "transitions": [
          {
            "state_name": "search"
          }
        ]
      },
      {
        "name": "search",
        "actions": [],
        "transitions": [
          {
            "state_name": "delete",
            "conditions": {
              "min_index_age": "5m"
            }
          }
        ]
      },
      {
        "name": "delete",
        "actions": [
          {
            "retry": {
              "count": 3,
              "backoff": "exponential",
              "delay": "1m"
            },
            "delete": {}
          }
        ],
        "transitions": []
      }
    ],
    "ism_template": null
  }
}
```

---

## 取得多個政策
**於 1.0 版推出**
{: .label .label-purple }

取得政策清單。此 API 接受搜尋參數，以篩選及分頁結果。

#### 端點

```json
GET _plugins/_ism/policies
```

### 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `size` | 整數 | 要傳回的政策數量。 |
| `from` | 整數 | 分頁的起始位置。 |
| `sortField` | 字串 | 用來排序結果的欄位，以儲存之政策文件中的路徑表示，例如 `policy.policy_id.keyword` 或 `policy.last_updated_time`。未對應的名稱（例如 `policy_id`）會遭到拒絕，並傳回 `400`。 |
| `sortOrder` | 字串 | 結果的排序順序。有效值為 `asc`（遞增）及 `desc`（遞減）。 |
| `queryString` | 字串 | 用來依名稱或其他屬性篩選政策的查詢字串。請參閱 [查詢字串查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/)。|

#### 範例請求

```json
GET _plugins/_ism/policies
```
{% include copy-curl.html %}

#### 範例回應

每個項目都包含政策的序號及主要分片任期，但不包含其 `_version`。為精簡起見，下列回應省略了每個政策的 `states` 陣列：

```json
{
  "policies": [
    {
      "_id": "policy_1",
      "_seq_no": 10,
      "_primary_term": 1,
      "policy": {
        "policy_id": "policy_1",
        "description": "ingesting logs",
        "last_updated_time": 1577990934044,
        "schema_version": 30,
        "error_notification": null,
        "default_state": "ingest",
        "states": [],
        "ism_template": null
      }
    },
    {
      "_id": "policy_2",
      "_seq_no": 11,
      "_primary_term": 1,
      "policy": {
        "policy_id": "policy_2",
        "description": "ingesting logs",
        "last_updated_time": 1577990934042,
        "schema_version": 30,
        "error_notification": null,
        "default_state": "ingest",
        "states": [],
        "ism_template": null
      }
    }
  ],
  "total_policies": 2
}
```

---

## 從索引移除政策
**於 1.0 版推出**
{: .label .label-purple }

從索引移除任何 ISM 政策。

#### 端點

```json
POST _plugins/_ism/remove/{index}
```

#### 範例請求

```json
POST _plugins/_ism/remove/index_1
```
{% include copy-curl.html %}


#### 範例回應

```json
{
  "updated_indices": 1,
  "failures": false,
  "failed_indices": []
}
```

---

## 更新受管理索引政策
**於 1.0 版推出**
{: .label .label-purple }

將受管理索引政策更新為新政策（或政策的新版本）。您可以使用索引模式一次更新多個索引。更新多個索引時，您可能想加入狀態篩選條件，只影響特定的受管理索引。變更政策會篩選所有現有的受管理索引，並只將變更套用至您指定狀態中的索引。您也可以明確指定受管理索引在變更政策生效後要轉換到的狀態。

政策變更是一種非同步的背景程序。變更會排入佇列，不會立即由背景程序執行。此執行延遲可保護目前正在執行的受管理索引，避免其進入損毀狀態。如果您要變更成的政策只有一些小幅組態變更，則變更會立即生效。例如，如果政策將輪替條件中的 `min_index_age` 參數從 `1000d` 變更為 `100d`，此變更會在其下次執行時立即生效。如果變更修改了索引目前所在狀態的狀態、動作或動作順序，則變更會在目前狀態結束時發生，然後才轉換至新狀態。

在此範例中，套用於 `index_1` 索引的政策會變更為 `policy_1`，這可以是全新的政策，也可以是現有政策的更新版本。此程序只會在索引目前處於 `searches` 狀態時套用變更。此政策變更生效後，`index_1` 會轉換至 `delete` 狀態。

#### 端點

```json
POST _plugins/_ism/change_policy/{index}
```

#### 範例請求

```json
POST _plugins/_ism/change_policy/index_1
{
  "policy_id": "policy_1",
  "state": "delete",
  "include": [
    {
      "state": "searches"
    }
  ]
}
```
{% include copy-curl.html %}


#### 範例回應

```json
{
  "updated_indices": 1,
  "failures": false,
  "failed_indices": []
}
```

變更會排入受管理索引的佇列，並在下次工作執行時生效，因此 `updated_indices` 計數的是已記錄變更政策的索引，而非已移至新政策的索引。

---

## 重試失敗的索引
**於 1.0 版推出**
{: .label .label-purple }

重試索引失敗的動作。若要讓重試呼叫成功，ISM 必須管理該索引，且索引必須處於失敗狀態。您可以使用索引模式（`*`）重試多個失敗的索引。

使用 [說明索引](#explain-index) 確認索引處於失敗狀態：其 `action` 物件包含 `"failed": true`，且其 `step` 物件包含 `"step_status": "failed"`。

您也可以在請求本文中指定 `state`，讓索引在該狀態重新啟動，而非在其失敗的狀態中重新啟動。

#### 端點

```json
POST _plugins/_ism/retry/{index}
```

#### 範例請求

```json
POST _plugins/_ism/retry/index_1
{
  "state": "hot"
}
```
{% include copy-curl.html %}


#### 回應範例

```json
{
  "updated_indices": 1,
  "failures": false,
  "failed_indices": []
}
```

如果索引並非處於失敗狀態，回應會以 `failed_indices` 回報該索引：

```json
{
  "updated_indices": 0,
  "failures": true,
  "failed_indices": [
    {
      "index_name": "index_1",
      "index_uuid": "t6a6I5YDQTiXY9c7cymI_w",
      "reason": "This index is not in failed state."
    }
  ]
}
```

---

## 說明索引
**1.0 版新增**
{: .label .label-purple }

取得索引的目前狀態。您可以使用索引模式來取得多個索引的狀態。

#### 端點

```json
GET _plugins/_ism/explain/{index}
```

#### 請求範例

```json
GET _plugins/_ism/explain/index_1
```
{% include copy-curl.html %}


#### 回應範例

```json
{
  "index_1": {
    "index.plugins.index_state_management.policy_id": "policy_1",
    "index.opendistro.index_state_management.policy_id": "policy_1",
    "index": "index_1",
    "index_uuid": "t6a6I5YDQTiXY9c7cymI_w",
    "policy_id": "policy_1",
    "enabled": true
  },
  "total_managed_indices": 1
}
```

在您新增政策後的即時狀態下，回應的欄位為 `null`，且 `total_managed_indices` 為 `0`。ISM 會在下一次掃描時建立受管理索引工作，之後回應便會填入內容。
{: .note}

您也可以選擇在請求的路徑中加入 `show_policy` 參數，以取得目前套用至索引的政策，這有助於確認套用至索引的政策是否為最新版本。若要取得最新的政策，請參閱 [取得政策 API]({{site.url}}{{site.baseurl}}/im-plugin/ism/api/#get-policy)。

#### 請求範例

```json
GET _plugins/_ism/explain/index_1?show_policy=true
```
{% include copy-curl.html %}

#### 回應範例

```json
{
  "index_1": {
    "index.plugins.index_state_management.policy_id": "sample-policy",
    "index.opendistro.index_state_management.policy_id": "sample-policy",
    "index": "index_1",
    "index_uuid": "gCFlS_zcTdih8xyxf3jQ-A",
    "policy_id": "sample-policy",
    "enabled": true,
    "policy": {
      "policy_id": "sample-policy",
      "description": "ingesting logs",
      "last_updated_time": 1647284980148,
      "schema_version": 30,
      "error_notification": null,
      "default_state": "ingest",
      "states": [],
      "ism_template": null
    }
  },
  "total_managed_indices": 1
}
```

`plugins.index_state_management.policy_id` 設定自 ODFE 1.13.0 版起已淘汰。為保持一致性，我們在回應 API 中保留此欄位。

## 使用篩選條件說明索引
**2.12 版新增**
{: .label .label-purple }

您可以在 Explain API 中使用 `POST` 方法，依據特定條件篩選結果。這可讓您依據政策 ID、目前狀態或動作類型來查詢索引。

#### 端點

```json
POST _plugins/_ism/explain/{index}
```

#### 請求本文

請求本文支援下列選用篩選條件。若未指定某個篩選條件，則該參數具有任何值的索引都會包含在結果中。API 只會傳回符合所有指定篩選條件的索引。

| 參數 | 類型 | 說明 |
|:----------|:-----|:------------|
| `policy_id` | 字串 | 篩選結果，只顯示由指定政策 ID 管理的索引。 |
| `state` | 字串 | 篩選結果，只顯示目前處於指定狀態的索引。 |
| `action_type` | 字串 | 篩選結果，只顯示目前正在執行指定動作類型的索引。 |
| `failed` | 布林值 | 篩選結果，只顯示失敗的受管理索引。 |

#### 請求範例：依政策 ID 篩選

```json
POST _plugins/_ism/explain/log-*
{
  "filter": {
    "policy_id": "hot-warm-delete-policy"
  }
}
```
{% include copy-curl.html %}

#### 請求範例：依狀態與動作類型篩選

```json
POST _plugins/_ism/explain/app-*
{
  "filter": {
    "state": "warm",
    "action_type": "allocation"
  }
}
```
{% include copy-curl.html %}

#### 請求範例：依所有條件篩選

```json
POST _plugins/_ism/explain/data-*
{
  "filter": {
    "policy_id": "data-lifecycle-policy",
    "state": "hot",
    "action_type": "rollover"
  }
}
```
{% include copy-curl.html %}

#### 回應範例

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "test-logs-001": {
    "index.plugins.index_state_management.policy_id": "test-lifecycle-policy",
    "index": "test-logs-001",
    "index_uuid": "LmJgKNatQZWHQu-qIHlcJw",
    "policy_id": "test-lifecycle-policy",
    "enabled": true,
    "policy": {
      "policy_id": "test-lifecycle-policy",
      "description": "Lifecycle policy for log data: hot -> warm -> cold -> delete",
      "last_updated_time": 1730308440926,
      "schema_version": 30,
      "error_notification": null,
      "default_state": "hot",
      "states": [
        {
          "name": "hot",
          "actions": [
            {
              "rollover": {
                "min_doc_count": 10000,
                "min_size": "1gb",
                "min_index_age": "1d"
              }
            }
          ],
          "transitions": [
            {
              "state_name": "warm",
              "conditions": {
                "min_index_age": "7d"
              }
            }
          ]
        },
        {
          "name": "warm",
          "actions": [
            {
              "replica_count": {
                "number_of_replicas": 0
              }
            }
          ],
          "transitions": [
            {
              "state_name": "cold",
              "conditions": {
                "min_index_age": "30d"
              }
            }
          ]
        },
        {
          "name": "cold",
          "actions": [],
          "transitions": [
            {
              "state_name": "delete",
              "conditions": {
                "min_index_age": "90d"
              }
            }
          ]
        },
        {
          "name": "delete",
          "actions": [
            {
              "delete": {}
            }
          ],
          "transitions": []
        }
      ],
      "ism_template": null
    },
    "policy_seq_no": 0,
    "policy_primary_term": 1,
    "rolled_over": false,
    "index_creation_date": 1730308447399,
    "state": {
      "name": "hot",
      "start_time": 1730308447644
    },
    "action": {
      "name": "rollover",
      "start_time": 1730308447644,
      "index": 0,
      "failed": false,
      "consumed_retries": 0,
      "last_retry_time": 0
    },
    "step": {
      "name": "attempt_rollover",
      "start_time": 1730308447644,
      "step_status": "starting"
    },
    "retry_info": {
      "failed": false,
      "consumed_retries": 0
    },
    "info": {
      "message": "Currently checking rollover conditions"
    },
    "enabled": true,
    "enabled_time": 1730308447644
  },
  "total_managed_indices": 1
}
```

</details>

---

## 模擬政策
**3.7 版新增**
{: .label .label-purple }

在不進行任何變更的情況下，預覽政策套用至一或多個索引的方式。對於每個索引，回應會包含目前狀態、下一個要執行的動作、每個轉移條件的評估結果，以及索引接下來會移至哪個狀態。請使用此端點在附加政策前進行驗證，或偵錯索引為何未如預期轉移。

必須且只能提供 `policy_id` 或 `policy` 其中之一。

#### 端點

```json
POST _plugins/_ism/simulate
```

#### 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 類型 | 必要 | 說明 |
|:------|:-----|:---------|:------------|
| `policy_id` | 字串 | 視情況而定 | 要模擬的已儲存 ISM 政策 ID。未提供 `policy` 時為必要。 |
| `policy` | 物件 | 視情況而定 | 要模擬但不儲存的內嵌政策定義。未提供 `policy_id` 時為必要。 |
| `indices` | 字串陣列 | 是 | 要模擬的索引名稱或萬用字元模式。萬用字元模式會展開為相符的具體索引。未符合任何索引的模式會以無訊息方式忽略。不存在的具體索引名稱會在每個索引的結果中傳回錯誤。 |

#### 回應本文欄位

下表列出所有回應本文欄位。回應包含 `simulate_results` 陣列，每個索引各有一個項目。

| 欄位 | 類型 | 說明 |
|:------|:-----|:------------|
| `index_name` | 字串 | 索引的名稱。 |
| `index_uuid` | 字串 | 索引的 UUID。找不到索引時為 `null`。 |
| `policy_id` | 字串 | 用於模擬的政策 ID。內嵌政策為空字串。 |
| `is_managed` | 布林值 | 索引是否由 ISM 管理。 |
| `current_state` | 字串 | 索引所在的狀態，或未受管理索引的起始狀態。存在 `error` 時省略。 |
| `current_action` | 字串 | 在目前狀態下接下來會執行的動作。存在 `error` 時省略。 |
| `transition_evaluation` | 陣列 | 每個轉換條件的評估結果。僅在索引處於轉換階段時出現（沒有待執行的動作）。存在 `error` 時省略。 |
| `next_state` | 字串 | 索引會轉換到的狀態（第一個符合的條件）。未符合任何條件時為 `null`。存在 `error` 時省略。 |
| `error` | 字串 | 索引層級的錯誤訊息。索引不存在或發生其他索引層級錯誤時出現。此欄位存在時，除了 `index_name`、`index_uuid`、`policy_id` 和 `is_managed` 以外的所有其他欄位都會省略。 |

`transition_evaluation` 中的每個物件都包含下列欄位。

| 欄位 | 類型 | 說明 |
|:------|:-----|:------------|
| `state_name` | 字串 | 此轉換會將索引移至的目標狀態。 |
| `condition_met` | 布林值 | 是否符合轉換條件。 |
| `condition_type` | 字串 | 條件類型（例如 `min_index_age`、`min_doc_count`、`min_size`）。沒有條件的轉換會設為 `unconditional`。 |
| `current_value` | 字串 | 所檢查指標的目前值，格式化為可讀字串（例如 `"3d 4h"`）。無條件轉換時省略。 |
| `required_value` | 字串 | 條件所需的閾值，格式化為可讀字串（例如 `"7d"`）。無條件轉換時省略。 |

#### 範例請求：模擬已儲存的政策

下列請求會對 `index_1` 及一個不存在的索引模擬 [`policy_1` 政策](#create-policy)：

```json
POST _plugins/_ism/simulate
{
  "policy_id": "policy_1",
  "indices": ["index_1", "nonexistent-index"]
}
```
{% include copy-curl.html %}

#### 範例回應：模擬已儲存的政策

第一個結果顯示 `index_1` 會以 `ingest` 狀態開始，並以 `rollover` 作為其下一個動作。第二個結果顯示具體索引名稱在叢集中不存在索引時所傳回的 `error` 欄位：

```json
{
  "simulate_results": [
    {
      "index_name": "index_1",
      "index_uuid": "CNMBFMEIR12NYiOeW-pX4A",
      "policy_id": "policy_1",
      "is_managed": false,
      "current_state": "ingest",
      "current_action": "rollover",
      "next_state": null
    },
    {
      "index_name": "nonexistent-index",
      "index_uuid": null,
      "policy_id": "policy_1",
      "is_managed": false,
      "error": "Index 'nonexistent-index' not found in cluster"
    }
  ]
}
```

#### 範例請求：模擬內嵌政策

下列請求會模擬未儲存在叢集中的政策：

```json
POST _plugins/_ism/simulate
{
  "policy": {
    "description": "hot-warm lifecycle",
    "default_state": "hot",
    "states": [
      {
        "name": "hot",
        "actions": [],
        "transitions": [
          {
            "state_name": "warm",
            "conditions": { "min_index_age": "7d" }
          }
        ]
      },
      { "name": "warm", "actions": [], "transitions": [] }
    ]
  },
  "indices": ["index_1"]
}
```
{% include copy-curl.html %}

#### 範例回應：模擬內嵌政策

因為 `hot` 狀態未定義任何動作，下一個動作就是轉換本身，所以回應包含 `transition_evaluation` 陣列。未符合 `min_index_age` 條件，因此 `next_state` 為 `null`。由於政策未儲存，`policy_id` 欄位為空字串：

```json
{
  "simulate_results": [
    {
      "index_name": "index_1",
      "index_uuid": "CNMBFMEIR12NYiOeW-pX4A",
      "policy_id": "",
      "is_managed": false,
      "current_state": "hot",
      "current_action": "transition",
      "transition_evaluation": [
        {
          "state_name": "warm",
          "condition_met": false,
          "condition_type": "min_index_age",
          "current_value": "8.5s",
          "required_value": "7d"
        }
      ],
      "next_state": null
    }
  ]
}
```



---

## 刪除政策
**於 1.0 版推出**
{: .label .label-purple }

依 `policy_id` 刪除政策。

#### 端點

```json
DELETE _plugins/_ism/policies/{policy_id}
```

#### 範例請求

```json
DELETE _plugins/_ism/policies/policy_1
```
{% include copy-curl.html %}


#### 範例回應

```json
{
  "_index": ".opendistro-ism-config",
  "_id": "policy_1",
  "_version": 3,
  "result": "deleted",
  "forced_refresh": true,
  "_shards": {
    "total": 2,
    "successful": 2,
    "failed": 0
  },
  "_seq_no": 15,
  "_primary_term": 1
}
```

## 錯誤預防驗證
**於 2.4 版推出**
{: .label .label-purple }

ISM 會自動執行動作。不過，動作可能因各種原因而失敗。您可以使用錯誤預防驗證來測試動作並找出可能的失敗。

若要啟用錯誤預防驗證，請將 `plugins.index_state_management.action_validation.enabled` 設為 `true`：

```json
PUT _cluster/settings
{
   "persistent": {
      "plugins.index_state_management.action_validation.enabled": true
   }
}
```
{% include copy-curl.html %}

#### 範例回應

下列回應確認設定已更新：

```json
{
  "acknowledged" : true,
  "persistent" : {
    "plugins" : {
      "index_state_management" : {
        "action_validation" : {
          "enabled" : "true"
        }
      }
    }
  },
  "transient" : { }
}
```

若要擷取錯誤預防驗證狀態和訊息，請將 `validate_action=true` 傳遞至 `_plugins/_ism/explain` 端點：

```json
GET _plugins/_ism/explain/test-000001?validate_action=true
```
{% include copy-curl.html %}

#### 範例回應

回應包含額外的 validate 物件，其中含有驗證訊息和狀態：

```json
{
  "test-000001" : {
    "index.plugins.index_state_management.policy_id" : "test_rollover",
    "index.opendistro.index_state_management.policy_id" : "test_rollover",
    "index" : "test-000001",
    "index_uuid" : "CgKsxFmQSIa8dWqpbSJmyA",
    "policy_id" : "test_rollover",
    "policy_seq_no" : -2,
    "policy_primary_term" : 0,
    "rolled_over" : false,
    "index_creation_date" : 1667410460649,
    "state" : {
      "name" : "rollover",
      "start_time" : 1667410766045
    },
    "action" : {
      "name" : "rollover",
      "start_time" : 1667411127803,
      "index" : 0,
      "failed" : false,
      "consumed_retries" : 0,
      "last_retry_time" : 0
    },
    "step" : {
      "name" : "attempt_rollover",
      "start_time" : 1667411127803,
      "step_status" : "starting"
    },
    "retry_info" : {
      "failed" : true,
      "consumed_retries" : 0
    },
    "info" : {
      "message" : "Previous action was not able to update IndexMetaData."
    },
    "enabled" : false,
    "validate" : {
      "validation_message" : "Missing rollover_alias index setting [index=test-000001]",
      "validation_status" : "re_validating"
    }
  },
  "total_managed_indices" : 1
}
```

如果您傳遞 `validate_action=false` 或省略 `validate_action` 參數，回應不會包含驗證狀態和訊息：

```json
GET _plugins/_ism/explain/test-000001?validate_action=false
```
{% include copy-curl.html %}

```json
GET _plugins/_ism/explain/test-000001
```
{% include copy-curl.html %}

#### 回應範例

```json
{
  "test-000001" : {
    "index.plugins.index_state_management.policy_id" : "test_rollover",
    "index.opendistro.index_state_management.policy_id" : "test_rollover",
    "index" : "test-000001",
    "index_uuid" : "CgKsxFmQSIa8dWqpbSJmyA",
    "policy_id" : "test_rollover",
    "policy_seq_no" : -2,
    "policy_primary_term" : 0,
    "rolled_over" : false,
    "index_creation_date" : 1667410460649,
    "state" : {
      "name" : "rollover",
      "start_time" : 1667410766045
    },
    "action" : {
      "name" : "rollover",
      "start_time" : 1667411127803,
      "index" : 0,
      "failed" : false,
      "consumed_retries" : 0,
      "last_retry_time" : 0
    },
    "step" : {
      "name" : "attempt_rollover",
      "start_time" : 1667411127803,
      "step_status" : "starting"
    },
    "retry_info" : {
      "failed" : true,
      "consumed_retries" : 0
    },
    "info" : {
      "message" : "Previous action was not able to update IndexMetaData."
    },
    "enabled" : false
  },
  "total_managed_indices" : 1
}
```
