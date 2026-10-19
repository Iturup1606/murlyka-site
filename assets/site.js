// Мурлыка: появление блоков при прокрутке и котик, который машет лапкой.
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Появление по очереди внутри одного раздела
  var items = [].slice.call(document.querySelectorAll('.reveal'));
  if (reduce || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        var group = el.closest('section, footer') || document.body;
        var shown = group.querySelectorAll('.reveal.is-in').length;
        el.style.transitionDelay = Math.min(shown, 6) * 110 + 'ms';
        el.classList.add('is-in');
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
  }

  // Котик: машет при загрузке, по нажатию машет, прыгает и говорит новую фразу
  var cat = document.getElementById('cat');
  var bubble = document.getElementById('bubble');
  if (!cat || !bubble) return;
  var phrases = ['Привет! Я Мурлыка', 'Давай учиться!', 'Который час?', 'Получилось!', 'Мяу!'];
  var i = 0;

  function replay(el, cls) {
    el.classList.remove(cls);
    void el.getBoundingClientRect();
    el.classList.add(cls);
  }
  cat.addEventListener('animationend', function (e) {
    if (e.animationName === 'wave') cat.classList.remove('is-waving');
    if (e.animationName === 'jump') cat.classList.remove('is-jumping');
  });
  bubble.addEventListener('animationend', function () { bubble.classList.remove('is-pop'); });

  cat.addEventListener('click', function () {
    i = (i + 1) % phrases.length;
    bubble.textContent = phrases[i];
    if (reduce) return;
    replay(bubble, 'is-pop');
    replay(cat, 'is-waving');
    replay(cat, 'is-jumping');
  });

  if (!reduce) setTimeout(function () { replay(cat, 'is-waving'); }, 900);
})();
