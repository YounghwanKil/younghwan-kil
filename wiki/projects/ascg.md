---
title: ASCG
layout: default
parent: Projects
grand_parent: Wiki
nav_order: 2
permalink: /wiki/projects/ascg/
---

# ASCG — Adaptive Spatial Classifier Guidance for Diffusion Models
{: .no_toc }

> **Venue:** Second Edition of Workshop on Synthetic & Adversarial ForEnsics (SAFE@CVPR 2026) — **accepted**.
> **Authors:** Younghwan Kil, Joonhyeong Park, Giung Nam, Juho Lee†.
> **Stack:** Python · PyTorch · diffusers · Grad-CAM · Stable Diffusion 1.4 · Qwen3-VL (evaluation).

[OpenReview](https://openreview.net/forum?id=S9HxdLOgqt) · [SAFE@CVPR](https://www.safeworkshop.org/cvpr-2026/)

- TOC
{:toc}

## What it is
An **inference-time** safety method for text-to-image diffusion. Instead of retraining or
bluntly steering the whole image away from a concept, ASCG uses **Grad-CAM to localize**
the emerging harmful concept during sampling and applies **classifier guidance only where
and when harm is detected** — suppressing unsafe content while leaving benign regions and
benign prompts untouched.

## Why it matters
Existing concept-erasure methods often damage benign generations (the "collateral damage"
problem) or require expensive fine-tuning. ASCG's **selective, spatially-gated** guidance
is the values-in-a-method idea: *precision over blanket censorship*. It also introduces a
**VLM-based safety-vs-fidelity evaluation** that goes beyond the NudeNet detector.

## Results
- Backbone: **Stable Diffusion 1.4**. **SOTA nudity erasure** across **three adversarial
  benchmarks** — UnlearnDiff, Ring-A-Bell, and I2P.
- **Minimal collateral damage** to benign prompts.
- Introduces a **VLM (Qwen3-VL) evaluation protocol** with a Success Rate (Safe + Partial)
  metric that separates *controlled suppression* from *safety-by-destruction* (image
  collapse) — a distinction binary detectors like NudeNet miss.
- Training-free — operates purely at inference.

<details markdown="1">
<summary>Writing notes</summary>

- **Situation:** Diffusion models generate harmful imagery; blunt erasure breaks normal use.
- **Task:** Suppress harm *without* collateral damage, without retraining.
- **Action:** Designed Grad-CAM-gated classifier guidance that activates only on localized
  harmful evidence; built a VLM (Qwen3-VL) evaluation beyond NudeNet; validated on SD 1.4
  across three adversarial benchmarks (UnlearnDiff, Ring-A-Bell, I2P).
- **Result:** SOTA erasure with minimal benign damage; accepted at CVPR-W SAFE 2026 (first author).
- **Emphasis:** I encode *"do no collateral harm"* directly into methods, and
  I validate at scale.

</details>
