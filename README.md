# Click Your Hospital — Home Page UI

Static desktop home page design for **Click Your Hospital** — *Care Aisi Family Jaisi*.

Open `index.html` in a browser (no build step needed).

Responsive: desktop (>1100px), tablet (≤1100px) and phone (≤768px, tested at 360/390px).
On phones the page gets a hamburger drawer menu, swipeable card rows, an app-style
services icon grid, a vertical journey timeline and a sticky bottom bar (Call / WhatsApp / Free Consultation).

## Structure

```
index.html              Page markup (all sections)
assets/css/styles.css   Design tokens + all section styles
assets/js/icons.js      Inline SVG icon sprite (no external icon library)
assets/js/main.js       Data (surgeries, tests, testimonials, FAQs) + interactions
```

## Sections (top → bottom)

1. Top utility bar + header (matches existing navbar) + category quick-nav
2. Full-width hero banner slider (3 slides) with H1, CTAs, popular chips + "Free Callback" lead form
3. Trust stats strip (patients, hospitals, labs, doctors, rating)
4. Services — Surgeries, Lab Tests, Clinics, Ayurveda, Blood Bank, Health Packages, Health Camps, Ambulance
5. Promo banners — Laser Piles offer, No-Cost EMI
6. Our Top Surgeries — filter tabs + carousel with price/EMI
7. Top Pathology & Top Radiology Tests — toggle, add-to-cart
8. Popular Health Packages
9. From Search to Recovery, We Stay With You — 6-step journey + Care Buddy CTA
10. Insurance & Cashless — insurer partners + 3-step cashless flow
11. Why Choose Us
12. Upcoming Health Camps + Blood Bank / Ambulance banners
13. Testimonials carousel
14. App promotion (store buttons, QR, phone mockups)
15. Partner with us — for Hospitals, Labs, Diagnostic Centres, Clinics, Ayurveda, Blood Banks
16. FAQ (categorised accordion)
17. Final CTA band + Footer, floating WhatsApp / Call buttons

## Brand tokens

Defined in `:root` in `styles.css` — orange `#f07a22` (CTA/care), navy `#1b3270` (trust).
Font: Plus Jakarta Sans (Google Fonts).

## To replace before production

- Logo: swap the text logo in the header/footer with the real logo image
- Phone numbers, email, address, prices, stats and insurer list are placeholders
- QR code in the app section is decorative
