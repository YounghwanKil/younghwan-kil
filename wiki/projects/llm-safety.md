---
title: LLM Safety Auditing
layout: default
parent: Projects
grand_parent: Wiki
nav_order: 6
permalink: /wiki/projects/llm-safety/
---

# LLM Safety Auditing
{: .no_toc }

> **Status:** three papers at SCIE Journal (Special Issue on Trustworthy and Safe AI) —
> one in **minor revision**, two in **major revision**. Auditing **6 open-source LLMs**.

- TOC
{:toc}

A line of work auditing where the safety of open-source language (and diffusion) models
*breaks* — and why. Three complementary findings:

## 1. Cross-Lingual Safety Asymmetry in Open-Source LLMs
*S. Chae, Y. Kil† · SCIE Journal — **minor revision**.*
Safety alignment that holds in **English leaks in other languages** — a model refuses a
harmful request in English but complies when it's phrased in another language. Documents
the asymmetry across open-source LLMs and what it implies for deploying "aligned" models
globally.

## 2. Reasoning Reshapes Safety Profiles
*Y. Kil, S. Chae† · SCIE Journal — **major revision**.*
**Chain-of-thought / reasoning can erode safety alignment**: making a model "think" more
can move it *past* its own guardrails. Characterizes this safety erosion in open-source
reasoning models.

## 3. Forbidden Fruit in Latent Space: Why Diffusion Models Misunderstand Negation
*S. Chae, Y. Kil† · SCIE Journal — **major revision**.*
Diffusion models handle **negation** poorly ("a photo *without* X" still contains X). Traces
this to how negation is represented in latent space — directly relevant to safe prompting
and concept removal (ties back to [ASCG]({{ '/wiki/projects/ascg/' \| relative_url }})).

## Why this matters
"Aligned" is not a fixed property — it varies by **language**, by **reasoning depth**, and
by **linguistic phenomena like negation**. This work maps those failure surfaces so they
can be fixed.

## STAR seed
- **S:** Open-source LLMs are called "safe," but safety is uneven.
- **T:** Find *where* and *why* it breaks.
- **A:** Systematic audits across 6 open-source LLMs — across languages, reasoning depth,
  and negation.
- **R:** Three findings (cross-lingual asymmetry, reasoning-induced erosion, negation
  failure), each a paper under review.
- **Says about me:** I think like a *red-teamer for trust* — I find the cracks before
  deployment does.
