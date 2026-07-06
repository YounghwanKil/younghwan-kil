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

- **Diffusion safety — training-free concept erasure (EBSG → NeurIPS 2026, ASCG →
  CVPR-W SAFE 2026).** Localized, *training-free* steering that suppresses unsafe concepts
  while preserving benign semantics. EBSG uses editable exemplar packs to decompose broad
  unsafe categories into steerable sub-concepts (SOTA across nudity / I2P / MJA benchmarks,
  multi-concept, transfers to SD3); ASCG gates classifier guidance on Grad-CAM evidence
  on Stable Diffusion 1.4 (three adversarial nudity benchmarks). Both introduce a
  **VLM-based** safety-vs-fidelity protocol beyond binary detectors.
- **LLM safety auditing.** Cross-lingual safety asymmetry (safety holds in English but
  leaks elsewhere), reasoning-induced safety erosion, and why diffusion models
  misunderstand negation — auditing 6 open-source LLMs.

### 2. Uncertainty-aware clinical AI
Medical models that quantify confidence and defer when unsure.

- **Attention over sparse clinical time series (DATAN → HealthAI 2026; Set-Based Temporal
  Attention → KIIE).** ICU mortality prediction under missing/irregular observations, and
  reliable Type-2-diabetes detection (HealthAI 2026).
- **Uncertainty methods.** Evidential deep learning (Dirichlet, epistemic vs aleatoric),
  split conformal prediction (distribution-free coverage + temperature-scaling
  calibration), and MC-Dropout — the toolkit for models that defer when unsure.

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
