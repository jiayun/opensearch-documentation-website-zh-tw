---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "修補辨別名稱"
parent: Distinguished name APIs
grand_parent: Security APIs
nav_order: 20
---

# 修補辨別名稱 API
**1.0 版導入**
{: .label .label-purple }

更新允許清單中的辨別名稱，而不會取代它們。指定叢集名稱即可更新單一叢集的辨別名稱，或省略叢集名稱以進行批次更新。

此 API 僅供超級管理員使用。請使用管理員憑證而非使用者名稱與密碼進行驗證。如需更多資訊，請參閱 [API 的存取控制]({{site.url}}{{site.baseurl}}/security/access-control/api/#access-control-for-the-api)。
{: .note}

<!-- spec_insert_start
api: security.patch_distinguished_names
component: endpoints
-->
## 端點
```json
PATCH /_plugins/_security/api/nodesdn
```
<!-- spec_insert_end -->
<!-- spec_insert_start
api: security.patch_distinguished_name
component: endpoints
omit_header: true
-->
```json
PATCH /_plugins/_security/api/nodesdn/{cluster_name}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `cluster_name` | 字串 | 否 | 您要更新其節點辨別名稱的叢集名稱。若省略，請求可修改多個叢集。 |

## 請求本文欄位

請求本文為必要項目。它是一個 JSON 物件陣列。每個物件包含下列欄位。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `op` | 字串 | 要執行的操作。有效值為 `add`、`remove`、`replace`、`move`、`copy` 與 `test`。 | 是 |
| `path` | 字串 | 要修改的路徑。指定叢集名稱時，路徑相對於該叢集，例如 `/nodes_dn/0`。省略叢集名稱時，路徑以叢集名稱開頭，例如 `/cluster1/nodes_dn/0`。 | 是 |
| `value` | 陣列 | 用於更新的新值。`add`、`replace` 與 `test` 操作需要此欄位。 | 否 |

## 範例請求

下列請求會取代 `cluster1` 允許清單中的第一個辨別名稱：

```json
PATCH _plugins/_security/api/nodesdn/cluster1
[
   {
      "op":"replace",
      "path":"/nodes_dn/0",
      "value": ["CN=Karen Berge,CN=admin,DC=corp,DC=Fabrikam,DC=COM", "CN=George Wall,CN=admin,DC=corp,DC=Fabrikam,DC=COM"]
   }
]
```
{% include copy-curl.html security=true %}

下列請求會在批次更新中進行相同的變更：

```json
PATCH _plugins/_security/api/nodesdn
[
   {
      "op":"replace",
      "path":"/cluster1/nodes_dn/0",
      "value": ["CN=Karen Berge,CN=admin,DC=corp,DC=Fabrikam,DC=COM", "CN=George Wall,CN=admin,DC=corp,DC=Fabrikam,DC=COM"]
   }
]
```
{% include copy-curl.html security=true %}

## 範例回應

更新單一叢集允許清單的請求會在回應中指明該叢集：

```json
{
  "status": "OK",
  "message": "'cluster1' updated."
}
```

批次請求不會指明其變更的叢集：

```json
{
  "status": "OK",
  "message": "Resource updated."
}
```

## 回應本文欄位

回應本文是具有下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `status` | 字串 | 請求的狀態。成功的請求會傳回 `OK`。 |
| `message` | 字串 | 描述操作結果的訊息。 |
