// PhishGuard - Background Service Worker
// Runs silently in the background, listens for tab changes

// ── Listen for tab updates ────────────────────────────────────
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.active) {
    // Update extension icon badge when page finishes loading
    chrome.action.setBadgeText({
      text: "NEW",
      tabId: tabId
    });
    chrome.action.setBadgeBackgroundColor({
      color: "#534AB7",
      tabId: tabId
    });
  }
});

// ── Clear badge when popup is opened ─────────────────────────
chrome.action.onClicked.addListener((tab) => {
  chrome.action.setBadgeText({
    text: "",
    tabId: tab.id
  });
});

// ── Listen for messages from content script ───────────────────
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "PAGE_LOADED") {
    chrome.action.setBadgeText({
      text: "!",
      tabId: sender.tab.id
    });
    chrome.action.setBadgeBackgroundColor({
      color: "#534AB7",
      tabId: sender.tab.id
    });
    sendResponse({ status: "ok" });
  }
  return true;
});