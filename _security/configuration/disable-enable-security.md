---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "停用與啟用 Security 外掛程式"
parent: Configuration
nav_order: 65
has_toc: true
redirect_from:
 - /security-plugin/configuration/disable/
 - /security/configuration/disable/
---

# 停用與啟用 Security 外掛程式

Security 外掛程式會隨 OpenSearch 一併預設安裝，但您可以暫時停用它，或將它完全移除。停用此外掛程式需要修改 `opensearch.yml` 檔案；您可能會為了簡化測試而這麼做。若要完全移除 Security 外掛程式，則需要更實質的變更。例如，當您使用自己的安全性解決方案，或基於開發目的需要移除它時，就可能想移除此外掛程式。

停用或移除外掛程式會使 Security 外掛程式的組態索引暴露在外。如果該索引包含敏感資訊，請務必透過其他方式加以保護。如果您不再需要該索引，請將它刪除。
{: .warning }

停用、移除或安裝 Security 外掛程式需要完整重新啟動叢集，因為在此過程中，各個節點無法彼此通訊。
{: .warning}

## 停用或啟用 Security 外掛程式

您可以透過編輯 `opensearch.yml` 檔案來停用 Security 外掛程式：

```yml
plugins.security.disabled: true
```
接著，您可以移除 `plugins.security.disabled` 設定來啟用外掛程式。

## 移除與新增 Security 外掛程式

您可以從 OpenSearch 執行個體中完全移除 Security 外掛程式。請注意，OpenSearch Dashboards 只能連接安全的叢集，因此如果您解除安裝 Security 外掛程式，也必須一併解除安裝 OpenSearch Dashboards 外掛程式。

### 從 OpenSearch 移除 Security 外掛程式

請執行下列步驟，從 OpenSearch 移除外掛程式。

1. 停用分片配置並停止所有節點，以免叢集重新啟動時分片移動：

   ```json
   curl -XPUT "https://localhost:9200/_cluster/settings" -u "admin:<password>" -H 'Content-Type: application/json' -d '{
      "transient": {
         "cluster.routing.allocation.enable": "none"
      }
   }'
   ```
   {% include copy.html %}
2. 從 `opensearch.yml` 刪除所有 `plugins.security.*` 組態項目。
3. 使用下列命令解除安裝 Security 外掛程式：

   ```bash
   ./bin/opensearch-plugin remove opensearch-security
   ```
4. 重新啟動節點並啟用分片配置：
   ```json
   curl -XPUT "http://localhost:9200/_cluster/settings" -H 'Content-Type: application/json' -d '{
    "transient": {
      "cluster.routing.allocation.enable": "all"
      }
   }'
   ```

