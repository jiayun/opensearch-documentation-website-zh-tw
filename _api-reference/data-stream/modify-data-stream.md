---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "修改資料串流"
parent: Data stream APIs
nav_order: 50
redirect_from:
  - /api-reference/index-apis/modify-data-stream/
---

# Modify Data Stream API
**於 3.8 版推出**
{: .label .label-purple }

這是實驗性功能，不建議在正式環境中使用。若要瞭解此功能的最新進展或提供意見回饋，請參閱相關的 [GitHub 議題](https://github.com/opensearch-project/OpenSearch/issues/8271)。
{: .warning}

Modify Data Stream API 可新增或移除[資料串流]({{site.url}}{{site.baseurl}}/im-plugin/data-streams/)的支援索引。使用此 API 可將既有的一般索引遷移至資料串流，或將支援索引從資料串流中分離而不刪除其資料。

新增或移除支援索引時，適用下列行為與限制：

- 新增和移除動作只會變更資料串流的中繼資料；索引及其資料維持不變。不會建立、刪除、還原或重新配置任何分片。
- 您可以在一個請求中包含多個新增和移除動作。所有動作都會在單次叢集狀態更新中以不可分割的方式套用，且結果與動作順序無關。
- 資料串流的世代由其支援索引推導而來（支援索引計數器值最高的索引即為寫入索引），無法直接設定。
- 無法移除寫入索引，且移除最後一個支援索引的操作會遭到拒絕。
- 新增的索引必須將資料串流的時間戳記欄位對應為 `date` 或 `date_nanos`。新增的索引會標記為隱藏；移除的索引則會恢復為可見。
- 新增的索引不必遵循 `.ds-<data_stream>-NNNNNN` 命名慣例，因此您可以將既有的一般索引遷移至資料串流。
- 一個索引不能作為多個資料串流的支援索引。

## 端點

```json
POST /_data_stream/_modify
```

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `cluster_manager_timeout` | 時間 | 等待叢集管理員節點回應的時間。預設為 `30s`。 |
| `timeout` | 時間 | 等待叢集回應的時間。預設為 `30s`。 |

## 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `actions` | 陣列 | 要執行的動作清單。您必須提供至少一個動作。必要。 |

`actions` 陣列中的每個元素都是指定單一動作的單一鍵物件。下表列出可用的動作欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `add_backing_index.data_stream` | 字串 | 要修改的資料串流名稱。必要。 |
| `add_backing_index.index` | 字串 | 要新增為支援索引的索引名稱。必要。 |
| `remove_backing_index.data_stream` | 字串 | 要修改的資料串流名稱。必要。 |
| `remove_backing_index.index` | 字串 | 要移除的支援索引名稱。必要。 |
| `add_backing_index` | 物件 | 將既有索引新增至資料串流，作為支援索引。選用。 |
| `remove_backing_index` | 物件 | 從資料串流移除支援索引。選用。 |

## 請求範例

下列請求會在單次不可分割的操作中，從 `logs-foo` 資料串流移除一個支援索引，並將既有的 `legacy-logs-2023` 索引新增至該資料串流：

```json
POST /_data_stream/_modify
{
  "actions": [
    {
      "remove_backing_index": {
        "data_stream": "logs-foo",
        "index": ".ds-logs-foo-000001"
      }
    },
    {
      "add_backing_index": {
        "data_stream": "logs-foo",
        "index": "legacy-logs-2023"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 回應範例

```json
{
  "acknowledged": true
}
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:admin/data_stream/modify`。

## 相關文件

- [資料串流]({{site.url}}{{site.baseurl}}/im-plugin/data-streams/)
- [Data Stream Stats API]({{site.url}}{{site.baseurl}}/api-reference/data-stream/data-stream-stats/)
