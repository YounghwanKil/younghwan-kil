---
title: Research Overview
layout: default
parent: Wiki
nav_order: 5
permalink: /wiki/research/
---

# Research Overview

My research asks one question in two forms: **can we trust this model when it acts?**

## Two pillars

### 1. Generative-model safety
Making powerful generators refuse harm *without* breaking benign use.

- **Diffusion safety (ASCG).** Grad-CAM localizes an emerging harmful concept during
  sampling; classifier guidance fires *only* there, *only* when needed. SOTA harmful-concept
  erasure across 4 diffusion backbones with minimal collateral damage; 60,000+ generations
  evaluated with a VLM-based safety-vs-fidelity protocol beyond NudeNet.
- **LLM safety auditing.** Cross-lingual safety asymmetry (safety holds in English but
  leaks elsewhere), reasoning-induced safety erosion, and why diffusion models
  misunderstand negation — auditing 6 open-source LLMs.

### 2. Uncertainty-aware clinical AI
Medical models that quantify confidence and defer when unsure.

- **Evidential deep learning (PerioEDL)** — Dirichlet output decomposing epistemic vs
  aleatoric uncertainty in one forward pass.
- **Conformal prediction (ImplantXrayCP)** — distribution-free coverage guarantees via
  split conformal + temperature scaling.
- **Graph neural networks + MC-Dropout (OralGNN)** — tooth-level prediction on an
  anatomically-structured dental graph.
- **Attention over sparse clinical time series (DATAN, Set-based temporal attention)** —
  ICU mortality and clinical events under missingness.

## The connective tissue

Across both pillars I prefer **methods with a mechanism or guarantee I can point to**:
guidance gated on localized evidence; prediction sets with provable coverage; uncertainty
that decomposes into interpretable parts. This is the industrial-engineering instinct —
*build systems that stay dependable under uncertainty* — applied to modern AI.

## Method toolbox

Diffusion models · classifier guidance · Grad-CAM · LLM alignment auditing · evidential
deep learning · split conformal prediction · temperature scaling · MC-Dropout · graph
attention networks · attention-based clinical time-series modeling · VLM-based evaluation.

See [Projects]({{ '/wiki/projects/' | relative_url }}) for per-project detail and
[Publications]({{ '/wiki/publications/' | relative_url }}) for the full list.
