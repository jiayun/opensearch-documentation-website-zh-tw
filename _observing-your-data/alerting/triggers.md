---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "觸發條件"
nav_order: 40
grand_parent: Alerting
parent: Monitors
---

# 警示觸發條件

建立觸發條件的方式取決於建立監視器時所選擇的監視器方法。監視器方法包括 **Visual editor**、**Extraction query editor** 和 **Anomaly detector**。請參閱下列各節，進一步了解每種類型。

## 建立觸發條件

若要建立觸發條件：

1. 在 **Create monitor** 視窗中，選取 **Add trigger**。
<!-- vale off -->
2. 輸入觸發條件名稱、嚴重性等級和觸發條件。嚴重性等級範圍從 1 (最高) 到 5 (最低)，可用於管理警示。例如，嚴重性等級高的觸發條件 (例如 1 或 2) 可能會通知特定人員，而嚴重性等級低的觸發條件 (4 或 5) 則可能通知聊天室。觸發條件包括「IS ABOVE」、「IS BELOW」和「IS EXACTLY」。
<!-- vale on -->

查詢層級監視器會針對查詢結果執行一次觸發條件的指令碼，而桶層級監視器則會在每個桶上執行觸發條件的指令碼。請建立最適合監視器方法的觸發條件。若要執行多個指令碼，您必須建立多個觸發條件。
{: .note}

## Visual editor

對於查詢層級監視器的觸發條件，請為您建立監視器時所選擇的彙總和時間範圍指定閾值 (例如「IS BELOW 1,000」或「IS EXACTLY 10」)。當您增加或減少閾值時，該線會上下移動。一旦數值跨越此線，觸發條件就會評估為 `true`。

對於桶層級監視器，您必須為彙總和時間範圍指定閾值和值。您最多可以使用五個條件來精簡觸發條件。此外，您也可以選擇使用關鍵字篩選器，篩選索引中的特定欄位。

對於文件層級監視器，請使用代表多個查詢的標籤，這些查詢由邏輯 `OR` 運算子連接。若要建立多重查詢觸發條件：

1. 選取 **Per document monitor**。
2. 選取資料來源。
3. 輸入查詢名稱和欄位資訊。例如，將查詢設定為使用「is」或「is not」運算子搜尋 `region` 欄位，並將值設為「us-west-2」。
4. 選取 **Add tag** 並輸入標籤名稱。
5. 選取 **Add another query** 建立第二個查詢，並為其加入相同的標籤。

現在您可以建立觸發條件並指定標籤名稱。這會建立一個組合觸發條件，檢查兩個都包含相同標籤的查詢。監視器會以邏輯 `OR` 運算檢查這兩個查詢，若任一查詢的條件符合，就會產生警示通知。

## Extraction query editor

對於查詢層級監視器，請指定會傳回 `true` 或 `false` 的 Painless 指令碼。Painless 是 OpenSearch 的預設指令碼語言，其語法類似 Groovy。如需更多資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

觸發條件指令碼以 `ctx.results[0]` 變數為核心，該變數對應至擷取查詢的回應。例如，指令碼可能會參照 `ctx.results[0].hits.total.value` 或 `ctx.results[0].hits.hits[i]._source.error_code`。

傳回值為 `true` 表示觸發條件已符合，觸發條件應執行其動作。請使用 **Run** 按鈕測試指令碼。

**Trigger condition** 旁的 **Info** 連結包含查詢可用變數和結果的實用摘要。
{: .tip }

桶層級監視器需要在觸發條件中指定更多資訊。至少必須包含下列欄位：

- `buckets_path`：將變數名稱對應至指令碼中使用的指標。
- `parent_bucket_path`：多重桶彙總的路徑。路徑可以包含單桶彙總，但最後一個彙總必須是多重桶彙總。例如，如果您有一個類似 `agg1>agg2>agg3` 的管線，`agg1` 和 `agg2` 是單桶彙總，但 `agg3` 必須是多重桶彙總。
- `script`：OpenSearch 用來評估是否觸發任何警示的指令碼。

以下是指令碼範例：

