---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "入門"
parent: Threat intelligence
nav_order: 41
---

# 威脅情報入門

若要開始使用威脅情報，您需要設定威脅情報來源，並設定監視器來掃描您的記錄來源。下列教學將說明如何透過 OpenSearch Dashboards 開始使用。您也可以使用 [API]({{site.url}}{{site.baseurl}}/security-analytics/threat-intelligence/api/threat-intel-api/)。

## 威脅情報檢視

若要存取威脅情報，請登入 OpenSearch Dashboards，然後選取 **Security Analytics** > **Threat Intelligence**。

在威脅情報檢視中，您可以存取下列分頁：

- **Threat intel sources**：顯示所有作用中與非作用中威脅情報來源的清單，包括預設的 IP 信譽資料來源 [AlienVault OTX](https://otx.alienvault.com/)，此資料來源在下載 OpenSearch 時已預先封裝。
- **Scan configuration**：顯示掃描組態的概觀，包括已設定的 **Log sources**、**Scan schedule** 與 **Alert triggers**。從 **Actions** 下拉式清單中，您也可以 **Stop scan**、**Edit scan configuration** 或 **Delete scan configuration**。


## 步驟 1：設定威脅情報來源

若要新增威脅情報來源，請在威脅情報頁面選取 **Add threat intel source**。此時會出現 **Add custom threat intelligence source** 頁面。

在威脅情報來源頁面上，新增下列資訊：

- **Name**：來源的名稱。
- **Description**：來源的選用描述。
- **Threat intel source type**：來源類型決定 `STIX2` 檔案的儲存位置。您可以選擇下列其中一個選項：
  - **Remote data store location**：連線至自訂資料儲存區。唯一支援的類型是 `S3_SOURCE`。此設定也讓您能夠設定下載排程，讓 OpenSearch 從資料儲存區下載最新的 `STIX2` 檔案。如需更多資訊，請參閱 [S3_SOURCE 連線詳細資訊](#s3_source-connection-information)。
  - **Local file upload**：上傳自訂的威脅情報 IOC 檔案。自訂檔案無法依排程下載，必須手動上傳才能更新 IOC。如需更多資訊，請參閱 [本機檔案上傳](#local-file-upload)。
- **Types of malicious indicators**：決定要從 `STIX2` 檔案擷取的惡意 IOC 類型。支援下列 IOC：
  - IPv4-Address
  - IPv6-Address
  - Domains
  - File hash

輸入所有相關資訊後，選取 **Add threat intel source**。

### 本機檔案上傳

上傳作為威脅情報來源的本機檔案必須符合下列規格：

- 以 `STIX2` 格式上傳為 JSON 檔案。若需範例 `STIX2` 檔案，請下載 [此檔案]({{site.url}}{{site.baseurl}}/assets/examples/all-ioc-type-examples.json)，其中包含所有支援 IOC 類型的範例格式。
- 檔案大小必須小於 500 kB。


<!-- vale off -->
### S3_SOURCE 連線資訊
<!-- vale on -->

使用 `S3_SOURCE` 作為遠端儲存區時，必須提供下列連線資訊：

- **IAM Role ARN**：AWS Identity and Access Management (IAM) 角色的 Amazon Resource Name (ARN)。使用 AWS OpenSearch Service 時，角色 ARN 必須與 OpenSearch 網域位於同一個帳戶中。如需為 AWS OpenSearch Service 新增角色的更多資訊，請參閱 [新增服務 ARN](#add-aws-opensearch-service-arn)。
- **S3 bucket directory**：儲存 `STIX2` 檔案的 Amazon Simple Storage Service (Amazon S3) 儲存貯體名稱。若要存取不同 AWS 帳戶中的 S3 儲存貯體，請參閱 [跨帳戶 S3 儲存貯體連線](#cross-account-s3-bucket-connection) 一節以取得更多詳細資訊。
- **Specify a file**：S3 儲存貯體中 `STIX2` 檔案的物件金鑰。
- **Region**：S3 儲存貯體所在的 AWS 區域。

您也可以設定 **Download schedule**，決定 OpenSearch 何時從連線的 S3 儲存貯體下載更新的 `STIX2` 檔案。預設間隔為每天一次。僅支援每日間隔。

或者，您可以勾選 **Download on demand** 選項，以防止自動下載儲存貯體中的新資料。

<!-- vale off -->
#### 新增 AWS OpenSearch Service ARN
<!-- vale on -->

如果您使用 AWS OpenSearch Service，請以自訂信任政策建立新的 ARN 角色。如需建立角色的說明，請參閱 [為 AWS 服務建立角色](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html#roles-creatingrole-service-console)。

建立角色時，請自訂下列設定：

- 新增下列自訂信任政策：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "opensearchservice.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```
      
- 在 Permissions policies 頁面上，新增 `AmazonS3ReadOnlyAccess` 權限。


#### 跨帳戶 S3 儲存貯體連線

由於角色 ARN 必須與 OpenSearch 網域位於同一個帳戶中，因此需要設定信任政策，允許 OpenSearch 網域從同一帳戶的 S3 儲存貯體下載。

若要從另一個帳戶的 S3 儲存貯體下載，該儲存貯體的信任政策必須授予角色 ARN 讀取物件的權限，如下列範例所示：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:role/account-1-threat-intel-role"
      },
      "Action": "s3:*",
      "Resource": "arn:aws:s3:::account-2-threat-intel-bucket/*"
    }
  ]
}
```

## 步驟 2：為您的記錄來源設定掃描

您可以設定威脅情報監視器來掃描您的別名與資料串流。監視器會掃描新匯入索引的資料，並將該資料與威脅情報來源中存在的任何 IOC 進行比對。掃描會套用至新增到 OpenSearch 的所有威脅情報來源。預設情況下，掃描每分鐘執行一次。

若要新增或編輯掃描組態：

1. 從威脅情報檢視中，選取 **Add scan configuration** 或 **Edit scan configuration**。
2. 選取要掃描的索引或別名。
3. 依據 IOC 類型，從您的索引或別名中選取要掃描的 **欄位**。例如，若別名有兩個名為 `src_ip` 與 `dst_ip` 的欄位包含 `ipv4` 位址，則這些欄位必須輸入到監視器請求的 `ipv4-addr` 區段中。
4. 為指定的索引或別名決定 **Scan schedule**。預設情況下，OpenSearch 每分鐘掃描一次 IOC。
5. 設定警示觸發器及其觸發條件。您可以新增多個觸發器：
   1. 為觸發器新增名稱。
   2. 選擇指標類型。指標類型會與 IOC 類型相符。
   3. 選取警示的嚴重性。
   4. 選取是否在觸發警示時傳送通知。啟用後，您可以自訂通知傳送至哪些頻道以及通知訊息。通知訊息可以使用 [Mustache 範本](https://mustache.github.io/mustache.5.html) 自訂。
6. 輸入所有設定後，選取 **Save and start monitoring**。

當發現惡意 IOC 時，OpenSearch 會建立 **findings**，提供有關該威脅的資訊。您也可以設定觸發器來建立警示，將通知傳送至已設定的 webhook 或端點。


## 檢視警示與發現

您可以檢視由威脅情報監視器產生的警示與發現，以分析安全性記錄檔中出現了哪些惡意指標。若要檢視警示或發現，請從威脅情報檢視中選取 **View findings** 或 **View alerts**。
