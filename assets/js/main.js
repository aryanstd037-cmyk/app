/* =========================================================
   Click Your Hospital — Home page interactions
   ========================================================= */
const icon = (name, cls = 'i') => `<svg class="${cls}"><use href="#i-${name}"/></svg>`;
const inr = (n) => '₹' + n.toLocaleString('en-IN');

/* ---------------- Data ---------------- */
const surgeries = [
  { name: 'Laser Piles Surgery', spec: 'Proctology', cat: 'General', ic: 'activity', tint: 't-orange', price: 24999, emi: 2083, time: '30 min', stay: 'Same-day discharge', laser: true, rating: 4.9 },
  { name: 'Cataract Surgery', spec: 'Ophthalmology', cat: 'Eye', ic: 'eye', tint: 't-blue', price: 14999, emi: 1250, time: '20 min', stay: 'Same-day discharge', laser: true, rating: 4.8 },
  { name: 'Hernia Repair', spec: 'General Surgery', cat: 'General', ic: 'scissors', tint: 't-green', price: 39999, emi: 3333, time: '45 min', stay: '1 day stay', laser: false, rating: 4.8 },
  { name: 'Kidney Stone Removal', spec: 'Urology', cat: 'Urology', ic: 'droplet', tint: 't-purple', price: 34999, emi: 2916, time: '60 min', stay: '1 day stay', laser: true, rating: 4.7 },
  { name: 'Gallbladder Stone', spec: 'Laparoscopic', cat: 'General', ic: 'heart-pulse', tint: 't-teal', price: 44999, emi: 3750, time: '60 min', stay: '1–2 day stay', laser: false, rating: 4.8 },
  { name: 'Knee Replacement', spec: 'Orthopaedics', cat: 'Ortho', ic: 'bone', tint: 't-amber', price: 149999, emi: 12499, time: '2 hrs', stay: '3–4 day stay', laser: false, rating: 4.7 },
  { name: 'LASIK Eye Surgery', spec: 'Ophthalmology', cat: 'Eye', ic: 'eye', tint: 't-pink', price: 29999, emi: 2499, time: '15 min', stay: 'Same-day discharge', laser: true, rating: 4.9 },
  { name: 'Hysterectomy', spec: 'Gynaecology', cat: 'Gynae', ic: 'baby', tint: 't-red', price: 59999, emi: 4999, time: '90 min', stay: '2–3 day stay', laser: false, rating: 4.7 },
  { name: 'Fistula Surgery', spec: 'Proctology', cat: 'General', ic: 'activity', tint: 't-orange', price: 27999, emi: 2333, time: '30 min', stay: 'Same-day discharge', laser: true, rating: 4.8 },
  { name: 'Circumcision', spec: 'Urology', cat: 'Urology', ic: 'scissors', tint: 't-blue', price: 19999, emi: 1666, time: '20 min', stay: 'Same-day discharge', laser: true, rating: 4.8 },
  { name: 'Normal / C-Section Delivery', spec: 'Obstetrics', cat: 'Gynae', ic: 'baby', tint: 't-pink', price: 34999, emi: 2916, time: '—', stay: '2–4 day stay', laser: false, rating: 4.8 },
  { name: 'ACL Reconstruction', spec: 'Orthopaedics', cat: 'Ortho', ic: 'bone', tint: 't-green', price: 89999, emi: 7499, time: '90 min', stay: '1–2 day stay', laser: false, rating: 4.7 }
];

const pathology = [
  { name: 'Complete Blood Count (CBC)', params: 28, tat: '12 hrs', price: 199, mrp: 450, ic: 'droplet', tint: 't-red', fasting: false },
  { name: 'Thyroid Profile (T3, T4, TSH)', params: 3, tat: '24 hrs', price: 349, mrp: 800, ic: 'activity', tint: 't-purple', fasting: false },
  { name: 'HbA1c (Diabetes)', params: 3, tat: '12 hrs', price: 299, mrp: 650, ic: 'flask', tint: 't-orange', fasting: false },
  { name: 'Lipid Profile', params: 9, tat: '24 hrs', price: 399, mrp: 900, ic: 'heart-pulse', tint: 't-pink', fasting: true },
  { name: 'Liver Function Test (LFT)', params: 12, tat: '24 hrs', price: 449, mrp: 1000, ic: 'flask', tint: 't-green', fasting: false },
  { name: 'Kidney Function Test (KFT)', params: 10, tat: '24 hrs', price: 449, mrp: 950, ic: 'flask', tint: 't-blue', fasting: false },
  { name: 'Vitamin D (25-OH)', params: 1, tat: '24 hrs', price: 699, mrp: 1600, ic: 'sparkles', tint: 't-amber', fasting: false },
  { name: 'Vitamin B12', params: 1, tat: '24 hrs', price: 549, mrp: 1200, ic: 'pill', tint: 't-teal', fasting: false },
  { name: 'Dengue NS1 Antigen', params: 1, tat: '6 hrs', price: 499, mrp: 900, ic: 'syringe', tint: 't-red', fasting: false }
];

