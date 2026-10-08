---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "遷移協助"
nav_order: 110
---

# 從 1.X 遷移至 2.X

對於已有與 OpenSearch Benchmark 整合之系統的使用者，我們建議執行下列步驟，以順利轉換至 OpenSearch Benchmark 2.0。

## 更新 Benchmark.ini
OpenSearch Benchmark 依賴 `benchmark.ini`，預設可在 `~/.benchmark` 目錄中找到。此組態檔提供與指標回報位置、工作負載取得方式等相關的組態。OpenSearch Benchmark 2.0 將 `[results_publishing]` 重新命名為 `[reporting]`。

組態檔應如下所示：
```ini
[reporting]
datastore.type = in-memory
datastore.host = <host-url>
datastore.port = <host-port>
datastore.secure = False
datastore.ssl.verification_mode = <ssl-verification-details>
datastore.user = <username>
datastore.password = <password>
...
```

如需如何設定 OpenSearch Benchmark 的資訊，請參閱[設定 OpenSearch Benchmark]({{site.url}}{{site.baseurl}}/benchmark/configuring-benchmark/)。

## 更新外部指標資料儲存區

許多使用者會使用外部指標資料儲存區來儲存先前測試執行的結果與指標。

OpenSearch Benchmark `1.X` 將測試詳細資料儲存在符合 `benchmark-test-executions-*` 索引模式的索引中。然而，在 `2.X` 中，則是儲存在符合 `benchmark-test-runs-*` 索引模式的索引中。我們建議在您的指標資料儲存區中加入這個新的索引模式，並更新可能仍在使用舊索引模式的儀表板。

舊索引模式 | 新索引模式 |
:--- | :--- |
benchmark-test-executions-* | benchmark-test-runs-* |

## 更新指令碼

有些使用者會以自訂指令碼包裝 OpenSearch Benchmark 來執行夜間效能測試。這些指令碼可能依賴某些在 `2.X` 中已被棄用的術語。

**請參閱下列術語並據此調整您的指令碼。**

1.X 術語 | 2.X 術語 |
:--- | :--- |
execute-test, test-execution-id, TestExecution | run, test-run, TestRun |
results_publishing, results_publisher | reporting, publisher |
provision-configs, provision-config-instances | cluster-configs, cluster-config-instances
load-worker-coordinator-hosts | worker-ips |

如果您在將 OpenSearch Benchmark 從 `1.X` 遷移至 `2.X` 時遇到任何問題，可透過下列任一方式聯繫 OpenSearch Benchmark 維護人員：
- [在 OpenSearch Benchmark Slack 頻道張貼問題](https://opensearch.slack.com/archives/C082PLA3VPW)。
- [參加 Community Meeting、Office Hours 與 Issue Triage](https://www.meetup.com/opensearch/events/309982456/?eventOrigin=group_upcoming_events)。
- [在 OpenSearch Benchmark GitHub 儲存庫建立 issue](https://github.com/opensearch-project/opensearch-benchmark/issues)。