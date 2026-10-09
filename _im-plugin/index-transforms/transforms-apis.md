---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "轉換相關 API"
nav_order: 10
parent: Index transforms
has_toc: true
---

# 轉換相關 API

除了使用 OpenSearch Dashboards 之外，您也可以使用 REST API 來建立、啟動、停止轉換任務，以及執行其他相關操作。

本頁的範例使用 OpenSearch Dashboards 的電子商務範例資料。若要新增該資料，請前往 OpenSearch Dashboards 首頁，選取 **Try our sample data**，然後在 **Sample eCommerce orders** 中選取 **Add data**。

#### 目錄
- TOC
{:toc}

## 建立轉換任務
**於 1.0 版推出**
{: .label .label-purple }

建立轉換任務。

### 端點

```json
PUT _plugins/_transform/{transform_id}
```

### 路徑參數

參數 | 資料類型 | 說明
:--- | :--- | :---
`transform_id` | 字串 | 轉換 ID |

### 請求本文欄位

您可以在 HTTP 請求本文中指定以下選項：

選項 | 資料類型 | 說明 | 必要
:--- | :--- | :--- | :---
`enabled` | 布林值 | 轉換任務在建立時是否啟用。預設為 `true`。 | 否
`continuous` | 布林值 | 指定轉換任務是否應為連續型。連續型任務會在每次依據 `schedule` 欄位排定的時間執行，並根據新轉換的桶以及新增至來源索引的任何新資料執行。非連續型任務只執行一次。預設為 `false`。 | 否
`schedule` | 物件 | 轉換任務的排程。包含一個 `interval` 物件，其中有 `period`、`unit` 和 `start_time` 欄位。 | 是
`description` | 字串 | 描述轉換任務。 | 是
`source_index` | 字串 | 包含待轉換資料的來源索引。 | 是
`target_index` | 字串 | 新轉換資料要加入的目標索引。您可以建立新索引或更新現有索引。 | 是
`data_selection_query` | 物件 | 用於篩選轉換任務來源索引子集的 Query DSL。若省略此欄位，任務會轉換來源索引中的每份文件。如需更多資訊，請參閱 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/)。 | 否
`page_size` | 整數 | IM 同時處理並編製索引的桶數。數值越高效能越好，但需要更多記憶體。若您的機器記憶體不足，Index Management (IM) 會自動調整此欄位並重試，直到操作成功為止。 | 是
`groups` | 陣列 | 指定轉換任務要使用的分組。每個項目會指定來源索引中的一個 `source_field` 以及要寫入的 `target_field`。支援的分組為 `terms`、`histogram` 和 `date_histogram`。任務必須定義至少一個分組。如需更多資訊，請參閱 [桶彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/index/)。 | 是
`aggregations` | 物件 | 轉換任務要使用的彙總。支援的彙總為 `sum`、`max`、`min`、`value_count`、`avg`、`scripted_metric` 和 `percentiles`。如需更多資訊，請參閱 [指標彙總]({{site.url}}{{site.baseurl}}/aggregations/metric/index/)。 | 否

#### 請求範例

以下請求會建立 ID 為 `sample` 的轉換任務：

