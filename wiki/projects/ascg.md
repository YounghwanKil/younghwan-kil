---
title: ASCG
layout: default
parent: Projects
grand_parent: Wiki
nav_order: 1
permalink: /wiki/projects/ascg/
---

# ASCG — Adaptive Spatial Classifier Guidance for Diffusion Models
{: .no_toc }

> **Venue:** CVPR Workshop on Safe and Trustworthy Foundation Models (SAFE) 2026 — **accepted**.
> **Authors:** Y. Kil, J. Park, G. Nam, J. Lee†.
> **Stack:** Python · PyTorch · diffusers · Grad-CAM · Stable Diffusion 1.4/1.5 · SDXL-Turbo · SDXL-Lightning.

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
- **SOTA harmful-concept (nudity) erasure across 4 diffusion backbones.**
- **Minimal collateral damage** to benign prompts.
- **60,000+ generations evaluated** (5,000 × 4 backbones × 3 conditions).
- Training-free — operates purely at inference.

## STAR seed (for 자소서 / interview)
- **Situation:** Diffusion models generate harmful imagery; blunt erasure breaks normal use.
- **Task:** Suppress harm *without* collateral damage, without retraining.
- **Action:** Designed Grad-CAM-gated classifier guidance that activates only on localized
  harmful evidence; built a VLM-based evaluation beyond NudeNet; validated over 60k+
  generations across 4 backbones.
- **Result:** SOTA erasure with minimal benign damage; accepted at CVPR-W SAFE 2026.
- **What it says about me:** I encode *"do no collateral harm"* directly into methods, and
  I validate at scale.
