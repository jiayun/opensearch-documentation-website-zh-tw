---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得已儲存指令碼"
parent: Script APIs
nav_order: 30
---

# 取得已儲存指令碼 API
**於 1.0 版推出**
{: .label .label-purple }

從叢集狀態擷取已儲存的指令碼。

## 端點

```json
GET _scripts/my-first-script
```

## 路徑參數

| 參數 | 資料類型 | 說明 | 
:--- | :--- | :---
| `script` | 字串 | 已儲存指令碼或搜尋範本的名稱。必要。|

## 查詢參數

| 參數 | 資料類型 | 說明 | 
:--- | :--- | :---
| `cluster_manager_timeout` | 時間 | 等待連線至叢集管理員的時間。選用，預設為 `30s`。 |

## 請求範例

以下範例會擷取已儲存的 `my-first-script` 指令碼。

<!-- spec_insert_start
component: example_code
rest: GET /_scripts/my-first-script
-->
{% capture step1_rest %}
GET /_scripts/my-first-script
{% endcapture %}

{% capture step1_python %}


response = client.get_script(
  id = "my-first-script"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

`GET _scripts/my-first-script` 請求會傳回下列欄位：

````json
{
  "_id" : "my-first-script",
  "found" : true,
  "script" : {
    "lang" : "painless",
    "source" : """
          int total = 0;
          for (int i = 0; i < doc['ratings'].length; ++i) {
            total += doc['ratings'][i];
          }
          return total;
        """
  }
}
````

## 回應本文欄位

`GET _scripts/my-first-script` 請求會傳回下列回應欄位：

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `_id` | 字串 | 指令碼的名稱。 |
| `found` | 布林值 | 請求的指令碼存在且已擷取。 |
| `script` | 物件 | 指令碼定義。請參閱[指令碼物件](#script-object)。  |

#### 指令碼物件

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `lang` | 字串 | 指令碼的語言。 |
| `source` | 字串 | 指令碼的本文。 |

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:admin/script/get`。
