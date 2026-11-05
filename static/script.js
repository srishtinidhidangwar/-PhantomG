const $ = (id) => document.getElementById(id);

function tone(el, cls) { el.className = "v " + cls; }

$("analyze").addEventListener("click", async () => {
  const text = $("email").value.trim();
  $("error").hidden = true;
  if (!text) { $("error").textContent = "Please paste some email text first."; $("error").hidden = false; return; }

  const btn = $("analyze");
  btn.disabled = true; btn.textContent = "Analyzing...";
  try {
    const res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Request failed");

    $("verdict").textContent = data.verdict;
    $("score").textContent = data.score + " / 100";
    $("confidence").textContent = data.confidence.toFixed(2);
    $("risk").textContent = data.risk_level;
    const bad = data.verdict === "PHISHING";
    tone($("verdict"), bad ? "bad" : "good");
    tone($("score"), bad ? "bad" : "good");
    tone($("confidence"), "");
    tone($("risk"), data.risk_level === "High" ? "bad" : data.risk_level === "Medium" ? "mid" : "good");

    const ul = $("indicators");
    ul.innerHTML = "";
    const items = data.indicators.length ? data.indicators : ["No suspicious indicators found"];
    items.forEach((t) => { const li = document.createElement("li"); li.textContent = t; ul.appendChild(li); });
    $("result").hidden = false;
  } catch (e) {
    $("error").textContent = e.message; $("error").hidden = false;
  } finally {
    btn.disabled = false; btn.textContent = "Analyze Email";
  }
});
