// Search in the page: the suggestion, the area/heading shortcuts, whole-word
// highlighting of short terms. The ranking itself is covered by the
// benchmark in test_search.js; these check what the reader sees.
const { test, expect } = require("@playwright/test");
const { ready } = require("./helpers");

test("a typo gets a suggestion once typing pauses; clicking it runs the query", async ({ page }) => {
  await page.goto("/?lang=tr");
  await ready(page);
  await page.locator("#q").fill("pyhton");
  const sug = page.locator("#qsug");
  await expect(sug).toHaveText("Bunu mu demek istedin: python?");
  await sug.locator("a").click();
  await expect(page.locator("#q")).toHaveValue("python");
  await expect(page.locator("#list h1")).toContainText("python");
});

test("an area name offers the area; following it clears the query", async ({ page }) => {
  await page.goto("/?q=g%C3%BCvenlik&lang=tr");
  await ready(page);
  const link = page.locator(".qhelp a[data-field]");
  await expect(link).toHaveText("Alan: IV Güvenlik →");
  await link.click();
  await expect(page).toHaveURL(/\?f=guvenlikalan&lang=tr$/);
  await expect(page.locator("#q")).toHaveValue("");
  await expect(page.locator("h1:visible")).toContainText("Güvenlik");
});

test("a heading name offers the heading; following it clears the query", async ({ page }) => {
  await page.goto("/?q=veritaban%C4%B1&lang=tr");
  await ready(page);
  const link = page.locator(".qhelp a[data-cat]");
  await expect(link).toHaveText("Başlık: Veritabanı →");
  await link.click();
  await expect(page).toHaveURL(/\?cat=veritabani&lang=tr$/);
  await expect(page.locator("#q")).toHaveValue("");
});

test("a short term is highlighted only as a whole word", async ({ page }) => {
  await page.goto("/?q=go");
  await ready(page);
  const marks = await page.locator("#list mark").allTextContents();
  expect(marks.length).toBeGreaterThan(0);
  expect(marks.every(m => m.toLowerCase() === "go")).toBe(true);
});

test("a query with no letters or digits finds nothing", async ({ page }) => {
  await page.goto("/?q=%3F%3F%3F&lang=tr");
  await ready(page);
  await expect(page.locator("#list h1")).toContainText("0 sonuç");
});

test("English: the suggestion speaks English", async ({ page }) => {
  await page.goto("/?q=pyhton&lang=en");
  await ready(page);
  await expect(page.locator("#qsug")).toHaveText("Did you mean: python?");
});
