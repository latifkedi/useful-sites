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
  await expect(page.locator("#langbtn")).toContainText("English");
  await expect(page.locator("#theme")).toContainText("Tema");
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
