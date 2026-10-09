---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: OpenSearch CLI
nav_order: 70
has_children: false
redirect_from:
  - /clients/cli/
---

# OpenSearch CLI

OpenSearch CLI 命令列介面 (`opensearch-cli`) 讓您可以從命令列管理 OpenSearch 叢集並自動化執行工作。

`opensearch-cli` 支援 [Anomaly Detection]({{site.url}}{{site.baseurl}}/monitoring-plugins/ad/) 與 [k-NN]({{site.url}}{{site.baseurl}}/search-plugins/knn/) 外掛程式，以及任意的 REST API 路徑。除了其他用途之外，您可以使用 `opensearch-cli` 建立與刪除偵測器、啟動與停止偵測器，以及檢查 k-NN 統計資料。

設定檔 (profile) 讓您可以輕鬆存取不同的叢集，或使用不同的憑證簽署請求。`opensearch-cli` 支援未驗證的請求、HTTP 基本簽署，以及適用於 Amazon Web Services 的 IAM 簽署。

此範例將偵測器 (`ecommerce-count-quantity`) 從預備環境的叢集移至生產環境的叢集：

```bash
opensearch-cli ad get ecommerce-count-quantity --profile staging > ecommerce-count-quantity.json
opensearch-cli ad create ecommerce-count-quantity.json --profile production
opensearch-cli ad start ecommerce-count-quantity.json --profile production
opensearch-cli ad stop ecommerce-count-quantity --profile staging
opensearch-cli ad delete ecommerce-count-quantity --profile staging
```


## 安裝

1. [下載](https://opensearch.org/downloads.html){:target='\_blank'}適用於您電腦的安裝套件並解壓縮。

1. 將 `opensearch-cli` 檔案設為可執行：

   ```bash
   chmod +x ./opensearch-cli
   ```

1. 將該命令加入您的路徑：

   ```bash
   export PATH=$PATH:$(pwd)
   ```

1. 確認 CLI 運作正常：

   ```bash
   opensearch-cli --version
   ```


## 設定檔

設定檔讓您可以輕鬆在不同的叢集與使用者憑證之間切換。若要開始使用，請使用 `--auth-type`、`--endpoint` 與 `--name` 選項執行 `opensearch-cli profile create`：

```bash
opensearch-cli profile create --auth-type basic --endpoint https://localhost:9200 --name docker-local
```

或者，將組態檔儲存至 `~/.opensearch-cli/config.yaml`：

```yaml
profiles:
    - name: docker-local
      endpoint: https://localhost:9200
      user: admin
      password: foobar
    - name: aws
      endpoint: https://some-cluster.us-east-1.es.amazonaws.com
      aws_iam:
        profile: ""
        service: es
```


## 使用方式

`opensearch-cli` 命令使用下列語法：

```bash
opensearch-cli <command> <subcommand> <flags>
```

例如，下列命令會擷取偵測器的相關資訊：

```bash
opensearch-cli ad get my-detector --profile docker-local
```

若要對 OpenSearch CAT API 發出請求，請嘗試下列命令：

```bash
opensearch-cli curl get --path _cat/plugins --profile aws
```

使用 `-h` 或 `--help` 旗標可查看所有支援的命令、子命令，或特定命令的使用方式：

```bash
opensearch-cli -h
opensearch-cli ad -h
opensearch-cli ad get -h
```
