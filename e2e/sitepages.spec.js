// The pages about the directory (about, changes, weekly digests,
// alternatives, the tag index, credits): the same rules as every other k/
// page -- shared stylesheet, no inline style, one h1, no sideways scroll on a
// phone, a clean console -- and every link on them that stays on the site
// answers, down to the #anchor it names.
const fs = require("fs");
const path = require("path");
const { test, expect } = require("@playwright/test");
const { watchErrors, overflow } = require("./helpers");

const ROOT = path.join(__dirname, "..");
const first = dir => "/" + dir + "/" + fs.readdirSync(path.join(ROOT, ...dir.split("/"))).filter(f => f.endsWith(".html")).sort()[0];

const PAGES = [
  "/k/en/about.html", "/k/about.html", "/k/en/changes.html", "/k/changes.html",
  first("k/en/week"), first("k/week"), first("k/en/alt"), first("k/alt"),
  "/k/en/tag/index.html", "/k/t/index.html", "/k/en/credits.html", "/k/en/tag/python.html",
];

for (const url of PAGES) {
  test(url + ": shared stylesheet, one h1, no sideways scroll, clean console", async ({ page, request }) => {
    const errors = watchErrors(page);
    const html = await (await request.get(url)).text();
    expect(html).not.toContain("<style");
    expect(html).toMatch(/<link rel="stylesheet" href="(\.\.\/)+style\.css\?v=[0-9a-f]{8}">/);
    await page.goto(url);
    await expect(page.locator("h1:visible")).toHaveCount(1);
    expect(await overflow(page)).toBeLessThanOrEqual(0);
    await expect(page.locator("footer .sf a[href$='about.html']")).toHaveCount(1);
    expect(errors).toEqual([]);
  });

  test(url + ": every link that stays on the site answers, with its anchor", async ({ page, request }) => {
    await page.goto(url);
    const links = await page.evaluate(() => [...new Set([...document.querySelectorAll("a[href]")]
      .map(a => a.href).filter(h => h.startsWith(location.origin)))]);
    expect(links.length).toBeGreaterThan(3);
    const bodies = {};
    for (const href of links) {
      const u = new URL(href);
      const key = u.pathname;
      if (!(key in bodies)) {
        const r = await request.get(key);
        expect(r.status(), href).toBe(200);
        bodies[key] = await r.text();
      }
      if (u.hash && key.endsWith(".html"))
        expect(bodies[key], href).toContain('id="' + decodeURIComponent(u.hash.slice(1)) + '"');
    }
  });
}

test("k/en/index.html forwards to the English home", async ({ page }) => {
  await page.goto("/k/en/index.html");
  await page.waitForURL(u => new URL(u).pathname === "/");
  await expect(page.locator("h1#hero")).toHaveCount(1);
});

test("a heading page shows when each entry was checked, its archive copy and its alternatives page", async ({ page }) => {
  const alt = first("k/en/alt").split("/").pop();
  const cat = fs.readdirSync(path.join(ROOT, "k", "en")).filter(f => f.endsWith(".html"))
    .find(f => fs.readFileSync(path.join(ROOT, "k", "en", f), "utf8").includes('href="alt/' + alt + '"'));
  await page.goto("/k/en/" + cat);
  const recs = page.locator("article.rec");
  const n = await recs.count();
  await expect(page.locator("article.rec a.arch[href^='https://web.archive.org/web/']")).toHaveCount(n);
  expect(await page.locator("article.rec .age").count() + await page.locator("article.rec .badge.chk").count()).toBe(n);
  await page.locator('a[href="alt/' + alt + '"]').first().click();
  await expect(page).toHaveURL(new RegExp("/k/en/alt/" + alt.replace(".", "\\.") + "$"));
  expect(await page.locator("article.rec").count()).toBeGreaterThanOrEqual(4);
});
