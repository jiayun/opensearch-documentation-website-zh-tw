---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 AWS Lambda 排程報告"
nav_order: 30
parent: Reporting using the CLI
grand_parent: Reporting
redirect_from:
  - /reporting/rep-cli-lambda/
  - /dashboards/reporting-cli/rep-cli-lambda/
---

<!-- vale off -->
# 使用 AWS Lambda 排程報告
<!-- vale on -->

使用 AWS Lambda 依觸發條件（例如排程）執行 Reporting CLI。Lambda 函式會從容器映像執行 Reporting CLI，因此您所產生報告的 OpenSearch Dashboards URL 必須可從 Lambda 函式連線。

容器映像會安裝僅適用於 x86-64 架構的 Google Chrome 相依套件。若要建置映像，您需要 Docker。在架構不同的電腦上（例如搭載 Apple 晶片的 Mac），請使用 `--platform linux/amd64` 選項建置映像。

### 必要條件

若要將 Reporting CLI 與 AWS Lambda 搭配使用，您需要先完成以下前置步驟。

- 取得 AWS 帳戶。相關說明請參閱 AWS Account Management 參考指南中的 [建立 AWS 帳戶](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-creating.html)。
- 設定 Amazon Elastic Container Registry (ECR)。相關說明請參閱 [使用 AWS Management Console 開始使用 Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-console.html)。

## 步驟 1：使用 Dockerfile 建立容器映像

您需要透過執行 Dockerfile 來組建容器映像。執行 Dockerfile 時，它會下載使用 Reporting CLI 所需的 OpenSearch 成品。若要進一步了解 Dockerfile，請參閱 [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)。

將下列範例組態複製到 Dockerfile 中：

```dockerfile
# Define function directory
ARG FUNCTION_DIR="/function"

# Base image of the docker container
FROM node:lts-slim AS build-image

# Include global arg in this stage of the build
ARG FUNCTION_DIR

# AWS Lambda runtime dependencies
RUN apt-get update && \
    apt-get install -y \
        g++ \
        make \
        unzip \
        libcurl4-openssl-dev \
        autoconf \
        automake \
        libtool \
        cmake \
        python3 \
        libkrb5-dev \
        curl

# Copy function code
WORKDIR ${FUNCTION_DIR}
RUN npm install @opensearch-project/reporting-cli && npm install aws-lambda-ric

# Build Stage 2: Copy Build Stage 1 files in to Stage 2. Install chrome, then remove chrome to keep the dependencies.
FROM node:lts-slim
# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}
# Copy in the build image dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# Install latest chrome dev package and fonts to support major char sets (Chinese, Japanese, Arabic, Hebrew, Thai and a few others)
# Note: this installs the necessary libs to make the bundled version of Chromium that Puppeteer installs, work.
RUN apt-get update \
    && apt-get install -y wget gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 \
      --no-install-recommends \
    && apt-get remove -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/usr/local/bin/npx", "aws-lambda-ric"]

ENV HOME="/tmp"
CMD [ "/function/node_modules/@opensearch-project/reporting-cli/src/index.handler" ]

```

接著，在包含 Dockerfile 的同一個目錄中執行以下建置命令：

```bash
docker build --platform linux/amd64 -t opensearch-reporting-cli .
```
{% include copy.html %}

## 步驟 2：使用 Amazon ECR 建立私有儲存庫

您需要依照說明建立映像儲存庫，請參閱 [使用 AWS Management Console 開始使用 Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-console.html)。

將您的儲存庫命名為 `opensearch-reporting-cli`。

除了 Amazon ECR 的說明之外，您還需要進行幾項調整，讓 Reporting CLI 能正常運作，詳情請參閱本程序中的後續步驟。

## 步驟 3：將映像推送至私有儲存庫

您需要從 AWS ECR 主控台取得數個命令，並在 Dockerfile 目錄中執行。

1. 建立儲存庫後，從 **Private repositories** 中選取它。
1. 選擇 **view push commands**。
1. 在 Dockerfile 目錄中，依序複製並執行 **Push commands for `opensearch-reporting-cli`** 中顯示的每個命令。

如需 Docker 推送命令的更多詳細資訊，請參閱 Amazon ECR 使用者指南中的 [推送 Docker 映像](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html)。

