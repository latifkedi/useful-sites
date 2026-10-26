// The edges of the app: deep links that must not jump, a page that works
// without JavaScript, per-view tab titles, bad addresses, keyboard and touch
// reach, print, the 404 page and how the scripts load.
const { test, expect } = require("@playwright/test");
const fs = require("fs");
const path = require("path");
const { ready, watchErrors } = require("./helpers");

const ROOT = path.join(__dirname, "..");

/* boot.js marks a deep link "pending" before the first paint; the header
   must already have its final, compact shape then, or it collapses when
   app.js draws (CLS). app.js is held back so the pending state stays. */
test("a deep link paints the final header before app.js runs", async ({ page, browser }) => {
  await page.route("**/app.js*", r => r.abort());
  await page.goto("/?cat=web");
  await expect(page.locator("html")).toHaveClass(/pending/);
  await expect(page.locator("#hero")).toBeHidden();
  const early = await page.locator("header.top").boundingBox();
  const p2 = await browser.newPage({ viewport: page.viewportSize() });
  await p2.goto("/?cat=web");
  await ready(p2);
  const late = await p2.locator("header.top").boundingBox();
  expect(Math.abs(early.height - late.height)).toBeLessThan(1);
  await p2.close();
});

test("the pre-rendered home links every heading to its static page; a plain click stays in the app", async ({ page, request }) => {
  const html = await (await request.get("/index.html")).text();
  const pre = html.slice(html.indexOf('<main id="list"'), html.indexOf("</main>"));
  const hrefs = [...pre.matchAll(/<a href="(k\/en\/[a-z_]+\.html)" data-cat="([a-z_]+)"/g)];
  expect(hrefs.length).toBeGreaterThan(40);
  for (const [, href, cat] of hrefs) {
    expect(href).toBe("k/en/" + cat + ".html");
    expect(fs.existsSync(path.join(ROOT, href)), href).toBe(true);
  }
  await page.goto("/");
  await ready(page);
  const first = page.locator(".fc a").first();
  const cat = await first.getAttribute("data-cat");
  await first.click();
  await expect(page).toHaveURL(new RegExp("\\?cat=" + cat + "$"));
  /* the Turkish home points at the Turkish pages */
  await page.goto("/?lang=tr");
  await ready(page);
  await expect(page.locator(".fc a").first()).toHaveAttribute("href", /^k\/[a-z_]+\.html$/);
});

test("desktop: a Ctrl-click on a home heading opens its static page in a new tab", async ({ page, context, isMobile }) => {
  test.skip(isMobile, "no modifier keys on the phone profile");
  await page.goto("/");
  await ready(page);
  const first = page.locator(".fc a").first();
  const href = await first.getAttribute("href");
  const [tab] = await Promise.all([context.waitForEvent("page"), first.click({ modifiers: ["Control"] })]);
  await tab.waitForURL(u => u.pathname.endsWith("/" + href));
  expect(page.url()).not.toContain("?cat=");
});

test("without JavaScript the home is English, says how to browse, and hides the script-only tools", async ({ browser }) => {
  const ctx = await browser.newContext({ javaScriptEnabled: false });
  const page = await ctx.newPage();
  await page.goto("/");
  await expect(page.locator("#t-title")).toHaveText("Useful Sites");
  const note = page.locator(".nojs");
  await expect(note).toBeVisible();
  await expect(note.locator('a[href="k/en/index.html"]')).toHaveCount(0);   // that page only forwards to /
  await expect(note.locator('a[href="k/index.html"]')).toHaveCount(1);
  for (const sel of ["#q", "#acts", "#menub", "#foot-x", "#foot-kb", "#savedb", "#rand", "#langbtn", "#theme"])
    await expect(page.locator(sel), sel).toBeHidden();
  for (const href of ["k/en/path/index.html", "k/en/about.html", "k/en/changes.html"])
    await expect(page.locator('#foot-t a[href="' + href + '"]')).toHaveCount(1);
  await ctx.close();
});

test("the app footer links About and Changes in both languages", async ({ page }) => {
  await page.goto("/");
  await ready(page);
  await expect(page.locator('#foot-t a[href="k/en/about.html"]')).toHaveCount(1);
  await expect(page.locator('#foot-t a[href="k/en/changes.html"]')).toHaveCount(1);
  await page.goto("/?lang=tr");
  await ready(page);
  await expect(page.locator('#foot-t a[href="k/about.html"]')).toHaveCount(1);
  await expect(page.locator('#foot-t a[href="k/changes.html"]')).toHaveCount(1);
});

