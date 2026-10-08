const { test } = require('node:test');
const assert = require('node:assert/strict');
const { createController, safeResultURL } = require('../../assets/js/search.js');
const base = '/opensearch-documentation-website-zh-tw/3.9';

test('Chinese, English API names and section filters reach the local engine unchanged', async () => {
  const seen = [];
  const results = [];
  const engine = { async search(query, options) { seen.push([query, options]); return { results: [{ data: async () => ({ url: base + '/api/', meta: { title: 'API' } }) }] }; } };
  const controller = createController({ load: async () => engine, results: (items) => results.push(items) });
  await controller.search('  叢集 _search  ', { filters: { section: 'API 參考' } });
  assert.deepEqual(seen, [['叢集 _search', { filters: { section: 'API 參考' } }]]);
  assert.equal(results[0][0].meta.title, 'API');
});

test('an older response cannot overwrite the current query', async () => {
  let finishOld;
  const displayed = [];
  const engine = { search(query) { return query === 'old' ? new Promise(resolve => { finishOld = resolve; }) : Promise.resolve({ results: [{ data: async () => ({ value: query }) }] }); } };
  const controller = createController({ load: async () => engine, results: items => displayed.push(items) });
  const old = controller.search('old');
  await Promise.resolve();
  await controller.search('new');
  finishOld({ results: [{ data: async () => ({ value: 'old' }) }] });
  await old;
  assert.deepEqual(displayed, [[{ value: 'new' }]]);
});

test('clearing input cancels outstanding results and ends loading', async () => {
  let finish;
  const displayed = [], loading = [];
  const engine = { search() { return new Promise(resolve => { finish = resolve; }); } };
  const controller = createController({ load: async () => engine, results: items => displayed.push(items), loading: state => loading.push(state) });
  const pending = controller.search('叢集');
  await Promise.resolve();
  await controller.search('');
  finish({ results: [] });
  await pending;
  assert.deepEqual(displayed, [[]]);
  assert.equal(loading.at(-1), false);
});

test('load failures report an error and always clear the spinner', async () => {
  const errors = [], loading = [];
  const controller = createController({ load: async () => { throw new Error('offline'); }, error: e => errors.push(e.message), loading: x => loading.push(x) });
  await controller.search('index');
  assert.deepEqual(errors, ['offline']);
  assert.deepEqual(loading, [true, false]);
});

test('result links preserve queries/encoded fragments and reject other hosts or repository prefixes', () => {
  assert.equal(safeResultURL(base + '/api/?q=x#%E7%B4%A2%E5%BC%95'), base + '/api/?q=x#%E7%B4%A2%E5%BC%95');
  assert.equal(safeResultURL('https://evil.example/a'), null);
  assert.equal(safeResultURL('/latest/api/'), null);
  assert.equal(safeResultURL(base + '-evil/api/'), null);
  assert.equal(safeResultURL('javascript:alert(1)'), null);
});
