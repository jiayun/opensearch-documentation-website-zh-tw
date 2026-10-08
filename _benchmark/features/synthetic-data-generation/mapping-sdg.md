---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用索引對應產生資料"
nav_order: 15
parent: Synthetic data generation
grand_parent: Additional features
---

# 使用索引對應產生資料

您可以使用 OpenSearch 索引對應來產生合成資料。這種方法在自動化與自訂之間取得平衡。

若要使用此方法，請將您的 OpenSearch 索引對應儲存至 JSON 檔案：

```json
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "standard",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "description": {
        "type": "text"
      },
      "price": {
        "type": "float"
      },
      "created_at": {
        "type": "date",
        "format": "strict_date_optional_time||epoch_millis"
      },
      "is_available": {
        "type": "boolean"
      },
      "category_id": {
        "type": "integer"
      },
      "tags": {
        "type": "keyword"
      }
    }
  },
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  }
}
```

OpenSearch Benchmark 適用於任何有效的索引對應，不論其複雜程度為何。您可以提供類似以下範例的更複雜對應：

<details markdown="block">
<summary>
    對應
</summary>
{: .text-delta}

```json
{
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "user": {
        "type": "object",
        "properties": {
          "id": {
            "type": "keyword"
          },
          "email": {
            "type": "keyword"
          },
          "name": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              },
              "completion": {
                "type": "completion"
              }
            },
            "analyzer": "standard"
          },
          "address": {
            "type": "object",
            "properties": {
              "street": {
                "type": "text"
              },
              "city": {
                "type": "keyword"
              },
              "state": {
                "type": "keyword"
              },
              "zip": {
                "type": "keyword"
              },
              "location": {
                "type": "geo_point"
              }
            }
          },
          "preferences": {
            "type": "object",
            "dynamic": true
          }
        }
      },
      "orders": {
        "type": "nested",
        "properties": {
          "id": {
            "type": "keyword"
          },
          "date": {
            "type": "date",
            "format": "strict_date_optional_time||epoch_millis"
          },
          "amount": {
            "type": "scaled_float",
            "scaling_factor": 100
          },
          "status": {
            "type": "keyword"
          },
          "items": {
            "type": "nested",
            "properties": {
              "product_id": {
                "type": "keyword"
              },
              "name": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "quantity": {
                "type": "short"
              },
              "price": {
                "type": "float"
              },
              "categories": {
                "type": "keyword"
              }
            }
          },
          "shipping_address": {
            "type": "object",
            "properties": {
              "street": {
                "type": "text"
              },
              "city": {
                "type": "keyword"
              },
              "state": {
                "type": "keyword"
              },
              "zip": {
                "type": "keyword"
              },
              "location": {
                "type": "geo_point"
              }
            }
          }
        }
      },
      "activity_log": {
        "type": "nested",
        "properties": {
          "timestamp": {
            "type": "date"
          },
          "action": {
            "type": "keyword"
          },
          "ip_address": {
            "type": "ip"
          },
          "details": {
            "type": "object",
            "enabled": false
          }
        }
      },
      "metadata": {
        "type": "object",
        "properties": {
          "created_at": {
            "type": "date"
          },
          "updated_at": {
            "type": "date"
          },
          "tags": {
            "type": "keyword"
          },
          "source": {
            "type": "keyword"
          },
          "version": {
            "type": "integer"
          }
        }
      },
      "description": {
        "type": "text",
        "analyzer": "english",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          },
          "standard": {
            "type": "text",
            "analyzer": "standard"
          }
        }
      },
      "ranking_scores": {
        "type": "object",
        "properties": {
          "popularity": {
            "type": "float"
          },
          "relevance": {
            "type": "float"
          },
          "quality": {
            "type": "float"
          }
        }
      },
      "permissions": {
        "type": "nested",
        "properties": {
          "user_id": {
            "type": "keyword"
          },
          "role": {
            "type": "keyword"
          },
          "granted_at": {
            "type": "date"
          }
        }
      }
    }
  },
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 2,
    "analysis": {
      "analyzer": {
        "email_analyzer": {
          "type": "custom",
          "tokenizer": "uax_url_email",
          "filter": ["lowercase", "stop"]
        }
      }
    }
  }
}
```

</details>

## 產生資料

若要使用索引對應產生合成資料，請使用 `generate-data` 子命令，並提供必要的索引對應檔案、索引名稱、輸出路徑，以及要產生的資料總量：

```shell
osb generate-data --index-name <NAME_OF_DATA_CORPORA> --index-mappings <PATH_TO_INDEX_MAPPINGS> --output-path <DESIRED_OUTPUT_PATH> --total-size <TOTAL_SIZE_OF_DATA_CORPORA_GENERATED_IN_GB>
```
{% include copy.html %}

如需可用參數及其說明的完整清單，請參閱 [`generate-data` 命令參考]({{site.url}}{{site.baseurl}}/benchmark/reference/commands/generate-data/)。

## 輸出範例

以下是產生 100 GB 資料時的輸出範例：

```
   ____                  _____                      __       ____                  __                         __
  / __ \____  ___  ____ / ___/___  ____ ___________/ /_     / __ )___  ____  _____/ /_  ____ ___  ____ ______/ /__
 / / / / __ \/ _ \/ __ \\__ \/ _ \/ __ `/ ___/ ___/ __ \   / __  / _ \/ __ \/ ___/ __ \/ __ `__ \/ __ `/ ___/ //_/
/ /_/ / /_/ /  __/ / / /__/ /  __/ /_/ / /  / /__/ / / /  / /_/ /  __/ / / / /__/ / / / / / / / / /_/ / /  / ,<
\____/ .___/\___/_/ /_/____/\___/\__,_/_/   \___/_/ /_/  /_____/\___/_/ /_/\___/_/ /_/_/ /_/ /_/\__,_/_/  /_/|_|
    /_/


