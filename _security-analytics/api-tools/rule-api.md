---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "規則 API"
parent: Security Analytics APIs
nav_order: 40
---

# 規則 API

下列 API 可用於執行多項與規則相關的工作，從搜尋預先封裝的規則，到建立及更新自訂規則。

---
## 建立自訂規則

使用 Sigma 安全性規則格式建立自訂規則。如需有關如何以 Sigma 格式撰寫規則的資訊，請參閱 [Sigma 的 GitHub 儲存庫](https://github.com/SigmaHQ/sigma) 所提供的資訊。

```json
POST /_plugins/_security_analytics/rules?category=windows
```

### 範例請求

```yml
Header:
Content-Type: application/json

Body:

title: Moriya Rootkit
id: 25b9c01c-350d-4b95-bed1-836d04a4f324
description: Detects the use of Moriya rootkit as described in the securelist's Operation TunnelSnake report
status: experimental
author: Bhabesh Raj
date: 2021/05/06
modified: 2021/11/30
references:
    - https://securelist.com/operation-tunnelsnake-and-moriya-rootkit/101831
tags:
    - attack.persistence
    - attack.privilege_escalation
    - attack.t1543.003
logsource:
    product: windows
    service: system
detection:
    selection:
        Provider_Name: 'Service Control Manager'
        EventID: 7045
        ServiceName: ZzNetSvc
    condition: selection
level: critical
falsepositives:
    - Unknown
```

### 範例回應

**範例 1：**

```json
{
    "_id": "M1Rm1IMByX0LvTiGvde2",
    "_version": 1,
    "rule": {
        "category": "windows",
        "title": "Moriya Rootkit",
        "log_source": "",
        "description": "Detects the use of Moriya rootkit as described in the securelist's Operation TunnelSnake report",
        "tags": [
            {
                "value": "attack.persistence"
            },
            {
                "value": "attack.privilege_escalation"
            },
            {
                "value": "attack.t1543.003"
            }
        ],
        "references": [
            {
                "value": "https://securelist.com/operation-tunnelsnake-and-moriya-rootkit/101831"
            }
        ],
        "level": "critical",
        "false_positives": [
            {
                "value": "Unknown"
            }
        ],
        "author": "Bhabesh Raj",
        "status": "experimental",
        "last_update_time": "2021-05-06T00:00:00.000Z",
        "rule": "title: Moriya Rootkit\nid: 25b9c01c-350d-4b95-bed1-836d04a4f324\ndescription: Detects the use of Moriya rootkit as described in the securelist's Operation TunnelSnake report\nstatus: experimental\nauthor: Bhabesh Raj\ndate: 2021/05/06\nmodified: 2021/11/30\nreferences:\n    - https://securelist.com/operation-tunnelsnake-and-moriya-rootkit/101831\ntags:\n    - attack.persistence\n    - attack.privilege_escalation\n    - attack.t1543.003\nlogsource:\n    product: windows\n    service: system\ndetection:\n    selection:\n        Provider_Name: 'Service Control Manager'\n        EventID: 7045\n        ServiceName: ZzNetSvc\n    condition: selection\nlevel: critical\nfalsepositives:\n    - Unknown"
    }
}
```

**範例 2：**

```json
{
  "error": {
    "root_cause": [
      {
        "type": "security_analytics_exception",
        "reason": "{\"error\":\"Sigma rule must have a log source\",\"error\":\"Sigma rule must have a detection definitions\"}"
      }
    ],
    "type": "security_analytics_exception",
    "reason": "{\"error\":\"Sigma rule must have a log source\",\"error\":\"Sigma rule must have a detection definitions\"}",
    "caused_by": {
      "type": "exception",
      "reason": "{\"error\":\"Sigma rule must have a log source\",\"error\":\"Sigma rule must have a detection definitions\"}"
    }
  },
  "status": 400
}
```

---
## 更新自訂規則 (非強制)

更新自訂規則。如果偵測器正在使用該規則，除非將 `forced` 旗標設為 `true`，否則會拒絕更新。

### 範例請求

```json
PUT /_plugins/_security_analytics/rules/ZaFv1IMBdLpXWBiBa1XI?category=windows

Content-Type: application/json

Body:

title: Moriya Rooskit
id: 25b9c01c-350d-4b95-bed1-836d04a4f324
description: Detects the use of Moriya rootkit as described in the securelist's Operation TunnelSnake report
status: experimental
author: Bhabesh Raj
date: 2021/05/06
modified: 2021/11/30
references:
    - https://securelist.com/operation-tunnelsnake-and-moriya-rootkit/101831
tags:
    - attack.persistence
    - attack.privilege_escalation
    - attack.t1543.003
logsource:
    product: windows
    service: system
detection:
    selection:
        Provider_Name: 'Service Control Manager'
        EventID: 7045
        ServiceName: ZzNetSvc
    condition: selection
level: critical
falsepositives:
    - Unknown
```

### 範例回應

```json
{
    "error": {
        "root_cause": [
            {
                "type": "security_analytics_exception",
                "reason": "Rule with id ZaFv1IMBdLpXWBiBa1XI is actively used by detectors. Update can be forced by setting forced flag to true"
            }
        ],
        "type": "security_analytics_exception",
        "reason": "Rule with id ZaFv1IMBdLpXWBiBa1XI is actively used by detectors. Update can be forced by setting forced flag to true",
        "caused_by": {
            "type": "exception",
            "reason": "org.opensearch.OpenSearchStatusException: Rule with id ZaFv1IMBdLpXWBiBa1XI is actively used by detectors. Update can be forced by setting forced flag to true"
        }
    },
    "status": 500
}
```

---
## 更新自訂規則 (強制)

強制更新自訂規則，即使偵測器正在使用該規則也一樣。

### 範例請求

```json
PUT /_plugins/_security_analytics/rules/ZaFv1IMBdLpXWBiBa1XI?category=windows&forced=true

Content-Type: application/json

Body:

title: Moriya Rooskit
id: 25b9c01c-350d-4b95-bed1-836d04a4f324
description: Detects the use of Moriya rootkit as described in the securelist's Operation TunnelSnake report
status: experimental
author: Bhabesh Raj
date: 2021/05/06
modified: 2021/11/30
references:
    - https://securelist.com/operation-tunnelsnake-and-moriya-rootkit/101831
tags:
    - attack.persistence
    - attack.privilege_escalation
    - attack.t1543.003
logsource:
    product: windows
    service: system
detection:
    selection:
        Provider_Name: 'Service Control Manager'
        EventID: 7045
        ServiceName: ZzNetSvc
    condition: selection
level: critical
falsepositives:
    - Unknown
```

### 範例回應

```json
{
    "_id": "ZaFv1IMBdLpXWBiBa1XI",
    "_version": 1,
    "rule": {
        "category": "windows",
        "title": "Moriya Rooskit",
        "log_source": "",
        "description": "Detects the use of Moriya rootkit as described in the securelist's Operation TunnelSnake report",
        "tags": [
            {
                "value": "attack.persistence"
            },
            {
                "value": "attack.privilege_escalation"
            },
            {
                "value": "attack.t1543.003"
            }
        ],
        "references": [
            {
                "value": "https://securelist.com/operation-tunnelsnake-and-moriya-rootkit/101831"
            }
        ],
        "level": "critical",
        "false_positives": [
            {
                "value": "Unknown"
            }
        ],
        "author": "Bhabesh Raj",
        "status": "experimental",
        "last_update_time": "2021-05-06T00:00:00.000Z",
        "rule": "title: Moriya Rooskit\nid: 25b9c01c-350d-4b95-bed1-836d04a4f324\ndescription: Detects the use of Moriya rootkit as described in the securelist's Operation TunnelSnake report\nstatus: experimental\nauthor: Bhabesh Raj\ndate: 2021/05/06\nmodified: 2021/11/30\nreferences:\n    - https://securelist.com/operation-tunnelsnake-and-moriya-rootkit/101831\ntags:\n    - attack.persistence\n    - attack.privilege_escalation\n    - attack.t1543.003\nlogsource:\n    product: windows\n    service: system\ndetection:\n    selection:\n        Provider_Name: 'Service Control Manager'\n        EventID: 7045\n        ServiceName: ZzNetSvc\n    condition: selection\nlevel: critical\nfalsepositives:\n    - Unknown"
    }
}
```

---
## 搜尋預先封裝的規則

依類別或其他條件搜尋預先封裝的規則。

### 範例請求

```json
POST /_plugins/_security_analytics/rules/_search?pre_packaged=true

{
  "from": 0,
  "size": 20,  
  "query": {
    "nested": {
      "path": "rule",
      "query": {
        "bool": {
          "must": [
            { "match": { "rule.category": "windows" } }
          ]
        }
      }
    }
  }
}
```

### 範例回應

```json
{
    "took": 3,
    "timed_out": false,
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 1580,
            "relation": "eq"
        },
        "max_score": 0.25863406,
        "hits": [
            {
                "_index": ".opensearch-pre-packaged-rules-config",
                "_id": "6KFv1IMBdLpXWBiBelZg",
                "_version": 1,
                "_seq_no": 386,
                "_primary_term": 1,
                "_score": 0.25863406,
                "_source": {
                    "category": "windows",
                    "title": "Change Outlook Security Setting in Registry",
                    "log_source": "registry_set",
                    "description": "Change outlook email security settings",
                    "references": [
                        {
                            "value": "https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1137/T1137.md"
                        },
                        {
                            "value": "https://docs.microsoft.com/en-us/outlook/troubleshoot/security/information-about-email-security-settings"
                        }
                    ],
                    "tags": [
                        {
                            "value": "attack.persistence"
                        },
                        {
                            "value": "attack.t1137"
                        }
                    ],
                    "level": "medium",
                    "false_positives": [
                        {
                            "value": "Administrative scripts"
                        }
                    ],
                    "author": "frack113",
                    "status": "experimental",
                    "last_update_time": "2021-12-28T00:00:00.000Z",
                    "queries": [
                        {
                            "value": "((TargetObject: *\\\\SOFTWARE\\\\Microsoft\\\\Office\\\\*) AND (TargetObject: *\\\\Outlook\\\\Security\\\\*)) AND (EventType: \"SetValue\")"
                        }
                    ],
                    "rule": "title: Change Outlook Security Setting in Registry\nid: c3cefdf4-6703-4e1c-bad8-bf422fc5015a\ndescription: Change outlook email security settings\nauthor: frack113\ndate: 2021/12/28\nmodified: 2022/03/26\nstatus: experimental\nreferences:\n    - https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1137/T1137.md\n    - https://docs.microsoft.com/en-us/outlook/troubleshoot/security/information-about-email-security-settings\nlogsource:\n    category: registry_set\n    product: windows\ndetection:\n    selection:\n        TargetObject|contains|all:\n            - '\\SOFTWARE\\Microsoft\\Office\\'\n            - '\\Outlook\\Security\\'\n        EventType: SetValue\n    condition: selection\nfalsepositives:\n    - Administrative scripts\nlevel: medium\ntags:\n  - attack.persistence\n  - attack.t1137\n"
                }
            }
        ]
    }
}
```

---
## 搜尋自訂規則

依類別或其他條件搜尋自訂規則。

### 範例請求

```json
POST /_plugins/_security_analytics/rules/_search?pre_packaged=false

Body:

{
  "from": 0,
  "size": 20,  
  "query": {
    "nested": {
      "path": "rule",
      "query": {
        "bool": {
          "must": [
            { "match": { "rule.category": "windows" } }
          ]
        }
      }
    }
  }
}
```

### 範例回應

```json
{
    "took": 1,
    "timed_out": false,
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 1,
            "relation": "eq"
        },
        "max_score": 0.2876821,
        "hits": [
            {
                "_index": ".opensearch-custom-rules-config",
                "_id": "ZaFv1IMBdLpXWBiBa1XI",
                "_version": 2,
                "_seq_no": 1,
                "_primary_term": 1,
                "_score": 0.2876821,
                "_source": {
                    "category": "windows",
                    "title": "Moriya Rooskit",
                    "log_source": "",
                    "description": "Detects the use of Moriya rootkit as described in the securelist's Operation TunnelSnake report",
                    "references": [
                        {
                            "value": "https://securelist.com/operation-tunnelsnake-and-moriya-rootkit/101831"
                        }
                    ],
                    "tags": [
                        {
                            "value": "attack.persistence"
                        },
                        {
                            "value": "attack.privilege_escalation"
                        },
                        {
                            "value": "attack.t1543.003"
                        }
                    ],
                    "level": "critical",
                    "false_positives": [
                        {
                            "value": "Unknown"
                        }
                    ],
                    "author": "Bhabesh Raj",
                    "status": "experimental",
                    "last_update_time": "2021-05-06T00:00:00.000Z",
                    "queries": [
                        {
                            "value": "(Provider_Name: \"Service_ws_Control_ws_Manager\") AND (event_uid: 7045) AND (ServiceName: \"ZzNetSvc\")"
                        }
                    ],
                    "rule": "title: Moriya Rooskit\nid: 25b9c01c-350d-4b95-bed1-836d04a4f324\ndescription: Detects the use of Moriya rootkit as described in the securelist's Operation TunnelSnake report\nstatus: experimental\nauthor: Bhabesh Raj\ndate: 2021/05/06\nmodified: 2021/11/30\nreferences:\n    - https://securelist.com/operation-tunnelsnake-and-moriya-rootkit/101831\ntags:\n    - attack.persistence\n    - attack.privilege_escalation\n    - attack.t1543.003\nlogsource:\n    product: windows\n    service: system\ndetection:\n    selection:\n        Provider_Name: 'Service Control Manager'\n        EventID: 7045\n        ServiceName: ZzNetSvc\n    condition: selection\nlevel: critical\nfalsepositives:\n    - Unknown"
                }
            }
        ]
    }
}
```

---
## 刪除自訂規則（非強制）

刪除自訂規則。如果該規則正被偵測器使用中，除非將 `forced` 旗標設為 `true`，否則刪除作業會被拒絕。

### 範例請求

```json
DELETE /_plugins/_security_analytics/rules/ZaFv1IMBdLpXWBiBa1XI
```

### 範例回應

```json
{
    "error": {
        "root_cause": [
            {
                "type": "security_analytics_exception",
                "reason": "Rule with id ZaFv1IMBdLpXWBiBa1XI is actively used by detectors. Deletion can be forced by setting forced flag to true"
            }
        ],
        "type": "security_analytics_exception",
        "reason": "Rule with id ZaFv1IMBdLpXWBiBa1XI is actively used by detectors. Deletion can be forced by setting forced flag to true",
        "caused_by": {
            "type": "exception",
            "reason": "org.opensearch.OpenSearchStatusException: Rule with id ZaFv1IMBdLpXWBiBa1XI is actively used by detectors. Deletion can be forced by setting forced flag to true"
        }
    },
    "status": 500
}
```

---
## 刪除自訂規則 (強制)

強制刪除自訂規則，即使偵測器正在使用該規則也一樣。

### 範例請求

```json
DELETE /_plugins/_security_analytics/rules/ZaFv1IMBdLpXWBiBa1XI?forced=true
```

### 範例回應

```json
{
    "_id": "ZaFv1IMBdLpXWBiBa1XI",
    "_version": 1
}
```

