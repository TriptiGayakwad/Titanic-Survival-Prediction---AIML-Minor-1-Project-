// ── Titanic Survival Predictor – Frontend JS ──

document.addEventListener('DOMContentLoaded', () => {
  const form       = document.getElementById('predForm');
  const resultCard = document.getElementById('resultCard');
  const resultInner = document.getElementById('resultInner');
  const submitBtn  = document.getElementById('submitBtn');
  const btnText    = document.getElementById('btnText');
  const btnLoader  = document.getElementById('btnLoader');

  // Animate factor bars on load
  setTimeout(() => {
    document.querySelectorAll('.bar-fill').forEach(bar => {
      const w = bar.style.width;
      bar.style.width = '0';
      requestAnimationFrame(() => {
        setTimeout(() => { bar.style.width = w; }, 100);
      });
    });
  }, 400);

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Gather form data
    const data = {
      pclass:   document.querySelector('input[name="pclass"]:checked')?.value,
      sex:      document.querySelector('input[name="sex"]:checked')?.value,
      age:      document.getElementById('age').value,
      sibsp:    document.getElementById('sibsp').value,
      parch:    document.getElementById('parch').value,
      fare:     document.getElementById('fare').value,
      embarked: document.querySelector('input[name="embarked"]:checked')?.value
    };

    // Basic validation
    for (const [key, val] of Object.entries(data)) {
      if (!val && val !== '0') {
        showError(`Please fill in all fields (missing: ${key})`);
        return;
      }
    }
    if (+data.age <= 0 || +data.age > 120) {
      showError('Please enter a valid age (0.1 – 120)');
      return;
    }
    if (+data.fare < 0) {
      showError('Fare cannot be negative');
      return;
    }

    // Show loading state
    btnText.style.display   = 'none';
    btnLoader.style.display = 'inline-block';
    submitBtn.disabled      = true;
    resultCard.style.display = 'none';

    try {
      const response = await fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();

      if (result.error) {
        showError('Prediction error: ' + result.error);
        return;
      }

      displayResult(result, data);
    } catch (err) {
      showError('Connection error. Make sure the Flask server is running.');
    } finally {
      btnText.style.display   = 'inline';
      btnLoader.style.display = 'none';
      submitBtn.disabled      = false;
    }
  });

  function displayResult({ survived, probability }, formData) {
    const cls      = survived ? 'survived' : 'perished';
    const emoji    = survived ? '🟢' : '💀';
    const bigEmoji = survived ? '🛟' : '⚓';
    const heading  = survived ? 'YOU SURVIVED!' : 'YOU PERISHED';
    const subMsg   = survived
      ? `With a ${probability}% survival probability, you made it to a lifeboat.`
      : `With only a ${probability}% survival chance, the Atlantic claimed you.`;
    const contextMsg = buildContextMsg(formData, probability);

    resultCard.className = `card result-card result-${cls}`;
    resultInner.innerHTML = `
      <span class="result-emoji">${bigEmoji}</span>
      <h2 class="result-heading ${cls}">${heading}</h2>
      <p class="result-sub">${subMsg}</p>

      <div class="gauge-wrap">
        <span class="gauge-label">Survival Probability</span>
        <div class="gauge-bar">
          <div class="gauge-fill ${cls}" id="gaugeFill" style="width:0%"></div>
        </div>
        <span class="gauge-pct" style="color:${survived ? '#2ecc71' : '#e74c3c'}">${probability}%</span>
      </div>

      <p style="margin-top:1.2rem; font-size:0.9rem; color:rgba(212,217,232,0.7); font-style:italic;">${contextMsg}</p>
    `;

    resultCard.style.display = 'block';

    // Animate gauge
    setTimeout(() => {
      const fill = document.getElementById('gaugeFill');
      if (fill) fill.style.width = probability + '%';
    }, 100);

    resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function buildContextMsg(data, prob) {
    const pclassNames = { '1': '1st Class', '2': '2nd Class', '3': '3rd Class' };
    const portNames   = { S: 'Southampton', C: 'Cherbourg', Q: 'Queenstown' };
    const gender = data.sex === 'female' ? 'woman' : 'man';
    const port   = portNames[data.embarked] || data.embarked;
    const cls    = pclassNames[data.pclass] || data.pclass;
    const famSize = +data.sibsp + +data.parch + 1;
    const famDesc = famSize === 1 ? 'travelling alone' : `travelling with ${famSize - 1} family member(s)`;
    return `As a ${data.age}-year-old ${gender} in ${cls}, ${famDesc}, embarked at ${port} — your survival probability was ${prob}%.`;
  }

  function showError(msg) {
    resultCard.className = 'card result-card result-perished';
    resultInner.innerHTML = `
      <span class="result-emoji">⚠️</span>
      <h2 class="result-heading perished">Input Error</h2>
      <p class="result-sub">${msg}</p>
    `;
    resultCard.style.display = 'block';
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
});
