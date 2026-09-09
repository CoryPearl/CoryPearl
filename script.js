const root = document.documentElement;
const themeToggle = document.querySelector('#theme-toggle');

function syncThemeLabel() {
  const dark = root.classList.contains('dark');
  themeToggle.setAttribute('aria-label', `Switch to ${dark ? 'light' : 'dark'} mode`);
}

themeToggle.addEventListener('click', () => {
  const dark = !root.classList.contains('dark');
  root.classList.toggle('dark', dark);
  localStorage.setItem('cory-theme', dark ? 'dark' : 'light');
  syncThemeLabel();
});
syncThemeLabel();

const dialog = document.querySelector('#resume-dialog');
const openResume = document.querySelector('#resume-open');
const viewResume = document.querySelector('#resume-view');
const closeResume = document.querySelector('#resume-close');
let resumeTrigger;

function showResume(event) {
  resumeTrigger = event.currentTarget;
  dialog.showModal();
}

openResume.addEventListener('click', showResume);
viewResume.addEventListener('click', showResume);
closeResume.addEventListener('click', () => dialog.close());
dialog.addEventListener('click', (event) => {
  const rect = dialog.getBoundingClientRect();
  const inside = event.clientX >= rect.left && event.clientX <= rect.right && event.clientY >= rect.top && event.clientY <= rect.bottom;
  if (!inside) dialog.close();
});
dialog.addEventListener('close', () => {
  resumeTrigger?.focus();
  resumeTrigger = undefined;
});

const copyButtons = document.querySelectorAll('.copy-contact');
const copyToast = document.querySelector('#copy-toast');
let toastTimer;

function showCopyToast() {
  clearTimeout(toastTimer);
  copyToast.textContent = 'Copied to clipboard';
  copyToast.classList.add('visible');
  toastTimer = setTimeout(() => {
    copyToast.classList.remove('visible');
    copyToast.textContent = '';
  }, 1800);
}

async function copyText(value) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(value);
    return;
  }

  const input = document.createElement('textarea');
  input.value = value;
  input.setAttribute('readonly', '');
  input.style.position = 'fixed';
  input.style.opacity = '0';
  document.body.append(input);
  input.select();
  document.execCommand('copy');
  input.remove();
}

copyButtons.forEach((button) => {
  let resetTimer;
  const idleLabel = button.getAttribute('aria-label');
  button.addEventListener('click', async () => {
    try {
      await copyText(button.dataset.copy);
      clearTimeout(resetTimer);
      button.classList.add('copied');
      button.setAttribute('aria-label', 'Copied');
      showCopyToast();
      resetTimer = setTimeout(() => {
        button.classList.remove('copied');
        button.setAttribute('aria-label', idleLabel);
      }, 1800);
    } catch {
      button.setAttribute('aria-label', 'Could not copy');
    }
  });
});

