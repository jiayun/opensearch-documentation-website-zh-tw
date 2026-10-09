---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引情境"
parent: Tuning indexes
nav_order: 50
redirect_from:
  - /opensearch/index-context/
---

# 索引情境
**於 2.17 版推出**
{: .label .label-purple }

這是實驗性功能，不建議在正式環境中使用。如需此功能的最新進展，或想提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/)的討論。
{: .warning}

索引情境會宣告索引的使用情境。OpenSearch 會利用情境資訊套用一組預先決定的設定和對應，帶來下列優點：

- 最佳化的效能
- 針對您的特定使用情境調整的設定
- 根據 [OpenSearch Integrations]({{site.url}}{{site.baseurl}}/integrations/) 的精確對應和別名

使用元件範本套用的設定和中繼資料組態，會在您的叢集啟動時自動載入。以 `@abc_template@` 開頭的元件範本或 Application-Based Configuration (ABC) 範本，只能透過 `context` 物件宣告使用，以避免發生組態問題。
{: .warning}

## 啟用索引情境

索引情境需要兩項設定，兩者都在節點啟動時套用。請在叢集中的每個節點上啟用這兩項設定，然後重新啟動節點：

1. 將 `opensearch.experimental.feature.application_templates.enabled` 功能旗標設為 `true`。如需詳細資訊，請參閱[實驗性功能旗標]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/experimental/)。

2. 將下列這行加入 `opensearch.yml`：

   ```yaml
   cluster.application_templates.enabled: true
   ```
   {% include copy.html %}

請勿使用 [Cluster settings API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/) 設定 `cluster.application_templates.enabled`。該 API 會接受更新並傳回 `200`，但節點接著無法套用產生的叢集狀態，並記錄功能旗標未啟用的錯誤。節點會反覆放棄其叢集管理員角色，而每個會變更叢集狀態的請求 (例如建立索引) 都會停止回應，直到您重新啟動節點為止。如果您將該值設為持續性設定，重新啟動後會再次套用。
{: .warning}

`opensearch-system-templates` 外掛程式提供支援每個情境的元件範本。除了最小發行版之外，所有 OpenSearch 發行版都隨附此程式。如果您使用最小發行版，請使用其中一種[安裝方法]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/#installing-plugins)加以安裝。

## 使用 `context` 設定

將 `context` 設定與 Index API 搭配使用，以新增使用情境專屬的情境。

### 注意事項

在建立索引期間使用 `context` 參數時，請考量下列事項：

- 如果您使用 `context` 參數建立索引，則在建立索引或動態設定更新期間，不能包含索引情境中宣告的任何設定。
- 在索引或索引範本上設定索引情境後，該情境即成為永久設定。

當您遵守這些限制時，建議的組態或對應會一致地套用至指定情境內已編製索引的資料。

如果未啟用 `cluster.application_templates.enabled`，宣告情境的請求會遭到拒絕，並傳回 `400`。

### 範例

下列範例顯示如何使用索引情境。

#### 建立索引

以下範例請求會建立索引以儲存指標資料，並將 `metrics` 對應宣告為情境：

```json
PUT /my-metrics-index
{
  "context": {
    "name": "metrics"
  }
}
```
{% include copy-curl.html %}

建立後，情境會新增至索引，並套用對應的設定。若要確認，請傳送下列請求：

```json
GET /my-metrics-index
```
{% include copy-curl.html %}

回應會包含情境及其套用的設定：

```json
{
    "my-metrics-index": {
        "aliases": {},
        "mappings": {},
        "settings": {
            "index": {
                "codec": "zstd_no_dict",
                "refresh_interval": "60s",
                "number_of_shards": "1",
                "provided_name": "my-metrics-index",
                "merge": {
                    "policy": "log_byte_size"
                },
                "context": {
                    "created_version": "1",
                    "current_version": "1"
                },
                ...
            }
        },
        "context": {
            "name": "metrics",
            "version": "_latest"
        }
    }
}
```


#### 建立索引範本

您也可以在建立索引範本時使用 `context` 參數。以下範例請求會建立索引範本，並將情境名稱設為 `logs`：

```json
PUT _index_template/my-logs
{
    "context": {
        "name": "logs",
        "version": "1"
    },
    "index_patterns": [
        "my-logs-*"
    ]
}
```
{% include copy-curl.html %}

所有使用此索引範本建立的索引，都會取得相關聯元件範本提供的中繼資料。若要確認 `context` 已新增至範本，請傳送下列請求：

```json
GET _index_template/my-logs
```
{% include copy-curl.html %}

回應會包含情境：

```json
{
    "index_templates": [
        {
            "name": "my-logs",
            "index_template": {
                "index_patterns": [
                    "my-logs-*"
                ],
                "context": {
                    "name": "logs",
                    "version": "1"
                }
            }
        }
    ]
}
```

如果您的範本直接宣告的任何設定、對應或別名，與情境的後端元件範本之間有任何衝突，在建立索引期間以後者優先。


## 可用的情境範本

下列範本可透過 `context` 參數使用：

- `logs`
- `metrics`
- `nginx-logs`
- `amazon-cloudtrail-logs`
- `amazon-elb-logs`
- `amazon-s3-logs`
- `apache-web-logs`
- `k8s-logs`

如需這些範本的詳細資訊，請參閱 [OpenSearch 系統範本儲存庫](https://github.com/opensearch-project/opensearch-system-templates/tree/main/src/main/resources/org/opensearch/system/applicationtemplates/v1)。

若要檢視叢集上這些範本的目前版本，請使用 `GET /_component_template`。