```json
{
  "buckets_path": {
    "count_var": "_count"
  },
  "parent_bucket_path": "composite_agg",
  "script": {
    "source": "params.count_var > 5"
  }
}
```

將 `count_var` 變數對應至 `_count` 指標後，您就可以在指令碼中使用 `count_var` 並參照 `_count` 資料。`composite_agg` 是多重桶彙總的路徑。

## Anomaly detector

若要使用異常偵測器方法：

1. 在 **Trigger type** 中，選擇 **Anomaly detector grade and confidence**。
2. 為您建立監視器時所選擇的彙總和時間範圍指定 **Anomaly grade condition**，例如「IS ABOVE 0.7」或「IS EXACTLY 0.5」。*異常等級* 是介於 0 和 1 之間的數字，表示資料點的異常程度。
3. 為先前選擇的彙總和時間範圍指定 **Anomaly confidence condition**，例如「IS ABOVE 0.7」或「IS EXACTLY 0.5」。*異常信賴度* 是對所回報異常等級符合預期異常等級之機率的估計值。當您增加或減少閾值時，該線會上下移動。一旦數值跨越此線，觸發條件就會評估為 `true`。

### 範例指令碼


```groovy
// Evaluates to true if the query returned any documents
ctx.results[0].hits.total.value > 0
```

```groovy
// Returns true if the avg_cpu aggregation exceeds 90
if (ctx.results[0].aggregations.avg_cpu.value > 90) {
  return true;
}
```

```groovy
// Performs some crude custom scoring and returns true if that score exceeds a certain value
int score = 0;
for (int i = 0; i < ctx.results[0].hits.hits.length; i++) {
  // Weighs 500 errors 10 times as heavily as 503 errors
  if (ctx.results[0].hits.hits[i]._source.http_status_code == "500") {
    score += 10;
  } else if (ctx.results[0].hits.hits[i]._source.http_status_code == "503") {
    score += 1;
  }
}
if (score > 99) {
  return true;
} else {
  return false;
}
```

#### 觸發條件變數

變數 | 資料類型 | 說明
:--- | :--- | :---
`ctx.trigger.id` | 字串 | 觸發條件 ID。
`ctx.trigger.name` | 字串 | 觸發條件名稱。
`ctx.trigger.severity` | 字串 | 觸發條件嚴重性。
`ctx.trigger.condition`| 物件 | 包含建立監視器時所使用的 Painless 指令碼。
`ctx.trigger.condition.script.source` | 字串 | 用來定義觸發條件的指令碼。
`ctx.trigger.condition.script.lang` | 字串 | 用來定義指令碼的語言。必須是 Painless。
`ctx.trigger.actions`| 陣列 | 包含一個元素的陣列，其中含有監視器需要觸發之動作的資訊。

#### 其他變數