const radiology = [
  { name: 'MRI Brain', params: 'Plain', tat: 'Same day', price: 3999, mrp: 7500, ic: 'brain', tint: 't-purple' },
  { name: 'CT Scan Chest (HRCT)', params: 'Plain', tat: 'Same day', price: 2499, mrp: 4500, ic: 'scan', tint: 't-blue' },
  { name: 'Ultrasound Whole Abdomen', params: 'USG', tat: '2 hrs', price: 799, mrp: 1500, ic: 'scan', tint: 't-teal' },
  { name: 'Digital X-Ray Chest (PA)', params: 'X-Ray', tat: '1 hr', price: 299, mrp: 600, ic: 'scan', tint: 't-orange' },
  { name: 'MRI Lumbar Spine', params: 'Plain', tat: 'Same day', price: 3999, mrp: 7000, ic: 'bone', tint: 't-green' },
  { name: '2D Echo', params: 'Cardiac', tat: '1 hr', price: 1499, mrp: 2800, ic: 'heart-pulse', tint: 't-pink' },
  { name: 'ECG', params: '12-lead', tat: '30 min', price: 199, mrp: 400, ic: 'activity', tint: 't-red' },
  { name: 'Mammography (Bilateral)', params: 'Digital', tat: 'Same day', price: 1799, mrp: 3200, ic: 'scan', tint: 't-amber' },
  { name: 'CT Scan Brain', params: 'Plain', tat: 'Same day', price: 1999, mrp: 3500, ic: 'brain', tint: 't-blue' }
];

const testimonials = [
  { name: 'Rakesh Srivastava', city: 'Lanka, Varanasi', proc: 'Laser Piles Surgery', tint: 't-orange', bg: '#f07a22', text: 'I was scared of surgery for 3 years. The Care Buddy explained everything, arranged cashless approval and even called me after a week. Walked home the same day!' },
  { name: 'Priya Kesarwani', city: 'Sigra, Varanasi', proc: 'Full Body Checkup', tint: 't-blue', bg: '#1b3270', text: 'Sample collected at 6:30 AM from home, report on WhatsApp by evening and a doctor explained it for free. Price was less than half of what I paid last year.' },
  { name: 'Anil Mishra', city: 'Mirzapur', proc: 'Cataract Surgery (Father)', tint: 't-green', bg: '#0d9488', text: 'They compared 4 hospitals for my father and found one with the best surgeon at a fixed price. Pick-up and drop were also arranged. Truly family jaisi care.' },
  { name: 'Sunita Devi', city: 'Ghazipur', proc: 'Gallbladder Surgery', tint: 't-purple', bg: '#6d4bd8', text: 'Ayushman card accepted, no running around for paperwork. Staff stayed in touch with my son throughout. Very grateful to the whole team.' },
  { name: 'Mohd. Arif', city: 'Jaunpur', proc: 'Kidney Stone Removal', tint: 't-pink', bg: '#d0347a', text: 'No-cost EMI made it possible to get treated immediately instead of waiting. Transparent bill — exactly what was promised, nothing extra.' }
];

