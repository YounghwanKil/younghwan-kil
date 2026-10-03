---
title: Home
layout: default
nav_order: 1
permalink: /
---

<section class="home-hero" aria-labelledby="page-title">
  <div class="home-hero__copy">
    <p class="eyebrow">KAIST AI · Trustworthy AI</p>
    <h1 id="page-title">Younghwan Kil <span>길영환</span></h1>
    <p class="home-hero__lede">M.S. student and graduate researcher at KAIST Kim Jaechul Graduate School of AI, working on generative-model safety and uncertainty-aware clinical AI.</p>
    <p class="home-hero__text">I study AI systems that can be trusted when they act: diffusion and LLM safety methods that reduce harmful generations without breaking benign use, and clinical models that know when to defer under uncertainty.</p>

    <div class="contact-strip" aria-label="Contact and profiles">
      <a href="mailto:yhgil99@snu.ac.kr">yhgil99@snu.ac.kr</a>
      <a href="https://github.com/YounghwanKil">GitHub</a>
      {% if site.openreview_url %}<a href="{{ site.openreview_url }}">OpenReview</a>{% endif %}
      <a href="{{ '/wiki/publications/' | relative_url }}">Publications</a>
    </div>
  </div>

  <figure class="home-portrait">
    <img src="{{ '/assets/profile.jpg' | relative_url }}" alt="Portrait of Younghwan Kil" width="425" height="567">
    <figcaption>Seoul, South Korea</figcaption>
  </figure>
</section>

<section class="home-section" aria-labelledby="research-areas">
  <div class="section-heading">
    <p class="eyebrow">Research areas</p>
    <h2 id="research-areas">Methods for reliable AI behavior</h2>
  </div>
  <div class="research-grid">
    <article class="research-card">
      <h3>Generative-model safety</h3>
      <p>Training-free concept erasure, localized guidance, LLM safety auditing, cross-lingual safety asymmetry, and evaluation protocols that separate safety from fidelity.</p>
    </article>
    <article class="research-card">
      <h3>Uncertainty-aware clinical AI</h3>
      <p>Evidential learning, conformal prediction, sparse clinical time-series modeling, and deferral-oriented systems for medical decision support.</p>
    </article>
    <article class="research-card">
      <h3>Efficient trustworthy systems</h3>
      <p>Research shaped by an industrial-engineering background: dependable behavior, interpretable mechanisms, and robust performance under real constraints.</p>
    </article>
  </div>
</section>

<section class="home-section" aria-labelledby="selected-publications">
  <div class="section-heading section-heading--inline">
    <div>
      <p class="eyebrow">Selected work</p>
      <h2 id="selected-publications">Accepted publications</h2>
    </div>
    <a class="text-link" href="{{ '/wiki/publications/' | relative_url }}">Full archive</a>
  </div>

  {% if site.data.publications %}
    {% assign selected_publications = site.data.publications | where: 'status', 'accepted' %}
    {% include publication-list.html publications=selected_publications %}
  {% else %}
    <div class="publication-list publication-list--fallback">
      <article class="publication-item">
        <h3 class="publication-title">Publication data is being refreshed.</h3>
        <p class="publication-venue">See the full archive for the current accepted and under-review list.</p>
        <p class="publication-links"><a class="publication-link" href="{{ '/wiki/publications/' | relative_url }}">Open publication archive</a></p>
      </article>
    </div>
  {% endif %}
</section>

<section class="home-section home-section--split" aria-labelledby="position-education">
  <div class="section-heading">
    <p class="eyebrow">Current path</p>
    <h2 id="position-education">Position & education</h2>
  </div>
  <div class="timeline-list">
    <article>
      <span class="timeline-list__date">2025–present</span>
      <h3>KAIST Kim Jaechul Graduate School of AI</h3>
      <p>M.S. student and graduate researcher focused on Trustworthy AI.</p>
    </article>
    <article>
      <span class="timeline-list__date">2018–2025</span>
      <h3>Seoul National University</h3>
      <p>B.S. in Industrial Engineering and Computer Science (double major), Summa Cum Laude, GPA 4.00/4.30.</p>
    </article>
  </div>
</section>

<section class="archive-callout" aria-labelledby="wiki-callout">
  <p class="eyebrow">Living archive</p>
  <h2 id="wiki-callout">More about my research.</h2>
  <p>Explore the projects, research background, and notes behind my work.</p>
  <div class="archive-callout__links">
    <a href="{{ '/wiki/' | relative_url }}">Browse the wiki</a>
    <a href="{{ '/wiki/research/' | relative_url }}">Research overview</a>
    <a href="{{ '/wiki/projects/' | relative_url }}">Projects</a>
  </div>
</section>
