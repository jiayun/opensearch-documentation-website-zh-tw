---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "移除 Migration Assistant"
nav_order: 9
parent: Migration phases
permalink: /classic/migration-assistant/migration-phases/remove-migration-infrastructure/
---

# 移除遷移基礎設施

遷移完成後，您應移除所有資源，但目標叢集以及（選用）您的 Amazon CloudWatch 記錄檔和 Traffic Replayer 記錄檔除外。

若要移除部署期間建立的 AWS Cloud Development Kit (AWS CDK) 堆疊，請在 CDK 目錄中執行下列命令：

```bash  
cd deployment/cdk/opensearch-service-migration
cdk destroy "*" --c contextId=<CONTEXT_ID>
```
{% include copy.html %}

請依照命令列上的指示，從您的 AWS 帳戶移除已部署的資源。

您也可以使用 AWS Management Console 移除 Migration Assistant 資源，並確認這些資源已不存在於帳戶中。

## 解除安裝 OpenSearch 的 Migration Assistant

您可以從 AWS Management Console 或使用 AWS Command Line Interface (AWS CLI) 解除安裝 OpenSearch Service 的 Migration Assistant。請手動移除符合語法 `cdk-<unique id>-assets-<account id>-<region>` 的 Amazon Simple Storage Service (Amazon S3) 儲存貯體內容，該儲存貯體是由 Migration Assistant 所建立。OpenSearch 的 Migration Assistant 不會自動刪除 S3 儲存貯體。

若要刪除已儲存的資料以及 Migration Assistant 所建立的 AWS CloudFormation 堆疊，請參閱 Amazon OpenSearch Service 文件中的 [解除安裝解決方案](https://docs.aws.amazon.com/solutions/latest/migration-assistant-for-amazon-opensearch-service/uninstall-the-solution.html)。

{% include migration-phase-navigation.html %}
