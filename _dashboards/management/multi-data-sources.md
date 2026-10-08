---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定和使用多個資料來源"
parent: Connecting data sources
nav_order: 20
redirect_from:
  - /dashboards/discover/multi-data-sources/
---

# 在 OpenSearch Dashboards 中設定和使用多個資料來源

您可以在 OpenSearch Dashboards 中匯入、處理和分析來自多個資料來源的資料。您可以在 **Dashboards Management** > **Data sources** 下設定資料來源。下圖顯示此介面。

![Dashboards Management 資料來源主畫面]({{site.url}}{{site.baseurl}}/images/dashboards/data_sources_management.png){: width="700" }

## 入門

下列教學將引導您在 OpenSearch Dashboards 中設定和使用多個資料來源。

使用多個資料來源時，不支援下列功能：時間軸 (timeline) 視覺化類型。
{: .note}

### 步驟 1：修改 YAML 檔案設定

若要使用多個資料來源，您必須啟用 `data_source.enabled` 設定。此設定預設為停用。若要啟用多個資料來源：

1. 開啟您本機的 OpenSearch Dashboards 組態檔案 `opensearch_dashboards.yml`。如果您沒有此檔案，可以在 GitHub 上取得 [`opensearch_dashboards.yml`](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/config/opensearch_dashboards.yml)。
2. 將 `data_source.enabled:` 設為 `true`，然後儲存 YAML 檔案。
3. 重新啟動 OpenSearch Dashboards 容器。
4. 連線至 OpenSearch Dashboards 並檢視 **Dashboards Management** 導覽選單，以確認組態設定已正確設定。側邊欄中會出現 **Data sources**。您會看到類似下圖的畫面。

![Dashboards Management 側邊欄中的 Data sources]({{site.url}}{{site.baseurl}}/images/dashboards/data_sources_management.png){: width="700" }

### 步驟 2：建立新的資料來源連線

資料來源連線會指定連線至資料來源所需的參數。這些參數會組成資料來源的連線字串。

若要建立新的資料來源連線：

1. 在 OpenSearch Dashboards 主選單中，選取 **Dashboards Management** > **Data sources** > **Create data source connection**。

2. 在每個欄位中新增必要資訊，以設定 **Connection Details** 和 **Authentication Method**。

    - 在 **Connection Details** 下，輸入標題和端點 URL。在本教學中，請使用 URL `https://localhost:9200/`。輸入說明為選用。

    - 在 **Authentication Method** 下，從下拉式清單中選取驗證方法。選取驗證方法後，會出現適用於該方法的欄位。接著您可以輸入必要的詳細資料。驗證方法選項如下：
        - **No authentication**：連線至資料來源時不使用任何驗證。
        - **Username & Password**：使用基本的使用者名稱和密碼連線至資料來源。
        - **AWS SigV4**：使用 AWS Signature Version 4 驗證請求連線至資料來源。AWS Signature Version 4 需要存取金鑰和私密金鑰。
            - 若要使用 AWS Signature Version 4 驗證，請先指定 **Region**。接著，從 **Service Name** 清單中選取 OpenSearch 服務。選項為 **Amazon OpenSearch Service** 和 **Amazon OpenSearch Serverless**。最後，輸入用於授權的 **Access Key** 和 **Secret Key**。

      如需 AWS 帳戶可用的 AWS 區域相關資訊，請參閱[可用區域](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-available-regions)。如需 AWS Signature Version 4 驗證請求的詳細資訊，請參閱[驗證請求 (AWS Signature Version 4)](https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-authenticating-requests.html)。
      {: .note}

    - 在所有必要欄位中輸入適當的詳細資料後，**Test connection** 和 **Create data source** 按鈕會變成可用。您可以選取 **Test connection** 以確認連線有效。

3. 選取 **Create data source** 以儲存您的設定。連線建立後，新的資料來源會出現在 **Data Sources** 主頁面的清單中。您建立的第一個資料來源會標示為預設資料來源。

