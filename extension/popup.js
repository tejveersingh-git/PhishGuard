const API_URL = "http://localhost:5000/predict";

const urlBox      = document.getElementById("urlBox");
const resultCard  = document.getElementById("resultCard");
const resultIcon  = document.getElementById("resultIcon");
const resultLabel = document.getElementById("resultLabel");
const resultDesc  = document.getElementById("resultDesc");
const confWrap    = document.getElementById("confWrap");
const confLabel   = document.getElementById("confLabel");
const confBar     = document.getElementById("confBar");
const pillsWrap   = document.getElementById("pillsWrap");
const scanFill    = document.getElementById("scanFill");
const recheckBtn  = document.getElementById("recheckBtn");
const reportBtn   = document.getElementById("reportBtn");
const helpBtn     = document.getElementById("helpBtn");
const urlInput    = document.getElementById("urlInput");
const checkBtn    = document.getElementById("checkBtn");
const panelCurrent= document.getElementById("panelCurrent");
const panelManual = document.getElementById("panelManual");
const tabCurrent  = document.getElementById("tabCurrent");
const tabManual   = document.getElementById("tabManual");

let activeTab = "current";

function switchTab(tab) {
  activeTab = tab;
  if (tab === "current") {
    tabCurrent.classList.add("active");
    tabManual.classList.remove("active");
    panelCurrent.style.display = "block";
    panelManual.style.display  = "none";
    checkCurrentTab();
  } else {
    tabManual.classList.add("active");
    tabCurrent.classList.remove("active");
    panelManual.style.display  = "block";
    panelCurrent.style.display = "none";
    showIdle();
  }
}

function showIdle() {
  resultCard.className    = "result-card loading";
  resultIcon.textContent  = "🔍";
  resultLabel.textContent = "Enter a URL above";
  resultDesc.textContent  = "Paste any URL and click Check";
  confWrap.style.display  = "none";
  pillsWrap.innerHTML     = "";
  scanFill.classList.remove("animating");
  scanFill.style.width    = "0%";
}

function showScanning(url) {
  if (activeTab === "current") urlBox.textContent = url;
  resultCard.className    = "result-card loading";
  resultIcon.textContent  = "⏳";
  resultLabel.textContent = "Scanning...";
  resultDesc.textContent  = "Analysing URL with ML model";
  confWrap.style.display  = "none";
  pillsWrap.innerHTML     = `<span style="font-size:11px;color:#999;">
    <span class="dot"></span>Contacting PhishGuard API...
  </span>`;
  scanFill.classList.add("animating");
}

function showResult(data) {
  scanFill.classList.remove("animating");
  scanFill.style.width = "100%";
  setTimeout(() => { scanFill.style.width = "0%"; }, 600);

  const isSafe    = data.result === "legitimate";
  const isWarning = data.risk_level === "warning";

  if (isSafe) {
    resultCard.className    = "result-card safe";
    resultIcon.textContent  = "✅";
    resultLabel.textContent = "Safe Site";
    resultDesc.textContent  = "No phishing indicators detected";
  } else if (isWarning) {
    resultCard.className    = "result-card warning";
    resultIcon.textContent  = "⚠️";
    resultLabel.textContent = "Suspicious Site";
    resultDesc.textContent  = "Some phishing signals found — be careful";
  } else {
    resultCard.className    = "result-card phish";
    resultIcon.textContent  = "🚨";
    resultLabel.textContent = "Phishing Detected!";
    resultDesc.textContent  = `${data.flagged_features.length} phishing signals found`;
  }

  confWrap.style.display = "block";
  confLabel.textContent  = `Confidence: ${data.confidence}%`;
  confBar.style.width    = data.confidence + "%";

  pillsWrap.innerHTML = "";
  const goodFeatures = [
    "SSLfinal_State", "having_IP_Address", "Shortening_Service",
    "having_At_Symbol", "DNSRecord", "HTTPS_token"
  ];

  goodFeatures.forEach(key => {
    const val = data.features[key];
    if (val !== undefined) {
      const pill       = document.createElement("span");
      pill.className   = "pill " + (val === 1 ? "ok" : val === 0 ? "warn" : "bad");
      pill.textContent = formatFeatureName(key);
      pillsWrap.appendChild(pill);
    }
  });

  if (data.flagged_features && data.flagged_features.length > 0) {
    data.flagged_features.forEach(key => {
      if (!goodFeatures.includes(key)) {
        const pill       = document.createElement("span");
        pill.className   = "pill bad";
        pill.textContent = formatFeatureName(key);
        pillsWrap.appendChild(pill);
      }
    });
  }
}

