---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "版本歷史"
nav_order: 105
---

# OpenSearch Benchmark 版本歷史

本頁面詳細說明 OpenSearch Benchmark 各版本的主要變更。

## OpenSearch Benchmark 2.0 的術語更新

OpenSearch Benchmark 2.0 引入了更新的術語，以提升使用者體驗並提供更直覺的基準測試工作流程。

1.X 術語 | 2.X 術語 |
:--- | :--- |
execute-test, test-execution-id, TestExecution | run, test-run, TestRun |
results_publishing, results_publisher | reporting, publisher |
provision-configs, provision-config-instances | cluster-configs, cluster-config-instances
load-worker-coordinator-hosts | worker-ips |

## 版本歷史

OpenSearch Benchmark 版本 | 版本重點 | 發布日期
:--- | :--- | :---
[2.0.0](https://github.com/opensearch-project/opensearch-build/blob/main/release-notes/opensearch-release-notes-3.1.0.md) | 引入新機制以提升使用者體驗與直覺的基準測試工作流程。新增合成資料產生、資料串流與視覺化等新功能。 | 2025 年 8 月 21 日
[1.15.0](https://github.com/opensearch-project/opensearch-benchmark/releases/tag/1.15.0) |  讓使用者能使用工作階段型驗證，自動處理暫時憑證的產生與重新整理，免除手動匯出 AWS 憑證的需求。在 compare 命令中新增 percent diff。修正 execute-test 的錯誤 | 2025 年 8 月 7 日
