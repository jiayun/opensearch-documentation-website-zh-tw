---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "驗證快照儲存庫"
parent: Snapshot APIs
nav_order: 40
---

# 驗證快照儲存庫 API
**自 1.0 版引入**
{: .label .label-purple }

驗證快照儲存庫是否正常運作。會對叢集中的每個節點驗證該儲存庫。

如果驗證成功，Verify Snapshot Repository API 會回傳連線到該快照儲存庫的節點清單。如果驗證失敗，API 會回傳錯誤。

如果您使用 Security 外掛程式，則必須具備 `manage cluster` 權限。
{: .note}

## 端點

```json
GET _snapshot/{repository}/
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 | 
:--- | :--- | :---
| `repository` | 字串 | 要驗證的儲存庫名稱。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 
:--- | :--- | :---
| `cluster_manager_timeout` | Time | 等待連線到叢集管理員節點的時間長度。選用，預設為 `30s`。 |
| `timeout` | Time | 等待回應的時間長度。如果在逾時值之前未收到回應，請求會失敗並回傳錯誤。預設為 `30s`。 |

## 範例請求

下列請求會驗證 `my-opensearch-repo` 是否正常運作：

<!-- spec_insert_start
component: example_code
rest: POST /_snapshot/my-opensearch-repo/_verify?timeout=0s&cluster_manager_timeout=50s
-->
{% capture step1_rest %}
POST /_snapshot/my-opensearch-repo/_verify?timeout=0s&cluster_manager_timeout=50s
{% endcapture %}

{% capture step1_python %}


response = client.snapshot.verify_repository(
  repository = "my-opensearch-repo",
  params = { "timeout": "0s", "cluster_manager_timeout": "50s" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

下列範例對應於前述的[範例請求](#example-request)。

`POST /_snapshot/my-opensearch-repo/_verify?timeout=0s&cluster_manager_timeout=50s` 請求會回傳下列欄位：

````json
{
  "nodes" : {
    "by1kztwTRoeCyg4iGU5Y8A" : {
      "name" : "opensearch-node1"
    }
  }
}
````

在上述範例中，有一個節點連線到該快照儲存庫。如果連線的節點更多，您會在回應中看到它們。範例：

````json
{
  "nodes" : {
    "lcfL6jv2jo6sMEtp4idMvg" : {
      "name" : "node-1"
    },
    "rEPtFT/B+cuuOHnQn0jy4s" : {
      "name" : "node-2"
  }
}
````

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `nodes` | 物件 | 連線到該快照儲存庫的節點清單（不是陣列）。每個節點本身是一個屬性，其中節點 ID 是鍵，並包含一個 ID（物件）和一個名稱（字串）。 |

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：`cluster:admin/repository/verify`。
