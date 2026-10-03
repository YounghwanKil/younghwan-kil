---
title: Home
layout: default
nav_order: 1
permalink: /
---

{% assign accepted_publications = site.data.publications | where: 'status', 'accepted' %}
{% assign review_publications = site.data.publications | where: 'status', 'review' %}

<section class="home-hero" aria-labelledby="page-title">
  <div class="home-hero__identity">
    <p class="eyebrow">M.S. student · Graduate researcher</p>
    <h1 id="page-title">Younghwan Kil <span>길영환</span></h1>
  </div>
    <p class="home-hero__lede">I study AI systems that can be trusted when they act: generative-model safety, LLM safety auditing, and uncertainty-aware clinical AI.</p>
    <p class="home-hero__text">My work focuses on mechanisms that preserve useful model behavior while reducing harmful generations, and on clinical models that know when to defer under uncertainty.</p>

    <dl class="identity-meta">
      <div>
        <dt>Affiliation</dt>
        <dd>KAIST Kim Jaechul Graduate School of AI</dd>
      </div>
      <div>
        <dt>Location</dt>
        <dd>Seoul, South Korea</dd>
      </div>
      <div>
        <dt>Contact</dt>
        <dd><a href="mailto:yhgil99@snu.ac.kr">yhgil99@snu.ac.kr</a></dd>
      </div>
    </dl>

    <nav class="profile-links" aria-label="Contact and profiles">
      <a href="mailto:yhgil99@snu.ac.kr">Email</a>
      <a href="https://github.com/YounghwanKil">GitHub</a>
      {% if site.openreview_url %}<a href="{{ site.openreview_url }}">OpenReview</a>{% endif %}
      <a href="{{ '/wiki/publications/' | relative_url }}">Publications</a>
    </nav>

  <figure class="home-portrait">
    <img src="{{ '/assets/profile.jpg' | relative_url }}" alt="Portrait of Younghwan Kil" width="425" height="567">
    <figcaption>Younghwan Kil · KAIST AI</figcaption>
  </figure>
</section>

<section class="index-strip" aria-label="Research index">
  <a href="{{ '/wiki/publications/' | relative_url }}#accepted-papers">
    <span class="index-strip__value">{{ accepted_publications.size | default: 0 }}</span>
    <span class="index-strip__label">accepted papers</span>
  </a>
  <a href="{{ '/wiki/publications/' | relative_url }}#under-review">
    <span class="index-strip__value">{{ review_publications.size | default: 0 }}</span>
    <span class="index-strip__label">under review</span>
  </a>
  <a href="{{ '/wiki/publications/' | relative_url }}#conference-presentations">
    <span class="index-strip__value">5</span>
    <span class="index-strip__label">presentations</span>
  </a>
  <a href="{{ '/wiki/research/' | relative_url }}">
    <span class="index-strip__value">2</span>
    <span class="index-strip__label">research pillars</span>
  </a>
</section>

<section class="home-section home-section--publications" aria-labelledby="selected-publications">
  <div class="section-heading section-heading--inline">
    <span class="section-number">01</span>
    <div>
      <p class="eyebrow">Selected work</p>
      <h2 id="selected-publications">Accepted publications</h2>
    </div>
    <a class="text-link" href="{{ '/wiki/publications/' | relative_url }}">Full publication archive</a>
  </div>

  {% if accepted_publications and accepted_publications.size > 0 %}
    {% include publication-list.html publications=accepted_publications %}
  {% else %}
    <ol class="publication-list publication-list--fallback">
      <li class="publication-item">
        <div class="publication-main">
          <h3 class="publication-title">Publication data is being refreshed.</h3>
          <p class="publication-venue">See the full archive for the current accepted and under-review list.</p>
        </div>
        <div class="publication-links"><a class="publication-link" href="{{ '/wiki/publications/' | relative_url }}">Open publication archive</a></div>
      </li>
    </ol>
  {% endif %}
</section>

<section class="home-section" aria-labelledby="research-areas">
  <div class="section-heading section-heading--inline">
    <span class="section-number">02</span>
    <div>
      <p class="eyebrow">Research ledger</p>
      <h2 id="research-areas">Methods for reliable AI behavior</h2>
    </div>
    <a class="text-link" href="{{ '/wiki/research/' | relative_url }}">Research overview</a>
  </div>

  <div class="research-ledger">
    <article class="research-section">
      <span class="research-number">A</span>
      <div>
        <h3>Generative-model safety</h3>
        <p class="research-statement">Training-free concept erasure, localized guidance, and evaluation protocols that separate safety from fidelity.</p>
        <ul class="keyword-list" aria-label="Generative-model safety keywords">
          <li>Diffusion safety</li>
          <li>Concept erasure</li>
          <li>VLM evaluation</li>
        </ul>
      </div>
    </article>
    <article class="research-section">
      <span class="research-number">B</span>
      <div>
        <h3>LLM safety auditing</h3>
        <p class="research-statement">Cross-lingual safety asymmetry, reasoning-induced safety erosion, and audits of open-weight model behavior.</p>
        <ul class="keyword-list" aria-label="LLM safety auditing keywords">
          <li>Alignment erosion</li>
          <li>Cross-lingual safety</li>
          <li>Open-weight LLMs</li>
        </ul>
      </div>
    </article>
    <article class="research-section">
      <span class="research-number">C</span>
      <div>
        <h3>Uncertainty-aware clinical AI</h3>
        <p class="research-statement">Evidential learning, conformal prediction, and sparse clinical time-series models that can defer when unsure.</p>
        <ul class="keyword-list" aria-label="Clinical AI keywords">
          <li>Clinical time series</li>
          <li>Conformal prediction</li>
          <li>Deferral</li>
        </ul>
      </div>
    </article>
  </div>
</section>

<section class="home-section home-section--split" aria-labelledby="position-education">
  <div class="section-heading section-heading--inline">
    <span class="section-number">03</span>
    <div>
      <p class="eyebrow">Current path</p>
      <h2 id="position-education">Position & education</h2>
    </div>
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
  <div>
    <p class="eyebrow">Living archive</p>
    <h2 id="wiki-callout">Research notes, projects, and source material.</h2>
    <p>Explore the project pages and wiki records behind this academic profile.</p>
  </div>
  <div class="archive-callout__links">
    <a href="{{ '/wiki/' | relative_url }}">Browse wiki</a>
    <a href="{{ '/wiki/research/' | relative_url }}">Research overview</a>
    <a href="{{ '/wiki/projects/' | relative_url }}">Projects</a>
  </div>
</section>
