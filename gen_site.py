import json
m = json.load(open("model.json"))
classes, vocab, idf, coef, icpt = m["classes"], m["vocabulary"], m["idf"], m["coef"], m["intercept"]
mt = m["metrics"]
acc, base = mt["cv_accuracy"], mt["baseline_accuracy"]
DOMAIN = "tickettriage.vercel.app"
BADGE = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
JS_MODEL = f"""const CLASSES = {json.dumps(classes)};
const VOCAB = {json.dumps(vocab)};
const IDF = {json.dumps(idf)};
const COEF = {json.dumps(coef)};
const INTERCEPT = {json.dumps(icpt)};
function priorityProbs(text){{
  const toks = (text.toLowerCase().match(/[a-z0-9_]{{2,}}/g) || []);
  const counts = {{}};
  toks.forEach(t => {{ if (t in VOCAB) counts[t] = (counts[t] || 0) + 1; }});
  const vals = {{}}; let norm = 0;
  for (const t in counts) {{
    const v = (1 + Math.log(counts[t])) * IDF[VOCAB[t]];
    vals[t] = v; norm += v * v;
  }}
  norm = Math.sqrt(norm);
  const z = INTERCEPT.slice();
  if (norm > 0) for (const t in vals) {{
    const w = vals[t] / norm, idx = VOCAB[t];
    for (let c = 0; c < 4; c++) z[c] += w * COEF[c][idx];
  }}
  const mx = Math.max.apply(null, z);
  const ex = z.map(v => Math.exp(v - mx));
  const s = ex.reduce((a, b) => a + b, 0);
  return ex.map(v => v / s * 100);
}}"""
index = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TicketTriage — Support Ticket Priority Classifier | AI/ML Project</title>
<meta name="description" content="TicketTriage reads a customer support ticket and predicts its priority — critical, high, medium or low — using a TF-IDF + multinomial logistic regression model trained on 200 hand-written tickets. Try it live in your browser.">
<link rel="canonical" href="https://{DOMAIN}/">
<meta property="og:title" content="TicketTriage — Support Ticket Priority Classifier">
<meta property="og:description" content="Paste a support ticket and instantly see its priority, with a real trained ML model running in your browser.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://{DOMAIN}/">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="TicketTriage — Support Ticket Priority Classifier">
<meta name="twitter:description" content="TF-IDF + multinomial logistic regression ticket triage. Try the live demo in your browser.">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebApplication","name":"TicketTriage","applicationCategory":"EducationalApplication","description":"Support ticket priority classifier using TF-IDF and multinomial logistic regression.","url":"https://{DOMAIN}/"}}</script>
<style>
body{{font-family:Arial,Helvetica,sans-serif;color:#000;background:#fff;max-width:720px;margin:0 auto;padding:24px;line-height:1.5}}
h1{{font-size:2em}} label{{display:block;margin:12px 0 4px;font-weight:bold}}
textarea{{width:100%;padding:10px;font-size:16px;border:1px solid #000;border-radius:4px;box-sizing:border-box}}
button{{margin-top:16px;margin-right:8px;padding:12px 24px;font-size:17px;background:#000;color:#fff;border:none;border-radius:4px;cursor:pointer}}
#result{{margin-top:24px;padding:20px;border:2px solid #000;border-radius:8px;display:none}}
#result b{{font-size:2em}}
.bar{{height:14px;background:#000;margin:2px 0 8px}}
.note{{color:#333;font-size:.95em}} code{{background:#f2f2f2;padding:2px 5px}}
</style>
</head>
<body>
<h1>&#127987; TicketTriage — Support Ticket Priority Classifier</h1>
<p class="note">A 2nd-year B.Tech AI/ML project by Vikranth Reddy. A TF-IDF + multinomial logistic regression model trained on 200 hand-written support tickets (50 each of critical, high, medium and low priority; {mt['vocab']} words) predicts how urgent a ticket is. 5-fold CV: <b>accuracy = {acc:.1%}</b> vs a majority-class baseline of {base:.1%}.</p>
<label>Paste a support ticket</label>
<textarea id="ticket" rows="3">The entire website is down and no customer can log in at all</textarea>
<button onclick="predict()">Classify Priority</button>
<button onclick="tryLow()">Try a low one</button>
<div id="result"></div>
<p class="note">How it works: the ticket is split into words, each word gets a TF-IDF weight (common words count less, rare words count more), the weights are multiplied by the model&apos;s learned coefficients for each of the four priorities, and a softmax turns the four scores into percentages. The exact same weights run in this page and in the Python training script (<code>train.py</code>), so the browser result matches the trained model.</p>
<p class="note">Try it: &ldquo;The entire website is down and no customer can log in at all&rdquo; &rarr; critical, about 72.4%. &ldquo;Many users cannot log in since the morning update and get an error&rdquo; &rarr; high, about 57.7%. &ldquo;There is a small spelling mistake in the welcome message on the home page&rdquo; &rarr; low, about 51.3%. A plain sentence with no ticket words, like &ldquo;The quarterly sales report was shared with the team on Tuesday&rdquo;, scores low and flat across all four — the model honestly says it cannot tell.</p>
<p><a href="https://github.com/HVRGAMING2705/tickettriage">View source on GitHub</a></p>
<script>
{JS_MODEL}
const BADGE = {json.dumps(BADGE)};
function show(){{
  const p = priorityProbs(document.getElementById("ticket").value);
  let best = 0; for (let i = 1; i < 4; i++) if (p[i] > p[best]) best = i;
  const el = document.getElementById("result");
  el.style.display = "block";
  let html = "<b>" + BADGE[CLASSES[best]] + " " + CLASSES[best].toUpperCase() + " — " + p[best].toFixed(1) + "%</b><br>";
  if (p[best] < 30) html += "<span class=note>No strong priority signal — the ticket reads fairly neutral.</span><br>";
  for (let i = 0; i < 4; i++) {{
    html += CLASSES[i] + " " + p[i].toFixed(1) + "%<div class=bar style='width:" + p[i].toFixed(1) + "%'></div>";
  }}
  html += "<span class=note>This is a classroom demo trained on hand-written tickets, not a production support tool.</span>";
  el.innerHTML = html;
}}
function predict(){{ show(); }}
function tryLow(){{ document.getElementById("ticket").value = "There is a small spelling mistake in the welcome message on the home page"; show(); }}
</script>
</body>
</html>
"""
open("index.html", "w").write(index)
vercel = {
 "headers": [{"headers": [
   {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload"},
   {"key": "X-Content-Type-Options", "value": "nosniff"},
   {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
   {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
   {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"},
   {"key": "Cross-Origin-Opener-Policy", "value": "same-origin"},
   {"key": "Access-Control-Allow-Origin", "value": f"https://{DOMAIN}"},
   {"key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; base-uri 'self'; frame-ancestors 'self'"}],
  "source": "/(.*)"}]}
open("vercel.json", "w").write(json.dumps(vercel, indent=1))
open("404.html", "w").write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Page Not Found — TicketTriage</title><style>body{{font-family:Arial,sans-serif;color:#000;max-width:640px;margin:60px auto;padding:24px}}</style></head><body><h1>404 — Page not found</h1><p>This page does not exist on TicketTriage.</p><p><a href="https://{DOMAIN}/">Back to TicketTriage</a></p></body></html>""")
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
open("sitemap.xml", "w").write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://{DOMAIN}/</loc></url></urlset>
""")
open("README.md", "w").write(f"""# TicketTriage — Support Ticket Priority Classifier

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

TF-IDF (word unigrams, sublinear TF, L2) + multinomial logistic regression (C=1.0) trained on 200 hand-written support tickets (50 per priority: critical, high, medium, low; {mt['vocab']} vocabulary words, seed 42).

- 5-fold CV accuracy: {acc:.1%} (majority-class baseline: {base:.1%})
- Live demo: https://{DOMAIN} (runs fully in the browser — no backend)
- `train.py` trains the model and writes `model.json`; `index.html` applies the same weights in JavaScript.
""")
samples = json.load(open("parity_samples.json"))
parity = JS_MODEL + "\n" + "\n".join(
    f"console.log(JSON.stringify({{text: {json.dumps(s['text'])}, js: priorityProbs({json.dumps(s['text'])}), py: {json.dumps(s['probs'])}}}));"
    for s in samples)
open("parity.js", "w").write(parity)
print("site files written, acc", acc)
