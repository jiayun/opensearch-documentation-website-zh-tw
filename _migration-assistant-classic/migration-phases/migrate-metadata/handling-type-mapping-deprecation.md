---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "轉換類型對應"
nav_order: 1
parent: Migrate metadata
grand_parent: Migration phases
permalink: /classic/migration-assistant/migration-phases/migrate-metadata/handling-type-mapping-deprecation/
---

# 轉換類型對應

{: .note }
這些轉換可能不適用於您的情境，但建立轉換的框架旨在處理變更，例如在修改工作負載或將其移至新目標時，進行資料異動、資料擴充及其他修改。

本指南提供在從 Elasticsearch 6.x 或更早版本遷移至 OpenSearch 時，管理類型對應功能棄用的解決方案。

在 Elasticsearch 6.x 之前的版本中，一個索引可以包含多個類型，每個類型都有自己的對應。這些類型可讓您在單一索引中儲存及查詢不同種類的文件，例如書籍和電影。舉例來說，`book` 和 `movie` 類型可以共用 `title` 這類欄位，同時各自擁有專屬於該類型的其他欄位。

較新版本的 Elasticsearch 和 OpenSearch 已不再支援多個對應類型。現在每個索引僅支援單一對應類型。遷移期間，您必須定義如何轉換或重新建構使用多個類型的資料。以下範例顯示多個對應類型：


```json
GET /library/_mappings
{
  "library": {
    "mappings": {
      "book": {
        "properties": {
          "title":      { "type": "text" },
          "pageCount":  { "type": "integer" }
        }
      },
      "movie": {
        "properties": {
          "title":      { "type": "text" },
          "runTime":    { "type": "integer" }
        }
      }
    }
  }
}
```

