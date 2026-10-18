// The comparison view: ?cmp=a,b (at most three) as a table of the
// directory's own fields, reached from the Compare toggle on records. On
// phones the row names stay put while the columns scroll and snap.
const { test, expect } = require("@playwright/test");
const { ready, overflow, watchErrors } = require("./helpers");

test("?cmp= draws a table with the curated 'differs in' axis", async ({ page }) => {
  const errors = watchErrors(page);
  await page.goto("/?cmp=squoosh.app,tinypng.com");
  await ready(page);
  await expect(page.locator("h1:visible")).toHaveText("Comparison");
  await expect(page.locator(".cmp thead th")).toHaveText([/Squoosh/, /TinyPNG/]);
  const rows = await page.locator(".cmp tbody th").allTextContents();
  expect(rows).toEqual(["What it does", "Price", "Source", "Last verified", "Repository", "Tags", "Differs in"]);
  await expect(page.locator(".cmp tbody tr").last()).toContainText("Where it runs, where the data lives");
  expect(await overflow(page)).toBeLessThanOrEqual(0);
  expect(errors).toEqual([]);
});

test("more than three, or unknown keys, are dropped", async ({ page }) => {
  await page.goto("/");
  await ready(page);
  const k = await page.evaluate(() => window.LINKS.slice(0, 5).map(d => d._k));
  await page.goto("/?cmp=" + ["nope.example"].concat(k).join(","));
  await ready(page);
  await expect(page.locator(".cmp thead th")).toHaveCount(3);
});

test("Compare on two records, then the tray, opens the comparison", async ({ page }) => {
  await page.goto("/?cat=diller");
  await ready(page);
  const recs = page.locator("#list .rec");
  const keys = [await recs.nth(0).getAttribute("data-k"), await recs.nth(1).getAttribute("data-k")];
  for (const i of [0, 1]) {
    await recs.nth(i).hover();
    await recs.nth(i).locator("[data-cmp]").click();
    await expect(recs.nth(i).locator("[data-cmp]")).toHaveAttribute("aria-pressed", "true");
  }
  await expect(page.locator("#tray")).toBeVisible();
  await page.locator("#tray [data-cmpgo]").click();
  await expect(page.locator(".cmp thead th")).toHaveCount(2);
  expect(new URL(page.url()).searchParams.get("cmp")).toBe(keys.join(","));
  await expect(page.locator("#tray")).toBeHidden();
  /* ✕ takes one out */
  await page.locator(".cmp [data-cmpoff]").first().click();
  await expect(page.locator(".cmp thead th")).toHaveCount(1);
});

test("phone: the first column is sticky and the columns snap", async ({ page, isMobile }) => {
  test.skip(!isMobile, "phone layout");
  await page.goto("/?cmp=squoosh.app,tinypng.com");
  await ready(page);
  const st = await page.evaluate(() => ({
    pos: getComputedStyle(document.querySelector(".cmp tbody th")).position,
    snap: getComputedStyle(document.querySelector(".cmpwrap")).scrollSnapType,
    scrolls: document.querySelector(".cmpwrap").scrollWidth > document.querySelector(".cmpwrap").clientWidth,
  }));
  expect(st.pos).toBe("sticky");
  expect(st.snap).toContain("x");
  expect(st.scrolls).toBe(true);
  expect(await overflow(page)).toBeLessThanOrEqual(0);
});

test("keys named like Object properties are unknown keys, not a crash", async ({ page }) => {
  const errors = watchErrors(page);
  for (const bad of ["constructor", "__proto__", "toString"]) {
    await page.goto("/?cmp=" + bad + "&list=" + bad);
    await ready(page);
    await expect(page.locator("#list")).toBeVisible();
  }
  expect(errors).toEqual([]);
});
