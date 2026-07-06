---
title: EBSG
layout: default
parent: Projects
grand_parent: Wiki
nav_order: 1
permalink: /wiki/projects/ebsg/
---

# EBSG — Example-Based Spatial Guidance for Training-Free Concept Erasure
{: .no_toc }

> **Venue:** NeurIPS 2026 Conference — **submission under review** (Submission #35988, May 2026).
> **Authors:** Younghwan Kil, Joonhyeong Park, Giung Nam, Jinwoo Shin, Juho Lee.
> **Primary area:** Socio-technical aspects of AI (safety). **Secondary:** Computer vision.

- TOC
{:toc}

## TL;DR
A **training-free**, exemplar-guided method for **localizing and suppressing unsafe visual
concepts** in text-to-image diffusion models while preserving benign semantics.

## What it is
EBSG uses **user-editable exemplar packs** — exemplar text–image pairs — to provide
*granular, localized* spatial guidance for precise concept steering. Instead of coarsely
pushing the *whole* image away from a broad concept (which yields weak signals and lets
models "collapse" to bypass safety checks), EBSG **decomposes a broad unsafe category into
specific sub-concepts** and steers against each with explicit, localized signals. It also
introduces a **VLM-based evaluation protocol** for fine-grained assessment, avoiding the
failure mode of conventional binary evaluators that permit model collapse.

## Why it matters
Current T2I safety is largely **monolithic** in both execution and evaluation — coarse
categorization within broad unsafe concepts, ignoring the specific constituent factors of
a violation. EBSG makes safety **precise and controllable** (per sub-concept, spatially
localized) and **training-free** (no fine-tuning), which is what makes it deployable and
robust to bypass.

## Results
- **State-of-the-art erasure** across diverse safety datasets and concept categories:
  - **4 nudity benchmarks**,
  - **7 I2P harmful-concept slices**,
  - **4 MJA metaphor categories**.
- Supports **multi-concept removal**.
- **Transfers to a modern backbone (SD3).**

## Relationship to ASCG
EBSG is the flagship successor in the same research line as
[ASCG]({{ '/wiki/projects/ascg/' | relative_url }}) (CVPR-W SAFE 2026): both are
**training-free, spatially-localized** safety methods with **VLM-based evaluation beyond
binary detectors**. ASCG gates classifier guidance on Grad-CAM evidence; EBSG replaces the
guidance signal with **editable exemplar packs** that decompose broad concepts into
steerable sub-concepts — a more granular, user-controllable, and transferable design.

## STAR seed (for 자소서 / interview)
- **Situation:** T2I safety methods are monolithic and coarse; models collapse to bypass
  binary safety checks.
- **Task:** Erase unsafe concepts *precisely* — per sub-concept, without retraining, and
  evaluate it honestly.
- **Action:** Designed EBSG — exemplar-pack spatial guidance decomposing broad concepts
  into localized sub-concepts; built a VLM-based fine-grained evaluation protocol;
  validated across nudity / I2P / MJA benchmarks and transferred to SD3.
- **Result:** SOTA erasure across 15 benchmark slices, multi-concept support, SD3 transfer;
  submitted to **NeurIPS 2026** (first author, with Jinwoo Shin & Juho Lee).
- **Says about me:** I push a research line from workshop (ASCG) to a top-venue submission
  (NeurIPS), and I insist that *evaluation* be as rigorous as the method.
