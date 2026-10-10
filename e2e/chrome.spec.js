// The frame around the list: the phone menu, the submit dialog, keyboard use.
const { test, expect } = require("@playwright/test");
const { ready } = require("./helpers");

test("desktop: the tools sit in the header, no menu button", async ({ page, isMobile }) => {
  test.skip(isMobile, "phones use the menu");
  await page.goto("/");
  await ready(page);
  await expect(page.locator("#acts")).toBeVisible();
  await expect(page.locator("#menub")).toBeHidden();
});

test("phone: the menu opens with named items, and the submit dialog replaces it", async ({ page, isMobile }) => {
  test.skip(!isMobile, "the tools are inline on desktop");
  await page.goto("/");
  await ready(page);
  await expect(page.locator("#acts")).toBeHidden();
  await page.locator("#menub").click();
  await expect(page.locator("#acts")).toBeVisible();
  await expect(page.locator("#langbtn")).toContainText("Türkçe");
  await expect(page.locator("#theme")).toContainText("Theme");
  await page.locator("#addbtn").click();
  await expect(page.locator("#sub")).toBeVisible();
  await expect(page.locator("#acts")).toBeHidden();
  await page.keyboard.press("Escape");
  await expect(page.locator("#sub")).toBeHidden();
});

test("the submit dialog switches tabs", async ({ page, isMobile }) => {
  await page.goto("/");
  await ready(page);
  if (isMobile) await page.locator("#menub").click();
  await page.locator("#addbtn").click();
  const tabs = page.locator("#sub [role=tab]");
  await expect(tabs.nth(0)).toHaveAttribute("aria-selected", "true");
  await tabs.nth(1).click();
  await expect(tabs.nth(1)).toHaveAttribute("aria-selected", "true");
  await expect(tabs.nth(0)).toHaveAttribute("aria-selected", "false");
});

test("keyboard: Tab reaches the skip link first, / focuses search, Escape clears", async ({ page, isMobile }) => {
  test.skip(isMobile, "no hardware keyboard on the phone profile");
  await page.goto("/");
  await ready(page);
  await page.keyboard.press("Tab");
  await expect(page.locator("#skip")).toBeFocused();
  await page.evaluate(() => document.activeElement.blur());
  await page.keyboard.press("/");
  await expect(page.locator("#q")).toBeFocused();
  await page.keyboard.type("docker");
  await expect(page.locator("#list h1")).toContainText("docker");
  await page.keyboard.press("Escape");
  await expect(page.locator("#q")).toHaveValue("");
  await expect(page.locator("body")).toHaveClass(/at-home/);
});

test("export: bookmarks file is the browser import format and carries the whole list", async ({ page }) => {
  await page.goto("/");
  await ready(page);
  const n = await page.evaluate(() => window.LINKS.length);
  const [dl] = await Promise.all([
    page.waitForEvent("download"),
    page.locator('[data-exp="bookmarks"]').click(),
  ]);
  expect(dl.suggestedFilename()).toBe("baglantilar-tumu.html");
  const text = require("fs").readFileSync(await dl.path(), "utf8");
  expect(text.startsWith("<!DOCTYPE NETSCAPE-Bookmark-file-1>")).toBe(true);
  expect((text.match(/<A HREF="/g) || []).length).toBe(n);
  expect(text).toContain("<DT><H3");
  expect(text).not.toMatch(/<A HREF="[^"]*"[^>]*>[^<]*<script/i);
});

test("export: bookmarks follow the filter", async ({ page }) => {
  await page.goto("/?cat=web");
  await ready(page);
  const n = await page.evaluate(() => window.LINKS.filter(d => d.cat === "web").length);
  const [dl] = await Promise.all([
    page.waitForEvent("download"),
    page.locator('[data-exp="bookmarks"]').click(),
  ]);
  expect(dl.suggestedFilename()).toBe("baglantilar-web.html");
  const text = require("fs").readFileSync(await dl.path(), "utf8");
  expect((text.match(/<A HREF="/g) || []).length).toBe(n);
});

test("a single record offers a pre-filled report that names the entry", async ({ page }) => {
  await page.goto("/");
  await ready(page);
  const rec = await page.evaluate(() => { const d = window.LINKS[0]; return { k: d._k, name: d.name, url: d.url } });
  await page.goto("/?e=" + encodeURIComponent(rec.k));
  await ready(page);
  const href = await page.locator("a.fix").getAttribute("href");
  const u = new URL(href);
  expect(u.origin + u.pathname).toBe("https://github.com/latifkedi/useful-sites/issues/new");
  expect(u.searchParams.get("template")).toBe("broken-entry.yml");
  expect(u.searchParams.get("title")).toBe("[fix] " + rec.name);
  expect(u.searchParams.get("url")).toBe(rec.url);
});

test("a record missing from the scan for weeks carries a badge; a fresh one does not", async ({ page }) => {
  /* Serve links.js with the first record's verification date moved back to 2020. */
  await page.route("**/links.js*", async route => {
    const res = await route.fetch();
    const body = (await res.text()).replace(/"ver":"[0-9-]+"/, '"ver":"2020-01-01"');
    await route.fulfill({ response: res, body });
  });
  await page.goto("/");
  await ready(page);
  const cat = await page.evaluate(() => window.LINKS.find(d => d.ver === "2020-01-01").cat);
  await page.goto("/?cat=" + cat);
  await ready(page);
  await expect(page.locator('.badge.chk[title*="2020-01-01"]')).toHaveCount(1);
  const fresh = await page.evaluate(() => window.LINKS.filter(d => d.ver && d.ver !== "2020-01-01").length);
  expect(fresh).toBeGreaterThan(100);
  await page.waitForLoadState("networkidle");
  await page.unroute("**/links.js*");
});

test("a record page lists what it is compared with, from either side", async ({ page }) => {
  await page.goto("/");
  await ready(page);
  const pair = await page.evaluate(() => {
    const d = window.LINKS.find(x => x.name === "Squoosh");
    const rival = window.LINKS[d.vs[0][0]];
    return { a: d._k, b: rival._k, an: d.name, bn: rival.name };
  });
  await page.goto("/?e=" + encodeURIComponent(pair.a));
  await ready(page);
  await expect(page.locator("h2.sh", { hasText: "Compare with" })).toBeVisible();
  await expect(page.locator(".vs li", { hasText: pair.bn })).toContainText("Where it runs, where the data lives");
  /* written on Squoosh only, shown on TinyPNG too */
  await page.goto("/?e=" + encodeURIComponent(pair.b));
  await ready(page);
  await expect(page.locator(".vs li", { hasText: pair.an })).toBeVisible();
  /* and the link leads to the other record's page */
  await page.locator(".vs li a", { hasText: pair.an }).click();
  await expect(page.locator("h1:visible")).toHaveText(pair.an);
});
