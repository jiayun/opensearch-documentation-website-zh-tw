---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "重新編製文件索引"
parent: Document APIs
nav_order: 60
redirect_from: 
  - /opensearch/reindex-data/
  - /opensearch/rest-api/document-apis/reindex/
---

# 重新編製文件索引 API
**1.0 版新增**
{: .label .label-purple}

重新編製文件索引 API 作業會將所有文件或部分文件從來源索引、資料串流或別名複製到目的地索引、資料串流或別名。來源與目的地必須不同。

重新編製索引作業會取得來源索引的快照，並將文件複製到目的地索引。對每份文件而言，複製是透過擷取文件來源（[`_source` 欄位]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/source/)）並將其編製索引到目的地來完成。

OpenSearch 原生支援跨叢集重新編製索引，讓您可以在不同的 OpenSearch 叢集之間複製資料。如需更多資訊，請參閱[跨叢集重新編製索引](#cross-cluster-reindexing)。

在使用 Reindex API 之前，請注意下列需求與限制：

- 重新編製索引作業需要來源索引中的所有文件都啟用 `_source` 欄位。如果 `_source` 已停用，作業將會失敗。
- 您必須在執行重新編製索引作業之前建立並設定目的地索引。OpenSearch 不會自動從來源索引複製設定、對應或分片組態。
- 請根據您的需求為目的地索引設定適當數量的分片、副本與欄位對應。
- 進行大規模的重新編製索引作業時，可考慮將 `number_of_replicas` 設定為 `0` 以暫時停用目的地索引的副本，並在完成後重新啟用。

重新編製大型資料集的索引可能會耗用大量資源，並可能影響叢集效能。請在重新編製索引作業期間監控叢集健康狀態，並考慮在正式環境中使用節流參數。如需更多資訊，請參閱[效能最佳化](#performance-optimization)。
{: .warning }

如需包含常見使用案例與範例的重新編製索引實務教學指南，請參閱[重新編製資料索引]({{site.url}}{{site.baseurl}}/im-plugin/reindex-data/)。
{: .tip }

與修改同一索引內文件的更新作業不同，重新編製索引作業是在不同的來源與目的地之間進行，因此不太可能發生版本衝突。`version_type` 參數控制 OpenSearch 在重新編製索引期間如何處理文件版本。預設情況下，版本衝突會停止重新編製索引程序。若要在發生衝突時繼續重新編製索引，請將 `conflicts` 參數設定為 `proceed`。回應將包含遇到的版本衝突數量。其他錯誤類型不受 `conflicts` 參數影響。

預設情況下，具有相同 ID 的文件會被覆寫。`op_type` 參數決定是否可以取代現有文件，或僅允許新文件；若是後者，嘗試為具有現有 ID 的文件編製索引會導致錯誤。如需更多資訊，請參閱[請求本文欄位](#request-body-fields)。

## 端點

```json
POST /_reindex
```

## 查詢參數

下表列出可用的查詢參數。所有參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`refresh` | 布林值 | 若為 `true`，OpenSearch 會重新整理分片，使重新編製索引作業的結果可供搜尋。有效值為 `true`、`false`，以及指定在執行作業前等待重新整理的 `wait_for`。預設為 `false`。
`timeout` | 時間單位 | 等待叢集回應的時間長度。預設為 `30s`。
`wait_for_active_shards` | 字串 | 在 OpenSearch 處理重新編製索引請求之前，必須可用的作用中分片數量。預設為 `1`（僅主要分片）。可設定為 `all` 或正整數。大於 `1` 的值需要副本。例如，若您指定值為 `3`，則索引必須有兩個副本分散在兩個額外的節點上，作業才能成功。
`wait_for_completion` | 布林值 | 若為 `false`，OpenSearch 會以非同步方式執行重新編製索引作業，而不等待其完成。請求會立即傳回，工作會在背景繼續進行。您可以使用 [Tasks API]({{site.url}}{{site.baseurl}}/api-reference/tasks/) 監控其進度。預設為 `true`，表示作業以同步方式執行。請參閱[非同步作業](#asynchronous-operations)。
`requests_per_second` | 整數 | 指定請求的節流，以每秒子請求數為單位。預設為 `-1`，表示不進行節流。請參閱[控制重新編製索引速率](#controlling-the-reindex-rate)與[節流與速率控制](#throttling-and-rate-control)。
`require_alias` | 布林值 | 目的地索引是否必須為別名。預設為 `false`。
`scroll` | 時間單位 | 保持搜尋上下文開啟的時間長度。預設為 `5m`。
`slices` | 整數 | 自動切片的切片數量。OpenSearch 會自動將重新編製索引作業分割為此數量的平行子工作。預設為 `1`（不切片）。將此參數設定為 `auto` 可讓 OpenSearch 自動決定最佳切片數量。請參閱[使用切片進行平行處理](#using-slicing-for-parallel-processing)。
`max_docs` | 整數 | 重新編製索引作業應處理的最大文件數量。預設為所有文件。請參閱[擷取範例資料](#extracting-sample-data)。

## 請求本文欄位

下表列出所有請求本文欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`source` | 物件 | 必要 | 要從中複製資料的來源。請參閱[`source` 物件](#the-source-object)。
`dest` | 物件 | 必要 | 要將資料複製到的目的地。請參閱[`dest` 物件](#the-dest-object)。
`conflicts` | 字串 | 選用 | 告知 OpenSearch 當重新編製索引作業遇到版本衝突時應如何處理。有效值為 `abort` 與 `proceed`。預設為 `abort`。
`script` | 物件 | 選用 | OpenSearch 在重新編製索引作業期間用來對資料套用轉換的指令碼。請參閱[`script` 物件](#the-script-object)。

### `source` 物件

`source` 物件支援下列欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`index` | 字串 | 必要 | 要從中複製資料的索引、資料串流或別名名稱。您可以以逗號分隔清單指定多個來源索引。
`query` | 物件 | 選用 | 用於重新編製索引作業的搜尋查詢。請參閱[依查詢篩選文件](#filtering-documents-by-query)。
`remote` | 物件 | 選用 | 要從中複製資料的遠端 OpenSearch 叢集資訊。請參閱[跨叢集重新編製索引](#cross-cluster-reindexing)。
`remote.host` | 字串 | 指定 `remote` 時必要 | 您要從中編製索引的遠端 OpenSearch 叢集 URL。
`remote.username` | 字串 | 選用 | 用於遠端主機驗證的使用者名稱。
`remote.password` | 字串 | 選用 | 用於遠端主機驗證的密碼。
`remote.socket_timeout` | 字串 | 選用 | 遠端 socket 讀取逾時。預設為 `30s`。
`remote.connect_timeout` | 字串 | 選用 | 遠端連線逾時。預設為 `30s`。
`size` | 整數 | 選用 | 每個批次要編製索引的文件數量。從遠端來源編製索引時使用此設定，以確保每個批次都能容納於堆積記憶體緩衝區中；該緩衝區的預設大小上限為 100 MB。
`slice` | 物件 | 選用 | 手動切片的組態。必須是包含 `id`（切片 ID）與 `max`（切片總數）屬性的物件，以手動指定要處理的資料切片。這可透過執行多個重新編製索引作業（每個作業處理不同的切片）來實現平行處理。請參閱[使用切片進行平行處理](#using-slicing-for-parallel-processing)。
`_source` | 布林值或陣列 | 選用 | 是否重新編製來源欄位的索引。指定要重新編製索引的欄位清單，或指定 `true` 以重新編製所有欄位的索引。預設為 `true`。請參閱[選取特定欄位](#selecting-specific-fields)。
`sort` | 陣列 | 選用 | _已淘汰_。用於在重新編製索引前排序文件的 `<field>:<direction>` 配對逗號分隔清單。若與 `max_docs` 搭配使用以控制要重新編製索引的文件，請考慮改用[依查詢篩選文件](#filtering-documents-by-query)來找出所需的資料子集。

### `dest` 物件

`dest` 物件支援下列欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`index` | 字串 | 必要 | 要複製過去的目標索引、資料串流或別名名稱。
`version_type` | 字串 | 選用 | 控制 OpenSearch 在重新編製索引時如何處理文件版本：<br>• `internal` (預設)：忽略版本，並覆寫目的地中與來源文件具有相同 ID 的任何文件。<br>• `external`：保留來源的版本，建立任何遺漏的文件，並且僅在目的地文件的版本比來源舊時才更新。<br>• `external_gt`：類似於 `external`，但僅在來源版本大於目的地版本時才更新文件。<br>• `external_gte`：類似於 `external`，但在來源版本大於或等於目的地版本時更新文件。
`op_type` | 字串 | 選用 | 決定重新編製索引時文件的處理方式：<br>• `index` (預設)：建立新文件並更新現有文件。<br>• `create`：僅建立目的地中不存在的文件。具有現有 ID 的文件會造成版本衝突。重新編製索引至資料串流 (僅能附加) 時為必要。
`pipeline` | 字串 | 選用 | 重新編製索引時要使用的資料匯入管線。請參閱[使用資料匯入管線轉換文件](#transforming-documents-using-ingest-pipelines)。
`routing` | 字串 | 選用 | 控制重新編製索引時文件路由的處理方式。有效值為 `keep` (保留現有路由，預設)、`discard` (移除路由) 或 `=<value>` (將路由設為特定值)。請參閱[路由](#routing)。

### `script` 物件

`script` 物件支援下列欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`source` | 字串 | 必要 | 以字串表示的指令碼原始碼。
`lang` | 字串 | 選用 | 指令碼語言。有效值為 `painless`、`expression`、`mustache` 和 `java`。預設為 `painless`。如需更多資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

## 重新編製索引的運作方式

重新編製索引作業會擷取來源索引的快照，並將文件複製到目的地索引。這種方式表示版本衝突不太可能發生，與在同一索引上運作的更新作業不同。

預設情況下，版本衝突會停止重新編製索引程序。若要在發生衝突時繼續重新編製索引，請將 `conflicts` 參數設為 `proceed`。回應將包含遇到的版本衝突數量。其他錯誤類型不受 `conflicts` 參數影響。

## 範例請求

<!-- spec_insert_start
component: example_code
rest: POST /_reindex
body: |
{
   "source":{
      "index":"my-source-index"
   },
   "dest":{
      "index":"my-destination-index"
   }
}
-->
{% capture step1_rest %}
POST /_reindex
{
  "source": {
    "index": "my-source-index"
  },
  "dest": {
    "index": "my-destination-index"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.reindex(
  body =   {
    "source": {
      "index": "my-source-index"
    },
    "dest": {
      "index": "my-destination-index"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

```json
{
    "took": 28829,
    "timed_out": false,
    "total": 111396,
    "updated": 0,
    "created": 111396,
    "deleted": 0,
    "batches": 112,
    "version_conflicts": 0,
    "noops": 0,
    "retries": {
        "bulk": 0,
        "search": 0
    },
    "throttled_millis": 0,
    "requests_per_second": -1.0,
    "throttled_until_millis": 0,
    "failures": []
}
```

## 回應本文欄位

下表列出所有回應本文欄位，並為每個欄位提供詳細說明。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`took` | 整數 | 完成整個重新編製索引作業所需的總時間 (毫秒)，包括所有批次處理與網路開銷。
`timed_out` | 布林值 | 指出重新編製索引作業是否有任何部分超過設定的逾時時間。若為 `true`，作業可能已部分完成。
`total` | 整數 | 重新編製索引作業期間成功處理的文件總數。包括已建立、已更新或產生無作業 (no-op) 的文件。
`updated` | 整數 | 因目的地索引中已存在相同 ID 的文件而更新的文件數量。
`created` | 整數 | 在目的地索引中建立的新文件數量。這些是先前不存在於目的地中的文件。
`deleted` | 整數 | 從目的地索引刪除的文件數量。這發生在指令碼設定 `ctx.op = "delete"` 時。
`batches` | 整數 | 重新編製索引作業期間處理的捲動批次數量。每個批次包含多個文件，數量由 `size` 參數設定。
`version_conflicts` | 整數 | 遇到的版本衝突數量。當目的地文件的版本高於來源文件時 (使用外部版本控制時)，會發生版本衝突。
`noops` | 整數 | 處理期間略過的文件數量。這發生在指令碼設定 `ctx.op = "noop"` 或不需要任何變更時。
`retries` | 物件 | 包含不同作業類型重試次數的重試統計物件。遇到暫時性失敗時會自動重試。
`retries.bulk` | 整數 | 重新編製索引作業期間嘗試的批次 (bulk) 作業重試次數。
`retries.search` | 整數 | 重新編製索引作業期間嘗試的搜尋作業重試次數。
`throttled_millis` | 整數 | 為符合 `requests_per_second` 設定而對作業進行節流的總時間 (毫秒)。數值越高表示套用的節流越多。
`requests_per_second` | 浮點數 | 作業期間每秒實際執行的請求速率。由於節流調整與系統效能，此值可能與請求的速率不同。
`throttled_until_millis` | 整數 | 對於非同步作業，此值表示節流請求下次執行的時間 (自 epoch 起算的毫秒數)。已完成的作業一律為 `0`。
`failures` | 陣列 | 描述作業期間遇到的任何無法復原錯誤的失敗物件陣列。每個失敗項目包含錯誤類型、原因與受影響文件的詳細資訊。

## 選擇性重新編製索引

下列範例示範在重新編製索引時選擇性複製資料的不同方式，包括篩選文件、選取特定欄位，以及擷取範例資料集。

### 依查詢篩選文件

僅複製符合特定條件的文件：

<!-- spec_insert_start
component: example_code
rest: POST /_reindex
body: |
{
  "source": {
    "index": "orders",
    "query": {
      "range": {
        "order_date": {
          "gte": "2024-01-01",
          "lte": "2024-12-31"
        }
      }
    }
  },
  "dest": {
    "index": "orders-2024"
  }
}
-->
{% capture step1_rest %}
POST /_reindex
{
  "source": {
    "index": "orders",
    "query": {
      "range": {
        "order_date": {
          "gte": "2024-01-01",
          "lte": "2024-12-31"
        }
      }
    }
  },
  "dest": {
    "index": "orders-2024"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.reindex(
  body =   {
    "source": {
      "index": "orders",
      "query": {
        "range": {
          "order_date": {
            "gte": "2024-01-01",
            "lte": "2024-12-31"
          }
        }
      }
    },
    "dest": {
      "index": "orders-2024"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 選取特定欄位

僅從來源文件複製特定欄位：

<!-- spec_insert_start
component: example_code
rest: POST /_reindex
body: |
{
  "source": {
    "index": "customer-data",
    "_source": ["customer_id", "name", "email", "created_date"]
  },
  "dest": {
    "index": "customers-minimal"
  }
}
-->
{% capture step1_rest %}
POST /_reindex
{
  "source": {
    "index": "customer-data",
    "_source": [
      "customer_id",
      "name",
      "email",
      "created_date"
    ]
  },
  "dest": {
    "index": "customers-minimal"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.reindex(
  body =   {
    "source": {
      "index": "customer-data",
      "_source": [
        "customer_id",
        "name",
        "email",
        "created_date"
      ]
    },
    "dest": {
      "index": "customers-minimal"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 擷取樣本資料

建立較小的資料集以供測試：

<!-- spec_insert_start
component: example_code
rest: POST /_reindex
body: |
{
  "max_docs": 1000,
  "source": {
    "index": "production-logs",
    "query": {
      "function_score": {
        "random_score": {
          "seed": 42
        },
        "min_score": 0.8
      }
    }
  },
  "dest": {
    "index": "test-sample"
  }
}
-->
{% capture step1_rest %}
POST /_reindex
{
  "max_docs": 1000,
  "source": {
    "index": "production-logs",
    "query": {
      "function_score": {
        "random_score": {
          "seed": 42
        },
        "min_score": 0.8
      }
    }
  },
  "dest": {
    "index": "test-sample"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.reindex(
  body =   {
    "max_docs": 1000,
    "source": {
      "index": "production-logs",
      "query": {
        "function_score": {
          "random_score": {
            "seed": 42
          },
          "min_score": 0.8
        }
      }
    },
    "dest": {
      "index": "test-sample"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 路由

依預設，如果重新編製索引作業遇到具有路由的文件，除非指令碼變更路由，否則會保留路由。您可以使用 `dest` 區段中的 `routing` 參數來控制路由行為：

- `keep`：保留來源文件的路由（預設）
- `discard`：移除重新編製索引之文件的路由
- `=<text>`：將所有重新編製索引之文件的路由設為指定值

下列請求會為所有重新編製索引的文件設定自訂路由值：

<!-- spec_insert_start
component: example_code
rest: POST /_reindex
body: |
{
  "source": {
    "index": "source"
  },
  "dest": {
    "index": "dest",
    "routing": "=company_a"
  }
}
-->
{% capture step1_rest %}
POST /_reindex
{
  "source": {
    "index": "source"
  },
  "dest": {
    "index": "dest",
    "routing": "=company_a"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.reindex(
  body =   {
    "source": {
      "index": "source"
    },
    "dest": {
      "index": "dest",
      "routing": "=company_a"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 使用資料匯入管線轉換文件

若要轉換資料，請在重新編製索引期間透過資料匯入管線處理文件。先建立管線，再於重新編製索引作業中參照該管線：

<!-- spec_insert_start
component: example_code
rest: POST /_reindex
body: |
{
  "source": {
    "index": "raw-data"
  },
  "dest": {
    "index": "processed-data",
    "pipeline": "data-enrichment"
  }
}
-->
{% capture step1_rest %}
POST /_reindex
{
  "source": {
    "index": "raw-data"
  },
  "dest": {
    "index": "processed-data",
    "pipeline": "data-enrichment"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.reindex(
  body =   {
    "source": {
      "index": "raw-data"
    },
    "dest": {
      "index": "processed-data",
      "pipeline": "data-enrichment"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

執行重新編製索引作業之前，請先建立資料匯入管線。此範例會建立一個管線，新增 `processed_at` 時間戳記，並將 `status` 欄位轉換為大寫：

```json
PUT /_ingest/pipeline/data-enrichment
{
  "description": "Enriches documents during reindexing",
  "processors": [
    {
      "set": {
        "field": "processed_at",
        "value": "{{_ingest.timestamp}}"
      }
    },
    {
      "uppercase": {
        "field": "status"
      }
    }
  ]
}
```

### 控制重新編製索引的速率

控制重新編製索引的速率，以盡量降低對叢集的影響：

<!-- spec_insert_start
component: example_code
rest: POST /_reindex?requests_per_second=500
body: |
{
  "source": {
    "index": "production-data"
  },
  "dest": {
    "index": "production-backup"
  }
}
-->
{% capture step1_rest %}
POST /_reindex?requests_per_second=500
{
  "source": {
    "index": "production-data"
  },
  "dest": {
    "index": "production-backup"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.reindex(
  params = { "requests_per_second": "500" },
  body =   {
    "source": {
      "index": "production-data"
    },
    "dest": {
      "index": "production-backup"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 指令碼作業

您可以在重新編製索引過程中使用指令碼轉換文件。您可以修改文件內容、中繼資料，並控制要處理哪些文件。

指令碼可以修改下列文件中繼資料欄位：

- `ctx._id`：變更文件 ID。
- `ctx._index`：將文件路由至不同的目的地索引。
- `ctx._version`：控制文件版本管理。
- `ctx._routing`：設定自訂路由值。

設定 `ctx.op` 欄位，以控制對每份文件執行的動作：

- `ctx.op = "index"`：正常編製文件索引（預設行為）。
- `ctx.op = "create"`：僅在文件不存在時建立文件。
- `ctx.op = "noop"`：略過文件（適用於條件式處理）。
- `ctx.op = "delete"`：從目的地索引刪除文件。

### 轉換欄位值

您可以在重新編製索引期間新增或修改文件中的欄位。例如，此指令碼會為每份文件新增時間戳記和遷移狀態：

<!-- spec_insert_start
component: example_code
rest: POST /_reindex
body: |
{
  "source": {
    "index": "source-data"
  },
  "dest": {
    "index": "migrated-data"
  },
  "script": {
    "source": "ctx._source.timestamp = System.currentTimeMillis(); ctx._source.status = 'migrated'"
  }
}
-->
{% capture step1_rest %}
POST /_reindex
{
  "source": {
    "index": "source-data"
  },
  "dest": {
    "index": "migrated-data"
  },
  "script": {
    "source": "ctx._source.timestamp = System.currentTimeMillis(); ctx._source.status = 'migrated'"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.reindex(
  body =   {
    "source": {
      "index": "source-data"
    },
    "dest": {
      "index": "migrated-data"
    },
    "script": {
      "source": "ctx._source.timestamp = System.currentTimeMillis(); ctx._source.status = 'migrated'"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 重新命名欄位

您可以使用指令碼，在重新編製索引時重新命名欄位。此指令碼會在重新編製索引作業期間，將 `client_name` 重新命名為 `customer_name`，並將 `total_amount` 重新命名為 `order_total`：

<!-- spec_insert_start
component: example_code
rest: POST /_reindex
body: |
{
  "source": {
    "index": "legacy-data"
  },
  "dest": {
    "index": "updated-data"
  },
  "script": {
    "source": "ctx._source.customer_name = ctx._source.remove('client_name'); ctx._source.order_total = ctx._source.remove('total_amount');"
  }
}
-->
{% capture step1_rest %}
POST /_reindex
{
  "source": {
    "index": "legacy-data"
  },
  "dest": {
    "index": "updated-data"
  },
  "script": {
    "source": "ctx._source.customer_name = ctx._source.remove('client_name'); ctx._source.order_total = ctx._source.remove('total_amount');"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.reindex(
  body =   {
    "source": {
      "index": "legacy-data"
    },
    "dest": {
      "index": "updated-data"
    },
    "script": {
      "source": "ctx._source.customer_name = ctx._source.remove('client_name'); ctx._source.order_total = ctx._source.remove('total_amount');"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 依條件處理文件

您可以依條件略過文件，或套用不同的轉換。例如，此指令碼會略過已封存的文件，並為所有其他文件新增遷移時間戳記：

<!-- spec_insert_start
component: example_code
rest: POST /_reindex
body: |
{
  "source": {
    "index": "mixed-data"
  },
  "dest": {
    "index": "processed-data"
  },
  "script": {
    "source": "if (ctx._source.category == 'archived') { ctx.op = 'noop' } else { ctx._source.migrated_at = new Date() }"
  }
}
-->
{% capture step1_rest %}
POST /_reindex
{
  "source": {
    "index": "mixed-data"
  },
  "dest": {
    "index": "processed-data"
  },
  "script": {
    "source": "if (ctx._source.category == 'archived') { ctx.op = 'noop' } else { ctx._source.migrated_at = new Date() }"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.reindex(
  body =   {
    "source": {
      "index": "mixed-data"
    },
    "dest": {
      "index": "processed-data"
    },
    "script": {
      "source": "if (ctx._source.category == 'archived') { ctx.op = 'noop' } else { ctx._source.migrated_at = new Date() }"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 將文件路由至不同索引

您可以根據文件內容，動態將文件路由至不同的目的地索引。例如，此指令碼會將產品路由至各類別專屬的索引：

<!-- spec_insert_start
component: example_code
rest: POST /_reindex
body: |
{
  "source": {
    "index": "product-catalog"
  },
  "dest": {
    "index": "placeholder-will-be-overridden"
  },
  "script": {
    "source": "ctx._index = 'products-' + ctx._source.category.toLowerCase()"
  }
}
-->
{% capture step1_rest %}
POST /_reindex
{
  "source": {
    "index": "product-catalog"
  },
  "dest": {
    "index": "placeholder-will-be-overridden"
  },
  "script": {
    "source": "ctx._index = 'products-' + ctx._source.category.toLowerCase()"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.reindex(
  body =   {
    "source": {
      "index": "product-catalog"
    },
    "dest": {
      "index": "placeholder-will-be-overridden"
    },
    "script": {
      "source": "ctx._index = 'products-' + ctx._source.category.toLowerCase()"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 整併以時間為基礎的索引

使用下列指令碼，將多個以時間為基礎的索引整併為單一索引：

<!-- spec_insert_start
component: example_code
rest: POST /_reindex
body: |
{
  "source": {
    "index": ["logs-2024-01-*", "logs-2024-02-*", "logs-2024-03-*"]
  },
  "dest": {
    "index": "logs-2024-q1"
  },
  "script": {
    "source": "ctx._source.quarter = 'Q1-2024'; ctx._source.consolidated_date = System.currentTimeMillis();"
  }
}
-->
{% capture step1_rest %}
POST /_reindex
{
  "source": {
    "index": [
      "logs-2024-01-*",
      "logs-2024-02-*",
      "logs-2024-03-*"
    ]
  },
  "dest": {
    "index": "logs-2024-q1"
  },
  "script": {
    "source": "ctx._source.quarter = 'Q1-2024'; ctx._source.consolidated_date = System.currentTimeMillis();"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.reindex(
  body =   {
    "source": {
      "index": [
        "logs-2024-01-*",
        "logs-2024-02-*",
        "logs-2024-03-*"
      ]
    },
    "dest": {
      "index": "logs-2024-q1"
    },
    "script": {
      "source": "ctx._source.quarter = 'Q1-2024'; ctx._source.consolidated_date = System.currentTimeMillis();"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

此範例會將 3 個月的每日記錄檔索引整併為季度索引，同時新增關於此次整併的中繼資料。

## 非同步作業

對於大型資料集，您可以非同步執行重新編製索引作業，以避免阻塞您的應用程式。當您設定 `wait_for_completion=false` 時，OpenSearch 會立即傳回工作 ID，您可以用它來監控作業進度：

<!-- spec_insert_start
component: example_code
rest: POST /_reindex?wait_for_completion=false
body: |
{
  "source": {
    "index": "large-source-index"
  },
  "dest": {
    "index": "destination-index"
  }
}
-->
{% capture step1_rest %}
POST /_reindex?wait_for_completion=false
{
  "source": {
    "index": "large-source-index"
  },
  "dest": {
    "index": "destination-index"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.reindex(
  params = { "wait_for_completion": "false" },
  body =   {
    "source": {
      "index": "large-source-index"
    },
    "dest": {
      "index": "destination-index"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應包含工作 ID：

```json
{
  "task": "oTUltX4IQMOUUVeiohTt8A:12345"
}
```

使用 [Tasks API]({{site.url}}{{site.baseurl}}/api-reference/tasks/) 檢查您的重新編製索引作業狀態：

```json
GET /_tasks/oTUltX4IQMOUUVeiohTt8A:12345
```

您可以使用下列作業管理長時間執行的重新編製索引工作：

- 取消正在執行的重新編製索引作業：`POST /_tasks/oTUltX4IQMOUUVeiohTt8A:12345/_cancel`
- 列出所有重新編製索引工作：`GET /_tasks?actions=*reindex*`
- 工作清理：OpenSearch 會自動移除已完成的工作文件，但若需要立即清理，您可以手動刪除這些文件。

## 跨叢集重新編製索引

從遠端 OpenSearch 叢集複製資料：

<!-- spec_insert_start
component: example_code
rest: POST /_reindex
body: |
{
  "source": {
    "remote": {
      "host": "https://remote-cluster.example.com:9200",
      "username": "reindex-user",
      "password": "secure-password"
    },
    "index": "remote-index",
    "size": 1000
  },
  "dest": {
    "index": "local-copy"
  }
}
-->
{% capture step1_rest %}
POST /_reindex
{
  "source": {
    "remote": {
      "host": "https://remote-cluster.example.com:9200",
      "username": "reindex-user",
      "password": "secure-password"
    },
    "index": "remote-index",
    "size": 1000
  },
  "dest": {
    "index": "local-copy"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.reindex(
  body =   {
    "source": {
      "remote": {
        "host": "https://remote-cluster.example.com:9200",
        "username": "reindex-user",
        "password": "secure-password"
      },
      "index": "remote-index",
      "size": 1000
    },
    "dest": {
      "index": "local-copy"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 遠端重新索引的 SSL 組態

透過 HTTPS 從遠端叢集重新索引時，請在 `opensearch.yml` 中設定 SSL 設定。

#### 憑證式驗證

使用個別憑證檔案設定 SSL：

```yaml
reindex.ssl.certificate_authorities: ["/path/to/ca-cert.pem"]
reindex.ssl.certificate: "/path/to/client-cert.pem"
reindex.ssl.key: "/path/to/client-key.pem"
reindex.ssl.verification_mode: full
```

#### 金鑰儲存區式驗證

使用金鑰儲存區和信任儲存區檔案設定 SSL：

```yaml
reindex.ssl.keystore.path: "/path/to/keystore.p12"
reindex.ssl.keystore.type: "PKCS12"
reindex.ssl.truststore.path: "/path/to/truststore.p12"
reindex.ssl.truststore.type: "PKCS12"
```

#### SSL 組態選項

下表列出可用的 SSL 組態參數。

參數 | 說明 | 預設值
:--- | :--- | :---
`reindex.ssl.verification_mode` | 憑證驗證等級：`full`、`certificate` 或 `none` | `full`
`reindex.ssl.certificate_authorities` | CA 憑證檔案路徑清單 | 無
`reindex.ssl.truststore.path` | 信任儲存區檔案的路徑（JKS 或 PKCS12） | 無
`reindex.ssl.keystore.path` | 用於用戶端驗證的金鑰儲存區檔案路徑 | 無
`reindex.ssl.supported_protocols` | 支援的 TLS 通訊協定版本 | `TLSv1.3,TLSv1.2`

SSL 設定必須在 `opensearch.yml` 中設定，且需要重新啟動叢集。這些設定無法在重新索引請求本文中設定。
{: .warning }

#### 遠端叢集允許清單

在 `opensearch.yml` 中設定允許的遠端主機：

```yaml
reindex.remote.allowlist: [
  "remote-cluster.example.com:9200",
  "backup-cluster.example.com:9200",
  "10.0.1.*:9200"
]
```

允許清單支援：

- 明確指定的主機與連接埠組合。
- 用於 IP 範圍的萬用字元模式。
- 多個叢集端點。

#### 重試設定

當傳送至遠端叢集的請求失敗時，OpenSearch 會採用指數退避方式重試。下列叢集設定可控制重試行為。

設定 | 說明 | 預設值
:--- | :--- | :---
`reindex.remote.retry.initial_backoff` | 第一次重試前的等待時間。之後每次重試的等待時間都會加倍。 | `500ms`
`reindex.remote.retry.max_count` | 重新索引作業失敗前的重試次數上限。 | `15`

## 效能最佳化

使用下列技巧將重新索引效能最佳化。

### 節流與速率控制

使用節流控制重新索引作業對叢集效能的影響：

<!-- spec_insert_start
component: example_code
rest: POST /_reindex?requests_per_second=100
body: |
{
  "source": {"index": "source"},
  "dest": {"index": "dest"}
}
-->
{% capture step1_rest %}
POST /_reindex?requests_per_second=100
{
  "source": {
    "index": "source"
  },
  "dest": {
    "index": "dest"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.reindex(
  params = { "requests_per_second": "100" },
  body =   {
    "source": {
      "index": "source"
    },
    "dest": {
      "index": "dest"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

您可以動態調整執行中重新索引作業的節流：

```json
POST /_reindex/task_id/_rethrottle?requests_per_second=200
```

### 使用切片進行平行處理

切片會將重新索引作業分成多個平行任務，以提升大型資料集的處理效能。

#### 自動切片

若要讓 OpenSearch 決定最佳切片數量，請將 `slices` 查詢參數設為 `auto`：

<!-- spec_insert_start
component: example_code
rest: POST /_reindex?slices=auto
body: |
{
  "source": {"index": "large-index"},
  "dest": {"index": "large-index-copy"}
}
-->
{% capture step1_rest %}
POST /_reindex?slices=auto
{
  "source": {
    "index": "large-index"
  },
  "dest": {
    "index": "large-index-copy"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.reindex(
  params = { "slices": "auto" },
  body =   {
    "source": {
      "index": "large-index"
    },
    "dest": {
      "index": "large-index-copy"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 手動切片

若要進一步控制平行處理，您可以在請求本文中指定切片 ID 和切片總數，以手動設定切片。

OpenSearch 使用 `max` 參數，在所有切片請求中以一致的方式分割資料集。OpenSearch 會使用 `max` 值，對每份文件套用雜湊函式，以判定文件屬於哪個切片。這可確保：

- 文件均勻分布於所有切片。
- 每份文件恰好分配到一個切片（沒有重複或遺漏）。
- 所有平行請求都必須使用相同的 `max` 值，以維持一致性。

例如，使用 `max: 4` 時，您可以平行執行四個獨立請求：

- 請求 1：`{"id": 0, "max": 4}`（處理切片 `0`）
- 請求 2：`{"id": 1, "max": 4}`（處理切片 `1`）
- 請求 3：`{"id": 2, "max": 4}`（處理切片 `2`）
- 請求 4：`{"id": 3, "max": 4}`（處理切片 `3`）

下列請求會處理總共 4 個切片中的切片 `0`：

<!-- spec_insert_start
component: example_code
rest: POST /_reindex
body: |
{
  "source": {
    "index": "large-index",
    "slice": {"id": 0, "max": 4}
  },
  "dest": {"index": "large-index-copy"}
}
-->
{% capture step1_rest %}
POST /_reindex
{
  "source": {
    "index": "large-index",
    "slice": {
      "id": 0,
      "max": 4
    }
  },
  "dest": {
    "index": "large-index-copy"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.reindex(
  body =   {
    "source": {
      "index": "large-index",
      "slice": {
        "id": 0,
        "max": 4
      }
    },
    "dest": {
      "index": "large-index-copy"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

使用不同的切片 ID（0--3）執行多個請求，以進行平行處理。

### 監控重新索引作業

使用下列方法監控您重新索引作業的進度與效能。

監控您叢集中所有進行中的重新索引作業：

```json
GET /_tasks?actions=*reindex*&detailed=true
```
{% include copy-curl.html %}

使用特定重新索引任務的任務 ID 檢查其進度：

```json
GET /_tasks/oTUltX4IQMOUUVeiohTt8A:12345
```
{% include copy-curl.html %}

在重新索引作業期間監控叢集效能與磁碟使用量：

```json
GET /_cluster/health
```
{% include copy-curl.html %}

```json
GET /_nodes/stats/indices/store
```
{% include copy-curl.html %}

## 必要權限

如果您使用 Security 外掛程式，請確保您具有適當的權限：`indices:data/write/reindex`。
