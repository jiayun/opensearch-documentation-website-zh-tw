---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "異常偵測器"
parent: Processors
grand_parent: Pipelines
nav_order: 30
---

# 異常偵測器處理器

`anomaly_detector` 處理器會接收結構化資料，並對該資料中您可設定的欄位執行異常偵測演算法。資料必須是整數或實數，異常偵測演算法才能偵測異常。在管線中將彙總處理器部署於 `anomaly_detector` 處理器之前，有助於您獲得最佳結果，因為彙總處理器會自動依索引鍵彙總事件，並將其保留在同一部主機上。例如，如果您要搜尋來自特定 IP 位址之延遲中的異常，且所有事件都傳送到同一部主機，該主機就會擁有這些事件的更多資料。這些額外資料能讓機器學習 (ML) 演算法獲得更好的訓練，進而帶來更好的異常偵測結果。

## 組態

您可以指定索引鍵及所選模式的選項，以設定 `anomaly_detector` 處理器。您可以使用下列選項來設定 `anomaly_detector` 處理器。

| 名稱 | 必要 | 說明 |
| :--- | :--- | :--- |
| `keys` | 是 | 無排序的 `List<String>`，作為 ML 演算法的輸入，用於偵測清單中各索引鍵值的異常。至少需要一個索引鍵。
| `mode` | 是 | 用於偵測異常的 ML 演算法 (或模型)。您必須提供模式。請參閱 [random_cut_forest 模式](#random_cut_forest-mode)。
| `identification_keys` | 否 | 若有提供，將在此索引鍵的每個唯一執行個體中偵測異常。例如，如果您提供 `ip` 欄位，將針對每個唯一 IP 位址分別偵測異常。
| `cardinality_limit` | 否 | 若使用 `identification_keys` 設定，將為每個基數建立新的 ML 模型。這可能會使用大量記憶體，因此設定模型數量上限會有所幫助。預設上限為 5000。
| `verbose` | 否 | RCF 會嘗試自動學習並減少偵測到的異常數量。例如，如果延遲一直介於 50 到 100 之間，然後突然跳升至約 1000，則只會偵測到轉變後的前一或兩個資料點 (除非有其他尖峰/異常)。同樣地，對於重複出現且達到相同程度的尖峰，RCF 可能會在最初幾個尖峰之後排除其中許多尖峰。這是因為預設設定是將偵測到的警示數量降至最低。將 `verbose` 設定設為 `true` 會使 RCF 持續偵測這些重複情況，這對於偵測持續一段較長時間的異常行為可能很有用。


### 索引鍵

`anomaly_detector` 處理器中使用的索引鍵存在於輸入事件中。例如，如果輸入事件為 `{"key1":value1, "key2":value2, "key3":value3}`，則該輸入事件中的任何索引鍵 (例如 `key1`、`key2`、`key3`) 都可以作為異常偵測器索引鍵，只要其值 (例如 `value1`、`value2`、`value3`) 為整數或實數即可。

<!-- vale off -->
### random_cut_forest 模式
<!-- vale on -->

隨機切割森林 (RCF) ML 演算法是一種非監督式演算法，用於偵測資料集中的異常資料點。為了偵測異常，`anomaly_detector` 處理器會使用 `random_cut_forest` 模式。

| 名稱 | 說明 |
| :--- | :--- |
| `random_cut_forest` | 使用 RCF ML 演算法處理事件以偵測異常。 | 

RCF 是一種非監督式 ML 演算法，用於偵測資料集中的異常資料點。OpenSearch Data Prepper 會將所設定索引鍵的值傳遞給 RCF，以使用 RCF 偵測資料中的異常。例如，當傳送延遲值為 11.5 的事件時，會產生下列異常事件：


```json
{ "latency": 11.5, "deviation_from_expected":[10.469302736820003],"grade":1.0}
```

在此範例中，`deviation_from_expected` 是各索引鍵與其對應預期值之偏差的清單，而 `grade` 是表示異常嚴重程度的異常等級。
     

您可以使用下列選項設定 `random_cut_forest` 模式。

| 名稱 | 預設值 | 範圍 | 說明 |
| :--- | :--- | :--- | :--- |
| `shingle_size` | `4` | 1--60 | ML 演算法中使用的 shingle 大小。 |
| `sample_size` | `256` | 100--2500 | ML 演算法中使用的樣本大小。 |
| `time_decay` | `0.1` | 0--1.0 | ML 演算法中使用的時間衰減值。在 ML 演算法中作為數學運算式 `timeDecay` 除以 `SampleSize` 使用。 |
| `type` | `metrics` | N/A | 傳送給演算法的資料類型。 |
| `output_after` | 32 | N/A | 指定在輸出任何偵測到的異常之前要處理的事件數量。 |
| `version` | `1.0` | N/A | 演算法版本號碼。 |

## 使用方式

若要開始使用，請建立下列 `pipeline.yaml` 檔案。您可以使用下列管線組態，在傳遞給處理器的事件中尋找 `latency` 欄位的異常。接著，您可以使用下列 YAML 組態檔案 `random_cut_forest` 模式來偵測異常：

```yaml
ad-pipeline:
  source:
    ...
  ....
  processor:
    - anomaly_detector:
        keys: ["latency"]
        mode:
            random_cut_forest:
```
{% include copy.html %}

當您執行 `anomaly_detector` 處理器時，處理器會擷取 `latency` 索引鍵的值，然後將該值傳遞給 RCF ML 演算法。您可以將任何以整數或實數為值的索引鍵設定為索引鍵。在下列範例中，您可以將 `bytes` 或 `latency` 設定為異常偵測器的索引鍵。

`{"ip":"1.2.3.4", "bytes":234234, "latency":0.2}`
