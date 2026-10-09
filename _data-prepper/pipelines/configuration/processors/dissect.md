---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Dissect
parent: Processors
grand_parent: Pipelines
nav_order: 120
---

# Dissect 處理器
 
`dissect` 處理器會從事件中擷取值，並根據使用者定義的 `dissect` 模式，將這些值對應至個別欄位。此處理器非常適合從結構已知的記錄檔訊息中擷取欄位。 

## 基本用法

若要使用 `dissect` 處理器，請建立下列 `pipeline.yaml` 檔案：

```yaml
dissect-pipeline:
  source:
    file:
      path: "/full/path/to/logs_json.log"
      record_type: "event"
      format: "json"
  processor:
    - dissect:
        map:
          log: "%{Date} %{Time} %{Log_Type}: %{Message}"
  sink:
    - stdout:
```
{% include copy.html %}

接著建立名為 `logs_json.log` 的下列檔案，並將 `pipeline.yaml` 檔案之檔案來源中的 `path` 替換為包含下列 JSON 資料之檔案的路徑：

```json
{"log": "07-25-2023 10:00:00 ERROR: error message"}
```

`dissect` 處理器會根據管線中設定的模式 `%{Date} %{Time} %{Type}: %{Message}`，從 `log` 訊息中擷取欄位（`Date`、`Time`、`Log_Type` 和 `Message`）。

執行管線後，您應該會收到下列標準輸出：

```json
{
    "log" : "07-25-2023 10:00:00 ERROR: Some error",
    "Date" : "07-25-2023"
    "Time" : "10:00:00"
    "Log_Type" : "ERROR"
    "Message" : "error message"
}
```

## 組態

您可以使用下列選項設定 `dissect` 處理器。

| 選項 | 必要 | 類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `map` | 是 | Map | 為特定索引鍵定義 `dissect` 模式。如需在 `dissect` 模式中定義欄位的詳細資訊，請參閱[欄位標記法](#field-notations)。 |
| `target_types` | 否 | Map | 指定擷取欄位的資料類型。有效選項為 `integer`、`double`、`string` 和 `boolean`。預設情況下，所有欄位皆為 `string` 類型。 |
| `delete_source` | 否 | 布林值 | 是否在成功剖析後刪除來源欄位。預設為 `false`。 |
| `dissect_when` | 否 | 字串 | 使用 [Data Prepper 運算式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/expression-syntax/)指定執行 `dissect` 作業的條件。若有指定，`dissect` 作業只會在運算式評估為 true 時執行。 |

### 欄位標記法

您可以使用下列欄位類型定義 `dissect` 模式。

#### 一般欄位

不含後置詞或前置詞的欄位。此欄位會直接新增至輸出事件。格式為 `%{field_name}`。

#### 略過欄位

不會包含在事件中的欄位。格式為 `%{}` 或 `%{?field_name}`。

#### 附加欄位

會與其他欄位合併的欄位。若要附加多個值並將最終值納入欄位中，請在 `dissect` 模式中的欄位名稱前使用 `+`。格式為 `%{+field_name}`。 

例如，使用模式 `%{+field_name}, %{+field_name}` 時，記錄檔訊息 `"foo, bar"` 會剖析為 `{"field_name": "foobar"}`。

您也可以藉由後置詞 `/<integer>` 定義串連的順序。 

例如，使用模式 `"%{+field_name/2}, %{+field_name/1}"` 時，記錄檔訊息 `"foo, bar"` 會剖析為 `{"field_name": "barfoo"}`。

若未指定順序，附加作業會依照 `dissect` 模式中所指定欄位的順序進行。 

#### 間接欄位

使用另一個欄位的值作為其欄位名稱的欄位。定義模式時，請在欄位前加上 `&`，以將該欄位中找到的值指派為鍵值組中的索引鍵。

例如，使用模式 `"%{?field_name}, %{&field_name}"` 時，記錄檔訊息 `"foo, bar"` 會剖析為 `{“foo”: “bar”}`。在此記錄檔訊息中，`foo` 是從略過欄位 `%{?field_name}` 擷取而來。接著，`foo` 會作為從欄位 `%{&field_name}` 擷取之值的索引鍵。

#### 填補欄位

移除右側填補內容的欄位。`->` 運算子可作為後置詞使用，表示可忽略此欄位之後的空白字元。

例如，使用模式 `%{field1->} %{field2}` 時，記錄檔訊息 `“firstname    lastname”` 會剖析為 `{“field1”: “firstname”, “field2”: “lastname”}`。
