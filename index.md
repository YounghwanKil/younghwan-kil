---
title: Home
layout: default
nav_order: 1
permalink: /
---

{% assign accepted_publications = site.data.publications | where: 'status', 'accepted' %}

<section class="home-hero" aria-labelledby="page-title">
  <div class="home-hero__identity">
    <h1 id="page-title">Younghwan Kil</h1>
    <p class="home-hero__bio">M.S. student at KAIST Kim Jaechul Graduate School of AI and graduate researcher in SIML, working on Trustworthy AI: safer generative models, LLM safety auditing, and uncertainty-aware clinical AI.</p>

    <nav class="profile-links" aria-label="Contact and profiles">
      <a href="mailto:yhgil99@snu.ac.kr">Email</a>
      <a href="https://github.com/YounghwanKil">GitHub</a>
      {% if site.openreview_url %}<a href="{{ site.openreview_url }}">OpenReview</a>{% endif %}
      <a href="{{ '/wiki/publications/' | relative_url }}">Publications</a>
    </nav>
  </div>

  <figure class="home-portrait">
    <div class="portrait-crop"><img src="{{ '/assets/portrait.jpg' | relative_url }}" alt="Portrait of Younghwan Kil" width="2400" height="3500"></div>
  </figure>
</section>

<section class="home-section" aria-labelledby="research-directions">
  <div class="section-heading section-heading--inline">
    <h2 id="research-directions">Research interests</h2>
    <a class="text-link" href="{{ '/wiki/research/' | relative_url }}">Research overview</a>
  </div>

  <div class="research-directions">
    <article class="research-section">
      <h3>Generative-model safety</h3>
      <p class="research-statement">Training-free concept erasure, localized guidance, and evaluations that separate safety from visual fidelity.</p>
      <ul class="keyword-list" aria-label="Generative-model safety keywords">
        <li>Diffusion safety</li>
        <li>Concept erasure</li>
        <li>VLM evaluation</li>
      </ul>
    </article>
    <article class="research-section">
      <h3>Uncertainty-aware clinical AI</h3>
      <p class="research-statement">Clinical time-series models, evidential learning, and conformal prediction for systems that know when to defer.</p>
      <ul class="keyword-list" aria-label="Clinical AI keywords">
        <li>Clinical time series</li>
        <li>Conformal prediction</li>
        <li>Deferral</li>
      </ul>
    </article>
  </div>
</section>

<section class="home-section" aria-labelledby="work-experience">
  <div class="section-heading section-heading--inline">
    <h2 id="work-experience">Work experience</h2>
    <a class="text-link" href="{{ '/wiki/timeline/' | relative_url }}">Career timeline</a>
  </div>
  <div class="education-highlights">
    <article>
      <span class="timeline-list__date">April 2026–Present</span>
      <h3>Haean Research Institute</h3>
    </article>
    <article>
      <span class="timeline-list__date">September–December 2022</span>
      <h3>AIRS Medical</h3>
      <p>Medical AI Intern</p>
    </article>
  </div>
</section>

<section class="home-section" aria-labelledby="education-honors">
  <div class="section-heading section-heading--inline">
    <h2 id="education-honors">Education &amp; Honors</h2>
    <a class="text-link" href="{{ '/wiki/education/' | relative_url }}">Details</a>
  </div>

  <div class="education-highlights">
    <article>
      <span class="timeline-list__date">2025–present</span>
      <h3>KAIST Kim Jaechul Graduate School of AI</h3>
      <p>M.S. student and graduate researcher focused on Trustworthy AI.</p>
    </article>
    <article>
      <span class="timeline-list__date">2018–2025</span>
      <h3>Seoul National University</h3>
      <p>B.S. in Industrial Engineering and Computer Science; Summa Cum Laude, GPA 4.00/4.30.</p>
    </article>
  </div>
</section>

<section class="home-section home-section--publications" aria-labelledby="home-publications">
  <div class="section-heading section-heading--inline">
    <h2 id="home-publications">Publications</h2>
    <a class="text-link" href="{{ '/wiki/publications/' | relative_url }}">All publications</a>
  </div>

  {% if accepted_publications and accepted_publications.size > 0 %}
    {% include publication-list.html publications=accepted_publications %}
  {% else %}
    <ol class="publication-list publication-list--fallback" role="list">
      <li class="publication-item">
        <div class="publication-main">
          <h3 class="publication-title">Publication data is being refreshed.</h3>
          <p class="publication-venue">See the full archive for the current accepted and under-review list.</p>
        </div>
        <div class="publication-links"><a class="publication-link" href="{{ '/wiki/publications/' | relative_url }}">Open publication archive</a></div>
      </li>
    </ol>
  {% endif %}

  <h3 id="published-conference-posters">Conference posters</h3>
  <p class="page-kicker">IOCDT 2026 · Online · 7–9 October 2026</p>
  {% include conference-posters.html heading_level=4 compact=true %}
<details class="conference-more">
<summary>More conference presentations — HealthAI and KIIE</summary>
{% include conference-presentations.html %}
</details>
</section>

<p class="home-archive-links"><a href="{{ '/wiki/' | relative_url }}">Research wiki</a> · <a href="{{ '/wiki/projects/' | relative_url }}">Project notes</a> · <a href="{{ '/wiki/profile/' | relative_url }}">Full profile</a></p>
