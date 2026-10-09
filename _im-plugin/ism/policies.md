---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "原則"
nav_order: 10
parent: Index State Management
has_children: true
---

# ISM 原則

原則是一些實體 (以 JSON 文件儲存)，用來定義下列項目：

- 索引可以處於的*狀態*，包括新索引的預設狀態。例如，您可以把狀態命名為「hot」、「warm」、「delete」等等。如需詳細資訊，請參閱[狀態](#states)。
- 當索引進入某個狀態時，您希望此外掛程式採取的任何*動作*，例如執行輪替。如需詳細資訊，請參閱[動作](#actions)。
- 索引必須符合才能移至新狀態的條件，稱為*轉換*。例如，如果索引已存在超過八週，您可能會想將它移至「delete」狀態。如需詳細資訊，請參閱[轉換](#transitions)。

動作和轉換會與狀態相關聯。條件 (例如索引大小或存在時間) 會觸發轉換至新狀態，而進入狀態則會觸發其動作。

您可以完全彈性地設計您的原則。您可以建立任何狀態、轉換至任何其他狀態，並在每個狀態中指定任意數量的動作。

下表列出原則的欄位。

欄位 | 說明 | 類型 | 必要 | 唯讀
:--- | :--- |:--- |:--- |
`policy_id` |  原則的名稱。 | 字串 | 是 | 是
`description` |  原則的人類可讀描述。 | 字串 | 是 | 否
`ism_template` | 用來將原則自動套用至新建立索引的 ISM 範本。 | 物件的巢狀清單 | 否 | 否
`ism_template.index_patterns` | 符合新建立索引名稱的模式。 | 字串清單 | 否 | 否
`ism_template.priority` | 當多個原則符合新建立的索引名稱時，用來選擇要套用哪個原則的優先順序。 | 整數 | 否 | 否
`last_updated_time`  |  原則上次更新的時間。 | 時間戳記 | 是 | 是
`error_notification` |  錯誤通知的目的地和訊息範本。目的地可以是 Amazon Chime、Slack 或 webhook URL。 | 物件 | 否 | 否
`default_state` | 使用此原則之每個索引的預設起始狀態。 | 字串 | 是 | 否
`states` | 您在原則中定義的狀態。 | 物件的巢狀清單 | 是 | 否


## 狀態

狀態會定義受管理索引的狀態。受管理的索引一次只能處於一個狀態。狀態的動作會在進入狀態時依序執行。狀態的轉換會在所有動作完成後定期檢查。

下表列出您可以為狀態定義的參數。

欄位 | 說明 | 類型 | 必要
:--- | :--- |:--- |:--- |
`name` |  狀態的名稱。 | 字串 | 是
`actions` | 進入狀態後要執行的動作。如果您省略此欄位，狀態不會執行任何動作。如需詳細資訊，請參閱[動作](#actions)。 | 物件的巢狀清單 | 否
`transitions` | 後續狀態以及轉換至這些狀態所需的條件。如果沒有轉換存在，原則會假設它已完成，且現在可以停止管理索引。如需詳細資訊，請參閱[轉換](#transitions)。 | 物件的巢狀清單 | 否


## 動作

動作是原則在進入特定狀態時可以執行的[操作]({{site.url}}{{site.baseurl}}/im-plugin/ism/policies-operations/)。

ISM 會依定義的順序執行動作。如果某個動作失敗，狀態動作會被放棄，其餘動作不會執行。

例如，如果您定義動作 `[A,B,C,D]`，ISM 會執行下列事項：
1. 執行動作 `A`。
2. 根據叢集設定 `plugins.index_state_management.job_interval` 休眠一段時間。
3. 執行動作 `B`。

依此類推。

如果 ISM 無法成功執行動作 `A`，則動作 `B`、`C` 和 `D` 不會執行。

您可以選擇性地定義動作的逾時期間。逾時到期時，ISM 會將該動作標示為失敗。逾時涵蓋整個動作，而非單次嘗試：計時器會在 ISM 開始動作時啟動，並持續執行經過每個步驟、重試和重試延遲，包括動作等待符合其條件時各次作業執行之間的時間。

ISM 只會在受管理索引作業執行時檢查計時器，預設為每 5 分鐘一次。例如，將 `min_index_age` 設為 `1d` 的[輪替]({{site.url}}{{site.baseurl}}/im-plugin/ism/policies-operations/#rollover)操作，會在每次作業執行時評估 `min_index_age`，直到索引存在滿 1 天為止。因此，`1h` 的 `timeout` 會導致動作在索引符合條件之前就失敗。

逾時到期時，ISM 會將動作標示為失敗，並停止管理索引，直到您呼叫 Retry failed index API 為止；該 API 會重新啟動動作及其計時器。逾時不會停止 ISM 已開始的工作，也不會復原動作已做的變更。

由於 ISM 每次作業執行只執行一個步驟，請將逾時設為長於動作所需的總時間，再加上其每個步驟的一個作業間隔。如果您省略 `timeout`，動作永遠不會逾時，並會根據其 `retry` 組態繼續重試。

下表列出您可以為動作定義的參數。

參數 | 說明 | 類型 | 必要 | 預設
:--- | :--- |:--- |:--- |
`timeout` |  動作的逾時期間。接受分鐘、小時和天的時間單位。 | 時間單位 | 否 | -
`retry` | 動作的重試組態。 | 物件 | 否 | 依動作而定

`retry` 操作具有下列參數。

參數 | 說明 | 類型 | 必要 | 預設
:--- | :--- |:--- |:--- |
`count` | 重試次數。 | 整數 | 是 | -
`backoff` | 重試時要使用的退避原則類型。有效值為 Exponential、Constant 和 Linear。 | 字串 | 否 | Exponential
`delay` | 重試之間等待的時間。接受分鐘、小時和天的時間單位。 | 時間單位 | 否 | 1 分鐘

### 範例動作

下列範例 `read_only` 動作的逾時期間為一小時。原則會以指數退避原則重試此動作三次，每次重試之間的延遲為 10 分鐘：

```json
"actions": [
  {
    "timeout": "1h",
    "retry": {
      "count": 3,
      "backoff": "exponential",
      "delay": "10m"
    },
    "read_only": {}
  }
]
```

如需可用單位類型的清單，請參閱[支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。

## 轉換

轉換會定義觸發狀態變更的條件。目前狀態中的所有動作完成後，原則會開始檢查轉換的條件。

ISM 會依定義的順序評估轉換。它會使用第一個評估為 `true` 的轉換。

如果您在轉換中未指定任何條件，則它一律評估為 `true`。如果原則檢查這類轉換，它會立即將索引轉換至轉換中定義的狀態。

例如，假設您已定義轉換：`[A,B,C,D]`，且轉換 `A`、`B` 和 `C` 目前評估為 `false`，而 `D` 沒有條件。ISM 會依序逐一查看清單，並將下一個狀態設為轉換 `D` 中定義的狀態。在其下一次執行時，ISM 會從 `D` 定義的狀態開始。

此表列出您可以為轉換定義的參數。

參數 | 說明 | 類型 | 必要
:--- | :--- |:--- |:--- |
`state_name` |  符合條件時要轉換至的狀態名稱。 | 字串 | 是
`conditions` |  列出轉換的條件。 | 清單 | 是

`conditions` 物件具有下列參數。

參數 | 說明 | 類型 | 必要
:--- | :--- |:--- |:--- |
`min_index_age` | 轉換所需的索引最小存在時間。 | 字串 | 否
`min_rollover_age` | 發生輪替後轉換至下一個狀態所需的最小存在時間。 | 字串 | 否
`min_state_age` | 索引在轉換前必須處於目前狀態的最短時間。 | 字串 | 否
`min_doc_count` | 轉換所需的索引最小文件計數。 | 整數 | 否
`min_size` | 轉換所需的主要分片儲存空間總大小下限 (不計副本)。例如，如果您將 `min_size` 設為 100 GiB，而您的索引有 5 個主要分片和 5 個副本分片，每個分片各為 20 GiB，則所有主要分片的總大小為 100 GiB，因此您的索引會轉換至下一個狀態。 | 字串 | 否
`no_alias` | 根據別名是否存在來控制轉換。如果為 `true`，則只有在索引**沒有別名**時才會轉換。如果為 `false`，則只有在至少**存在一個別名**時才會轉換。 | 布林值 | 否
`cron` | 如果沒有其他轉換先發生，則觸發轉換的 `cron` 作業。 | 物件 | 否
`cron.cron.expression` | 觸發轉換的 `cron` 運算式。如需語法，請參閱 [Cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/#cron-expressions)。 | 字串 | 是
`cron.cron.timezone` | 觸發轉換的 `cron` 運算式所使用的時區。 | 字串 | 是

所有以時間為基礎的值 (`min_index_age`、`min_rollover_age`、`min_state_age`) 都使用[標準 OpenSearch 時間單位]({{site.url}}{{site.baseurl}}/api-reference/units/#time-units)。
{: .note}


下列範例會在 30 天後將索引轉換至 `cold` 狀態：

```json
"transitions": [
  {
    "state_name": "cold",
    "conditions": {
      "min_index_age": "30d"
    }
  }
]
```

ISM 會根據 `job_interval` [設定]({{site.url}}{{site.baseurl}}/im-plugin/ism/settings/)，在每次執行原則時檢查條件。

此範例使用 `cron` 條件，在每週六下午 5:00 (PT) 轉換索引：

```json
"transitions": [
  {
    "state_name": "cold",
    "conditions": {
      "cron": {
        "cron": {
          "expression": "* 17 * * SAT",
          "timezone": "America/Los_Angeles"
        }
      }
    }
  }
]
```

請注意，此條件不會在下午 5:00 準時執行；作業仍會依 `job_interval` 設定所定義的方式執行。由於開始時間有這樣的差異，加上動作可能需要一些時間才能完成，之後才會檢查轉換條件，因此我們不建議使用過於狹窄的 cron 運算式。例如，請勿使用 `15 17 * * SAT` (週六下午 5:15)。

此範例使用的一小時時間範圍通常已足夠，但您可以將它增加到 2 或 3 小時，以避免錯過時間範圍而必須等待一週才能進行轉換。或者，您也可以使用更廣泛的運算式，例如 `* * * * SAT,SUN`，讓轉換在週末的任何時間發生。

如需撰寫 cron 運算式的相關資訊，請參閱 [Cron 運算式]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/#cron-expressions)。


## 錯誤通知

當您受管理的索引失敗時，`error_notification` 會傳送通知。請在原則層級設定，與 `default_state` 和 `states` 並列：

```json
PUT _plugins/_ism/policies/hot_delete_workflow
{
  "policy": {
    "description": "hot delete workflow",
    "default_state": "hot",
    "error_notification": {
      "channel": {
        "id": "<channel_id>"
      },
      "message_template": {
        "source": "The index {% raw %}{{ctx.index}}{% endraw %} failed during policy execution."
      }
    },
    "states": [
      {
        "name": "hot",
        "actions": [],
        "transitions": []
      }
    ]
  }
}
```
{% include copy-curl.html %}

`error_notification` 需要 `message_template`，且必須指定 `destination` 或 `channel`，因此空物件會被拒絕並傳回 `400`。
{: .note}

錯誤通知會傳送至單一目的地或[通知頻道]({{site.url}}{{site.baseurl}}/notifications-plugin/index/)，並附上自訂訊息。

參數 | 說明 | 類型 | 必要
:--- | :--- |:--- |:--- |
`destination` | 目的地 URL。 | Slack、Amazon Chime 或 webhook URL | 若未指定 `channel` 則為必要
`channel` | 通知頻道的 ID | 字串 | 若未指定 `destination` 則為必要
`message_template` | 訊息的文字內容。您可以使用 [Mustache 範本](https://mustache.github.io/mustache.5.html) 在訊息中加入變數。 | 物件 | 必要

目的地系統**必須**傳回回應，否則 `error_notification` 操作會擲回錯誤。

### 範例 1：Chime 通知

```json
{
  "error_notification": {
    "destination": {
      "chime": {
        "url": "<url>"
      }
    },
    "message_template": {
      "source": "The index {% raw %}{{ctx.index}}{% endraw %} failed during policy execution."
    }
  }
}
```

### 範例 2：自訂 webhook 通知

```json
{
  "error_notification": {
    "destination": {
      "custom_webhook": {
        "url": "https://<your_webhook>"
      }
    },
    "message_template": {
      "source": "The index {% raw %}{{ctx.index}}{% endraw %} failed during policy execution."
    }
  }
}
```

### 範例 3：Slack 通知

```json
{
  "error_notification": {
    "destination": {
      "slack": {
        "url": "https://hooks.slack.com/services/xxx/xxxxxx"
      }
    },
    "message_template": {
      "source": "The index {% raw %}{{ctx.index}}{% endraw %} failed during policy execution."
    }
  }
}
```

### 範例 4：使用通知頻道

```json
{
  "error_notification": {
    "channel": {
      "id": "some-channel-config-id"
    },
    "message_template": {
      "source": "The index {% raw %}{{ctx.index}}{% endraw %} failed during policy execution."
    }
  }
}
```

您可以使用與 [Notification]({{site.url}}{{site.baseurl}}/im-plugin/ism/policies-operations/#notification) 操作相同的選項作為 `ctx` 變數。

## OpenSearch Dashboards 中的原則

若要前往 **Index Management** 頁面，請在頂端選單中前往 **Management > Index Management**。選取 **State management policies** 以列出叢集中的原則。

原則可透過視覺化編輯器或 JSON 編輯器建立。視覺化編輯器將原則的各部分呈現為獨立面板---錯誤通知、ISM 範本和狀態---並以清單列出可用的動作與轉換條件，因此適合用來撰寫新原則。若要貼上您已有的原則，請使用 JSON 編輯器。

下圖顯示 **State management policies** 頁面。

![狀態管理原則頁面]({{site.url}}{{site.baseurl}}/images/admin-ui-index/state-management-policies.png)

### 檢視原則

1. 在 **Index Management** 中，選取 **State management policies**。
1. 在 **Policy** 欄中選取原則。

頁面會顯示 **Policy settings**、**ISM templates** 和 **States** 面板。若要檢視某個狀態的動作與轉換，請選取該狀態名稱旁的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/arrow-right-icon.png" class="inline-icon" alt="expand icon"/>{:/} (展開) 圖示。

### 建立原則

1. 在 **Index Management** 中，選取 **State management policies**，然後選取 **Create policy**。
1. 選取 **Visual editor** 或 **JSON editor**，然後選取 **Continue**。
1. 在 **Policy info** 中，輸入描述原則用途的唯一 **Policy ID**，例如 `hot_cold_workflow`，並可選擇性地輸入說明。
1. 您可以選擇性地在 **Error notification** 中選取 **Channel ID**，以便在原則執行失敗時收到通知。如需更多資訊，請參閱 [錯誤通知](#error-notifications)。如果原則會自動輪替索引，請設定此通知：當輪替失敗時，它會提醒您索引異常龐大。
1. 您可以選擇性地在 **ISM templates** 中新增索引模式，將此原則附加至新索引。請參閱 [新增 ISM 範本](#adding-an-ism-template)。
1. 在 **States** 中，選取 **Add state** 以新增原則的每個狀態。請參閱 [新增狀態](#adding-a-state)。原則必須至少包含一個狀態。
1. 在 **Initial state** 中，選取新受管理索引起始所在的狀態。
1. 選取 **Create**。

在 JSON 編輯器中，於 **Name policy** 輸入原則 ID，於 **Define policy** 輸入原則，然後選取 **Create**。

### 新增狀態

在 **Create policy** 頁面的 **States** 中，選取 **Add state**，然後執行下列步驟：

1. 輸入描述索引生命週期階段的 **State name**，例如 `hot`、`warm` 或 `delete`。
1. 若要相對於已定義的狀態放置此狀態，請在 **Order** 中選取 **Add before** 或 **Add after**，然後選取要相對定位的狀態。第一個狀態可略過此步驟。
1. 對於該狀態執行的每個操作，請執行下列步驟：

   1. 選取 **Add action**。
   1. 選取 **Action type**。如需可用類型及其參數，請參閱 [ISM 支援的操作]({{site.url}}{{site.baseurl}}/im-plugin/ism/policies-operations/)。
   1. 輸入動作的參數。例如，快照動作需要儲存庫和快照名稱。
   1. 您可以選擇性地輸入動作失敗前的 **Timeout** 期間，例如 `5h`，以及 **Retry count**、**Retry backoff** 原則和 **Retry delay**，例如 `1d`。
   1. 選取 **Add action**。

1. 對於離開該狀態的每個轉換，請執行下列步驟：

   1. 選取 **Add transition**。
   1. 在 **Destination state** 中，選取要轉換到的狀態。若要將狀態轉換至自身，請輸入其名稱，因為清單中不會列出它。
   1. 選取 **Condition** 並輸入其參數。例如，最小文件數條件需要觸發轉換的文件數量。沒有條件的轉換一律評估為 `true`。
   1. 選取 **Add transition**。

1. 選取 **Save state**。

### 新增 ISM 範本

ISM 範本會將原則附加至名稱符合其索引模式之一的每個新索引：

1. 在 **Create policy** 頁面的 **ISM templates** 中，選取 **Add template**。
1. 在 **Index patterns** 中，輸入索引模式。例如，模式 `sample-index-*` 會將原則附加至名稱以 `sample-index-` 開頭的每個新索引。索引模式不可包含下列任何字元：`:`、`"`、`+`、`/`、`\`、`|`、`?`、`#`、`>` 或 `<`。
1. 在 **Priority** 中，輸入該模式的優先順序。當多個範本符合新索引的名稱時，ISM 會套用優先順序最高的範本。
1. 您可以選擇性地重複上述步驟以新增更多範本。

ISM 範本僅適用於在其之後建立的索引。如需更多資訊，請參閱 [將原則附加至新索引]({{site.url}}{{site.baseurl}}/im-plugin/ism/index/#attaching-a-policy-to-new-indexes)。

### 編輯政策

1. 在 **Index Management** 中，選取 **State management policies**。
1. 在 **Policy** 欄中選取該政策，然後選取 **Edit**。
1. 選取 **Visual editor** 或 **JSON editor**。
1. 變更政策的任何部分 (政策 ID 除外)，然後選取 **Update**。

變更會在政策下次執行時生效。在此之前，政策已管理的索引會繼續使用快取版本的政策。若要將受管理的索引移至其他政策，請參閱[受管理的索引]({{site.url}}{{site.baseurl}}/im-plugin/ism/managedindexes/)。

### 刪除政策

1. 在 **Index Management** 中，選取 **State management policies**。
1. 選取您要刪除之每個政策旁的核取方塊，然後選取 **Delete**。
1. 在確認對話方塊中選取 **Delete**。

已刪除的政策會立即停止管理其索引，且無法復原。
{: .warning}

