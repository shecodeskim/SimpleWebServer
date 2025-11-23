// loan.js
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('loan-form');
  const principalEl = document.getElementById('principal');
  const rateEl = document.getElementById('rate');
  const tenureEl = document.getElementById('tenure');
  const resultDiv = document.getElementById('loan-result');
  const clearBtn = document.getElementById('loan-clear');

  // EMI formula: E = P * r * (1+r)^n / ((1+r)^n - 1)
  // where r = monthly rate (decimal), n = total months
  function calcEMI(P, annualRatePercent, years) {
    const monthlyRate = (annualRatePercent / 100) / 12;
    const n = Math.round(years * 12);
    if (monthlyRate === 0) {
      return { emi: P / n, total: P, interest: 0, n };
    }
    const r = monthlyRate;
    const factor = Math.pow(1 + r, n);
    const emi = P * r * factor / (factor - 1);
    const total = emi * n;
    const interest = total - P;
    return { emi, total, interest, n };
  }

  function calcSimpleInterest(P, annualRatePercent, years) {
    const interest = (P * (annualRatePercent / 100) * years);
    const total = P + interest;
    return { interest, total };
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const P = parseFloat(principalEl.value);
    const r = parseFloat(rateEl.value);
    const years = parseFloat(tenureEl.value);
    if (!P || P <= 0 || r < 0 || !years || years <= 0) {
      showAlert(resultDiv, 'Enter valid principal, rate and tenure', 'danger');
      return;
    }

    const emiRes = calcEMI(P, r, years);
    const si = calcSimpleInterest(P, r, years);

    resultDiv.innerHTML = `
      <div class="result-card">
        <h5>EMI: ${formatNumber(emiRes.emi)} / month</h5>
        <p class="mb-1">Tenure: ${emiRes.n} months</p>
        <p class="mb-1">Total payable (EMI): <strong>${formatNumber(emiRes.total)}</strong> (Interest: ${formatNumber(emiRes.interest)})</p>
        <hr>
        <h6>Simple Interest (for comparison)</h6>
        <p class="mb-1">Total interest: ${formatNumber(si.interest)}</p>
        <p class="mb-1">Total payable (Simple Interest): ${formatNumber(si.total)}</p>
      </div>
    `;
  });

  clearBtn.addEventListener('click', () => {
    principalEl.value = '';
    rateEl.value = '';
    tenureEl.value = '';
    resultDiv.innerHTML = '';
  });
});
