---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Painless 語言參考"
parent: Painless scripting language
nav_order: 10
---

# Painless 語言參考

本頁面說明 Painless 的語法：包括其類型、運算子、陳述式、函式與正規表示式。關於特定指令碼情境所提供的欄位與變數，請參閱[在指令碼中存取文件欄位]({{site.url}}{{site.baseurl}}/scripting/accessing-fields/)與[指令碼情境]({{site.url}}{{site.baseurl}}/scripting/script-contexts/)。

若要試用本頁面上的任何語法，請使用 [Execute Inline Script API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/exec-script/)，它會執行指令碼並回傳結果。將本頁面的任何程式碼片段或您自己的指令碼，代入下列請求的 `source` 欄位：

```json
POST _scripts/painless/_execute
{
  "script": {
    "source": "int a = 4; def b = 2.5; return a * b"
  }
}
```
{% include copy-curl.html %}

OpenSearch 會回傳轉換為字串的指令碼結果：

```json
{
  "result": "10.0"
}
```

## 類型

Painless 是靜態類型語言，但允許您延後選擇類型。當您知道類型時，請以具體類型宣告變數：

```js
int count = 42;
double price = 249.99;
boolean onSale = true;
String sku = "AUD-1001";
```

當類型會變動時，請以 `def` 宣告。一個欄位在某份文件中可能只有單一值，在另一份文件中則是值的陣列，而 `def` 變數兩者皆可接受，因此指令碼可以測試它收到的是哪一種：

```js
def ratings = params.ratings;
return ratings instanceof List ? ratings.size() : 1;
```

具體類型會在指令碼編譯時檢查，而 `def` 類型則是在指令碼每次執行時檢查。延後檢查會耗費少量效能，並將類型不符轉變為執行時期錯誤，因此只要類型固定，就應宣告具體類型。將前述指令碼的變數宣告為 `List` 時，對於有多個評分的文件會回傳評分數量，但對於只有一個評分的文件則會在執行時期失敗，並出現 `class java.lang.Integer cannot be cast to class java.util.List`。

下表列出基本類型及其與 `def` 相容的裝箱後的對應類型。

類型 | 說明
:--- | :---
`byte`, `short`, `int`, `long` | 位元寬度遞增的有號整數。算術運算溢位時會環繞，而不是擲回錯誤。
`float`, `double` | 浮點數。帶有小數點的數值字面值是 `double`。
`boolean` | `true` 或 `false`。
`char` | 單一 UTF-16 碼元。沒有字元字面值，因此需從單一字元字串轉型：`(char) 'A'`。
`def` | 任何類型的預留位置，於執行時期解析。

整數除法會向零截斷，而整數與浮點值結合的運算會回傳浮點結果。下表各列出一個範例。

運算式 | 結果
:--- | :---
`7 / 2` | `3`
`7 / 2.0` | `3.5`

整數算術在溢位時會無聲地環繞，因此 `int i = 2147483647; return i + 1` 會回傳 `-2147483648`。對於可能超出 `int` 範圍的值，請使用 `long`。
{: .warning}

## 轉型

將值轉型為數值範圍較寬的數值類型（例如 `int` 轉為 `double`）會自動進行。將值轉型為數值範圍較窄的數值類型（例如 `double` 轉為 `int`）則必須明確撰寫，且會截斷值而非四捨五入：

```js
double d = 9.7;
return (int) d;  // 9
```

`def` 值會自動轉型為其目標類型，但檢查是在執行時期而非編譯時期進行。將 `def` 值轉型為數值範圍較窄的類型時，仍必須明確撰寫：

```js
def x = 41.7;
int y = (int) x;
return y;
```

若沒有轉型，`int y = x` 會編譯成功，然後在第一份文件上失敗並出現 `cannot implicitly cast def [double] to int`。這是 `def` 的實際取捨：以具體類型撰寫的相同指派 `double d = 9.7; int i = d`，則會在編譯時期被拒絕。

使用 `instanceof` 測試 `def` 值的執行時期類型：

```js
def x = new ArrayList();
return x instanceof List;  // true
```

## 運算子

Painless 支援 Java 的算術、比較、位元與邏輯運算子，並新增了兩個自有運算子。下表列出 Painless 特有或與 Java 不同的運算子。

