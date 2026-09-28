// The text version under k/ (for crawlers and readers without JavaScript):
// it shares style.css with the app, carries no inline style (CSP
// style-src 'self'), and holds the same one-h1, no-sideways-scroll rules.
const { test, expect } = require("@playwright/test");
const { watchErrors, overflow } = require("./helpers");

for (const url of ["/k/index.html", "/k/diller.html", "/k/tesekkur.html", "/k/en/index.html", "/k/en/diller.html"]) {
  test(url + ": shared stylesheet, one h1, no sideways scroll, clean console", async ({ page, request }) => {
    const errors = watchErrors(page);
    const html = await (await request.get(url)).text();
    expect(html).not.toContain("<style");
    expect(html).toMatch(/<link rel="stylesheet" href="(\.\.\/)+style\.css\?v=[0-9a-f]{8}">/);
    await page.goto(url);
    await expect(page.locator("h1:visible")).toHaveCount(1);
    expect(await overflow(page)).toBeLessThanOrEqual(0);
    expect(await page.evaluate(() => getComputedStyle(document.body).backgroundColor)).not.toBe("rgba(0, 0, 0, 0)");
    expect(errors).toEqual([]);
  });
}

test("an entry's anchor on a static page brings that entry into view", async ({ page }) => {
  await page.goto("/k/c_rust.html");
  const target = page.locator("article.rec").nth(12);
  const id = await target.getAttribute("id");
  expect(id).toMatch(/^[a-z0-9-]+$/);
  await page.goto("/k/c_rust.html#" + id);
  await expect(target).toBeInViewport();
});