const faqs = {
  general: [
    ['What is Click Your Hospital?', 'Click Your Hospital is a healthcare facilitation platform that helps you find, compare and book surgeries, lab tests, clinics, ayurveda centres, blood banks and ambulances — with a dedicated Care Buddy who supports you from search to recovery.'],
    ['Is the consultation really free?', 'Yes. Talking to our medical experts and getting a treatment opinion is completely free. You only pay for the actual treatment or test you choose to book.'],
    ['Which cities do you serve?', 'We currently serve Varanasi and nearby cities across Purvanchal including Prayagraj, Mirzapur, Jaunpur, Ghazipur, Azamgarh, Ballia and Chandauli, with more cities coming soon.'],
    ['How are hospitals and labs verified?', 'Our team physically visits every partner to check accreditation (NABH/NABL), doctor credentials, hygiene, equipment and patient feedback before listing them.']
  ],
  surgery: [
    ['Are surgery prices fixed?', 'Most of our surgery packages have fixed, all-inclusive pricing covering surgeon fee, OT charges, room, medicines and follow-up. Any variation due to medical condition is explained to you before admission.'],
    ['Will someone help me during admission?', 'Yes. Your Care Buddy coordinates admission, paperwork and insurance, and stays in touch with your family until discharge and recovery follow-up.'],
    ['Can I choose my hospital and surgeon?', 'Absolutely. We show you multiple options with prices, surgeon experience and reviews so you can choose what suits you best.']
  ],
  lab: [
    ['Is home sample collection free?', 'Yes, home sample collection is free on most tests and all health packages within our service areas.'],
    ['When will I get my reports?', 'Most pathology reports are delivered within 12–24 hours on WhatsApp, email and the app. Radiology reports are usually ready the same day.'],
    ['Do I need to fast before my test?', 'Some tests like Lipid Profile and Fasting Blood Sugar need 10–12 hours of fasting. We mention this clearly on each test and remind you before collection.']
  ],
  payment: [
    ['Do you support cashless insurance?', 'Yes, we work with 40+ insurers and TPAs including Star Health, HDFC ERGO, ICICI Lombard, Niva Bupa and Care Health, and also Ayushman Bharat at empanelled hospitals.'],
    ['Is No-Cost EMI available?', 'Yes. You can pay for surgeries in easy monthly instalments at 0% interest, subject to quick eligibility check.'],
    ['What payment modes are accepted?', 'UPI, debit/credit cards, net banking, EMI and cash at the hospital are all accepted.']
  ]
};

/* ---------------- Renderers ---------------- */
function renderSurgeries(filter = 'All') {
  const track = document.getElementById('surgeryTrack');
  const list = filter === 'All' ? surgeries : surgeries.filter((s) => s.cat === filter);
  track.innerHTML = list.map((s) => `
    <article class="surgery-card">
      <div class="top ${s.tint}">
        <span class="tag">${icon('star')} ${s.rating} · ${s.time}</span>
        ${icon(s.ic)}
        ${s.laser ? '<span class="laser">Advanced / Laser</span>' : ''}
      </div>
      <div class="body">
        <h4>${s.name}</h4>
        <div class="spec">${s.spec}</div>
        <ul class="feats">
          <li>${icon('check-circle')} ${s.stay}</li>
          <li>${icon('check-circle')} Free pick-up &amp; drop</li>
          <li>${icon('check-circle')} Insurance &amp; cashless</li>
        </ul>
        <div class="price-row">
          <div><small>Starting from</small><b>${inr(s.price)}</b><div class="emi">EMI ${inr(s.emi)}/mo</div></div>
          <a href="#callback" class="btn btn-primary btn-sm">Get Estimate</a>
        </div>
      </div>
    </article>`).join('');
  track.scrollLeft = 0;
}

function renderSurgeryTabs() {
  const cats = [['All', 'sparkles'], ['General', 'scissors'], ['Eye', 'eye'], ['Urology', 'droplet'], ['Ortho', 'bone'], ['Gynae', 'baby']];
  const wrap = document.getElementById('surgeryTabs');
  wrap.innerHTML = cats.map(([c, ic], i) => `<button class="tab ${i === 0 ? 'active' : ''}" data-cat="${c}">${icon(ic)} ${c === 'All' ? 'All Surgeries' : c}</button>`).join('');
  wrap.addEventListener('click', (e) => {
    const btn = e.target.closest('.tab');
    if (!btn) return;
    wrap.querySelectorAll('.tab').forEach((t) => t.classList.toggle('active', t === btn));
    renderSurgeries(btn.dataset.cat);
  });
}