4. 編輯或更新資料來源連線。

    - 在 **Data Sources** 主頁面上，選取您要修改的連線。**Connection Details** 視窗隨即開啟。

    - 若要將所選資料來源標示為預設，請選取 **Set as default** 選項。

    - 若要變更 **Connection Details**，請編輯 **Title** 和 **Description** 欄位的其中之一或兩者，然後選取畫面右下角的 **Save changes**。您也可以在此處取消變更。若要變更 **Authentication Method**，請選擇其他驗證方法，輸入您的認證資訊 (如適用)，然後選取畫面右下角的 **Save changes**。變更隨即儲存。

        - 當所選的驗證方法為 **Username & Password** 時，您可以選擇 **Password** 欄位旁的 **Update stored password** 來更新密碼。在彈出式視窗中，於第一個欄位輸入新密碼，然後在第二個欄位再次輸入以確認。在彈出式視窗中選取 **Update stored password**。新密碼隨即儲存。選取 **Test connection** 以確認連線有效。
        - 當所選的驗證方法為 **AWS SigV4** 時，您可以選取 **Update stored AWS credential** 來更新認證資訊。在彈出式視窗中，於第一個欄位輸入新的存取金鑰，並在第二個欄位輸入新的私密金鑰。在彈出式視窗中選取 **Update stored AWS credential**。新的認證資訊隨即儲存。選取畫面右上角的 **Test connection** 以確認連線有效。

5. 選取標題左側的核取方塊，然後選擇 **Delete 1 connection**，即可刪除資料來源連線。支援為多個連線選取多個核取方塊。或者，您也可以選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/dashboards/trash-can-icon.png" class="inline-icon" alt="trash can icon"/>{:/} (垃圾桶) 圖示。

下圖顯示資料來源連線介面。

![資料來源連線畫面]({{site.url}}{{site.baseurl}}/images/dashboards/data_source_connection.png){: width="700" }

### 透過 Dev Tools 主控台選取多個資料來源

或者，您也可以透過 [Dev Tools]({{site.url}}{{site.baseurl}}/dashboards/dev-tools/index/) 主控台選取多個資料來源。此選項可讓您處理更廣泛的資料，並更深入地了解您的程式碼和應用程式。

請觀看下列 10 秒的影片，了解實際運作方式。

![Dev Tools 中的多個資料來源示範]({{site.url}}{{site.baseurl}}/images/dashboards/multidata-dev-tools.gif)

若要透過 Dev Tools 主控台選取資料來源，請依照下列步驟操作：

1. 找到您的 `opensearch_dashboards.yml` 檔案，並在您選擇的編輯器中開啟。
2. 將 `data_source.enabled` 設為 `true`。
3. 連線至 OpenSearch Dashboards，然後在選單中選取 **Dev Tools**。
4. 在 **Console** 的編輯器窗格中輸入下列查詢，然後選取播放按鈕：

    ```json
    GET /_cat/indices
    ```
    {% include copy-curl.html %}

5. 從 **Data source** 下拉式選單中選取資料來源，然後查詢該來源。
6. 針對您要選取的每個資料來源，重複上述步驟。

---

## 從已連線的資料來源將已儲存物件上傳至儀表板

若要將已連線資料來源中的已儲存物件上傳至具有多個資料來源的儀表板，請從該資料來源的 **Saved object management** 頁面將其匯出為 NDJSON 檔案，接著將該檔案上傳至儀表板的 **Saved object management** 頁面。此方法可簡化已儲存物件在儀表板之間的轉移。以下 20 秒的影片展示此功能的實際運作情形。

![Saved object management 中的多個資料來源]({{site.url}}{{site.baseurl}}/images/dashboards/import_saved_objects_with_file_upload.gif)

### 從已連線的資料來源匯入已儲存物件

請依照下列步驟，從已連線的資料來源匯入已儲存物件：

1. 找到您的 `opensearch_dashboards.yml` 檔案，並以您慣用的文字編輯器開啟。
2. 將 `data_source.enabled` 設為 `true`。
3. 連線至 OpenSearch Dashboards，然後前往 **Dashboards Management** > **Saved objects**。
4. 選取 **Import** > **Select file**，並上傳從已連線資料來源取得的檔案。
5. 從下拉式選單中選擇適當的 **Data source**，設定您的 **Conflict management** 選項，然後選取 **Import** 按鈕。

---

## 顯示或隱藏驗證方法
於 2.13 版推出
{: .label .label-purple }

您可以透過 `opensearch_dashboards.yml` 檔案中的功能旗標，在 `data_source` 外掛程式中顯示或隱藏驗證方法。下列設定會隱藏 `AWSSigV4` 的驗證方法。

````
# Set enabled to false to hide the authentication method from multiple data source in OpenSearch Dashboards.
# If this setting is commented out, then all three options will be available in OpenSearch Dashboards.
# The default value will be considered as true.
data_source.authTypes:
   NoAuthentication:
     enabled: true
   UsernamePassword:
     enabled: true
   AWSSigV4:
     enabled: false
