'use strict';
document.documentElement.classList.add('js');

/* Header: shadow on scroll, mobile menu, active link */
const header = document.querySelector('.site-header');
const onScroll = () => {
  header.classList.toggle('scrolled', window.scrollY > 8);
  if (window.scrollY < 200) navLinks.forEach(l => { l.classList.remove('active'); l.removeAttribute('aria-current'); });
};

const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('#main-nav');
function setMenu(open) {
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  nav.classList.toggle('open', open);
}
menuButton.addEventListener('click', () => setMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
nav.addEventListener('click', e => { if (e.target.closest('a')) setMenu(false); });
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); menuButton.focus(); }
});
document.addEventListener('click', e => { if (!e.target.closest('.site-header')) setMenu(false); });
matchMedia('(min-width: 1081px)').addEventListener('change', e => { if (e.matches) setMenu(false); });

const navLinks = [...nav.querySelectorAll('a[href^="#"]')];
onScroll();
window.addEventListener('scroll', onScroll, { passive: true });
if ('IntersectionObserver' in window) {
  const spy = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      navLinks.forEach(link => {
        const active = link.hash === `#${entry.target.id}`;
        link.classList.toggle('active', active);
        if (active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
      });
    }
  }, { rootMargin: '-80px 0px -60% 0px' });
  navLinks.forEach(link => { const s = document.querySelector(link.hash); if (s) spy.observe(s); });
}

/* Gentle reveal for below-the-fold content */
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
if ('IntersectionObserver' in window && !reduced) {
  const targets = document.querySelectorAll('.section-head, .about-copy, .aff-grid li, .interest, .project-card, .role, .degree, .skills > div, .outreach-grid > *, .cert-list li, .awards, .contact-list');
  const io = new IntersectionObserver(entries => {
    entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('in'); io.unobserve(entry.target); } });
  }, { rootMargin: '0px 0px -40px 0px', threshold: 0.05 });
  targets.forEach(el => {
    if (el.getBoundingClientRect().top > window.innerHeight) { el.classList.add('reveal'); io.observe(el); }
  });
}

/* Publications: type, year, topic and text filters */
const list = document.querySelector('#publication-list');
const papers = [...list.querySelectorAll('.publication')];
const search = document.querySelector('#pub-search');
const yearSel = document.querySelector('#pub-year');
const topicSel = document.querySelector('#pub-topic');
const typeButtons = [...document.querySelectorAll('.segmented button')];
let pubType = 'all';
function filterPublications() {
  const q = search.value.toLowerCase().trim();
  let shown = 0;
  for (const p of papers) {
    const ok = (pubType === 'all' || p.dataset.type === pubType)
      && (yearSel.value === 'all' || p.dataset.year === yearSel.value)
      && (topicSel.value === 'all' || p.dataset.topic === topicSel.value)
      && (!q || p.textContent.toLowerCase().includes(q));
    p.hidden = !ok;
    if (ok) shown++;
  }
  document.querySelector('#pub-count').textContent = shown === papers.length
    ? `Showing all ${papers.length} publications`
    : `Showing ${shown} of ${papers.length} publications`;
  document.querySelector('#pub-empty').hidden = shown !== 0;
}
typeButtons.forEach(btn => btn.addEventListener('click', () => {
  pubType = btn.dataset.type;
  typeButtons.forEach(b => { const on = b === btn; b.classList.toggle('active', on); b.setAttribute('aria-pressed', String(on)); });
  filterPublications();
}));
search.addEventListener('input', filterPublications);
[yearSel, topicSel].forEach(s => s.addEventListener('change', filterPublications));
document.querySelector('#reset-filters').addEventListener('click', () => {
  search.value = ''; yearSel.value = 'all'; topicSel.value = 'all';
  typeButtons[0].click(); search.focus();
});

/* Project details dialog */
const projects = JSON.parse(document.querySelector('#project-data').textContent);
const dialog = document.querySelector('#project-dialog');
let opener = null;
const esc = v => String(v).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
function openProject(id, button) {
  const p = projects.find(x => x.id === id);
  if (!p) return;
  opener = button;
  const row = (label, text) => `<div><dt>${label}</dt><dd>${esc(text)}</dd></div>`;
  const img = p.image ? p.image.replace('-1440.', '-960.') : '';
  document.querySelector('#dialog-content').innerHTML =
    (img ? `<img class="dialog-art" src="${esc(img)}" alt="Illustrative rendering">` : '') +
    `<div class="dialog-body"><p class="kicker">${esc(p.category)}</p><h2 id="dialog-title">${esc(p.title)}</h2>` +
    `<dl class="project-facts">${row('Problem', p.problem)}${row('Approach', p.solution)}${row('My role', p.role)}` +
    `<div><dt>Technologies</dt><dd><ul class="tags">${p.technologies.map(t => `<li>${esc(t)}</li>`).join('')}</ul></dd></div>` +
    `${row('Status', p.status)}</dl>` +
    (p.link ? `<a class="text-link" href="${esc(p.link)}" target="_blank" rel="noopener noreferrer">${esc(p.linkLabel || 'Related link')} ↗</a>` : '') +
    `</div>`;
  dialog.showModal();
  document.body.style.overflow = 'hidden';
  dialog.scrollTop = 0;
  dialog.querySelector('.dialog-close').focus();
}
document.querySelectorAll('.project-open').forEach(b => b.addEventListener('click', () => openProject(b.dataset.project, b)));
dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', e => {
  if (e.target !== dialog) return;
  const r = dialog.getBoundingClientRect();
  if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close();
});
dialog.addEventListener('close', () => { document.body.style.overflow = ''; if (opener) opener.focus(); });

/* Copy email */
document.querySelector('#copy-email').addEventListener('click', async () => {
  const status = document.querySelector('#copy-status');
  const email = 'aqib.shafiq89@gmail.com';
  try { await navigator.clipboard.writeText(email); status.textContent = 'Email address copied.'; }
  catch { status.textContent = `Email: ${email}`; }
  setTimeout(() => { status.textContent = ''; }, 3000);
});

document.querySelector('#year').textContent = new Date().getFullYear();
