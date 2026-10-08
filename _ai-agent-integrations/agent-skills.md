---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "代理程式技能"
nav_order: 20
---

# 代理程式技能

使用 OpenSearch 建置應用程式通常包含多個步驟：啟動叢集、設計索引對應、選擇搜尋策略、匯入資料、撰寫查詢，以及評估結果。若缺乏引導，AI 助理必須自行推斷每個步驟，可能導致結果不一致，且需要反覆請求釐清。

[OpenSearch 代理程式技能](https://github.com/opensearch-project/opensearch-agent-skills)是封裝好的工作流程，可教導 AI 程式設計助理如何使用 OpenSearch。每項技能都包含指示、參考資料與可執行的指令碼。您可以用自然語言提問（例如 *「使用 OpenSearch 建置語意搜尋應用程式」*），即可取得可運作的程式碼、已設定的索引，以及可執行的測試。

技能遵循 [Agent Skills 規格](https://agentskills.io/specification)，可搭配任何相容的用戶端使用，包括 Claude Code、Cursor 與 Kiro。

代理程式技能具有下列特性：

- 技能提供結構化的工作流程，涵蓋嵌入模型選擇、搜尋管線組態與測試程序。
- 每項技能都遵循一致的實作模式，產生相同的索引對應、搜尋管線處理器與查詢範本。
- 技能在 AI 用戶端內執行。助理會讀取技能指示，並在您的本機上執行隨附的指令碼。
- 技能可與 [OpenSearch MCP Server]({{site.url}}{{site.baseurl}}/ai-agent-integrations/mcp-server/) 搭配使用。兩者皆已設定時，助理可以遵循技能工作流程，並直接呼叫 API 來檢查叢集狀態或驗證組態。
- 技能是 Markdown 檔案，可依自訂工作流程進行修改或擴充。

## 可用的技能

下表列出可用的技能。

| 類別 | 技能 | 功能 |
|----------|-------|--------------|
| 搜尋 | [`opensearch-launchpad`](https://github.com/opensearch-project/opensearch-agent-skills/tree/main/skills/opensearch-skills/search/opensearch-launchpad) | 建置搜尋應用程式，例如 BM25、語意、混合與代理式搜尋。 |
| 可觀測性 | [`log-analytics`](https://github.com/opensearch-project/opensearch-agent-skills/tree/main/skills/opensearch-skills/observability/log-analytics) | 使用 PPL 查詢與分析記錄檔、識別錯誤模式並偵測異常。 |
| 可觀測性 | [`trace-analytics`](https://github.com/opensearch-project/opensearch-agent-skills/tree/main/skills/opensearch-skills/observability/trace-analytics) | 調查分散式追蹤，包括緩慢的 span、服務對應圖與代理程式呼叫。 |
| 雲端 | [`aws-setup`](https://github.com/opensearch-project/opensearch-agent-skills/tree/main/skills/opensearch-skills/cloud/aws-setup) | 將 OpenSearch 部署至 Amazon OpenSearch Service 或 Amazon OpenSearch Serverless。 |

如需完整的技能清單，請參閱[技能儲存庫](https://github.com/opensearch-project/opensearch-agent-skills)。

## 先決條件

使用代理程式技能之前，請確認您具備下列元件：

- Python 3.11 或更新版本。
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/)。
- 已在本機安裝並執行 Docker。技能會使用 Docker 啟動 OpenSearch 以進行本機實驗。
- AWS 認證資料，如果您打算使用 `aws-setup` 將 OpenSearch 部署至 Amazon OpenSearch Service 或 Amazon OpenSearch Serverless。

## 安裝技能

使用 [`npx skills`](https://agentskills.io) 命令安裝技能。 

若要安裝所有技能，請執行下列命令：

```bash
npx skills add opensearch-project/opensearch-agent-skills
```
{% include copy.html %}

若要安裝單一技能，請執行下列命令：

```bash
npx skills add opensearch-project/opensearch-agent-skills@opensearch-launchpad --full-depth
npx skills add opensearch-project/opensearch-agent-skills@log-analytics --full-depth
npx skills add opensearch-project/opensearch-agent-skills@trace-analytics --full-depth
npx skills add opensearch-project/opensearch-agent-skills@aws-setup --full-depth
```
{% include copy.html %}

### 安裝選項

下表列出可用的安裝選項。

| 選項 | 說明 | 範例 |
| :--- | :--- | :--- |
| `-a <agent>` | 為特定代理程式安裝技能。如需支援的代理程式清單，請參閱 [agentskills.io](https://agentskills.io/)。 | `npx skills add opensearch-project/opensearch-agent-skills -a claude-code` |
| `-g` | 全域安裝技能，讓每個專案都能使用。 | `npx skills add opensearch-project/opensearch-agent-skills -g` |
| `--all` | 為偵測到的每個代理程式安裝技能。 | `npx skills add opensearch-project/opensearch-agent-skills --all` |
| `--list` | 在安裝前列出可用的技能。 | `npx skills add opensearch-project/opensearch-agent-skills --list` |

## 使用技能

安裝技能後，請與您的 AI 助理開始對話並描述您的需求。助理會載入技能的 `SKILL.md` 指示並加以遵循。不需要 MCP 伺服器；技能完全在用戶端內執行。

### 範例：建置語意搜尋應用程式

下列逐步說明示範使用 `opensearch-launchpad` 技能的工作階段。

**使用者**：我想使用 OpenSearch 建置語意搜尋應用程式。

**助理**：我來協助您建置語意搜尋應用程式。首先，我會檢查您是否有正在執行的 OpenSearch 叢集。

```bash
uv run python scripts/opensearch_ops.py preflight-check
```

找不到叢集。正在使用 Docker 啟動叢集：

```bash
bash scripts/start_opensearch.sh
```

OpenSearch 正在 `http://localhost:9200` 上執行。您想要搜尋哪些資料？您可以提供 CSV、JSON 或 PDF 檔案，或由我載入範例資料集。

---

**使用者**：使用電子商務範例資料集。

**助理**：正在載入範例資料集：

```bash
uv run python scripts/opensearch_ops.py load-sample --dataset ecommerce
```

已將 4,675 份文件載入 `ecommerce` 索引。現在，您想使用哪一種搜尋策略？

1. BM25 — 關鍵字搜尋，速度快，不需要機器學習
2. 密集向量 — 使用文字嵌入的語意搜尋
3. 神經稀疏 — 使用學習式稀疏表示法的語意搜尋
4. 混合 — 結合關鍵字與語意評分
5. 代理式 — 由 LLM 驅動的多步驟檢索（需要 OpenSearch 3.2 以上版本）

---

**使用者**：混合搜尋。

**助理**：這很適合電子商務---混合搜尋能在精確的關鍵字比對（產品名稱、SKU）與語意理解（意圖、同義詞）之間取得平衡。計畫如下：

- 嵌入模型：`amazon/titan-embed-text-v1`（使用 ML Commons）
- 索引：`ecommerce-hybrid`，同時包含 `text` 與 `embedding` 欄位
- 搜尋管線：結合 BM25 與 k-NN 分數的正規化處理器

要繼續進行嗎？

---

**使用者**：是的。

**助理**：正在設定混合搜尋管線：

```bash
uv run python scripts/opensearch_ops.py setup-index \
  --strategy hybrid \
  --index ecommerce-hybrid \
  --source-index ecommerce
```

完成。正在啟動 Search Builder UI：

```bash
uv run python scripts/opensearch_ops.py launch-ui --index ecommerce-hybrid
```

您的搜尋應用程式已在 `http://127.0.0.1:8765` 上線。試試看 *「100 美元以下的舒適跑鞋」* 這類查詢，即可看到混合評分的實際效果。

---

### 其他技能範例

下列範例示範其他可用的技能：

- 記錄分析：*「找出過去 24 小時內我的記錄檔中前 5 名的錯誤模式。」* `log-analytics` 技能會產生 PPL 查詢、對您的記錄檔索引執行這些查詢，並摘要說明這些模式。
- 追蹤分析：*「顯示結帳服務中最慢的 span。」* `trace-analytics` 技能會在追蹤索引中查詢高延遲的 span，並呈現服務對應圖摘要。

### 搭配 MCP 伺服器使用技能

技能的設計可與 MCP 伺服器搭配運作。在已設定 MCP 伺服器的情況下使用技能時，助理可以遵循技能的結構化工作流程，並即時呼叫 API 來檢查索引狀態、執行測試查詢或驗證對應，而無須離開對話。

`opensearch-launchpad` 技能的 `SKILL.md` 包含一個選用的 MCP 伺服器組態區塊。您可以將此區塊新增至用戶端組態，讓助理在工作階段期間能直接存取 API：

```json
{
  "mcpServers": {
    "opensearch": {
      "command": "uvx",
      "args": ["opensearch-mcp-server-py"],
      "env": {
        "OPENSEARCH_URL": "http://localhost:9200",
        "OPENSEARCH_USERNAME": "admin",
        "OPENSEARCH_PASSWORD": "admin",
        "OPENSEARCH_SSL_VERIFY": "false"
      }
    }
  }
}
```
{% include copy.html %}

## 相關文件

- [`opensearch-agent-skills`](https://github.com/opensearch-project/opensearch-agent-skills) -- GitHub 上的代理程式技能儲存庫。
- [Agent Skills 規格](https://agentskills.io/specification) -- 規格文件。
- [OpenSearch MCP Server]({{site.url}}{{site.baseurl}}/ai-agent-integrations/mcp-server/) -- 從 AI 用戶端直接存取 API。
- [使用 MCP 工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/mcp/) -- 從 OpenSearch 代理程式整合外部 MCP 伺服器。
