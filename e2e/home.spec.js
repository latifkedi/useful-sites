// The home page is pre-rendered into index.html by data/emit.py and must be
// byte for byte what app.js's homeHTML() draws -- otherwise the page shifts
// on load, and the two quietly drift apart.
const { test, expect } = require("@playwright/test");
const { ready } = require("./helpers");

test("the pre-rendered home is exactly what app.js draws", async ({ page, request }) => {
  const src = await (await request.get("/index.html")).text();
  await page.goto("/");
  await ready(page);
  const pre = await page.evaluate(html => {
    const doc = new DOMParser().parseFromString(html, "text/html");
    doc.querySelector("#list [data-pre]").removeAttribute("data-pre");
    return doc.querySelector("#list").innerHTML;
  }, src);
  /* Turkish and back: the second English home comes from homeHTML(). */
  await page.evaluate(() => document.querySelector("#langbtn").click());
  await expect(page.locator("html")).toHaveAttribute("lang", "tr");
  await page.evaluate(() => document.querySelector("#langbtn").click());
  await expect(page.locator("html")).toHaveAttribute("lang", "en");
  await expect(page.locator("#list [data-pre]")).toHaveCount(0);
  expect(await page.locator("#list").evaluate(el => el.innerHTML)).toBe(pre);
});

test("the hero carries the live record count", async ({ page }) => {
  await page.goto("/");
  await ready(page);
  const n = await page.evaluate(() => window.LINKS.length);
  await expect(page.locator("#hero em")).toHaveText(n.toLocaleString("en-US"));
});

test("the proof line under the hero carries live numbers; a query chip runs a search", async ({ page }) => {
  await page.goto("/");
  await ready(page);
  const f = await page.evaluate(() => ({
    n: window.LINKS.length.toLocaleString("en-US"),
    flagged: window.LINKS.filter(d => d.hs).length,
    last: window.LINKS.reduce((m, d) => d.ver && d.ver > m ? d.ver : m, ""),
  }));
  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const day = +f.last.slice(8, 10) + " " + months[+f.last.slice(5, 7) - 1] + " " + f.last.slice(0, 4);
  await expect(page.locator(".proof")).toHaveText(
    f.n + " links · last checked " + day + " · " + f.flagged + " flagged archived or dormant · no trackers · works offline");
  const chips = page.locator(".tryq .chip");
  expect(await chips.count()).toBeGreaterThanOrEqual(4);
  await chips.filter({ hasText: "postgres" }).click();
  await expect(page).toHaveURL(/\?q=postgres$/);
  await expect(page.locator("#list .rec").first()).toBeVisible();
});

test("desktop: Start Here sits above the fold", async ({ page, isMobile }) => {
  test.skip(isMobile, "on phones the index comes first");
  await page.goto("/");
  await ready(page);
  const box = await page.locator(".hpicks li").first().boundingBox();
  expect(box.y + box.height).toBeLessThan(900);
});
