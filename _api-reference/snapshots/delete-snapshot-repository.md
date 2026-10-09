---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除快照儲存庫"
parent: Snapshot APIs
nav_order: 3
---

# 刪除快照儲存庫組態 API
**引進於 1.0 版**
{: .label .label-purple }

刪除快照儲存庫組態。  
 
OpenSearch 中的儲存庫只是一種組態，將儲存庫名稱對應到某個類型（檔案系統或 s3 儲存庫），並依類型包含其他資訊。該組態由檔案系統位置或 s3 儲存貯體支援。當您呼叫此 API 時，並不會刪除實體的檔案系統或 s3 儲存貯體本身，只會刪除組態。

若要進一步了解儲存庫，請參閱[註冊或更新快照儲存庫]({{site.url}}{{site.baseurl}}/api-reference/snapshots/create-repository/)。

## 端點

```json
DELETE _snapshot/{repository}
```

## 路徑參數

參數 | 資料類型 | 說明
:--- | :--- | :---
`repository` | 字串 | 要刪除的儲存庫。 |

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

若要驗證儲存庫是否已刪除，請使用[取得快照儲存庫]({{site.url}}{{site.baseurl}}/api-reference/snapshots/get-snapshot-repository/) API，並將儲存庫名稱作為 `repository` 路徑參數傳入。
{: .note}

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`cluster:admin/repository/delete`。
