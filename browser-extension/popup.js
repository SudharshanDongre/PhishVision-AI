const API_URL = "https://phishvision-ai.onrender.com";

// Get current tab URL and display it
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  const url = tabs[0].url;
  document.getElementById("currentUrl").textContent = url;
  document.getElementById("scanBtn").dataset.url = url;
});

// Scan button click
document.getElementById("scanBtn").addEventListener("click", async () => {
  const url = document.getElementById("scanBtn").dataset.url;
  const model = document.getElementById("modelSelect").value;

  if (!url) return;

  // Show loading
  document.getElementById("loading").style.display = "block";
  document.getElementById("resultBox").style.display = "none";
  document.getElementById("scanBtn").disabled = true;

  // ── FIX 1: Show warmup message if API takes > 4 seconds (Render free tier) ──
  const resultBox = document.getElementById("resultBox");
  const resultTitle = document.getElementById("resultTitle");
  const resultMsg = document.getElementById("resultMsg");
  const confBar = document.getElementById("confBar");
  const confLabel = document.getElementById("confLabel");

  let isWarmedUp = false;
  const warmupTimer = setTimeout(() => {
    if (!isWarmedUp) {
      resultBox.style.display = "block";
      resultBox.className = "result-box result-safe";
      resultTitle.className = "result-title safe-text";
      resultTitle.textContent = "⏳ Warming Up Server...";
      resultMsg.textContent = "The server was asleep. Waking it up — this takes up to 30 seconds. Please wait...";
      confBar.style.width = "0%";
      confLabel.textContent = "Starting up PhishVision API...";
    }
  }, 4000);

  try {
    // ── FIX 2: Correct endpoint URL (was missing /predict) ──
    const response = await fetch(`${API_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url, model: model })
    });

    // Server responded — cancel warmup message
    isWarmedUp = true;
    clearTimeout(warmupTimer);

    const data = await response.json();

    // Hide loading
    document.getElementById("loading").style.display = "none";
    document.getElementById("scanBtn").disabled = false;

    resultBox.style.display = "block";

    if (data.is_phishing) {
      resultBox.className = "result-box result-phishing";
      resultTitle.className = "result-title phishing-text";
      resultTitle.textContent = "⚠️ PHISHING DETECTED";
      resultMsg.textContent = "This URL matches known malicious patterns. Do not enter any credentials.";
      confBar.style.background = "#dc3545";
    } else {
      resultBox.className = "result-box result-safe";
      resultTitle.className = "result-title safe-text";
      resultTitle.textContent = "✅ SAFE — LEGITIMATE";
      resultMsg.textContent = "This URL appears to be safe based on ML analysis.";
      confBar.style.background = "#28a745";
    }

    confBar.style.width = data.confidence + "%";
    confLabel.textContent = `Confidence: ${data.confidence}%  |  Model: ${data.model_used.toUpperCase()}`;

  } catch (err) {
    isWarmedUp = true;
    clearTimeout(warmupTimer);

    document.getElementById("loading").style.display = "none";
    document.getElementById("scanBtn").disabled = false;

    resultBox.style.display = "block";
    resultBox.className = "result-box result-phishing";
    resultTitle.textContent = "❌ Connection Error";
    resultMsg.textContent = "Could not reach the PhishVision API. Please try again in 30 seconds.";
  }
});