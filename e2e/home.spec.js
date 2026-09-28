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
  /* English and back: the second Turkish home comes from homeHTML(). */
  await page.evaluate(() => document.querySelector("#langbtn").click());
  await expect(page.locator("html")).toHaveAttribute("lang", "en");
  await page.evaluate(() => document.querySelector("#langbtn").click());
  await expect(page.locator("html")).toHaveAttribute("lang", "tr");
  await expect(page.locator("#list [data-pre]")).toHaveCount(0);
  expect(await page.locator("#list").evaluate(el => el.innerHTML)).toBe(pre);
});

test("the hero carries the live record count", async ({ page }) => {
  await page.goto("/");
  await ready(page);
  const n = await page.evaluate(() => window.LINKS.length);
  await expect(page.locator("#hero em")).toHaveText(String(n));
});
