---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "遷移工作流程"
nav_order: 40
nav_exclude: false
has_children: true
has_toc: false
permalink: /migration-assistant/migration-phases/
redirect_from:
  - /migration-assistant/overview/migration-phases/
  - /migration-phases/
---

# 遷移工作流程

Migration Assistant 以工作流程驅動。您選擇遷移模式、完成一次組態設定、執行試行、驗證結果，然後執行切換。

## 通用生命週期

大多數遷移都遵循相同的生命週期：

1. **評估** 相容性、不支援的元件及停機需求。
2. **部署** Migration Assistant 至 Kubernetes 或 Amazon EKS。
3. **設定** 工作流程，使用適用於您已安裝版本的範例。
4. **執行試行**，使用小型允許清單。
5. **提交完整工作流程**，並透過 Workflow CLI 監控。
6. **核准** 需經核准的階段轉換，且僅在驗證後進行。
7. **切換** 至目標。
8. **移除基礎架構**，且僅在回復期間結束後進行。

## 情境 1：僅回填

最適合可容忍短暫停止寫入，或可暫停寫入並從外部佇列重播寫入的叢集。下圖顯示此工作流程：

```
Snapshot source → Migrate metadata → Backfill documents → Verify → Switch traffic
```

## 情境 2：僅擷取與重播

最適合資料量夠小、僅靠即時重播即可同步目標的情況，或您想對多個目標叢集重播流量以比較結果的情況。下圖顯示此工作流程：

```
Reroute traffic to capture proxy → Migrate metadata → Replay traffic → Verify → Switch traffic to target
```

## 情境 3：回填 + 擷取與重播（零停機）

先開始擷取以確保不遺失任何寫入，再透過回填移轉歷史資料，最後透過重播讓目標追上即時狀態。下圖顯示此工作流程：

```
Reroute traffic to capture proxy → Snapshot source → Migrate metadata → Backfill documents → Replay captured traffic → Verify → Switch traffic to target
```

## 階段概觀

下表說明遷移工作流程的各個階段。

| 階段 | 說明 | 指南 |
|:------|:------------|:------|
| [評估]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/assessment/) | 檢視不相容變更並規劃您的遷移 | 不限版本 |
| [選擇您的部署方式]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/) | 部署 Migration Assistant 至 Kubernetes 或 EKS | [Kubernetes]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/deploying-to-kubernetes/) / [EKS]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/deploying-to-eks/) |
| [將用戶端流量重新導向擷取代理伺服器]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/reroute-source-to-proxy/) | 讓流量通過擷取代理伺服器以記錄寫入 | 僅適用於擷取與重播 |
| [遷移中繼資料]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/migrate-metadata/) | 移轉索引設定、對應、範本及別名 | Workflow CLI |
| [回填]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/backfill/) | 使用以快照為基礎的重新編製索引（RFS）遷移文件 | Workflow CLI |
| [重播擷取的流量]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/replay-captured-traffic/) | 重播已記錄的流量，讓目標追上即時狀態 | 僅適用於擷取與重播 |
| [將流量切換至目標]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/switch-traffic-to-target/) | 將用戶端從擷取代理伺服器重新導向目標叢集 | 僅適用於擷取與重播 |
| [移除基礎架構]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/remove-migration-infrastructure/) | 移除 Migration Assistant 資源 | Helm/CloudFormation |

## 不會自動遷移的元件

Migration Assistant 不會自動遷移下列元件。您必須個別遷移這些元件：

- 安全性組態
- ISM 或 ILM 原則
- 資料匯入管線
- 儀表板或 Kibana 儲存的物件
- 資料串流
- 叢集層級的調校

## 後續步驟

如需更多資訊，請參閱下列資源：

- 如果尚未部署 Migration Assistant，請參閱[選擇您的部署方式]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/)。
- 如果您需要設定並提交工作流程，請參閱 [Workflow CLI]({{site.url}}{{site.baseurl}}/migration-assistant/workflow-cli/)。
- 如果您已知道來源與目標的組合，請參閱[操作手冊]({{site.url}}{{site.baseurl}}/migration-assistant/playbooks/)。

{% include migration-phase-navigation.html %}
