---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "網路設定"
parent: Configuring OpenSearch
nav_order: 20
---

# 網路設定

OpenSearch 使用 HTTP 設定來設定透過 REST API 與外部用戶端之間的通訊，並使用傳輸設定來處理 OpenSearch 內部節點對節點的通訊。

若要了解如何套用這些設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

OpenSearch 支援下列一般網路設定：

- `network.host`（靜態，清單）：將 OpenSearch 節點繫結至某個位址。使用 `0.0.0.0` 可包含所有可用的網路介面，或指定已指派給特定介面的 IP 位址。若 `network.bind_host` 與 `network.publish_host` 的值相同，`network.host` 設定即為兩者的組合。除了 `network.host` 之外，您也可以視需要分別設定 `network.bind_host` 與 `network.publish_host`。請參閱[進階網路設定](#advanced-network-settings)。

- `http.port`（靜態，單一值或範圍）：將 OpenSearch 節點繫結至自訂連接埠或連接埠範圍，以進行 HTTP 通訊。您可以指定一個位址或位址範圍。預設為 `9200-9300`。

- `transport.port`（靜態，單一值或範圍）：將 OpenSearch 節點繫結至自訂連接埠，以進行節點之間的通訊。您可以指定一個位址或位址範圍。預設為 `9300-9400`。

## 進階網路設定

OpenSearch 支援下列進階網路設定：

- `network.bind_host`（靜態，清單）：將 OpenSearch 節點繫結至一或多個位址，以接收傳入連線。預設為 `network.host` 中的值。

- `network.publish_host`（靜態，清單）：指定 OpenSearch 節點向叢集中其他節點發布的一或多個位址，讓其他節點可以連線至該節點。

## 一般 TCP 設定

OpenSearch 支援下列適用於所有網路連線（包括 HTTP 層與傳輸層）的 TCP 設定：

- `network.tcp.keep_alive`（靜態，布林值）：為 OpenSearch 使用的所有 TCP 連線（包括 HTTP 層與傳輸層）啟用或停用 TCP keep-alive。啟用後，作業系統會定期傳送 keep-alive 封包以偵測失效的連線。預設為 `true`。

- `network.tcp.no_delay`（靜態，布林值）：為所有 TCP 連線啟用或停用 `TCP_NODELAY` 選項。啟用後會停用 Nagle 演算法，可降低小型訊息的延遲，但代價是增加網路流量。此設定同時適用於 HTTP 連線與傳輸連線。預設為 `true`。

- `network.tcp.receive_buffer_size`（靜態，位元組單位）：設定 OpenSearch 使用的所有 TCP 連線的 TCP 接收緩衝區大小。此設定會影響 HTTP 連線與傳輸連線。較大的緩衝區可提升高頻寬連線的輸送量。預設不會明確設定此值，而是使用作業系統的預設值。

- `network.tcp.reuse_address`（靜態，布林值）：控制所有 TCP 連線是否可重複使用 TCP 位址。此設定會影響 HTTP 連線與傳輸連線的通訊端繫結行為。在非 Windows 機器上預設為 `true`，在 Windows 上預設為 `false`。

- `network.tcp.send_buffer_size`（靜態，位元組單位）：設定 OpenSearch 使用的所有 TCP 連線的 TCP 傳送緩衝區大小。此設定會影響 HTTP 連線與傳輸連線。較大的緩衝區可提升高頻寬連線的輸送量。預設不會明確設定此值，而是使用作業系統的預設值。

- `network.server`（靜態，布林值）：啟用網路伺服器功能。預設為 `true`。

- `network.tcp.keep_count`（靜態，整數）：中斷連線前的 TCP keep-alive 探測次數。預設為 `-1`（系統預設值）。最小值為 `-1`。

- `network.tcp.keep_idle`（靜態，整數）：開始進行 TCP keep-alive 探測前的時間長度（以秒為單位）。預設為 `-1`（系統預設值）。最小值為 `-1`。最大值為 `300`。

- `network.tcp.keep_interval`（靜態，整數）：TCP keep-alive 探測之間的時間間隔（以秒為單位）。預設為 `-1`（系統預設值）。最小值為 `-1`。最大值為 `300`。

- `network.tcp.connect_timeout`（靜態，時間單位）：設定所有網路層建立 TCP 連線的逾時時間。此設定同時適用於 HTTP 連線與傳輸連線，並控制在逾時之前等待連線建立的時間長度。預設為 `30s`。

## 進階 HTTP 設定

OpenSearch 支援下列用於 HTTP 通訊的進階網路設定：

- `http.host`（靜態，清單）：設定 OpenSearch 節點用於 HTTP 通訊的位址。若 `http.bind_host` 與 `http.publish_host` 的值相同，`http.host` 設定即為兩者的組合。除了 `http.host` 之外，您也可以視需要分別設定 `http.bind_host` 與 `http.publish_host`。

- `http.bind_host`（靜態，清單）：指定 OpenSearch 節點繫結的一或多個位址，以接聽傳入的 HTTP 連線。

- `http.publish_host`（靜態，清單）：指定 OpenSearch 節點為進行 HTTP 通訊而向其他節點發布的一或多個位址。

- `http.compression`（靜態，布林值）：在適用時啟用 `Accept-Encoding` 壓縮支援。啟用 `HTTPS` 時，預設為 `false`；否則預設為 `true`。停用 HTTPS 的壓縮有助於降低潛在的安全性風險，例如 `BREACH` 攻擊。若要為 HTTPS 流量啟用壓縮，請將 `http.compression` 明確設定為 `true`。

- `http.max_header_size`：（靜態，字串）請求中允許的所有 HTTP 標頭的最大總大小。預設為 `16KB`。

- `http.compression_level`（靜態，整數）：定義啟用壓縮時 HTTP 回應所使用的壓縮層級。有效值的範圍為 1（最低壓縮）至 9（最高壓縮）。較高的值可提供較佳的壓縮效果，但會使用較多 CPU 資源。預設為 `3`。

- `http.max_chunk_size`（靜態，位元組單位）：設定處理請求與回應時 HTTP 區塊的大小上限。此設定控制 HTTP 訊息如何分割成較小的片段進行傳輸。較大的區塊大小可提升大型請求的輸送量，但可能增加記憶體使用量。預設為 `8kb`。

- `http.max_content_length`（靜態，位元組單位）：設定 HTTP 請求允許的最大內容長度。超過此限制的請求將遭到拒絕。此設定有助於防止極大型請求所造成的記憶體問題。預設為 `100mb`。

- `http.max_initial_line_length`（靜態，位元組單位）：設定初始請求行中 HTTP URL 允許的最大長度。超過此限制的 URL 將遭到拒絕。預設為 `4kB`。

- `http.max_warning_header_count`（靜態，整數）：設定傳送給用戶端的 HTTP 回應中可包含的警告標頭數量上限。警告標頭會提供有關請求處理的額外資訊。預設為無上限（不限制）。

- `http.max_warning_header_size`（靜態，位元組單位）：設定傳送給用戶端的 HTTP 回應中所有警告標頭合計的總大小上限。這有助於防止回應標頭變得過大。預設為無上限（不限制）。

- `http.pipelining.max_events`（靜態，整數）：設定在關閉 HTTP 連線之前，可在記憶體中排入佇列的事件數量上限。此設定有助於管理管線化 HTTP 請求的記憶體使用量。預設為 `10000`。

- `http.publish_port`（靜態，整數）：指定 HTTP 用戶端與此節點通訊時應使用的連接埠。當叢集節點位於 Proxy 或防火牆後方，且實際的 `http.port` 無法從網路外部直接定址時，此設定相當實用。預設為透過 `http.port` 指派的實際連接埠。

- `http.tcp.no_delay`（靜態，布林值）：控制 HTTP 連線的 `TCP_NODELAY` 選項。啟用後會停用 Nagle 演算法，可降低小型訊息的延遲，但代價是增加網路流量。預設為 `true`。

## HTTP CORS 設定

OpenSearch 支援下列適用於 HTTP 的跨來源資源共用 (CORS) 設定：

- `http.cors.enabled`（靜態，布林值）：啟用或停用 HTTP 請求的 CORS。啟用時，如果請求來源受到允許，OpenSearch 會處理 CORS 預檢請求，並以適當的 `Access-Control-Allow-Origin` 標頭回應。停用時，OpenSearch 會忽略 `Origin` 請求標頭，實際上即停用 CORS。預設為 `false`。

- `http.cors.allow-origin`（靜態，清單）：指定 CORS 請求允許的來源。您可以使用萬用字元 (`*`) 允許所有來源，但這會被視為安全性風險。您也可以用正斜線包住值來使用規則運算式（例如 `/https?:\/\/localhost(:[0-9]+)?/`）。預設為不允許任何來源。

- `http.cors.allow-methods`（靜態，清單）：指定 CORS 請求允許的 HTTP 方法。預設為 `OPTIONS, HEAD, GET, POST, PUT, DELETE`。

- `http.cors.allow-headers`（靜態，清單）：指定 CORS 請求中允許的 HTTP 標頭。預設為 `X-Requested-With, Content-Type, Content-Length`。

- `http.cors.allow-credentials`（靜態，布林值）：控制 CORS 回應中是否應包含 `Access-Control-Allow-Credentials` 標頭。只有在此設定為 `true` 時才會傳回此標頭。預設為 `false`。

- `http.cors.max-age`（靜態，時間單位）：定義瀏覽器應將 CORS 預檢 `OPTIONS` 請求的結果快取多久。瀏覽器會在發出實際的跨來源請求之前，先傳送預檢請求以判斷 CORS 設定。預設為 `1728000` 秒（20 天）。

## HTTP 錯誤處理設定

OpenSearch 支援下列 HTTP 錯誤處理設定：

- `http.detailed_errors.enabled`（靜態，布林值）：控制 HTTP 回應輸出中是否包含詳細的錯誤訊息和堆疊追蹤。設為 `false` 時，只會傳回簡單的錯誤訊息，除非指定了 `error_trace` 請求參數（在停用詳細錯誤時，這會傳回錯誤）。預設為 `true`。

## HTTP 偵錯設定

OpenSearch 支援下列用於追蹤 HTTP 通訊的 HTTP 偵錯設定：

- `http.tracer.include`（動態，清單）：指定以逗號分隔的 HTTP 請求路徑或萬用字元模式清單，以納入 HTTP 追蹤。設定後，只有符合這些模式的 HTTP 請求才會在記錄檔中被追蹤。此設定適用於對特定 HTTP 端點或 API 呼叫進行偵錯。預設為 `[]`（空白清單，啟用 HTTP 追蹤時會追蹤所有請求）。

- `http.tracer.exclude`（動態，清單）：指定以逗號分隔的 HTTP 請求路徑或萬用字元模式清單，以從 HTTP 追蹤中排除。即使已啟用 HTTP 追蹤，符合這些模式的 HTTP 請求也不會在記錄檔中被追蹤。此設定適用於減少來自頻繁或不重要端點的雜訊。預設為 `[]`（空白清單，啟用 HTTP 追蹤時不排除任何請求）。

- `http.netty.receive_predictor_size`（靜態，位元組大小）：Netty HTTP 傳輸的初始接收緩衝區大小預測值。預設為 `64kb`。

- `http.netty.worker_count`（靜態，整數）：Netty HTTP 傳輸的工作執行緒數量。預設為 `0`（自動偵測）。

- `http.read_timeout`（靜態，時間單位）：HTTP 連線的讀取逾時。預設值 0 表示沒有讀取逾時。預設為 `0`。最小值為 `0`。

- `http.reset_cookies`（靜態，布林值）：是否要重設 HTTP 回應中的 Cookie。由於通常不需要 Cookie，因此預設為停用。預設為 `false`。

- `http.tcp.keep_alive`（靜態，布林值）：為 HTTP 連線啟用 TCP keep-alive。預設為 `true`。

- `http.tcp.keep_count`（靜態，整數）：中斷連線前的 TCP keep-alive 探測次數。預設為系統預設值。最小值為 `-1`。

- `http.tcp.keep_idle`（靜態，整數）：開始 TCP keep-alive 探測前的時間長度（以秒為單位）。預設為系統預設值。最小值為 `-1`。最大值為 `300`。

- `http.tcp.keep_interval`（靜態，整數）：TCP keep-alive 探測之間的時間間隔（以秒為單位）。預設為系統預設值。最小值為 `-1`。最大值為 `300`。

- `http.tcp.receive_buffer_size`（靜態，位元組大小）：HTTP 連線的 TCP 接收緩衝區大小。預設為系統預設值。

- `http.tcp.reuse_address`（靜態，布林值）：為 HTTP 連線啟用 TCP 位址重複使用。預設為系統預設值。

- `http.tcp.send_buffer_size`（靜態，位元組大小）：HTTP 連線的 TCP 傳送緩衝區大小。預設為系統預設值。

## 實驗性 HTTP 設定

OpenSearch 支援下列實驗性 HTTP 設定：

- `http.protocol.http3.enabled`（靜態，布林值）：如果作業系統和架構支援，則啟用 HTTP/3 通訊協定。預設為 `false`。

    HTTP/3 傳輸目前為實驗性功能，使用時應謹慎。
    {: .warning}

    無法事先判斷目標伺服器是否支援 HTTP/3。此外，現有的 HTTP/1.1 或 HTTP/2 連線無法升級為 HTTP/3，因為 HTTP/1.1 和 HTTP/2 建立在 TCP 串流之上，而 HTTP/3 則使用透過 UDP 資料包傳輸的 QUIC。啟用時，HTTP/3 傳輸預設會與 HTTP/1.1 和 HTTP/2 傳輸使用相同的連接埠。
    {: .note}

    與 HTTP/1.1 和 HTTP/2 傳輸不同，此實作依賴原生程式庫，並使用直接 NIO 緩衝區。估算原生記憶體用量時，請將此納入考量。

    HTTP/3 預設即為安全，且只有在為 HTTP 傳輸啟用 SSL/TLS 時才可使用。OpenSearch 會使用 `Alt-Svc` 標頭公告 HTTP/3 的可用性，例如：

    ```yaml
    < HTTP/2 200
    < alt-svc: h3=":9200"; ma=3600
    < x-opensearch-version: OpenSearch/3.5.0 (opensearch)
    < content-type: application/json; charset=UTF-8
    < content-length: 572
    ```

    支援下列平台和架構：
    - Linux/Aarch64
    - Linux/x86_64
    - OSX/Aarch64
    - OSX/x86_64
    - Windows/x86_64

## 進階傳輸設定

OpenSearch 支援下列用於傳輸通訊的進階網路設定：

- `transport.host`（靜態，清單）：設定 OpenSearch 節點用於傳輸通訊的位址。當 `transport.bind_host` 和 `transport.publish_host` 為相同值時，`transport.host` 設定即為兩者的組合。除了 `transport.host` 之外，您也可以視需要分別設定 `transport.bind_host` 和 `transport.publish_host`。 

- `transport.bind_host`（靜態，清單）：指定 OpenSearch 節點繫結以接聽傳入傳輸連線的一或多個位址。 

- `transport.publish_host`（靜態，清單）：指定 OpenSearch 節點為進行傳輸通訊而向其他節點發布的一或多個位址。

- `transport.netty.boss_count`（靜態，整數）：Netty 傳輸的 boss 執行緒數量。預設為 `1`。最小值為 `1`。

- `transport.netty.receive_predictor_max`（靜態，位元組大小）：Netty 傳輸的最大接收緩衝區大小預測值。預設為 `64kb`。

- `transport.netty.receive_predictor_min`（靜態，位元組大小）：Netty 傳輸的最小接收緩衝區大小預測值。預設為 `64kb`。

- `transport.netty.receive_predictor_size`（靜態，位元組大小）：Netty 傳輸的初始接收緩衝區大小預測值。預設為 `64kb`。

- `transport.ssl.dual_mode.enabled`（靜態，布林值）：為傳輸層啟用雙模式 SSL（同時支援 SSL 和非 SSL）。預設為 `false`。

## 傳輸連線設定

OpenSearch 支援下列傳輸連線設定，可控制節點之間為不同類型作業所建立的連線數量：

- `transport.connections_per_node.bulk`（靜態，整數）：設定每個節點專用於大量作業（例如大量編製索引和大量更新請求）的連線數量。這些連線負責處理節點之間的高輸送量資料傳輸作業。在大型叢集中，較高的值可改善大量作業的效能，但會耗用較多網路資源。預設值為 `3`。最小值為 `1`。

- `transport.connections_per_node.ping`（靜態，整數）：設定每個節點用於 ping 作業及節點之間基本連線檢查的連線數量。Ping 連線用於叢集健康狀態監控和節點探索。預設值為 `1`。最小值為 `1`。

- `transport.connections_per_node.recovery`（靜態，整數）：設定每個節點專用於分片復原作業（包括副本復原和分片重新平衡）的連線數量。復原連線負責在復原過程中於節點之間傳輸分片資料。較高的值可加快復原作業，但可能會增加網路負載。預設值為 `2`。最小值為 `1`。

- `transport.connections_per_node.reg`（靜態，整數）：設定每個節點用於一般叢集作業、搜尋請求和管理工作的一般連線數量。這些是大多數節點間通訊所使用的主要連線。由於一般作業最為常見，因此此設定的預設值最高。預設值為 `6`。最小值為 `1`。

- `transport.connections_per_node.state`（靜態，整數）：設定每個節點用於叢集狀態同步和中繼資料作業的連線數量。狀態連線負責分發叢集狀態更新、對應變更及其他中繼資料作業。預設值為 `1`。最小值為 `1`。

## 傳輸偵錯設定

OpenSearch 支援下列傳輸偵錯設定，用於追蹤傳輸通訊：

- `transport.tracer.include`（動態，清單）：指定以逗號分隔的傳輸動作或模式清單，以納入傳輸追蹤。設定後，只有符合這些模式的傳輸通訊才會在記錄檔中被追蹤。此設定適用於針對 OpenSearch 特定的內部作業進行偵錯。預設值為 `[]`（空白清單，啟用傳輸追蹤時會追蹤所有動作）。

- `transport.tracer.exclude`（動態，清單）：指定以逗號分隔的傳輸動作或模式清單，以從傳輸追蹤中排除。即使已啟用傳輸追蹤，符合這些模式的傳輸通訊也不會在記錄檔中被追蹤。此設定適用於減少頻繁或不重要作業所產生的雜訊。預設值為 `[]`（空白清單，啟用傳輸追蹤時不排除任何項目）。

## 傳輸設定檔設定

OpenSearch 支援下列傳輸設定檔設定，可讓您為不同類型的連線設定多個傳輸設定檔。

傳輸設定檔可讓您針對不同類型的連線，繫結至不同介面上的多個連接埠。`default` 設定檔可作為其他設定檔的備援，並控制此節點如何連線至叢集中的其他節點。每個傳輸設定檔可設定下列設定：

- `transport.profiles.<profile_name>.port`（動態，單一值或範圍）：設定此傳輸設定檔要繫結的連接埠或連接埠範圍。不同的設定檔可使用不同的連接埠，以區隔各類型的流量。

- `transport.profiles.<profile_name>.bind_host`（動態，清單）：指定此傳輸設定檔應繫結哪些網路介面以接收傳入連線。不同的設定檔可繫結至不同的網路介面。

- `transport.profiles.<profile_name>.publish_host`（動態，清單）：指定此傳輸設定檔對其他節點發布的位址，讓其他節點能夠與其連線。當繫結位址與外部可存取的位址不同時，此設定非常實用。

- `transport.profiles.<profile_name>.tcp.no_delay`（動態，布林值）：控制此傳輸設定檔上連線的 `TCP_NODELAY` 選項。啟用後，會停用 Nagle 演算法，以降低小型訊息的延遲。

- `transport.profiles.<profile_name>.tcp.keep_alive`（動態，布林值）：控制此傳輸設定檔上連線的 `SO_KEEPALIVE` 選項。啟用後，作業系統會定期傳送 keep-alive 封包，以偵測已中斷的連線。

- `transport.profiles.<profile_name>.tcp.keep_idle`（動態，時間單位）：設定連線必須閒置多久後，才開始傳送 TCP keep-alive 探測。僅適用於搭配 JDK 11 或更新版本的 Linux 和 Mac。預設值為 `-1`（使用系統預設值）。

- `transport.profiles.<profile_name>.tcp.keep_interval`（動態，時間單位）：設定此傳輸設定檔上連線的 TCP keep-alive 探測間隔。僅適用於搭配 JDK 11 或更新版本的 Linux 和 Mac。預設值為 `-1`（使用系統預設值）。

- `transport.profiles.<profile_name>.tcp.keep_count`（動態，整數）：設定在中斷連線之前，可容許未獲確認的 TCP keep-alive 探測數量。僅適用於搭配 JDK 11 或更新版本的 Linux 和 Mac。預設值為 `-1`（使用系統預設值）。

- `transport.profiles.<profile_name>.tcp.reuse_address`（動態，布林值）：控制此傳輸設定檔上通訊端的 `SO_REUSEADDR` 選項，允許在通訊端關閉後重複使用位址。

- `transport.profiles.<profile_name>.tcp.send_buffer_size`（動態，位元組單位）：設定此傳輸設定檔上連線的 TCP 傳送緩衝區大小。較大的緩衝區可改善高頻寬連線的輸送量。

- `transport.profiles.<profile_name>.tcp.receive_buffer_size`（動態，位元組單位）：設定此傳輸設定檔上連線的 TCP 接收緩衝區大小。較大的緩衝區可改善高頻寬連線的輸送量。

## 進階傳輸設定

OpenSearch 支援下列進階傳輸設定：

- `transport.compress`（靜態，布林值）：為所有節點間的傳輸通訊啟用 `DEFLATE` 壓縮。啟用後，節點之間傳輸的資料會經過壓縮以減少網路頻寬用量，這對於透過較慢網路連結連線的叢集可能有所助益。不過，壓縮和解壓縮作業會增加 CPU 負擔。預設值為 `false`。

- `transport.connect_timeout`（靜態，時間單位）：設定在節點之間建立新傳輸連線的逾時時間。如果連線嘗試未在此時間限制內完成，即視為失敗。此設定有助於防止節點在嘗試連線至無回應或無法連線的節點時無限期停滯。預設值為 `30s`。

- `transport.ping_schedule`（靜態，時間單位）：設定傳送應用程式層級 ping 訊息的間隔，以維持節點之間的傳輸連線。設為正值時，節點會定期傳送 ping 訊息，以偵測並防止閒置連線逾時。將此設定設為 `-1` 會停用應用程式層級的 ping。一般建議改用 TCP keep-alive 設定，因為這些設定可為所有連線類型提供更全面的連線監控。預設值為 `-1`（停用）。

- `transport.publish_port`（靜態，整數）：指定其他節點連線至此節點進行傳輸通訊時應使用的連接埠。當節點位於 Proxy、防火牆或 NAT 組態之後，且實際繫結的連接埠與外部可存取的連接埠不同時，此設定特別實用。如果未指定，其他節點將使用由 `transport.port` 設定所決定的連接埠。預設值為透過 `transport.port` 指派的實際連接埠。

## 傳輸 TCP 設定

OpenSearch 支援下列傳輸層 TCP 設定，用於控制節點間通訊的低階 TCP 行為：

- `transport.tcp.keep_alive`（靜態，布林值）：為節點之間的傳輸連線啟用 TCP keep-alive。啟用時，作業系統會定期傳送 keep-alive 封包，以偵測失效的連線並維持連線狀態。這有助於更快偵測網路故障和無回應的節點。預設為 `true`。

- `transport.tcp.keep_count`（靜態，整數）：設定在未收到回應的情況下可傳送的 TCP keep-alive 探測次數，超過此次數後，連線即被視為失效並關閉。此設定僅在啟用 TCP keep-alive 時生效。預設為 `-1`（使用系統預設值）。最小值為 `-1`。

- `transport.tcp.keep_idle`（靜態，整數）：設定傳輸連線必須閒置多久（以秒為單位）才會開始傳送 TCP keep-alive 探測。此設定控制 keep-alive 機制何時對閒置連線啟動。預設為 `-1`（使用系統預設值）。最小值為 `-1`。最大值為 `300`。

- `transport.tcp.keep_interval`（靜態，整數）：設定傳輸連線的 TCP keep-alive 探測之間的時間間隔（以秒為單位）。keep-alive 探測開始後，此設定決定探測的傳送頻率。預設為 `-1`（使用系統預設值）。最小值為 `-1`。最大值為 `300`。

- `transport.tcp.receive_buffer_size`（靜態，位元組單位）：設定傳輸連線的 TCP 接收緩衝區大小。這會控制作業系統為傳入的傳輸訊息緩衝多少資料。較大的緩衝區可提升高頻寬節點間通訊的輸送量，但會耗用更多記憶體。預設為 `-1`（使用系統預設值）。

- `transport.tcp.reuse_address`（靜態，布林值）：控制傳輸連線的 `SO_REUSEADDR` 通訊端選項。啟用時，傳輸層可在連線關閉後立即重複使用 TCP 位址，這在節點快速重新啟動或連線頻繁更替時很有幫助。預設值取決於作業系統（在非 Windows 系統上通常為 `true`，在 Windows 上為 `false`）。

- `transport.tcp.send_buffer_size`（靜態，位元組單位）：設定傳輸連線的 TCP 傳送緩衝區大小。這會控制作業系統為傳出的傳輸訊息緩衝多少資料。較大的緩衝區可提升高頻寬節點間通訊的輸送量，但會耗用更多記憶體。預設為 `-1`（使用系統預設值）。

- `transport.tcp.no_delay`（靜態，布林值）：控制節點之間傳輸連線的 `TCP_NODELAY` 選項。啟用時會停用 Nagle 演算法，可降低小型訊息的延遲，但代價是增加網路流量。此設定對於低延遲至關重要的叢集通訊尤其重要。預設為 `true`。

- `transport.tcp.compress`（靜態，布林值）：為節點之間的傳輸層通訊啟用 DEFLATE 壓縮。啟用時可減少網路頻寬用量，但代價是壓縮和解壓縮會帶來額外的 CPU 負擔。此設定已由較新的 `transport.compress` 設定取代。預設為 `false`。

- `transport.tcp.connect_timeout`（靜態，時間單位）：設定在節點之間的傳輸層建立 TCP 連線的逾時時間。如果連線嘗試未在此時間限制內完成，即視為失敗。此設定已由較新的 `transport.connect_timeout` 設定取代。預設為 `30s`。

- `transport.tcp_no_delay`（靜態，布林值）：**已淘汰。** 控制傳輸連線 `TCP_NODELAY` 選項的舊版設定。此設定已由 `transport.tcp.no_delay` 取代，保留此設定是為了回溯相容性。請改用 `transport.tcp.no_delay`。預設為 `true`。

## 傳輸功能設定

OpenSearch 支援下列傳輸功能設定，用於控制選用的傳輸層功能：

- `transport.features.*`（靜態，群組設定）：控制節點間通訊要啟用哪些傳輸功能。這是一個群組設定，可啟用或停用特定的傳輸層功能，例如壓縮、安全性增強功能或通訊協定擴充功能。個別功能名稱會以後綴形式附加，以設定特定的傳輸功能。這些設定必須在叢集中的所有節點上一致地設定，以確保相容性。

## 傳輸和 HTTP 類型設定

OpenSearch 支援控制叢集所使用之預設傳輸和 HTTP 實作類型的設定。

OpenSearch 支援下列靜態傳輸和 HTTP 類型設定：

- `transport.type.default`（靜態，字串）：設定節點間通訊的預設傳輸實作類型。此設定決定在未設定特定傳輸類型時，OpenSearch 使用哪種傳輸實作。預設實作為 `netty4`，它提供以 Netty 4 為基礎的高效率非同步網路功能。外掛程式可提供替代實作。預設為 `netty4`。

- `http.type.default`（靜態，字串）：設定用戶端通訊的預設 HTTP 實作類型。此設定決定在未設定特定 HTTP 類型時，OpenSearch 使用哪種 HTTP 實作。預設實作為 `netty4`，它提供以 Netty 4 為基礎的高效率非同步 HTTP 處理。外掛程式可提供 `reactor-netty4` 等替代實作。預設為 `netty4`。

## 選取傳輸

預設的 OpenSearch 傳輸由 `transport-netty4` 模組提供，並使用 [Netty 4](https://netty.io/) 引擎處理叢集中節點之間以 TCP 為基礎的內部通訊，以及與用戶端之間以 HTTP 為基礎的外部通訊。此通訊完全是非同步且非阻塞的。下表列出其他可互換使用的傳輸外掛程式。

外掛程式 | 說明
:---------- | :--------
`transport-reactor-netty4`    | 以 [Project Reactor](https://github.com/reactor/reactor-netty) 和 Netty 4 為基礎的 OpenSearch HTTP 傳輸（**實驗性**）<br> 安裝：`./bin/opensearch-plugin install transport-reactor-netty4` <br> 組態（使用 `opensearch.yml`）：<br> `http.type: reactor-netty4` <br> `http.type: reactor-netty4-secure`<br>支援的通訊協定：**HTTP/1.1**、**HTTP/2**、**HTTP/3**（實驗性，請參閱 [HTTP 實驗性設定](#experimental-http-settings)）