## 步驟 4：使用容器映像檔建立 Lambda 函式

現在您已為 Reporting CLI 建立容器映像檔，接著需要建立以該容器映像檔定義的函式。

1. 開啟 AWS Lambda 主控台，然後選擇 [Functions](https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions)。
1. 選擇 **Create function**，接著選擇 **Container image**，並填入函式名稱。
1. 在 **Container image URI** 中，選擇 **Browse images**，並選取 `opensearch-reporting-cli` 作為映像檔儲存庫。
1. 在 **Images** 中選取映像檔，然後選擇 **Select image**。
1. 在 **Architecture** 中，選擇 **x86_64**。
1. 選擇 **Create function**。
1. 前往 **Lambda** > **functions**，然後選擇您建立的函式。
1. 選擇 **Configuration > General configuration > Edit timeout**，並將 Lambda 的逾時設定為 5 分鐘，讓 Reporting CLI 有足夠時間產生報告。
1. 將 **Ephemeral storage** 設定變更為至少 1024 MB。預設設定的儲存空間不足以支援報告產生。
1. 在 JSON 測試事件中或以 Lambda 環境變數的方式提供值，以測試函式。

若要提供每次執行都相同的值（例如電子郵件地址），請在 Lambda 函式組態中設定對應的環境變數，例如 `OPENSEARCH_FROM` 和 `OPENSEARCH_TO`。若要在測試事件或觸發酬載中提供值，請使用不含前置破折號的完整選項名稱作為 JSON 鍵，例如 `url`、`format`、`transport`、`from` 和 `to`。對於 `credentials` 鍵，請以 `<username>:<password>` 格式指定值。如需選項與環境變數的清單，請參閱 [Reporting CLI 選項]({{site.url}}{{site.baseurl}}/dashboards/reporting/rep-cli-options/)。

下列範例事件指定了 URL、電子郵件傳輸方式、寄件者與收件者電子郵件地址，以及電子郵件主旨：

```json
{
  "url": "https://playground.opensearch.org/app/dashboards#/view/084aed50-6f48-11ed-a3d5-1ddbf0afc873",
  "transport": "ses",
  "from": "sender@example.com",
  "to": "recipient@example.com",
  "subject": "Test lambda docker image"
}
```

Lambda 函式會將報告儲存在函式的 `/tmp` 目錄中，因此請指定電子郵件傳輸方式以接收報告。

若要進一步了解 AWS Lambda 函式，請參閱 AWS Lambda 文件中的[將 Lambda 函式部署為容器映像檔](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-images.html)。

## 步驟 5：新增觸發條件以啟動 AWS Lambda 函式

設定啟動報告的觸發條件。AWS Lambda 可以使用其他 AWS 服務作為觸發條件，例如 Amazon Simple Notification Service (Amazon SNS)、Amazon S3 或 Amazon EventBridge。

1. 在 **Triggers** 區段中，選擇 **Add trigger**。
1. 從清單中選取觸發條件。若要依排程產生報告，請使用 Amazon EventBridge 排程。如需詳細資訊，請參閱 AWS Lambda 文件中的[依排程叫用 Lambda 函式](https://docs.aws.amazon.com/lambda/latest/dg/with-eventbridge-scheduler.html)。
1. 選擇 **Test** 以啟動函式。

## （選用）步驟 6：新增 Amazon SES 的角色權限

如果您想使用 Amazon SES 傳送電子郵件，則需要設定權限。

1. 選取 **Configuration**，然後選擇 **Execution role**。
1. 在 **Summary** 中，選擇 **Permissions**。
1. 選取 **{}JSON** 以開啟 JSON 政策編輯器。
1. 為您想使用的 Amazon SES 資源新增權限。

下列範例提供傳送電子郵件動作的資源 ARN：

```json
{
"Effect": "Allow",
"Action": [
      "ses:SendEmail",
      "ses:SendRawEmail"
            ],
"Resource": "arn:aws:ses:us-west-2:555555511111:identity/sender@example.com"
}
```

若要進一步瞭解如何設定角色權限，請參閱 AWS Lambda 使用者指南中的[權限](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-images.html#gettingstarted-images-permissions)。