運算子 | 說明
:--- | :---
`?:` | null 合併運算子，又稱 Elvis 運算子。除非 `x` 為 `null`，否則 `x ?: "fallback"` 會評估為 `x`。
`?.` | Null 安全成員存取。當 `m.a` 為 `null` 時，`m.a?.toString()` 會評估為 `null`，而不是擲回錯誤。
`=~` | 測試正規表示式是否在字串中的任何位置符合。範例請參閱[正規表示式](#regular-expressions)。
`==~` | 測試正規表示式是否符合整個字串。範例請參閱[正規表示式](#regular-expressions)。

將 `?.` 與 `?:` 結合可取代一般的 null 檢查：

```js
def m = ["a": null];
return m.a?.toString() ?: "was null";  // was null
```

使用 `+` 進行字串串接時，會自動轉換另一個運算元，因此 `"id-" + 42` 會回傳 `id-42`。

## 集合與陣列

Painless 為清單與映射提供了字面值語法，因此指令碼可以在不指定類別名稱的情況下建構結構化值。下表列出兩種字面值形式及其產生的值。

運算式 | 結果
:--- | :---
`[3, 1, 2]` | `[3, 1, 2]`
`["a": 1, "b": 2]` | `{a=1, b=2}`

空的映射字面值是 `[:]`，空的清單字面值是 `[]`。負數清單索引從結尾算起，因此 `[10, 20, 30][-1]` 是 `30`。

映射項目可透過點號與方括號兩種記法存取。`params.a` 與 `params["b"]` 等價，而當鍵不是有效的識別字時，必須使用方括號記法。

陣列使用 Java 語法，並帶有 `length` 屬性：

```js
int[] a = new int[3];
a[0] = 5;
return a[0] + a.length;  // 8
```

多維陣列的運作方式與 Java 相同：`int[][] g = new int[2][2]`。

透過映射的項目集迭代映射：

```js
def m = ["b": 2, "a": 1];
def out = [];
for (def e : m.entrySet()) {
  out.add(e.getKey() + "=" + e.getValue());
}
return out;  // [a=1, b=2]
```

## 陳述式

Painless 支援 `if`/`else`、三元條件式、`for`、增強版 `for`、`while`、`do`/`while`、`break`、`continue` 與 `return`：

```js
int s = 0;
for (int i = 1; i <= 4; i++) {
  s += i;
}
return s;  // 10
```

```js
int s = 0;
for (int v : [2, 4, 6]) {
  s += v;
}
return s;  // 12
```

未以明確 `return` 結尾的指令碼，會回傳其最後一個運算式的值，這就是為什麼像 `doc['price'].value * 2` 這樣的單行指令碼不需要 `return`。

`try`/`catch` 區塊只能捕捉 Painless 允許清單中的例外類型：

```js
int z = 0;
try {
  return 4 / z;
} catch (ArithmeticException e) {
  return "divide by zero";
}
```

`throw` 陳述式會擲回例外，同一指令碼中的 `catch` 子句可以處理它：

```js
try {
  throw new IllegalArgumentException("bad sku");
} catch (IllegalArgumentException e) {
  return "caught: " + e.getMessage();
}
```

`switch` 陳述式、帶標籤的 `break` 陳述式與 `finally` 區塊在 Painless 中無法使用，且各自都會產生編譯錯誤。由於指令碼無法定義類別，`new` 無法套用於使用者定義的類型。
{: .note}

## 函式

宣告函式時必須明確指定回傳型別與參數型別：

```js
int sq(int n) {
  return n * n;
}
return sq(7);  // 49
```

所有函式宣告都必須位於指令碼的陳述式之前。若宣告出現在陳述式之後，將無法編譯並產生 `unexpected token ['('] was expecting one of [{<EOF>, ';'}]`，因此 `int a = 1; int sq(int n) { return n * n }` 是無效的。宣告可以任意順序出現，所以函式可以呼叫在其之後才宣告的另一個函式。

函式可以遞迴，也可以透過不同數量的參數進行多載。兩個接受相同參數數量的函式無論其型別為何都會衝突，並產生 `invalid function definition: found duplicate function [f/1]` 錯誤，因為 Painless 僅以名稱與參數數量來識別函式。

下表列出遞迴函式與一組多載函式的範例，以及每個指令碼回傳的結果。

運算式 | 結果
:--- | :---
`int f(int n) { return n <= 1 ? 1 : n * f(n-1) } return f(5)` | `120`
`int f(int n){return n} int f(int a,int b){return a+b} return f(1,2)` | `3`

函式主體只能讀取自己的參數。它無法讀取指令碼中宣告的變數，也無法讀取 `params`，因此 `int g() { return (int) params.n }` 無法編譯並產生 `cannot resolve symbol [params.n]`。請將函式需要的每個值都以參數傳入，如 `int g(int v) { return v } return g((int) params.n)` 所示。

由於宣告不能出現在陳述式之後，讀取指令碼變數的函式會依其所在位置產生不同的錯誤。`int g() { return x } int x = 5;` 會回報 `cannot resolve symbol [x]`，而 `int x = 5; int g() { return x }` 會回報 `unexpected token ['('] was expecting one of [{<EOF>, ';'}]`，且根本不會執行到該變數。

## Lambda 與方法參照

Lambda 提供函式式介面的主體，使 Java 的集合與串流方法得以使用：

```js
def l = [3, 1, 2];
l.sort((a, b) -> a - b);
return l;  // [1, 2, 3]
```

```js
def l = [1, 2, 3, 4];
l.removeIf(x -> x % 2 == 0);
return l;  // [1, 3]
```

方法參照使用 `::`：

```js
def l = ["b", "a"];
l.sort(String::compareTo);
return l;  // [a, b]
```

Java 的串流方法皆可使用，但 `Stream` 沒有提供 `sum` 方法：呼叫它會無法編譯並產生 `member method [java.util.stream.Stream, sum/0] not found`。請先將串流轉換為基本型別串流：

```js
return [1, 2, 3].stream().mapToInt(x -> x * 2).sum();  // 12
```

## 正規表示式

正規表示式字面值以斜線界定，旗標位於結尾斜線之後。使用 `=~` 進行搜尋，使用 `==~` 比對整個字串。下表列出每個運算子的範例。

運算式 | 結果
:--- | :---
`"AUD-1001" =~ /^AUD-/` | `true`
`"AUD-1001" ==~ /^[A-Z]{3}-\d{4}$/` | `true`

這兩個運算子的差異在於模式是否必須比對整個字串。下列請求將兩者套用至相同的值：

```json
POST _scripts/painless/_execute
{
  "script": {
    "source": "def found = params.sku =~ /\\d{4}/; def matched = params.sku ==~ /^[A-Z]{3}-\\d{4}$/; return \"found=\" + found + \" matched=\" + matched",
    "params": { "sku": "AUD-1001" }
  }
}
```
{% include copy-curl.html %}

兩個運算子都回報比對成功：

```json
{
  "result": "found=true matched=true"
}
```

將 `sku` 改為 `Refurbished AUD-1001 unit` 會回傳 `found=true matched=false`。這四個數字仍存在於字串中的某處，因此 `=~` 比對成功，但字串整體已不再是 SKU，所以 `==~` 比對失敗。

若要使用擷取群組，請建立 `Matcher`：

```js
Matcher m = /(\w+)-(\d+)/.matcher("AUD-1001");
if (m.find()) {
  return m.group(2);  // 1001
}
return "no match";
```

群組只能以編號存取。`m.group("name")` 無法編譯並產生 `Cannot cast from [java.lang.String] to [int]`，因為 `group` 的字串多載未列入允許清單，因此無法讀取具名擷取群組。
{: .note}

Painless 以自己的版本取代 Java 的 `replaceAll` 與 `replaceFirst` 方法，這些版本接受一個模式與一個函式，而非兩個字串。提供函式可讓替換內容取決於比對到的結果。下表列出每個方法的範例。

運算式 | 結果
:--- | :---
`"AUD-1001".replaceAll(/\d/, m -> "#")` | `AUD-####`
`"a1b2".replaceFirst(/\d/, m -> "X")` | `aXb2`

以純字串作為替換內容會失敗並產生 `Cannot cast from [java.lang.String] to [java.util.function.Function]`。

正規表示式預設在複雜度預算下執行，也可以完全停用。請參閱 [控制正規表示式]({{site.url}}{{site.baseurl}}/scripting/painless/#controlling-regular-expressions)。

## 可用的程式庫

Painless 公開 Java 標準程式庫的子集。常用的類別包括 `String`、`StringBuilder`、`Math`、裝箱後的數值型別、`List`、`Map`、`Set`、`ArrayList`、`HashMap`、`HashSet`、`java.time` 類別，以及 `Matcher` 與 `Pattern`。完整清單請參閱 OpenSearch 儲存庫中的 [允許清單定義](https://github.com/opensearch-project/OpenSearch/tree/main/modules/lang-painless/src/main/resources/org/opensearch/painless/spi)，其中列出每個允許類別上可呼叫的欄位、建構子與方法。下表列出呼叫允許清單中類別的範例。

運算式 | 結果
:--- | :---
`"  Aurora ".trim().toUpperCase()` | `AURORA`
`Math.round(Math.sqrt(50) * 100) / 100.0` | `7.07`
`ZonedDateTime.parse("2024-03-15T00:00:00Z").getDayOfWeek().toString()` | `FRIDAY`

若命名允許清單未包含的類別，或呼叫其未包含的方法或建構子，會導致編譯時期錯誤，因此這類指令碼永遠不會對您的資料執行。下表列出代表性的錯誤。

嘗試 | 錯誤
:--- | :---
`"x".getClass()` | `member method [java.lang.String, getClass/0] not found`
`new java.io.File("/etc/passwd")` | `Not a type [java.io.File].`
`new Thread()` | `Not a type [Thread].`

反射、類別載入、檔案與網路存取、執行緒建立以及時鐘讀取皆被排除。相關原因以及進一步限制指令碼的設定，請參閱 [指令碼安全性]({{site.url}}{{site.baseurl}}/scripting/script-security/)。

## 判斷值的型別

當指令碼因值的型別不如預期而失敗時，請將該值包在 `Debug.explain` 中。指令碼會停止，OpenSearch 會在錯誤回應中回報該型別。下列搜尋會檢查 `scripting-products` 索引中的日期欄位，該索引建立於 [測試設定]({{site.url}}{{site.baseurl}}/scripting/using-scripts/#test-setup)：

```json
GET scripting-products/_search
{
  "_source": false,
  "query": { "term": { "sku": "AUD-1001" } },
  "script_fields": {
    "inspect": {
      "script": { "source": "Debug.explain(doc['release_date'].value)" }
    }
  }
}
```
{% include copy-curl.html %}

`painless_class`、`java_class` 與 `to_string` 欄位可識別該值：

<details open markdown="block">
<summary>
  回應
</summary>

```json
{
  "error": {
    "root_cause": [
      {
        "type": "script_exception",
        "reason": "runtime error",
        "painless_class": "java.time.ZonedDateTime",
        "to_string": "2024-03-15T00:00Z",
        "java_class": "java.time.ZonedDateTime",
        "script_stack": [
          "Debug.explain(doc['release_date'].value)",
          "                                 ^---- HERE"
        ],
        "script": "Debug.explain(doc['release_date'].value)",
        "lang": "painless",
        "position": {
          "offset": 33,
          "start": 0,
          "end": 40
        }
      }
    ],
    "type": "search_phase_execution_exception",
    "reason": "all shards failed",
    "phase": "query",
    "grouped": true
  },
  "status": 400
}
```
</details>

`Debug.explain` 一律會使請求失敗，因此取得答案後請將其移除。

## 範例

下列指令碼結合了使用者定義函式、含有擷取群組的正規表示式、映射以及迴圈，用來分類產品清單：

```json
POST _scripts/painless/_execute
{
  "script": {
    "source": "String tier(double p) { if (p >= 500) return 'premium'; else if (p >= 100) return 'standard'; return 'budget' } def out = [:]; for (int i = 0; i < params.items.length; i++) { def it = params.items[i]; Matcher m = /^([A-Z]{3})-/.matcher(it.sku); String dept = m.find() ? m.group(1) : 'UNK'; out[it.sku] = dept + ':' + tier(it.price) } return out",
    "params": {
      "items": [
        { "sku": "AUD-1001", "price": 249.99 },
        { "sku": "DSP-3001", "price": 599.0 },
        { "sku": "x", "price": 12.5 }
      ]
    }
  }
}
```
{% include copy-curl.html %}

每個產品都會標上其部門前綴與價格層級：

```json
{
  "result": "{DSP-3001=DSP:premium, AUD-1001=AUD:standard, x=UNK:budget}"
}
```

在 Painless 中，單引號與雙引號一樣都是字串分隔符號。在 JSON 請求本文中使用單引號，可避免對指令碼中的每個引號進行逸出。
{: .tip}

## 相關文件

- [指令碼情境]({{site.url}}{{site.baseurl}}/scripting/script-contexts/)
- [指令碼安全性]({{site.url}}{{site.baseurl}}/scripting/script-security/)
