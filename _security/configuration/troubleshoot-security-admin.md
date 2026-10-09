---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "securityadmin.sh 疑難排解"
parent: Applying changes to configuration files
grand_parent: Configuration
nav_order: 10
redirect_from:
  - /troubleshoot/security-admin/
---

# securityadmin.sh 疑難排解

使用下列疑難排解步驟，解決位於 `/plugins/opensearch-security/tools/securityadmin.sh` 的 `securityadmin.sh` 指令碼相關問題。如需使用此工具的更多資訊，請參閱[將變更套用至組態檔]({{site.url}}{{site.baseurl}}/security/configuration/security-admin/)。


---

#### 目錄
- TOC
{:toc}


---

## 叢集無法連線

如果 `securityadmin.sh` 無法連線至叢集，它會輸出：

```
OpenSearch Security Admin v6
Will connect to localhost:9200
ERR: Seems there is no opensearch running on localhost:9200 - Will exit
```


### 檢查主機名稱

預設情況下，`securityadmin.sh` 使用 `localhost`。如果您的叢集執行於其他主機，請使用 `-h` 選項指定主機名稱。


### 檢查連接埠

檢查您是否對 HTTP 連接埠（而**非**傳輸連接埠）執行 `securityadmin.sh`。

預設情況下，`securityadmin.sh` 使用 `9200`。如果您的叢集執行於不同的連接埠，請使用 `-p` 選項指定連接埠號碼。


## 沒有任何已設定的節點可用

如果 `securityadmin.sh` 可以連線至叢集，但無法更新組態，它會輸出此錯誤：

```
Contacting opensearch cluster 'opensearch' and wait for YELLOW clusterstate ...
Cannot retrieve cluster state due to: None of the configured nodes are available: [{#transport#-1}{mr2NlX3XQ3WvtVG0Dv5eHw}{localhost}{127.0.0.1:9300}]. This is not an error, will keep on trying ...
```

* 嘗試以 `-icl` 和 `-nhnv` 執行 `securityadmin.sh`。

  如果這樣可行，請檢查您的叢集名稱以及 SSL 憑證中的主機名稱。如果這樣仍不可行，請嘗試以 `--diagnose` 執行 `securityadmin.sh`，並查看診斷追蹤記錄檔。

* 新增 `--accept-red-cluster`，以允許 `securityadmin.sh` 在紅色狀態的叢集上運作。


### 檢查叢集名稱

預設情況下，`securityadmin.sh` 使用 `opensearch` 作為叢集名稱。

如果您的叢集有不同的名稱，您可以使用 `-icl` 選項完全忽略名稱，或使用 `-cn` 選項指定名稱。


### 檢查主機名稱驗證

預設情況下，`securityadmin.sh` 會驗證節點憑證中的主機名稱是否與節點的實際主機名稱相符。

如果不符合（例如您使用的是示範憑證），可以新增 `-nhnv` 選項來停用主機名稱驗證。


### 檢查叢集狀態

預設情況下，`securityadmin.sh` 只會在叢集狀態至少為黃色時執行。

如果您的叢集狀態為紅色，您仍可執行 `securityadmin.sh`，但需要新增 `-arc` 選項。


### 檢查安全性索引名稱

預設情況下，Security 外掛程式使用 `.opendistro_security` 作為組態索引的名稱。如果您在 `opensearch.yml` 中設定了不同的索引名稱，請使用 `-i` 選項指定該名稱。


## 「ERR: DN is not an admin user」

如果用來啟動 `securityadmin.sh` 的 TLS 憑證不是管理員憑證，指令碼會輸出：

```
Connected as CN=node-0.example.com,OU=SSL,O=Test,L=Test,C=DE
ERR: CN=node-0.example.com,OU=SSL,O=Test,L=Test,C=DE is not an admin user
```

執行此指令碼時必須使用管理員憑證。若要深入了解，請參閱[設定超級管理員憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/#configuring-admin-certificates)。

## 使用 diagnose 選項

如需 `securityadmin.sh` 未執行的更多資訊，請新增 `--diagnose` 選項（或其簡短形式 `-dg`）：

```
./securityadmin.sh --diagnose -cd ../../../config/opensearch-security/ -cacert ... -cert ... -key ... -keypass ...
```

指令碼會列印所產生診斷檔案的位置。
