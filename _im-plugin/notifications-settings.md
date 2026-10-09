---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "長時間執行作業通知"
nav_order: 70
redirect_from:
  - /im-plugin/notifications/
  - /dashboards/im-dashboards/notifications/
  - /dashboards/admin-ui-index/notifications/
---

# 長時間執行作業通知

**於 2.8 版推出**
{: .label .label-purple }

重新索引、調整大小、強制合併及開啟作業可能需要執行數分鐘或數小時。當您傳送其中一個請求並將 `wait_for_completion` 設為 `false` 時，它會立即傳回任務 ID，而不會持續等待作業完成。針對該任務 ID 或作業類型設定通知，即可在工作完成或失敗時收到通知，而不必輪詢。

通知會透過 [Notifications]({{site.url}}{{site.baseurl}}/observing-your-data/notifications/index/) 應用程式中設定的管道傳送，該應用程式支援 Amazon Chime、Amazon Simple Notification Service (Amazon SNS)、Amazon Simple Email Service (Amazon SES)、透過 SMTP 傳送的電子郵件、Slack 及自訂 Webhook。

## 設定通知設定

`lron_config` 物件接受 `task_id` 或 `action_name`，而您的選擇會決定該設定的存續時間：

- 提供 `task_id` 以建立一次性設定。當任務結束時，它會自動刪除。如果您同時提供 `task_id` 和 `action_name`，則會忽略 `action_name`，不過它有助於您搜尋及偵錯您的通知設定。
- 提供 `action_name` 而不提供 `task_id`，以建立適用於該類型每個作業的全域持續性設定。

下表列出長時間執行索引作業通知的參數。

| 參數 | 類型 | 說明 |
| :--- | :--- | :--- |
| `lron_config` | 物件 | 長時間執行索引作業通知組態。 |
| `task_id` | 字串 | 您要收到通知的任務其任務 ID。選用。必須指定 `task_id` 和 `action_name` 其中之一。|
| `action_name` | 字串 | 您要收到通知的作業類型。提供 `action_name` 而不提供 `task_id`，以收到此類型所有作業的通知。支援的值為 `indices:data/write/reindex`、`indices:admin/resize`、`indices:admin/forcemerge` 及 `indices:admin/open`。選用。必須指定 `task_id` 和 `action_name` 其中之一。 |
| `lron_condition` | 物件 | 指定您要收到通知的事件。選用。若未提供，您會同時收到作業成功與失敗的通知。 |
| `lron_condition.success` | 布林值 | 將此參數設為 `true`，以在作業成功時收到通知。選用。預設為 `true`。 |
| `lron_condition.failure` | 布林值 | 將此參數設為 `true`，以在作業失敗或逾時時收到通知。選用。預設為 `true`。 |
| `channels` | 物件 | 支援的通訊管道包括 Amazon Chime、Amazon Simple Notification Service (Amazon SNS)、Amazon Simple Email Service (Amazon SES)、透過 SMTP 傳送的電子郵件、Slack 及自訂 Webhook。如果 `lron_condition.success` 或 `lron_condition.failure` 為 `true`，則 `channels` 必須包含至少一個管道。請在 [Notifications]({{site.url}}{{site.baseurl}}/observing-your-data/notifications/index/) 中瞭解如何設定通知管道。 |

### 建立通知設定

下列範例請求會為每個失敗的重新索引作業設定通知：

```json
POST /_plugins/_im/lron
{
  "lron_config": {
    "action_name": "indices:data/write/reindex",
    "lron_condition": {
      "success": false,
      "failure": true
    },
    "channels": [
      {
        "id": "my_chime"
      }
    ]
  }
}
```
{% include copy-curl.html %}

回應包含新通知設定的 ID：

```json
{
  "_id": "LRON:indices:data/write/reindex",
  "lron_config": {
    "lron_condition": {
      "success": false,
      "failure": true
    },
    "action_name": "indices:data/write/reindex",
    "channels": [
      {
        "id": "my_chime"
      }
    ]
  }
}
```

若要收到單一作業的通知，而非某類型所有作業的通知，請提供其任務 ID。傳送作業時將 `wait_for_completion` 設為 `false`，使其傳回任務 ID，而不會持續等待作業完成。

下列請求會將文件編製索引，這會建立重新索引作業所讀取的來源索引：

```json
POST /my-source-index/_doc?refresh=true
{
  "message": "test document"
}
```
{% include copy-curl.html %}

下列請求會重新索引該索引並傳回任務 ID：

```json
POST /_reindex?wait_for_completion=false
{
  "source": {
    "index": "my-source-index"
  },
  "dest": {
    "index": "my-dest-index"
  }
}
```
{% include copy-curl.html %}

然後在 `task_id` 中提供傳回的任務 ID：

```json
POST /_plugins/_im/lron
{
  "lron_config": {
    "task_id": "<task_id>",
    "lron_condition": {
      "success": false,
      "failure": true
    },
    "channels": [
      {
        "id": "my_chime"
      }
    ]
  }
}
```
{% include copy-curl.html %}

任務 ID 必須屬於叢集中的節點。來自其他叢集的任務 ID，或您自行虛構的任務 ID，會遭到拒絕並傳回 `400`。
{: .note}

### 通知設定 ID

回應會在 `_id` 欄位中傳回通知設定的 ID。您可以使用此 ID 來讀取、更新或刪除此通知設定。對於全域 `lron_config`，ID 的格式為 `LRON:<action_name>` (例如 `LRON:indices:data/write/reindex`)。

`action_name` 可能包含斜線字元 (`/`)，如果您在 Dev Tools 主控台中使用它，必須將其 HTTP 編碼為 `%2F`。例如，`LRON:indices:data/write/reindex` 會變成 `LRON:indices:data%2Fwrite%2Freindex`。
{: .important}

