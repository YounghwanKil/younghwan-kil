---
title: Publications
layout: default
parent: Wiki
nav_order: 4
permalink: /wiki/publications/
---

# Publications
{: .no_toc }

{% assign accepted_papers = site.data.publications | where: "status", "accepted" %}
{% assign review_papers = site.data.publications | where: "status", "review" %}

<p class="page-intro">Work on generative-model safety, dependable clinical AI, and efficient learning.</p>

<div class="publication-summary">
  <span><strong>{{ site.data.publications.size }} papers</strong> / {{ accepted_papers.size }} accepted · {{ review_papers.size }} under review</span>
  <span>{{ site.data.conference_posters.size | plus: 5 }} conference presentations</span>
  {% if site.openreview_url %}<a href="{{ site.openreview_url }}">OpenReview profile <span aria-hidden="true">↗</span></a>{% endif %}
</div>

<p class="author-key"><strong>My name</strong> is highlighted. † Corresponding author · * Equal contribution.</p>

<nav class="archive-jump" aria-label="Publication sections">
  <a href="#accepted-papers">Accepted</a>
  <a href="#under-review">Under review</a>
  <a href="#conference-presentations">Presentations</a>
</nav>

<h2 id="accepted-papers">Accepted papers</h2>

{% include publication-list.html publications=accepted_papers %}

<h2 id="under-review">Under review</h2>

{% include publication-list.html publications=review_papers %}

<h2 id="conference-presentations">Conference presentations</h2>

### International · IOCDT 2026 · Online · 7–9 October 2026
{% include conference-posters.html %}

### International · HealthAI 2026 · Prague
<ol class="conference-list" role="list">
  <li>
    <h3 class="conference-title">DATAN: Diffusion-Augmented Temporal Attention Network for ICU Mortality Prediction Under Sparse Clinical Observations.</h3>
    <p class="conference-authors"><strong>Younghwan Kil*</strong>, S. K. Kim*, S. Kim, Y. Kim, S. Yang, G. Manalu.</p>
    <p class="conference-venue">HealthAI 2026 · Poster (accepted) · Co-first author.</p>
    <a class="text-link" href="{{ '/wiki/projects/datan/' | relative_url }}">Project <span aria-hidden="true">↗</span></a>
  </li>
  <li>
    <h3 class="conference-title">Uncertainty-Aware Deep Feature Interaction Attention Network for Reliable Type 2 Diabetes Detection.</h3>
    <p class="conference-authors"><strong>Younghwan Kil</strong>.</p>
    <p class="conference-venue">HealthAI 2026 · Poster (accepted) · Sole author.</p>
  </li>
</ol>

### Domestic · KIIE
<ol class="conference-list" role="list">
  <li>
    <h3 class="conference-title">Set-Based Temporal Attention Networks for Clinical Time Series: A Clinical Informatics Framework.</h3>
    <p class="conference-authors"><strong>Younghwan Kil</strong>, N. Kil†.</p>
    <p class="conference-venue">KIIE conference presentation · 2025.</p>
  </li>
  <li>
    <h3 class="conference-title">Time-Dependent Queuing Distribution for Resilient Capacity Arrangement.</h3>
    <p class="conference-authors"><strong>Younghwan Kil</strong>, S. Chae†.</p>
    <p class="conference-venue">KIIE conference presentation · 2024.</p>
  </li>
  <li>
    <h3 class="conference-title">Optimization of Sequential Agent Order in Competitive Systems.</h3>
    <p class="conference-authors"><strong>Younghwan Kil</strong>, S. Chae†.</p>
    <p class="conference-venue">KIIE conference presentation · 2024.</p>
  </li>
</ol>

## By theme

- **Generative-model / diffusion safety:** ASCG, EBSG (NeurIPS 2026), Forbidden Fruit in Latent Space
- **LLM safety auditing:** Cross-lingual safety asymmetry, Reasoning Reshapes Safety Profiles
- **Efficient learning with physical nonlinearities:** Placement over Device Diversity
- **Uncertainty-aware clinical AI:** DATAN, T2D detection, set-based temporal attention
- **Dental AI:** tooth-level periodontal graph learning, conformal implant classification, oral histopathology MIL
- **Industrial-engineering / OR roots:** queuing, sequential agents