function setupProjectCarousel(carousel) {
  const track = carousel.querySelector('.carousel-track');
  const slides = [...carousel.querySelectorAll('.media-slide')];
  const previous = carousel.querySelector('.carousel-prev');
  const next = carousel.querySelector('.carousel-next');
  const dotsContainer = carousel.querySelector('.carousel-dots');
  let currentSlide = 0;
  let autoplayTimer;
  let scrollFrame;

  carousel.classList.toggle('single-slide', slides.length < 2);
  dotsContainer.replaceChildren();

  const dots = slides.map((slide, index) => {
    const dot = document.createElement('button');
    dot.className = 'carousel-dot';
    dot.type = 'button';
    dot.setAttribute('aria-label', `Show image ${index + 1} of ${slides.length}`);
    dot.addEventListener('click', () => {
      showSlide(index);
      restartAutoplay();
    });
    dotsContainer.append(dot);
    return dot;
  });

  function updateDots() {
    dots.forEach((dot, index) => {
      const active = index === currentSlide;
      dot.classList.toggle('active', active);
      if (active) dot.setAttribute('aria-current', 'true');
      else dot.removeAttribute('aria-current');
    });
  }

  function showSlide(index) {
    currentSlide = (index + slides.length) % slides.length;
    track.scrollTo({ left: slides[currentSlide].offsetLeft, behavior: 'smooth' });
    updateDots();
  }

  function startAutoplay() {
    if (slides.length < 2 || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    clearInterval(autoplayTimer);
    autoplayTimer = setInterval(() => showSlide(currentSlide + 1), 10000);
  }

  function stopAutoplay() {
    clearInterval(autoplayTimer);
  }

  function restartAutoplay() {
    stopAutoplay();
    startAutoplay();
  }

  previous.addEventListener('click', () => {
    showSlide(currentSlide - 1);
    restartAutoplay();
  });

  next.addEventListener('click', () => {
    showSlide(currentSlide + 1);
    restartAutoplay();
  });

  track.addEventListener('scroll', () => {
    cancelAnimationFrame(scrollFrame);
    scrollFrame = requestAnimationFrame(() => {
      const visibleSlide = Math.round(track.scrollLeft / track.clientWidth);
      if (visibleSlide !== currentSlide && slides[visibleSlide]) {
        currentSlide = visibleSlide;
        updateDots();
      }
    });
  });

  carousel.addEventListener('mouseenter', stopAutoplay);
  carousel.addEventListener('mouseleave', startAutoplay);
  carousel.addEventListener('focusin', stopAutoplay);
  carousel.addEventListener('focusout', (event) => {
    if (!carousel.contains(event.relatedTarget)) startAutoplay();
  });

  updateDots();
  startAutoplay();
  carousel.stopCarousel = stopAutoplay;
}

document.querySelectorAll('.project-carousel').forEach(setupProjectCarousel);

const projectDialog = document.querySelector('#project-dialog');
const projectDialogClose = document.querySelector('#project-dialog-close');
const projectDialogMedia = projectDialog.querySelector('.project-dialog-media');
const projectDialogCopy = projectDialog.querySelector('.project-dialog-copy');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
let expandedCarousel;
let projectTrigger;

function openProjectDialog(card) {
  projectTrigger = card;
  const projectName = card.querySelector('.project-body h3').textContent;
  expandedCarousel = card.querySelector('.project-carousel').cloneNode(true);
  const expandedBody = card.querySelector('.project-body').cloneNode(true);
  expandedBody.querySelector('h3').id = 'project-dialog-title';

  projectDialogMedia.replaceChildren(expandedCarousel);
  projectDialogCopy.replaceChildren(expandedBody);
  projectDialog.setAttribute('aria-label', `${projectName} project details`);
  document.body.classList.add('dialog-open');
  projectDialog.showModal();
  setupProjectCarousel(expandedCarousel);
  projectDialogClose.focus();
}

function closeProjectDialog() {
  if (!projectDialog.open || projectDialog.classList.contains('closing')) return;
  projectDialog.classList.add('closing');
  expandedCarousel?.stopCarousel();

  window.setTimeout(() => {
    projectDialog.close();
    projectDialog.classList.remove('closing');
    document.body.classList.remove('dialog-open');
    projectDialogMedia.replaceChildren();
    projectDialogCopy.replaceChildren();
    expandedCarousel = undefined;
    projectTrigger?.focus();
    projectTrigger = undefined;
  }, reducedMotion.matches ? 0 : 220);
}

document.querySelectorAll('.project-card').forEach((card) => {
  const projectName = card.querySelector('.project-body h3').textContent;
  card.tabIndex = 0;
  card.setAttribute('aria-label', `Open ${projectName} project details`);

  card.addEventListener('click', (event) => {
    if (event.target.closest('a, button')) return;
    openProjectDialog(card);
  });

  card.addEventListener('keydown', (event) => {
    if (event.target !== card || !['Enter', ' '].includes(event.key)) return;
    event.preventDefault();
    openProjectDialog(card);
  });
});

projectDialogClose.addEventListener('click', closeProjectDialog);
projectDialog.addEventListener('click', (event) => {
  if (event.target === projectDialog) closeProjectDialog();
});
projectDialog.addEventListener('cancel', (event) => {
  event.preventDefault();
  closeProjectDialog();
});