若要在 Docker 映像上執行這些步驟，請參閱[使用外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/docker/#working-with-plugins)。
{: .note }

### 從 OpenSearch Dashboards 移除 Security 外掛程式

如果您在 `opensearch.yml` 中停用 Security 外掛程式，但仍想使用 OpenSearch Dashboards，就必須移除對應的 OpenSearch Dashboards Security 外掛程式。如需更多資訊，請參閱[移除外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/plugins/#removing-plugins)。

請參考下列安裝類型來移除 OpenSearch Dashboards 外掛程式。

#### Docker

1. 從 `opensearch_dashboards.yml` 移除所有 Security 外掛程式組態設定，或將範例檔案移動到與 `Dockerfile` 相同的資料夾：

   ```yml
   ---
   server.name: opensearch-dashboards
   server.host: "0.0.0.0"
   opensearch.hosts: http://localhost:9200
   ```

1. 建立新的 `Dockerfile`：

   ```
   FROM opensearchproject/opensearch-dashboards:{{site.opensearch_dashboards_version}}
   RUN /usr/share/opensearch-dashboards/bin/opensearch-dashboards-plugin remove securityDashboards
   COPY --chown=opensearch-dashboards:opensearch-dashboards opensearch_dashboards.yml /usr/share/opensearch-dashboards/config/
   ```

1. 若要建置新的 Docker 映像，請執行下列命令：

   ```bash
   docker build --tag=opensearch-dashboards-no-security .
   ```

1. 在 `docker-compose.yml` 中，將 `opensearchproject/opensearch-dashboards:{{site.opensearch_dashboards_version}}` 變更為 `opensearch-dashboards-no-security`。
1. 將 `OPENSEARCH_HOSTS` 或 `opensearch.hosts` 變更為 `http://`，而不是 `https://`。
1. 輸入 `docker compose up`。

#### Tarball

1. 前往 OpenSearch Dashboards 安裝資料夾中的 `/bin` 目錄，並按下 `Ctrl + C` 停止正在執行的 OpenSearch Dashboards 執行個體。

1. 執行下列命令以解除安裝 Security 外掛程式：

   ```bash
   ./bin/opensearch-dashboards-plugin remove securityDashboards
   ```

1. 從 `opensearch_dashboards.yml` 檔案移除所有 Security 外掛程式組態設定，或使用下列範例檔案：

   ```yml
   ---
   server.name: opensearch-dashboards
   server.host: "0.0.0.0"
   opensearch.hosts: http://localhost:9200
   ```
   
1. 啟動 OpenSearch Dashboards：
   ```bash
   ./bin/opensearch-dashboards
   ```
   
#### RPM 與 Debian

1. 使用下列命令停止正在執行的 OpenSearch Dashboards 執行個體：

   ```bash
   sudo systemctl stop opensearch-dashboards
   ```

1. 前往 OpenSearch Dashboards 資料夾 `/usr/share/opensearch-dashboards`，並執行下列命令以解除安裝 Security 外掛程式：

   ```bash
   ./bin/opensearch-dashboards-plugin remove securityDashboards
   ```

1. 從 `opensearch_dashboards.yml` 檔案移除所有 Security 外掛程式組態設定，或將範例檔案放置於 `/etc/opensearch_dashboards` 資料夾：

   ```yml
   ---
   server.name: opensearch-dashboards
   server.host: "0.0.0.0"
   opensearch.hosts: http://localhost:9200
   ```
1. 啟動 OpenSearch Dashboards：
   ```bash
   sudo systemctl start opensearch-dashboards
   ```

### 安裝 Security 外掛程式

使用下列步驟重新安裝外掛程式：

1. 停用分片配置並停止所有節點，以免叢集重新啟動時分片移動：

    ```json
    curl -XPUT "http://localhost:9200/_cluster/settings" -H 'Content-Type: application/json' -d '{
      "transient": {
        "cluster.routing.allocation.enable": "none"
        }
     }'
    ```
    {% include copy.html %}
 
2. 使用其中一種[安裝方法]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/#installing-plugins)，在叢集中的所有節點上安裝 Security 外掛程式：

    ```bash
    bin/opensearch-plugin install opensearch-security
    ```
    {% include copy.html %}
    
3. 在 `opensearch.yml` 中新增 TLS 加密所需的組態。有關需要設定的設定，請參閱[組態]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/security-settings/)。

4. 建立 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 變數。如需更多資訊，請參閱[設定自訂管理員密碼]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/#setting-up-a-custom-admin-password)。
  
5. 重新啟動節點並重新啟用分片配置：

   ```json
   curl -XPUT "https://localhost:9200/_cluster/settings" -u "admin:<password>" -H 'Content-Type: application/json' -d '{
     "transient": {
      "cluster.routing.allocation.enable": "all"
     }
   }'
   ```
   {% include copy.html %}

### 在 OpenSearch Dashboards 上安裝 Security 外掛程式

使用下列步驟在 OpenSearch Dashboards 上重新安裝外掛程式：

1. 停止執行您的 OpenSearch Dashboards 叢集。
2. 安裝 Security 外掛程式：

   ```bash
      ./bin/opensearch-dashboards-plugin install securityDashboards
   ```
   
4. 在 `opensearch_dashboards.yml` 檔案中新增必要的[組態]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/tls/)設定。
5. 啟動 OpenSearch Dashboards。如果外掛程式安裝成功，系統會提示您輸入登入憑證。
