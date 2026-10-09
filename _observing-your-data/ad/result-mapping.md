---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "異常結果對應"
parent: Anomaly detection
nav_order: 6
redirect_from: 
  - /monitoring-plugins/ad/result-mapping/
---

# 異常結果對應

當您在 **Custom result index** 窗格中選取 **Enable custom result index** 方塊時，Anomaly Detection 外掛程式會將結果儲存到您選擇的索引。當異常偵測器未偵測到異常時，結果格式如下：

```json
{
  "detector_id": "kzcZ43wBgEQAbjDnhzGF",
  "schema_version": 5,
  "data_start_time": 1635898161367,
  "data_end_time": 1635898221367,
  "feature_data": [
    {
      "feature_id": "processing_bytes_max",
      "feature_name": "processing bytes max",
      "data": 2322
    },
    {
      "feature_id": "processing_bytes_avg",
      "feature_name": "processing bytes avg",
      "data": 1718.6666666666667
    },
    {
      "feature_id": "processing_bytes_min",
      "feature_name": "processing bytes min",
      "data": 1375
    },
    {
      "feature_id": "processing_bytes_sum",
      "feature_name": "processing bytes sum",
      "data": 5156
    },
    {
      "feature_id": "processing_time_max",
      "feature_name": "processing time max",
      "data": 31198
    }
  ],
  "execution_start_time": 1635898231577,
  "execution_end_time": 1635898231622,
  "anomaly_score": 1.8124904404395776,
  "anomaly_grade": 0,
  "confidence": 0.9802940756605277,
  "entity": [
    {
      "name": "process_name",
      "value": "process_3"
    }
  ],
  "model_id": "kzcZ43wBgEQAbjDnhzGF_entity_process_3",
  "threshold": 1.2368549346675202
}
```
{% include copy-curl.html %}

## 回應本文欄位

欄位 | 說明
:--- | :---
`detector_id` | 用於識別偵測器的唯一 ID。
`schema_version` | 結果索引的對應版本。
`data_start_time` | 彙總資料偵測範圍的開始時間。
`data_end_time` | 彙總資料偵測範圍的結束時間。
`feature_data` | `data_start_time` 與 `data_end_time` 之間彙總資料點的陣列。
`execution_start_time` | 產生異常結果的特定執行中，偵測器的實際開始時間。此開始時間包含您可設定以延遲資料收集的 window delay 參數。Window delay 是 `execution_start_time` 與 `data_start_time` 之間的差異。
`execution_end_time` | 產生異常結果的特定執行中，偵測器的實際結束時間。
`anomaly_score` | 指出異常的相對嚴重性。分數越高，資料點就越異常。
`anomaly_grade` | `anomaly_score` 的正規化版本，範圍介於 0 與 1 之間。
`confidence` | `anomaly_score` 準確度的機率。此數字越接近 1，準確度越高。在執行中偵測器的觀察期間，由於其暴露於有限的資料，信心水準會偏低（< 0.9）。
`entity` | 實體是特定類別欄位值的組合。它包含類別欄位的名稱與值。在前述範例中，`process_name` 是類別欄位，而 `process_3` 等其中一個處理程序則是該欄位的值。`entity` 欄位僅存在於高基數偵測器（您已選取類別欄位者）。
`model_id` | 用於識別模型的唯一 ID。如果偵測器是單一串流偵測器（沒有類別欄位），則它只有一個模型。如果偵測器是高基數偵測器（具有一或多個類別欄位），則它可能有多個模型，每個實體各一個。
`threshold` | 偵測器將資料點分類為異常的準則之一，是其 `anomaly_score` 必須超過動態閾值。此欄位會記錄目前的閾值。

當啟用插補選項時，異常結果會包含 `feature_imputed` 陣列，顯示哪些特徵因資料遺漏而遭到修改。如果沒有插補任何特徵，則會排除此項。

在下列異常結果輸出範例中，`processing_bytes_max` 特徵已插補，如 `imputed: true` 狀態所示：

