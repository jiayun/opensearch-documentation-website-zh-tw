---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "動作"
nav_order: 50
grand_parent: Alerting
parent: Monitors
---

# 警示動作

當觸發條件符合時，動作會傳送通知。請參閱[通知]({{site.url}}{{site.baseurl}}/notifications-plugin/index/)以了解如何建立通知。如果您不想接收通知，請勿在觸發條件中新增動作。

## 新增動作

若要新增動作：

1. 在 **Triggers** 面板中，選取 **Add action**。
1. 在 **Notification** 區段中輸入動作詳細資訊，包括動作名稱、通知通道與通知訊息本文。

    您可以使用 [Mustache 範本](https://mustache.github.io/mustache.5.html)在訊息中加入變數。您可以使用 `ctx.action.name`、目前動作的名稱，以及所有[動作變數](#actions-variables)。

    如果您的通知通道是預期特定資料格式的自訂 webhook，請直接在訊息本文中包含 JSON（或 XML）：

    ```json
    {% raw %}{ "text": "Monitor {{ctx.monitor.name}} just entered alert status. Please investigate the issue. - Trigger: {{ctx.trigger.name}} - Severity: {{ctx.trigger.severity}} - Period start: {{ctx.periodStart}} - Period end: {{ctx.periodEnd}}" }{% endraw %}
    ```

    在上述範例中，訊息內容必須符合[自訂 webhook]({{site.url}}{{site.baseurl}}/notifications-plugin/index/) 中的 `Content-Type` 標頭。

1. 如果您使用的是桶層級監視器，請選擇監視器應在每次執行時還是針對每個警示執行動作。
1. （選用）使用動作節流來限制您在特定時間範圍內接收的通知數量。

    例如，如果監視器每分鐘檢查一次觸發條件，您可能每分鐘都會收到一次通知。如果您將動作節流設定為 60 分鐘，即使該小時內觸發條件符合數十次，您每小時也只會收到不超過一次的通知。

1. 選擇 **Create**。

動作傳送訊息後，該訊息的內容即離開 Alerting 外掛程式的管轄範圍。保護訊息的存取權（例如 Slack 頻道的存取權）是您的責任。

#### 訊息範例

```mustache
{% raw %}Monitor {{ctx.monitor.name}} just entered an alert state. Please investigate the issue.
- Trigger: {{ctx.trigger.name}}
- Severity: {{ctx.trigger.severity}}
- Period start: {{ctx.periodStart}}
- Period end: {{ctx.periodEnd}}{% endraw %}
```

若要在訊息中使用 `ctx.results` 變數，請使用 `{% raw %}{{ctx.results.0}}{% endraw %}` 而非 `{% raw %}{{ctx.results[0]}}{% endraw %}`。此差異是因為 Mustache 處理括號標記法的方式所致。
{: .note }

#### 動作變數

變數 | 資料類型 | 說明
:--- | :--- | :---
`ctx.trigger.actions.id` | 字串 | 動作 ID。
`ctx.trigger.actions.name` | 字串 | 動作名稱。
`ctx.trigger.actions.message_template.source` | 字串 | 警示中要傳送的訊息。
`ctx.trigger.actions.message_template.lang` | 字串 | 用於定義訊息的指令碼語言。必須是 Mustache。
`ctx.trigger.actions.throttle_enabled` | 布林值 | 此觸發條件是否已啟用節流。如需節流的更多資訊，請參閱[新增動作](#adding-actions)。
`ctx.trigger.actions.subject_template.source` | 字串 | 警示中訊息的主旨。
`ctx.trigger.actions.subject_template.lang` | 字串 | 用於定義主旨的指令碼語言。必須是 Mustache。
