---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除快照儲存庫"
parent: Snapshot APIs
nav_order: 30
---

# 刪除快照儲存庫 API
**於 1.0 版推出**
{: .label .label-purple }

從叢集刪除快照儲存庫的註冊。儲存位置及其中的快照不會被刪除。若要再次使用這些快照，請使用[建立或更新快照儲存庫 API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/create-repository/) 重新註冊儲存庫。

## 端點

```json
DELETE _snapshot/{repository}
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`repository` | 字串 | 要刪除的儲存庫。

## 範例請求

下列請求會刪除 `my-opensearch-repo` 儲存庫：

<!-- spec_insert_start
component: example_code
rest: DELETE /_snapshot/my-opensearch-repo
-->
{% capture step1_rest %}
DELETE /_snapshot/my-opensearch-repo
{% endcapture %}

{% capture step1_python %}


response = client.snapshot.delete_repository(
  repository = "my-opensearch-repo"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

成功時，回應會傳回下列 JSON 物件：

````json
{
  "acknowledged" : true
}
````

若要確認儲存庫已刪除，請使用[取得快照儲存庫]({{site.url}}{{site.baseurl}}/api-reference/snapshots/get-snapshot-repository/) API，並將儲存庫名稱傳入 `repository` 路徑參數。
{: .note}

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`cluster:admin/repository/delete`。
