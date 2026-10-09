---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "複合監視器"
nav_order: 25
parent: Monitors
grand_parent: Alerting
has_children: false
---

# 複合監視器

---

<details markdown="block">
  <summary>
    目錄
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 關於複合監視器

Alerting 外掛程式的基本[監視器類型]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/monitors/#monitor-types)設計為定義單一觸發條件類型。例如，每文件監視器可根據查詢與文件的相符情形觸發警示，而每桶監視器則可根據針對資料來源中彙總值的查詢觸發警示。複合監視器會將多個監視器依序組合，以依據多項準則分析資料來源，然後使用各監視器的個別警示來產生單一的連鎖警示。這可讓您取得資料來源更細微的資訊，而且不需要手動協調個別監視器的排程。

複合監視器以下列方式移除基本監視器的限制：

* 複合監視器讓您能夠透過多種類型監視器所產生的觸發條件組合，建立複雜的查詢。
* 它們能夠定義以單次執行方式執行的一組規則與查詢管線。
* 它們會向使用者傳送單一警示，而不是其工作流程中各個監視器所產生的多個警示。
* 它們會依序執行多個監視器及多種類型的監視器，提供指定資料來源更完整的檢視，產生更聚焦的結果並減少結果中的雜訊。


## 重要詞彙

下表的重要詞彙說明複合監視器的基本概念。如需所有類型監視器通用的其他詞彙，請參閱 Alerting 一節中的[重要詞彙]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/index/#key-terms)。

| 詞彙 | 定義 |
| :--- | :--- |
| 複合監視器 | 複合監視器是一種支援以循序工作流程執行多個監視器的監視器類型。它支援設定觸發條件以建立連鎖警示。 |
| 委派監視器 | 委派監視器會依據其在複合監視器定義中的順序循序執行。當委派監視器的觸發條件符合時，它會產生稽核警示。此稽核警示接著會成為複合監視器觸發條件的條件。複合監視器支援每查詢、每桶及每文件監視器作為委派監視器。 |
| workflow ID | workflow ID 為所有委派監視器的整個工作流程提供識別碼。它與複合監視器的 monitor ID 同義。 |
| 連鎖警示 | 當委派監視器產生稽核警示時，連鎖警示會從複合監視器觸發條件產生。連鎖警示觸發條件支援使用邏輯運算子 `AND`、`OR` 及 `NOT`，因此您可以將多個函式結合成單一運算式。 |
| 稽核警示 | 委派監視器會產生處於 **audit** 狀態的警示。使用者不會收到每個個別稽核警示的通知，也不需要確認它們。稽核警示用於評估複合監視器中的連鎖警示觸發條件。 |
| 執行 | 在複合監視器組態中定義的順序中，所有委派監視器的單次執行。 |

## 基本工作流程

您可將個別監視器結合成工作流程來建立複合監視器，該工作流程會依定義的順序執行每個監視器。當委派監視器的個別稽核警示符合複合監視器的觸發條件時，複合監視器會產生自己的連鎖警示。請考量下列事件順序，以了解設定兩個委派監視器的簡單複合監視器如何執行其工作流程。在此範例中，當第一個監視器與第二個監視器都產生警示時，即符合複合監視器的觸發條件。

1. 複合監視器開始執行並將其委派給第一個監視器。第一個監視器的觸發條件符合，並產生稽核警示。
1. 複合監視器接著將執行委派給第二個監視器。第二個監視器的觸發條件也符合，並產生自己的稽核警示。
1. 由於複合監視器的觸發條件要求第一個與第二個監視器都產生稽核警示，因此複合監視器接著會觸發連鎖警示。
1. 若在複合監視器的定義中設定了通知，使用者會收到連鎖警示的通知。不過，他們不會收到兩個委派監視器所產生的個別稽核警示。

在這個簡單範例中，第一個監視器可以是設定為使用三個不同查詢分析資料來源的每文件監視器，而第二個監視器則可以是依用戶端 IP 彙總資料的每桶監視器。透過結合每個委派監視器的需求，複合監視器會聚焦於決定是否產生警示的準則。這可提升警示的意義，同時移除沒有確定價值的多餘警示。


## 使用 API 管理複合監視器

