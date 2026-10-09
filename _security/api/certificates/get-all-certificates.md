---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得所有憑證"
parent: Certificate APIs
grand_parent: Security APIs
nav_order: 20
---

# Get All Certificates API
**於 2.15 版推出**
{: .label .label-purple }

擷取叢集中每個節點正在使用的憑證，並依節點分組。若要擷取單一節點正在使用的憑證，請使用 [Get Node Certificates API]({{site.url}}{{site.baseurl}}/security/api/certificates/get-node-certificates/)。

此 API 保留給超級管理員使用。請使用管理員憑證進行驗證，而非使用者名稱與密碼。如需更多資訊，請參閱 [API 存取控制]({{site.url}}{{site.baseurl}}/security/access-control/api/#access-control-for-the-api)。
{: .note}

<!-- spec_insert_start
api: security.get_all_certificates
component: endpoints
-->
## 端點
```json
GET /_plugins/_security/api/certificates
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: security.get_all_certificates
component: query_parameters
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `cert_type` | 字串 | 要從所有節點擷取的憑證類型（`HTTP`、`TRANSPORT` 或 `ALL`）。 |
| `timeout` | 字串 | 在逾時前從所有節點擷取憑證所花費的最長持續時間（以秒為單位）。 |

<!-- spec_insert_end -->

## 範例請求

```json
GET _plugins/_security/api/certificates
```
{% include copy-curl.html security=true %}

## 範例回應

此處的回應經過縮減：

```json
{
  "_nodes": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "cluster_name": "opensearch-cluster",
  "nodes": {
    "DOlaf_0NSe-HkUXbca8-xA": {
      "name": "opensearch-node1",
      "certificates": {
        "http": [
          {
            "format": "pem",
            "alias": null,
            "subject_dn": "CN=Example Com Inc. Root CA,OU=Example Com Inc. Root CA,O=Example Com Inc.,DC=example,DC=com",
            "san": "",
            "serial_number": "76447790750572770562330390669309351583040514274",
            "issuer_dn": "CN=Example Com Inc. Root CA,OU=Example Com Inc. Root CA,O=Example Com Inc.,DC=example,DC=com",
            "has_private_key": false,
            "not_after": "2034-02-17T17:00:36Z",
            "not_before": "2034-02-17T17:00:36Z"
          },
          {
            "format": "pem",
            "alias": null,
            "subject_dn": "CN=node-0.example.com,OU=node,O=node,L=test,C=de",
            "san": "[[2, localhost], [2, node-0.example.com], [7, 0:0:0:0:0:0:0:1], [7, 127.0.0.1], [8, 1.2.3.4.5.5]]",
            "serial_number": "602402108696974692907516685054550755684962846902",
            "issuer_dn": "CN=Example Com Inc. Root CA,OU=Example Com Inc. Root CA,O=Example Com Inc.,DC=example,DC=com",
            "has_private_key": true,
            "not_after": "2034-02-17T17:03:25Z",
            "not_before": "2034-02-17T17:03:25Z"
          }
        ],
        "transport": [ ... ],
        "transport_client": [ ... ]
      }
    }
  }
}
```

## 回應本文欄位

回應本文是包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `_nodes` | 物件 | 請求觸及的節點數，以及成功和失敗的節點數。 |
| `cluster_name` | 字串 | 叢集的名稱。 |
| `nodes` | 物件 | 每個節點上的憑證，以節點 ID 為鍵。 |
| `nodes.<node_id>.name` | 字串 | 節點的名稱。 |
| `nodes.<node_id>.certificates` | 物件 | 節點的憑證，分組為 `http`、`transport` 和 `transport_client` 清單。 |

每個憑證包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `format` | 字串 | 憑證的格式，例如 `pem`。 |
| `alias` | 字串 | 金鑰儲存區中憑證的別名，或當憑證沒有別名時為 `null`。 |
| `subject_dn` | 字串 | 憑證主體的辨別名稱。 |
| `issuer_dn` | 字串 | 簽發該憑證的憑證授權單位辨別名稱。 |
| `san` | 字串 | 憑證中的主體替代名稱。 |
| `serial_number` | 字串 | 憑證的序號。 |
| `has_private_key` | 布林值 | 節點是否持有該憑證的私密金鑰。 |
| `not_before` | 字串 | 憑證生效的日期與時間。 |
| `not_after` | 字串 | 憑證到期的日期與時間。 |