對於任務 `lron_config`，ID 的格式為 `LRON:<task ID>`。

## 擷取通知設定

下列範例會擷取目前設定的通知設定。

使用下列請求來擷取具有指定 [通知設定 ID](#notification-setting-id) 的通知設定：

```json
 GET /_plugins/_im/lron/{lronID}
```
{% include copy-curl.html %}

例如，下列請求會擷取 `reindex` 作業的通知設定：

```json
GET /_plugins/_im/lron/LRON:indices:data%2Fwrite%2Freindex
```
{% include copy-curl.html %}

回應包含該設定：

```json
{
  "lron_configs": [
    {
      "_id": "LRON:indices:data/write/reindex",
      "lron_config": {
        "lron_condition": {
          "success": false,
          "failure": true
        },
        "action_name": "indices:data/write/reindex",
        "channels": [
          {
            "id": "my_chime"
          }
        ]
      }
    }
  ],
  "total_number": 1
}
```

使用下列請求來擷取所有通知設定：

```json
GET /_plugins/_im/lron
```
{% include copy-curl.html %}

回應包含所有已設定通知設定及其 ID：

```json
{
  "lron_configs": [
    {
      "_id": "LRON:indices:admin/open",
      "lron_config": {
        "lron_condition": {
          "success": false,
          "failure": false
        },
        "action_name": "indices:admin/open",
        "channels": []
      }
    },
    {
      "_id": "LRON:indices:data/write/reindex",
      "lron_config": {
        "lron_condition": {
          "success": false,
          "failure": true
        },
        "action_name": "indices:data/write/reindex",
        "channels": [
          {
            "id": "my_chime"
          }
        ]
      }
    }
  ],
  "total_number": 2
}
```

## 更新通知設定

下列範例會修改具有指定 [通知設定 ID](#notification-setting-id) 的現有通知設定：

```json
PUT /_plugins/_im/lron/LRON:indices:data%2Fwrite%2Freindex
{
  "lron_config": {
    "action_name": "indices:data/write/reindex",
    "lron_condition": {
      "success": true,
      "failure": true
    },
    "channels": [
      {
        "id": "my_chime"
      }
    ]
  }
}
```
{% include copy-curl.html %}

回應包含更新後的設定：

```json
{
  "_id": "LRON:indices:data/write/reindex",
  "lron_config": {
    "lron_condition": {
      "success": true,
      "failure": true
    },
    "action_name": "indices:data/write/reindex",
    "channels": [
      {
        "id": "my_chime"
      }
    ]
  }
}
```

## 刪除通知設定

下列範例會移除具有指定 [通知設定 ID](#notification-setting-id) 的通知設定：

```json
DELETE /_plugins/_im/lron/{lronID}
```
{% include copy-curl.html %}

例如，下列請求會刪除 `reindex` 作業的通知設定：

```json
DELETE _plugins/_im/lron/LRON:indices:data%2Fwrite%2Freindex
```
{% include copy-curl.html %}

## OpenSearch Dashboards 中的通知

若要前往 **Index Management** 頁面，請在上方功能表前往 **Management > Index Management**。選取 **Notification settings** 以設定支援通知之作業的預設值，如下圖所示。

![通知設定頁面]({{site.url}}{{site.baseurl}}/images/admin-ui-index/notification-settings.png)

### 建立通知管道

通知設定至少需要一個可傳送的管道：

1. 在 **Index Management** 中，選取 **Notification settings**，然後選取 **Manage channels**。**Channels** 頁面會在不同的視窗中開啟。
1. 選取 **Create channel**。
1. 輸入管道名稱，並選擇性地輸入說明。
1. 在 **Configurations** 中，選取 **Channel type**。後續設定取決於類型：電子郵件管道會要求寄件者類型、寄件者及收件者，而 Slack 管道則會要求 Webhook URL。
1. 輸入該管道類型的設定。
1. 選擇性地選取 **Send test message**，以確認管道可正常運作。
1. 選取 **Create**。

### 設定所有作業的預設值

預設設定會套用至叢集中的每個重新索引、縮小、分割、複製、強制合併及開啟作業：

1. 在 **Index Management** 中，選取 **Notification settings**。
1. 在 **Defaults for index operations** 中，為 **reindex**、**shrink, split, clone**、**force merge** 及 **open** 各選取 **Has failed**、**Has completed** 或兩者。
1. 針對您選取通知的每個作業，從 **Notification channels** 中選取一或多個管道。
1. 選取 **Save**。

檢視或變更預設通知設定需要讀取這些設定的權限。

### 傳送其他通知

重新索引、分割、縮小及強制合併作業除了預設值之外，還能帶有自己的通知設定：

1. 在 **Index Management** 中，選取 **Indexes**。
1. 選取該作業適用的索引。
1. 選取 **Actions**，然後選取作業，例如 **Reindex**。
1. 展開 **Advanced settings**。**Notifications** 區段會列出目前生效的預設值。
1. 選取 **Send additional notifications**。
1. 選取 **Has failed / timed out**、**Has completed** 或兩者。
1. 從 **Notification channels** 中選取管道。
1. 選取該作業的按鈕，例如 **Reindex**。

## 相關文件

- [通知]({{site.url}}{{site.baseurl}}/observing-your-data/notifications/index/)
- [索引維護]({{site.url}}{{site.baseurl}}/im-plugin/index-maintenance/)
- [重新編製資料索引]({{site.url}}{{site.baseurl}}/im-plugin/reindex-data/)
- [ISM API]({{site.url}}{{site.baseurl}}/im-plugin/ism/api/)
