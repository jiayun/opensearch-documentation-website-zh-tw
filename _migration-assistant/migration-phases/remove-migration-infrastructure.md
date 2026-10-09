---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "移除 Migration Assistant"
nav_order: 90
parent: Migration workflows
permalink: /migration-assistant/migration-phases/remove-migration-infrastructure/
redirect_from:
  - /migration-assistant/migration-phases/removing-migration-infrastructure/
  - /migration-phases/removing-migration-infrastructure/

---

# 移除遷移基礎架構

請勿在遷移成功後立即移除遷移基礎架構。

移除前，請確認下列事項：

- 正式環境流量在目標端已穩定運作。
- 您不再需要使用來源端進行復原。
- 您不再需要重播或比較檢查。
- 您想保留的所有快照產物都已明確保留。

## 一般 Kubernetes 移除程序

若要移除 Helm 部署和持久磁碟區，請執行下列命令：

```bash
helm uninstall -n ma ma
kubectl -n ma delete pvc --all
kubectl delete namespace ma
```
{% include copy.html %}

## Amazon EKS 移除程序

如果您使用了 EKS 啟動程序，請先移除 Helm 發行版本，再移除 CloudFormation 堆疊：

```bash
helm uninstall -n ma ma
kubectl -n ma delete pvc --all
aws cloudformation delete-stack --stack-name <STACK_NAME>
aws cloudformation wait stack-delete-complete --stack-name <STACK_NAME>
```
{% include copy.html %}

這會移除解決方案堆疊所建立的 EKS 平台資源。

## 保留快照與產物

請審慎決定是否移除 S3。預設的遷移儲存貯體通常仍可用於：

- 稽核與復原調查
- 保存快照
- 比較切換後的行為

請僅在確定不再需要儲存貯體的內容後，才刪除該儲存貯體。
{: .warning }

{% include migration-phase-navigation.html %}