---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定 Log4j"
parent: Managing OpenSearch Data Prepper
nav_order: 20
---

# 設定 Log4j

您可以在 OpenSearch Data Prepper 中使用 Log4j 來設定記錄。

## 記錄 

Data Prepper 使用 [SLF4J](https://www.slf4j.org/) 搭配 [Log4j 2 繫結](https://logging.apache.org/log4j/2.x/log4j-slf4j-impl.html)。

Data Prepper 會從 Data Prepper 主目錄中的 `config/log4j2-rolling.properties` 檔案讀取其 Log4j 2 組態。若要自訂記錄，請編輯或取代此檔案。在 Docker 中，檔案路徑為 `/usr/share/data-prepper/config/log4j2-rolling.properties`。

若要使用位於其他位置的組態檔，請在啟動 Data Prepper 之前，於 `JAVA_OPTS` 環境變數中設定 `log4j.configurationFile` 系統屬性：

```bash
export JAVA_OPTS="-Dlog4j.configurationFile=/path/to/log4j2.properties"
bin/data-prepper
```
{% include copy.html %}

在 Docker 中，請使用 `-e` 選項傳遞環境變數，並將組態檔掛載至容器中：

```bash
docker run --name data-prepper \
  -e JAVA_OPTS="-Dlog4j.configurationFile=/usr/share/data-prepper/custom/log4j2.properties" \
  -v ${PWD}/log4j2.properties:/usr/share/data-prepper/custom/log4j2.properties \
  -v ${PWD}/pipelines.yaml:/usr/share/data-prepper/pipelines/pipelines.yaml \
  opensearchproject/data-prepper:latest
```
{% include copy.html %}

如需 Log4j 2 組態的更多資訊，請參閱 [Log4j 2 組態文件](https://logging.apache.org/log4j/2.x/manual/configuration.html)。

