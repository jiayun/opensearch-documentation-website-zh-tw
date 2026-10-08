---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "節點熱門執行緒"
parent: Nodes APIs
nav_order: 30
---

# Nodes Hot Threads API
**1.0 版推出**
{: .label .label-purple }

Nodes Hot Threads 端點提供所選叢集節點上忙碌 JVM 執行緒的相關資訊，讓您以獨特的角度檢視每個節點上的活動。


## 端點

```json
GET /_nodes/hot_threads
GET /_nodes/{node_id}/hot_threads
```

## 路徑參數

您可以在請求中加入下列選用的路徑參數。

參數 | 類型 | 說明
:--- | :--- | :---
`node_id` | String | 以逗號分隔的節點 ID 清單，用於篩選結果。支援[節點篩選條件]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/index/#node-filters)。預設為 `_all`。

## 查詢參數

您可以在請求中加入下列查詢參數。所有查詢參數皆為選用。

參數 | 類型 | 說明
:--- | :---| :---
`snapshots` | Integer | 執行緒堆疊追蹤的取樣次數。預設為 `10`。
`interval` | Time | 連續兩次取樣之間的間隔。預設為 `500ms`。
`threads` | Integer | 要傳回資訊的最忙碌執行緒數量。預設為 `3`。
`ignore_idle_threads` | Boolean   | 不顯示處於已知閒置狀態的執行緒，例如正在等待 socket select 或正從空的工作佇列中拉取工作的執行緒。預設為 `true`。
type | String | 支援的執行緒類型為 `cpu`、`wait` 或 `block`。預設為 `cpu`。
`timeout` | Time | 設定節點回應的時間限制。預設值為 `30s`。

## 範例請求

<!-- spec_insert_start
component: example_code
rest: GET /_nodes/hot_threads
-->
{% capture step1_rest %}
GET /_nodes/hot_threads
{% endcapture %}

{% capture step1_python %}