function testCard(t, radio) {
  const off = Math.round((1 - t.price / t.mrp) * 100);
  return `
    <article class="test-card">
      <div class="head"><h4>${t.name}</h4><span class="ic ${t.tint}">${icon(t.ic)}</span></div>
      <div class="info">
        <span>${icon(radio ? 'scan' : 'flask')} ${radio ? t.params : t.params + ' parameters'}</span>
        <span>${icon('clock')} Report in ${t.tat}</span>
        ${radio ? `<span>${icon('map-pin')} 12 centres</span>` : `<span>${icon('home')} ${t.fasting ? 'Fasting req.' : 'Home pickup'}</span>`}
      </div>
      <div class="foot">
        <div class="price"><b>${inr(t.price)}</b><s>${inr(t.mrp)}</s><span class="off">${off}% OFF</span></div>
        <button class="add-btn" data-name="${t.name}">${icon('plus')} ${radio ? 'Book' : 'Add'}</button>
      </div>
    </article>`;
}

function renderTests() {
  document.getElementById('pathologyGrid').innerHTML = pathology.map((t) => testCard(t, false)).join('');
  document.getElementById('radiologyGrid').innerHTML = radiology.map((t) => testCard(t, true)).join('');

  const seg = document.getElementById('testSeg');
  seg.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b) return;
    seg.querySelectorAll('button').forEach((x) => x.classList.toggle('active', x === b));
    document.getElementById('pathologyGrid').hidden = b.dataset.target !== 'pathology';
    document.getElementById('radiologyGrid').hidden = b.dataset.target !== 'radiology';
  });

  document.getElementById('tests').addEventListener('click', (e) => {
    const b = e.target.closest('.add-btn');
    if (!b) return;
    const added = b.classList.toggle('added');
    b.innerHTML = added ? `${icon('check')} Added` : `${icon('plus')} Add`;
    if (added) showToast(`${b.dataset.name} added to cart`);
  });
}

function renderTestimonials() {
  const stars = icon('star').repeat(5);
  document.getElementById('testiTrack').innerHTML = testimonials.map((t) => `
    <article class="testi-card">
      <span class="q">${icon('quote')}</span>
      <div class="stars">${stars}</div>
      <p>“${t.text}”</p>
      <span class="tag-proc ${t.tint}">${t.proc}</span>
      <div class="person" style="margin-top:16px">
        <span class="av" style="background:${t.bg}">${t.name.split(' ').map((w) => w[0]).slice(0, 2).join('')}</span>
        <div><b>${t.name}</b><small>${t.city}</small></div>
        <span class="verified">${icon('badge-check')} Verified</span>
      </div>
    </article>`).join('');
}

function renderFaqs(cat = 'general') {
  const list = document.getElementById('faqList');
  list.innerHTML = faqs[cat].map(([q, a], i) => `
    <div class="faq-item ${i === 0 ? 'open' : ''}">
      <button class="faq-q">${q}<span class="tg">${icon('plus')}</span></button>
      <div class="faq-a"><p>${a}</p></div>
    </div>`).join('');
  const first = list.querySelector('.faq-item.open .faq-a');
  if (first) first.style.maxHeight = first.scrollHeight + 'px';
}

function initFaq() {
  renderFaqs();
  document.getElementById('faqList').addEventListener('click', (e) => {
    const q = e.target.closest('.faq-q');
    if (!q) return;
    const item = q.parentElement;
    const open = item.classList.contains('open');
    document.querySelectorAll('.faq-item').forEach((it) => { it.classList.remove('open'); it.querySelector('.faq-a').style.maxHeight = null; });
    if (!open) { item.classList.add('open'); const a = item.querySelector('.faq-a'); a.style.maxHeight = a.scrollHeight + 'px'; }
  });
  const cats = document.getElementById('faqCats');
  cats.addEventListener('click', (e) => {
    const b = e.target.closest('.tab');
    if (!b) return;
    cats.querySelectorAll('.tab').forEach((t) => t.classList.toggle('active', t === b));
    renderFaqs(b.dataset.cat);
  });
}