function showError(message) {
  scanFill.classList.remove("animating");
  resultCard.className    = "result-card warning";
  resultIcon.textContent  = "⚠️";
  resultLabel.textContent = "Could not scan";
  resultDesc.textContent  = message;
  confWrap.style.display  = "none";
  pillsWrap.innerHTML     = "";
}

function formatFeatureName(key) {
  const names = {
    "SSLfinal_State":              "HTTPS",
    "having_IP_Address":           "No IP in URL",
    "Shortening_Service":          "No shortener",
    "having_At_Symbol":            "No @ symbol",
    "DNSRecord":                   "DNS valid",
    "HTTPS_token":                 "Clean domain",
    "URL_Length":                  "URL length",
    "Prefix_Suffix":               "No dash in domain",
    "having_Sub_Domain":           "Subdomains",
    "Domain_registeration_length": "Domain age",
    "age_of_domain":               "Domain age",
    "Google_Index":                "Google indexed",
    "Statistical_report":          "Clean TLD",
    "Iframe":                      "No iFrame",
    "on_mouseover":                "No mouseover",
    "RightClick":                  "Right-click OK",
    "popUpWidnow":                 "No popups",
  };
  return names[key] || key.replace(/_/g, " ");
}

async function callAPI(url) {
  showScanning(url);
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url })
    });
    if (!response.ok) throw new Error(`API status ${response.status}`);
    const data = await response.json();
    showResult(data);
  } catch (error) {
    if (error.message.includes("Failed to fetch") ||
        error.message.includes("ERR_CONNECTION_REFUSED")) {
      showError("API offline. Run: python app.py");
    } else {
      showError("Error: " + error.message);
    }
  }
}

async function checkCurrentTab() {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab || !tab.url) { showError("Could not read tab URL."); return; }
    const url = tab.url;
    if (!url.startsWith("http://") && !url.startsWith("https://")) {
      urlBox.textContent      = url;
      resultIcon.textContent  = "ℹ️";
      resultLabel.textContent = "Not applicable";
      resultDesc.textContent  = "Only checks http/https pages.";
      scanFill.classList.remove("animating");
      pillsWrap.innerHTML = "";
      return;
    }
    await callAPI(url);
  } catch (error) {
    showError("Error: " + error.message);
  }
}

async function checkManualURL() {
  let url = urlInput.value.trim();
  if (!url) { showError("Please enter a URL first."); return; }
  if (!url.startsWith("http://") && !url.startsWith("https://")) {
    url = "https://" + url;
    urlInput.value = url;
  }
  await callAPI(url);
}

// ── All event listeners here — no onclick in HTML ─────────────
tabCurrent.addEventListener("click", () => switchTab("current"));
tabManual.addEventListener("click",  () => switchTab("manual"));
checkBtn.addEventListener("click", checkManualURL);
urlInput.addEventListener("keydown", (e) => { if (e.key === "Enter") checkManualURL(); });
recheckBtn.addEventListener("click", () => {
  if (activeTab === "current") checkCurrentTab();
  else checkManualURL();
});
reportBtn.addEventListener("click", () => {
  chrome.tabs.create({ url: "https://www.phishtank.com/report_phishing.php" });
});
helpBtn.addEventListener("click", () => {
  chrome.tabs.create({ url: "https://www.phishtank.com" });
});

document.addEventListener("DOMContentLoaded", checkCurrentTab);