[NOTE] ✨ Dashboard link to monitor processes and task streams: [http://127.0.0.1:8787/status]
[NOTE] ✨ For users who are running generation on a virtual machine, consider SSH port forwarding (tunneling) to localhost to view dashboard.
[NOTE] Example of localhost command for SSH port forwarding (tunneling) from an AWS EC2 instance:
ssh -i <PEM_FILEPATH> -N -L localhost:8787:localhost:8787 ec2-user@<DNS>

Total GB to generate: [1]
Average document size in bytes: [412]
Max file size in GB: [40]

100%|███████████████████████████████████████████████████████████████████| 100.07G/100.07G [3:35:29<00:00, 3.98MB/s]

Generated 24271844660 docs in 12000 seconds. Total dataset size is 100.21GB.
✅ Visit the following path to view synthetically generated data: /home/ec2-user/

-----------------------------------
[INFO] ✅ SUCCESS (took 272 seconds)
-----------------------------------
```

## 進階組態

您可以建立 YAML 組態檔案，控制合成資料的產生方式。以下組態檔案範例在 `MappingGenerationValues` 參數中定義自訂規則：

```yml
MappingGenerationValues:
  # For users who want more granular control over how data is generated when providing an OpenSearch mapping
  generator_overrides:
    # Overrides all instances of generators with these settings. Specify type and params
    integer:
      min: 0
      max: 20
    long:
      min: 0
      max: 1000
    float:
      min: 0.0
      max: 1.0
    double:
      min: 0.0
      max: 2000.0
    date:
      start_date: "2020-01-01"
      end_date: "2023-01-01"
      format: "yyyy-mm-dd"
    text:
      must_include: ["lorem", "ipsum"]
    keyword:
      choices: ["alpha", "beta", "gamma"]

  field_overrides:
    # Specify field name as key of dict. For its values, specify generator and its params. Params must adhere to existing params for each generator
    # For nested fields, use dot notation: Example preferences.allergies if allergies is a subfield of preferences object
    title:
      generator: generate_keyword
      params:
        choices: ["Helly R", "Mark S", "Irving B"]

    promo_codes:
      generator: generate_keyword
      params:
        choices: ["HOT_SUMMER", "TREATSYUM!"]

    # Nested fields, use dot notation
    orders.items.product_id:
      generator: generate_keyword
      params:
        choices: ["Python", "English"]
```
{% include copy.html %}

`MappingGenerationValues` 支援下列參數。

| 參數 | 說明 |
|---|---|
| `generator_overrides` | 為特定 OpenSearch 欄位類型定義自訂產生器規則。任何使用對應類型的欄位都會遵循這些規則。請參閱[產生器覆寫參數](#generator-overrides-parameters)。 |
| `field_overrides` | 依欄位名稱為個別欄位定義產生器規則。這些規則僅適用於明確列出的欄位。對於巢狀欄位，請使用點記法（例如 `orders.items.product_id`）。請參閱[欄位覆寫參數](#field-overrides-parameters)。 |

如果同時存在 `generator_overrides` 和 `field_overrides`，則 `field_overrides` 優先。
{: .important}

#### 產生器覆寫參數

`generator_overrides` 中的每種 OpenSearch 欄位類型都可使用下列參數。

| 欄位類型 | 參數 |
|---|---|
| `integer`, `long`, `short`, `byte` | `min`, `max` |
| `float`, `double` | `min`, `max`, `round`（四捨五入後保留的小數位數） |
| `date` | `start_date`, `end_date`, `format` |
| `text` | `must_include`（要包含在產生文字中的詞彙陣列） |
| `keyword` | `choices`（供隨機選取的關鍵字陣列） |

#### 欄位覆寫參數

下列產生器及其參數可用於 `field_overrides`。

| 產生器 | 參數 |
|---|---|
| `generate_text` | `must_include`（要包含在產生文字中的詞彙陣列） |
| `generate_keyword` | `choices`（供隨機選取的關鍵字陣列） |
| `generate_integer` | `min`, `max` |
| `generate_long` | `min`, `max` |
| `generate_short` | `min`, `max` |
| `generate_byte` | `min`, `max` |
| `generate_float` | `min`, `max`, `round`（四捨五入後保留的小數位數） |
| `generate_double` | `min`, `max` |
| `generate_boolean` | 不適用|
| `generate_date` | `format`, `start_date`, `end_date` |
| `generate_ip` | 不適用|
| `generate_geo_point` | 不適用|
| `generate_knn_vector` | `dimension`, `sample_vectors`, `noise_factor`, `distribution_type`, `normalize`。請參閱[產生向量](/benchmark/features/synthetic-data-generation/generating-vectors/)。 |
| `generate_sparse_vector` | `num_tokens`, `min_weight`, `max_weight`, `token_id_start`, `token_id_step`。請參閱[產生向量](/benchmark/features/synthetic-data-generation/generating-vectors/)。 |

### 使用組態

若要使用您的組態檔案，請在 `--custom-config` 參數中提供其完整路徑：

```shell
osb generate-data --index-name <NAME_OF_DATA_CORPORA> --index-mappings <PATH_TO_INDEX_MAPPINGS> --output-path <DESIRED_OUTPUT_PATH> --total-size <TOTAL_SIZE_OF_DATA_CORPORA_GENERATED_IN_GB> --custom-config ~/Desktop/sdg-config.yml
```
{% include copy.html %}

## 相關文件

- [`generate-data` 命令參考]({{site.url}}{{site.baseurl}}/benchmark/reference/commands/generate-data/)
- [使用自訂邏輯產生資料]({{site.url}}{{site.baseurl}}/benchmark/features/synthetic-data-generation/custom-logic-sdg/)