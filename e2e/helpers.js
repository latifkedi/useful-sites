// Shared helpers for the browser tests.

/* Console errors and uncaught exceptions; a test asserts the list stays empty. */
function watchErrors(page) {
  const errors = [];
  page.on("console", m => { if (m.type() === "error") errors.push(m.text()) });
  page.on("pageerror", e => errors.push(String(e)));
  return errors;
}

/* The app has drawn its view: #list holds something. */
async function ready(page) {
  await page.waitForFunction(() => {
    const l = document.querySelector("#list");
    return l && l.children.length > 0;
  });
}

/* Pixels the page can scroll sideways; 0 means it fits. */
function overflow(page) {
  return page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
}

module.exports = { watchErrors, ready, overflow };
