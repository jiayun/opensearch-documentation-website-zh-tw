---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在 Amazon OpenSearch Service 中收集 UBI 格式的資料"
parent: User Behavior Insights
grand_parent: Optimizing search quality
has_children: false
nav_order: 30
---


# 在 Amazon OpenSearch Service 中收集 UBI 格式的資料

本教學說明如何在使用 Amazon OpenSearch Service 時，以 User Behavior Insights (UBI) 格式收集查詢與事件。

原生 UBI 外掛程式僅適用於開源 OpenSearch 發行版本，並不包含在 Amazon OpenSearch Service 中。如果您使用的是 OpenSearch Service，並且想實作 UBI 風格的資料收集，本教學將示範一種替代做法。
{: .important}

完成本教學後，您將能夠使用 `curl` 命令列工具，將已驗證的查詢與事件傳送至 Amazon Simple Storage Service (Amazon S3) 進行長期儲存，並傳送至 OpenSearch 進行即時處理。

本教學假設以下條件：

1. 您正在使用 Amazon OpenSearch Service。
2. 您並未使用 OpenSearch 的 UBI 外掛程式。UBI 外掛程式僅適用於開源版本的 OpenSearch，並未包含在 Amazon OpenSearch Service 中。
3. 您正在使用 [Amazon OpenSearch Ingestion](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ingestion.html)（OpenSearch Data Prepper 的受管版本）將 UBI 資料寫入 OpenSearch。
4. 您已依照 [教學：使用 Amazon OpenSearch Ingestion 將資料匯入網域](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/osis-get-started.html) 中的指示（特別是 *必要權限* 步驟），設定了 OpenSearch Ingestion 與受管叢集之間的權限。

## 步驟 1：為 UBI 設定 OpenSearch 索引

請依照下列步驟建立 UBI 資料所需的索引：

