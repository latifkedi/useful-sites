// Shared helpers for the browser tests.

/* Console errors and uncaught exceptions; a test asserts the list stays empty. */
function watchErrors(page) {
  const errors = [];
  page.on("console", m => { if (m.type() === "error") errors.push(m.text()) });
  page.on("pageerror", e => errors.push(String(e)));
  return errors;
}

/* The app has drawn its view. #list is never empty -- index.html ships the
   pre-rendered home in it -- so "has children" alone passed before app.js
   ran, on any view. The app always drops the pre-render's data-pre marker
   when it draws (the attribute on the home, the whole markup elsewhere). */
async function ready(page) {
  await page.waitForFunction(() => {
    const l = document.querySelector("#list");
    return l && l.children.length > 0 && !l.querySelector("[data-pre]");
  });
}

/* Pixels the page can scroll sideways; 0 means it fits. */
function overflow(page) {
  return page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
}

module.exports = { watchErrors, ready, overflow };
