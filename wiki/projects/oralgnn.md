---
title: OralGNN
layout: default
parent: Projects
grand_parent: Wiki
nav_order: 3
permalink: /wiki/projects/oralgnn/
---

# OralGNN — Graph Attention Networks for Tooth-Level Periodontal Prediction
{: .no_toc }

> **Status:** under review — Euro Dentistry 2026. **Authors:** Y. Kil, N. Kil†.
> **Stack:** Python · PyTorch · PyTorch Geometric · GAT.

- TOC
{:toc}

## What it is
A **28-node dental graph** (one node per tooth) with **three anatomical edge types** —
adjacent, opposing, same-quadrant — processed by a **3-layer multi-head Graph Attention
Network** with **MC-Dropout uncertainty**. It models inter-tooth spatial dependency to
predict periodontal status at the level of individual teeth.

## Why it matters
Periodontal disease is spatially correlated across the mouth; a per-tooth model that
ignores neighbours throws away signal. Encoding dental anatomy as graph structure captures
that dependency, and MC-Dropout adds calibrated uncertainty.

## Results
- Evaluated on **NHANES 2013–2014**: 3,367 patients, **81,130 tooth-level samples**, 4
  severity classes.
- **Accuracy 0.963 ± 0.008**, **macro-F1 0.943 ± 0.011**, **AUC-ROC 0.998 ± 0.001**.
- **Selective accuracy 0.991 @ 90% coverage.**
- Outperforms GCN, GraphSAGE, and MLP baselines.

## STAR seed
- **S:** Per-tooth periodontal prediction ignores spatial correlation between teeth.
- **T:** Exploit dental anatomy while staying uncertainty-aware.
- **A:** Built a 28-tooth graph with 3 anatomical edge types; 3-layer multi-head GAT +
  MC-Dropout.
- **R:** 0.963 acc, 0.998 AUC, beats GCN/GraphSAGE/MLP; 0.991 selective acc @ 90% coverage.
- **Says about me:** I bring the *right inductive bias* (structure) to a domain problem.
