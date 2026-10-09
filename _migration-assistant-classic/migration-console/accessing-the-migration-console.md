---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "存取遷移主控台"
nav_order: 1
parent: Migration Console
permalink: /classic/migration-assistant/migration-console/accessing-the-migration-console/
---

# 存取遷移主控台

透過 Migration Assistant 部署的 bootstrap 機器中包含一個指令碼，可簡化透過該執行個體存取 Migration Console 的程序。

若要存取 Migration Console，請使用下列命令：

```shell
export STAGE=dev  # Use the same stage value from your cdk.context.json deployment
export AWS_REGION=us-west-2
/opensearch-migrations/deployment/cdk/opensearch-service-migration/accessContainer.sh migration-console ${STAGE} ${AWS_REGION}
```
{% include copy.html %}

**重要：**`STAGE` 的值必須與您在 CDK context 組態中使用的 `stage` 參數相符。例如：
- 如果您使用 `"stage": "test"` 進行部署，請使用 `export STAGE=test`。
- 如果您使用 `"stage": "prod"` 進行部署，請使用 `export STAGE=prod`。
- 如果您使用 `"stage": "dev"` 進行部署，請使用 `export STAGE=dev`。

開啟主控台時，命令提示字元上方會顯示一則訊息，即 `Welcome to the Migration Assistant Console`。

在已安裝 [AWS Command Line Interface (AWS CLI)](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) 與 [AWS Session Manager 外掛程式](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html) 的機器上，您可以直接連線至 Migration Console。請確保您已使用具備該環境存取權限的憑證執行 `aws configure`。

請使用下列命令：

```shell
export STAGE=dev  # Match your deployment stage
export SERVICE_NAME=migration-console
export TASK_ARN=$(aws ecs list-tasks --cluster migration-${STAGE}-ecs-cluster --family "migration-${STAGE}-${SERVICE_NAME}" | jq --raw-output '.taskArns[0]')
aws ecs execute-command --cluster "migration-${STAGE}-ecs-cluster" --task "${TASK_ARN}" --container "${SERVICE_NAME}" --interactive --command "/bin/bash"
```
{% include copy.html %}

### 階段組態範例

針對不同的部署環境，請相應調整階段：

```shell
# For test environment deployment
export STAGE=test
./accessContainer.sh migration-console test us-west-2

# For production environment deployment  
export STAGE=prod
./accessContainer.sh migration-console prod us-west-2

# For development environment deployment
export STAGE=dev
./accessContainer.sh migration-console dev us-west-2
```
{% include copy.html %}

`STAGE` 的值對應於您在部署時於 AWS CDK context 組態中指定的 `stage` 參數。
