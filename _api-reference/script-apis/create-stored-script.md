---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立或更新預存指令碼"
parent: Script APIs
nav_order: 10
---

# 建立或更新預存指令碼 API
**1.0 版引入**
{: .label .label-purple }

在叢集狀態中建立或更新預存指令碼或搜尋範本。預存指令碼只會編譯一次，且可在多個請求之間重複使用，以獲得更好的效能。

如需 Painless 指令碼的更多資訊，請參閱：

* [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

* [k-NN Painless 指令碼擴充功能]({{site.url}}{{site.baseurl}}/search-plugins/knn/painless-functions/)。

* [k-NN]({{site.url}}{{site.baseurl}}/search-plugins/knn/index/)。


## 路徑參數

| 參數 | 資料類型 | 說明 | 
:--- | :--- | :---
| `script-id` | String | 預存指令碼或搜尋範本 ID。在整個叢集中必須是唯一的。必要。 |

## 查詢參數

所有參數皆為選用。

| 參數 | 資料類型 | 說明 | 
:--- | :--- | :---
| `context` | String | 指令碼或搜尋範本執行時所在的情境。為避免發生錯誤，API 會立即在此情境中編譯指令碼或範本。 |
| `cluster_manager_timeout` | Time | 等待與叢集管理員建立連線的時間長度。預設為 30 秒。 |
| `timeout` | Time | 等待回應的時間長度。若在逾時值之前未收到回應，請求即會失敗並傳回錯誤。預設為 30 秒。|

## 請求本文欄位

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `script` | Object | 定義指令碼或搜尋範本、其參數及其語言。請參閱下方的 *Script 物件* 一節。 |

*Script 物件*

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `lang` | String | 指令碼語言。必要。 |
| `source` | String 或 Object | 必要。<br /> <br /> 對於指令碼，為包含指令碼內容的字串。<br /> <br /> 對於搜尋範本，為定義搜尋範本的物件。支援與 [Search]({{site.url}}{{site.baseurl}}/api-reference/search/) API 請求本文相同的參數。搜尋範本也支援 Mustache 變數。 |

## 請求範例

下列請求範例使用名為 `books` 的索引，其中包含下列文件：

<!-- spec_insert_start
component: example_code
rest: POST /_bulk
body: |
{"index":{"_index":"books","_id":1}}
{"name":"book1","author":"Faustine","ratings":[4,3,5]}
{"index":{"_index":"books","_id":2}}
{"name":"book2","author":"Amit","ratings":[5,5,5]}
{"index":{"_index":"books","_id":3}}
{"name":"book3","author":"Gilroy","ratings":[2,1,5]}
-->
{% capture step1_rest %}
POST /_bulk
{"index":{"_index":"books","_id":1}}
{"name":"book1","author":"Faustine","ratings":[4,3,5]}
{"index":{"_index":"books","_id":2}}
{"name":"book2","author":"Amit","ratings":[5,5,5]}
{"index":{"_index":"books","_id":3}}
{"name":"book3","author":"Gilroy","ratings":[2,1,5]}
{% endcapture %}

{% capture step1_python %}


response = client.bulk(
  body = '''
{"index":{"_index":"books","_id":1}}
{"name":"book1","author":"Faustine","ratings":[4,3,5]}
{"index":{"_index":"books","_id":2}}
{"name":"book2","author":"Amit","ratings":[5,5,5]}
{"index":{"_index":"books","_id":3}}
{"name":"book3","author":"Gilroy","ratings":[2,1,5]}
'''
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 建立 Painless 指令碼

下列請求會建立 Painless 指令碼 `my-first-script`。此指令碼會加總每本書的評分，並在輸出中顯示總和。

<!-- spec_insert_start
component: example_code
rest: PUT /_scripts/my-first-script
body: |
{
  "script": {
      "lang": "painless",
      "source": """
          int total = 0;
          for (int i = 0; i < doc['ratings'].length; ++i) {
            total += doc['ratings'][i];
          }
          return total;
        """
  }
}
-->
{% capture step1_rest %}
PUT /_scripts/my-first-script
{
  "script": {
      "lang": "painless",
      "source": """
          int total = 0;
          for (int i = 0; i < doc['ratings'].length; ++i) {
            total += doc['ratings'][i];
          }
          return total;
        """
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.put_script(
  id = "my-first-script",
  body = '''
{
  "script": {
      "lang": "painless",
      "source": """
          int total = 0;
          for (int i = 0; i < doc['ratings'].length; ++i) {
            total += doc['ratings'][i];
          }
          return total;
        """
  }
}
'''
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

上述範例使用 OpenSearch Dashboards 中 Dev Tools 主控台的語法。您也可以使用 cURL 請求。
{: .note }

下列 cURL 請求等同於先前的 Dashboards 主控台範例：

````json
curl -XPUT "http://opensearch:9200/_scripts/my-first-script" -H 'Content-Type: application/json' -d'
{
  "script": {
      "lang": "painless",
      "source": "\n          int total = 0;\n          for (int i = 0; i < doc['\''ratings'\''].length; ++i) {\n            total += doc['\''ratings'\''][i];\n          }\n          return total;\n        "
  }
}'
````
{% include copy.html %}


如需執行指令碼的相關資訊，請參閱[執行 Painless 預存指令碼]({{site.url}}{{site.baseurl}}/api-reference/script-apis/exec-stored-script/)。

### 建立或更新含參數的預存指令碼

Painless 指令碼支援使用 `params` 將變數傳遞給指令碼。 

下列請求會建立 Painless 指令碼 `multiplier-script`。此請求會加總每本書的評分，將加總值乘以 `multiplier` 參數，並在輸出中顯示結果：

<!-- spec_insert_start
component: example_code
rest: PUT /_scripts/multiplier-script
body: |
{
  "script": {
      "lang": "painless",
      "source": """
          int total = 0;
          for (int i = 0; i < doc['ratings'].length; ++i) {
            total += doc['ratings'][i];
          }
          return total * params['multiplier'];
        """
  }
}
-->
{% capture step1_rest %}
PUT /_scripts/multiplier-script
{
  "script": {
      "lang": "painless",
      "source": """
          int total = 0;
          for (int i = 0; i < doc['ratings'].length; ++i) {
            total += doc['ratings'][i];
          }
          return total * params['multiplier'];
        """
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.put_script(
  id = "multiplier-script",
  body = '''
{
  "script": {
      "lang": "painless",
      "source": """
          int total = 0;
          for (int i = 0; i < doc['ratings'].length; ++i) {
            total += doc['ratings'][i];
          }
          return total * params['multiplier'];
        """
  }
}
'''
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

`PUT _scripts/my-first-script` 請求會傳回下列欄位：

````json
{
  "acknowledged" : true
}
````

若要確認指令碼是否已成功建立，請使用 [Get stored script]({{site.url}}{{site.baseurl}}/api-reference/script-apis/get-stored-script/) API，並將指令碼名稱作為 `script` 路徑參數傳入。
{: .note}

## 必要權限

若您使用 Security 外掛程式，請確認您具有適當的權限：`cluster:admin/script/put`。
