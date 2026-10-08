---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立自訂工作負載"
nav_order: 35
has_children: true
has_toc: false
redirect_from:
  - /benchmark/user-guide/creating-custom-workloads/
  - /benchmark/user-guide/creating-osb-workloads/
  - /benchmark/user-guide/working-with-workloads/creating-custom-workloads/
---

# 建立自訂工作負載

OpenSearch Benchmark 內建一組[工作負載](https://github.com/opensearch-project/opensearch-benchmark-workloads)，可用來對您叢集中的資料進行基準測試。您也可以使用下列其中一種方式，建立專屬於您自己資料的工作負載：

- [從現有叢集建立工作負載](#creating-a-workload-from-an-existing-cluster)
- [在沒有現有叢集的情況下建立工作負載](#creating-a-workload-without-an-existing-cluster)

## 從現有叢集建立工作負載

如果您已經有一個含有已編製索引資料的 OpenSearch 叢集，請依照下列步驟為您的叢集建立自訂工作負載。

### 必要條件

在建立自訂 OpenSearch Benchmark 工作負載之前，請確認您已具備下列必要條件：

- 一個 OpenSearch 叢集，其中索引包含 1000 筆或更多文件。如果叢集的索引未包含至少 1000 筆文件，工作負載仍然可以執行測試，但無法使用 `--test-mode` 執行工作負載。
- 您必須具備存取 OpenSearch 叢集的正確權限。如需叢集權限的更多資訊，請參閱[權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/)。

### 自訂工作負載

若要開始建立自訂 OpenSearch Benchmark 工作負載，請使用 `opensearch-benchmark create-workload` 命令。

```bash
opensearch-benchmark create-workload \
--workload="<WORKLOAD NAME>" \
--target-hosts="<CLUSTER ENDPOINT>" \
--client-options="basic_auth_user:'<USERNAME>',basic_auth_password:'<PASSWORD>'" \
--indices="<INDEXES TO GENERATE WORKLOAD FROM>" \
--output-path="<LOCAL DIRECTORY PATH TO STORE WORKLOAD>"
```

請將上述範例中的下列選項，替換為您現有叢集的專屬資訊：

- `--workload`：自訂工作負載的自訂名稱。
- `--target-hosts:` 以逗號分隔的 host:port 配對清單，叢集會從這些位址擷取資料。
- `--client-options`：OpenSearch Benchmark 用來存取叢集的基本驗證用戶端選項。
- `--indices`：OpenSearch 叢集中一或多個含有資料的索引。
- `--output-path`：OpenSearch Benchmark 建立工作負載及其組態檔案的目錄。

下列範例回應會從一個名為 `movies-info` 的索引所在叢集，建立一個名為 `movies` 的工作負載。`movies-info` 索引包含超過 2,000 筆文件。

```bash
   ____                  _____                      __       ____                  __                         __
  / __ \____  ___  ____ / ___/___  ____ ___________/ /_     / __ )___  ____  _____/ /_  ____ ___  ____ ______/ /__
 / / / / __ \/ _ \/ __ \\__ \/ _ \/ __ `/ ___/ ___/ __ \   / __  / _ \/ __ \/ ___/ __ \/ __ `__ \/ __ `/ ___/ //_/
/ /_/ / /_/ /  __/ / / /__/ /  __/ /_/ / /  / /__/ / / /  / /_/ /  __/ / / / /__/ / / / / / / / / /_/ / /  / ,<
\____/ .___/\___/_/ /_/____/\___/\__,_/_/   \___/_/ /_/  /_____/\___/_/ /_/\___/_/ /_/_/ /_/ /_/\__,_/_/  /_/|_|
    /_/

[INFO] You did not provide an explicit timeout in the client options. Assuming default of 10 seconds.
[INFO] Connected to OpenSearch cluster [380d8fd64dd85b5f77c0ad81b0799e1e] version [1.1.0].

Extracting documents for index [movies] for test mode...      1000/1000 docs [100.0% done]
Extracting documents for index [movies]...                    2000/2000 docs [100.0% done]

[INFO] Workload movies has been created. Run it with: opensearch-benchmark --workload-path=/Users/hoangia/Desktop/workloads/movies

-----------------------------------
[INFO] ✅ SUCCESS  (took 2 seconds)
-----------------------------------
```

在建立工作負載的過程中，OpenSearch Benchmark 會產生下列檔案。您可以在 `--output-path` 選項指定的目錄中存取這些檔案。

- `workload.json`：包含一般工作負載規格。
- `<index>.json`：包含所擷取索引的對應與設定。
- `<index>-documents.json`：包含所擷取索引中每份文件的來源。任何以 `-1k` 為字尾的來源僅涵蓋工作負載文件語料庫的一部分，且只在工作負載以測試模式執行時使用。

預設情況下，OpenSearch Benchmark 並未包含產生查詢的參考。由於您最了解自己的資料，我們建議在 `workload.json` 中新增一個符合您索引規格的查詢。請以下列 `match_all` 查詢作為新增至工作負載的查詢範例：

```json
{
      "operation": {
        "name": "query-match-all",
        "operation-type": "search",
        "body": {
          "query": {
            "match_all": {}
          }
        }
      },
      "clients": 8,
      "warmup-iterations": 1000,
      "iterations": 1000,
      "target-throughput": 100
    }
```

### 在沒有現有叢集的情況下建立工作負載

如果您想建立自訂工作負載，但沒有含已編製索引資料的現有 OpenSearch 叢集，您可以透過直接建置工作負載原始檔來建立工作負載。您只需要可匯出為 JSON 格式的資料即可。

若要使用原始檔建置工作負載，請為您的工作負載建立一個目錄，並執行下列步驟：

1. 建置一個 `<index>-documents.json` 檔案，其中包含組成工作負載文件語料庫的文件列，並存放所有要匯入叢集並進行查詢的資料。下列範例顯示一個 `movies-documents.json` 檔案的前幾列，其中包含有關知名電影的文件列：

  ```json
  {"title": "Back to the Future", "director": "Robert Zemeckis", "revenue": "$212,259,762 USD", "rating": "8.5 out of 10",  "image_url": "https://imdb.com/images/32"}
  {"title": "Avengers: Endgame", "director": "Anthony and Joe Russo", "revenue": "$2,800,000,000 USD", "rating": "8.4 out   of 10", "image_url": "https://imdb.com/images/2"}
  {"title": "The Grand Budapest Hotel", "director": "Wes Anderson", "revenue": "$173,000,000 USD", "rating": "8.1 out of 10", "image_url": "https://imdb.com/images/65"}
  {"title": "The Godfather: Part II", "director": "Francis Ford Coppola", "revenue": "$48,000,000 USD", "rating": "9 out of 10", "image_url": "https://imdb.com/images/7"}
  ```

2. 在同一個目錄中，建置一個 `index.json` 檔案。工作負載會使用此檔案作為 `<index>-documents.json` 中所含文件的資料對應與索引設定參考。下列範例會建立上一個步驟中 `movie-documents.json` 資料專屬的對應與設定：

    ```json
    {
    "settings": {
        "index.number_of_replicas": 0
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
        "title": {
            "type": "text"
        },
        "director": {
            "type": "text"
        },
        "revenue": {
            "type": "text"
        },
        "rating": {
            "type": "text"
        },
        "image_url": {
            "type": "text"
        }
        }
    }
    }
    ```

3. 接著，建置一個 `workload.json` 檔案，提供工作負載的高階概觀，並決定工作負載如何執行基準測試。`workload.json` 檔案包含下列區段：

   - `indices`：定義要在 OpenSearch 叢集中建立的索引名稱，並使用上一個步驟所建立工作負載的 `index.json` 檔案中的對應。
   - `corpora`：定義語料庫與原始檔，包括：
      - `document-count`：`<index>-documents.json` 中的文件數。若要取得準確的文件數，請執行 `wc -l <index>-documents.json`。
      - `uncompressed-bytes`：索引內的位元組數。若要取得準確的位元組數，請在 macOS 上執行 `stat -f %z <index>-documents.json`，或在 GNU/Linux 上執行 `stat -c %s <index>-documents.json`。或者，也可以執行 `ls -lrt | grep <index>-documents.json`。
   - `schedule`：定義工作負載的作業順序與可用的測試程序。

下列範例 `workload.json` 檔案提供 `movies` 工作負載的進入點。`indices` 區段會建立一個名為 `movies` 的索引。語料庫區段參照在步驟一中建立的原始檔 `movie-documents.json`，並提供文件數與未壓縮位元組數。最後，排程區段定義工作負載被叫用時執行的幾項作業，包括：

- 刪除任何現有名為 `movies` 的索引。
- 根據 `movie-documents.json` 的資料與 `index.json` 的對應，建立一個名為 `movies` 的索引。
- 驗證叢集健康狀態良好，並且可以匯入新索引。
- 將 `workload.json` 的資料語料庫匯入叢集。
- 查詢結果。

    ```json
    {
    "version": 2,
    "description": "Tutorial benchmark for OpenSearch Benchmark",
    "indices": [
        {
        "name": "movies",
        "body": "index.json"
        }
    ],
    "corpora": [
        {
        "name": "movies",
        "documents": [
            {
            "source-file": "movies-documents.json",
            "document-count": 11658903, # Fetch document count from command line
            "uncompressed-bytes": 1544799789 # Fetch uncompressed bytes from command line
            }
        ]
        }
    ],
    "schedule": [
        {
        "operation": {
            "operation-type": "delete-index"
        }
        },
        {
        "operation": {
            "operation-type": "create-index"
        }
        },
        {
        "operation": {
            "operation-type": "cluster-health",
            "request-params": {
            "wait_for_status": "green"
            },
            "retry-until-success": true
        }
        },
        {
        "operation": {
            "operation-type": "bulk",
            "bulk-size": 5000
        },
        "warmup-time-period": 120,
        "clients": 8
        },
        {
        "operation": {
            "operation-type": "force-merge"
        }
        },
        {
        "operation": {
            "name": "query-match-all",
            "operation-type": "search",
            "body": {
            "query": {
                "match_all": {}
            }
            }
        },
        "clients": 8,
        "warmup-iterations": 1000,
        "iterations": 1000,
        "target-throughput": 100
        }
    ]
    }
    ```

語料庫區段參照在步驟一中建立的原始檔 `movie-documents.json`，並提供文件數與未壓縮位元組數。最後，排程區段定義工作負載被叫用時執行的幾項作業，包括：

- 刪除任何現有名為 `movies` 的索引。
- 根據 `movie-documents.json` 的資料與 `index.json` 的對應，建立一個名為 `movies` 的索引。
   - 驗證叢集健康狀態良好，並且可以匯入新索引。
   - 將 `workload.json` 的資料語料庫匯入叢集。
   - 查詢結果。



對於所有建立的工作負載檔案，請執行測試以驗證工作負載可正常運作。若要驗證工作負載，請執行下列命令，並將 `--workload-path` 替換為您的工作負載目錄路徑：

```bash
opensearch-benchmark list workloads --workload-path=</path/to/workload/>
```

## 叫用您的自訂工作負載

使用 `opensearch-benchmark run` 命令來叫用您的新工作負載，並對您的 OpenSearch 叢集執行基準測試，如下列範例所示。將 `--workload-path` 取代為您自訂工作負載的路徑，將 `--target-host` 取代為您叢集的 `host:port` 配對，並將 `--client-options` 取代為存取叢集所需的任何授權選項。

```bash
opensearch-benchmark run \
--pipeline="benchmark-only" \
--workload-path="<PATH OUTPUTTED IN THE OUTPUT OF THE CREATE-WORKLOAD COMMAND>" \
--target-host="<CLUSTER ENDPOINT>" \
--client-options="basic_auth_user:'<USERNAME>',basic_auth_password:'<PASSWORD>'"
```

測試結果會出現在 `workloads.json` 中 `--output-path` 選項所設定的目錄中。

## 進階選項

您可以使用下列進階選項來增強自訂工作負載的功能。

### 測試模式

如果您想要在測試模式中執行測試，以確保工作負載如預期運作，請將 `--test-mode` 選項新增至 `run` 命令。測試模式只會匯入所提供每個索引的前 1,000 份文件，並對它們執行查詢操作。

若要使用測試模式，請使用下列命令建立一個 `<index>-documents-1k.json` 檔案，其中包含 `<index>-documents.json` 的前 1000 份文件：

```bash
head -n 1000 <index>-documents.json > <index>-documents-1k.json
```

然後，使用選項 `--test-mode` 執行 `opensearch-benchmark run`。測試模式會執行工作負載測試的快速版本。

```bash
opensearch-benchmark run \
--pipeline="benchmark-only"  \
--workload-path="<PATH OUTPUTTED IN THE OUTPUT OF THE CREATE-WORKLOAD COMMAND>" \
--target-host="<CLUSTER ENDPOINT>" \
--client-options"basic_auth_user:'<USERNAME>',basic_auth_password:'<PASSWORD>'" \
--test-mode
```

### 為測試程序新增變化

使用自訂工作負載數次之後，您可能會想要使用相同的工作負載，但以不同的順序執行工作負載的操作。您不需要建立新的工作負載或直接重新整理程序，而是可以提供測試程序來變化工作負載操作。

若要為工作負載操作新增變化，請前往您的 `workload.json` 檔案，並將 `schedule` 區段取代為 `test_procedures` 陣列，如下列範例所示。陣列中的每個項目包含下列內容：

- `name`：測試程序的名稱。
- `default`：設為 `true` 時，如果未指定其他測試程序，OpenSearch Benchmark 會預設為工作負載中指定為 `default` 的測試程序。
- `schedule`：測試程序將執行的所有操作。


```json
"test_procedures": [
    {
      "name": "index-and-query",
      "default": true,
      "schedule": [
        {
          "operation": {
            "operation-type": "delete-index"
          }
        },
        {
          "operation": {
            "operation-type": "create-index"
          }
        },
        {
          "operation": {
            "operation-type": "cluster-health",
            "request-params": {
              "wait_for_status": "green"
            },
            "retry-until-success": true
          }
        },
        {
          "operation": {
            "operation-type": "bulk",
            "bulk-size": 5000
          },
          "warmup-time-period": 120,
          "clients": 8
        },
        {
          "operation": {
            "operation-type": "force-merge"
          }
        },
        {
          "operation": {
            "name": "query-match-all",
            "operation-type": "search",
            "body": {
              "query": {
                "match_all": {}
              }
            }
          },
          "clients": 8,
          "warmup-iterations": 1000,
          "iterations": 1000,
          "target-throughput": 100
        }
      ]
    }
  ]
}
```

### 分開操作與測試程序

如果您想要讓 `workload.json` 檔案更容易閱讀，可以將操作和測試程序分開放到不同的目錄，並在 `workload.json` 中參考每個項目的路徑。若要分開操作與程序，請執行下列步驟：

1. 將所有測試程序新增至單一檔案。您可以為檔案取任何名稱。因為前述的 `movies` 工作負載包含索引工作和查詢，所以此步驟將測試程序檔案命名為 `index-and-query.json`。
2. 將所有操作新增至名為 `operations.json` 的檔案。
3. 在 `workloads.json` 中參考新檔案，方法是新增下列語法，並將 `parts` 取代為每個檔案的相對路徑，如下列範例所示：

    ```json
    "operations": [
        {% raw %}{{ benchmark.collect(parts="operations/*.json") }}{% endraw %}
    ]
    # Reference test procedure files in workload.json
    "test_procedures": [
        {% raw %}{{ benchmark.collect(parts="test_procedures/*.json") }}{% endraw %}
    ]
    ```

## 後續步驟

- 若要調整工作負載，使其更貼近您的生產環境，請參閱[微調自訂工作負載]({{site.url}}{{site.baseurl}}/benchmark/finetune-workloads/)。
- 若要將您的工作負載貢獻給 OpenSearch Project，請參閱[分享自訂工作負載]({{site.url}}{{site.baseurl}}/benchmark/contributing-workloads/)。
- 如需設定 OpenSearch Benchmark 的詳細資訊，請參閱[設定 OpenSearch Benchmark]({{site.url}}{{site.baseurl}}/benchmark/configuring-benchmark/)。
- 若要顯示 OpenSearch Benchmark 預先封裝的工作負載清單，請參閱 [`opensearch-benchmark-workloads`](https://github.com/opensearch-project/opensearch-benchmark-workloads) 儲存庫。
