---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除快照"
parent: Snapshot APIs
nav_order: 7
---

# 刪除快照 API
**於 1.0 版導入**
{: .label .label-purple }

從儲存庫刪除快照。

刪除正在進行中的快照會停止快照作業，並刪除已部分建立的快照。

* 若要進一步了解快照，請參閱 [快照]({{site.url}}{{site.baseurl}}/opensearch/snapshots/index/)。

* 若要檢視儲存庫清單，請參閱 [cat repositories]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-repositories/)。

* 若要檢視快照清單，請參閱 [cat snapshots]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-snapshots/)。

## 路徑與 HTTP 方法

```json
DELETE _snapshot/{repository}/{snapshot}
```

## 路徑參數

參數 | 資料類型 | 說明
:--- | :--- | :---
`repository` | 字串 | 包含快照的儲存庫。 |
`snapshot` | 字串 | 要刪除的快照。 |

## 範例請求

下列請求從 `my-opensearch-repo` 儲存庫刪除名為 `my-first-snapshot` 的快照：

<!-- spec_insert_start
component: example_code
rest: DELETE /_snapshot/my-opensearch-repo/my-first-snapshot
-->
{% capture step1_rest %}
DELETE /_snapshot/my-opensearch-repo/my-first-snapshot
{% endcapture %}

{% capture step1_python %}


response = client.snapshot.delete(
  repository = "my-opensearch-repo",
  snapshot = "my-first-snapshot"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

成功時，回應會傳回下列 JSON 物件：

```json
{
  "acknowledged": true
}
```

若要驗證快照是否已刪除，請使用 [Get snapshot]({{site.url}}{{site.baseurl}}/api-reference/snapshots/get-snapshot/) API，並將快照名稱作為 `snapshot` 路徑參數傳入。
{: .note}

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：`cluster:admin/snapshot/delete`。
