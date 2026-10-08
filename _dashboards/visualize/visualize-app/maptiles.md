---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定 Web Map Service (WMS)"
parent: Configuring maps
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 30
redirect_from:
  - /dashboards/visualize/maptiles/
  - /dashboards/maptiles/
---

{%- comment -%}The `/docs/opensearch-dashboards/maptiles/` redirect is specifically to support the UI links in OpenSearch Dashboards 1.0.0.{%- endcomment -%}

# 設定 Web Map Service

Open Geospatial Consortium (OGC) Web Map Service (WMS) 規格是用於在網路上請求動態地圖的國際規格。OpenSearch Dashboards 內含預設的地圖圖磚。若需要特殊用途的地圖，您可以依照下列步驟在 OpenSearch Dashboards 上設定 WMS：

1. 在 `https://<host>:<port>` 登入 OpenSearch Dashboards。例如，您可以連線至 [https://localhost:5601](https://localhost:5601) 來連線到 OpenSearch Dashboards。預設的使用者名稱和密碼為 `admin`。
2. 選擇 **Management** > **Advanced Settings**。
3. 找到 `visualization:tileMap:WMSdefaults`。
4. 將 `enabled` 變更為 `true`，並加入有效 WMS 伺服器的 URL，如下列範例所示：

   ```json
   {
     "enabled": true,
     "url": "{wms-map-server-url}",
     "options": {
       "format": "image/png",
       "transparent": true
     }
   }
   ```

Web 地圖服務可能有授權費用或限制，您有責任遵守任何此類費用或限制。
{: .note }