```json
{
    "detector_id": "kzcZ43wBgEQAbjDnhzGF",
    "schema_version": 5,
    "data_start_time": 1635898161367,
    "data_end_time": 1635898221367,
    "feature_data": [
        {
            "feature_id": "processing_bytes_max",
            "feature_name": "processing bytes max",
            "data": 2322
        },
        {
            "feature_id": "processing_bytes_avg",
            "feature_name": "processing bytes avg",
            "data": 1718.6666666666667
        },
        {
            "feature_id": "processing_bytes_min",
            "feature_name": "processing bytes min",
            "data": 1375
        },
        {
            "feature_id": "processing_bytes_sum",
            "feature_name": "processing bytes sum",
            "data": 5156
        },
        {
            "feature_id": "processing_time_max",
            "feature_name": "processing time max",
            "data": 31198
        }
    ],
    "execution_start_time": 1635898231577,
    "execution_end_time": 1635898231622,
    "anomaly_score": 1.8124904404395776,
    "anomaly_grade": 0,
    "confidence": 0.9802940756605277,
    "entity": [
        {
            "name": "process_name",
            "value": "process_3"
        }
    ],
    "model_id": "kzcZ43wBgEQAbjDnhzGF_entity_process_3",
    "threshold": 1.2368549346675202,
    "feature_imputed": [
        {
            "feature_id": "processing_bytes_max",
            "imputed": true
        },
        {
            "feature_id": "processing_bytes_avg",
            "imputed": false
        },
        {
            "feature_id": "processing_bytes_min",
            "imputed": false
        },
        {
            "feature_id": "processing_bytes_sum",
            "imputed": false
        },
        {
            "feature_id": "processing_time_max",
            "imputed": false
        }
    ]
}
```
{% include copy-curl.html %}

當偵測到異常時，結果會以下列格式提供：

```json
{
  "detector_id": "fylE53wBc9MCt6q12tKp",
  "schema_version": 0,
  "data_start_time": 1635927900000,
  "data_end_time": 1635927960000,
  "feature_data": [
    {
      "feature_id": "processing_bytes_max",
      "feature_name": "processing bytes max",
      "data": 2291
    },
    {
      "feature_id": "processing_bytes_avg",
      "feature_name": "processing bytes avg",
      "data": 1677.3333333333333
    },
    {
      "feature_id": "processing_bytes_min",
      "feature_name": "processing bytes min",
      "data": 1054
    },
    {
      "feature_id": "processing_bytes_sum",
      "feature_name": "processing bytes sum",
      "data": 5032
    },
    {
      "feature_id": "processing_time_max",
      "feature_name": "processing time max",
      "data": 11422
    }
  ],
  "anomaly_score": 1.1986675882872033,
  "anomaly_grade": 0.26806225550178464,
  "confidence": 0.9607519742565531,
  "entity": [
    {
      "name": "process_name",
      "value": "process_3"
    }
  ],
  "approx_anomaly_start_time": 1635927900000,
  "relevant_attribution": [
    {
      "feature_id": "processing_bytes_max",
      "data": 0.03628638020431366
    },
    {
      "feature_id": "processing_bytes_avg",
      "data": 0.03384479053991436
    },
    {
      "feature_id": "processing_bytes_min",
      "data": 0.058812549572819096
    },
    {
      "feature_id": "processing_bytes_sum",
      "data": 0.10154576265526988
    },
    {
      "feature_id": "processing_time_max",
      "data": 0.7695105170276828
    }
  ],
  "expected_values": [
    {
      "likelihood": 1,
      "value_list": [
        {
          "feature_id": "processing_bytes_max",
          "data": 2291
        },
        {
          "feature_id": "processing_bytes_avg",
          "data": 1677.3333333333333
        },
        {
          "feature_id": "processing_bytes_min",
          "data": 1054
        },
        {
          "feature_id": "processing_bytes_sum",
          "data": 6062
        },
        {
          "feature_id": "processing_time_max",
          "data": 23379
        }
      ]
    }
  ],
  "threshold": 1.0993584705913992,
  "execution_end_time": 1635898427895,
  "execution_start_time": 1635898427803
}
```
{% include copy-curl.html %}

請注意，結果包含下列額外欄位。

欄位 | 說明
:--- | :---
`relevant_attribution` | 代表每個輸入變數的貢獻。歸因的總和會正規化為 1。
`expected_values` | 每個特徵的預期值。

偵測器可能會延遲偵測到異常。例如：偵測器觀察到一系列在「緩慢週」（以三元組 {1, 2, 3} 表示）與「忙碌週」（以三元組 {2, 4, 5} 表示）之間交替的資料。如果偵測器遇到模式 {2, 2, X}，而它尚未看到 X 會取什麼值，則偵測器會推斷該模式為異常。然而，它無法判斷是哪個 2 造成的。如果 X = 3，則第一個 2 是異常。如果 X = 5，則第二個 2 是異常。如果是第一個 2，則偵測器會延遲偵測到異常。

當偵測器延遲偵測到異常時，結果會包含下列額外欄位。

