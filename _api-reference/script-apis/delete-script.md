---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除預存指令碼"
parent: Script APIs
nav_order: 40
---

# 刪除預存指令碼 API
**1.0 版推出**
{: .label .label-purple }

從叢集狀態中刪除預存指令碼。

## 端點

```json
DELETE _scripts/my-script
```

## 路徑參數

路徑參數為選用。 

| 參數 | 資料類型 | 說明 | 
:--- | :--- | :---
| `script-id` | 字串 | 要刪除的指令碼 ID。 |

## 查詢參數

| 參數 | 資料類型 | 說明 | 
:--- | :--- | :---
| `cluster_manager_timeout` | Time | 等待與叢集管理員節點建立連線的時間長度。選用，預設為 `30s`。 |
| `timeout` | Time | 等待回應的時間長度。如果在逾時值之前未收到回應，請求將會被捨棄。

## 請求範例

下列請求會刪除 `my-first-script` 指令碼：

<!-- spec_insert_start
component: example_code
rest: DELETE /_scripts/my-script
-->
{% capture step1_rest %}
DELETE /_scripts/my-script
{% endcapture %}

{% capture step1_python %}


response = client.delete_script(
  id = "my-script"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

`DELETE _scripts/my-first-script` 請求會傳回下列欄位：

````json
{
  "acknowledged" : true
}
````

若要確認預存指令碼是否已成功刪除，請使用[取得預存指令碼]({{site.url}}{{site.baseurl}}/api-reference/script-apis/get-stored-script/) API，並將指令碼名稱作為 `script` 路徑參數傳入。

## 回應本文欄位

此 <HTTP METHOD> <endpoint> 請求會傳回下列回應欄位：

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `acknowledged` | 布林值 | 是否已收到刪除指令碼請求。 |

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:admin/script/delete`。
