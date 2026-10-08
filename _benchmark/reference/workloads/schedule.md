---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: schedule
parent: Anatomy of a workload
nav_order: 40
---

<!-- vale off -->
# schedule 元素
<!-- vale on -->

`schedule` 元素包含一份任務清單，這些任務會在基準測試期間依指定順序執行。每個任務都是 OpenSearch Benchmark 支援的一項操作。

您可以在下列任一位置定義 `schedule`：

- 在 `workload.json` 的最上層。當工作負載只定義單一基準測試情境時，請使用此形式。OpenSearch Benchmark 會將該排程視為隱含的預設測試程序。
- 在測試程序內的 [`test_procedures`]({{site.url}}{{site.baseurl}}/benchmark/reference/workloads/test-procedures/) 元素中。當工作負載定義多個情境，且每個情境都有自己的名稱、說明和排程時，請使用此形式。

## 範例

下列 `schedule` 會建立索引、等待叢集變為健康狀態、大量將文件編製索引，然後執行 `match_all` 查詢：

```json
  "schedule": [
    {
      "operation": {
        "operation-type": "create-index"
      }
    },
    {
      "operation": {
        "operation-type": "cluster-health",
        "request-params": {
          "wait_for_status": "green"
        },
        "retry-until-success": true
      }
    },
    {
      "operation": {
        "operation-type": "bulk",
        "bulk-size": 5000
      },
      "warmup-time-period": 120,
      "clients": 8
    },
    {
      "operation": {
        "name": "query-match-all",
        "operation-type": "search",
        "body": {
          "query": {
            "match_all": {}
          }
        }
      },
      "iterations": 1000,
      "target-throughput": 100
    }
  ]
```

根據此 `schedule`，動作會依下列順序執行：

1. `create-index` 操作會建立索引。在 `bulk` 操作加入含有基準測試資料的文件之前，該索引會保持空白。
2. `cluster-health` 操作會在執行工作負載之前評估叢集的健康狀態。在此範例中，工作負載會等到叢集的健康狀態為 `green`。
   - `bulk` 操作會執行 `bulk` API，同時將 `5000` 文件編製索引。
   - 在進行基準測試之前，工作負載會等到指定的 `warmup-time-period` 經過。在此範例中，暖機期間為 `120` 秒。
3. `clients` 欄位定義同時執行大量編製索引操作的用戶端數量，在此範例中為八個。
4. `search` 操作會在文件由指定的用戶端透過 `bulk` API 編製索引之後，執行 `match_all` 查詢以比對所有文件。
   - `iterations` 欄位定義每個用戶端執行 `search` 操作的次數。基準測試報告會根據此數字自動調整百分位數。若要產生精確的百分位數，基準測試至少需要執行 1,000 次反覆運算。
   - `target-throughput` 欄位定義每個用戶端每秒執行的請求數量。此設定有助於降低基準測試延遲。例如，`target-throughput` 為 100 個請求除以 8 個用戶端，表示每個用戶端每秒發出 12 個請求。如需有關 OpenSearch Benchmark 中如何定義目標輸送量的詳細資訊，請參閱[目標輸送量]({{site.url}}{{site.baseurl}}/benchmark/target-throughput/)。

## 定義任務

`schedule` 元素會使用本節所述的方法來定義任務。

### 使用 operations 元素

下列範例使用 `operations` 元素定義 `force-merge` 和 `match-all` 查詢任務。`force-merge` 操作不使用任何參數，因此只需要 `name` 和 `operation-type`。`match-all-query` 參數需要查詢 `body` 和 `operation-type`。

在 `operations` 元素中定義的操作可以在排程中重複使用多次：

```yml
{
  "operations": [
    {
      "name": "force-merge",
      "operation-type": "force-merge"
    },
    {
      "name": "match-all-query",
      "operation-type": "search",
      "body": {
        "query": {
          "match_all": {}
        }
      }
    }
  ],
  "schedule": [
    {
      "operation": "force-merge",
      "clients": 1
    },
    {
      "operation": "match-all-query",
      "clients": 4,
      "warmup-iterations": 1000,
      "iterations": 1000,
      "target-throughput": 100
    }
  ]
}
```

如需可用操作類型的完整清單，請參閱 [`operations`]({{site.url}}{{site.baseurl}}/benchmark/reference/workloads/operations/)。

### 以內嵌方式定義操作

如果您不想在排程中重複使用某項操作，可以在 `schedule` 元素內定義操作，如下列範例所示：

```yml
{
  "schedule": [
    {
      "operation": {
        "name": "force-merge",
        "operation-type": "force-merge"
      },
      "clients": 1
    },
    {
      "operation": {
        "name": "match-all-query",
        "operation-type": "search",
        "body": {
          "query": {
            "match_all": {}
          }
        }
      },
      "clients": 4,
      "warmup-iterations": 1000,
      "iterations": 1000,
      "target-throughput": 100
    }
  ]
}
```