變數 | 資料類型 | 說明
:--- | :--- | :---
`ctx.results` | 陣列 | 包含一個元素 (`ctx.results.0`) 的陣列。含有查詢結果。如果觸發條件無法擷取結果，此變數為空。請參閱 `ctx.error`。
`ctx.last_update_time` | 毫秒 | 監視器上次更新的 Unix 紀元時間。
`ctx.periodStart` | 字串 | 觸發警示之期間開始的 Unix 時間戳記。例如，如果監視器每 10 分鐘執行一次，期間可能從 10:40 開始，到 10:50 結束。
`ctx.periodEnd` | 字串 | 觸發警示之期間的結束時間。
`ctx.error` | 字串 | 如果觸發條件無法擷取結果或無法評估時所顯示的錯誤訊息，通常是由於編譯錯誤或空指標例外狀況。否則為 Null。
`ctx.alert` | 物件 | 目前作用中的警示 (如果存在)。包含 `ctx.alert.id`、`ctx.alert.version` 和 `ctx.alert.isAcknowledged`。如果沒有作用中的警示則為 Null。僅適用於查詢層級監視器。
`ctx.alerts` | 陣列 | 新建立的警示。包含觸發警示的 `ctx.alerts.0.finding_ids` 以及與發現結果相關聯的 `ctx.alerts.0.related_doc_ids`。僅適用於文件層級監視器。
`ctx.dedupedAlerts` | 陣列 | 已觸發的警示。OpenSearch 會保留現有的警示，以防止外掛程式不斷建立相同的警示。僅適用於桶層級監視器。
`ctx.newAlerts` | 陣列 | 新建立的警示。僅適用於桶層級監視器。
`ctx.completedAlerts` | 陣列 | 已完成或已到期的警示。僅適用於桶層級監視器。
`bucket_keys` | 字串 | 監視器桶鍵值的逗號分隔清單。僅適用於 `ctx.dedupedAlerts`、`ctx.newAlerts` 和 `ctx.completedAlerts`。透過 `ctx.dedupedAlerts.0.bucket_keys` 變數存取。
`parent_bucket_path` | 字串 | 觸發警示之桶的上層桶路徑。透過 `ctx.dedupedAlerts.0.parent_bucket_path` 存取。
`associated_queries` | 陣列 | 觸發建立與警示相關聯之發現結果的文件層級監視器查詢陣列。僅適用於文件層級監視器。透過 `ctx.alerts.0.associated_queries` 變數存取。
`sample_documents` | 陣列 | 符合監視器查詢的範例文件陣列。僅適用於桶層級和文件層級監視器。分別透過 `ctx.newAlerts.0.sample_documents` 和 `ctx.alerts.0.sample_documents` 變數存取。

#### `associated_queries` 和 `sample_documents` 變數

每桶與每文件監視器支援在通知訊息中列印範例文件。每文件監視器支援列印觸發建立與警示相關聯之發現結果的查詢清單。當監視器執行時，它會將每個新警示加入 `ctx` 變數，例如每桶監視器為 `newAlerts`，每文件監視器為 `alerts`。每個警示都有自己的 `sample_documents` 清單，且每個每文件監視器警示都有自己的 `associated_queries` 清單。訊息範本可以格式化為逐一迭代警示清單、`associated_queries` 清單，以及每個警示的 `sample_documents`。

警示監視器會使用建立它的使用者的權限。請留意警示訊息傳送至的 Notifications 外掛程式頻道，以及訊息 mustache 範本的內容。若要進一步了解 Alerting 外掛程式中的安全性，請參閱[警示安全性]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/security/)。
{: .note}

#### 範例文件變數

變數 | 資料類型 | 說明
:--- | :--- | :---
`_index` | 字串 | 包含範例文件的索引。
`_id` | 字串 | 範例文件 ID。
`_score` | 浮點數 | 一個正 32 位元浮點數，說明所傳回文件的相關性。
`_source` | 物件 | 範例文件的 JSON 承載。

##### Mustache 範本範例

{% raw %}
```groovy
Alerts:
{{#ctx.alerts}}
    RULES
    {{#associated_queries}}
        Name: {{name}}
        Id: {{id}}
        Tags: {{tags}}
    ------------------------
    {{/associated_queries}}
{{/ctx.alerts}}
```
{% endraw %}

#### 相關聯的查詢變數

變數 | 資料類型 | 說明
:--- | :--- | :---
`id` | 字串 | 文件層級查詢的 ID。
`name` | 字串 | 文件層級查詢的名稱。
`tags` | 陣列 | 為文件層級查詢設定的標籤陣列 (每個標籤的類型為字串)。

##### Mustache 範本範例

此範例中的 `_source` 物件是以 OpenSearch Dashboards 中提供的 `opensearch_dashboards_sample_data_ecommerce` 索引為基礎。在此範例中，訊息範本正在存取每文件監視器的 `ctx.alerts` 變數。
{: .note}

{% raw %}
```groovy
Alerts
{{#ctx.alerts}}
    Sample documents:
    {{#sample_documents}}
        Index: {{_index}}
        Document ID: {{_id}}
       
        Order date: {{_source.order_date}}
        Order ID: {{_source.order_id}}
        Clothing category: {{_source.category}}
        -----------------
    {{/sample_documents}}
{{/ctx.alerts}}
```
{% endraw %}