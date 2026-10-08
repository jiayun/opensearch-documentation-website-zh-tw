---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "擴充工作負載的資料語料庫"
nav_order: 55
redirect_from:
  - /benchmark/user-guide/optimizing-benchmarks/expand-data-corpus/
---

# 擴充工作負載的資料語料庫

本教學說明如何使用 [`expand-data-corpus.py`](https://github.com/opensearch-project/opensearch-benchmark/blob/main/scripts/expand-data-corpus.py) 指令碼來增加 OpenSearch Benchmark 工作負載的資料語料庫大小。在大型 OpenSearch 叢集上執行 `http_logs` 工作負載時，這項功能會有所幫助。

此指令碼僅適用於 `http_logs` 工作負載。
{: .warning}

## 先決條件

若要使用本教學，請確認您符合下列先決條件：

1. 您已安裝 Python 3.x 或更新版本。
2. `http_logs` 工作負載的資料語料庫已儲存在執行 OpenSearch Benchmark 的負載產生主機上。

## 瞭解指令碼

`expand-data-corpus.py` 指令碼透過複製並修改 `http_logs` 工作負載語料庫中的現有文件，產生更大的資料語料庫。它主要調整時間戳記欄位，同時保留其他欄位不變。它也會產生偏移量檔案，讓 OpenSearch Benchmark 能更快啟動。

## 使用 `expand-data-corpus.py`

若要使用 `expand-data-corpus.py`，請使用下列語法：

```bash
./expand-data-corpus.py [options]
```

此指令碼提供數個自訂選項。以下是最常用的選項：

- `--corpus-size`：所需的語料庫大小，以 GB 為單位
- `--output-file-suffix`：輸出檔案名稱的後綴。

## 範例

下列指令碼命令範例會產生 100 GB 的語料庫：

```bash
./expand-data-corpus.py --corpus-size 100 --output-file-suffix 100gb
```

指令碼會開始產生文件。對於 100 GB 的語料庫，產生完整語料庫最多可能需要 30 分鐘。

您可以使用不同的輸出後綴多次執行指令碼，以產生多個語料庫。OpenSearch Benchmark 會在資料注入期間依序使用此指令碼產生的所有語料庫。

## 驗證文件

指令碼執行完成後，請檢查下列位置是否有新檔案：

- 在 `http_logs` 的 OpenSearch Benchmark 資料目錄中：
   - `documents-100gb.json`：產生的語料庫
   - `documents-100gb.json.offset`：相關的偏移量檔案

- 在 `http_logs` 工作負載目錄中：
   - `gen-docs-100gb.json`：產生的語料庫的中繼資料
   - `gen-idx-100gb.json`：產生的語料庫的索引規格

## 在測試中使用語料庫

若要在 OpenSearch Benchmark 測試中使用新產生的語料庫，請使用下列語法：

```bash
opensearch-benchmark run --workload http_logs --workload-params=generated_corpus:t [other_options]
```

`generated_corpus:t` 參數會指示 OpenSearch Benchmark 使用擴充後的語料庫。您可以在 `--workload-params` 選項中使用逗號分隔，附加任何其他工作負載參數。

## 專家級設定

使用 `--help` 可查看此指令碼支援的所有選項。使用下列專家級設定時請謹慎，因為這些設定可能會影響語料庫結構：

- `-f`：指定用作產生新文件基礎的輸入檔案
- `-n`：設定要產生的文件數量，而非語料庫大小
- `-i`：定義連續時間戳記之間的間隔
- `-t`：設定所產生文件的起始時間戳記
- `-b`：定義寫入偏移量檔案時每批次的文件數量