test("the tab title names the view, in both languages", async ({ page }) => {
  await page.goto("/");
  await ready(page);
  await expect(page).toHaveTitle("Useful Sites");
  await page.goto("/?e=squoosh.app");
  await ready(page);
  await expect(page).toHaveTitle("Squoosh — Useful Sites");
  await page.goto("/?cat=web");
  await ready(page);
  const h1 = (await page.locator("#list h1").textContent()).trim();
  await expect(page).toHaveTitle(h1 + " — Useful Sites");
  await page.locator("#q").fill("regex");
  await expect(page).toHaveTitle("“regex” · " + h1 + " — Useful Sites");
  await page.goto("/?q=regex");
  await ready(page);
  await expect(page).toHaveTitle("“regex” — Useful Sites");
  await page.goto("/?saved=1");
  await ready(page);
  await expect(page).toHaveTitle("Saved — Useful Sites");
  await page.goto("/?new=1");
  await ready(page);
  await expect(page).toHaveTitle("Recently Added — Useful Sites");
  await page.goto("/?q=regex&lang=tr");
  await ready(page);
  await expect(page).toHaveTitle("“regex” — Kullanışlı Siteler");
});

for (const [bad, left] of [
  ["/?e=nope", ""],
  ["/?cat=zzz", ""],
  ["/?cat=diller&p=999", null],
  ["/?cmp=,,,a", ""],
  ["/?tag=%3Cscript%3E", ""],
  ["/?zz=1&cat=web", "?cat=web"],
  ["/?q=%E0%A4%A", null],
]) {
  test("a bad address shows a short notice and is cleaned: " + bad, async ({ page }) => {
    const errors = watchErrors(page);
    await page.goto(bad);
    await ready(page);
    const note = page.locator("#list .urlnote");
    await expect(note).toBeVisible();
    await expect(note).toHaveAttribute("role", "status");
    if (left !== null) expect(new URL(page.url()).search).toBe(left);
    else expect(new URL(page.url()).search).not.toBe(new URL("http://x" + bad).search);
    expect(await page.locator("#q").inputValue()).not.toContain("�");
    expect(errors).toEqual([]);
  });
}

test("a good address shows no notice and is left alone; tracking keys are dropped quietly", async ({ page }) => {
  await page.goto("/?cat=web");
  await ready(page);
  await expect(page.locator(".urlnote")).toHaveCount(0);
  expect(new URL(page.url()).search).toBe("?cat=web");
  await page.goto("/?cat=web&utm_source=x");
  await ready(page);
  await expect(page.locator(".urlnote")).toHaveCount(0);
  await expect(page).toHaveURL(/\?cat=web$/);
});

test("keyboard: Tab from search reaches 'Skip to results', which lands on the first result", async ({ page, isMobile }) => {
  test.skip(isMobile, "no hardware keyboard on the phone profile");
  await page.goto("/?q=regex");
  await ready(page);
  await page.locator("#q").focus();
  const ring = await page.locator("#q").evaluate(el => getComputedStyle(el).outlineStyle);
  expect(ring).toBe("solid");
  await page.keyboard.press("Tab");
  await expect(page.locator("#skipr")).toBeFocused();
  await expect(page.locator("#skipr")).toBeVisible();
  await page.keyboard.press("Enter");
  await expect(page.locator("#list .rec a.name").first()).toBeFocused();
  /* zero-count index entries are clickable but out of the Tab order */
  const empties = page.locator(".side a.empty");
  for (let i = 0; i < await empties.count(); i++) await expect(empties.nth(i)).toHaveAttribute("tabindex", "-1");
});

test("keyboard: the 'similar' links are one Tab stop, walked with the arrow keys", async ({ page, isMobile }) => {
  test.skip(isMobile, "no hardware keyboard on the phone profile");
  await page.goto("/?cat=diller");
  await ready(page);
  const rel = page.locator(".rel").filter({ has: page.locator("a:nth-of-type(2)") }).first();
  const a = rel.locator("a");
  await expect(a.nth(0)).not.toHaveAttribute("tabindex", "-1");
  await expect(a.nth(1)).toHaveAttribute("tabindex", "-1");
  await a.nth(0).focus();
  await page.keyboard.press("ArrowRight");
  await expect(a.nth(1)).toBeFocused();
  await expect(a.nth(1)).toHaveAttribute("tabindex", "0");
  await expect(a.nth(0)).toHaveAttribute("tabindex", "-1");
  await page.keyboard.press("ArrowLeft");
  await expect(a.nth(0)).toBeFocused();
});