/* ---------------- Hero slider ---------------- */
function initHero() {
  const slides = [...document.querySelectorAll('.hero-slide')];
  const dots = document.getElementById('heroDots');
  let idx = 0, timer;
  dots.innerHTML = slides.map((_, i) => `<button aria-label="Slide ${i + 1}" class="${i === 0 ? 'active' : ''}"></button>`).join('');
  const go = (n) => {
    idx = (n + slides.length) % slides.length;
    slides.forEach((s, i) => s.classList.toggle('active', i === idx));
    [...dots.children].forEach((d, i) => d.classList.toggle('active', i === idx));
    restart();
  };
  const restart = () => { clearInterval(timer); timer = setInterval(() => go(idx + 1), 6000); };
  dots.addEventListener('click', (e) => { const i = [...dots.children].indexOf(e.target); if (i >= 0) go(i); });
  document.getElementById('heroPrev').onclick = () => go(idx - 1);
  document.getElementById('heroNext').onclick = () => go(idx + 1);
  restart();
}

/* ---------------- Carousels ---------------- */
function initCarousels() {
  document.querySelectorAll('.carousel-nav').forEach((nav) => {
    const track = document.getElementById(nav.dataset.for);
    nav.addEventListener('click', (e) => {
      const b = e.target.closest('button');
      if (!b) return;
      track.scrollBy({ left: Number(b.dataset.dir) * track.clientWidth * 0.75, behavior: 'smooth' });
    });
  });
}

/* ---------------- Callback form ---------------- */
function initCallback() {
  const form = document.getElementById('callbackForm');
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = form.querySelector('#cbName');
    const phone = form.querySelector('#cbPhone');
    let ok = true;
    [name, phone].forEach((f) => f.closest('.form-input').style.borderColor = '');
    if (!name.value.trim()) { name.closest('.form-input').style.borderColor = 'var(--red)'; ok = false; }
    if (!/^[6-9]\d{9}$/.test(phone.value.trim())) { phone.closest('.form-input').style.borderColor = 'var(--red)'; ok = false; }
    if (!ok) return showToast('Please enter a valid name and 10-digit mobile number');
    document.getElementById('callback').classList.add('done');
  });
}

/* ---------------- Misc ---------------- */
function showToast(msg) {
  const t = document.getElementById('toast');
  t.querySelector('span').textContent = msg;
  t.classList.add('show');
  clearTimeout(showToast._t);
  showToast._t = setTimeout(() => t.classList.remove('show'), 2400);
}
window.showToast = showToast;

function initQr() {
  // Decorative QR-like pattern (replace with real QR image for production)
  const pattern = '1111111100000110111011010101101011010111010001101111111';
  document.getElementById('qrBox').innerHTML = [...Array(49)].map((_, i) => `<i class="${pattern[i % pattern.length] === '1' ? '' : 'w'}"></i>`).join('');
}

function initScroll() {
  const header = document.getElementById('header');
  const toTop = document.getElementById('toTop');
  const onScroll = () => {
    header.classList.toggle('scrolled', window.scrollY > 40);
    toTop.classList.toggle('show', window.scrollY > 600);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  toTop.onclick = () => window.scrollTo({ top: 0, behavior: 'smooth' });

  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach((el, i) => { el.style.transitionDelay = (i % 4) * 60 + 'ms'; io.observe(el); });
}

function initCounters() {
  const els = document.querySelectorAll('[data-count]');
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      const el = en.target, end = +el.dataset.count, suf = el.dataset.suffix || '';
      const start = performance.now(), dur = 1400;
      const tick = (now) => {
        const p = Math.min((now - start) / dur, 1);
        el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))).toLocaleString('en-IN') + suf;
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
      io.unobserve(el);
    });
  }, { threshold: 0.5 });
  els.forEach((el) => io.observe(el));
}

function initSearchPlaceholder() {
  const input = document.getElementById('headerSearch');
  const words = ['surgery', 'lab test', 'clinic', 'blood bank', 'MRI scan', 'ambulance', 'ayurveda'];
  let i = 0;
  setInterval(() => {
    if (document.activeElement === input) return;
    i = (i + 1) % words.length;
    input.placeholder = `Search ${words[i]}, ${words[(i + 1) % words.length]}, ${words[(i + 2) % words.length]}...`;
  }, 2500);
}

document.addEventListener('DOMContentLoaded', () => {
  renderSurgeryTabs();
  renderSurgeries();
  renderTests();
  renderTestimonials();
  initFaq();
  initHero();
  initCarousels();
  initCallback();
  initQr();
  initScroll();
  initCounters();
  initSearchPlaceholder();
});
