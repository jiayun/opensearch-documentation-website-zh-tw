---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "運算式語法"
parent: Pipelines
nav_order: 5
---

# 運算式語法  

運算式可讓您靈活地操作、篩選及路由資料。以下各節提供 OpenSearch Data Prepper 運算式語法的相關資訊。

## 重要術語

以下重要術語用於運算式的語境。

術語 | 定義
-----|-----------
**運算式** | 包含基本項或運算子的通用元件。運算式可以巢狀置於其他運算式中。運算式的直接子項可以包含 0–1 個運算子。
**運算式字串** | 在 Data Prepper 運算式中具有最高優先順序，且僅支援一個產生回傳值的運算式字串。運算式字串與運算式不同。
**字面值** | 沒有子項的基本值。字面值可以是下列其中一種：浮點數、整數、布林值、JSON 指標、字串或 null。請參閱[字面值](#literals)。
**運算子** | 識別運算式所用運算的硬式編碼詞元。
**基本項** | 可以是下列其中一種：集合初始化式、優先運算式或字面值。
**陳述式** | 運算式字串中優先順序最高的元件。

## 運算子

下表列出支援的運算子。運算子依優先順序排列（由上到下、由左到右）。

| 運算子               | 說明                                           | 結合方向 |
|------------------------|-------------------------------------------------------|---------------|
| `()`                   | 優先運算式                                   | 由左到右 |
| `not`<br> `+`<br>  `-` | 一元邏輯 NOT<br>一元正號<br>一元負號 | 由右到左 |
| `*`, `/`, `%`           | 乘法（`*`）、除法（`/`）及模數（`%`）運算子        | 由左到右 |
| `+`, `-`               | 加法及減法運算子                    | 由左到右 |
| `+`                    | 字串串接運算子                         | 由左到右 |
| `<`, `<=`, `>`, `>=`   | 關係運算子                                  | 由左到右 |
| `==`, `!=`             | 相等運算子                                    | 由左到右 |
| `and`, `or`            | 條件運算式                                | 由左到右 |

### 關係運算子

關係運算子會比較數值，或解析為數值的 JSON 指標。這些運算子用於測試兩個運算元之間的關係，判斷其中一個是否大於、小於或等於另一個。使用關係運算子的語法如下：

```
<Number | JSON Pointer> < <Number | JSON Pointer>
<Number | JSON Pointer> <= <Number | JSON Pointer>
<Number | JSON Pointer> > <Number | JSON Pointer>
<Number | JSON Pointer> >= <Number | JSON Pointer>
```
{% include copy.html %}

例如，若要檢查事件中 `status_code` 欄位的值是否在成功 HTTP 回應的範圍（200--299）內，您可以使用下列運算式：

```
/status_code >= 200 and /status_code < 300
```
{% include copy.html %}

### 相等運算子

相等運算子用於測試兩個值是否相等。這些運算子會比較任何類型的值，包括 JSON 指標、字面值及運算式。使用相等運算子的語法如下： 

```
<Any> == <Any>
<Any> != <Any>
```
{% include copy.html %}

以下是一些相等運算子的範例：

- `/is_cool == true`：檢查 JSON 指標參照的值是否等於布林值。
- `3.14 != /status_code`：檢查數值是否不等於 JSON 指標參照的值。
- `{1, 2} == /event/set_property`：檢查陣列是否等於 JSON 指標參照的值。 

### 條件運算式

條件運算式可讓您使用邏輯運算子結合多個運算式或值，以建立更複雜的求值條件。可用的條件運算子為 `and`、`or` 及 `not`。使用這些條件運算子的語法如下：

```
<Any> and <Any>
<Any> or <Any>
not <Any>
```

以下是一些條件運算式的範例： 

```
/status_code == 200 and /message == "Hello world"
/status_code == 200 or /status_code == 202
not /status_code in {200, 202}
/response == null
/response != null
```
{% include copy.html %}

### 算術運算式

算術運算式可執行加法、減法、乘法及除法等基本數學運算。這些運算式可與條件運算式結合，以建立更複雜的條件陳述式。可用的算術運算子為 +、-、* 及 /。使用算術運算子的語法如下：

```
<Any> + <Any>
<Any> - <Any>
<Any> * <Any>
<Any> / <Any>
```

以下是算術運算式的範例： 

```
/value + length(/message)
/bytes / 1024
/value1 - /value2
/TimeInSeconds * 1000
```
{% include copy.html %}

以下是在條件運算式中使用算術運算式的一些範例： 

```
/value + length(/message) > 200
/bytes / 1024 < 10
/value1 - /value2 != /value3 + /value4
```
{% include copy.html %}

### 字串串接運算式

字串串接運算式可讓您結合字串，以建立新字串。這些串接後的字串也可用於條件運算式中。使用字串串接的語法如下：

```
<String Variable or String Literal> + <String Variable or String Literal>
```

以下是字串串接運算式的範例：

```
/name + "suffix"
"prefix" + /name
"time of " + /timeInMs + " ms"
```
{% include copy.html %}

以下是可用於條件運算式中的字串串接運算式範例：

```
/service + ".com" == /url
"www." + /service != /url
```
{% include copy.html %}

### 保留符號

某些符號，例如 ^、%、xor、=、+=、-=、*=、/=、%=、++、-- 及 ${<text>}，保留供未來的功能或擴充使用。保留符號包括 `^`、`%`、`xor`、`=`、`+=`、`-=`、`*=`、`/=`、`%=`、`++`、`--` 及 `${<text>}`。

## 語法元件

語法元件是 Data Prepper 運算式的基本組成要素。它們可讓您定義集合、指定求值順序、參照事件中的值、使用字面值，以及遵循特定的空白字元規則。瞭解這些元件，對於在 Data Prepper 管線中有效建立及使用運算式至關重要。

### 優先運算式

優先運算式指定運算式的求值順序。它們以括號 `()` 括住。優先運算式必須包含運算式或值（不支援空括號）。以下是優先運算式的範例：

```
/is_cool == (/name == "Steven")
```
{% include copy.html %}

### JSON 指標

JSON 指標用於參照事件中的值。它們以正斜線 `/` 開頭，後面接英數字元或底線，並以其他正斜線 `/` 分隔。 

JSON 指標可透過以雙引號 `""` 括住整個指標，並使用反斜線 `\` 逸出字元，來使用擴充字元集。請注意，`~` 及 `/` 字元視為指標路徑的一部分，不需要逸出。以下是一些有效 JSON 指標的範例：以 `~0` 表示字面字元 `~`，或以 `~1` 表示字面字元 `/`。

#### 簡寫語法

JSON 指標的簡寫語法可使用下列規則運算式模式表示，其中 `\w` 代表任何單字字元（A--Z、a-z、0--9 或底線）：

```
/\w+(/\w+)*`
```
{% include copy.html %}
 

以下是此簡寫語法的範例：

```
/Hello/World/0
```
{% include copy.html %}

#### 逸出語法

JSON 指標的逸出語法可表示如下：

```
"/<Valid String Characters | Escaped Character>(/<Valid String Characters | Escaped Character>)*"
```
{% include copy.html %}

以下是逸出 JSON 指標的範例：

```
# Path
# { "Hello - 'world/" : [{ "\"JsonPointer\"": true }] }
"/Hello - 'world\//0/\"JsonPointer\""
```
{% include copy.html %}

### 字面值

字面值是沒有子項的基本值。Data Prepper 支援下列字面值類型： 

- **浮點數：** 支援從 3.40282347 x 10^38 到 1.40239846 x 10^-45 的值。
- **整數：** 支援從 -2,147,483,648 到 2,147,483,647 的值。
- **布林值：** 支援 `true` 或 `false`。
- **JSON 指標：** 如需詳細資訊，請參閱 [JSON 指標](#json-pointers)。
- **字串：** 支援有效的 Java 字串。
- **Null：** 支援使用 `null` 檢查 JSON 指標是否存在。

### 空白字元規則

關係運算子、規則運算式相等運算子、相等運算子及逗號的周圍可選擇性加入空白字元。集合初始化式、優先運算式、集合運算子及條件運算式的周圍必須加入空白字元。

| 運算子             | 說明              | 是否需要空白字元 | ✅ 有效範例                                               | ❌ 無效範例                    |
|----------------------|--------------------------|----------------------|----------------------------------------------------------------|---------------------------------------|
| `{}`                 | 集合初始化式          | 是                  | `/status in {200}`                                             | `/status in{200}`                     |
| `()`                 | 優先運算式      | 是                  | `/a==(/b==200)`<br>`/a in ({200})`                             | `/status in({200})`                   |
| `in`, `not in`       | 集合運算子            | 是                  | `/a in {200}`<br>`/a not in {400}`                             | `/a in{200, 202}`<br>`/a not in{400}` |
| `<`, `<=`, `>`, `>=` | 關係運算子     | 否                   | `/status < 300`<br>`/status>=300`                              |                                       |
| `+`                  | 字串串接運算子   | 否                   | `/status_code + /message + "suffix"`
| `+`, `-`             | 算術加法及減法運算子 | 否      | `/status_code + length(/message) - 2`
| `*`, `/`             | 乘法及除法運算子 | 否              | `/status_code * length(/message) / 3`
| `=~`, `!~`           | 規則運算式相等運算子 | 否                   | `/msg =~ "^\w*$"`<br>`/msg=~"^\w*$"`                           |                                       |
| `==`, `!=`           | 相等運算子       | 否                   | `/status == 200`<br>`/status_code==200`                        |                                       |
| `and`, `or`, `not`   | 條件運算子    | 是                  | `/a<300 and /b>200`                                            | `/b<300and/b>200`                     |
| `,`                  | 集合值分隔符號      | 否                   | `/a in {200, 202}`<br>`/a in {200,202}`<br>`/a in {200 , 202}` | `/a in {200,}`                        |
| `typeof`             | 型別檢查運算子      | 是                   | `/a typeof integer`<br>`/a typeof long`<br>`/a typeof string`<br> `/a typeof double`<br> `/a typeof boolean`<br>`/a typeof map`<br>`/a typeof array` |`/a typeof /b`<br>`/a typeof 2`                      |

## 相關文件

- [函式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/functions/)