test("phone: small links are at least 24px tall to the touch", async ({ page, isMobile }) => {
  test.skip(!isMobile, "touch targets are a phone concern");
  for (const [url, sel] of [["/", ".fc a, .hpicks a, .hlinks a, .tryq .chip, footer a"],
                            ["/?q=regex", ".rec .arch, .rec .path a, .rec .rel a, .rec .cmpb, .rec .save, .crumb a"]]) {
    await page.goto(url);
    await ready(page);
    const small = await page.locator(sel).evaluateAll(els => els
      .map(e => [e.textContent.trim().slice(0, 20), e.getBoundingClientRect().height])
      .filter(([, h]) => h > 0 && h < 24));
    expect(small, url).toEqual([]);
    /* Bigger boxes must not steal the tap from a neighbour: the middle of every
       link has to hit that link. (12 px of padding on stacked category links
       covered the next link's middle: tapping one opened another.) */
    const stolen = await page.locator(sel).evaluateAll(els => els.slice(0, 80).flatMap(e => {
      e.scrollIntoView({ block: "center" });
      const r = e.getBoundingClientRect();
      if (!r.width || !r.height) return [];
      const t = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
      return t && (t === e || e.contains(t)) ? [] : [e.textContent.trim().slice(0, 20) + " -> " + (t ? t.textContent.trim().slice(0, 20) : "nothing")];
    }));
    expect(stolen, url + " (taps stolen by a neighbour)").toEqual([]);
  }
});

test("print: tools are hidden and record links print their address", async ({ page }) => {
  await page.goto("/?e=squoosh.app");
  await ready(page);
  await page.emulateMedia({ media: "print" });
  for (const sel of ["#q", ".visit", "#foot-kb", ".rec .save"]) await expect(page.locator(sel).first(), sel).toBeHidden();
  const after = await page.locator(".rec a.name").first().evaluate(el => getComputedStyle(el, "::after").content);
  expect(after).toMatch(/attr\(href\)|squoosh\.app/);
  const bg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
  expect(bg).toBe("rgb(255, 255, 255)");
});

test("404.html: both languages, a search form to ?q=, absolute links, no script", async ({ request }) => {
  const html = await (await request.get("/404.html")).text();
  expect(html).toContain("Page not found");
  expect(html).toContain("Sayfa bulunamadı");
  expect(html).not.toMatch(/<script/i);
  expect(html).toMatch(/<form[^>]+action="\/useful-sites\/"[^>]*method="get"/);
  expect(html).toContain('name="q"');
  expect(html).not.toContain('/useful-sites/k/en/index.html');   // that page only forwards to /
  expect(html).toContain('href="/useful-sites/k/index.html"');
  expect(html).toContain('href="/useful-sites/style.css"');
  expect(html).toContain("form-action 'self'");
});

test("the three scripts download in parallel and still run in order", async ({ request }) => {
  const html = await (await request.get("/index.html")).text();
  for (const n of ["links.js", "search.js", "app.js"]) {
    expect(html).toMatch(new RegExp('<link rel="preload" href="' + n.replace(".", "\\.") + '\\?v=[0-9a-f]+" as="script">'));
    expect(html).toMatch(new RegExp('<script src="' + n.replace(".", "\\.") + '\\?v=[0-9a-f]+" defer></script>'));
  }
  expect(html.indexOf('src="links.js')).toBeLessThan(html.indexOf('src="search.js'));
  expect(html.indexOf('src="search.js')).toBeLessThan(html.indexOf('src="app.js'));
});

test("the layout warm-up leaves nothing behind", async ({ page }) => {
  const errors = watchErrors(page);
  await page.goto("/");
  await ready(page);
  await page.locator("#q").focus();
  await expect(page.locator("#sort")).toHaveCount(0);
  await expect(page.locator("#filtb")).toHaveCount(0);
  await page.keyboard.type("r");
  await expect(page.locator("#sort")).toHaveCount(1);
  expect(errors).toEqual([]);
});
