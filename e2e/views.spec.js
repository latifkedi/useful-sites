// Every view, in both colour schemes, at desktop and phone size: exactly one
// visible h1, nothing to scroll sideways, a clean console.
const { test, expect } = require("@playwright/test");
const { watchErrors, ready, overflow } = require("./helpers");

const VIEWS = [
  ["home", "/"],
  ["area", "/?f=guvenlikalan"],
  ["category", "/?cat=diller"],
  ["category, page 2", "/?cat=diller&p=2"],
  ["search", "/?q=postgres"],
  ["search with no results", "/?q=zzqqxx"],
  ["recent", "/?new=1"],
  ["all links A-Z", "/?sort=az"],
  ["Turkish home", "/?lang=tr"],
  ["Turkish category", "/?cat=web&lang=tr"],
];

const PAPER = { light: "rgb(246, 241, 231)", dark: "rgb(21, 20, 15)" };

for (const scheme of ["light", "dark"]) {
  test.describe(scheme, () => {
    test.use({ colorScheme: scheme });
    /* The site opens light whatever the system prefers; dark is a saved choice. */
    test.beforeEach(async ({ page }) => {
      if (scheme === "dark") await page.addInitScript(() => localStorage.setItem("theme", "dark"));
    });

    for (const [name, url] of VIEWS) {
      test(name + ": one visible h1, no sideways scroll, clean console", async ({ page }) => {
        const errors = watchErrors(page);
        await page.goto(url);
        await ready(page);
        await expect(page.locator("h1:visible")).toHaveCount(1);
        expect(await overflow(page)).toBeLessThanOrEqual(0);
        expect(errors).toEqual([]);
      });
    }

    test("the page is on the " + scheme + " paper", async ({ page }) => {
      await page.goto("/");
      await ready(page);
      expect(await page.evaluate(() => getComputedStyle(document.body).backgroundColor)).toBe(PAPER[scheme]);
    });
  });
}

test("single entry: the entry's name is the only h1", async ({ page }) => {
  const errors = watchErrors(page);
  await page.goto("/?cat=diller");
  await ready(page);
  const first = page.locator("#list .rec").first();
  const name = (await first.locator("a.name").textContent()).trim();
  const perma = await first.locator('a[href^="?e="]').getAttribute("href");
  await page.goto("/" + perma);
  await ready(page);
  await expect(page.locator("h1:visible")).toHaveCount(1);
  await expect(page.locator("h1:visible")).toHaveText(name);
  expect(await overflow(page)).toBeLessThanOrEqual(0);
  expect(errors).toEqual([]);
});

test("a category's second page continues the numbering", async ({ page }) => {
  await page.goto("/?cat=diller&p=2");
  await ready(page);
  await expect(page.locator("#list .rec .no").first()).toHaveText("21");
});

test("the site opens light even when the system prefers dark", async ({ browser }) => {
  const ctx = await browser.newContext({ colorScheme: "dark" });
  const page = await ctx.newPage();
  await page.goto("/");
  await ready(page);
  await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  expect(await page.evaluate(() => getComputedStyle(document.body).backgroundColor)).toBe(PAPER.light);
  await ctx.close();
});
