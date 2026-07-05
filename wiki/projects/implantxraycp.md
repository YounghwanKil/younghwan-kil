---
title: ImplantXrayCP
layout: default
parent: Projects
grand_parent: Wiki
nav_order: 4
permalink: /wiki/projects/implantxraycp/
---

# ImplantXrayCP — Conformal Dental-Implant Classification
{: .no_toc }

> **Status:** under review (2026). **Authors:** Y. Kil, N. Kil†.
> **Stack:** Python · PyTorch · Split Conformal Prediction · Temperature Scaling.

- TOC
{:toc}

## What it is
**ResNet-50 / EfficientNet-B0 / DenseNet-121** fine-tuned on panoramic dental radiographs,
**calibrated via temperature scaling**, then wrapped with **split conformal prediction
(APS)** to produce prediction *sets* with **distribution-free coverage guarantees**.

## Why it matters
For a clinical classifier, a point prediction isn't enough — you want a guarantee. Split
conformal gives provable coverage regardless of the underlying model, and temperature
scaling first fixes overconfidence so the sets stay small (usually a single class).

## Results
- Trained on the **Mendeley Dental Implant Dataset** (5,107 radiographs, 4 classes).
- **Accuracy 0.974 ± 0.008** (DenseNet-121), **AUC-ROC 0.999 ± 0.001**.
- **ECE 0.051–0.074 → 0.015–0.016** after temperature scaling.
- **100% empirical coverage at 90% target**; **98%+ singleton prediction sets**.

## STAR seed
- **S:** Implant-type classifiers give point predictions with no reliability guarantee.
- **T:** Add distribution-free coverage without ballooning set size.
- **A:** Fine-tuned 3 CNN backbones, temperature-scaled for calibration, wrapped with split
  conformal (APS).
- **R:** 0.974 acc, ECE cut ~4–5×, target coverage met with 98%+ singleton sets.
- **Says about me:** I reach for *guarantees* (conformal) and *calibration*, not just accuracy.
