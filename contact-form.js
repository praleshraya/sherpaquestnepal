(() => {
  const form = document.querySelector('[data-enquiry-form]');
  if (!form) return;
  const business = form.querySelector('.business-field');
  const businessInput = business.querySelector('input');
  const status = form.querySelector('.form-status');
  const submit = form.querySelector('button[type="submit"]');
  const directEmail = form.querySelector('[data-direct-email]');

  function updateDirectEmail() {
    const values = Object.fromEntries(new FormData(form));
    const type = values['Enquiry type'] === 'Wholesaler' ? 'Wholesale' : 'Retail';
    const body = [
      `Enquiry type: ${type}`,
      values.name && `Name: ${values.name}`,
      values.email && `Reply email: ${values.email}`,
      values.phone && `Phone: ${values.phone}`,
      values['Business name'] && `Business: ${values['Business name']}`,
      values['Product or category'] && `Product or category: ${values['Product or category']}`,
      '',
      values.message || ''
    ].filter(value => value !== undefined && value !== false).join('\n');
    directEmail.href = `mailto:sherpaquestoffroad@gmail.com?subject=${encodeURIComponent(`${type} enquiry — Sherpa Quest Nepal`)}&body=${encodeURIComponent(body)}`;
  }

  function updateType() {
    const wholesale = form.querySelector('[name="Enquiry type"]:checked')?.value === 'Wholesaler';
    business.hidden = !wholesale;
    businessInput.required = wholesale;
    if (!wholesale) businessInput.value = '';
    updateDirectEmail();
  }
  form.querySelectorAll('[name="Enquiry type"]').forEach(input => input.addEventListener('change', updateType));
  form.addEventListener('input', updateDirectEmail);
  updateType();

  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    submit.disabled = true;
    status.textContent = 'Sending your enquiry…';
    const values = Object.fromEntries(new FormData(form));
    values._subject = `${values['Enquiry type']} enquiry — Sherpa Quest Nepal`;
    try {
      const response = await fetch('https://formsubmit.co/ajax/sherpaquestoffroad@gmail.com', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
        body: JSON.stringify(values)
      });
      const result = await response.json();
      if (!response.ok || (result.success !== true && result.success !== 'true')) throw new Error('Delivery failed');
      status.textContent = 'Thank you. Your enquiry has been submitted.';
      form.reset();
      updateType();
    } catch {
      status.innerHTML = 'We could not send your enquiry. Please email <a href="mailto:sherpaquestoffroad@gmail.com">sherpaquestoffroad@gmail.com</a>.';
    } finally {
      submit.disabled = false;
    }
  });
})();
