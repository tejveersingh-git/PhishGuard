// PhishGuard - Content Script
// Injected into every page, notifies background worker when page loads

(function () {
  // Notify background service worker that a new page has loaded
  chrome.runtime.sendMessage(
    { type: "PAGE_LOADED", url: window.location.href },
    (response) => {
      if (chrome.runtime.lastError) {
        // Silently ignore — background may not be ready yet
      }
    }
  );
})();