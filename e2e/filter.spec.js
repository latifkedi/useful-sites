// The Süz panel: a non-modal panel under its button on desktop, a modal
// bottom sheet on phones. Choosing a facet filters the list and the URL;
// closing gives focus back to the Süz button.
const { test, expect } = require("@playwright/test");
const { ready } = require("./helpers");

async function openFilter(page) {
  await page.goto("/?cat=diller&lang=tr");
  await ready(page);
  await page.locator("#filtb").click();
  const filt = page.locator("#filt");
  await expect(filt).toBeVisible();
  return filt;
}

test("Süz is a panel on desktop and a bottom sheet on phones", async ({ page, isMobile }) => {
  const filt = await openFilter(page);
  expect(await filt.evaluate(d => d.matches(":modal"))).toBe(!!isMobile);
  await expect(filt.locator(":focus")).toHaveCount(1);
});

/* The sheet's "N sonucu göster" footer exists only on phones; on desktop
   the list updates live and ✕ closes the panel. */
test("a facet filters the list and the URL; closing gives focus back to Süz", async ({ page, isMobile }) => {
  const filt = await openFilter(page);
  const chip = filt.locator("#f-body .chip", { hasText: "Açık Kaynak" });
  await chip.click();
  await expect.poll(() => decodeURIComponent(page.url())).toContain("tag=açık-kaynak");
  const shown = Number((await chip.textContent()).match(/\d+/)[0]);
  if (isMobile) {
    await expect(page.locator("#f-go")).toContainText(String(shown));
    await page.locator("#f-go").click();
  } else {
    await expect(page.locator("#f-go")).toBeHidden();
    await page.locator("#f-close").click();
  }
  await expect(filt).toBeHidden();
  await expect(page.locator("#filtb")).toBeFocused();
  await expect(page.locator("#list .tb")).toContainText(shown + " / ");
});

/* iOS Safari does not focus a tapped button, so the browser has nothing to
   give focus back to; app.js moves it to Süz itself. Chromium focuses on
   click, which would hide the difference -- hence opening without focus. */
test("focus goes back to Süz even when the button never took focus", async ({ page }) => {
  await page.goto("/?cat=diller&lang=tr");
  await ready(page);
  await page.evaluate(() => { document.activeElement.blur(); document.querySelector("#filtb").click() });
  await expect(page.locator("#filt")).toBeVisible();
  await page.locator("#f-close").click();
  await expect(page.locator("#filt")).toBeHidden();
  await expect(page.locator("#filtb")).toBeFocused();
});

/* "Ücretsiz" sat on three records in four: as a chip it read like a choice. It
   is a "hide paid & freemium" switch now, and old ?tag=ücretsiz links land on it. */
test("hide paid & freemium replaces the Free chip, and old ?tag=ücretsiz links map to it", async ({ page }) => {
  await page.goto("/?cat=diller&tag=%C3%BCcretsiz");
  await ready(page);
  const total = await page.evaluate(() => window.LINKS.filter(d => d.cat === "diller").length);
  const free = await page.evaluate(() => window.LINKS.filter(d => d.cat === "diller" && d.tags.includes("ücretsiz")).length);
  await expect(page.locator("#list .tb .cw")).toHaveText(free + " / " + total + " links");
  await expect(page.locator("#list .tb .chip.on[data-free]")).toHaveCount(1);
  await page.locator("#filtb").click();
  await expect(page.locator("#f-body [data-free]")).toHaveAttribute("aria-pressed", "true");
  await expect(page.locator("#f-body [data-tag='ücretsiz']")).toHaveCount(0);
  await page.locator("#f-body [data-free]").click();
  await expect(page.locator("#list .tb .cw")).toHaveText(total + " / " + total + " links");
  expect(page.url()).not.toContain("free=1");
});

test("phone: a sticky bar with Filter (n), a live result count and removable chips", async ({ page, isMobile }) => {
  test.skip(!isMobile, "the sticky mini-bar is the phone layout");
  await page.goto("/?cat=diller&free=1");
  await ready(page);
  const tb = page.locator("#list .tb");
  expect(await tb.evaluate(el => getComputedStyle(el).position)).toBe("sticky");
  await expect(page.locator("#filtb")).toContainText("Filter (1)");
  await expect(tb.locator(".cn")).toBeVisible();
  await expect(tb.locator(".cn")).toHaveText(/^\d+ results$/);
  await page.mouse.wheel(0, 1500);
  await expect(tb).toBeInViewport();
  /* the sheet's button counts live as the choice changes */
  await page.locator("#filtb").click();
  const go = page.locator("#f-go");
  const before = await go.textContent();
  expect(before).toMatch(/^Show \d+ results$/);
  await page.locator("#f-body .chip[data-tag]").last().click();   /* facets sort by count: the last is the rarest */
  await expect(go).not.toHaveText(before);
  await go.click();
  await expect(page.locator("#filtb")).toContainText("Filter (2)");
  /* and a chip on the bar removes its filter */
  await page.goto("/?cat=diller&free=1");
  await ready(page);
  await tb.locator(".chip.on[data-free]").click();
  await expect(page.locator("#filtb")).not.toContainText("(");
});

test("Escape closes the panel and gives focus back to Süz", async ({ page }) => {
  const filt = await openFilter(page);
  await page.keyboard.press("Escape");
  await expect(filt).toBeHidden();
  await expect(page.locator("#filtb")).toBeFocused();
});
