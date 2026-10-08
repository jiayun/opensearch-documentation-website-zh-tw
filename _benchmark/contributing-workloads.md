---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分享自訂工作負載"
parent: Creating custom workloads
nav_order: 20
redirect_from:
  - /benchmark/user-guide/contributing-workloads/
  - /benchmark/user-guide/working-with-workloads/contributing-workloads/
---

# 分享自訂工作負載

您可以將自訂工作負載上傳至 GitHub 上的[工作負載儲存庫](https://github.com/opensearch-project/opensearch-benchmark-workloads/)，與其他 OpenSearch 使用者分享。

請確認工作負載資料集中包含的任何資料都不含專有資料或個人識別資訊 (PII)。

如要分享自訂工作負載，請依照下列步驟操作。

## 建立 README.md

提供詳細的 `README.MD` 檔案，其中包含下列內容：

- 工作負載的用途。為工作負載建立說明時，請考量其特定用途，以及該用途與[工作負載儲存庫](https://github.com/opensearch-project/opensearch-benchmark-workloads/)中其他用途的差異。
- 資料集中的範例文件，可協助使用者瞭解資料結構。
- 可用來自訂工作負載的工作負載參數。
- 工作負載所含的預設測試程序清單，以及工作負載可執行的其他測試程序。
- 執行測試後，工作負載所產生的輸出範例。
- 開放原始碼授權的副本，授予使用者和 OpenSearch Benchmark 使用該資料集的權限。

如需範例工作負載 `README` 檔案，請前往 `http_logs` [`README`](https://github.com/opensearch-project/opensearch-benchmark-workloads/blob/main/http_logs/README.md)。

## 驗證工作負載的結構

工作負載必須包含下列檔案：

- `workload.json`
- `index.json`
- `files.txt`
- `test_procedures/default.json`
- `operations/default.json`

兩個 `default.json` 檔案名稱都可自訂為具描述性的名稱。工作負載可包含選用的 `workload.py` 檔案，以新增更多動態功能。如需檔案內容的詳細資訊，請前往[工作負載的結構]({{site.url}}{{site.baseurl}}/benchmark/anatomy-of-a-workload/)。

## 測試工作負載

所有貢獻至 OpenSearch Benchmark 的工作負載都必須符合下列測試需求：

- 為探索工作負載並產生範例而執行的所有測試，都必須以 OpenSearch 叢集為目標。
- 工作負載必須通過所有整合測試。請依照下列步驟，確保工作負載通過整合測試：
   1. 將工作負載新增至您所 fork 的[工作負載儲存庫](https://github.com/opensearch-project/opensearch-benchmark-workloads/)副本。請確認您已 fork `opensearch-benchmark-workloads` 儲存庫和 [OpenSeach Benchmark](https://github.com/opensearch-project/opensearch-benchmark) 儲存庫。
   3. 在您所 fork 的 OpenSearch Benchmark 儲存庫中，更新 `/osbenchmark/it/resources` 目錄中的 `benchmark-os-it.ini` 和 `benchmark-in-memory.ini` 檔案，使其指向包含您工作負載的已 fork 工作負載儲存庫。
   4. 修改 `.ini` 檔案後，將變更提交至分支以進行測試。
   6. 選取您提交變更的分支，使用 GitHub Actions 執行整合測試。確認測試已如預期執行。
   7. 如果整合測試如預期執行，請前往您所 fork 的工作負載儲存庫，將工作負載變更合併至 `1` 和 `2` 分支。這可讓您的工作負載同時出現在兩個主要版本的 OpenSearch Benchmark 中。

## 建立 PR

測試工作負載後，請從您的 fork 建立提取要求 (PR) 至 `opensearch-project` [工作負載儲存庫](https://github.com/opensearch-project/opensearch-benchmark-workloads/)。在 PR 說明中新增範例輸出和摘要結果。OpenSearch Benchmark 維護人員將會審查該 PR。

PR 通過核准後，您必須分享資料集的資料語料庫。OpenSearch Benchmark 團隊接著可將該資料集新增至共用的 S3 儲存貯體。如果您的資料語料庫儲存在 S3 儲存貯體中，您可以使用 [AWS DataSync](https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html) 來分享資料語料庫。否則，您必須告知維護人員資料語料庫所在的位置。
