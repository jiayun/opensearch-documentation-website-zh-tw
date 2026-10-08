---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: generate-data
nav_order: 50
parent: Command reference
grand_parent: Reference
redirect_from:
  - /benchmark/commands/generate-data/
---

<!-- vale off -->
# generate-data 命令
<!-- vale on -->

`generate-data` 命令會建立用於基準測試與測試的合成資料集。OpenSearch Benchmark 支援兩種資料產生方式：使用 OpenSearch 索引對應，或使用包含使用者自訂邏輯的 Python 模組。如需更多資訊，請參閱 [合成資料產生]({{site.url}}{{site.baseurl}}/benchmark/features/synthetic-data-generation/)。

## 用法

```shell
osb generate-data --index-name <INDEX_NAME> --output-path <OUTPUT_PATH> --total-size <SIZE_GB> [OPTIONS]
```

**必要條件**：

- 必須指定 `--index-mappings` 或 `--custom-module` 其中之一，但不可同時指定兩者。
- 使用 `--custom-module` 時，您的 Python 模組必須包含 `generate_synthetic_document(providers, **custom_lists)` 函式。

## 資料產生方式

請選擇下列其中一種方式：

**方式 1：使用索引對應**：

```shell
osb generate-data --index-name my-index --index-mappings mapping.json --output-path ./data --total-size 1
```

**方式 2：使用自訂 Python 模組**：

```shell
osb generate-data --index-name my-index --custom-module custom.py --output-path ./data --total-size 1
```

## 選項

搭配 `generate-data` 命令使用下列選項。

| 選項 | 必要/選用 | 說明 |
|---|---|---|
| `--index-name` 或 `-n` | 必要 | 您要產生的資料語料庫名稱。 |
| `--output-path` 或 `-p` | 必要 | 您要產生資料的目的地路徑。 |
| `--total-size` 或 `-s` | 必要 | 您要產生的資料總量，單位為 GB。 |
| `--index-mappings` 或 `-i` | 條件式（必須指定 `--index-mappings` 或 `--custom-module` 其中之一）| 您要使用的 OpenSearch 索引對應路徑。使用對應式產生時為必要。不可與 `--custom-module` 併用。 |
| `--custom-module` 或 `-m` | 條件式（必須指定 `--index-mappings` 或 `--custom-module` 其中之一）| 包含您自訂邏輯的 Python 模組路徑。使用自訂邏輯產生時為必要。不可與 `--index-mappings` 併用。Python 模組必須包含 `generate_synthetic_document(providers, **custom_lists)` 函式。 |
| `--custom-config` 或 `-c` | 選用 | 定義資料產生規則的 YAML 組態檔路徑。 |
| `--test-document` 或 `-t` | 選用 | 當此旗標存在時，OpenSearch Benchmark 會產生單一合成文件並輸出至主控台，讓您能驗證產生的範例文件是否符合預期。當此旗標不存在時，將產生整個資料語料庫。 |

## 範例輸出

以下是產生合成資料時的範例輸出：

```
   ____                  _____                      __       ____                  __                         __
  / __ \____  ___  ____ / ___/___  ____ ___________/ /_     / __ )___  ____  _____/ /_  ____ ___  ____ ______/ /__
 / / / / __ \/ _ \/ __ \\__ \/ _ \/ __ `/ ___/ ___/ __ \   / __  / _ \/ __ \/ ___/ __ \/ __ `__ \/ __ `/ ___/ //_/
/ /_/ / /_/ /  __/ / / /__/ /  __/ /_/ / /  / /__/ / / /  / /_/ /  __/ / / / /__/ / / / / / / / / /_/ / /  / ,<
\____/ .___/\___/_/ /_/____/\___/\__,_/_/   \___/_/ /_/  /_____/\___/_/ /_/\___/_/ /_/_/ /_/ /_/\__,_/_/  /_/|_|
    /_/


[NOTE] ✨ Dashboard link to monitor processes and task streams: [http://127.0.0.1:8787/status]
[NOTE] ✨ For users who are running generation on a virtual machine, consider SSH port forwarding (tunneling) to localhost to view dashboard.
[NOTE] Example of localhost command for SSH port forwarding (tunneling) from an AWS EC2 instance:
ssh -i <PEM_FILEPATH> -N -L localhost:8787:localhost:8787 ec2-user@<DNS>

Total GB to generate: [1]
Average document size in bytes: [412]
Max file size in GB: [40]

100%|███████████████████████████████████████████████████████████████████| 100.07G/100.07G [3:35:29<00:00, 3.98MB/s]

Generated 24271844660 docs in 12000 seconds. Total dataset size is 100.21GB.
✅ Visit the following path to view synthetically generated data: /home/ec2-user/

-----------------------------------
[INFO] ✅ SUCCESS (took 272 seconds)
-----------------------------------
```

## 相關文件

- [使用索引對應產生資料]({{site.url}}{{site.baseurl}}/benchmark/features/synthetic-data-generation/mapping-sdg/)
- [使用自訂邏輯產生資料]({{site.url}}{{site.baseurl}}/benchmark/features/synthetic-data-generation/custom-logic-sdg/)