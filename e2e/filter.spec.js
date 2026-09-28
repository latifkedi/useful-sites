// The Süz panel: a non-modal panel under its button on desktop, a modal
// bottom sheet on phones. Choosing a facet filters the list and the URL;
// closing gives focus back to the Süz button.
const { test, expect } = require("@playwright/test");
const { ready } = require("./helpers");

async function openFilter(page) {
  await page.goto("/?cat=diller");
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

/* The sheet's "N bağlantıyı göster" footer exists only on phones; on desktop
   the list updates live and ✕ closes the panel. */
test("a facet filters the list and the URL; closing gives focus back to Süz", async ({ page, isMobile }) => {
  const filt = await openFilter(page);
  const chip = filt.locator("#f-body .chip", { hasText: "Ücretsiz" });
  await chip.click();
  await expect(page).toHaveURL(/tag=(%C3%BC|ü)cretsiz/);
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
  await page.goto("/?cat=diller");
  await ready(page);
  await page.evaluate(() => { document.activeElement.blur(); document.querySelector("#filtb").click() });
  await expect(page.locator("#filt")).toBeVisible();
  await page.locator("#f-close").click();
  await expect(page.locator("#filt")).toBeHidden();
  await expect(page.locator("#filtb")).toBeFocused();
});

test("Escape closes the panel and gives focus back to Süz", async ({ page }) => {
  const filt = await openFilter(page);
  await page.keyboard.press("Escape");
  await expect(filt).toBeHidden();
  await expect(page.locator("#filtb")).toBeFocused();
});
