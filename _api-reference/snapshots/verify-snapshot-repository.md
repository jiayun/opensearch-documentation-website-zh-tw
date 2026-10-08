---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "驗證快照儲存庫"
parent: Snapshot APIs
nav_order: 4
---

# Verify Snapshot Repository API
**自 1.0 版起提供**
{: .label .label-purple }

驗證快照儲存庫是否正常運作。在叢集中的每個節點上驗證儲存庫。

如果驗證成功，Verify Snapshot Repository API 會傳回已連線至快照儲存庫的節點清單。如果驗證失敗，API 會傳回錯誤。

如果您使用 Security 外掛程式，您必須具備 `manage cluster` 權限。
{: .note}

## 端點

```json
GET _snapshot/{repository}/
```

## 路徑參數

路徑參數為選用。 

| 參數 | 資料類型 | 說明 | 
:--- | :--- | :---
| `repository` | 字串 | 要驗證的儲存庫名稱。 |

## 查詢參數

| 參數 | 資料類型 | 說明 | 
:--- | :--- | :---
| `cluster_manager_timeout` | 時間 | 等待與叢集管理員節點建立連線的時間。選用，預設為 `30s`。 |
| `timeout` | 時間 | 等待回應的時間。如果在逾時值所指定的時間內未收到回應，請求會失敗並傳回錯誤。預設為 `30s`。 |

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

下列範例對應至前述的[範例請求](#example-request)。

`POST /_snapshot/my-opensearch-repo/_verify?timeout=0s&cluster_manager_timeout=50s` 請求會傳回下列欄位：

````json
{
  "nodes" : {
    "by1kztwTRoeCyg4iGU5Y8A" : {
      "name" : "opensearch-node1"
    }
  }
}
````

在前述範例中，有一個節點已連線至快照儲存庫。如果有更多節點已連線，您會在回應中看到這些節點。例如：

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

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `nodes` | 物件 | 已連線至快照儲存庫的節點清單（並非陣列）。每個節點本身都是一個屬性，其中節點 ID 是索引鍵，而名稱具有 ID（物件）和名稱（字串）。 |

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:admin/repository/verify`。
