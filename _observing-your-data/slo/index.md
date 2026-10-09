---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "SLO"
nav_order: 125
has_children: false
redirect_from:
  - /observing-your-data/slo/
---

# 服務等級目標
**於 3.7 版推出**
{: .label .label-purple }

這是實驗性功能，不建議在正式環境中使用。如欲了解功能的最新進展，或想提供意見回饋，歡迎前往 [OpenSearch 論壇](https://forum.opensearch.org/)參與討論。
{: .warning}

服務等級目標 (SLO) 可讓您為服務定義可用性與延遲目標，將支援的記錄與警示規則部署到與 Prometheus 相容的 ruler，並在 OpenSearch Dashboards 的專屬檢視中追蹤應用程式健康狀態、錯誤預算與預算消耗率 (burn rate)。

SLO 會彙整來自 OpenSearch 監視器與 Prometheus 警示規則的警示，讓您不必在多個工具之間切換，即可跨資料來源監控服務健康狀態。

當您建立 SLO 時，OpenSearch Dashboards 會根據您的組態產生 Prometheus 記錄與警示規則，並將其部署到與 Prometheus 相容的 ruler。這些規則會追蹤每個目標的健康狀態、達成率與剩餘錯誤預算。

下表定義 SLO 與 SLI 相關詞彙。

| 詞彙 | 定義 |
| :--- | :--- |
| 服務等級指標 (SLI) | 服務效能的量化衡量指標，例如可用性或延遲。支援的 SLI 類型包括 `availability`、`latency_threshold` 與 `custom`。 |
| 服務等級目標 (SLO) | 針對一或多個 SLI 的目標達成水準，以單一時間範圍進行評估。每個 SLO 包含一或多個目標。 |
| 目標 | SLI 的目標值，以 `0.5` 到 `0.99999` 之間的小數表示 (例如 `0.999`)。每個目標都會產生自己的一組記錄與警示規則。 |
| 時間範圍 | 評估 SLO 的滾動期間 (例如 `7d`、`28d`、`30d`)。目前尚不支援日曆時間範圍。 |
| 錯誤預算 | 時間範圍內允許的失敗事件比例。當錯誤預算降至零以下時，即表示目標已遭違反。 |
| 消耗率 | 相對於時間範圍，錯誤預算被消耗的速率。用於依不同嚴重性層級觸發警示。 |
| SLO 模式 | 控制警示是否啟用。在 `active` 模式下，會同時部署記錄與警示規則。在 `shadow` 模式下，只會部署記錄規則，這對於在啟用警示前驗證 SLO 很有用。 |
| 資料來源 | SLO 所使用的 `DirectQuery` Prometheus 連線。每個 SLO 都繫結至單一資料來源。 |
| 工作區 | SLO 所屬的 OpenSearch Dashboards 工作區。每個工作區都有自己的一組 SLO 與 ruler 命名空間。 |

## 先決條件

使用 SLO 之前，請先完成下列設定步驟。

### 啟用功能

SLO 預設為停用。如欲啟用，請將下列設定新增至 `opensearch_dashboards.yml`：

```yaml
workspace.enabled: true
explore.enabled: true
explore.discoverTraces.enabled: true
observability.slo.enabled: true
```
{% include copy.html %}

然後重新啟動 OpenSearch Dashboards。

### 可觀測性工作區

SLO 功能可在可觀測性[工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/)中使用。如欲建立工作區，請依照下列步驟操作：

1. 前往 OpenSearch Dashboards 首頁。
2. 選取 **Create workspace**。
3. 輸入工作區名稱。
4. 選取 **Observability** 使用案例。
5. 選取 **Create workspace**。

### 與 Prometheus 相容的 ruler

SLO 會透過 `DirectQuery` 資源代理，將記錄與警示規則部署到與 Prometheus 相容的 ruler（Cortex 或 Grafana Mimir）。ruler 必須支援下列 API 端點：

- `POST /api/v1/rules/{namespace}` -- 建立或更新規則群組。
- `DELETE /api/v1/rules/{namespace}/{groupName}` -- 刪除規則群組。

指定工作區的規則群組會寫入命名空間 `slo-generated-<workspace-id>`。租用戶身分（例如 `X-Scope-OrgID`）會在 [Prometheus 連接器]({{site.url}}{{site.baseurl}}/dashboards/management/connect-prometheus/)的設定中指定。

### 資料來源

每個 SLO 都繫結至單一資料來源，該資料來源必須是已註冊的 `DirectQuery` Prometheus 連線。如需設定 Prometheus 資料來源的相關資訊，請參閱[將 Prometheus 連線至 OpenSearch]({{site.url}}{{site.baseurl}}/dashboards/management/connect-prometheus/)。

### 資料先決條件

SLI 定義會決定 ruler 必須能夠查詢哪些資料：

- **可用性與延遲閾值 SLI** 需要在已設定的後端中存在具名的 Prometheus 計數器或直方圖指標。應用程式效能監控（APM）服務範本預期會使用由 [OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) 產生的 span 衍生 Rate、Error、Duration（RED）指標。OpenTelemetry（OTel）語意慣例範本則預期會使用對應的 HTTP、RPC、資料庫用戶端、訊息傳遞或生成式 AI 指標。
- **自訂 SLI** 需要您的 PromQL 運算式能夠在後端成功評估。

## 存取 SLO

如欲存取 SLO，請從首頁選取您的可觀測性工作區，或者如果您還沒有工作區，請建立一個（請參閱[可觀測性工作區](#observability-workspace)）。然後前往 **Application Performance** > **SLOs**。


## 建立 SLO

如欲建立 SLO，請依照下列步驟操作：

1. 在 **SLOs** 檢視中，選擇 **Create SLO**。
2. 選取範本。範本分為下列類別：
   - **APM service SLOs**：以 [OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) 的 RED 指標為基礎的 SLI。範本包括 **APM service availability**、**APM service latency**、**APM dependency availability** 與 **APM dependency latency**。
   - **OTel semantic convention metrics**：以標準 OTel 指標為基礎的 SLI。範本包括 **HTTP availability**、**HTTP latency**、**RPC/gRPC availability**、**RPC/gRPC latency**、**Database client latency**、**Messaging processing latency** 與 **GenAI invocation availability**。
   - **Custom**：用於自訂 PromQL 運算式的空白 **Custom PromQL** 範本。
3. 在精靈中設定 SLO。精靈包含下列區段：
   - **Identity**：唯一名稱、描述與資料來源 (已註冊的 DirectQuery Prometheus 連線)。
   - **Window & mode**：滾動時間範圍 (例如 `28d`) 與選用的 shadow 模式，後者會部署記錄規則但不發出警示。
   - **Service & owner**：服務名稱與負責團隊。
   - **SLI**：對於預先建置的範本，SLI 類型與指標已預先設定。您可以選擇性地新增維度 (標籤篩選條件) 來縮小查詢範圍。對於 **Custom PromQL** 範本，您需自行提供 PromQL 運算式---可以是分開的正常事件與總事件查詢，或是單一預先計算的錯誤率查詢。
   - **Probe SLI**：在可設定的回溯期間 (`1h`、`24h` 或 `7d`) 內，針對 Prometheus 後端測試建議的查詢，讓您可以在建立 SLO 之前先確認查詢會傳回資料。
   - **Objectives**：介於 `0.5` 與 `0.99999` 之間的一或多個目標值 (例如 `99.9%`)。對於延遲 SLI，每個目標也會設定延遲界限。
   - **Advanced**：消耗率警示層級、預算警告與補充警示。
   - **Exclusion windows**：SLO 忽略測量值的時間期間 (例如維護時間範圍或部署凍結期)。
   - **Labels & annotations**：會傳播至所產生規則的選用中繼資料。
   - **Rule preview**：將部署至 ruler 的記錄與警示規則唯讀預覽。
4. 選擇 **Create SLO**。規則會經過驗證並部署至 ruler。如果 ruler 拒絕這些規則，系統會顯示錯誤，且不會儲存 SLO。

## 監控 SLO

**SLOs** 清單會顯示每個 SLO 的目前狀態、達成率、剩餘錯誤預算與走勢圖。


下表說明 SLO 狀態。

| 狀態 | 說明 |
| :--- | :--- |
| `ok` | 所有目標都高於目標值。 |
| `warning` | 至少有一個目標消耗預算的速度比預期快。 |
| `breached` | 至少有一個目標已用盡其錯誤預算。 |
| `no_data` | SLI 查詢在評估時間範圍內未傳回任何資料。 |
| `stale` | 最新的資料樣本比預期舊，這可能表示資料來源連線有問題。 |
| `disabled` | SLO 已停用。 |
| `rules_missing` | ruler 上不存在預期的記錄規則。 |

如欲檢視特定 SLO 的詳細資料，請在清單中選取該 SLO。詳細資料頁面會顯示每個目標的達成率、剩餘錯誤預算、預算消耗率，以及已部署的記錄與警示規則。

## 編輯 SLO

如欲更新 SLO，請在清單中選取該 SLO，然後選擇 **Edit**。只有您變更的欄位會更新。更新成功後，規則群組會重新產生並重新部署至 ruler。

您也可以變更 SLO 模式，而不必編輯完整組態：

- **Disable**：從 ruler 移除規則群組並停止警示。
- **Enable**：重新部署規則群組並恢復狀態計算。
- **Shadow mode**：保留記錄規則但停止警示。可用於在啟用警示前驗證新的 SLO。

## 刪除 SLO

如欲刪除 SLO，請從清單中選取該 SLO，然後從詳細資料頁面或資料列動作選單中選擇 **Delete**。相關聯的規則群組會從 ruler 移除，且 SLO 組態會遭到刪除。

如果 SLO 與其他 SLO 共用記錄規則 (啟用規則去重時)，則只會釋放參照。共用的規則會在寬限期 (預設為 24 小時) 過後自動移除。

## 組態設定

下表列出 SLO 組態設定。

| 設定 | 預設值 | 說明 |
| :--- | :--- | :--- |
| `observability.slo.enabled` | `false` | 啟用 SLO。需要重新啟動 OpenSearch Dashboards。 |
| `observability.slo.ruleDedup.enabled` | `true` | 允許使用相同查詢的多個 SLO 在 ruler 上共用單一組記錄規則，以減少重複評估。 |
| `observability.slo.reconciler.enabled` | `true` | 啟用自動清理不再被任何 SLO 參照的共用記錄規則。 |
| `observability.slo.reconciler.intervalMs` | `300000` (5 分鐘) | 清理程序的執行頻率，以毫秒為單位。 |
| `observability.slo.reconciler.graceMs` | `86400000` (24 小時) | 在共用規則的所有參照都移除後，等待多久才從 ruler 刪除該規則，以毫秒為單位。 |

## 疑難排解

下表說明常見問題及其解決方案。

| 問題 | 解決方案 |
| :--- | :--- |
| ruler 在建立或更新 SLO 時傳回錯誤。 | 錯誤詳細資料會顯示在精靈中。請修正根本問題 (例如驗證失敗或 PromQL 格式錯誤) 並重新提交。 |
| SLO 顯示 `rules_missing` 或 `no_data`。 | 使用詳細資料頁面上的 **Rule health** 動作來檢查 ruler 與 SLI 查詢。使用 **Repair** 重新部署缺少的規則群組。 |

## 限制

SLO 有下列限制：

- SLI 評估僅支援 Prometheus 資料來源。
- 僅支援單一 SLI。結合多個 SLO 的複合式 SLO 目前尚不提供。
- 僅支援滾動時間範圍。日曆時間範圍 (`week`、`month`、`quarter`) 目前尚不提供。
- 僅支援多時間範圍、多消耗率 (MWMBR) 警示策略。
- 可以設定排除時間範圍，但目前尚不會進行評估。

## 相關文件

- [應用程式效能監控]({{site.url}}{{site.baseurl}}/observing-your-data/apm/)
- [警示]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/)