## 任務選項

每個任務都包含下列選項。

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`operation` | 是 | 清單 | 參照在 `operations` 元素中定義的操作名稱，或以內嵌方式包含整個操作。
`name` | 否 | 字串 | 當多個任務使用相同操作時，為該任務指定唯一名稱。
`tags` | 否 | 字串 | 唯一識別碼，可用於在 `tasks.clients` 之間進行篩選，或篩選應同時執行任務的用戶端數量。預設值為 1。
`clients` | 否 | 整數 | 指定將同時執行該任務的用戶端數量。預設值為 `1`。

## 目標選項

執行任務時，OpenSearch Benchmark 需要下列其中一個選項。

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`target-throughput` | 否 | 整數 | 定義基準測試模式。未定義時，OpenSearch Benchmark 會假設這是輸送量基準測試，並盡可能快速地執行任務。這適用於批次操作，此類操作偏好達到更好的輸送量，而非更低的延遲。定義後，目標會指定所有用戶端合計每秒的請求數量。例如，如果您以 8 個用戶端指定 `target-throughput: 1000`，每個用戶端每秒會發出 125 (= 1000 / 8) 個請求。
`target-interval` | 否 | 間隔 | 當 `target-throughput` 小於每秒 1 次操作時，定義 1 除以 `target-throughput` (以秒為單位) 的間隔。請定義 `target-throughput` 或 `target-interval` 其中之一，但不可同時定義兩者，否則 OpenSearch Benchmark 會引發錯誤。
`ignore-response-error-level` | 否 | 布林值 | 控制使用 `on-error=abort` 命令旗標執行基準測試時，是否忽略任務期間遇到的錯誤。

## 以反覆運算次數為基礎的選項

以反覆運算次數為基礎的選項決定操作應執行的次數。當任務以[平行](#parallel-tasks)方式執行時，這些選項也可以定義反覆執行的次數。若要設定以反覆運算次數為基礎的排程，請使用下列選項。

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`iterations` | 否 | 整數 | 指定用戶端應執行某項操作的次數。所有反覆運算都會納入測量結果。預設值為 `1`。
`warmup-iterations` | 否 | 整數 | 指定用戶端為了讓基準測試對象暖機而應執行某項操作的次數。`warmup-iterations` 不會出現在測量結果中。預設值為 `0`。

## 以時間為基礎的選項

以時間為基礎的選項決定操作應執行的持續時間 (以秒為單位)。這非常適合批次類型的操作，此類操作可能需要額外的暖機期間。

若要設定以時間為基礎的排程，請使用下列選項。

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`time-period` | 否 | 整數 | 指定 OpenSearch Benchmark 納入測量的時間長度 (以秒為單位)。大量編製索引不需要此選項，因為 OpenSearch Benchmark 會將所有文件大量編製索引，並在指定的 `warmup-time-period` 之後自然地測量所有樣本。
`ramp-up-time-period` | 否 | 整數 | 指定 OpenSearch Benchmark 逐步加入用戶端，直到達到為該操作指定之用戶端總數的時間長度 (以秒為單位)。
`warmup-time-period` | 否 | 整數 | 指定讓基準測試對象暖機的時間長度 (以秒為單位)。暖機期間擷取的回應資料都不會出現在測量結果中。

## 平行任務

`parallel` 元素會同時執行包在該元素內的任務。

平行執行任務時，每個任務都需要 `client` 選項，以確保基準測試中的用戶端保留給該任務使用。否則，當 `client` 選項在 `parallel` 元素內指定且未與任務關聯時，基準測試會對所有任務使用該數量的用戶端。

在下列範例中，`parallel-task-1` 和 `parallel-task-2` 會同時執行 `bulk` 操作：

```yml
{
  "name": "parallel-any",
  "description": "Workload completed-by property",
  "schedule": [
    {
      "parallel": {
        "tasks": [
          {
            "name": "parellel-task-1",
            "operation": {
              "operation-type": "bulk",
              "bulk-size": 1000
            },
            "clients": 8
          },
          {
            "name": "parellel-task-2",
            "operation": {
              "operation-type": "bulk",
              "bulk-size": 500
            },
            "clients": 8
          }
        ]
      }
    }
  ]
}
```

除了下列選項之外，`parallel` 元素也支援所有 `schedule` 參數。

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`tasks` | 是 | 陣列 | 定義應同時執行的任務清單。
`completed-by` | 否 | 字串 | 可讓您定義任務清單中某個任務的名稱，或定義值 `any`。如果 `completed-by` 設定為清單中某個任務的名稱，則該特定任務完成後，`parallel-task` 結構即視為完成。如果 `completed-by` 設定為 `any`，則清單中任一任務完成時，`parallel-task` 結構即視為完成。如果未明確定義 `completed-by`，則清單中所有任務都完成後，`parallel-task` 結構即視為完成。
