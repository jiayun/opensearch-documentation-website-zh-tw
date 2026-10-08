---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用儀表板變數"
parent: Dashboard variables
grand_parent: Creating visualizations using queries
great_grand_parent: Building data visualizations
nav_order: 20
---

# 使用儀表板變數

您可以在視覺化編輯器的查詢中參照儀表板變數，以建立動態的互動式儀表板。

## 變數語法

您可以使用下列語法選項，在查詢中參照儀表板變數。

### 基本語法

大多數情況請使用 `$variableName`：

```sql
source=logs | where service='$service' | stats count() by region
```
{% include copy.html %}

### 大括號語法

當變數名稱後方緊接其他字元且沒有空白時，請使用 `${variableName}`：

```sql
source = logs | where ${env}_level = "error"
```
{% include copy.html %}

大括號語法可確保變數名稱正確分隔。若未使用大括號，`$env_level` 會被解譯為名為 `env_level` 的變數，而非 `env`。

## 在查詢中使用變數

儀表板變數支援 Piped Processing Language (PPL) 和 Prometheus Query Language (PromQL)。下列範例使用 PPL。

#### 用於篩選的單值變數

下列查詢會依單值變數篩選記錄檔：

```sql
source=logs | where service='$service' | stats count() by status_code
```
{% include copy.html %}

當 `service` 設為 `api` 時，查詢會解析為：

```sql
source=logs | where service='api' | stats count() by status_code
```

#### 用於篩選的多值變數

下列查詢會依多值變數篩選記錄檔：

```sql
source=logs | where region IN $region | stats count() by service
```
{% include copy.html %}

當 `region` 選取了多個值（`us-east`、`us-west`）時，查詢會解析為：

```sql
source=logs | where region IN ('us-east', 'us-west') | stats count() by service
```

#### 數值的多值變數

當查詢變數的選項被偵測為數值或布林值時，多個值的格式不會加上引號：

```sql
source=logs | where status_code IN $status | stats count()
```
{% include copy.html %}

當 `status` 選取了多個數值時，查詢會解析為：

```sql
source=logs | where status_code IN (200, 404, 500) | stats count()
```

#### 用於分組維度的變數

下列查詢使用變數來控制分組維度：

```sql
source=logs | stats count() by `$group_by`
```
{% include copy.html %}

當 `group_by` 設為 `region` 時，查詢會解析為：

```sql
source=logs | stats count() by region
```

#### 用於時間間隔的變數

下列查詢使用變數來控制時間間隔：

```sql
source=logs | stats count() by span(timestamp, $interval)
```
{% include copy.html %}

當 `interval` 設為 `5m` 時，查詢會解析為：

```sql
source=logs | stats count() by span(timestamp, 5m)
```

#### 用於指標計算的變數

下列查詢使用變數來控制要計算的指標：

```sql
source=metrics | stats avg($metric) by service
```
{% include copy.html %}

當 `metric` 設為 `response_time` 時，查詢會解析為：

```sql
source=metrics | stats avg(response_time) by service
```

### 多值變數格式

當變數允許多重選取時，系統會根據查詢語言自動格式化各個值。

<table>
  <thead>
    <tr>
      <th>查詢語言</th>
      <th>字串值</th>
      <th>數值或布林值</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PPL</td>
      <td><code>('value1', 'value2')</code></td>
      <td><code>(123, 456)</code></td>
    </tr>
    <tr>
      <td>PromQL</td>
      <td><code>(value1|value2)</code></td>
      <td><code>(value1|value2)</code></td>
    </tr>
    <tr>
      <td>其他</td>
      <td><code>value1, value2</code></td>
      <td><code>value1, value2</code></td>
    </tr>
  </tbody>
</table>

### 自動完成建議

OpenSearch Dashboards 中的查詢編輯器會為儀表板變數提供自動完成建議。

1. 在查詢編輯器中輸入 `$`。畫面上會出現下拉式清單，顯示所有可用的儀表板變數。
1. 從清單中選取變數，或繼續輸入以進行篩選，如下圖所示。

   ![查詢編輯器顯示含有可用儀表板變數的自動完成下拉式清單]({{site.url}}{{site.baseurl}}/images/dashboard-variables/variable_autocomplete.png)
1. 按下 Enter 或 Tab 鍵以插入變數。

## 在視覺化中使用變數

