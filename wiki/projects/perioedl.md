---
title: PerioEDL
layout: default
parent: Projects
grand_parent: Wiki
nav_order: 2
permalink: /wiki/projects/perioedl/
---

# PerioEDL — Evidential Deep Learning for Periodontitis Staging
{: .no_toc }

> **Status:** under review (2026). **Authors:** Y. Kil, N. Kil†.
> **Stack:** Python · PyTorch · Evidential Deep Learning · Transformers.

- TOC
{:toc}

## What it is
A **Cross-Feature Attention Transformer** with an **evidential Dirichlet output** for
uncertainty-aware periodontitis staging. It decomposes **epistemic vs aleatoric**
uncertainty in a *single forward pass*, enabling selective prediction: the model defers on
cases it is unsure about instead of guessing.

## Why it matters
Clinical staging must be trustworthy. Evidential DL gives calibrated uncertainty cheaply
(one pass, no sampling), so high-confidence predictions can be automated while uncertain
ones route to a clinician.

## Results
- Trained on **CDC NHANES 2013–2014** (3,607 adults, 23 features).
- **Accuracy 0.942**, **macro-F1 0.943**.
- **Selective accuracy 0.960 @ 95% coverage**, **0.967 @ 92.5% coverage** — uncertainty
  guidance lifts accuracy at high-coverage operating points.

## STAR seed
- **S:** Periodontitis staging models are confidently wrong on hard cases.
- **T:** Add trustworthy, cheap uncertainty so the model can defer.
- **A:** Cross-Feature Attention Transformer + evidential Dirichlet head decomposing
  epistemic/aleatoric uncertainty in one pass.
- **R:** 0.942 acc / 0.943 F1; selective accuracy up to 0.967 at high coverage.
- **Says about me:** I build models that *know when they don't know*.
