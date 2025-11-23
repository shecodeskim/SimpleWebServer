// main.js - small helpers
function showAlert(container, message, type = 'danger') {
  container.innerHTML = `<div class="alert alert-${type} mt-2" role="alert">${message}</div>`;
  setTimeout(()=> container.querySelector('.alert')?.remove(), 4500);
}

function formatNumber(x) {
  return Number(x).toLocaleString(undefined, {maximumFractionDigits: 2});
}