欄位 | 說明
:--- | :---
`past_values` | 觸發異常的實際輸入。如果 `past_values` 是 `null`，則歸因或預期值來自目前的輸入。如果 `past_values` 不是 `null`，則歸因或預期值來自過去的輸入（例如資料的前兩個步驟 [1,2,3]）。
`approx_anomaly_start_time` | 觸發異常的實際輸入的近似時間。此欄位可協助您了解偵測器標記異常的時間。單一串流與高基數偵測器都不會查詢先前的異常結果，因為這些查詢是成本高昂的操作。對於可能有許多實體的高基數偵測器，成本尤其高昂。如果資料不連續，則此欄位的準確度偏低，且偵測器偵測到異常的實際時間可能更早。

```json
{
  "detector_id": "kzcZ43wBgEQAbjDnhzGF",
  "confidence": 0.9746820962328963,
  "relevant_attribution": [
    {
      "feature_id": "deny_max1",
      "data": 0.07339452532666227
    },
    {
      "feature_id": "deny_avg",
      "data": 0.04934972719948845
    },
    {
      "feature_id": "deny_min",
      "data": 0.01803003656061806
    },
    {
      "feature_id": "deny_sum",
      "data": 0.14804918212089874
    },
    {
      "feature_id": "accept_max5",
      "data": 0.7111765287923325
    }
  ],
  "task_id": "9Dck43wBgEQAbjDn4zEe",
  "threshold": 1,
  "model_id": "kzcZ43wBgEQAbjDnhzGF_entity_app_0",
  "schema_version": 5,
  "anomaly_score": 1.141419389056506,
  "execution_start_time": 1635898427803,
  "past_values": [
    {
      "feature_id": "processing_bytes_max",
      "data": 905
    },
    {
      "feature_id": "processing_bytes_avg",
      "data": 479
    },
    {
      "feature_id": "processing_bytes_min",
      "data": 128
    },
    {
      "feature_id": "processing_bytes_sum",
      "data": 1437
    },
    {
      "feature_id": "processing_time_max",
      "data": 8440
    }
  ],
  "data_end_time": 1635883920000,
  "data_start_time": 1635883860000,
  "feature_data": [
    {
      "feature_id": "processing_bytes_max",
      "feature_name": "processing bytes max",
      "data": 1360
    },
    {
      "feature_id": "processing_bytes_avg",
      "feature_name": "processing bytes avg",
      "data": 990
    },
    {
      "feature_id": "processing_bytes_min",
      "feature_name": "processing bytes min",
      "data": 608
    },
    {
      "feature_id": "processing_bytes_sum",
      "feature_name": "processing bytes sum",
      "data": 2970
    },
    {
      "feature_id": "processing_time_max",
      "feature_name": "processing time max",
      "data": 9670
    }
  ],
  "expected_values": [
    {
      "likelihood": 1,
      "value_list": [
        {
          "feature_id": "processing_bytes_max",
          "data": 905
        },
        {
          "feature_id": "processing_bytes_avg",
          "data": 479
        },
        {
          "feature_id": "processing_bytes_min",
          "data": 128
        },
        {
          "feature_id": "processing_bytes_sum",
          "data": 4847
        },
        {
          "feature_id": "processing_time_max",
          "data": 15713
        }
      ]
    }
  ],
  "execution_end_time": 1635898427895,
  "anomaly_grade": 0.5514172746375128,
  "entity": [
    {
      "name": "process_name",
      "value": "process_3"
    }
  ],
  "approx_anomaly_start_time": 1635883620000
}
```
{% include copy-curl.html %}

## 攤平的異常結果對應

當您在 **Custom result index** 窗格中選取 **Enable flattened custom result index** 選項時，Anomaly Detection 外掛程式會將所有巢狀欄位攤平後的結果儲存在索引中。

儲存在索引中的巢狀欄位會使用下列攤平規則。

欄位 | 攤平規則 | 巢狀輸入範例 | 攤平後的輸出範例
:--- | :--- | :--- | :---
`relevant_attribution` | `relevant_attribution_$FEATURE_NAME_data: $RELEVANT_ATTRIBUTION_FEATURE_DATA` | `relevant_attribution : [{"feature_id": "deny_max1", "data": 0.07339452532666227}]` | `relevant_attribution_deny_max1_data: 0.07339452532666227`
`past_values` | `past_values_$FEATURE_NAME_data: $PAST_VALUES_FEATURE_DATA`  | `"past_values": [{"feature_id": "processing_bytes_max", "data": 905}]`                                           | `past_values_processing_bytes_max_data: 905`
`feature_data` | `feature_data_$FEATURE_NAME_data: $FEATURE_DATA_FEATURE_NAME_DATA` | `"feature_data": [{"feature_id": "processing_bytes_max", "feature_name": "processing bytes max", "data": 1360}]` | `feature_data_processing_bytes_max_data: 1360`
`expected_values` | `expected_values_$FEATURE_NAME_data: $EXPECTED_VALUES_FEATURE_DATA`  | `"expected_values": [{"likelihood": 1, "value_list": [{"feature_id": "processing_bytes_max", "data": 905}]}]`    | `expected_values_processing_bytes_max_data: 905` 
`entity` | `entity_$NAME_value: $ENTITY_VALUE ` | `"entity": [{"name": "process_name", "value": "process_3"}]` | `entity_process_name_value: process_3 `

