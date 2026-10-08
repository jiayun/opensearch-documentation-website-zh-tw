---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: list
nav_order: 80
parent: Command reference
grand_parent: Reference
redirect_from:
  - /benchmark/commands/list/
---

<!-- vale off -->
# list 命令
<!-- vale on -->

`list` 命令會列出 OpenSearch Benchmark 使用的下列元素：

- `telemetry`：遙測裝置
- `workloads`：工作負載
- `pipelines`：管線
- `test-runs`：工作負載的單次執行
- `cluster-configs`：OpenSearch 叢集組態
- `opensearch-plugins`：OpenSearch 外掛程式


## 用法

下列範例會列出所有工作負載測試執行，以及每項測試的詳細資訊：

```
`opensearch-benchmark list test-runs
```

OpenSearch Benchmark 會傳回每項測試的相關資訊。

```
opensearch-benchmark list test-runs

   ____                  _____                      __       ____                  __                         __
  / __ \____  ___  ____ / ___/___  ____ ___________/ /_     / __ )___  ____  _____/ /_  ____ ___  ____ ______/ /__
 / / / / __ \/ _ \/ __ \\__ \/ _ \/ __ `/ ___/ ___/ __ \   / __  / _ \/ __ \/ ___/ __ \/ __ `__ \/ __ `/ ___/ //_/
/ /_/ / /_/ /  __/ / / /__/ /  __/ /_/ / /  / /__/ / / /  / /_/ /  __/ / / / /__/ / / / / / / / / /_/ / /  / ,<
\____/ .___/\___/_/ /_/____/\___/\__,_/_/   \___/_/ /_/  /_____/\___/_/ /_/\___/_/ /_/_/ /_/ /_/\__,_/_/  /_/|_|
    /_/


Recent test-runs:

TestRun ID                            TestRun Timestamp    Workload    Workload Parameters    TestProcedure        ClusterConfigInstance    User Tags    workload Revision    Cluster Config Revision
------------------------------------  -------------------  ----------  ---------------------  -------------------  -----------------------  -----------  -------------------  -------------------------
729291a0-ee87-44e5-9b75-cc6d50c89702  20230524T181718Z           geonames                           append-no-conflicts  4gheap                                  30260cf
f91c33d0-ec93-48e1-975e-37476a5c9fe5  20230524T170134Z           geonames                           append-no-conflicts  4gheap                                  30260cf
d942b7f9-6506-451d-9dcf-ef502ab3e574  20230524T144827Z           geonames                           append-no-conflicts  4gheap                                  30260cf
a33845cc-c2e5-4488-a2db-b0670741ff9b  20230523T213145Z           geonames                           append-no-conflicts  4gheap                                  30260cf
ba643ed3-0db5-452e-a680-2b0dc0350cf2  20230522T224450Z           geonames                           append-no-conflicts  external                                30260cf
8d366ec5-3322-4e09-b041-a4b02e870033  20230519T201514Z           geonames                           append-no-conflicts  external                                30260cf
4574c13e-8742-41af-a4fa-79480629ecf0  20230519T195617Z           geonames                           append-no-conflicts  external                                30260cf
3e240d18-fc87-4c49-9712-863196efcef4  20230519T195412Z           geonames                           append-no-conflicts  external                                30260cf
90f066ae-3d83-41e9-bbeb-17cb0480d578  20230519T194448Z           geonames                           append-no-conflicts  external                                30260cf
78602e07-0ff8-4f00-9a0e-746fb64e4129  20230519T193258Z           geonames                           append-no-conflicts  external                                30260cf

----------------------------------
[INFO] ✅ SUCCESS (took 0 seconds)
----------------------------------
```

## 選項

您可以在 `test` 命令中使用下列選項：

- `--limit`：限制最近測試執行的搜尋結果數量。預設值為 `10`。
- `--workload-repository`：定義 OpenSearch Benchmark 載入工作負載的儲存庫。
- `--workload-path`：定義已下載或自訂工作負載的路徑。
- `--workload-revision`：定義 OpenSearch Benchmark 應使用的工作負載原始碼樹中的特定修訂版本。


