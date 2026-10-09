---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "ISM 支援的操作"
nav_order: 10
parent: Policies
grand_parent: Index State Management
has_children: false
---


# ISM 支援的操作

ISM 支援以下操作：

- [強制合併](#force-merge)
- [唯讀](#read-only)
- [讀寫](#read-write)
- [發布欄位定義域](#publish-field-domains)
- [副本數量](#replica-count)
- [縮減](#shrink)
- [關閉](#close)
- [開啟](#open)
- [刪除](#delete)
- [輪替](#rollover)
- [通知](#notification)
- [快照](#snapshot)
- [將索引轉換為遠端索引](#convert-index-to-remote)
- [索引優先順序](#index-priority)
- [分配](#allocation)
- [彙整](#rollup)
- [停止複寫](#stop-replication)
- [僅供搜尋](#search-only)

## 強制合併

透過合併個別分片的分段，減少 Lucene 分段的數量。此操作會在開始合併程序之前，嘗試將索引設定為 `read-only` 狀態。

參數 | 說明 | 類型 | 必要
:--- | :--- |:--- |:--- |
`max_num_segments` | 分片要縮減至的分段數量。 | 整數 | 是

以下範例將每個分片的分段合併為單一分段：

```json
{
  "force_merge": {
    "max_num_segments": 1
  }
}
```
{% include copy.html %}

## 唯讀

將受管理的索引設定為唯讀。

`read_only` 操作不接受任何參數：

```json
{
  "read_only": {}
}
```
{% include copy.html %}

為受管理的索引將索引設定 `index.blocks.write` 設定為 `true`。

`index.blocks.write` 區塊不會阻止索引重新整理。
{: .note}

## 讀寫

將受管理的索引設定為可寫入。

`read_write` 操作不接受任何參數：

```json
{
  "read_write": {}
}
```
{% include copy.html %}

## 發布欄位定義域
**於 3.9 版推出**
{: .label .label-purple }

為受管理的索引計算欄位定義域 (field domain)，並將其發布至索引中繼資料。OpenSearch 使用欄位定義域進行[索引層級的搜尋剪枝]({{site.url}}{{site.baseurl}}/search-plugins/index-level-search-pruning/)。

欄位定義域包含單一索引中某個欄位的最小值與最大值。`date_range` 欄位定義域類型適用於 `date` 與 `date_nanos` 欄位。對於 `date` 欄位，ISM 以 epoch 毫秒儲存邊界；對於 `date_nanos` 欄位，ISM 以 epoch 奈秒儲存邊界。

在計算欄位定義域之前，ISM 會先重新整理索引。接著為每個已設定的欄位計算最小值與最大值，並將其發布至索引的 `index_field_domains` 中繼資料。如果某個已設定的欄位在索引中沒有任何值，ISM 就不會為該欄位發布欄位定義域；如果沒有產生任何欄位定義域，此操作會在未發布任何欄位定義域的情況下完成。

參數 | 說明 | 類型 | 必要
:--- | :--- |:--- |:--- |
`fields` | ISM 要計算並發布欄位定義域的欄位。 | 陣列 | 是
`fields.field` | 欄位名稱。 | 字串 | 是
`fields.type` | 欄位定義域類型。有效值為 `date_range`。 | 字串 | 是

以下範例為 `@timestamp` 欄位發布 `date_range` 欄位定義域：

```json
{
  "publish_field_domains": {
    "fields": [
      {
        "field": "@timestamp",
        "type": "date_range"
      }
    ]
  }
}
```
{% include copy.html %}

在此操作執行之前，受管理的索引必須處於寫入封鎖狀態，因此請在 `publish_field_domains` 之前加入 `read_only` 操作：

```json
{
  "actions": [
    {
      "read_only": {}
    },
    {
      "publish_field_domains": {
        "fields": [
          {
            "field": "@timestamp",
            "type": "date_range"
          }
        ]
      }
    }
  ]
}
```
{% include copy.html %}

此操作僅適用於發布後仍維持寫入封鎖狀態的索引。如果恢復寫入，新文件可能會落在已發布的欄位定義域之外，剪枝可能會略過包含符合條件文件的索引，從而無聲地遺失搜尋結果。
{: .important}

如果已啟用 Security 外掛程式，ISM 執行使用者必須具有使用 `indices:admin/field_domains/put` 操作發布欄位定義域的權限。

## 副本數量

設定要指派給索引的副本數量。

參數 | 說明 | 類型 | 必要
:--- | :--- |:--- |:--- |
`number_of_replicas` | 定義要指派給索引的副本數量。 | 整數 | 是

以下範例為索引指派兩個副本：

```json
{
  "replica_count": {
    "number_of_replicas": 2
  }
}
```
{% include copy.html %}

如需設定副本的資訊，請參閱 [主要分片與副本分片]({{site.url}}{{site.baseurl}}/intro/#primary-and-replica-shards)。

## 縮減

允許您減少索引中的主要分片數量。透過此操作，您可以指定：

- 目標索引應包含的主要分片數量。
- 目標索引中主要分片的最大分片大小。
- 指定縮減目標索引主要分片數量的百分比。

以下範例將索引縮減為一個主要分片，透過在來源索引名稱後附加 `_shrunken` 來命名目標索引，並新增 `my-alias` 別名：

```json
"shrink": {
    "num_new_shards": 1,
    "target_index_name_template": {
        "source": "{% raw %}{{ctx.index}}{% endraw %}_shrunken"
    },
    "aliases": [
      {
        "my-alias": {}
      }
    ],
    "switch_aliases": true,
    "force_unsafe": false
}
```
{% include copy.html %}

參數 | 說明 | 類型 | 範例 | 必要
:--- | :--- |:--- |:--- |
`num_new_shards` | 縮減後索引中主要分片的最大數量。 | 整數 | `5` | 是。但不可與 `max_shard_size` 或 `percentage_of_source_shards` 搭配使用。
`max_shard_size` | 目標索引中分片的最大大小 (位元組)。 | 關鍵字 | `5gb` | 是，但不可與 `num_new_shards` 或 `percentage_of_source_shards` 搭配使用。
`percentage_of_source_shards` | 要縮減的原始主要分片數量的百分比。此參數表示縮減主要分片數量時使用的最小百分比。必須介於 0.0 與 1.0 之間 (不含端點)。 | 百分比 | `0.5` | 是，但不可與 `max_shard_size` 或 `num_new_shards` 搭配使用
`target_index_name_template` | 縮減後索引的名稱。接受字串以及 Mustache 變數 `{% raw %}{{ctx.index}}{% endraw %}` 和 `{% raw %}{{ctx.indexUuid}}{% endraw %}`。 | 字串或 Mustache 範本 | `{"source": "{% raw %}{{ctx.index}}_shrunken"}{% endraw %}` | 否
`aliases` | 要新增至新索引的別名。 | 物件 | `myalias` | 否。必須是別名物件的陣列。
`switch_aliases` | 若為 `true`，則將別名從來源索引複製到目標索引。如果與 `aliases` 欄位中的別名發生名稱衝突，則使用 `aliases` 欄位中的別名取代該名稱。 | 布林值 | `true` | 否。預設隱含值為 `false`，表示預設不會複製任何別名。
`force_unsafe` | 若為 `true`，即使索引沒有副本也會進行縮減。 | 布林值 | `false` | 否

如果您想在此操作中加入 `aliases`，該參數必須包含[別名物件]({{site.url}}{{site.baseurl}}/api-reference/alias/)的陣列，如下列範例所示：

```json
"aliases": [
  {
    "my-alias": {}
  },
  {
    "my-second-alias": {
      "is_write_index": false,
      "filter": {
        "multi_match": {
          "query": "QUEEN",
          "fields": ["speaker", "text_entry"]
        }
      },
      "index_routing" : "1",
      "search_routing" : "1"
    }
  }
]
```
{% include copy.html %}

## 關閉

關閉受管理的索引。

`close` 操作不接受任何參數：

```json
{
  "close": {}
}
```
{% include copy.html %}

已關閉的索引仍會保留在磁碟上，但不會耗用 CPU 或記憶體。您無法從已關閉的索引讀取、寫入或搜尋。

如果您需要保留資料的時間比需要主動搜尋它的時間更長，而且資料節點上有足夠的磁碟空間，關閉索引是不錯的選擇。如果您需要再次搜尋資料，重新開啟已關閉的索引比從快照還原索引更簡單。

## 開啟

開啟受管理的索引。

`open` 操作不接受任何參數：

```json
{
  "open": {}
}
```
{% include copy.html %}

## 刪除

刪除受管理的索引。

`delete` 操作不接受任何參數：

```json
{
  "delete": {}
}
```
{% include copy.html %}

## 輪替

當受管理的索引符合其中一個輪替條件時，將別名輪替至新索引。

<p id="important-note"></p>

> **重要**
>
>ISM 會根據**設定的間隔**，在**每次執行原則**時檢查操作的條件，_而非_持續檢查。如果在**執行檢查時**值**已達到**或_已超過_設定的限制，就會執行輪替。例如，當 `min_size` 設定為 100 GiB 時，ISM 可能在索引為 99 GiB 時檢查，而不執行輪替。不過，如果索引在下次檢查時已超過限制（例如達到 105 GiB），就會執行該操作。
{: .important}

如果您需要略過輪替動作，可以將索引設定 `index.plugins.index_state_management.rollover_skip` 設為 `true`。例如，如果您收到「Missing alias or not the write index...」錯誤訊息，可以將 `index.plugins.index_state_management.rollover_skip` 參數設為 `true` 並重試，以略過輪替動作。

索引格式必須符合模式：`^.*-\d+$`。例如，`(logs-000001)`。
將 `index.plugins.index_state_management.rollover_alias` 設為要輪替的別名。

`rollover` 操作具有下列參數，全部都是選用的。

參數 | 說明 | 類型 | 範例
:--- | :--- |:--- |:---
`min_size` | 輪替索引所需的主要分片儲存空間總大小下限（不含副本）。例如，如果您將 `min_size` 設為 100 GiB，而您的索引有 5 個主要分片和 5 個副本分片，每個為 20 GiB，則所有主要分片的總大小為 100 GiB，因此會執行輪替。請參閱[**重要**注意](#important-note)。 | 字串 | `20gb` 或 `5mb`
`min_primary_shard_size` | 輪替索引所需的**單一主要分片**儲存空間大小下限。例如，如果您將 `min_primary_shard_size` 設為 30 GiB，而索引中**其中一個**主要分片的大小大於該條件，就會執行輪替。請參閱[**重要**注意](#important-note)。 | 字串 | `20gb` 或 `5mb`
`min_doc_count` |  輪替索引所需的文件數下限。請參閱[**重要**注意](#important-note)。 | 整數 | `2000000`
`min_index_age` |  輪替索引所需的存留時間下限。索引存留時間是指從建立到現在的時間。支援的單位為 `d`（天）、`h`（小時）、`m`（分鐘）、`s`（秒）、`ms`（毫秒）和 `micros`（微秒）。請參閱[**重要**注意](#important-note)。 | 字串 | `5d` 或 `7h`
`copy_alias` | 控制是否將目前索引的所有別名複製到新建立的索引。預設為 `false`。  | 布林值 | `true` 或 `false`
`prevent_empty_rollover` | 控制當索引不含任何文件時是否略過輪替。當 `true` 時，空索引不會輪替。預設為 `false`。 | 布林值 | `true` 或 `false`
`any_of` | 條件群組的清單。每個群組是一個物件，包含 `min_size`、`min_primary_shard_size`、`min_doc_count` 和 `min_index_age` 其中一或多項。在群組內，條件會以 AND 合併；群組之間則以 OR 合併。與直接設定在 `rollover` 物件上的條件互斥。同時指定兩者、空清單或空群組都會傳回錯誤。 | 陣列 | `[{"min_index_age": "7d"}]`

直接設定在 `rollover` 物件上的條件會以邏輯 OR 合併，因此只要符合其中一個條件就會執行輪替。下列輪替動作會在索引存留時間至少 7 天或大小至少 50 GiB 時輪替索引：

```json
{
  "rollover": {
    "min_index_age": "7d",
    "min_size": "50gb"
  }
}
```
{% include copy.html %}

若要要求必須同時符合多個條件，請使用 `any_of`。此參數接受條件群組的清單。群組內的條件會以 AND 合併，群組之間則以 OR 合併，因此只要至少一個群組中的每個條件都符合，就會執行輪替。 

下列輪替動作會在索引存留時間至少 7 天且大小至少 50 GiB 時，或在達到 100,000,000 份文件時輪替索引：

```json
{
  "rollover": {
    "any_of": [
      {
        "min_index_age": "7d",
        "min_size": "50gb"
      },
      {
        "min_doc_count": 100000000
      }
    ]
  }
}
```
{% include copy.html %}

在混合版本的叢集中，每個節點都必須執行 OpenSearch 3.7 或更新版本，才能評估分組條件。執行較舊版本的節點不會處理 `any_of`。
{: .note}

## 通知

傳送通知給您。

參數 | 說明 | 類型 | 必要
:--- | :--- |:--- |:--- |
`destination` | 目的地 URL。 | Slack、Amazon Chime 或 webhook URL | 是
`message_template` |  訊息文字。您可以使用 [Mustache 範本](https://mustache.github.io/mustache.5.html)將變數新增至訊息。 | 物件 | 是

目的地系統**必須**傳回回應，否則通知操作會擲回錯誤。

### 範例 1：Chime 通知

下列通知操作會將訊息傳送至 Amazon Chime webhook：

```json
{
  "notification": {
    "destination": {
      "chime": {
        "url": "<url>"
      }
    },
    "message_template": {
      "source": "the index is {% raw %}{{ctx.index}}{% endraw %}"
    }
  }
}
```
{% include copy.html %}

### 範例 2：自訂 webhook 通知

下列通知操作會將訊息傳送至自訂 webhook：

```json
{
  "notification": {
    "destination": {
      "custom_webhook": {
        "url": "https://<your_webhook>"
      }
    },
    "message_template": {
      "source": "the index is {% raw %}{{ctx.index}}{% endraw %}"
    }
  }
}
```
{% include copy.html %}

### 範例 3：Slack 通知

下列通知操作會將訊息傳送至 Slack webhook：

```json
{
  "notification": {
    "destination": {
      "slack": {
        "url": "https://hooks.slack.com/services/xxx/xxxxxx"
      }
    },
    "message_template": {
      "source": "the index is {% raw %}{{ctx.index}}{% endraw %}"
    }
  }
}
```
{% include copy.html %}

您可以在訊息中使用 `ctx` 變數，根據原則過去的執行情形來代表多個原則參數。例如，如果您的原則有輪替動作，您可以在訊息中使用 `{% raw %}{{ctx.action.name}}{% endraw %}` 來代表輪替的名稱。

下列 `ctx` 變數選項適用於每個原則：

### 保證可用的變數

參數 | 說明 | 類型
:--- | :--- |:--- |:--- |
`index` | 索引的名稱。 | 字串
`index_uuid` | 索引的 UUID。 | 字串
`policy_id` | 政策的名稱。 | 字串

## 快照

備份叢集的索引與狀態。如需快照的詳細資訊，請參閱 [建立及還原快照]({{site.url}}{{site.baseurl}}/opensearch/snapshots/snapshot-restore/)。

`snapshot` 操作具有下列參數。

參數 | 說明 | 類型 | 必要 | 預設
:--- | :--- |:--- |:--- |
`repository` | 您透過原生快照 API 操作註冊的儲存庫名稱。 | 字串 | 是 | -
`snapshot` | 快照的名稱。接受字串以及 Mustache 變數 `{% raw %}{{ctx.index}}{% endraw %}` 和 `{% raw %}{{ctx.indexUuid}}{% endraw %}`。如果 Mustache 變數無效，快照名稱會預設為索引的名稱。 | 字串或 Mustache 範本 | 是 | -

以下範例會在 `my_backup` 儲存庫中為索引建立快照，並使用索引 UUID 為快照命名：

```json
{
  "snapshot": {
    "repository": "my_backup",
    "snapshot": "{% raw %}{{ctx.indexUuid}}{% endraw %}"
  }
}
```
{% include copy.html %}

## 將索引轉換為遠端索引

透過從遠端快照儲存庫還原，將現有索引轉換為可搜尋快照。此動作會將不常存取的資料移至遠端儲存空間，同時保持其可搜尋，藉此降低儲存成本。將 `delete_original_index` 設定為 `true`，即可在還原請求被接受後移除原始索引，只留下以遠端快照為基礎的索引。

`convert_index_to_remote` 操作具有下列參數。

參數 | 說明 | 類型 | 必要 | 預設
:--- | :--- |:--- |:--- |
`repository` | 透過原生快照 API 操作註冊的儲存庫名稱。必須是遠端儲存庫（例如 S3、Azure 或 GCS）。 | 字串 | 是 | N/A
`snapshot` | 由快照動作建立的快照名稱。 | 字串 | 是 | N/A
`include_aliases` | 還原操作期間是否包含索引別名。若為 `true`，與原始索引關聯的所有別名都會隨遠端索引一併還原。如果您的應用程式透過別名存取索引，請將此參數設定為 `true`。 | 布林值 | 否 | `false`
`ignore_index_settings` | 還原操作期間要忽略的索引設定清單，以逗號分隔。例如 `index.refresh_interval,index.number_of_replicas`。當您想為還原後的遠端索引套用與原始索引不同的設定時，此參數非常實用。 | 字串 | 否 | 空字串
`number_of_replicas` | 為還原後的遠端索引設定的副本數量。這讓您能在轉換過程中控制副本分配，而不需要另外執行更新操作。在轉換期間設定 `number_of_replicas` 有助於防止叢集進入黃色狀態，或在副本分配期間產生不必要的負載。 | 整數 | 否 | `0`
`rename_pattern` | 還原後的可搜尋快照索引的命名模式。使用 `$1` 作為原始索引名稱的預留位置。例如，`remote_$1` 會將 `my-index` 重新命名為 `remote_my-index`。 | 字串 | 否 | `$1_remote`
`delete_original_index` | 是否在還原請求被接受後刪除原始索引。 | 布林值 | 否 | `false`

### 必要條件

使用 `convert_index_to_remote` 動作之前，請確認下列事項：

- 已註冊遠端儲存庫（S3、Azure 或 GCS）且可存取。
- 指定儲存庫中存在索引的快照，通常是以 `snapshot` 動作建立。
- 儲存庫名稱與快照動作中使用的名稱相符。

### 使用注意事項

將索引還原為可搜尋快照時，請注意下列事項，以確保轉換順利且可預期：

- 只有當您將 `delete_original_index` 設定為 `true` 時，原始索引才會在遠端快照還原成功被接受後刪除。預設情況下，原始索引會與可搜尋快照版本並存。
- `convert_index_to_remote` 操作中使用的儲存庫名稱必須與快照動作中指定的儲存庫名稱相符。
- `actions` 陣列中的每個物件都包含一個動作。將 `snapshot` 和 `convert_index_to_remote` 放在同一個物件中雖然會被接受，但只會儲存其中一個，因此永遠不會建立快照。請將每個動作列在各自的物件中。
- 您可以使用 `{% raw %}{{ctx.index}}{% endraw %}` 或 `{% raw %}{{ctx.indexUuid}}{% endraw %}` 等 Mustache 變數來參照快照，以進行動態命名。
- 設定 `number_of_replicas` 時，請考量叢集的容量。如果沒有足夠的合格節點可供副本還原，叢集可能會進入黃色狀態。

### 基本範例

以下範例示範使用最少必要參數的基本轉換。`snapshot` 動作會建立快照，然後由 `convert_index_to_remote` 還原，因此兩者各自是 `actions` 陣列中的獨立物件：

```json
"actions": [
  {
    "snapshot": {
      "repository": "my_backup",
      "snapshot": "{% raw %}{{ctx.index}}{% endraw %}"
    }
  },
  {
    "convert_index_to_remote": {
      "repository": "my_backup",
      "snapshot": "{% raw %}{{ctx.index}}{% endraw %}"
    }
  }
]
```
{% include copy.html %}

### 進階組態範例

以下範例示範使用所有可用的組態選項。此組態包含別名、在還原期間忽略某些索引設定，並為可搜尋快照設定兩個副本：

```json
{
   "convert_index_to_remote": {
      "repository": "my_backup",
      "snapshot": "daily-snapshot",
      "include_aliases": true,
      "ignore_index_settings": "index.refresh_interval,index.number_of_replicas",
      "number_of_replicas": 0,
      "rename_pattern": "remote_$1"
   }
}
```
{% include copy.html %}

### 完整政策範例

以下政策會將超過 30 天的索引移至可搜尋快照，並使用針對成本效益最佳化的設定：

```json
{
  "policy": {
    "description": "Convert old indexes to searchable snapshots",
    "default_state": "active",
    "states": [
      {
        "name": "active",
        "actions": [],
        "transitions": [
          {
            "state_name": "archive",
            "conditions": {
              "min_index_age": "30d"
            }
          }
        ]
      },
      {
        "name": "archive",
        "actions": [
          {
            "snapshot": {
              "repository": "remote-repo",
              "snapshot": "{% raw %}{{ctx.index}}{% endraw %}"
            }
          },
          {
            "convert_index_to_remote": {
              "repository": "remote-repo",
              "snapshot": "{% raw %}{{ctx.index}}{% endraw %}",
              "include_aliases": true,
              "ignore_index_settings": "index.refresh_interval,index.number_of_replicas",
              "number_of_replicas": 0
            }
          }
        ],
        "transitions": []
      }
    ]
  }
}
```
{% include copy.html %}

## 索引優先順序

設定索引在特定狀態下的優先順序。索引未分配的分片會盡可能依其優先順序復原。優先順序值較高的索引會先復原，接著才是優先順序值較低的索引。

`index_priority` 操作具有下列參數。

參數 | 說明 | 類型 | 必要 | 預設
:--- | :--- |:--- |:--- |:---
`priority` | 索引進入狀態時的優先順序。 | 整數 | 是 | 1

以下範例將索引優先順序設定為 `50`：

```json
"actions": [
  {
    "index_priority": {
      "priority": 50
    }
  }
]
```
{% include copy.html %}

## 配置

將索引配置到具有特定屬性設定的節點，[如本例所示]({{site.url}}{{site.baseurl}}/opensearch/cluster/#advanced-step-7-set-up-a-hot-warm-architecture)。
例如，將 `require` 設為 `warm`，只會將您的資料移至「warm」節點。

`allocation` 操作具有下列參數。必須至少指定 `require`、`include` 或 `exclude` 其中之一。

參數 | 說明 | 類型 | 必要
:--- | :--- |:--- |:---
`require` | 將索引配置到具有指定屬性的節點。 | 物件 | 否
`include` | 將索引配置到具有任一指定屬性的節點。 | 物件 | 否
`exclude` | 不將索引配置到具有任一指定屬性的節點。 | 物件 | 否
`wait_for` | 等待政策執行後，再將索引配置到具有指定屬性的節點。 | 布林值 | 否。預設為 `false`。

下列範例會將索引配置到 `temp` 屬性設為 `warm` 的節點：

```json
"actions": [
  {
    "allocation": {
      "require": { "temp": "warm" }
    }
  }
]
```
{% include copy.html %}

## 彙整

[索引彙整]({{site.url}}{{site.baseurl}}/im-plugin/index-rollups/index/)可讓您定期將舊資料彙整為摘要索引，以降低資料的細緻程度。在 `ism_rollup` 物件中定義作業。如需其接受的欄位，請參閱[建立或更新索引彙整作業]({{site.url}}{{site.baseurl}}/im-plugin/index-rollups/rollup-api/#create-or-update-an-index-rollup-job)。

彙整作業可以是持續性或非持續性作業。使用 ISM 政策建立的彙整作業只能是非持續性作業。
{: .note }

下列政策會將 `opensearch_dashboards_sample_data_ecommerce` 欄位彙整為 `target` 索引中每小時一個的桶：

```json
PUT _plugins/_ism/policies/sample_rollup_policy
{
    "policy": {
        "description": "Sample rollup" ,
        "default_state": "rollup",
        "states": [
            {
                "name": "rollup",
                "actions": [
                    {
                        "rollup": {
                            "ism_rollup": {
                                "description": "Creating rollup through ISM",
                                "target_index": "target",
                                "target_index_settings":{
                                    "index.number_of_shards": 1,
                                    "index.number_of_replicas": 1,
                                    "index.codec": "best_compression"
                                 },
                                "page_size": 1000,
                                "dimensions": [
                                    {
                                        "date_histogram": {
                                            "fixed_interval": "60m",
                                            "source_field": "order_date",
                                            "target_field": "order_date",
                                            "timezone": "America/Los_Angeles"
                                        }
                                    },
                                    {
                                        "terms": {
                                            "source_field": "customer_gender",
                                            "target_field": "customer_gender"
                                        }
                                    },
                                    {
                                        "terms": {
                                            "source_field": "day_of_week",
                                            "target_field": "day_of_week"
                                        }
                                    }
                                ],
                                "metrics": [
                                    {
                                        "source_field": "taxless_total_price",
                                        "metrics": [
                                            {
                                                "sum": {}
                                            }
                                        ]
                                    },
                                    {
                                        "source_field": "total_quantity",
                                        "metrics": [
                                            {
                                                "avg": {}
                                            },
                                            {
                                                "max": {}
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                ],
                "transitions": []
            }
        ]
    }
}
```
{% include copy-curl.html %}

若要在 OpenSearch Dashboards 中建立彙整作業，請參閱[建立彙整作業]({{site.url}}{{site.baseurl}}/im-plugin/index-rollups/index/#creating-a-rollup-job)。

## 停止複寫

停止複寫，並將追隨者索引轉換為一般索引。

`stop_replication` 操作不接受任何參數：

```json
{
  "stop_replication": {}
}
```
{% include copy.html %}

啟用跨叢集複寫時，追隨者索引會變成唯讀，阻止所有寫入操作。若要管理追隨者叢集上的複寫索引，您可以先執行 `stop_replication` 動作，再執行其他寫入操作。例如，您可以定義一個政策，先執行 `stop_replication`，再執行 `delete` 動作來刪除索引。

如果已啟用安全性，除了[停止複寫權限]({{site.url}}{{site.baseurl}}/tuning-your-cluster/replication-plugin/permissions/#replication-permissions)之外，您還必須具有 `indices:internal/plugins/replication/index/stop` 權限，才能使用 `stop_replication` 動作。
{: .note}

## 僅供搜尋

當索引進入 `search_only` 模式時，OpenSearch 會移除其主要分片和一般副本分片，同時保留搜尋副本供查詢操作使用。對該索引的所有寫入操作都會遭到封鎖。這適用於記錄檔生命週期管理，因為較舊的索引不再需要寫入功能，但仍應可供搜尋。

> 此動作必須符合下列先決條件：
> - 叢集必須啟用遠端儲存。
> - 索引必須啟用分段複寫。
> - 索引必須設定搜尋副本。
>
> 如需僅供搜尋模式及讀取器與寫入器分離的詳細資訊，請參閱[分離索引編製與搜尋工作負載]({{site.url}}{{site.baseurl}}/tuning-your-cluster/separate-index-and-search-workloads/)。
{: .note}

使用下列動作將索引設為僅供搜尋模式：

```json
{
  "search_only": {}
}
```
{% include copy.html %}

如果索引已處於僅供搜尋模式，此動作會成功完成，且不會進行任何變更。

您可以呼叫 [Scale API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/scale/)，在 ISM 政策之外手動啟用或停用 `search_only` 模式。
{: .tip}

下列範例政策會在 7 天後將索引轉換為 `search_only` 模式：

```json
PUT _plugins/_ism/policies/hot-warm-search-only
{
  "policy": {
    "description": "Move indexes to search-only mode after 7 days",
    "default_state": "hot",
    "states": [
      {
        "name": "hot",
        "actions": [],
        "transitions": [
          {
            "state_name": "warm",
            "conditions": {
              "min_index_age": "7d"
            }
          }
        ]
      },
      {
        "name": "warm",
        "actions": [
          {
            "search_only": {}
          }
        ],
        "transitions": []
      }
    ]
  }
}
```
{% include copy-curl.html %}
