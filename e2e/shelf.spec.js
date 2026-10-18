// The local shelf: saving is per browser, one localStorage key of stable
// record keys, no account. The saved view, the "seen" state, the share link
// and its read-only shared list, and export of what is saved.
const { test, expect } = require("@playwright/test");
const { ready, watchErrors } = require("./helpers");

const shelf = page => page.evaluate(() => JSON.parse(localStorage.getItem("shelf") || "null"));

test("the pre-rendered home carries no save controls; app-drawn records do", async ({ page, request }) => {
  const src = await (await request.get("/index.html")).text();
  expect(src).not.toContain("data-save");
  await page.goto("/?cat=diller");
  await ready(page);
  await expect(page.locator("#list .rec").first().locator("[data-save]")).toHaveCount(1);
});

test("saving an entry stores its key, counts it in the header and lists it at ?saved=1", async ({ page, isMobile }) => {
  await page.goto("/?cat=diller");
  await ready(page);
  const first = page.locator("#list .rec").first();
  const key = await first.getAttribute("data-k");
  const name = (await first.locator("a.name").textContent()).trim();
  const save = first.locator("[data-save]");
  await save.click();
  await expect(save).toHaveAttribute("aria-pressed", "true");
  expect((await shelf(page)).s).toEqual([key]);
  await expect(page.locator("#savedb .c")).toHaveText("1");
  if (isMobile) await page.locator("#menub").click();
  await page.locator("#savedb").click();
  await expect(page).toHaveURL(/\?saved=1$/);
  await expect(page.locator("h1:visible")).toHaveText("Saved");
  await expect(page.locator("#list .rec a.name")).toHaveText([name]);
  /* removing it in the saved view drops it from the list */
  await page.locator("#list .rec [data-save]").click();
  await expect(page.locator("#list .rec")).toHaveCount(0);
  await expect(page.locator("#list .lede")).toContainText("Nothing saved yet");
  expect((await shelf(page)).s).toEqual([]);
});

test("following an entry's link marks it seen, and it stays dimmed after a reload", async ({ page }) => {
  await page.goto("/?cat=diller");
  await ready(page);
  /* keep the browser from leaving for the external site */
  await page.evaluate(() => addEventListener("click", e => e.preventDefault()));
  const first = page.locator("#list .rec").first();
  const key = await first.getAttribute("data-k");
  await first.locator("a.name").click();
  await expect(first).toHaveClass(/\bseen\b/);
  expect((await shelf(page)).v).toEqual([key]);
  await page.reload();
  await ready(page);
  await expect(page.locator("#list .rec").first()).toHaveClass(/\bseen\b/);
  await expect(page.locator("#list .rec").nth(1)).not.toHaveClass(/\bseen\b/);
});

test("a shared list is read-only until 'Save all'; unknown keys are dropped", async ({ page }) => {
  await page.goto("/");
  await ready(page);
  const keys = await page.evaluate(() => [window.LINKS[3]._k, window.LINKS[40]._k]);
  await page.goto("/?list=" + encodeURIComponent(keys.join(",") + ",not-a-record.example,<script>"));
  await ready(page);
  await expect(page.locator("h1:visible")).toHaveText("Shared List");
  await expect(page.locator("#list .rec")).toHaveCount(2);
  expect(await shelf(page)).toBeNull();
  await page.locator("[data-saveall]").click();
  expect((await shelf(page)).s.sort()).toEqual(keys.slice().sort());
  await expect(page.locator("#savedb .c")).toHaveText("2");
});

test("a shared list with no known entry, or one past the length cap, says so", async ({ page }) => {
  const errors = watchErrors(page);
  await page.goto("/?list=nothing-here,%22%3E%3Cimg%3E");
  await ready(page);
  await expect(page.locator("#list .lede")).toContainText("names no entry");
  await expect(page.locator("#list .rec")).toHaveCount(0);
  await page.goto("/?list=" + "a".repeat(7000));
  await ready(page);
  await expect(page.locator("#list .rec")).toHaveCount(0);
  expect(errors).toEqual([]);
});

test("the share link carries the saved keys and opens the same list", async ({ page, context }) => {
  await context.grantPermissions(["clipboard-read", "clipboard-write"]);
  await page.goto("/");
  await ready(page);
  const keys = await page.evaluate(() => [window.LINKS[5]._k, window.LINKS[9]._k]);
  await page.evaluate(k => localStorage.setItem("shelf", JSON.stringify({ s: k, v: [] })), keys);
  await page.goto("/?saved=1");
  await ready(page);
  await page.locator("[data-share]").click();
  const link = await page.evaluate(() => navigator.clipboard.readText());
  expect(new URL(link).searchParams.get("list")).toBe(keys.join(","));
  await page.goto(link);
  await ready(page);
  await expect(page.locator("#list .rec")).toHaveCount(2);
});

test("export from the saved view writes only what is saved", async ({ page }) => {
  await page.goto("/");
  await ready(page);
  const keys = await page.evaluate(() => [window.LINKS[1]._k, window.LINKS[50]._k, window.LINKS[700]._k]);
  await page.evaluate(k => localStorage.setItem("shelf", JSON.stringify({ s: k, v: [] })), keys);
  await page.goto("/?saved=1");
  await ready(page);
  const [dl] = await Promise.all([page.waitForEvent("download"), page.locator('[data-exp="json"]').click()]);
  expect(dl.suggestedFilename()).toBe("baglantilar-kayitli.json");
  const j = JSON.parse(require("fs").readFileSync(await dl.path(), "utf8"));
  expect(j.count).toBe(3);
});

test("a browser that refuses storage still draws the page and saves for the visit", async ({ page }) => {
  await page.addInitScript(() => {
    Storage.prototype.getItem = () => { throw new Error("denied") };
    Storage.prototype.setItem = () => { throw new Error("denied") };
  });
  const errors = watchErrors(page);
  await page.goto("/?cat=diller");
  await ready(page);
  await page.locator("#list .rec [data-save]").first().click();
  await expect(page.locator("#savedb .c")).toHaveText("1");
  expect(errors).toEqual([]);
});

test("broken JSON in the shelf key is treated as an empty shelf", async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem("shelf", "{nope"));
  const errors = watchErrors(page);
  await page.goto("/?saved=1");
  await ready(page);
  await expect(page.locator("#list .lede")).toContainText("Nothing saved yet");
  expect(errors).toEqual([]);
});
