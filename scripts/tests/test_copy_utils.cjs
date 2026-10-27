const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { spawnSync } = require('node:child_process');

const root = path.resolve(__dirname, '../..');
function load(context, file) {
  vm.runInContext(fs.readFileSync(path.join(root, file), 'utf8'), context, { filename: file });
}
function fixture() {
  const copied = [];
  const context = vm.createContext({
    window: { navigator: { clipboard: { writeText: text => copied.push(text) } } },
    document: {
      querySelectorAll: () => [], getElementById: () => null, addEventListener() {},
      createElement: () => ({ attrs: {}, setAttribute(name, value) { this.attrs[name] = value; } })
    }
  });
  load(context, 'assets/js/copy-utils.js');
  return { context, copied, convert: context.window.CopyUtils.convertToCurl };
}
// Parse generated shell text as data. Never execute the generated cURL request.
function argv(command) {
  const result = spawnSync('python3', ['-c', 'import json,shlex,sys; print(json.dumps(shlex.split(sys.stdin.read())))'],
    { input: command, encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
  return JSON.parse(result.stdout);
}

test('request paths retain query parameters and add pretty only when absent', () => {
  const { convert } = fixture();
  for (const [request, expected] of [
    ['GET _cat/indices\n', 'http://localhost:9200/_cat/indices?pretty'],
    ['GET /logs/_search?size=1', 'http://localhost:9200/logs/_search?size=1&pretty'],
    ['GET /logs/_search?pretty=false&size=1', 'http://localhost:9200/logs/_search?pretty=false&size=1'],
    ['GET /logs/_search?size=1&pretty', 'http://localhost:9200/logs/_search?size=1&pretty']
  ]) {
    assert.deepEqual(argv(convert(request, false)), ['curl', '-XGET', expected]);
  }
});

test('Security examples retain HTTPS and the admin password placeholder', () => {
  assert.deepEqual(argv(fixture().convert('GET /_cluster/health', true)),
    ['curl', '-k', '-u', 'admin:<custom-admin-password>', '-XGET', 'https://localhost:9200/_cluster/health?pretty']);
});

test('array bodies and apostrophes survive shell quoting without changing JSON values', () => {
  const value = [{ name: "O'Reilly", path: 'C:\\logs', message: '台灣文件' }];
  const args = argv(fixture().convert('POST /_example\n' + JSON.stringify(value), false));
  assert.equal(args[2], 'http://localhost:9200/_example?pretty');
  assert.equal(args[args.indexOf('-H') + 1], 'Content-Type: application/json');
  assert.deepEqual(JSON.parse(args.find(arg => arg.startsWith('-d')).slice(2)), value);
});

test('Dev Tools triple quoted content becomes valid JSON with the same text', () => {
  const content = 'line one\n"quoted"\tC:\\logs\r\nO\'Reilly';
  const request = 'POST /_example\n{"script":{"source":"""' + content + '"""}}';
  const args = argv(fixture().convert(request, false));
  assert.equal(JSON.parse(args.find(arg => arg.startsWith('-d')).slice(2)).script.source, content);
});

test('both page button styles use the shared conversion and preserve Chinese labels', () => {
  const { context, copied, convert } = fixture();
  load(context, 'assets/js/copy-button.js');
  load(context, 'assets/js/listener.js');
  const request = 'POST /logs/_search\n{"query":{"match":{"name":"O\'Reilly"}}}';
  const button = context.createButton(request, '複製為 cURL', '以 cURL 格式複製程式碼', true, false);
  assert.equal(button.innerText, '複製為 cURL');
  assert.equal(button.attrs['data-text'], convert(request, false));
  context.copyAsCurl({ closest: () => ({ querySelector: () => ({ textContent: request }) }) });
  assert.deepEqual(copied, [button.attrs['data-text']]);
});

test('the rendered page loads the shared converter before either button script', () => {
  const layout = fs.readFileSync(path.join(root, '_layouts/default.html'), 'utf8');
  const helper = layout.indexOf('/assets/js/copy-utils.js');
  assert.ok(helper >= 0);
  assert.ok(helper < layout.indexOf('/assets/js/copy-button.js'));
  assert.ok(helper < layout.indexOf('/assets/js/listener.js'));
});
