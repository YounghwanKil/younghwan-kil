---
title: Publications
layout: default
parent: Wiki
nav_order: 6
permalink: /wiki/publications/
---

# Publications
{: .no_toc }

{% assign accepted_papers = site.data.publications | where: "status", "accepted" %}
{% assign review_papers = site.data.publications | where: "status", "review" %}

{{ site.data.publications.size }} papers · {{ accepted_papers.size }} accepted · {{ review_papers.size }} under review.<br>
Plus 5 conference presentations: 2 international posters and 3 domestic talks.

**Younghwan Kil** is highlighted in author lists. `†` = corresponding author · `*` = equal contribution.
{% if site.openreview_url %}
[OpenReview profile]({{ site.openreview_url }})
{% endif %}

## Accepted papers

{% include publication-list.html publications=accepted_papers %}

## Under review

{% include publication-list.html publications=review_papers %}

## Conference presentations — international (HealthAI 2026, Prague)

7. **DATAN: Diffusion-Augmented Temporal Attention Network for ICU Mortality Prediction
   Under Sparse Clinical Observations.** HealthAI 2026 — poster (accepted). *Y. Kil\*,
   S. K. Kim\*, S. Kim, Y. Kim, S. Yang, G. Manalu.* — co-first author.
   → [project]({{ '/wiki/projects/datan/' | relative_url }})
8. **Uncertainty-Aware Deep Feature Interaction Attention Network for Reliable Type 2
   Diabetes Detection.** HealthAI 2026 — poster (accepted). *Y. Kil.* — sole author.

## Conference presentations — domestic (KIIE)

9. **Set-Based Temporal Attention Networks for Clinical Time Series: A Clinical
   Informatics Framework.** KIIE conference presentation, 2025. *Y. Kil, N. Kil†.*
10. **Time-Dependent Queuing Distribution for Resilient Capacity Arrangement.** KIIE
    conference presentation, 2024. *Y. Kil, S. Chae†.*
11. **Optimization of Sequential Agent Order in Competitive Systems.** KIIE conference
    presentation, 2024. *Y. Kil, S. Chae†.*

---

## By theme

- **Generative-model / diffusion safety:** ASCG, EBSG (NeurIPS 2026), Forbidden Fruit in Latent Space
- **LLM safety auditing:** Cross-lingual safety asymmetry, Reasoning Reshapes Safety Profiles
- **Efficient learning with physical nonlinearities:** Placement over Device Diversity
- **Uncertainty-aware clinical AI:** DATAN, T2D detection, set-based temporal attention
- **Industrial-engineering / OR roots:** queuing, sequential agents
