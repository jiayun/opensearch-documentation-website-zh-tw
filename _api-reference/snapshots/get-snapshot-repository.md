---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得快照儲存庫"
parent: Snapshot APIs
nav_order: 2
---

# 取得快照儲存庫 API
**1.0 版推出**
{: .label .label-purple }

擷取快照儲存庫的相關資訊。

若要進一步了解儲存庫，請參閱[註冊儲存庫]({{site.url}}{{site.baseurl}}/opensearch/snapshots/snapshot-restore#register-repository)。

您也可以在建立快照期間及之後取得快照的詳細資訊。請參閱[取得快照狀態]({{site.url}}{{site.baseurl}}/api-reference/snapshots/get-snapshot-status/)。
{: .note}

## 端點

```json
GET /_snapshot/{repository}
```

## 路徑參數

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `repository` | 字串 | 要擷取的快照儲存庫名稱清單，以逗號分隔。支援萬用字元（`*`）運算式，包括將萬用字元與以 `-` 開頭的排除模式結合使用。 |

## 查詢參數

| 參數 | 資料類型 | 說明 | 
:--- | :--- | :---
| `local` | 布林值 | 是否從本機節點取得資訊。選用，預設為 `false`。|
| `cluster_manager_timeout` | 時間 | 等待連線至叢集管理員節點的時間長度。選用，預設為 30 秒。 |

## 範例請求

下列請求會擷取 `my-opensearch-repo` 儲存庫的資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_snapshot/my-opensearch-repo
-->
{% capture step1_rest %}
GET /_snapshot/my-opensearch-repo
{% endcapture %}

{% capture step1_python %}


response = client.snapshot.get_repository(
  repository = "my-opensearch-repo"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

成功時，回應會傳回儲存庫資訊。此範例適用於 `s3` 儲存庫類型。

````json
{
  "my-opensearch-repo" : {
    "type" : "s3",
    "settings" : {
      "bucket" : "my-open-search-bucket",
      "base_path" : "snapshots"
    }
  }
}
````

## 回應本文欄位

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- | 
| `type` | 字串 | 桶 (bucket) 類型：`fs`（檔案系統）或 `s3`（S3 桶） |
| `bucket` | 字串 | S3 桶名稱。 |
| `base_path` | 字串 | 桶內用於儲存快照的資料夾。 |

## 必要權限

如果您使用 Security 外掛程式，請確認您擁有適當的權限：`cluster:admin/repository/get`。
