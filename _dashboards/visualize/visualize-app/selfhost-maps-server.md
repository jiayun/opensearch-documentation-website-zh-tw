---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用自行託管的地圖伺服器"
parent: Configuring maps
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 40
redirect_from:
  - /dashboards/visualize/selfhost-maps-server/
  - /dashboards/selfhost-maps-server/
---

# 使用自行託管的地圖伺服器

OpenSearch Dashboards 的自行託管地圖伺服器可讓您在實體隔離 (air-gapped) 環境中存取預設的地圖服務。與 OpenSearch 相容的地圖 URL 包括含有地圖圖磚與向量的地圖資訊清單、地圖圖磚，以及地圖向量。

以下各節說明設定自行託管地圖伺服器並搭配 OpenSearch Dashboards 使用的步驟。

您可以從 OpenSearch 官方的 [Docker Hub 儲存庫](https://hub.docker.com/u/opensearchproject)取得 `maps-server` 映像檔。
{: .note}

## 下載 Docker 映像檔

開啟您的終端機並執行下列命令：

`docker pull opensearchproject/opensearch-maps-server:1.0.0`

## 設定伺服器

執行伺服器之前，您必須先設定地圖圖磚。您有兩種設定選項：使用 OpenSearch 提供的地圖服務圖磚集，或產生點陣圖磚集。

### 選項 1：使用 OpenSearch 提供的地圖服務圖磚集

建立 Docker 磁碟區以存放圖磚集：

`docker volume create tiles-data`

從 OpenSearch 地圖服務下載圖磚集。依所需的縮放層級，提供兩種全球圖磚集：

- 縮放層級 8（https://maps.opensearch.org/offline/planet-osm-default-z0-z8.tar.gz）
- 縮放層級 10（https://maps.opensearch.org/offline/planet-osm-default-z0-z10.tar.gz）

縮放層級 10 的全球圖磚集（壓縮後 2 GB／解壓縮後 6.8 GB）約為縮放層級 8 圖磚集（壓縮後 225 MB／解壓縮後 519 MB）的 10 倍大。
{: .note} 

```
docker run \
    -e DOWNLOAD_TILES=https://maps.opensearch.org/offline/planet-osm-default-z0-z8.tar.gz \
    -v tiles-data:/usr/src/app/public/tiles/data/ \
    opensearch/opensearch-maps-server \
    import
```

### 選項 2：產生點陣圖磚集

若要產生點陣圖磚集，請使用[點陣圖磚產生管線](https://github.com/opensearch-project/maps/tree/main/tiles-generation/cdk)，然後使用圖磚集的絕對路徑建立磁碟區以啟動伺服器。

## 啟動伺服器

使用下列命令，透過 Docker 磁碟區 `tiles-data` 啟動伺服器。下列命令是使用主機 URL「localhost」與連接埠「8080」的範例：

```
docker run \
    -v tiles-data:/usr/src/app/public/tiles/data/ \
    -e HOST_URL='http://localhost' \
    -p 8080:8080 \
    opensearch/opensearch-maps-server \
    run
```

或者，如果您已產生點陣圖磚集，請使用該圖磚集執行伺服器：

```
docker run \
    -v /absolute/path/to/tiles/:/usr/src/app/dist/public/tiles/data/ \
    -p 8080:8080 \
    opensearch/opensearch-maps-server \
    run
```
若要確認伺服器正在執行，請在主機的瀏覽器中開啟下列各個連結，或使用 `curl` 命令（例如 `curl http://localhost:8080/manifest.json`）。

* 地圖資訊清單 URL：`http://localhost:8080/manifest.json`
* 地圖圖磚 URL：`http://localhost:8080/tiles/data/{z}/{x}/{y}.png`
* 地圖圖磚示範 URL：`http://localhost:8080/`

## 搭配 OpenSearch Dashboards 使用自行託管地圖伺服器

若要搭配 OpenSearch Dashboards 使用自行託管地圖伺服器，您可以將參數新增至 `opensearch_dashboards.yml`，或在 OpenSearch Dashboards 中設定預設 WMS 屬性。

### 選項 1：設定 opensearch_dashboards.yml

在 `opensearch_dashboards.yml` 中設定資訊清單 URL：

`map.opensearchManifestServiceUrl: "http://localhost:8080/manifest.json"`

### 選項 2：在 OpenSearch Dashboards 中設定預設 WMS 屬性

1. 在 OpenSearch Dashboards 主控台中，選取 **Dashboards Management** > **Advanced Settings**。
2. 在 **Default WMS properties** 下找到 `visualization:tileMap:WMSdefaults`。
3. 將 `"enabled": false` 變更為 `"enabled": true`，並新增有效地圖伺服器的 URL。

## 授權

Tiles are generated per [Terms of Use for Natural Earth vector map data](https://www.naturalearthdata.com/about/terms-of-use/) and [Copyright and License for OpenStreetMap](https://www.openstreetmap.org/copyright).

## 相關文件

* [設定 Web Map Service (WMS)]({{site.url}}{{site.baseurl}}/dashboards/visualize/maptiles/)
* [座標地圖]({{site.url}}{{site.baseurl}}/dashboards/visualize/coordinate-maps/)
* [區域地圖]({{site.url}}{{site.baseurl}}/dashboards/visualize/region-maps/)
