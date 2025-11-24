// age.js
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('age-form');
  const birthEl = document.getElementById('birthdate');
  const resultDiv = document.getElementById('age-result');
  const clearBtn = document.getElementById('age-clear');

  function calculateAgeParts(birthDate, now = new Date()) {
    if (birthDate > now) return null;
    // Start with year difference
    let years = now.getFullYear() - birthDate.getFullYear();
    let months = now.getMonth() - birthDate.getMonth();
    let days = now.getDate() - birthDate.getDate();

    if (days < 0) {
      // borrow days from previous month
      const prevMonth = new Date(now.getFullYear(), now.getMonth(), 0); // last day of previous month
      days += prevMonth.getDate();
      months -= 1;
    }
    if (months < 0) {
      months += 12;
      years -= 1;
    }
    return { years, months, days };
  }

  function nextBirthdayCountdown(birthDate, now = new Date()) {
    const thisYear = now.getFullYear();
    let next = new Date(thisYear, birthDate.getMonth(), birthDate.getDate());
    if (next <= now) next = new Date(thisYear + 1, birthDate.getMonth(), birthDate.getDate());
    const diff = next - now;
    // compute days/hours/minutes
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
    const minutes = Math.floor((diff / (1000 * 60)) % 60);
    return { days, hours, minutes, nextDate: next.toDateString() };
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const val = birthEl.value;
    if (!val) {
      showAlert(resultDiv, 'Please enter a birthdate', 'danger');
      return;
    }
    const b = new Date(val + 'T00:00:00');
    const now = new Date();
    const parts = calculateAgeParts(b, now);
    if (!parts) {
      showAlert(resultDiv, 'Birthdate is in the future. Please pick a valid date', 'danger');
      return;
    }
    const countdown = nextBirthdayCountdown(b, now);
    resultDiv.innerHTML = `
      <div class="result-card">
        <h5>Age: ${parts.years} years, ${parts.months} months, ${parts.days} days</h5>
        <p class="mb-1 small-muted">Next birthday in ${countdown.days} days, ${countdown.hours} hours, ${countdown.minutes} minutes (on ${countdown.nextDate}).</p>
      </div>
    `;
  });

  clearBtn.addEventListener('click', () => {
    birthEl.value = '';
    resultDiv.innerHTML = '';
  });
});
