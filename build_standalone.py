"""
Generate a completely standalone Titanic predictor HTML file.
No server needed — just double-click the output file in any browser!
"""
import json, textwrap

with open('model_js.json') as f:
    forest_json = f.read()

with open('static/css/style.css', encoding='utf-8') as f:
    css = f.read()

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Titanic Survival Predictor</title>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Lato:wght@300;400;700&display=swap" rel="stylesheet"/>
  <style>
{css}
  </style>
</head>
<body>

  <div class="ocean-bg" id="oceanBg"></div>

  <header class="site-header">
    <div class="header-inner">
      <div class="ship-icon">&#x1F6A2;</div>
      <h1>Titanic Survival Predictor</h1>
      <p class="subtitle">Would you have survived the night of April 14&#8211;15, 1912?</p>
    </div>
  </header>

  <main class="container">
    <div class="card form-card">
      <h2>Enter Passenger Details</h2>
      <form id="predForm" novalidate>

        <div class="form-row">
          <div class="field-group">
            <label>Passenger Class</label>
            <div class="radio-group">
              <label class="radio-btn"><input type="radio" name="pclass" value="1" required/> 1st Class</label>
              <label class="radio-btn"><input type="radio" name="pclass" value="2"/> 2nd Class</label>
              <label class="radio-btn"><input type="radio" name="pclass" value="3" checked/> 3rd Class</label>
            </div>
          </div>
          <div class="field-group">
            <label>Gender</label>
            <div class="radio-group">
              <label class="radio-btn"><input type="radio" name="sex" value="male" checked/> Male</label>
              <label class="radio-btn"><input type="radio" name="sex" value="female"/> Female</label>
            </div>
          </div>
        </div>

        <div class="form-row">
          <div class="field-group">
            <label for="age">Age (years)</label>
            <input type="number" id="age" min="0.1" max="100" step="0.5" placeholder="e.g. 28" value="28" required/>
          </div>
          <div class="field-group">
            <label for="fare">Ticket Fare (&pound;)</label>
            <input type="number" id="fare" min="0" max="600" step="0.5" placeholder="e.g. 32.20" value="32.20" required/>
          </div>
        </div>

        <div class="form-row">
          <div class="field-group">
            <label for="sibsp">Siblings / Spouse aboard</label>
            <input type="number" id="sibsp" min="0" max="10" value="0" required/>
          </div>
          <div class="field-group">
            <label for="parch">Parents / Children aboard</label>
            <input type="number" id="parch" min="0" max="10" value="0" required/>
          </div>
        </div>

        <div class="form-row">
          <div class="field-group full-width">
            <label>Port of Embarkation</label>
            <div class="radio-group">
              <label class="radio-btn"><input type="radio" name="embarked" value="S" checked/> Southampton (S)</label>
              <label class="radio-btn"><input type="radio" name="embarked" value="C"/> Cherbourg (C)</label>
              <label class="radio-btn"><input type="radio" name="embarked" value="Q"/> Queenstown (Q)</label>
            </div>
          </div>
        </div>

        <button type="submit" class="predict-btn" id="submitBtn">
          <span id="btnText">&#x1F50D; Predict My Fate</span>
          <span id="btnLoader" class="loader" style="display:none;"></span>
        </button>
      </form>
    </div>

    <div class="card result-card" id="resultCard" style="display:none;">
      <div id="resultInner"></div>
    </div>

    <div class="card info-card">
      <h2>Key Survival Factors</h2>
      <div class="factor-grid">
        <div class="factor">
          <div class="factor-icon">&#x1F469;</div>
          <div class="factor-label">Women &amp; Children First</div>
          <div class="factor-bar"><div class="bar-fill" style="width:0%" data-w="92%"></div></div>
        </div>
        <div class="factor">
          <div class="factor-icon">&#x1F3A9;</div>
          <div class="factor-label">1st Class Privilege</div>
          <div class="factor-bar"><div class="bar-fill" style="width:0%" data-w="78%"></div></div>
        </div>
        <div class="factor">
          <div class="factor-icon">&#x1F4B0;</div>
          <div class="factor-label">Higher Fare = Better Access</div>
          <div class="factor-bar"><div class="bar-fill" style="width:0%" data-w="65%"></div></div>
        </div>
        <div class="factor">
          <div class="factor-icon">&#x1F46A;</div>
          <div class="factor-label">Family Size Matters</div>
          <div class="factor-bar"><div class="bar-fill" style="width:0%" data-w="50%"></div></div>
        </div>
        <div class="factor">
          <div class="factor-icon">&#x2693;</div>
          <div class="factor-label">Port of Embarkation</div>
          <div class="factor-bar"><div class="bar-fill" style="width:0%" data-w="35%"></div></div>
        </div>
      </div>
    </div>

    <div class="card stats-card">
      <h2>Historical Statistics</h2>
      <div class="stats-grid">
        <div class="stat"><div class="stat-number">2,224</div><div class="stat-label">Total Aboard</div></div>
        <div class="stat"><div class="stat-number">710</div><div class="stat-label">Survived</div></div>
        <div class="stat"><div class="stat-number">1,514</div><div class="stat-label">Perished</div></div>
        <div class="stat"><div class="stat-number">31.9%</div><div class="stat-label">Survival Rate</div></div>
        <div class="stat survived"><div class="stat-number">97%</div><div class="stat-label">1st Class Women Survived</div></div>
        <div class="stat perished"><div class="stat-number">13%</div><div class="stat-label">3rd Class Men Survived</div></div>
      </div>
    </div>
  </main>

  <footer>
    <p>Built with scikit-learn (Random Forest) &amp; Vanilla JS &bull; Titanic Survival Predictor &bull; 5th Sem AI/ML Project</p>
  </footer>

  <script>
  // ── Embedded Random Forest model (200 trees, exported from scikit-learn) ──
  const FOREST = {forest_json};

  // ── Feature indices (must match train_model.py) ──
  // 0:Pclass 1:Sex 2:Age 3:SibSp 4:Parch 5:Fare 6:Embarked 7:FamilySize 8:IsAlone 9:FarePerPerson

  function traverseTree(node, features) {{
    if (node.leaf) return node.prob;
    return features[node.feat] <= node.thresh
      ? traverseTree(node.left,  features)
      : traverseTree(node.right, features);
  }}

  function predict(features) {{
    let sumProb = 0;
    for (const tree of FOREST) sumProb += traverseTree(tree, features);
    const prob = sumProb / FOREST.length;
    return {{ survived: prob >= 0.5 ? 1 : 0, probability: Math.round(prob * 1000) / 10 }};
  }}

  function buildFeatures(data) {{
    const pclass    = +data.pclass;
    const sex       = data.sex === 'female' ? 1 : 0;
    const age       = +data.age;
    const sibsp     = +data.sibsp;
    const parch     = +data.parch;
    const fare      = +data.fare;
    const embarked  = {{S:0, C:1, Q:2}}[data.embarked] ?? 0;
    const familySz  = sibsp + parch + 1;
    const isAlone   = familySz === 1 ? 1 : 0;
    const farePerPx = fare / familySz;
    return [pclass, sex, age, sibsp, parch, fare, embarked, familySz, isAlone, farePerPx];
  }}

  // ── UI Logic ──
  document.addEventListener('DOMContentLoaded', () => {{
    // Animate factor bars
    setTimeout(() => {{
      document.querySelectorAll('.bar-fill[data-w]').forEach(bar => {{
        bar.style.width = bar.dataset.w;
      }});
    }}, 400);

    const form        = document.getElementById('predForm');
    const resultCard  = document.getElementById('resultCard');
    const resultInner = document.getElementById('resultInner');
    const btnText     = document.getElementById('btnText');
    const btnLoader   = document.getElementById('btnLoader');
    const submitBtn   = document.getElementById('submitBtn');

    form.addEventListener('submit', (e) => {{
      e.preventDefault();

      const data = {{
        pclass:   document.querySelector('input[name="pclass"]:checked')?.value,
        sex:      document.querySelector('input[name="sex"]:checked')?.value,
        age:      document.getElementById('age').value,
        sibsp:    document.getElementById('sibsp').value,
        parch:    document.getElementById('parch').value,
        fare:     document.getElementById('fare').value,
        embarked: document.querySelector('input[name="embarked"]:checked')?.value,
      }};

      for (const [k, v] of Object.entries(data)) {{
        if (!v && v !== '0') {{ showError('Please fill in all fields (missing: ' + k + ')'); return; }}
      }}
      if (+data.age <= 0 || +data.age > 120) {{ showError('Please enter a valid age.'); return; }}
      if (+data.fare < 0) {{ showError('Fare cannot be negative.'); return; }}

      btnText.style.display   = 'none';
      btnLoader.style.display = 'inline-block';
      submitBtn.disabled      = true;

      // Small timeout so loader renders, then run prediction
      setTimeout(() => {{
        try {{
          const features = buildFeatures(data);
          const result   = predict(features);
          displayResult(result, data);
        }} catch(err) {{
          showError('Prediction error: ' + err.message);
        }} finally {{
          btnText.style.display   = 'inline';
          btnLoader.style.display = 'none';
          submitBtn.disabled      = false;
        }}
      }}, 60);
    }});

    function displayResult({{ survived, probability }}, data) {{
      const cls      = survived ? 'survived' : 'perished';
      const bigEmoji = survived ? '&#x1F6DF;' : '&#x2693;';
      const heading  = survived ? 'YOU SURVIVED!' : 'YOU PERISHED';
      const subMsg   = survived
        ? 'With a ' + probability + '% survival probability, you made it to a lifeboat.'
        : 'With only a ' + probability + '% survival chance, the Atlantic claimed you.';

      const pclassName = {{1:'1st Class',2:'2nd Class',3:'3rd Class'}}[+data.pclass];
      const portName   = {{S:'Southampton',C:'Cherbourg',Q:'Queenstown'}}[data.embarked];
      const gender     = data.sex === 'female' ? 'woman' : 'man';
      const famSz      = +data.sibsp + +data.parch + 1;
      const famDesc    = famSz === 1 ? 'travelling alone' : 'travelling with ' + (famSz-1) + ' family member(s)';
      const context    = 'As a ' + data.age + '-year-old ' + gender + ' in ' + pclassName + ', ' + famDesc + ', embarked at ' + portName + ' — your survival probability was ' + probability + '%.';

      resultCard.className = 'card result-card result-' + cls;
      resultInner.innerHTML = `
        <span class="result-emoji">${{bigEmoji}}</span>
        <h2 class="result-heading ${{cls}}">${{heading}}</h2>
        <p class="result-sub">${{subMsg}}</p>
        <div class="gauge-wrap">
          <span class="gauge-label">Survival Probability</span>
          <div class="gauge-bar">
            <div class="gauge-fill ${{cls}}" id="gaugeFill" style="width:0%"></div>
          </div>
          <span class="gauge-pct" style="color:${{survived?'#2ecc71':'#e74c3c'}}">${{probability}}%</span>
        </div>
        <p style="margin-top:1.2rem;font-size:0.9rem;color:rgba(212,217,232,0.7);font-style:italic;">${{context}}</p>
      `;
      resultCard.style.display = 'block';
      setTimeout(() => {{
        const fill = document.getElementById('gaugeFill');
        if (fill) fill.style.width = probability + '%';
      }}, 100);
      resultCard.scrollIntoView({{ behavior:'smooth', block:'start' }});
    }}

    function showError(msg) {{
      resultCard.className = 'card result-card result-perished';
      resultInner.innerHTML = '<span class="result-emoji">&#x26A0;&#xFE0F;</span><h2 class="result-heading perished">Input Error</h2><p class="result-sub">' + msg + '</p>';
      resultCard.style.display = 'block';
      resultCard.scrollIntoView({{ behavior:'smooth', block:'start' }});
    }}
  }});
  </script>
</body>
</html>"""

with open('titanic_predictor.html', 'w', encoding='utf-8') as f:
    f.write(HTML)

import os
size_kb = os.path.getsize('titanic_predictor.html') // 1024
print(f"Created titanic_predictor.html  ({size_kb} KB)")
print("Just double-click it to open in any browser!")
