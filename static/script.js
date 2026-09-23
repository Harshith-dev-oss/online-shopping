document.addEventListener('DOMContentLoaded', function () {
  const cartCount = document.querySelector('[data-cart-count]');
  if (!cartCount) return;

  const count = Number(cartCount.dataset.cartCount || 0);
  if (count > 0) {
    cartCount.textContent = count;
    cartCount.style.display = 'inline-flex';
  }
});