例如，當偵測器延遲偵測到異常時，攤平後的結果會以下列格式顯示：

```json
{
  "detector_id": "kzcZ43wBgEQAbjDnhzGF",
  "confidence": 0.9746820962328963,
  "relevant_attribution": [
    {
      "feature_id": "deny_max1",
      "data": 0.07339452532666227
    },
    {
      "feature_id": "deny_avg",
      "data": 0.04934972719948845
    },
    {
      "feature_id": "deny_min",
      "data": 0.01803003656061806
    },
    {
      "feature_id": "deny_sum",
      "data": 0.14804918212089874
    },
    {
      "feature_id": "accept_max5",
      "data": 0.7111765287923325
    }
  ],
  "relevant_attribution_deny_max1_data": 0.07339452532666227,
  "relevant_attribution_deny_avg_data": 0.04934972719948845,
  "relevant_attribution_deny_min_data": 0.01803003656061806,
  "relevant_attribution_deny_sum_data": 0.14804918212089874,
  "relevant_attribution_deny_max5_data": 0.7111765287923325,
  "task_id": "9Dck43wBgEQAbjDn4zEe",
  "threshold": 1,
  "model_id": "kzcZ43wBgEQAbjDnhzGF_entity_app_0",
  "schema_version": 5,
  "anomaly_score": 1.141419389056506,
  "execution_start_time": 1635898427803,
  "past_values": [
    {
      "feature_id": "processing_bytes_max",
      "data": 905
    },
    {
      "feature_id": "processing_bytes_avg",
      "data": 479
    },
    {
      "feature_id": "processing_bytes_min",
      "data": 128
    },
    {
      "feature_id": "processing_bytes_sum",
      "data": 1437
    },
    {
      "feature_id": "processing_time_max",
      "data": 8440
    }
  ],
  "past_values_processing_bytes_max_data": 905,
  "past_values_processing_bytes_avg_data": 479,
  "past_values_processing_bytes_min_data": 128,
  "past_values_processing_bytes_sum_data": 1437,
  "past_values_processing_bytes_max_data": 8440,
  "data_end_time": 1635883920000,
  "data_start_time": 1635883860000,
  "feature_data": [
    {
      "feature_id": "processing_bytes_max",
      "feature_name": "processing bytes max",
      "data": 1360
    },
    {
      "feature_id": "processing_bytes_avg",
      "feature_name": "processing bytes avg",
      "data": 990
    },
    {
      "feature_id": "processing_bytes_min",
      "feature_name": "processing bytes min",
      "data": 608
    },
    {
      "feature_id": "processing_bytes_sum",
      "feature_name": "processing bytes sum",
      "data": 2970
    },
    {
      "feature_id": "processing_time_max",
      "feature_name": "processing time max",
      "data": 9670
    }
  ],
  "feature_data_processing_bytes_max_data": 1360,
  "feature_data_processing_bytes_avg_data": 990,
  "feature_data_processing_bytes_min_data": 608,
  "feature_data_processing_bytes_sum_data": 2970,
  "feature_data_processing_time_max_data": 9670,
  "expected_values": [
    {
      "likelihood": 1,
      "value_list": [
        {
          "feature_id": "processing_bytes_max",
          "data": 905
        },
        {
          "feature_id": "processing_bytes_avg",
          "data": 479
        },
        {
          "feature_id": "processing_bytes_min",
          "data": 128
        },
        {
          "feature_id": "processing_bytes_sum",
          "data": 4847
        },
        {
          "feature_id": "processing_time_max",
          "data": 15713
        }
      ]
    }
  ],
  "expected_values_processing_bytes_max_data": 905,
  "expected_values_processing_bytes_avg_data": 479,
  "expected_values_processing_bytes_min_data": 128,
  "expected_values_processing_bytes_sum_data": 4847,
  "expected_values_processing_time_max_data": 15713,
  "execution_end_time": 1635898427895,
  "anomaly_grade": 0.5514172746375128,
  "entity": [
    {
      "name": "process_name",
      "value": "process_3"
    }
  ],
  "entity_process_name_value": "process_3",
  "approx_anomaly_start_time": 1635883620000
}
```