````

以下示範展示此流程。

![多個資料來源隱藏與顯示驗證]({{site.url}}{{site.baseurl}}/images/dashboards/multidata-hide-show-auth.gif)

## 顯示或隱藏本機叢集
於 2.13 版推出
{: .label .label-purple }

您可以透過 `opensearch_dashboards.yml` 檔案中的功能旗標，在 `data_source` 外掛程式中隱藏本機叢集選項。此選項會在資料來源下拉式選單及索引建立頁面中隱藏本機叢集，適用於具有或不具有本機 OpenSearch 叢集的環境。下列範例設定會隱藏本機叢集，如 20 秒示範所示：

````
# hide local cluster in the data source dropdown and index pattern creation page.
data_source.hideLocalCluster: true
````

以下示範展示此流程。

![多個資料來源隱藏本機叢集]({{site.url}}{{site.baseurl}}/images/dashboards/multidata-hide-localcluster.gif)

---

## 搭配外部儀表板外掛程式使用多個資料來源
於 2.14 版推出
{: .label .label-purple}

下列外掛程式現已支援多個資料來源。

### 索引管理

設定 `data_source.enabled:true` 後，您可以直接從介面檢視並選取資料來源及其相關聯的索引：

1. 在主選單下前往 **Management** > **Index Management**。
2. 從側邊欄選單中選取 **Indexes**，然後選取右上方選單列上的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/database-icon.png" class="inline-icon" alt="database icon"/>{:/}（資料庫）圖示。
3. 從下拉式選單中選擇適當的資料來源，然後從清單中選擇適當的索引。預設會顯示您預設資料來源中的索引。您可以選擇任何已連線的資料來源，以檢視其對應的索引。

下列 GIF 說明這些步驟。

![ISM 清單頁面中的多個資料來源]({{site.url}}{{site.baseurl}}/images/dashboards/ism_mds1.gif)

若要對資料來源中的特定索引執行操作，請從清單中選取該索引。若要建立新索引，請選取 **Create Index** 按鈕以開啟表單。輸入必要資訊，然後選取 **Create** 按鈕。索引會建立在所選的資料來源中。下列 GIF 說明這些步驟。

![ISM 建立頁面中的多個資料來源]({{site.url}}{{site.baseurl}}/images/dashboards/ism_mds2.gif)

### 異常偵測

設定 `data_source.enabled:true` 後，您可以建立或檢視與資料來源相關聯的偵測器：

