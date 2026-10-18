// Keyboard and discovery: the command palette (Ctrl/Cmd+K), the "?" help,
// j/k through the list, the random key opening a record page inside the app,
// and an empty search that points somewhere instead of stopping.
const { test, expect } = require("@playwright/test");
const { ready } = require("./helpers");

test("Ctrl+K opens the palette as a combobox; arrows move, Enter goes, focus comes back", async ({ page, isMobile }) => {
  test.skip(isMobile, "no hardware keyboard on the phone profile");
  await page.goto("/?cat=diller");
  await ready(page);
  await page.keyboard.press("j");
  const firstName = page.locator("#list .rec a.name").first();
  await expect(firstName).toBeFocused();
  await page.keyboard.press("j");
  await expect(page.locator("#list .rec a.name").nth(1)).toBeFocused();
  await page.keyboard.press("k");
  await expect(firstName).toBeFocused();

  await page.keyboard.press("Control+k");
  const pal = page.locator("#pal");
  const box = page.locator("#pal-q");
  await expect(pal).toBeVisible();
  await expect(box).toBeFocused();
  await expect(box).toHaveAttribute("role", "combobox");
  /* Escape closes and gives focus back to what had it */
  await page.keyboard.press("Escape");
  await expect(pal).toBeHidden();
  await expect(firstName).toBeFocused();

  await page.keyboard.press("Control+k");
  await page.keyboard.type("squoosh");
  await expect(page.locator("#pal-list [role=option]").first()).toContainText("Squoosh");
  await expect(page.locator("#pal-list mark").first()).toHaveText(/squoosh/i);
  await expect(box).toHaveAttribute("aria-activedescendant", "pal-o0");
  await page.keyboard.press("ArrowDown");
  await page.keyboard.press("ArrowUp");
  await expect(box).toHaveAttribute("aria-activedescendant", "pal-o0");
  await page.keyboard.press("Enter");
  await expect(pal).toBeHidden();
  await expect(page).toHaveURL(/\?e=squoosh\.app/);
  await expect(page.locator("h1:visible")).toHaveText("Squoosh");
});

test("the palette runs actions: theme, and a heading by name", async ({ page, isMobile }) => {
  test.skip(isMobile, "no hardware keyboard on the phone profile");
  await page.goto("/");
  await ready(page);
  await page.keyboard.press("Control+k");
  await expect(page.locator("#pal-list .pal-g").first()).toHaveText("Actions");
  await page.keyboard.type("theme");
  await page.keyboard.press("Enter");
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await page.keyboard.press("Control+k");
  await page.keyboard.type("databases");
  await page.locator("#pal-list [role=option]", { hasText: "Databases" }).first().click();
  await expect(page).toHaveURL(/\?cat=veritabani/);
});

test("? opens the keyboard help, Escape closes it", async ({ page, isMobile }) => {
  test.skip(isMobile, "no hardware keyboard on the phone profile");
  await page.goto("/");
  await ready(page);
  await page.keyboard.press("?");
  await expect(page.locator("#kbh")).toBeVisible();
  await expect(page.locator("#kbh dt kbd").first()).toHaveText("/");
  await page.keyboard.press("Escape");
  await expect(page.locator("#kbh")).toBeHidden();
});

test("r opens a random record inside the app; the site is a second step", async ({ page, isMobile }) => {
  test.skip(isMobile, "no hardware keyboard on the phone profile");
  await page.goto("/");
  await ready(page);
  const popups = [];
  page.on("popup", p => popups.push(p));
  await page.keyboard.press("r");
  await expect(page).toHaveURL(/\?e=/);
  await expect(page.locator("h1:visible")).toHaveCount(1);
  await expect(page.locator(".visit a.btn")).toHaveAttribute("target", "_blank");
  const first = page.url();
  await page.locator(".visit [data-rand]").click();
  await expect(page).not.toHaveURL(first);
  expect(popups).toEqual([]);
});

test("the Random menu item opens a record page on phones too", async ({ page, isMobile }) => {
  await page.goto("/");
  await ready(page);
  if (isMobile) await page.locator("#menub").click();
  await page.locator("#rand").click();
  await expect(page).toHaveURL(/\?e=/);
  await expect(page.locator(".visit a.btn")).toBeVisible();
});

test("an empty search offers the nearest heading, the other language and a pre-filled suggestion", async ({ page }) => {
  /* postgres has matches, but not under Web: the nearest heading clears the filter */
  await page.goto("/?cat=web&q=postgres");
  await ready(page);
  const near = page.locator(".none-x [data-near]");
  await expect(near).toContainText("Closest heading:");
  await near.click();
  await expect(page.locator("#list .rec").first()).toBeVisible();
  await expect(page.locator("#q")).toHaveValue("postgres");

  await page.goto("/?q=zzqqxx");
  await ready(page);
  await expect(page.locator("[data-olang]")).toHaveText("Search the Turkish descriptions too");
  await page.locator("[data-suggest]").click();
  await expect(page.locator("#sub")).toBeVisible();
  await expect(page.locator("#f-name")).toHaveValue("zzqqxx");
});

test("a manifest shortcut, ?go=search, lands in the search box", async ({ page, isMobile }) => {
  test.skip(isMobile, "focus on load is the desktop case");
  await page.goto("/?go=search");
  await ready(page);
  await expect(page.locator("#q")).toBeFocused();
  await expect(page).toHaveURL(/\/$/);
});