如需更多資訊，請參閱 [Elasticsearch 官方文件中有關移除對應類型的說明](https://www.elastic.co/guide/en/elasticsearch/reference/7.10/removal-of-types.html)。

## 使用類型對應轉換器

若要解決類型對應棄用的問題，請使用 `TypeMappingsSanitizationTransformer`。此轉換器可以修改資料，包括中繼資料、文件和請求，讓先前對應的資料可在 OpenSearch 中使用。若要使用對應轉換器：

1. 瀏覽至 bootstrap box 並使用 Vim 開啟 `cdk.context.json` 檔案。
2. 新增或更新 `reindexFromSnapshotExtraArgs` 索引鍵，加入 `--doc-transformer-config-file /shared-logs-output/transformation.json`。
3. 新增或更新 `trafficReplayerExtraArgs` 索引鍵，加入 `--transformer-config-file /shared-logs-output/transformation.json`。
4. 部署 Migration Assistant。
5. 瀏覽至 Migration Assistant 主控台。
6. 建立名為 `/shared-logs-output/transformation.json` 的檔案。
7. 將您的轉換組態新增至該檔案。如需組態選項，請參閱[組態選項](#configuration-options)。
8. 執行中繼資料遷移時，使用 `console metadata migrate --transformer-config-file /shared-logs-output/transformation.json` 命令搭配轉換器執行組態。

每當轉換組態更新時，必須停止並重新啟動回填和 Replayer 工具，才能套用變更。先前遷移的資料和中繼資料可能需要清除，以避免狀態不一致。

### 組態選項

`TypeMappingsSanitizationTransformer` 支援多種管理類型對應的策略：

1. **將不同類型路由至個別索引**：將不同類型分割至各自的索引。
2. **將所有類型合併至單一索引**：將多個類型合併至單一索引。
3. **捨棄特定類型**：僅選擇性遷移特定類型。
4. **保留原始結構**：維持相同的索引名稱，同時符合新的類型標準。

### 類型對應轉換器組態結構描述

類型對應轉換器使用下列組態選項。

| **欄位**  | **類型** | **必要** | **說明** | 
| :--- | :--- | :--- | :--- |
| `staticMappings`   | `object` | 否   | 用於**靜態**路由特定類型的 `{ indexName: { typeName: targetIndex } }` 對應。<br/><br/> 對於此頁面上列出的任何**索引**，未包含在其物件中的類型會遭到**捨棄**（這些省略的類型不會遷移任何資料或請求）。   |
| `regexMappings`    | `array`  | 否   | 用於將來源索引/類型名稱**動態**路由至目標索引的**規則運算式**規則清單。<br/><br/> 此陣列中的每個元素本身都是一個物件，包含 `sourceIndexPattern`、`sourceTypePattern` 和 `targetIndexPattern` 欄位。<br/><br/> 如需**預設值**的相關資訊，請參閱[預設值](#Defaults)。 |
| `sourceProperties` | `object` | 是  | 來源的額外**中繼資料**（例如其 Elasticsearch/OpenSearch 版本）。至少必須包含 `"version"`，並具有 `"major"` 和 `"minor"` 欄位。   |

下列範例 JSON 組態提供轉換結構描述：

<details markdown="block">
<summary>範例 JSON 組態</summary>

```json
{
  "TypeMappingSanitizationTransformerProvider": {
    "staticMappings": {
      "{index-name-1}": {
        "{type-name-1}": "{target-index-name-1}",
        "{type-name-2}": "{target-index-name-2}"
      }
    },
    "regexMappings": [
      {
        "sourceIndexPattern": "{source-index-pattern}",
        "sourceTypePattern": "{source-type-pattern}",
        "targetIndexPattern": "{target-index-pattern}"
      }
    ],
    "sourceProperties": {
      "version": {
        "major": "NUMBER",
        "minor": "NUMBER"
      }
    }
  }
}
```
{% include copy.html %}

</details>

## 範例組態

下列範例組態說明如何針對不同的對應類型情境使用轉換器。

### 將不同類型路由至個別索引

如果您有一個索引 `activity`，其中包含類型 `user` 和 `post`，且您想將其分割至個別索引，請使用下列組態：

```json
[
  {
    "TypeMappingSanitizationTransformerProvider": {
      "staticMappings": {
        "activity": {
          "user": "new_users",
          "post": "new_posts"
        }
      },
      "sourceProperties": {
        "version": {
          "major": 6,
          "minor": 8
        }
      }
    }
  }
]
```
{% include copy.html %}

此轉換器將執行下列操作：

- 將類型為 `user` 的文件路由至 `new_users` 索引。
- 將類型為 `post` 的文件路由至 `new_posts` 索引。

### 將所有類型合併至單一索引

若要將所有類型合併至單一索引，請使用下列組態：

```json
[
  {
    "TypeMappingSanitizationTransformerProvider": {
      "staticMappings": {
        "activity": {
          "user": "activity",
          "post": "activity"
        }
      },
      "sourceProperties": {
        "version": {
          "major": 6,
          "minor": 8
        }
      }
    }
  }
]
```
{% include copy.html %}

### 捨棄特定類型

若只要遷移 `activity` 索引中的 `user` 類型，並捨棄所有未直接指定類型的文件/請求，請使用下列組態：

```json
[
  {
    "TypeMappingSanitizationTransformerProvider": {
      "staticMappings": {
        "activity": {
          "user": "users_only"
        }
      },
      "sourceProperties": {
        "version": {
          "major": 6,
          "minor": 8
        }
      }
    }
  }
]
```
{% include copy.html %}

此組態僅遷移類型為 `user` 的文件，並忽略 `activity` 索引中的其他文件類型。

### 保留原始結構

若只要遷移特定類型並保留原始結構，請使用下列組態：

```json
[
  {
    "TypeMappingSanitizationTransformerProvider": {
      "regexMappings": [
        {
          "sourceIndexPattern": "(.*)",
          "sourceTypePattern": ".*",
          "targetIndexPattern": "$1"
        }
      ],
      "sourceProperties": {
        "version": {
          "major": 6,
          "minor": 8
        }
      }
    }
  }
]
```
{% include copy.html %}

這等同於將所有類型合併到一個索引的策略，但同時也使用以模式為基礎的路由策略。

### 結合多種策略

您可以同時結合靜態對應與以正規表示式為基礎的對應，在單一遷移中管理不同的索引或模式。例如，您可能有一個必須使用 `staticMappings` 的索引，以及另一個使用 `regexMappings` 依模式路由所有類型的索引。

對於每個文件、請求或中繼資料項目（大量請求會逐一處理），會執行下列步驟：

1. 檢查索引是否符合靜態對應中的項目。
   - 若符合，則檢查類型是否符合該靜態對應項目的索引元件。
     - 若類型符合，則套用對應，產生的索引會包含 type 鍵的值。
     - 若類型不符合，則捨棄該請求／文件／中繼資料，不予遷移。
2. 若索引在靜態對應中沒有符合項目，則依序從頭到尾檢查索引與類型的組合是否符合 regex 對應清單中的每個項目。若找到符合項目，則套用對應，產生的索引會包含 type 鍵的值，且不再執行後續的 regex 比對。
3. 任何不符合前述情況的請求、文件或中繼資料都會被捨棄，其所包含的文件也不會被遷移。

下列範例示範如何為不同索引結合靜態對應與以 regex 為基礎的對應：

```json
[
  {
    "TypeMappingSanitizationTransformerProvider": {
      "staticMappings": {
        "activity": {
          "user": "users_activity",
          "post": "posts_activity"
        },
        "logs": {
          "error": "logs_error",
          "info": "logs_info"
        }
      },
      "regexMappings": [
        {
          "sourceIndexPattern": "orders.*",
          "sourceTypePattern": ".*",
          "targetIndexPattern": "all_orders"
        }
      ],
      "sourceProperties": {
        "version": {
          "major": 6,
          "minor": 8
        }
      }
    }
  }
]
```
{% include copy.html %}

### 預設值

當轉換組態中缺少 `regexMappings` 鍵時，`regexMappings` 會預設為下列內容：

```json
{
  "regexMappings": [
    {
      "sourceIndexPattern": "(.+)",
      "sourceTypePattern": "_doc",
      "targetIndexPattern": "$1"
    },
    {
      "sourceIndexPattern": "(.+)",
      "sourceTypePattern": "(.+)",
      "targetIndexPattern": "$1_$2"
    }
  ]
}
```
{% include copy.html %}

這會使在 Elasticsearch 6.x 或更新版本中建立的索引保留其索引名稱，同時將在 Elasticsearch 5.x 中建立的索引的類型名稱與索引名稱合併。若您想保留在 Elasticsearch 5.x 中建立的索引的索引名稱，請使用 `staticMappings` 選項，或使用 `regexMappings` 選項覆寫類型對應。

## 限制

使用轉換器時，請記住下列限制。

### Traffic Replayer

對於 Traffic Replayer，僅支援**包含類型的請求中的一個子集**。這些請求列於下表。

| **操作** | **HTTP 方法** | **端點**   | **說明**  |
| :--- | :--- | :--- | :--- |
| **Index (by ID)**  | PUT/POST           | `/{index}/{type}/{id}`  | 以明確 ID 建立或更新單一文件。   |
| **Index (auto ID)**          | PUT/POST           | `/{index}/{type}/`      | 建立單一文件，其 ID 自動產生。  |
| **Get Document**             | GET                | `/{index}/{type}/{id}`  | 依 ID 擷取文件。  |
| **Bulk Index/Update/Delete** | PUT/POST           | `/_bulk`                | 在單一請求中執行多個建立／更新／刪除操作。 |
| **Bulk Index/Update/Delete** | PUT/POST           | `/{index}/_bulk`        | 在單一請求中以預設索引指派執行多個建立／更新／刪除操作。                                                                                                                                                 |
| **Bulk Index/Update/Delete** | PUT/POST           | `/{index}/{type}/_bulk` | 在單一請求中以預設索引與類型指派執行多個建立／更新／刪除操作。                                                                                                                                        |
| **Create/Update Index**      | PUT/POST           | `/{index}`              | 建立或更新索引。<br/><br/> Traffic Replayer 不支援 **Split** 行為。若要提供意見回饋或為此功能投票，請參閱[此 GitHub issue](https://github.com/opensearch-project/opensearch-migrations/issues/1305)。 |

### Reindex-from-Snapshot

對於 `Reindex-From-Snapshot,`，在 Elasticsearch 6.x 或更新版本中建立的索引會使用 `_doc` 作為所有文件的類型，即使在 Elasticsearch 6 中指定了不同的類型也一樣。
