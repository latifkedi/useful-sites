// Offline and installable: after one visit the service worker (sw.js) has
// cached the page and its stamped files, so the site opens with no network
// -- including a view never opened before, because the app draws views from
// the query itself. The manifest and its icons are served.
const { test, expect } = require("@playwright/test");
const { ready, watchErrors } = require("./helpers");

async function installed(page) {
  await page.evaluate(() => navigator.serviceWorker.ready);
  /* the install step caches the page and what it references */
  await page.waitForFunction(async () => {
    const names = await caches.keys();
    if (!names.length) return false;
    const keys = await (await caches.open(names[0])).keys();
    return keys.some(r => /app\.js\?v=/.test(r.url)) && keys.some(r => /links\.js\?v=/.test(r.url));
  });
}

test("after one visit the site opens offline, even a view never opened", async ({ page, context }) => {
  await page.goto("/");
  await ready(page);
  await installed(page);
  await context.setOffline(true);
  const errors = watchErrors(page);
  await page.goto("/?cat=web");
  await ready(page);
  await expect(page.locator("h1:visible")).toHaveCount(1);
  await expect(page.locator("#list .rec").first()).toBeVisible();
  /* searching works offline too; inside a category the h1 stays the
     category and the results get an h2 */
  await page.locator("#q").fill("css");
  await expect(page.locator("#list h2").first()).toContainText("css");
  expect(errors).toEqual([]);
});

test("a repeat visit takes the stamped files from the service worker", async ({ page }) => {
  await page.goto("/");
  await ready(page);
  await installed(page);
  const fromSW = [];
  page.on("response", r => { if (/\?v=/.test(r.url()) && r.fromServiceWorker()) fromSW.push(r.url()) });
  await page.reload();
  await ready(page);
  expect(fromSW.some(u => /app\.js\?v=/.test(u))).toBe(true);
  expect(fromSW.some(u => /links\.js\?v=/.test(u))).toBe(true);
});

test("the manifest and every icon it names are served", async ({ request }) => {
  const man = await (await request.get("/manifest.webmanifest")).json();
  expect(man.start_url).toBe("./");
  expect(man.display).toBe("standalone");
  for (const icon of man.icons) {
    const r = await request.get("/" + icon.src);
    expect(r.ok(), icon.src).toBe(true);
    expect(r.headers()["content-type"]).toContain("image/png");
  }
});