您可以使用 OpenSearch REST API 或 [OpenSearch Dashboards](#creating-composite-monitors-in-opensearch-dashboards) 來管理複合監視器。本節說明複合監視器的 API 功能。

### 建立複合監視器

此 API 可讓您建立複合監視器。

```json
POST _plugins/_alerting/workflows
```
{% include copy-curl.html %}

#### 請求本文欄位

| 欄位 | 類型 | 說明 |
| :--- | :--- | :--- |
| `schedule` | 物件 | 決定執行作業執行頻率的排程。 |
| `schedule.period.interval` | 數值 | 接受數值以設定執行作業的執行頻率。 |
| `schedule.period.unit` | 物件 | 間隔的時間單位：`SECONDS`、`MINUTES`、`HOURS`、`DAYS`。 |
| `inputs` | 物件 | 接受輸入以定義委派監視器，其會指定委派監視器及其在執行順序中的順序。 |
| `inputs.composite_input.sequence.delegates` | 物件 | 構成複合監視器之個別監視器的設定。 |
| `inputs.composite_input.sequence.delegates.order` | 數字 | 指定監視器在執行中執行的順序。 |
| `inputs.composite_input.sequence.delegates.monitor_id` | 字串 | 監視器的唯一識別碼。 |
| `enabled_time` | 數字 | 啟用監視器的時間。以 epoch 時間表示。 |
| `enabled` | 布林值 | 決定複合監視器是否啟用的設定。將其設為 `true` 會啟用複合監視器。預設為 `true`。 |
| `workflow_type` | 字串 | 針對複合監視器設為 `composite`。 |
| `triggers` | 物件 | 個別警示觸發條件的詳細資料。 |
| `triggers.chained_alert_trigger` | 物件 | 每個個別警示觸發條件的詳細資料。每個監視器的警示觸發條件都需要其組態的設定。 |
| `triggers.chained_alert_trigger.id` | 字串 | 警示觸發條件的唯一識別碼。 |
| `triggers.chained_alert_trigger.name` | 字串 | 警示觸發條件的名稱。 |
| `triggers.chained_alert_trigger.severity` | 數字 | 警示嚴重性。1 = 最高；2 = 高；3 = 中；4 = 低；5 = 最低。 |
| `triggers.chained_alert_trigger.condition.script` | 物件 | 決定觸發警示之條件的指令碼詳細資料。 |
| `triggers.chained_alert_trigger.condition.script.source` | 字串 | 定義觸發警示之條件的 Painless 指令碼。如需更多資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。 |
| `triggers.chained_alert_trigger.condition.script.lang` | 字串 | 針對 Painless 指令碼語言輸入 `painless`。 |
| `actions` | 物件 | 提供設定警示通知的欄位。 |

#### 請求範例

```json
POST _plugins/_alerting/workflows
{
	"last_update_time": 1679468231835,
	"owner": "alerting",
	"type": "workflow",
	"schedule": {
		"period": {
			"interval": 1,
			"unit": "MINUTES"
		}
	},
	"inputs": [{
		"composite_input": {
			"sequence": {
				"delegates": [{
						"order": 1,
						"monitor_id": "grsbCIcBvEHfkjWFeCqb"
					},
					{
						"order": 2,
						"monitor_id": "agasbCIcBvEHfkjWFeCqa"
					}
				]
			}
		}
	}],
	"enabled_time": 1679468231835,
	"enabled": true,
	"workflow_type": "composite",
	"name": "scale_up",
	"triggers": [{
			"chained_alert_trigger": {
				"id": "m1ANDm2",
				"name": "jnkjn",
				"severity": "1",
				"condition": {
					"script": {
						"source": "(monitor[id=grsbCIcBvEHfkjWFeCqb] && monitor[id=agasbCIcBvEHfkjWFeCqa])",
						"lang": "painless"
					}
				}
			},
			"actions": [{
				"name": "test-action",
				"destination_id": "ld7912sBlQ5JUWWFThoW",
				"message_template": {
					"source": "This is my message body."
				},
				"throttle_enabled": true,
				"throttle": {
					"value": 27,
					"unit": "MINUTES"
				},
				"subject_template": {
					"source": "TheSubject"
				}
			}]
		},
		{
			"chained_alert_trigger": {
				"id": "m1ORm2",
				"name": "jnkjn",
				"severity": "1",
				"condition": {
					"script": {
						"source": "(monitor[id=grsbCIcBvEHfkjWFeCqb] || monitor[id=agasbCIcBvEHfkjWFeCqa])",
						"lang": "painless"
					}
				}
			}
		}
	]
}
```
{% include copy-curl.html %}

#### 使用 Painless 指令碼語言定義連鎖警示觸發條件

複合監視器組態使用 Painless 指令碼語言來定義產生連鎖警示的條件。每次執行複合監視器時，都會套用這些條件。您可在請求的 `triggers.chained_alert_triggers.condition.script.source` 欄位中定義警示觸發條件。使用 Painless 語法，您可以透過基本布林運算子 AND、OR、NOT 及優先順序，對監視器之間的連結套用邏輯：

* AND = `&&`
* OR = `||`
* NOT = `!`
* 優先順序 = `()`

請參閱下列範例，瞭解如何在監視器定義中使用各個運算子及優先順序。

* **範例 1**
   
   `monitor[id=1] && monitor[id=2]`
   
   下列委派監視器條件會在監視器 #1 與監視器 #2 皆產生警示時，觸發複合監視器產生連鎖警示。

* **範例 2**
   
   `monitor[id=1] || !monitor[id=2]`

   下列條件會在監視器 #1 產生警示，或監視器 #2 未產生警示時，觸發複合監視器產生連鎖警示。

* **範例 3**
   
   `monitor[id=1] && (monitor[id=2] || monitor[id=3])`

   下列條件會在監視器 #1 產生警示，且監視器 #2 或監視器 #3 產生警示時，觸發複合監視器產生連鎖警示。
   
Painless 指令碼中的監視器 ID 順序並不決定監視器的執行順序。監視器的執行順序由請求中的 `inputs.composite_input.sequence.delegates.order` 欄位定義。
{: .note }


### 取得複合監視器

此 API 會擷取指定監視器的資訊。

```json
GET _plugins/_alerting/workflows/{workflow_id}
```
{% include copy-curl.html %}

#### 路徑參數

| 欄位 | 類型 | 說明 |
| :--- | :--- | :--- |
| `workflow_id` | 字串 | 複合監視器的[工作流程 ID](#key-terms)。 |


### 更新複合監視器

此 API 會更新複合監視器的詳細資料。如需請求欄位的說明，請參閱[建立複合監視器](#create-composite-monitor)。

#### 請求範例

```json
PUT _plugins/_alerting/workflows/{workflow_id}
{
    "owner": "security_analytics",
    "type": "workflow",
    "schedule": {
        "period": {
        "interval": 1,
        "unit": "MINUTES"
        }
    },
    "inputs": [
        {
            "composite_input": {
                "sequence": {
                    "delegates": [
                        {
                            "order": 1,
                            "monitor_id": "grsbCIcBvEHfkjWFeCqb"
                        },
                        {
                            "order": 2,
                            "monitor_id": "agasbCIcBvEHfkjWFeCqa"
                        }
                    ]
                }
            }
        }
    ],
    "enabled_time": 1679468231835,
    "enabled": true,
    "workflow_type": "composite",
    "name": "NTxdwApKbv"
}
```
{% include copy-curl.html %}


### 刪除複合監視器

```json
DELETE _plugins/_alerting/workflows/{workflow_id}
```
{% include copy-curl.html %}


### 執行複合監視器

此 API 會開始執行複合監視器的工作流程：

```json
POST /_plugins/_alerting/workflows/{workflow_id}/_execute
```
{% include copy-curl.html %}

#### 回應範例

```json
{
    "execution_id": "I0GXeIgBYKBG2nHoiHCL_2023-06-01T20:18:48.511884_a9c1d055-9b70-49c2-b32a-716cff1f562e",
    "workflow_name": "scale_up",
    "workflow_id": "I0GXeIgBYKBG2nHoiHCL",
    "trigger_results": {
        "m1ANDm2": {
            "name": "jnkjn",
            "triggered": true,
            "action_results": {},
            "error": null
        },
        "m1ORm2": {
            "name": "jnkjn",
            "triggered": true,
            "action_results": {},
            "error": null
        }
    },
    "monitor_run_results": [{
            "monitor_name": "test triggers",
            "period_start": 1685650668501,
            "period_end": 1685650728501,
            "error": null,
            "input_results": {
                "results": [{
                    "bhjh": [
                        "OkGceIgBYKBG2nHoyHAn|test1",
                        "O0GceIgBYKBG2nHozHCW|test1"
                    ],
                    "nkjkj": [
                        "OkGceIgBYKBG2nHoyHAn|test1",
                        "O0GceIgBYKBG2nHozHCW|test1"
                    ],
                    "jknkjn": [
                        "OkGceIgBYKBG2nHoyHAn|test1",
                        "O0GceIgBYKBG2nHozHCW|test1"
                    ]
                }],
                "error": null
            },
            "trigger_results": {
                "NC3Dd4cBCDCIfBYtViLI": {
                    "name": "njkkj",
                    "triggeredDocs": [
                        "OkGceIgBYKBG2nHoyHAn|test1",
                        "O0GceIgBYKBG2nHozHCW|test1"
                    ],
                    "action_results": {},
                    "error": null
                }
            }
        },
        {
            "monitor_name": "test triggers 2",
            "period_start": 1685650668501,
            "period_end": 1685650728501,
            "error": null,
            "input_results": {
                "results": [{
                    "bhjh": [
                        "PEGceIgBYKBG2nHo1HCw|test",
                        "PUGceIgBYKBG2nHo3HA8|test"
                    ],
                    "nkjkj": [
                        "PEGceIgBYKBG2nHo1HCw|test",
                        "PUGceIgBYKBG2nHo3HA8|test"
                    ],
                    "jknkjn": [
                        "PEGceIgBYKBG2nHo1HCw|test",
                        "PUGceIgBYKBG2nHo3HA8|test"
                    ]
                }],
                "error": null
            },
            "trigger_results": {
                "NC3Dd4cBCDCIfBYtViLI": {
                    "name": "njkkj",
                    "triggeredDocs": [
                        "PEGceIgBYKBG2nHo1HCw|test",
                        "PUGceIgBYKBG2nHo3HA8|test"
                    ],
                    "action_results": {},
                    "error": null
                }
            }
        }
    ],
    "execution_start_time": "2023-06-01T20:18:48.511874Z",
    "execution_end_time": "2023-06-01T20:18:53.682405Z",
    "error": null
}
```


### 取得連鎖警示

此 API 會回傳在複合監視器工作流程中產生的連鎖警示陣列：

```json
GET /_plugins/_alerting/workflows/alerts?workflowIds={workflow_ids}&getAssociatedAlerts=true
```

#### 查詢參數

| 欄位 | 類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `workflowIds` | 陣列 | 否 | 使用此參數時，會回傳由指定工作流程建立的警示。 |
| `getAssociatedAlerts` | 布林值 | 否 | 當設定為 `true` 時，回應會回傳複合監視器用來建立連鎖警示的稽核警示。預設值為 `false`。 |


#### 回應範例

```json
{
    "alerts": [
        {
            "id": "PbQoZokBfd2ci_FqMGi6",
            "version": 1,
            "monitor_id": "",
            "workflow_id": "G7QoZokBfd2ci_FqD2iZ",
            "workflow_name": "scale_up",
            "associated_alert_ids": [
                "4e8256c5-529a-484c-bf7b-d3980c03e9a4",
                "513a8cb3-44bc-4eee-8aac-131be10b399e"
            ],
            "schema_version": -1,
            "monitor_version": -1,
            "monitor_name": "",
            "execution_id": "G7QoZokBfd2ci_FqD2iZ_2023-07-17T23:20:55.244970_edd977d2-c02b-4cbe-8a79-2aa7991c4191",
            "trigger_id": "m1ANDm2",
            "trigger_name": "jnkjn",
            "finding_ids": [],
            "related_doc_ids": [],
            "state": "ACTIVE",
            "error_message": null,
            "alert_history": [],
            "severity": "1",
            "action_execution_results": [],
            "start_time": 1689636057269,
            "last_notification_time": 1689636057270,
            "end_time": null,
            "acknowledged_time": null
        },
        {
            "id": "PrQoZokBfd2ci_FqMGj8",
            "version": 1,
            "monitor_id": "",
            "workflow_id": "G7QoZokBfd2ci_FqD2iZ",
            "workflow_name": "scale_up",
            "associated_alert_ids": [
                "4e8256c5-529a-484c-bf7b-d3980c03e9a4",
                "513a8cb3-44bc-4eee-8aac-131be10b399e"
            ],
            "schema_version": -1,
            "monitor_version": -1,
            "monitor_name": "",
            "execution_id": "G7QoZokBfd2ci_FqD2iZ_2023-07-17T23:20:55.244970_edd977d2-c02b-4cbe-8a79-2aa7991c4191",
            "trigger_id": "m1ORm2",
            "trigger_name": "jnkjn",
            "finding_ids": [],
            "related_doc_ids": [],
            "state": "ACTIVE",
            "error_message": null,
            "alert_history": [],
            "severity": "1",
            "action_execution_results": [],
            "start_time": 1689636057340,
            "last_notification_time": 1689636057340,
            "end_time": null,
            "acknowledged_time": null
        }
    ],
    "associatedAlerts": [
        {
            "id": "4e8256c5-529a-484c-bf7b-d3980c03e9a4",
            "version": -1,
            "monitor_id": "DrQoZokBfd2ci_FqCWh8",
            "workflow_id": "G7QoZokBfd2ci_FqD2iZ",
            "workflow_name": "",
            "associated_alert_ids": [],
            "schema_version": 5,
            "monitor_version": 1,
            "monitor_name": "test triggers",
            "execution_id": "G7QoZokBfd2ci_FqD2iZ_2023-07-17T23:20:55.244970_edd977d2-c02b-4cbe-8a79-2aa7991c4191",
            "trigger_id": "NC3Dd4cBCDCIfBYtViLI",
            "trigger_name": "njkkj",
            "finding_ids": [
                "277afca7-d5aa-46ed-8023-5449ece65d36"
            ],
            "related_doc_ids": [
                "H7QoZokBfd2ci_FqFmii|test1"
            ],
            "state": "AUDIT",
            "error_message": null,
            "alert_history": [],
            "severity": "1",
            "action_execution_results": [],
            "start_time": 1689636056410,
            "last_notification_time": 1689636056410,
            "end_time": null,
            "acknowledged_time": null
        },
        {
            "id": "513a8cb3-44bc-4eee-8aac-131be10b399e",
            "version": -1,
            "monitor_id": "EbQoZokBfd2ci_FqCmiR",
            "workflow_id": "G7QoZokBfd2ci_FqD2iZ",
            "workflow_name": "",
            "associated_alert_ids": [],
            "schema_version": 5,
            "monitor_version": 1,
            "monitor_name": "test triggers 2",
            "execution_id": "G7QoZokBfd2ci_FqD2iZ_2023-07-17T23:20:55.244970_edd977d2-c02b-4cbe-8a79-2aa7991c4191",
            "trigger_id": "NC3Dd4cBCDCIfBYtViLI",
            "trigger_name": "njkkj",
            "finding_ids": [
                "6d185585-a077-4dde-8e43-b4c01b9f3102"
            ],
            "related_doc_ids": [
                "ILQoZokBfd2ci_FqGmhb|test"
            ],
            "state": "AUDIT",
            "error_message": null,
            "alert_history": [],
            "severity": "1",
            "action_execution_results": [],
            "start_time": 1689636056943,
            "last_notification_time": 1689636056943,
            "end_time": null,
            "acknowledged_time": null
        }
    ],
    "totalAlerts": 2
}
```

#### 請求本文欄位

| 欄位 | 類型 | 說明 |
| :--- | :--- | :--- |
| `alerts` | 陣列 | 由複合監視器產生的連鎖警示清單。 |
| `associatedAlerts` | 陣列 | 由委派監視器產生的稽核警示清單。 |


### 確認連鎖警示

[取得警示之後](#get-chained-alerts)，您可以在一次呼叫中確認多個作用中的警示。如果警示已處於 ERROR、COMPLETED 或 ACKNOWLEDGED 狀態，則會出現在 failed 陣列中。

```json
POST _plugins/_alerting/workflows/{workflow_id}/_acknowledge/alerts
{
    "alerts": ["eQURa3gBKo1jAh6qUo49"]
}
```
{% include copy-curl.html %}

#### 請求本文欄位

| 欄位 | 類型 | 說明 |
| :--- | :--- | :--- |
| `alerts` | 陣列 | 依 ID 列出的警示清單。結果包含由系統確認的警示，以及系統無法識別的警示。 |

#### 回應範例

```json
{
    "success": [
    "eQURa3gBKo1jAh6qUo49"
    ],
    "failed": []
}
```

## 在 OpenSearch Dashboards 中建立複合監視器

首先前往 OpenSearch Dashboards 的 **Create monitor** 頁面：**Alerting > Monitors**，然後選取 **Create monitor**。為監視器命名，然後選取 **Composite monitor** 作為監視器類型。建立複合監視器工作流程與觸發條件的步驟，會因您使用 **Visual editor** 或 **Extraction query editor** 而有所不同。前者提供定義複合監視器的基本 UI 選取器，後者則允許您使用指令碼建立工作流程與觸發條件。決定使用哪種方法後，請參閱對應的章節。

### 視覺化編輯器

若要使用視覺化編輯器定義工作流程與觸發條件，請在 **Monitor defining method** 區段中選取 **Visual editor** 單選按鈕。如下圖所示。

![選取 Visual editor]({{site.url}}{{site.baseurl}}/images/alerting/vis-editor.png){: width="50%" }

若要在視覺化編輯器中完成建立複合監視器，請依照下列步驟操作：

1. 在 **Frequency** 下拉式清單中，選取 **By interval**、**Daily**、**Weekly**、**Monthly** 或 **Custom cron expression**：
  * **By interval** — 允許您根據指定的分鐘、小時或天數重複執行排程。
  * **Daily** — 指定一天中的時間與時區。
  * **Weekly** — 指定一週中的某一天、一天中的時間與時區。
  * **Monthly** — 指定一個月中的某一天、一天中的時間與時區。
  * **Custom cron expression** — 為排程建立自訂 cron 運算式。可使用 **cron expressions** 連結協助建立這些運算式，或參閱 [Cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/#cron-expressions)。

1. 在 **Delegate monitors** 區段中，透過下拉式清單選取要納入工作流程的個別監視器。在 **Visual editor** 中，選取監視器的順序會決定它們在工作流程中的順序。
  
   選取 **Add another monitor** 以新增另一個下拉式清單。至少需要兩個委派監視器，總計最多允許 10 個。請注意，複合監視器支援以每查詢、每桶及每文件監視器作為委派監視器。
   
   在每個下拉式清單旁，您可以選取檢視監視器圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/dashboards/view-monitor-icon.png" class="inline-icon" alt="view monitor icon"/>{:/}) 以開啟監視器的詳細資訊視窗，並檢視其相關資訊。
   
1. 為複合監視器定義一或多個觸發條件。在 **Triggers** 區段中，選取 **Add trigger**。新增觸發條件名稱，然後定義觸發條件。
    * 使用 **Select delegate monitor** 標籤開啟下圖所示的快顯視窗。
    
    ![此快顯視窗顯示選取委派監視器與觸發條件運算子的選項]({{site.url}}{{site.baseurl}}/images/alerting/trigger1.png){: width="50%" }
    
    * 使用 **Select delegate monitor** 下拉式清單，從先前步驟中定義的監視器中選取一個委派監視器。對於第一個委派監視器，您可以視需要選取 NOT 作為運算子。監視器填入欄位後，您可以使用清單右側的垃圾桶圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/alerting/trash-can-icon.png" class="inline-icon" alt="trash can icon"/>{:/}) 在需要時移除該監視器。
    * 選取第一個監視器右側的加號 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/alerting/plus-sign-icon.png" class="inline-icon" alt="plus sign"/>{:/}) 以選取第二個委派監視器。選取第二個監視器後，選取其中一個運算子 `AND`、`OR`、`AND NOT` 或 `OR NOT`，將條件套用於兩個監視器之間。套用運算子後，您可以選取該運算子再次開啟快顯視窗並變更選取項目。
    * 選取警示的嚴重性等級。選項包括 **1 (Highest)**、**2 (High)**、**3 (Medium)**、**4 (Low)** 與 **5 (Lowest)**。
    * 在 **Notifications** 區段中，從下拉式清單選取通知頻道。如果沒有任何頻道，請選取下拉式清單右側的 **Manage channels** 標籤以設定通知頻道。如需通知的詳細資訊，請參閱[通知]({{site.url}}{{site.baseurl}}/observing-your-data/notifications/index/)文件。您也可以選取 **Add notification** 為警示觸發條件指定其他通知。
      
      所有監視器類型的通知皆為選用。
      {: .note }

    * 若要定義其他觸發條件，請選取 **Add another trigger**。總計最多可有 10 個觸發條件。選取畫面右側的 **Remove trigger** 以移除觸發條件。
    
1. 完成監視器工作流程並定義觸發條件後，選取畫面右下角的 **Create**。複合監視器即建立完成，並會開啟監視器的詳細資訊視窗。

### 擷取查詢編輯器

若要使用擷取查詢編輯器來定義工作流程與觸發條件，請在 **Monitor defining method** 區段中選取 **Extraction query editor** 選項按鈕。如下圖所示。

![選取擷取查詢編輯器]({{site.url}}{{site.baseurl}}/images/alerting/extract-q-editor.png){: width="50%" }

擷取查詢編輯器遵循與視覺化編輯器相同的一般步驟，但它可讓您使用 API 查詢的擷取內容來建置複合監視器工作流程與警示觸發條件。這讓您能夠建立視覺化編輯器不支援的更進階組態。下列各節提供這兩個欄位的內容範例。複合監視器建立的所有其他步驟都與視覺化編輯器的步驟相同。

* **Define workflow**
  
  在 **Define workflow** 欄位中，輸入可定義委派監視器及其在工作流程中順序的序列。下列範例顯示工作流程中包含的委派監視器，以及它們在序列中的順序：

  ```json
  {
      "sequence": {
          "delegates": [
              {
                  "order": 1,
                  "monitor_id": "0TgBZokB2ZtsLaRvXz70"
              },
              {
                  "order": 2,
                  "monitor_id": "8jgBZokB2ZtsLaRv6z4N"
              }
          ]
      }
  }
  ```
  
  工作流程中包含的所有委派監視器都需要 `monitor_id` 以及 `order` 的值。
  
* **Trigger condition**
  
  在 **Trigger condition** 欄位中，輸入將用來定義監視器之間條件的監視器與運算子。此欄位要求觸發條件必須以 Painless 指令碼語言格式化。若要了解這些指令碼如何形成觸發條件，請參閱[使用 Painless 指令碼定義連鎖警示觸發條件](#using-painless-scripting-language-to-define-chained-alert-trigger-conditions)。

  下列範例顯示一個觸發條件，其要求第一個監視器或第二個監視器產生稽核警示，複合監視器才能產生連鎖警示：

  ```painless
  (monitor[id=8d36S4kB0DWOHH7wpkET] || monitor[id=4t36S4kB0DWOHH7wL0Hk])
  ```

### 檢視監視器詳細資料

建立複合監視器後，它會出現在 **Monitors** 索引標籤的監視器清單中。**Type** 欄會指出監視器類型，包括複合監視器類型。**Associations with composite monitors** 欄會提供基本監視器作為委派監視器用於多少個複合監視器的計數。在 **Monitor name** 欄中選取監視器，即可開啟其詳細資料視窗。

對於複合監視器，詳細資料視窗的 **Alerts** 區段包含 **Actions** 欄，其中包含檢視詳細資料圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/dashboards/view-monitor-icon.png" class="inline-icon" alt="view monitor icon"/>{:/})。下圖顯示 **Actions** 欄位於最右側的最後一欄。

![監視器詳細資料視窗的警示區段]({{site.url}}{{site.baseurl}}/images/alerting/comp-details-alerts.png){: width="75%" }

選取此圖示可開啟 **Alert details** 視窗。此視窗會顯示屬於產生連鎖警示之執行作業一部分的所有稽核警示，並包含產生稽核警示的委派監視器。選取視窗右上角的 **X** 以關閉 **Alert details**。

返回監視器詳細資料視窗的 **Alerts** 區段後，您可以選取 **Alert start time** 左側的核取方塊來醒目顯示該警示。醒目顯示警示後，您可以選取此區段右上部分的 **Acknowledge**。警示即會確認，且 **State** 欄中的狀態會從 Active 變更為 Acknowledged。 
