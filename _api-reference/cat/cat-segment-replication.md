---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "CAT 區段複寫"
parent: CAT APIs
nav_order: 53
has_children: false
---

# CAT Segment Replication API
**於 2.7 版引入**
{: .label .label-purple }

CAT 區段複寫操作會傳回每個副本分片上進行中及最近完成的[區段複寫]({{site.url}}{{site.baseurl}}/opensearch/segment-replication/index/)事件資訊，包括相關的分片層級指標。這些指標可顯示副本落後主要分片的程度。

請僅對已啟用區段複寫的索引呼叫 CAT Segment Replication API。
{: .note}

<!-- spec_insert_start
api: cat.segment_replication
component: endpoints
-->
## 端點
```json
GET /_cat/segment_replication
GET /_cat/segment_replication/{index}
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: cat.segment_replication
component: path_parameters
columns: Parameter, Data type, Description
include_deprecated: false
-->
## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `index` | List | 以逗號分隔的資料串流、索引和別名清單，用於限制請求範圍。支援萬用字元（`*`）。若要以所有資料串流和索引為目標，請省略此參數，或使用 `*` 或 `_all`。 |

<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.segment_replication
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設值 |
| :--- | :--- | :--- | :--- |
| `active_only` | Boolean | 若為 `true`，回應僅包含進行中的區段複寫事件。 | `false` |
| `allow_no_indices` | Boolean | 當萬用字元索引運算式未解析出任何具體索引時，是否忽略該索引。這包括 `_all` 字串或未指定任何索引的情況。 | N/A |
| `bytes` | String | 用於顯示位元組值的單位。<br> 有效值為：`b`、`kb`、`k`、`mb`、`m`、`gb`、`g`、`tb`、`t`、`pb` 和 `p`。 | N/A |
| `completed_only` | Boolean | 若為 `true`，回應僅包含最近完成的區段複寫事件。 | `false` |
| `detailed` | Boolean | 若為 `true`，回應會包含區段複寫事件各階段的額外指標。 | `false` |
| `expand_wildcards` | List or String | 指定萬用字元運算式可比對的索引類型。支援以逗號分隔的值。<br> 有效值為：<br> - `all`：比對任何索引，包括隱藏索引。<br> - `closed`：比對已關閉的非隱藏索引。<br> - `hidden`：比對隱藏索引。必須與 `open`、`closed` 或兩者搭配使用。<br> - `none`：不接受萬用字元運算式。<br> - `open`：比對開啟的非隱藏索引。 | N/A |
| `format` | String | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | List | 以逗號分隔的要顯示的欄名清單。 | N/A |
| `help` | Boolean | 傳回說明資訊。 | `false` |
| `ignore_throttled` | Boolean | 指定的具體、展開或別名索引在受到節流時是否應予以忽略。 | N/A |
| `ignore_unavailable` | Boolean | 指定的具體索引在遺失或已關閉時是否應予以忽略。 | N/A |
| `index` | List | 以逗號分隔的資料串流、索引和別名清單，用於限制請求範圍。支援萬用字元（`*`）。若要以所有資料串流和索引為目標，請省略此參數，或使用 `*` 或 `_all`。 | N/A |
| `s` | List | 以逗號分隔的用於排序的欄名或欄別名清單。 | N/A |
| `shards` | List | 以逗號分隔的要顯示的分片清單。 | N/A |
| `time` | String | 指定時間單位，例如 `5d` 或 `7h`。如需更多資訊，請參閱[支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。<br> 有效值為：`nanos`、`micros`、`ms`、`s`、`m`、`h` 和 `d`。 | N/A |
| `timeout` | String | 操作逾時時間。 | N/A |
| `v` | Boolean | 啟用詳細模式，此模式會顯示欄標題。 | `false` |

<!-- spec_insert_end -->

## 路徑參數

參數 | 類型 | 說明
:--- | :--- | :---
`index` | String | 索引名稱，或用於篩選結果的以逗號分隔的索引名稱清單或萬用字元運算式。若未提供此參數，回應會包含叢集中所有索引的資訊。

## 查詢參數

參數 | 資料類型  | 說明
:--- |:-----------| :---
`active_only` | Boolean    | 若為 `true`，回應僅包含進行中的區段複寫。預設為 `false`。
[`detailed`](#additional-detailed-response-metrics) | String     | 若為 `true`，回應會包含區段複寫事件各階段的額外指標。預設為 `false`。
`shards` | String     | 以逗號分隔的要顯示的分片清單。
`bytes` | 位元組單位 | 用於顯示位元組大小值的[單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。
`format` | String     | HTTP accept 標頭的簡短版本。有效值包括 `JSON` 和 `YAML`。
`h` | String     | 以逗號分隔的要顯示的欄名清單。
`help` | Boolean    | 若為 `true`，回應會包含說明資訊。預設為 `false`。
`time` | 時間單位 | 用於顯示時間值的[單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。
`v` | Boolean    | 若為 `true`，回應會包含欄標題。預設為 `false`。
`s` | String     | 指定結果的排序方式。例如，`s=shardId:desc` 會依 shardId 遞減排序。

## 請求範例
<!-- spec_insert_start
component: example_code
rest: GET /_cat/segment_replication?v&s=s:desc
-->
{% capture step1_rest %}
GET /_cat/segment_replication?v&s=s:desc
{% endcapture %}

{% capture step1_python %}


response = client.cat.segment_replication(
  params = { "v": "true", "s": "s:desc" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

下列範例說明各種區段複寫回應。

### 沒有進行中的區段複寫事件

下列查詢會請求所有索引的區段複寫指標，並包含欄標題：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/segment_replication?v=true
-->
{% capture step1_rest %}
GET /_cat/segment_replication?v=true
{% endcapture %}

{% capture step1_python %}


response = client.cat.segment_replication(
  params = { "v": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應包含上述請求的指標：

```bash
shardId target_node target_host checkpoints_behind bytes_behind current_lag last_completed_lag rejected_requests
[index-1][0] runTask-1 127.0.0.1 0 0b 0s 7ms 0
```

###  已指定分片 ID

下列查詢會請求索引 `index1` 和 `index2` 中 ID 為 `0` 的分片的區段複寫指標，並包含欄標題：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/segment_replication/index1,index2?v=true&shards=0
-->
{% capture step1_rest %}
GET /_cat/segment_replication/index1,index2?v=true&shards=0
{% endcapture %}

{% capture step1_python %}


response = client.cat.segment_replication(
  index = "index1,index2",
  params = { "v": "true", "shards": "0" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應包含上述請求的指標。欄標題與指標名稱相對應：

```bash
shardId target_node target_host checkpoints_behind bytes_behind current_lag last_completed_lag rejected_requests
[index-1][0] runTask-1 127.0.0.1 0 0b 0s 3ms 0
[index-2][0] runTask-1 127.0.0.1 0 0b 0s 5ms 0
```

###  詳細回應

下列查詢會要求所有索引的詳細區段複寫指標，並附上欄標題：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/segment_replication?v=true&detailed=true
-->
{% capture step1_rest %}
GET /_cat/segment_replication?v=true&detailed=true
{% endcapture %}

{% capture step1_python %}


response = client.cat.segment_replication(
  params = { "v": "true", "detailed": "true" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應包含區段複寫事件的檔案與階段的其他指標：

```bash
shardId target_node target_host checkpoints_behind bytes_behind current_lag last_completed_lag rejected_requests stage time files_fetched files_percent bytes_fetched bytes_percent start_time stop_time files files_total bytes bytes_total replicating_stage_time_taken get_checkpoint_info_stage_time_taken file_diff_stage_time_taken get_files_stage_time_taken finalize_replication_stage_time_taken
[index-1][0] runTask-1 127.0.0.1 0 0b 0s 3ms 0 done 10ms 6 100.0% 4753 100.0% 2023-03-16T13:46:16.802Z 2023-03-16T13:46:16.812Z 6 6 4.6kb 4.6kb 0s 2ms 0s 3ms 3ms
[index-2][0] runTask-1 127.0.0.1 0 0b 0s 5ms 0 done 7ms 3 100.0% 3664 100.0% 2023-03-16T13:53:33.466Z 2023-03-16T13:53:33.474Z 3 3 3.5kb 3.5kb 0s 1ms 0s 2ms 2ms
```

###  排序結果

下列查詢會要求所有索引的區段複寫指標，並附上欄標題，依分片 ID 遞減排序：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/segment_replication?v&s=shardId:desc
-->
{% capture step1_rest %}
GET /_cat/segment_replication?v&s=shardId:desc
{% endcapture %}

{% capture step1_python %}


response = client.cat.segment_replication(
  params = { "v": "true", "s": "shardId:desc" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應包含排序後的結果：

```bash
shardId    target_node  target_host checkpoints_behind bytes_behind current_lag last_completed_lag rejected_requests
[test6][1] runTask-2   127.0.0.1   0                  0b           0s          5ms                0
[test6][0] runTask-2   127.0.0.1   0                  0b           0s          4ms                0
```

### 使用指標別名 

在請求中，您可以使用指標的完整名稱或其任一別名。下列查詢與前一個查詢相同，但使用別名 `s` 而非 `shardID` 來排序：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/segment_replication?v&s=s:desc
-->
{% capture step1_rest %}
GET /_cat/segment_replication?v&s=s:desc
{% endcapture %}

{% capture step1_python %}


response = client.cat.segment_replication(
  params = { "v": "true", "s": "s:desc" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應指標

下表列出所有請求都會傳回的回應指標。在查詢參數中參照指標時，您可以提供指標的完整名稱或其任一別名，如先前的[範例](#using-a-metric-alias)所示。

指標 | 別名 | 說明
:--- | :--- | :---
`shardId` | `s` | 特定分片的 ID。
`target_host` | `thost` | 目標主機 IP 位址。
`target_node` | `tnode` | 目標節點名稱。
`checkpoints_behind` | `cpb` | 副本分片落後主要分片的檢查點數量。
`bytes_behind` | `bb` | 副本分片落後主要分片的位元組數。
`current_lag` | `clag` | 等待副本分片追上主要分片所經過的時間。
`last_completed_lag` | `lcl` | 副本分片追上最新主要分片重新整理所花費的時間。
`rejected_requests` | `rr` | 複寫群組被拒絕的請求數。

### 其他詳細回應指標

下表列出當 `detailed` 設為 `true` 時所傳回的其他回應欄位。

指標 | 別名 | 說明
:--- |:--- |:---
`stage` | `st` | 區段複寫事件的目前階段。
`time` | `t`, `ti` | 區段複寫事件完成所花費的時間，以毫秒為單位。
`files_fetched` | `ff` | 區段複寫事件迄今已擷取的檔案數。
`files_percent` | `fp` | 區段複寫事件迄今已擷取檔案的百分比。
`bytes_fetched` | `bf` | 區段複寫事件迄今已擷取的位元組數。
`bytes_percent` | `bp` | 區段複寫事件迄今已擷取的位元組數百分比。
`start_time` | `start` | 區段複寫開始時間。
`stop_time` | `stop` | 區段複寫停止時間。
`files` | `f` | 區段複寫事件需要擷取的檔案數。
`files_total` | `tf` | 屬於此復原的檔案總數，包含重複使用與已復原的檔案。
`bytes` | `b` | 區段複寫事件需要擷取的位元組數。
`bytes_total` | `tb` | 分片中的位元組總數。
`replicating_stage_time_taken` | `rstt` | 區段複寫事件的 `replicating` 階段完成所花費的時間。 
`get_checkpoint_info_stage_time_taken` | `gcistt` | 區段複寫事件的 `get checkpoint info` 階段完成所花費的時間。 
`file_diff_stage_time_taken` | `fdstt` | 區段複寫事件的 `file diff` 階段完成所花費的時間。 
`get_files_stage_time_taken` | `gfstt` | 區段複寫事件的 `get files` 階段完成所花費的時間。 
`finalize_replication_stage_time_taken` | `frstt` | 區段複寫事件的 `finalize replication` 階段完成所花費的時間。
