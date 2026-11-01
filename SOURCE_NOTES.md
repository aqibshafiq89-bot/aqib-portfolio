# Content provenance

Reviewed 29 October 2026. This is an editorial source record, not an assertion that all professional activities remain current.

## Primary supplied material

- Academic CV: education, role titles/dates, prototypes, supervision, software skills, certifications, awards and the 12 listed publications.
- Supplied portrait: `dist/assets/aqib-shafiq.png`.
- User brief: public name, contact phone, intended positioning, visual direction, PhD interest and research-interest categories.
- Requested email: aqib.shafiq89@gmail.com (matches the CV).
- Requested phone: +971 56 786 3596 (matches the CV).

## Profile sources

- LinkedIn: https://www.linkedin.com/in/engr-aqib-shafiq-abbasi-355b24179/
- Publicly indexed regional LinkedIn profile confirms the Robootika founder statement: https://ae.linkedin.com/in/engr-aqib-shafiq-abbasi-355b24179
- Robootika company page: https://pk.linkedin.com/company/robootika
- Google Scholar profile supplied by the owner: https://scholar.google.com/citations?user=bwT94LAAAAAJ&hl=en

Direct profile retrieval was restricted. Public search indexing supplied limited LinkedIn details. No live Scholar citation or h-index statistics are claimed. An indexed LinkedIn education date differs from the CV's BS end date; the website follows the supplied CV (2013–2017).

## Publication checks

All DOI URLs were extracted from the CV's actual PDF link annotations, not inferred. Source URLs are retained per publication in `content/publications.json`.

- Frontiers publisher record confirms the 2023 charging-scheduling paper and full author list: https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2023.1086793/full
- Energy publisher record confirms smart-grid customer-involvement paper authors: https://www.sciencedirect.com/science/article/pii/S0360544223010204
- Energy publisher record confirms the load-management paper and contribution roles: https://www.sciencedirect.com/science/article/abs/pii/S0360544223017267
- MDPI issue metadata confirms authors of the 2022 inverter-control paper: https://www.mdpi.com/1996-1073/15/17?page=4
- MDPI publisher record confirms V2G paper metadata: https://www.mdpi.com/2071-1050/14/20/13211
- KFUPM institutional record confirms security-bike paper authors: https://pure.kfupm.edu.sa/en/publications/solar-pv-based-electric-vehicle-charging-station-for-security-bik/
- KFUPM institutional record confirms IEEE Access campus-PV author order: https://pure.kfupm.edu.sa/en/publications/feasibility-study-and-deployment-of-solar-photovoltaic-system-to-/
- The author-uploaded Energy Reports manuscript provides corrected author order rather than the CV's abbreviated first-author form: https://www.researchgate.net/publication/371166471_Transition_towards_a_sustainable_power_system_MA-DADC_framework_based_voltage_control_in_high_PV_penetration_networks
- A Frontiers paper's reference list supplies an expanded citation for the multi-agent conference paper: https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2024.1397748/full

Research summaries are short, title-based editorial descriptions, not copied abstracts. Impact factors were intentionally omitted because the supplied CV numbers are historical. The 8+4 figure is explicitly scoped to the CV bibliography, not the complete current scholarly record.

## Public-copy decisions

The website displays city/country, requested email and requested phone. The public CV omits the government-identifier field and the references section. No private identifier or referee contact is retained in the project source.

## Verification

- Local asset and anchor validation; JSON-LD and project-data parse checks.
- Publication totals and project totals checked against the content files.
- Public CV text/link inspection and rendered page review.
- Desktop and 375px effective mobile viewport visual inspection.
- Publication type/year/search/empty-state/reset, project modal and mobile-menu interactions checked in-browser.
- GitHub deployment is prepared but awaits a connected account with write access and Pages settings access.

## Premium redesign — 29 October 2026

The owner's updated brief explicitly supplies six years of robotics/IoT training, 40 schools and approximately 4,000 students as overall reach, plus Founder / Lead Trainer of Robootika. These statements are distinguished from the dated NEP-NIC CV entry (2019–2023, 30 schools). They do not update any employment dates or imply a new institutional appointment. The publication count remains 12 records in the supplied CV, not a live Google Scholar total.

Replaced the old network SVG and six project SVG illustrations with seven original AI-generated concept renders: connected energy installation, campus solar, slow/fast charging cabinets, exploded inductive charging pad, ECG instrumentation, embedded workbench and robotics platform. Full generation prompts and conceptual-use limitations are in `content/visual-assets.json`. These are illustrative visual assets and are not technical references, exact ESP32 pinouts, actual UAJK photographs or evidence of implementation.

Added a separate procedural Three.js r180 energy-system scene. Geometry and scene code are original; Three.js and OrbitControls retain their MIT license. The model is explicitly conceptual, has no performance telemetry and does not reproduce the undocumented thesis architecture. The supplied authentic portrait and public CV are preserved.

The QA browser's WebGL implementation is disabled. Static images, load-failure fallback, layout and interaction checks are verified; the GPU scene requires visual validation on a WebGL2-capable device.

## Professional redesign — 2 November 2026

Rebuilt the page with a lighter academic layout: portrait-led hero, publications placed before projects, and a single "illustrative renderings" note in place of the per-image disclaimers. Removed the optional Three.js viewer and its vendored library. Fonts are now self-hosted. Profile data (research interests, experience, certifications) moved from `scripts/build.py` to `content/profile.json`. Project descriptions were reworded in the first person without adding any new claims; the internal "supporting documentation to add" notes are no longer shown on the public page.