儀表板變數與 OpenSearch Dashboards 視覺化編輯器整合；從儀表板編輯視覺化時，視覺化編輯器完整支援儀表板變數。

### 依變數值篩選

變數可作為視覺化中的篩選條件。您不必將篩選條件套用至整個儀表板，而是可以將變數直接嵌入 PPL 查詢，針對特定面板進行篩選。

若要依變數值篩選視覺化，請依照下列步驟操作：

1. 建立 `machine_os` 變數：
   1. 在您的 Observability 工作區中，選取左側導覽列中的 **Dashboards**。
   1. 開啟現有的儀表板，或選取 **Create** > **Dashboard** 以建立新的儀表板。若要建立新的儀表板，請先輸入標題並選取 **Save** 加以儲存。
   1. 在儀表板頂端選取 **Add variable**。
   1. 在 **Name** 中輸入 `machine_os`。在 **Type** 中選取 **Query**。在 **Options Query** 中選取 `opensearch_dashboards_sample_data_logs`。在查詢方塊中輸入下列查詢：
   
      ```sql
      | FIELDS `machine.os`
      ```
      {% include copy.html %}
   1. 選取 **Preview**，並確認 **Preview of values** 中顯示 `win 8`、`ios` 和 `win xp` 等值。接著選取 **Add variable** 以儲存。


1. 依變數值篩選：
   1. 在儀表板中選取 **Create new**，然後選取 **Add visualization**，以開啟新的視覺化編輯器。 
   1. 在時間篩選器中選取 **Last 30 days**。
   1. 在查詢方塊中輸入下列查詢：

   ```sql
   | WHERE `machine.os` = '${machine_os}' | STATS avg(memory) BY span(`@timestamp`, 1d) 
   ```
   {% include copy.html %}

   若要依 `machine_os` 值篩選視覺化，請在 `machine_os` 下拉式清單中選取值（例如選取 `win 8`），如下圖所示。

   ![視覺化編輯器顯示依 machine_os 設為 win 8 篩選後的平均記憶體隨時間變化]({{site.url}}{{site.baseurl}}/images/dashboard-variables/filter_case_variable.png)
   
### 動態選取指標

使用變數來控制彙總中使用的欄位。如此一來，您無需編輯查詢，即可在不同指標之間切換（例如 `memory` 和 `bytes`）。

若要動態選取指標，請依照下列步驟操作：

1. 建立 `log_metric` 變數：
   1. 在您的 Observability 工作區中，選取左側導覽列中的 **Dashboards**。
   1. 開啟現有的儀表板，或選取 **Create** > **Dashboard** 以建立新的儀表板。若要建立新的儀表板，請先輸入標題並選取 **Save** 加以儲存。
   1. 在儀表板頂端選取 **Add variable**。
   1. 在 **Name** 中輸入 `log_metric`。在 **Type** 中選取 **Custom**。在 **Custom options** 中輸入 `memory`，然後按下 **Enter** 新增。接著輸入 `bytes`，然後按下 **Enter** 新增。 
   1. 選取 **Add variable** 以儲存。

1. 在視覺化中使用變數：
   1. 在儀表板中選取 **Create new**，然後選取 **Add visualization**，以開啟新的視覺化編輯器。 
   1. 在時間篩選器中選取 **Last 30 days**。
   1. 在查詢方塊中輸入下列查詢：

      ```sql
      source=opensearch_dashboards_sample_data_logs
      | stats avg($log_metric) as avg_${log_metric} by span(`timestamp`, 1h) as timestamp, response
      ```
      {% include copy.html %}

   若要在不同指標之間切換，請在 `log_metric` 下拉式清單中選取值（例如選取 `memory` 或 `bytes`）。

   ![視覺化編輯器顯示 log_metric 變數設為 memory 時的平均記憶體隨時間變化]({{site.url}}{{site.baseurl}}/images/dashboard-variables/metrics_case_variable.png)

### 動態變更時間間隔

使用變數，讓儀表板檢視者無須編輯查詢，即可在不同的時間彙總間隔之間切換（例如 `1h`、`6h` 或 `1d`）。

若要動態變更時間間隔，請依照下列步驟操作：

