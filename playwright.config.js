// Browser tests: npm run e2e (after npm ci and npx playwright install chromium).
//
// They run against the committed files, served as-is by Python's static
// server -- the same files GitHub Pages serves -- at desktop and phone size.
// What they guard is written down in e2e/README.md.
const { defineConfig } = require("@playwright/test");

const PORT = 8733;

module.exports = defineConfig({
  testDir: "e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  /* "github" turns a failure into an annotation on the run, readable without
     downloading the report. */
  reporter: process.env.CI ? [["github"], ["list"], ["html", { open: "never" }]] : "list",
  use: {
    baseURL: "http://127.0.0.1:" + PORT,
    trace: "retain-on-failure",
    /* The service worker installs right after load and fetches the page's
       files; left on, that work races the context closing at the end of
       unrelated tests ("browserContext.close: Test ended"). Only
       offline.spec.js, which is about it, turns it back on. */
    serviceWorkers: "block",
  },
  webServer: {
    command: "python -m http.server " + PORT + " --bind 127.0.0.1",
    url: "http://127.0.0.1:" + PORT + "/",
    reuseExistingServer: !process.env.CI,
  },
  projects: [
    { name: "desktop", use: { browserName: "chromium", viewport: { width: 1440, height: 900 } } },
    { name: "phone", use: { browserName: "chromium", viewport: { width: 375, height: 812 },
                            isMobile: true, hasTouch: true, deviceScaleFactor: 2 } },
  ],
});