```json
PUT _plugins/_transform/sample
{
  "transform": {
    "enabled": true,
    "continuous": true,
    "schedule": {
      "interval": {
        "period": 1,
        "unit": "Minutes",
        "start_time": 1602100553
      }
    },
    "description": "Sample transform job",
    "source_index": "opensearch_dashboards_sample_data_ecommerce",
    "target_index": "ecommerce_transform",
    "data_selection_query": {
      "match_all": {}
    },
    "page_size": 1,
    "groups": [
      {
        "terms": {
          "source_field": "customer_gender",
          "target_field": "gender"
        }
      },
      {
        "terms": {
          "source_field": "day_of_week",
          "target_field": "day"
        }
      }
    ],
    "aggregations": {
      "quantity": {
        "sum": {
          "field": "total_quantity"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 回應範例

```json
{
  "_id": "sample",
  "_version": 1,
  "_seq_no": 13,
  "_primary_term": 1,
  "transform": {
    "transform_id": "sample",
    "schema_version": 30,
    "schedule": {
      "interval": {
        "start_time": 1602100553,
        "period": 1,
        "unit": "Minutes"
      }
    },
    "metadata_id": null,
    "updated_at": 1621467964243,
    "enabled": true,
    "enabled_at": 1621467964243,
    "description": "Sample transform job",
    "source_index": "opensearch_dashboards_sample_data_ecommerce",
    "data_selection_query": {
      "match_all": {
        "boost": 1.0
      }
    },
    "target_index": "ecommerce_transform",
    "page_size": 1,
    "groups": [
      {
        "terms": {
          "source_field": "customer_gender",
          "target_field": "gender"
        }
      },
      {
        "terms": {
          "source_field": "day_of_week",
          "target_field": "day"
        }
      }
    ],
    "aggregations": {
      "quantity": {
        "sum": {
          "field": "total_quantity"
        }
      }
    },
    "continuous": true
  }
}
```

`metadata_id` 欄位由 OpenSearch 指派，在任務首次執行前為 `null`。在請求中設定此欄位不會產生任何作用。
{: .note}

## 更新轉換任務
**於 1.0 版推出**
{: .label .label-purple }

若 `transform_id` 已存在，則更新該轉換任務。此請求必須指定要更新之轉換的序號與主要分片任期。若要取得這些值，請使用 [取得轉換任務的詳細資料](#get-a-transform-jobs-details) API 呼叫。

### 端點

```json
PUT _plugins/_transform/{transform_id}?if_seq_no={seq_no}&if_primary_term={primary_term}
```

### 查詢參數

更新操作支援以下查詢參數：

參數 | 說明 | 必要
:---| :--- | :---
`if_seq_no` | 僅在上一次變更轉換任務的操作具有指定序號時，才執行轉換操作。 | 是
`if_primary_term` | 僅在上一次變更轉換任務的操作具有指定的主要分片任期時，才執行轉換操作。 | 是

### 請求本文欄位

請在請求本文中傳送完整的轉換物件。您只能變更以下欄位。

選項 | 資料類型 | 說明
:--- | :--- | :---
`enabled` | 布林值 | 轉換任務是否啟用。
`schedule` | 物件 | 轉換任務的排程。包含 `interval.start_time`、`interval.period` 和 `interval.unit` 欄位。
`interval.start_time` | 整數 | 轉換任務的 Unix epoch 開始時間。
`interval.period` | 整數 | 轉換任務的執行頻率。
`interval.unit` | 字串 | 與執行週期相關的時間單位。可用選項為 `Minutes`、`Hours` 和 `Days`。
`description` | 字串 | 描述轉換任務。
`page_size` | 整數 | IM 同時處理並編製索引的桶數。數值越高效能越好，但需要更多記憶體。若您的機器記憶體不足，IM 會自動調整此欄位並重試，直到操作成功為止。

其餘欄位請以任務現有的值重複填入。變更 `continuous`、`source_index`、`target_index`、`data_selection_query`、`groups` 或 `aggregations` 會被拒絕並傳回 `400`，而省略其中任一欄位也視為變更。例如，對於以 `"continuous": true` 建立的任務，若在本文中省略 `continuous`，將會失敗。
{: .note}

#### 範例請求

下列請求會以 ID `sample`、序號 `13` 及主要分片任期 `1` 更新轉換任務：

```json
PUT _plugins/_transform/sample?if_seq_no=13&if_primary_term=1
{
  "transform": {
    "enabled": true,
    "continuous": true,
    "schedule": {
      "interval": {
        "period": 1,
        "unit": "Minutes",
        "start_time": 1602100553
      }
    },
    "description": "Updated sample transform job",
    "source_index": "opensearch_dashboards_sample_data_ecommerce",
    "target_index": "ecommerce_transform",
    "data_selection_query": {
      "match_all": {}
    },
    "page_size": 10,
    "groups": [
      {
        "terms": {
          "source_field": "customer_gender",
          "target_field": "gender"
        }
      },
      {
        "terms": {
          "source_field": "day_of_week",
          "target_field": "day"
        }
      }
    ],
    "aggregations": {
      "quantity": {
        "sum": {
          "field": "total_quantity"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "_id": "sample",
  "_version": 2,
  "_seq_no": 14,
  "_primary_term": 1,
  "transform": {
    "transform_id": "sample",
    "schema_version": 30,
    "schedule": {
      "interval": {
        "start_time": 1602100553,
        "period": 1,
        "unit": "Minutes"
      }
    },
    "metadata_id": null,
    "updated_at": 1621467999831,
    "enabled": true,
    "enabled_at": 1621467999830,
    "description": "Updated sample transform job",
    "source_index": "opensearch_dashboards_sample_data_ecommerce",
    "data_selection_query": {
      "match_all": {
        "boost": 1.0
      }
    },
    "target_index": "ecommerce_transform",
    "page_size": 10,
    "groups": [
      {
        "terms": {
          "source_field": "customer_gender",
          "target_field": "gender"
        }
      },
      {
        "terms": {
          "source_field": "day_of_week",
          "target_field": "day"
        }
      }
    ],
    "aggregations": {
      "quantity": {
        "sum": {
          "field": "total_quantity"
        }
      }
    },
    "continuous": true
  }
}
```

## 取得轉換任務的詳細資料
**於 1.0 版推出**
{: .label .label-purple }

傳回轉換任務的詳細資料。

### 端點

```json
GET _plugins/_transform/{transform_id}
```

#### 範例請求

下列請求會傳回 ID 為 `sample` 的轉換任務詳細資料：

```json
GET _plugins/_transform/sample
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "_id": "sample",
  "_version": 3,
  "_seq_no": 15,
  "_primary_term": 1,
  "transform": {
    "transform_id": "sample",
    "schema_version": 30,
    "schedule": {
      "interval": {
        "start_time": 1602100553,
        "period": 1,
        "unit": "Minutes"
      }
    },
    "metadata_id": "cAgQ_8RVFy4ZoSZb0g4XNw",
    "updated_at": 1621468022451,
    "enabled": true,
    "enabled_at": 1621467999830,
    "description": "Updated sample transform job",
    "source_index": "opensearch_dashboards_sample_data_ecommerce",
    "data_selection_query": {
      "match_all": {
        "boost": 1.0
      }
    },
    "target_index": "ecommerce_transform",
    "page_size": 10,
    "groups": [
      {
        "terms": {
          "source_field": "customer_gender",
          "target_field": "gender"
        }
      },
      {
        "terms": {
          "source_field": "day_of_week",
          "target_field": "day"
        }
      }
    ],
    "aggregations": {
      "quantity": {
        "sum": {
          "field": "total_quantity"
        }
      }
    },
    "continuous": true
  }
}
```

您也可以省略 `transform_id` 來取得所有轉換任務的詳細資料。

#### 範例請求

下列請求會傳回所有轉換任務的詳細資料：

```json
GET _plugins/_transform/
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "total_transforms": 1,
  "transforms": [
    {
      "_id": "sample",
      "_seq_no": 15,
      "_primary_term": 1,
      "transform": {
        "transform_id": "sample",
        "schema_version": 30,
        "schedule": {
          "interval": {
            "start_time": 1602100553,
            "period": 1,
            "unit": "Minutes"
          }
        },
        "metadata_id": "cAgQ_8RVFy4ZoSZb0g4XNw",
        "updated_at": 1621468022451,
        "enabled": true,
        "enabled_at": 1621467999830,
        "description": "Updated sample transform job",
        "source_index": "opensearch_dashboards_sample_data_ecommerce",
        "data_selection_query": {
          "match_all": {
            "boost": 1.0
          }
        },
        "target_index": "ecommerce_transform",
        "page_size": 10,
        "groups": [
          {
            "terms": {
              "source_field": "customer_gender",
              "target_field": "gender"
            }
          },
          {
            "terms": {
              "source_field": "day_of_week",
              "target_field": "day"
            }
          }
        ],
        "aggregations": {
          "quantity": {
            "sum": {
              "field": "total_quantity"
            }
          }
        },
        "continuous": true
      }
    }
  ]
}
```

每個項目都會省略 `_version`，只有在您請求單一轉換任務時，回應才會傳回該欄位。

### 查詢參數

您可以指定下列 GET API 操作的查詢參數來篩選結果。

參數 | 說明 | 必要
:--- | :--- | :---
`from` | 要傳回的起始轉換任務。預設為 0。 | 否
`size` | 指定要傳回的轉換任務數量。預設為 10。 | 否
`search` | 用來篩選結果的搜尋詞彙。 | 否
`sortField` | 用來排序結果的欄位，以存放的轉換任務文件中的路徑表示，例如 `transform.transform_id.keyword` 或 `transform.updated_at`。未對應的名稱（例如 `transform_id`）會遭到拒絕並傳回 `500`。 | 否
`sortDirection` | 指定排序結果的方向。可為 `ASC` 或 `DESC`。預設為 `ASC`。 | 否

#### 範例請求

下列請求會從轉換任務 `8` 開始傳回兩筆結果，並依轉換任務 ID 排序：

```json
GET _plugins/_transform?size=2&from=8&sortField=transform.transform_id.keyword
```
{% include copy-curl.html %}

#### 範例回應

```json
{
  "total_transforms": 18,
  "transforms": [
    {
      "_id": "sample8",
      "_seq_no": 93,
      "_primary_term": 1,
      "transform": {
        "transform_id": "sample8",
        "schema_version": 30,
        "schedule": {
          "interval": {
            "start_time": 1622063596812,
            "period": 1,
            "unit": "Minutes"
          }
        },
        "metadata_id": "y4hFAB2ZURQ2dzY7BAMxWA",
        "updated_at": 1622063657233,
        "enabled": false,
        "enabled_at": null,
        "description": "Sample transform job",
        "source_index": "opensearch_dashboards_sample_data_ecommerce",
        "data_selection_query": {
          "match_all": {
            "boost": 1.0
          }
        },
        "target_index": "ecommerce_transform8",
        "page_size": 1,
        "groups": [
          {
            "terms": {
              "source_field": "customer_gender",
              "target_field": "gender"
            }
          },
          {
            "terms": {
              "source_field": "day_of_week",
              "target_field": "day"
            }
          }
        ],
        "aggregations": {
          "quantity": {
            "sum": {
              "field": "total_quantity"
            }
          }
        },
        "continuous": false
      }
    },
    {
      "_id": "sample9",
      "_seq_no": 98,
      "_primary_term": 1,
      "transform": {
        "transform_id": "sample9",
        "schema_version": 30,
        "schedule": {
          "interval": {
            "start_time": 1622063598065,
            "period": 1,
            "unit": "Minutes"
          }
        },
        "metadata_id": "x8tCIiYMTE3veSbIJkit5A",
        "updated_at": 1622063658388,
        "enabled": false,
        "enabled_at": null,
        "description": "Sample transform job",
        "source_index": "opensearch_dashboards_sample_data_ecommerce",
        "data_selection_query": {
          "match_all": {
            "boost": 1.0
          }
        },
        "target_index": "ecommerce_transform9",
        "page_size": 1,
        "groups": [
          {
            "terms": {
              "source_field": "customer_gender",
              "target_field": "gender"
            }
          },
          {
            "terms": {
              "source_field": "day_of_week",
              "target_field": "day"
            }
          }
        ],
        "aggregations": {
          "quantity": {
            "sum": {
              "field": "total_quantity"
            }
          }
        },
        "continuous": false
      }
    }
  ]
}
```

## 啟動轉換作業
**於 1.0 版引入**
{: .label .label-purple }

使用 API 建立的轉換作業會自動啟用，但如果您需要啟用作業，可以使用 start API 操作。 

### 端點

```json
POST _plugins/_transform/{transform_id}/_start
```

#### 請求範例

下列請求會啟動 ID 為 `sample` 的轉換作業：

```json
POST _plugins/_transform/sample/_start
```
{% include copy-curl.html %}

#### 回應範例

```json
{
  "acknowledged": true
}
```

## 停止轉換作業
**於 1.0 版引入**
{: .label .label-purple }

停止轉換作業。 

### 端點

```json
POST _plugins/_transform/{transform_id}/_stop
```

#### 請求範例

下列請求會停止 ID 為 `sample` 的轉換作業：

```json
POST _plugins/_transform/sample/_stop
```
{% include copy-curl.html %}

#### 回應範例

```json
{
  "acknowledged": true
}
```

## 取得轉換作業的狀態
**於 1.0 版引入**
{: .label .label-purple }

傳回轉換作業的狀態與中繼資料。 

### 端點

```json
GET _plugins/_transform/{transform_id}/_explain
```

#### 請求範例

下列請求會傳回 ID 為 `sample` 的轉換作業詳細資訊：

```json
GET _plugins/_transform/sample/_explain
```
{% include copy-curl.html %}

#### 回應範例

```json
{
  "sample": {
    "metadata_id": "cAgQ_8RVFy4ZoSZb0g4XNw",
    "transform_metadata": {
      "transform_id": "sample",
      "last_updated_at": 1621883525873,
      "status": "started",
      "failure_reason": null,
      "stats": {
        "pages_processed": 3,
        "documents_processed": 4675,
        "documents_indexed": 14,
        "index_time_in_millis": 22,
        "search_time_in_millis": 88
      },
      "continuous_stats": {
        "last_timestamp": 1621883525672,
        "documents_behind": {
          "opensearch_dashboards_sample_data_ecommerce": 0
        }
      }
    }
  }
}
```

作業執行時，`status` 欄位為 `started`；非持續性作業完成後為 `finished`；您停止作業後為 `stopped`；作業失敗時則為 `failed`，此時 `failure_reason` 會包含訊息，例如 `Failed to index the documents`。`continuous_stats` 物件僅存在於持續性作業中，其中 `documents_behind` 會計算作業尚未轉換的來源文件數量。

在作業首次執行之前，`metadata_id` 和 `transform_metadata` 都是 `null`。
{: .note}

## 預覽轉換作業的結果
**於 1.0 版引入**
{: .label .label-purple }

傳回轉換後索引的預覽。預覽不會建立作業，也不會寫入目標索引。

### 端點

```json
POST _plugins/_transform/_preview
```

#### 請求範例

```json
POST _plugins/_transform/_preview
{
  "transform": {
    "enabled": false,
    "schedule": {
      "interval": {
        "period": 1,
        "unit": "Minutes",
        "start_time": 1602100553
      }
    },
    "description": "test transform",
    "source_index": "opensearch_dashboards_sample_data_ecommerce",
    "target_index": "ecommerce_transform",
    "data_selection_query": {
      "match_all": {}
    },
    "page_size": 10,
    "groups": [
      {
        "terms": {
          "source_field": "customer_gender",
          "target_field": "gender"
        }
      },
      {
        "terms": {
          "source_field": "day_of_week",
          "target_field": "day"
        }
      }
    ],
    "aggregations": {
      "quantity": {
        "sum": {
          "field": "total_quantity"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 回應範例

每份文件都包含分組欄位、彙總值，以及桶中的來源文件數量，此數量會同時在 `_doc_count` 和 `transform._doc_count` 中回報：

```json
{
  "documents" : [
    {
      "_doc_count" : 399,
      "quantity" : 862.0,
      "gender" : "FEMALE",
      "transform._doc_count" : 399,
      "day" : "Friday"
    },
    {
      "_doc_count" : 320,
      "quantity" : 682.0,
      "gender" : "FEMALE",
      "transform._doc_count" : 320,
      "day" : "Monday"
    },
    {
      "_doc_count" : 365,
      "quantity" : 772.0,
      "gender" : "FEMALE",
      "transform._doc_count" : 365,
      "day" : "Saturday"
    },
    {
      "_doc_count" : 315,
      "quantity" : 669.0,
      "gender" : "FEMALE",
      "transform._doc_count" : 315,
      "day" : "Sunday"
    },
    {
      "_doc_count" : 417,
      "quantity" : 887.0,
      "gender" : "FEMALE",
      "transform._doc_count" : 417,
      "day" : "Thursday"
    },
    {
      "_doc_count" : 323,
      "quantity" : 690.0,
      "gender" : "FEMALE",
      "transform._doc_count" : 323,
      "day" : "Tuesday"
    },
    {
      "_doc_count" : 294,
      "quantity" : 612.0,
      "gender" : "FEMALE",
      "transform._doc_count" : 294,
      "day" : "Wednesday"
    },
    {
      "_doc_count" : 371,
      "quantity" : 821.0,
      "gender" : "MALE",
      "transform._doc_count" : 371,
      "day" : "Friday"
    },
    {
      "_doc_count" : 259,
      "quantity" : 586.0,
      "gender" : "MALE",
      "transform._doc_count" : 259,
      "day" : "Monday"
    },
    {
      "_doc_count" : 371,
      "quantity" : 798.0,
      "gender" : "MALE",
      "transform._doc_count" : 371,
      "day" : "Saturday"
    }
  ]
}
```

預覽最多會傳回 `page_size` 份文件，因此請提高 `page_size` 的值以檢視其餘的桶。
{: .note}

## 刪除轉換作業
**於 1.0 版引入**
{: .label .label-purple }

刪除轉換作業。此操作不會刪除來源或目標索引。 

已啟用的作業無法刪除。請先[停止作業](#stop-a-transform-job)，或將 `force` 設為 `true`，以在作業仍啟用時將其刪除。

### 端點

```json
DELETE _plugins/_transform/{transform_id}
```

### 查詢參數

參數 | 說明 | 必要
:--- | :--- | :---
`force` | 即使轉換作業已啟用，仍會將其刪除。預設值為 `false`。 | 否

#### 請求範例

下列請求會刪除 ID 為 `sample` 的轉換作業：

```json
DELETE _plugins/_transform/sample
```
{% include copy-curl.html %}

#### 回應範例

```json
{
  "took": 205,
  "errors": false,
  "items": [
    {
      "delete": {
        "_index": ".opendistro-ism-config",
        "_id": "sample",
        "_version": 4,
        "result": "deleted",
        "forced_refresh": true,
        "_shards": {
          "total": 2,
          "successful": 1,
          "failed": 0
        },
        "_seq_no": 6,
        "_primary_term": 1,
        "status": 200
      }
    }
  ]
}
```

刪除仍啟用的作業會失敗，並傳回 `409`。刪除不存在的作業會傳回 `200`，且項目中會包含 `"result": "not_found"` 和 `"status": 404`。
{: .note}