response = client.nodes.info(
  node_id_or_metric = "hot_threads"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

```bash
::: {opensearch}{F-ByTQzVQ3GQeYzQJArJGQ}{GxbcLdCATPWggOuQHJAoCw}{127.0.0.1}{127.0.0.1:9300}{dimr}{shard_indexing_pressure_enabled=true}
   Hot threads at 2022-09-29T19:46:44.533Z, interval=500ms, busiestThreads=3, ignoreIdleThreads=true:
   
    0.1% (455.5micros out of 500ms) cpu usage by thread 'ScheduledMetricCollectorsExecutor'
     10/10 snapshots sharing following 2 elements
       java.base@17.0.4/java.lang.Thread.sleep(Native Method)
       org.opensearch.performanceanalyzer.collectors.ScheduledMetricCollectorsExecutor.run(ScheduledMetricCollectorsExecutor.java:100)
```

## 範例回應

與大多數 OpenSearch API 回應不同，此回應為文字格式。

回應中包含的每個叢集節點各有一個區段。

每個區段都以單獨一行開頭，該行包含下列片段：

行片段 | 說明
:--- |:-------
<code>:::&nbsp;</code>  | 行首（一個易於辨識的視覺符號）。
`{global-eu-35}` | 節點名稱。
`{uFPbKLDOTlOmdnwUlKW8sw}` | NodeId。
`{OAM8OT5CQAyasWuIDeVyUA}` | EphemeralId。
`{global-eu-35.local}` | 主機名稱。
`{[gdv2:a284:2acv:5fa6:0:3a2:7260:74cf]:9300}` | 主機位址。
`{dimr}` | 節點角色（d=資料、i=匯入、m=叢集管理員、r=遠端叢集用戶端）。
`{zone=west-a2, shard_indexing_pressure_enabled=true}` | 節點屬性。

接著會提供所選類型執行緒的相關資訊。

```bash
::: {global-eu-35}{uFPbKLDOTlOmdnwUlKW8sw}{OAM8OT5CQAyasWuIDeVyUA}{global-eu-35.local}{[gdv2:a284:2acv:5fa6:0:3a2:7260:74cf]:9300}{dimr}{zone=west-a2, shard_indexing_pressure_enabled=true}
   Hot threads at 2022-04-01T15:15:27.658Z, interval=500ms, busiestThreads=3, ignoreIdleThreads=true:
   
    0.1% (645micros out of 500ms) cpu usage by thread 'opensearch[global-eu-35][transport_worker][T#7]'
     4/10 snapshots sharing following 3 elements
       io.netty.util.concurrent.SingleThreadEventExecutor$4.run(SingleThreadEventExecutor.java:986)
       io.netty.util.internal.ThreadExecutorMap$2.run(ThreadExecutorMap.java:74)
       java.base@11.0.14.1/java.lang.Thread.run(Thread.java:829)
::: {global-eu-62}{4knOxAdERlOB19zLQIT1bQ}{HJuZs2HiQ_-8Elj0Fvi_1g}{global-eu-62.local}{[gdv2:a284:2acv:5fa6:0:3a2:bba6:fe3f]:9300}{dimr}{zone=west-a2, shard_indexing_pressure_enabled=true}
   Hot threads at 2022-04-01T15:15:27.659Z, interval=500ms, busiestThreads=3, ignoreIdleThreads=true:
      
   18.7% (93.4ms out of 500ms) cpu usage by thread 'opensearch[global-eu-62][transport_worker][T#3]'
     6/10 snapshots sharing following 3 elements
       io.netty.util.concurrent.SingleThreadEventExecutor$4.run(SingleThreadEventExecutor.java:986)
       io.netty.util.internal.ThreadExecutorMap$2.run(ThreadExecutorMap.java:74)
       java.base@11.0.14.1/java.lang.Thread.run(Thread.java:829)
::: {global-eu-44}{8WW3hrkcTwGvgah_L8D_jw}{Sok7spHISFyol0jFV6i0kw}{global-eu-44.local}{[gdv2:a284:2acv:5fa6:0:3a2:9120:e79e]:9300}{dimr}{zone=west-a2, shard_indexing_pressure_enabled=true}
   Hot threads at 2022-04-01T15:15:27.659Z, interval=500ms, busiestThreads=3, ignoreIdleThreads=true:
   
   42.6% (212.7ms out of 500ms) cpu usage by thread 'opensearch[global-eu-44][write][T#5]'
     2/10 snapshots sharing following 43 elements
       java.base@11.0.14.1/sun.nio.ch.IOUtil.write1(Native Method)
       java.base@11.0.14.1/sun.nio.ch.EPollSelectorImpl.wakeup(EPollSelectorImpl.java:254)
       io.netty.channel.nio.NioEventLoop.wakeup(NioEventLoop.java:787)
       io.netty.util.concurrent.SingleThreadEventExecutor.execute(SingleThreadEventExecutor.java:846)
       io.netty.util.concurrent.SingleThreadEventExecutor.execute(SingleThreadEventExecutor.java:815)
       io.netty.channel.AbstractChannelHandlerContext.safeExecute(AbstractChannelHandlerContext.java:989)
       io.netty.channel.AbstractChannelHandlerContext.write(AbstractChannelHandlerContext.java:796)
       io.netty.channel.AbstractChannelHandlerContext.writeAndFlush(AbstractChannelHandlerContext.java:758)
       io.netty.channel.DefaultChannelPipeline.writeAndFlush(DefaultChannelPipeline.java:1020)
       io.netty.channel.AbstractChannel.writeAndFlush(AbstractChannel.java:311)
       org.opensearch.transport.netty4.Netty4TcpChannel.sendMessage(Netty4TcpChannel.java:159)
       app//org.opensearch.transport.OutboundHan...
```

## 必要權限

如果您使用 Security 外掛程式，請確認您已設定下列權限：`cluster:monitor/nodes/hot_threads`。
