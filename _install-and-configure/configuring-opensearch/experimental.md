---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "實驗性功能旗標"
parent: Configuring OpenSearch
nav_order: 180
---

# 實驗性功能旗標

OpenSearch 版本可能包含實驗性功能，您可以視需要啟用或停用這些功能。視安裝類型而定，有數種方法可以啟用功能旗標。

## 在 opensearch.yml 中啟用

如果您正在執行 OpenSearch 叢集，並且想要在組態檔案中啟用功能旗標，請將下列這一行新增至 `opensearch.yml`：

```yaml
opensearch.experimental.feature.<feature_name>.enabled: true
```
{% include copy.html %}

## 在 Docker 容器上啟用

如果您正在執行 Docker，請將下列這一行新增至 `docker-compose.yml` 中的 `opensearch-node` > `environment` 區段下：

```bash
OPENSEARCH_JAVA_OPTS="-Dopensearch.experimental.feature.<feature_name>.enabled=true"
```
{% include copy.html %}

## 在 tarball 安裝上啟用

若要在 tarball 安裝上啟用功能旗標，請在 `config/jvm.options` 或 `OPENSEARCH_JAVA_OPTS` 中提供新的 JVM 參數。

### 選項 1：修改 jvm.options

在啟動 `opensearch` 程序之前，將下列幾行新增至 `config/jvm.options`，以啟用該功能及其相依項目：

```bash
-Dopensearch.experimental.feature.<feature_name>.enabled=true
```
{% include copy.html %}

接著執行 OpenSearch：

```bash
./bin/opensearch
```
{% include copy.html %}

### 選項 2：使用環境變數啟用

除了直接修改 `config/jvm.options` 之外，您也可以使用環境變數來定義這些屬性。您可以在啟動 OpenSearch 時以單一命令完成，或使用 `export` 定義該變數。

若要在啟動 OpenSearch 時以內嵌方式新增功能旗標，請執行下列命令：

```bash
OPENSEARCH_JAVA_OPTS="-Dopensearch.experimental.feature.<feature_name>.enabled=true" ./opensearch-{{site.opensearch_version}}/bin/opensearch
```
{% include copy.html %}

如果您想在執行 OpenSearch 之前另外定義環境變數，請執行下列命令：

```bash
export OPENSEARCH_JAVA_OPTS="-Dopensearch.experimental.feature.<feature_name>.enabled=true"
```
{% include copy.html %}

```bash
./bin/opensearch
```
{% include copy.html %}

## 為 OpenSearch 開發啟用

若要為開發啟用功能旗標，您必須在建置 OpenSearch 之前，將正確的屬性新增至 `run.gradle`。如需如何使用 Gradle 建置 OpenSearch 的相關資訊，請參閱[開發人員指南](https://github.com/opensearch-project/OpenSearch/blob/main/DEVELOPER_GUIDE.md)。

將下列屬性新增至 run.gradle 以啟用該功能：

```gradle
testClusters {
    runTask {
      testDistribution = 'archive'
      if (numZones > 1) numberOfZones = numZones
      if (numNodes > 1) numberOfNodes = numNodes
      systemProperty 'opensearch.experimental.feature.<feature_name>.enabled', 'true'
    }
  }
```
{% include copy.html %}