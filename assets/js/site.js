(function () {
  var toggle = document.querySelector('[data-nav-toggle]');
  var nav = document.querySelector('[data-site-nav]');

  if (!toggle || !nav) return;

  document.documentElement.classList.add('js');

  toggle.addEventListener('click', function () {
    var expanded = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!expanded));
    nav.toggleAttribute('data-open', !expanded);
  });

  nav.addEventListener('click', function (event) {
    if (event.target && event.target.matches('a')) {
      toggle.setAttribute('aria-expanded', 'false');
      nav.removeAttribute('data-open');
    }
  });

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      toggle.focus();
      toggle.setAttribute('aria-expanded', 'false');
      nav.removeAttribute('data-open');
    }
  });
})();
