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

test("records off screen skip layout, and the fade-in is short", async ({ page }) => {
  await page.goto("/?cat=diller");
  await ready(page);
  const s = await page.evaluate(() => ({
    cv: getComputedStyle(document.querySelector("#list .rec")).contentVisibility,
    dur: parseFloat(getComputedStyle(document.querySelector("#list .catpage")).animationDuration),
  }));
  expect(s.cv).toBe("auto");
  expect(s.dur).toBeLessThanOrEqual(0.2);
});

test("reduced motion: no fade-in", async ({ browser }) => {
  const ctx = await browser.newContext({ reducedMotion: "reduce" });
  const page = await ctx.newPage();
  await page.goto("/?cat=diller");
  await ready(page);
  expect(await page.evaluate(() => getComputedStyle(document.querySelector("#list .catpage")).animationName)).toBe("none");
  await ctx.close();
});

test("a deep link shows a skeleton, not the home, until the app draws", async ({ page }) => {
  await page.route("**/app.js*", route => route.abort());
  await page.goto("/?cat=web");
  await expect(page.locator("html")).toHaveClass(/pending/);
  await expect(page.locator("#list [data-pre]")).toBeHidden();
});

/* WCAG AA for body text: every text colour on every surface it sits on, both themes. */
for (const scheme of ["light", "dark"]) {
  test("contrast: text tokens reach 4.5:1 on every surface (" + scheme + ")", async ({ page }) => {
    if (scheme === "dark") await page.addInitScript(() => localStorage.setItem("theme", "dark"));
    await page.goto("/");
    await ready(page);
    const low = await page.evaluate(() => {
      const cs = getComputedStyle(document.documentElement);
      const hex = n => cs.getPropertyValue("--" + n).trim();
      const lum = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16) / 255)
        .map(v => v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4))
        .reduce((s, v, i) => s + v * [.2126, .7152, .0722][i], 0);
      const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05) };
      const out = [];
      for (const f of ["fg", "dim", "faint", "red"])
        for (const b of ["bg", "panel", "field", "red-soft", "mark"])
          if (ratio(hex(f), hex(b)) < 4.5) out.push(f + "/" + b + " " + ratio(hex(f), hex(b)).toFixed(2));
      if (ratio(hex("on-red"), hex("red")) < 4.5) out.push("on-red/red");
      return out;
    });
    expect(low).toEqual([]);
  });
}

test("prefers-contrast: more darkens the faint text; forced colours mark the pressed state", async ({ browser }) => {
  const ctx = await browser.newContext({ contrast: "more" });
  const page = await ctx.newPage();
  await page.goto("/");
  await ready(page);
  expect(await page.evaluate(() => getComputedStyle(document.documentElement).getPropertyValue("--faint").trim())).toBe("#46423a");
  await ctx.close();
  const ctx2 = await browser.newContext({ forcedColors: "active" });
  const p2 = await ctx2.newPage();
  await p2.goto("/?cat=diller&free=1");
  await ready(p2);
  expect(await p2.locator("#list .tb .chip.on").evaluate(el => getComputedStyle(el).forcedColorAdjust)).toBe("none");
  await ctx2.close();
});