1. 登入 Amazon OpenSearch Service 中的 OpenSearch Dashboards。
1. 在主選單中選取 **Management > Dev Tools**，開啟 **Dev Tools** 主控台。
1. 建立兩個新索引：`ubi_events` 與 `ubi_queries`。

    1. 首先，開始建立 `ubi_events` 索引的對應：

        ```json
        PUT /ubi_events
        {
          "mappings": 
        }
        ```

        此時會出現語法警告。這是預期行為；您接下來會輸入對應。

        開啟 [events-mapping.json](https://github.com/opensearch-project/user-behavior-insights/blob/main/src/main/resources/events-mapping.json) 檔案，複製其內容，並貼到 `"mappings":` 行之後：

        ```json
        PUT ubi_events
        {
          "mappings": {
            "properties": {
              "application": {
                "type": "keyword",
                "ignore_above": 256
              },
              "action_name": {
                "type": "keyword",
                "ignore_above": 100
              },
              ...
            }
          }
        }
        ```

        執行該命令並確認成功。

    1. 接著，以類似方式建立 `ubi_queries` 索引。設定對應：

        ```json
        PUT ubi_queries
        {
          "mappings": 
        }
        ```

        開啟 [queries-mapping.json](https://github.com/opensearch-project/user-behavior-insights/blob/main/src/main/resources/queries-mapping.json?utm_source=chatgpt.com) 檔案，複製其內容，並貼到 `"mappings":` 行之後。執行該命令並確認成功。

## 步驟 2：設定 Amazon S3 儲存

若要長期儲存 UBI 資料，請使用 Amazon S3。

在繼續之前，請先建立一個 S3 儲存貯體，用於儲存查詢與事件資料。您可以在 AWS Management Console 中執行此操作。請記下儲存貯體名稱及其建立的 AWS 區域；後續步驟將需要這些資訊。

## 步驟 3：設定查詢與事件的資料匯入管線

請依照下列步驟設定查詢與事件的資料匯入管線。

### 必要權限

若要完成本教學，您的使用者或角色必須附加具有下列最低權限的身分型政策。這些權限可讓您建立管線角色並附加政策（`iam:Create*` 與 `iam:Attach*`）、建立或修改網域（`es:*`），以及使用管線（`osis:*`）：

```json
{
   "Version":"2012-10-17",
   "Statement":[
      {
         "Effect":"Allow",
         "Resource":"*",
         "Action":[
            "osis:*",
            "iam:Create*",
            "iam:Attach*",
            "es:*"
         ]
      },
      {
         "Resource":[
            "arn:aws:iam::111122223333:role/OpenSearchIngestion-PipelineRole"
         ],
         "Effect":"Allow",
         "Action":[
            "iam:CreateRole",
            "iam:AttachRolePolicy",
            "iam:PassRole"
         ]
      }
   ]
}
```
{% include copy.html %}

您的 `DataPrepperOpenSearchRole` 必須具有類似下列的權限：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "es:ESHttpPost",
                "es:ESHttpPut",
                "es:ESHttpGet",
                "es:ESHttpHead"
            ],
            "Resource": "arn:aws:es:*:<YOUR_AWS_ACCOUNT_NUMBER>:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::<YOUR-BUCKET>/*"
        }
    ]
}
```
{% include copy.html %}

### 步驟 3(a)：建立查詢管線

請依照下列步驟建立 UBI 查詢資料的管線：

1. 在 Amazon OpenSearch Service 主控台中，從左側導覽窗格選取 **Pipelines**。
1. 選取 **Create pipeline**。
1. 選取 **Blank** 管線，然後選取 **Select blueprint**。
1. 將管線設定為使用 **HTTP** 來源外掛程式，該外掛程式接受 JSON 陣列格式的 UBI 查詢資料。將 OpenSearch Service 網域設為接收端 (sink)，將所有資料導入 `ubi_queries` 索引。此外，將所有事件以 `.ndjson` 格式記錄到 S3 儲存貯體。
1. 在 **Source** 選單中，選取 **HTTP**。在 **Path** 中輸入 `/ubi/queries`。
1. 在 **Source network options** 中，選取 **Public access**，以允許從您的應用程式張貼資料。
1. 選取 **Next**。
1. 在 **Processor** 畫面上選取 **Next**，略過中間的 **Processor** 步驟。
1. 設定第一個接收端：
   * 在 **OpenSearch resource type** 中，選取 **Managed cluster**。
   * 選取您稍早建立的 OpenSearch Service 網域。
   * 在 **Index name** 中輸入 `ubi_queries`。請確認此索引已存在且具備必要的 UBI 結構描述。
1. 設定第二個接收端：
    * 選取 **Add Sink**。
    * 選取 **Amazon S3**。
    * 輸入您先前建立的儲存貯體名稱與 AWS 區域。
    * 在 **Event Collection Timeout** 中輸入 `60s`，以便快速觀察資料流。
    * 選取 **NDJSON** 作為格式。
1. 選取 **Next**。
1. 將管線命名為 `ubi-queries-pipeline`，並將容量設定保留為預設值。
1. 選取 **Next**，然後選取 **Create Pipeline**。

### 步驟 3(b)：測試查詢管線

當管線狀態為 `Active` 時，您就可以開始將資料匯入其中。您必須使用 [AWS Signature Version 4](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html) 對所有傳送至管線的 HTTP 請求進行簽署。請使用 [Postman](https://www.getpostman.com/) 或 [`awscurl`](https://github.com/okigan/awscurl) 等 HTTP 工具，將一些資料傳送至管線。如同直接將資料編製索引至網域一樣，將資料匯入管線一律需要 AWS Identity and Access Management (IAM) 角色或 [IAM 存取金鑰與私密金鑰](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html)。

若要測試管線，請依照下列步驟：

1. 從 **Pipeline settings** 頁面取得匯入 URL，如下圖所示。

    ![Pipeline Settings]({{site.url}}{{site.baseurl}}/images/ubi/opensearch-ingestion-pipeline.png "Pipeline Settings")

1. 將 UBI 查詢張貼至資料匯入管線。以下是使用 [`awscurl`](https://github.com/okigan/awscurl) 張貼查詢的範例：

    ```bash
    awscurl --service osis --region us-east-1 \
        -X POST \
        -H "Content-Type: application/json" \
        -d '[{
        "query_response_id": "117d75fb-ea76-41dc-9d1d-1d7bba548bd8",
        "user_query": "laptop",
        "query_id": "d194b734-70a4-41dc-b103-b26a56a277b5",
        "application": "Chorus",
        "query_response_hit_ids": [
          "B076YX2LML",
          "B07S3T59VP",
          "B075ZGJSL1",
          "B07FMGGRGG",
          "B07KN5JP3H",
          "B07FM8BNBC",
          "B007OYLNGA",
          "B07P75NDMB",
          "B004HJ1ZB8",
          "B01M69KU15",
          "B072ZW6NBL",
          "B07R7NL612",
          "B083GH3L2N",
          "B06XNQDR8J",
          "B07ZQJQ4HV",
          "B07YZHH5WY",
          "B07F822FND",
          "B004XAVT8K",
          "B07F5JN761",
          "B087RNZT41"
        ],
        "query_attributes": {},
        "client_id": "CLIENT-9a9968ac-664b-42d7-9a9e-96f412b5ab49",
        "timestamp": "2025-01-23T13:18:22.274+0000"
      }]' \
    https://ubi-queries-pipeline-il3g3pwe4ve4nov4bwhnzlrm4q.us-east-1.osis.amazonaws.com/ubi/queries
    ```
    {% include copy.html %}

    您應該會收到 `200 OK` 回應。

1. 使用 Dev Tools 主控台查詢您張貼的事件資料。請注意，資料可能需要一些時間才能透過 OpenSearch Ingestion 流入 `ubi_queries` 索引：

    ```json
    GET /ubi_queries/_search
    {
      "query": {
        "match_all": {}
      },
      "sort": [
        { "timestamp": { "order": "desc" } }
      ]
    }
    ```
    {% include copy-curl.html %}

    如果您希望新寫入的資料立即顯示，請執行下列請求：

    ```json
    POST /ubi_queries/_refresh
    ```
    {% include copy-curl.html %}

### 步驟 3(c)：建立事件管線

重複 [步驟 3(a)](#step-3a-create-a-query-pipeline) 來設定 UBI 事件資料的管線。請使用下表將查詢專屬的值替換為對應的事件值。

| 設定                  | 查詢管線           | 事件管線           |
|--------------------------|------------------------|------------------------|
| 路徑                     | `/ubi/queries`         | `/ubi/events`          |
| 索引名稱               | `ubi_queries`          | `ubi_events`           |
| 管線名稱            | `ubi-queries-pipeline` | `ubi-events-pipeline`  |
| S3 路徑前置詞模式   | `ubi_queries/`         | `ubi_events/`          |
| Dev Tools 搜尋         | `GET ubi_queries/_search` | `GET ubi_events/_search` |
| 重新整理命令          | `POST ubi_queries/_refresh` | `POST ubi_events/_refresh` |

### 步驟 3(d)：測試事件管線

依照 [步驟 3(b)](#step-3b-test-the-query-pipeline) 測試事件管線。以下是使用 [`awscurl`](https://github.com/okigan/awscurl) 張貼查詢的範例：

```bash
awscurl --service osis --region us-east-1 \
    -X POST \
    -H "Content-Type: application/json" \
    -d '[
  {
    "action_name": "product_hover",
    "client_id": "CLIENT-9a9968ac-664b-42d7-9a9e-96f412b5ab49",
    "query_id": "d194b734-70a4-41dc-b103-b26a56a277b5",
    "page_id": "/",
    "message_type": "INFO",
    "message": "Integral 2GB SD Card memory card (undefined)",
    "timestamp": 1724944081669,
    "event_attributes": {
      "object": {
        "object_id_field": "product",
        "object_id": "1625640",
        "description": "Integral 2GB SD Card memory card",
        "object_detail": null
      }
    }
  }
]
' \
https://ubi-events-pipeline-il3g3pwe4ve4nov4bwhnzlrm4q.us-east-1.osis.amazonaws.com/ubi/events
```
{% include copy.html %}

現在您可以開始為您的應用程式收集 UBI 資料了。