1. 建立 `interval` 變數：
   1. 在您的 Observability 工作區中，於左側導覽列選取 **Dashboards**。
   1. 開啟現有的儀表板，或選取 **Create** > **Dashboard** 以建立新的儀表板。若要建立新的儀表板，請先輸入標題並選取 **Save** 加以儲存。
   1. 在儀表板頂端，選取 **Add variable**。
   1. 在 **Name** 中輸入 `interval`。在 **Type** 中選取 **Custom**。在 **Custom options** 中輸入 `1d`，然後按 **Enter** 加入。對 `12h`、`6h` 和 `1h` 重複此步驟。
   1. 選取 **Add variable** 以儲存。

1. 在視覺化中使用變數：
   1. 在儀表板中選取 **Create new**，然後選取 **Add visualization**，以開啟新的視覺化編輯器。
   1. 在時間篩選器中，選取 **Last 30 days**。
   1. 在查詢方塊中，輸入下列查詢：

      ```sql
      source=opensearch_dashboards_sample_data_logs | stats AVG(`bytes`) as avg_bytes, MAX(`bytes`) as max_bytes by span(`timestamp`, $interval)
      ```
      {% include copy.html %}

   若要在不同間隔之間切換，請在 `interval` 下拉式清單中選取一個值（例如選取 `6h`），然後選取 **Update**。視覺化會反映所選的時間分桶方式，如下圖所示。

   ![視覺化編輯器顯示 avg_bytes 和 max_bytes 隨時間的變化，interval 變數設為 1d]({{site.url}}{{site.baseurl}}/images/dashboard-variables/interval_case_variable.png)

### 動態變更彙總函式

使用變數，讓儀表板檢視者無須編輯查詢，即可在不同的彙總函式之間切換（例如 `avg`、`max` 或 `min`）。

若要動態變更彙總函式，請依照下列步驟操作：

1. 建立 `function` 變數：
   1. 在您的 Observability 工作區中，於左側導覽列選取 **Dashboards**。
   1. 開啟現有的儀表板，或選取 **Create** > **Dashboard** 以建立新的儀表板。若要建立新的儀表板，請先輸入標題並選取 **Save** 加以儲存。
   1. 在儀表板頂端，選取 **Add variable**。
   1. 在 **Name** 中輸入 `function`。在 **Type** 中選取 **Custom**。在 **Custom options** 中輸入 `avg`，然後按 **Enter** 加入。對 `max` 和 `min` 重複此步驟。
   1. 選取 **Add variable** 以儲存。

1. 在視覺化中使用變數：
   1. 在儀表板中選取 **Create new**，然後選取 **Add visualization**，以開啟新的視覺化編輯器。
   1. 在時間篩選器中，選取 **Last 30 days**。
   1. 在查詢方塊中，輸入下列查詢：

      ```sql
      | STATS ${function}(memory) BY span(`@timestamp`, 1d)
      ```
      {% include copy.html %}

   若要在不同函式之間切換，請在 `function` 下拉式清單中選取一個值（例如選取 `max`），然後選取 **Update**。視覺化會反映所選的彙總函式，如下圖所示。

   ![視覺化編輯器顯示平均記憶體隨時間的變化，function 變數設為 avg]({{site.url}}{{site.baseurl}}/images/dashboard-variables/function_case_variable.png)

## 串聯變數與跨面板變數

下列章節說明進階的變數使用案例。

### 串聯變數

建立相依變數，讓一個變數篩選另一個變數的選項。例如，先選取區域，再從該區域中可用的服務進行選取。

建立 `region` 變數：

```sql
source=logs | dedup region | fields region
```
{% include copy.html %}

建立參照 `region` 的 `service` 變數：

```sql
source=logs | where region='$region' | dedup service | fields service
```
{% include copy.html %}

當 `region` 的值變更時，`service` 變數會自動重新整理其選項，僅顯示所選區域中的服務。

### 跨面板篩選

使用單一變數同時篩選多個視覺化。例如，建立 `service` 變數，並在多個視覺化編輯器中參照該變數。

視覺化編輯器 1（依服務統計的請求數）：

```sql
source=logs | where service='$service' | stats count() by status_code
```
{% include copy.html %}

視覺化編輯器 2（依服務統計的回應時間）：

```sql
source=metrics | where service='$service' | stats avg(response_time)
```
{% include copy.html %}

變更 `service` 變數的值，會同時更新這兩個視覺化編輯器。

## 後續步驟

- [建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)
