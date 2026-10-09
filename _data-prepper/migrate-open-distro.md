---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "從 Open Distro 遷移"
nav_order: 30
redirect_from:
  - /clients/data-prepper/migrate-open-distro/
---

# 從 Open Distro 遷移

現有使用者可以從 Open Distro Data Prepper 遷移至 OpenSearch Data Prepper。從 Data Prepper 1.1 版開始，OpenSearch Data Prepper 只有一種發行版本。

## 變更您的管線組態

`elasticsearch` sink 已變更為 `opensearch`。因此，請變更您現有的管線，改用 `opensearch` 外掛程式，而非 `elasticsearch`。

雖然 Data Prepper 外掛程式的名稱為 `opensearch`，它仍與 Open Distro 及 Elasticsearch 7.x 相容。
{: .note}

## 更新 Docker 映像

在您的 Data Prepper Docker 組態中，將 `amazon/opendistro-for-elasticsearch-data-prepper` 調整為 `opensearchproject/data-prepper`。這項變更會下載最新的 Data Prepper Docker 映像。

## 後續步驟

如需 Data Prepper 組態的詳細資訊，請參閱[開始使用 OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/clients/data-prepper/get-started/)。
