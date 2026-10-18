// The goal paths, the tag pages and the legacy field links. The new static
// pages hold the same rules as the other k/ pages (shared stylesheet, one h1,
// no sideways scroll, clean console); a removed field key still lands.
const { test, expect } = require("@playwright/test");
const { watchErrors, ready, overflow } = require("./helpers");

for (const url of ["/k/yol/index.html", "/k/yol/veri-analisti.html", "/k/en/path/index.html",
                   "/k/en/path/security-beginner.html", "/k/t/python.html", "/k/en/tag/python.html"]) {
  test(url + ": shared stylesheet, one h1, no sideways scroll, clean console", async ({ page, request }) => {
    const errors = watchErrors(page);
    const html = await (await request.get(url)).text();
    expect(html).not.toContain("<style");
    expect(html).toMatch(/<link rel="stylesheet" href="(\.\.\/)+style\.css\?v=[0-9a-f]{8}">/);
    expect(html).toMatch(/<link rel="alternate" hreflang="tr" href="[^"]+">/);
    expect(html).toMatch(/<link rel="alternate" hreflang="en" href="[^"]+">/);
    await page.goto(url);
    await expect(page.locator("h1:visible")).toHaveCount(1);
    expect(await overflow(page)).toBeLessThanOrEqual(0);
    expect(errors).toEqual([]);
  });
}

test("a path step links to its entry on the heading page", async ({ page }) => {
  await page.goto("/k/en/path/data-analyst.html");
  const steps = page.locator("article.rec");
  expect(await steps.count()).toBeGreaterThanOrEqual(8);
  await steps.first().locator(".path a").click();
  await expect(page).toHaveURL(/\/k\/en\/[a-z_]+\.html#[a-z0-9-]+$/);
  const id = new URL(page.url()).hash.slice(1);
  await expect(page.locator("#" + id)).toBeInViewport();
});

test("the app footer links to the learning paths", async ({ page }) => {
  await page.goto("/");
  await ready(page);
  await expect(page.locator('#foot-t a[href="k/en/path/index.html"]')).toHaveCount(1);
});

/* 'verialan' (Data) was folded into Data & AI in October 2026. */
test("an old ?f=verialan link opens Data & AI and the address is corrected", async ({ page }) => {
  const errors = watchErrors(page);
  await page.goto("/?f=verialan");
  await ready(page);
  await expect(page.locator("h1:visible")).toContainText("Data & AI");
  await expect(page).toHaveURL(/\?f=yapayzeka$/);
  expect(errors).toEqual([]);
});