1. 在主選單下前往 **OpenSearch Plugins** > **Anomaly Detection**。
2. 選取右上方選單列上的資料庫圖示，以檢視已連線資料來源的清單。
3. 選取資料來源，以檢視相關聯偵測器的清單。如果所選的資料來源沒有偵測器，右上方選單列下方會出現 **Create detector** 按鈕。如需透過介面建立偵測器的說明，請參閱[建立異常偵測器]({{site.url}}{{site.baseurl}}/observing-your-data/ad/dashboards-anomaly-detection/#creating-anomaly-detectors)。

下列 GIF 說明這些步驟。

![異常偵測儀表板頁面中的多個資料來源]({{site.url}}{{site.baseurl}}/images/dashboards/ad_mds1.gif)

您可以在左側邊欄下的 **Detectors** 索引標籤中，編輯與資料來源相關聯的偵測器。

1. 選取 **Detectors**，然後選取右上方選單列上的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/database-icon.png" class="inline-icon" alt="database icon"/>{:/}（資料庫）圖示。
2. 從下拉式選單中選取適當的資料來源。畫面會顯示相關聯偵測器的清單。
3. 從清單中選擇偵測器，選取 **Actions**，然後從下拉式選單中選擇適當的編輯選項。
4. 輸入適用的設定與組態詳細資料。

下列 GIF 說明這些步驟。

![異常偵測偵測器頁面中的多個資料來源]({{site.url}}{{site.baseurl}}/images/dashboards/ad_mds2.gif)

### 安全性

設定 `data_source.enabled:true` 後，您可以檢視並管理每個已連線資料來源的角色：

1. 在主選單下前往 **Management** > **Security**。
2. 從左側邊欄選單中選取 **Roles**，然後選取右上方選單列上的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/database-icon.png" class="inline-icon" alt="database icon"/>{:/}（資料庫）圖示。
3. 從下拉式選單中選取適當的資料來源，然後選取 **Create role** 按鈕以新增角色。
4. 輸入必要的組態資訊，然後選取 **Create** 按鈕以儲存。

下列 GIF 說明這些步驟。

![Security 外掛程式中的多個資料來源]({{site.url}}{{site.baseurl}}/images/dashboards/security_mds1.gif)

### 地圖

設定 `data_source.enabled:true` 後，您可以在地圖中檢視所有可用的資料來源，包括目前用作圖層的資料來源：

1. 在主選單下前往 **OpenSearch Plugins** > **Maps**。
2. 從下拉式選單中選取適當的資料來源，以編輯或建立相關聯的地圖圖層：
  - 從 **Layers** 下拉式選單中選取圖層以進行編輯。在快顯視窗中檢視設定，並視需要加以編輯。
  - 從下拉式選單中選取 **Add layer** 按鈕，然後在快顯視窗中選取 **Documents**，即可新增圖層。右側會出現另一個快顯視窗。在 **Data** 索引標籤中輸入必要資訊。請注意，資料來源名稱會加在索引模式名稱前面作為前綴。**Style** 和 **Settings** 索引標籤包含選用資訊。
  - 選取 **Update** 以儲存設定。
3. 選取選單列上的 **Save** 按鈕，以儲存已編輯或新增的圖層。
4. 選取右上方選單列上的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/database-icon.png" class="inline-icon" alt="database icon"/>{:/} 圖示，確認新的資料來源已列在下拉式選單中。

下列 GIF 說明這些步驟。

![Maps 外掛程式中的多個資料來源]({{site.url}}{{site.baseurl}}/images/dashboards/maps_mds1.gif)

### 機器學習

當您設定 `data_source.enabled:true` 時，即可檢視及管理來自不同已連線資料來源的機器學習模型：

1. 在主選單中前往 **OpenSearch Plugins** > **Machine Learning**。
2. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/database-icon.png" class="inline-icon" alt="database icon"/>{:/} 圖示，然後從下拉式選單中選擇資料來源。畫面上會顯示與所選資料來源相關聯的模型清單。
3. 選取清單中模型右側的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/inspect-icon.png" class="inline-icon" alt="inspect icon"/>{:/} 圖示，即可檢視該模型在所選資料來源中的組態詳細資訊。

下列 GIF 示範了這些步驟。

![機器學習外掛程式中的多個資料來源]({{site.url}}{{site.baseurl}}/images/dashboards/ml_mds1.gif)

### 通知

當您設定 `data_source.enabled:true` 時，即可檢視及管理不同資料來源的通知管道：

1. 在主選單中前往 **Management** > **Notifications**。
2. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/database-icon.png" class="inline-icon" alt="database icon"/>{:/} 圖示，然後從下拉式選單中選擇資料來源。畫面上會顯示與所選資料來源相關聯的管道清單。
3. 從清單中選擇一個管道，以檢視或管理其設定。
  - 若要編輯管道的設定，請選取 **Actions** 按鈕並選擇 **Edit** 選項。在 **Edit channel** 面板中輸入必要資訊，然後選擇 **Save**。
  - 若要傳送測試訊息至管道，請在 **Edit channel** 視窗中選取 **Send test message** 按鈕。或者，您也可以在管道詳細資訊視窗中選取 **Actions** 按鈕，然後從下拉式選單中選擇 **Send test message** 選項。

下列 GIF 示範了這些步驟。

![通知外掛程式中的多個資料來源]({{site.url}}{{site.baseurl}}/images/dashboards/notification_mds1.gif)

### 搜尋相關性

當您設定 `data_source.enabled:true` 時，即可比較來自不同資料來源之索引的搜尋結果：

1. 在主選單中前往 **OpenSearch Plugins** > **Search Relevance**。
2. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/database-icon.png" class="inline-icon" alt="database icon"/>{:/} 圖示，然後從下拉式選單中選擇資料來源。畫面上會顯示可用資料來源的清單。
3. 在 **Query 1** 和 **Query 2** 下方，分別選取資料來源和索引。
4. 選取 **Search** 按鈕以執行查詢。查詢結果會顯示在各自的結果面板中。

下列 GIF 示範了這些步驟。

![搜尋相關性外掛程式中的多個資料來源]({{site.url}}{{site.baseurl}}/images/dashboards/searchrelevance_mds1.gif)

### Security Analytics
於 2.15 版推出
{: .label .label-purple}

當您設定 `data_source.enabled:true` 時，即可跨多個已連線的資料來源檢視及管理 Security Analytics 資源，例如偵測規則：

1. 在主選單中前往 **OpenSearch Plugins** > **Security Analytics**。
2. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/database-icon.png" class="inline-icon" alt="database icon"/>{:/} 圖示，然後從下拉式選單中選擇資料來源。
3. 從左側導覽選單中選取 **Detectors** > **Detection rules**。畫面上會顯示偵測規則清單。
4. 選取一條規則，以開啟包含該規則詳細資訊的快顯視窗。

下列 GIF 示範了這些步驟。

![Security Analytics 清單頁面中的多個資料來源]({{site.url}}{{site.baseurl}}/images/dashboards/mds_sa_detection_rules_view.gif)

1. 在主選單中前往 **OpenSearch Plugins** > **Security analytics**。
2. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/database-icon.png" class="inline-icon" alt="database icon"/>{:/} 圖示，然後從下拉式選單中選擇資料來源。
3. 從左側導覽選單中選取 **Detectors** > **Detection rules**。
4. 選取右上方的 **Create detection rule** 按鈕，然後在 **Create detection rule** 視窗中輸入必要的組態詳細資訊。
5. 選取右下方的 **Create detection rule** 按鈕以儲存規則。該規則現在已與資料來源相關聯。

下列 GIF 示範了這些步驟。

![Security Analytics 建立頁面中的多個資料來源]({{site.url}}{{site.baseurl}}/images/dashboards/mds_sa_detection_rules_create.gif)

### 警示
於 2.15 版推出
{: .label .label-purple }

當您設定 `data_source.enabled:true` 時，即可跨多個已連線的資料來源檢視及管理警示監視器：

1. 在主選單中前往 **OpenSearch Plugins** > **Alerting**。
2. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/database-icon.png" class="inline-icon" alt="database icon"/>{:/} 圖示，然後從下拉式選單中選擇資料來源。畫面上會顯示相關聯的監視器清單。
3. 選取一個監視器以檢視其詳細資訊。

下列 GIF 示範了這些步驟。

![警示清單頁面中的多個資料來源]({{site.url}}{{site.baseurl}}/images/dashboards/mds_monitor_view.gif)

若要建立新的監視器，請選取 **Create monitor**。填寫表單後選取 **Create**。監視器會建立在所選的資料來源中。

#### 從 Dashboards 應用程式中管理警示監視器

若要從 **Dashboards** 中管理資料來源監視器：

1. 在主選單中前往 **Dashboards** 應用程式，然後從清單中選取一個儀表板。
2. 在儀表板中，選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/ellipsis-icon.png" class="inline-icon" alt="ellipsis icon"/>{:/}（省略符號）圖示以開啟 **Options** 下拉式選單，然後選擇 **Alerting**。
4. 從 **Alerting** 下拉式選單中選擇 **Associated monitors**，以開啟組態視窗。
5. 從清單中選取一個監視器，以檢視或編輯其詳細資訊。

下列 GIF 示範了這些步驟。

![搭配 Feature anywhere 相關聯監視器的多個資料來源]({{site.url}}{{site.baseurl}}/images/dashboards/mds_feature_anywhere_view_alerting.gif)

若要將監視器與資料來源建立關聯：

1. 在主選單中前往 **Dashboards** 應用程式，然後從清單中選取一個儀表板。
2. 在儀表板中，選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/ellipsis-icon.png" class="inline-icon" alt="ellipsis icon"/>{:/}（省略符號）圖示以開啟 **Options** 下拉式選單，然後選擇 **Alerting**。
3. 從 **Alerting** 下拉式選單中選擇 **Add alerting monitor**，以開啟組態視窗。
4. 輸入組態資訊，然後選取 **Create monitor** 按鈕。該監視器現在已與資料來源相關聯。

下列 GIF 示範了這些步驟。

![搭配 Feature anywhere 新增相關聯監視器的多個資料來源]({{site.url}}{{site.baseurl}}/images/dashboards/mds_feature_anywhere_create_alerting.gif)

---

## 後續步驟

設定多個資料來源後，您可以分析來自每個來源的資料。如需詳細資訊，請參閱下列資源：

- [索引模式]({{site.url}}{{site.baseurl}}/dashboards/management/index-patterns/) 
- [索引管理]({{site.url}}{{site.baseurl}}/dashboards/im-dashboards/index/)
- [透過 OpenSearch Dashboards 連接 OpenSearch 與 Amazon S3]({{site.url}}{{site.baseurl}}/dashboards/management/S3-data-source/)
- [OpenSearch 整合]({{site.url}}{{site.baseurl}}/integrations/index/)
