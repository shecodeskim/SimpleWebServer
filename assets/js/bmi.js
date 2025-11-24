// bmi.js
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('bmi-form');
  const weightEl = document.getElementById('weight');
  const heightEl = document.getElementById('height');
  const heightUnit = document.getElementById('height-unit');
  const resultDiv = document.getElementById('bmi-result');
  const clearBtn = document.getElementById('bmi-clear');

  function calcBMI(weight, heightMeters) {
    return weight / (heightMeters * heightMeters);
  }

  function categoryForBMI(bmi) {
    if (bmi < 18.5) return 'Underweight';
    if (bmi < 25) return 'Normal weight';
    if (bmi < 30) return 'Overweight';
    return 'Obesity';
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const w = parseFloat(weightEl.value);
    let h = parseFloat(heightEl.value);
    if (!w || !h) {
      showAlert(resultDiv, 'Enter valid height and weight', 'danger');
      return;
    }
    if (heightUnit.value === 'cm') h = h / 100;
    const bmi = calcBMI(w, h);
    const cat = categoryForBMI(bmi);
    resultDiv.innerHTML = `
      <div class="result-card">
        <h5>BMI: ${formatNumber(bmi)}</h5>
        <p class="mb-1">Category: <strong>${cat}</strong></p>
        <small class="small-muted">BMI is a general indicator — interpret with care.</small>
      </div>
    `;
  });

  clearBtn.addEventListener('click', () => {
    weightEl.value = '';
    heightEl.value = '';
    resultDiv.innerHTML = '';
  });
});
