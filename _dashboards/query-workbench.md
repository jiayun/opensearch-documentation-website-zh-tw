---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 Query Workbench"
parent: Exploring data
nav_order: 30
redirect_from:
  - /search-plugins/sql/workbench/
---

# 使用 Query Workbench

您可以在 OpenSearch Dashboards 中使用 Query Workbench 來執行隨選的 [SQL]({{site.url}}{{site.baseurl}}/search-plugins/sql/sql/index/) 和 [PPL]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/) 查詢，將查詢轉換為等效的 REST API 呼叫，並以不同的 [回應格式]({{site.url}}{{site.baseurl}}/search-plugins/sql/response-formats/) 檢視及儲存結果。

Query Workbench 不支援透過 SQL 或 PPL 執行刪除或更新操作。對資料的存取為唯讀。
{: .important}

## 前置條件

在開始本教學之前，請透過發送以下 [Bulk API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) 請求來為範例文件編製索引：

```json
PUT accounts/_bulk?refresh
{"index":{"_id":"1"}}
{"account_number":1,"balance":39225,"firstname":"Amber","lastname":"Duke","age":32,"gender":"M","address":"880 Holmes Lane","employer":"Pyrami","email":"amberduke@pyrami.com","city":"Brogan","state":"IL"}
{"index":{"_id":"6"}}
{"account_number":6,"balance":5686,"firstname":"Hattie","lastname":"Bond","age":36,"gender":"M","address":"671 Bristol Street","employer":"Netagy","email":"hattiebond@netagy.com","city":"Dante","state":"TN"}
{"index":{"_id":"13"}}
{"account_number":13,"balance":32838,"firstname":"Nanette","lastname":"Bates","age":28,"gender":"F","address":"789 Madison Street","employer":"Quility","email":"nanettebates@quility.com","city":"Nogal","state":"VA"}
{"index":{"_id":"18"}}
{"account_number":18,"balance":4180,"firstname":"Dale","lastname":"Adams","age":33,"gender":"M","address":"467 Hutchinson Court","email":"daleadams@boink.com","city":"Orick","state":"MD"}
```
{% include copy-curl.html %}

請參閱 [管理索引]({{site.url}}{{site.baseurl}}/im-plugin/index/) 以了解如何為您自己的資料編製索引。

## 在 Query Workbench 中執行 SQL 查詢
 
 以下步驟將引導您對 OpenSearch 資料執行 SQL 查詢：

1. 存取 Query Workbench。
    - 若要存取 Query Workbench，請前往 OpenSearch Dashboards，並從主選單選擇 **OpenSearch Plugins** > **Query Workbench**。

2. 執行查詢。
    - 選取 **SQL** 按鈕。在查詢編輯器中輸入 SQL 運算式，然後選取 **Run** 按鈕以執行查詢。 
    
    以下範例查詢會從 `accounts` 索引中擷取餘額大於 10,000 之帳戶的名字、姓氏和餘額，並依餘額遞減排序：

    ```sql
    SELECT
      firstname,
      lastname,
      balance
    FROM
      accounts
    WHERE
      balance > 10000
    ORDER BY
      balance DESC;
    ```
    {% include copy.html %}
    
3. 檢視結果。
    - 在 **Results** 窗格中檢視結果，該窗格會以表格格式呈現查詢輸出。您可以視需要篩選及下載結果。

4. 清除查詢編輯器。  
    - 選取 **Clear** 按鈕以清除查詢編輯器並執行新的查詢。 

5. 檢查查詢的處理方式。
    - 選取 **Explain** 按鈕以檢查 OpenSearch 如何處理查詢，包括所涉及的步驟及作業順序。

## 在 Query Workbench 中執行 PPL 查詢

請依照以下步驟了解如何對 OpenSearch 資料執行 PPL 查詢：

1. 存取 Query Workbench。
    - 若要存取 Query Workbench，請前往 OpenSearch Dashboards，並從主選單選擇 **OpenSearch Plugins** > **Query Workbench**。

2. 執行查詢。
    - 選取 **PPL** 按鈕。在查詢編輯器中輸入 PPL 查詢，然後選取 **Run** 按鈕以執行查詢。 
    
    以下範例查詢會針對 `accounts` 索引中年齡大於 `18` 的文件，擷取 `firstname` 和 `lastname` 欄位：
    
    ```sql
    search source=accounts
    | where age > 18
    | fields firstname, lastname
    ```
    {% include copy.html %}
    
3. 檢視結果。
    - 在 **Results** 窗格中檢視結果，該窗格會以表格格式呈現查詢輸出。

4. 清除查詢編輯器。  
    - 選取 **Clear** 按鈕以清除查詢編輯器並執行新的查詢。 

5. 檢查查詢的處理方式。
    - 選取 **Explain** 按鈕以檢查 OpenSearch 如何處理查詢，包括所涉及的步驟及作業順序。
