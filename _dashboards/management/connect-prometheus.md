---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "將 Prometheus 連接至 OpenSearch"
parent: Connecting data sources
nav_order: 60
---

# 將 Prometheus 連接至 OpenSearch
於 2.16 版引入
{: .label .label-purple }

本文件說明如何使用 OpenSearch Dashboards 介面將 Prometheus 連接至 OpenSearch 的主要步驟，包括設定資料來源連線、修改連線詳細資料，以及為 Prometheus 資料建立索引模式。

## 先決條件與權限

連接資料來源之前，請確認您已符合[先決條件]({{site.url}}{{site.baseurl}}/dashboards/management/data-sources/#prerequisites)並具備必要的[權限]({{site.url}}{{site.baseurl}}/dashboards/management/data-sources/#permissions)。

## 建立 Prometheus 資料來源連線

資料來源連線會指定連接至資料來源所需的參數。這些參數會組成該資料來源的連線字串。您可以使用 OpenSearch Dashboards 新增 **Prometheus** 資料來源連線，或管理現有的連線。

請依照下列步驟連接您的資料來源：

1. 在 OpenSearch Dashboards 主選單中，前往 **Management** > **Data sources** > **New data source** > **Prometheus**。

2. 在 **Configure Prometheus data source** 區段中：
   
   - 在 **Data source details** 下，提供標題及選用的描述。
   - 在 **Prometheus data location** 下，輸入 Prometheus URI。
   - 在 **Authentication details** 下，從下拉式清單中選取適當的驗證方法，並輸入必要的詳細資料：
       - **Basic authentication**：輸入使用者名稱和密碼。
       - **AWS Signature Version 4**：指定 **Region**，從 **Service Name** 清單中選取 OpenSearch 服務（**Amazon OpenSearch Service** 或 **Amazon OpenSearch Serverless**），然後輸入 **Access Key** 和 **Secret Key**。
   - 在 **Query permissions** 下，選擇搜尋資料及將資料編製索引所需的角色。如果您選取 **Restricted**，將會出現一個額外的欄位，供您設定所需的角色。

3. 選取 **Review Configuration** > **Connect to Prometheus** 以儲存您的設定。新的連線將會出現在資料來源清單中。

## 修改資料來源連線

若要修改資料來源連線，請依照下列步驟操作：

1. 在 **Data sources** 主頁面的清單中選取所需的連線。這會開啟 **Connection Details** 視窗。
2. 在 **Connection Details** 視窗中，編輯 **Title** 和 **Description** 欄位。選取 **Save changes** 按鈕以套用變更。
3. 若要更新 **Authentication Method**，請從下拉式清單中選擇方法，並輸入任何必要的憑證資訊。選取 **Save changes** 以套用變更。
    - 若要更新 **Basic authentication** 驗證方法，請選取 **Update stored password** 按鈕。在快顯視窗中輸入更新後的密碼並加以確認，然後選取 **Update stored password** 以儲存變更。若要測試連線，請選取 **Test connection** 按鈕。
    - 若要更新 **AWS Signature Version 4** 驗證方法，請選取 **Update stored AWS credential** 按鈕。在快顯視窗中輸入更新後的存取金鑰和秘密金鑰，然後選取 **Update stored AWS credential** 以儲存變更。若要測試連線，請選取 **Test connection** 按鈕。

## 刪除資料來源連線

若要刪除資料來源連線，請選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/dashboards/trash-can-icon.png" class="inline-icon" alt="delete icon"/>{:/}（刪除）圖示。

## 建立索引模式

建立資料來源連線之後，下一步是為該資料來源建立索引模式。如需索引模式的詳細資訊和教學，請參閱[索引模式]({{site.url}}{{site.baseurl}}/dashboards/management/index-patterns/)。 
