---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "強制恢復"
nav_order: 25
parent: Cross-cluster replication
---

# 強制恢復複寫
**於 3.8 版推出**
{: .label .label-purple }


當跨叢集複寫暫停的時間超過保留租約期限（由領導索引上的 `index.soft_deletes.retention_lease.period` 設定控制，預設為 12 小時）時，領導叢集的 translog 不再保留追隨者所需的作業。由於保留租約已過期，一般的恢復請求會失敗。您可以在傳送恢復請求時使用 `force_resume` 參數，從領導者的快照還原追隨者索引並重新建立複寫。這可免除手動停止現有複寫、刪除追隨者索引，以及從頭開始複寫的需求。

強制恢復複寫會依循下列步驟：

1. 驗證複寫目前處於 `PAUSED` 狀態，且保留租約已過期（使一般恢復無法進行）。如果保留租約尚未過期，則會忽略 `force_resume` 旗標，並正常恢復複寫。
1. 呼叫現有的停止複寫動作來停止複寫，這會刪除複寫中繼資料，並移除索引區塊與複寫任務。
1. 刪除追隨者索引，以便從快照還原。
1. 使用原始連線別名與領導索引組態啟動複寫。這會觸發從領導叢集進行快照還原，並在還原過程中取得新的保留租約。
1. 在還原完成後恢復以 translog 為基礎的複寫。分片複寫任務會啟動，並使用新取得的保留租約來複寫領導者持續進行的作業。

強制恢復會使用原始複寫權限，且不需要重新設定。所有作業都會記錄以供稽核。
{: .note}

## 強制恢復工作流程

下列範例示範完整的強制恢復工作流程。

### 步驟 1：驗證複寫狀態

確認複寫已暫停，並找出暫停的原因：

```json
GET /_plugins/_replication/follower-01/_status
```
{% include copy-curl.html %}

例如，下列回應顯示複寫處於使用者起始的暫停狀態：

```json
{
  "status": "PAUSED",
  "reason": "User initiated",
  "leader_alias": "my-connection-alias",
  "leader_index": "leader-01",
  "follower_index": "follower-01"
}
```

### 步驟 2：嘗試正常恢復複寫

嘗試正常恢復複寫：

```json
POST /_plugins/_replication/follower-01/_resume
{}
```
{% include copy-curl.html %}

如果保留租約已過期，您會收到下列錯誤：

```json
{
  "error": {
    "root_cause": [{
      "type": "resource_not_found_exception",
      "reason": "Retention lease doesn't exist. Use force_resume=true to restore from snapshot."
    }],
    "type": "resource_not_found_exception",
    "reason": "Retention lease doesn't exist. Use force_resume=true to restore from snapshot."
  },
  "status": 404
}
```

### 步驟 3：使用強制恢復

使用強制恢復從快照還原追隨者索引：

```json
POST /_plugins/_replication/follower-01/_resume
{
   "force_resume": true
}
```
{% include copy-curl.html %}


### 步驟 4：監視恢復進度

起始強制恢復後，在快照還原進行期間，追隨者索引會暫時無法使用。若要監視其狀態，請傳送下列請求：

```json
GET /_plugins/_replication/follower-01/_status
```
{% include copy-curl.html %}

在快照還原期間，`status` 為 `RESTORING`：

```json
{
  "status": "RESTORING",
  "reason": "User initiated",
  "leader_alias": "my-connection-alias",
  "leader_index": "leader-01",
  "follower_index": "follower-01"
}
```

還原完成後，`status` 會變更為 `SYNCING`：

```json
{
  "status": "SYNCING",
  "reason": "User initiated",
  "leader_alias": "my-connection-alias",
  "leader_index": "leader-01",
  "follower_index": "follower-01",
  "syncing_details": {
    "leader_checkpoint": 150,
    "follower_checkpoint": 150,
    "seq_no": 0
  }
}
```

## 失敗復原

下列清單說明在強制恢復期間的任何階段發生失敗時的預期行為：

- 如果停止失敗，作業會中止，追隨者會維持在 `PAUSED` 狀態。不會進行任何變更。您可以重試強制恢復。
- 如果停止後刪除失敗，複寫已停止，但追隨者索引仍然存在。您可以手動刪除索引並啟動複寫，或重試強制恢復。
- 如果刪除後啟動失敗，追隨者索引已刪除，且複寫中繼資料已移除。您需要使用標準啟動複寫 API，以原始連線別名與領導索引手動啟動複寫。
- 如果快照還原失敗，複寫任務會轉為失敗狀態並自動暫停。您可以重試強制恢復。

## 限制

請注意下列限制：

- 在強制恢復過程中，追隨者索引會被刪除並還原。在此期間，該索引無法用於搜尋查詢。持續時間取決於索引大小與叢集之間的網路頻寬。
- 強制恢復會還原整個索引。無法選擇只還原特定分片。
- 強制恢復後，追隨者索引是快照還原當下領導者的全新副本，複寫會從該時間點繼續進行。
- 針對指定的索引，一次只能執行一個恢復或強制恢復作業。在強制恢復進行期間傳送的第二個請求會被拒絕。

## 相關文件

- 如需 API 參考，包括請求語法與參數，請參閱[恢復複寫]({{site.url}}{{site.baseurl}}/tuning-your-cluster/replication-plugin/api/#resume-replication)。