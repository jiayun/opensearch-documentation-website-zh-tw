---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: info
nav_order: 70
parent: Command reference
grand_parent: Reference
redirect_from:
  - /benchmark/commands/info/
---

<!-- vale off -->
# info 命令
<!-- vale on -->

`info` 命令會印出 OpenSearch Benchmark 元件的詳細資訊。

## 使用方式

下列範例會傳回名為 `nyc_taxis` 的工作負載資訊：

```
opensearch-benchmark info --workload=nyc_taxis
```

OpenSearch Benchmark 會傳回工作負載的資訊，如下列範例回應所示：

```
   ____                  _____                      __       ____                  __                         __
  / __ \____  ___  ____ / ___/___  ____ ___________/ /_     / __ )___  ____  _____/ /_  ____ ___  ____ ______/ /__
 / / / / __ \/ _ \/ __ \\__ \/ _ \/ __ `/ ___/ ___/ __ \   / __  / _ \/ __ \/ ___/ __ \/ __ `__ \/ __ `/ ___/ //_/
/ /_/ / /_/ /  __/ / / /__/ /  __/ /_/ / /  / /__/ / / /  / /_/ /  __/ / / / /__/ / / / / / / / / /_/ / /  / ,<
\____/ .___/\___/_/ /_/____/\___/\__,_/_/   \___/_/ /_/  /_____/\___/_/ /_/\___/_/ /_/_/ /_/ /_/\__,_/_/  /_/|_|
    /_/

Showing details for workload [nyc_taxis]:

* Description: Taxi rides in New York in 2015
* Documents: 165,346,692
* Compressed Size: 4.5 GB
* Uncompressed Size: 74.3 GB

===================================
TestProcedure [searchable-snapshot]
===================================

Measuring performance for Searchable Snapshot feature. Based on the default test procedure 'append-no-conflicts'.

Schedule:
----------

1. delete-index
2. create-index
3. check-cluster-health
4. index (8 clients)
5. refresh-after-index
6. force-merge
7. refresh-after-force-merge
8. wait-until-merges-finish
9. create-snapshot-repository
10. delete-snapshot
11. create-snapshot
12. wait-for-snapshot-creation
13. delete-local-index
14. restore-snapshot
15. default
16. range
17. distance_amount_agg
18. autohisto_agg
19. date_histogram_agg

====================================================
TestProcedure [append-no-conflicts] (run by default)
====================================================

Indexes the entire document corpus using a setup that will lead to a larger indexing throughput than the default settings and produce a smaller index (higher compression rate). Document IDs are unique, so all index operations are append only. After that, a couple of queries are run.

Schedule:
----------

1. delete-index
2. create-index
3. check-cluster-health
4. index (8 clients)
5. refresh-after-index
6. force-merge
7. refresh-after-force-merge
8. wait-until-merges-finish
9. default
10. range
11. distance_amount_agg
12. autohisto_agg
13. date_histogram_agg

==============================================
TestProcedure [append-no-conflicts-index-only]
==============================================

Indexes the whole document corpus using a setup that will lead to a larger indexing throughput than the default settings and produce a smaller index (higher compression rate). Document ids are unique so all index operations are append only.

Schedule:
----------

1. delete-index
2. create-index
3. check-cluster-health
4. index (8 clients)
5. refresh-after-index
6. force-merge
7. refresh-after-force-merge
8. wait-until-merges-finish

=====================================================
TestProcedure [append-sorted-no-conflicts-index-only]
=====================================================

Indexes the whole document corpus in an index sorted by pickup_datetime field in descending order (most recent first) and using a setup that will lead to a larger indexing throughput than the default settings and produce a smaller index (higher compression rate). Document ids are unique so all index operations are append only.

Schedule:
----------

1. delete-index
2. create-index
3. check-cluster-health
4. index (8 clients)
5. refresh-after-index
6. force-merge
7. refresh-after-force-merge
8. wait-until-merges-finish

======================
TestProcedure [update]
======================

Schedule:
----------

1. delete-index
2. create-index
3. check-cluster-health
4. update (8 clients)
5. refresh-after-index
6. force-merge
7. refresh-after-force-merge
8. wait-until-merges-finish


----------------------------------
[INFO] ✅ SUCCESS (took 2 seconds)
----------------------------------
```

## 選項

您可以搭配 `info` 命令使用下列選項：


- `--workload-repository`：定義 OpenSearch Benchmark 載入工作負載的來源儲存庫。
- `--workload-path`：定義已下載或自訂工作負載的路徑。
- `--workload-revision`：定義 OpenSearch Benchmark 應使用的工作負載原始碼樹特定修訂版本。
- `--workload`：根據工作負載名稱定義要使用的工作負載。您可以使用 `opensearch-benchmark list workloads` 查詢預先載入的工作負載清單。
- `--test-procedure`：定義要使用的測試程序。您可以使用 `opensearch-benchmark list test_procedures` 查詢測試程序清單。
- `--include-tasks`：定義要執行的測試程序工作清單，以逗號分隔。預設會執行測試程序陣列中列出的所有工作。
- `--exclude-tasks`：定義不要執行的測試程序工作清單，以逗號分隔。
