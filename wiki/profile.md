---
title: Profile
layout: default
parent: Wiki
nav_order: 1
permalink: /wiki/profile/
---

# Profile — Younghwan Kil
{: .no_toc }

- TOC
{:toc}

---

## Snapshot

| Attribute | Details |
|---|---|
| **Name** | Younghwan Kil |
| **Role** | M.S. student & graduate researcher, KAIST Kim Jaechul Graduate School of AI |
| **Field** | Trustworthy AI — generative-model safety (diffusion, LLMs) & uncertainty-aware clinical AI |
| **Location** | Yangjae, Seoul, South Korea |
| **Contact** | yhgil99@snu.ac.kr (academic) · yhgil99@naver.com (personal) |
| **Links** | [github.com/YounghwanKil](https://github.com/YounghwanKil) |
| **Education** | KAIST M.S. (AI, 2025–) · SNU B.S. Industrial Engineering & Computer Science — double major (2018–2025, *Summa Cum Laude*) |

## Work experience

- **Haean Research Institute** · 2025-04 - present.
- **AIRS Medical** · Medical AI Intern · September–December 2022.

## Research focus

ML researcher building **AI you can trust** — models that refuse to generate harm and
that *know when they don't know*, validated at scale across diffusion backbones and
open-source LLMs.

## Biography

Younghwan Kil is an M.S. student and graduate researcher at KAIST's Kim Jaechul Graduate
School of AI, working on Trustworthy AI. His research spans two complementary halves of
"AI you can trust": **generative-model safety** — making text-to-image diffusion models
and open-source LLMs refuse harmful outputs without breaking benign behaviour — and
**uncertainty-aware clinical AI** — building medical models that quantify their own
confidence so they can defer when unsure. He came to AI from a **double major in
Industrial Engineering and Computer Science at Seoul National University** — pairing a
systems/optimization foundation with a full CS core — where he graduated *Summa Cum
Laude* (GPA 4.00/4.30), and now works across diffusion models, LLM alignment auditing,
evidential/conformal uncertainty, and graph neural networks. His work has been accepted
at NeurIPS 2026, the Workshop on Synthetic & Adversarial ForEnsics (SAFE@CVPR 2026),
ETRI Journal, and HealthAI 2026, with additional manuscripts under review.

## Research narrative

I am a Trustworthy-AI researcher who believes the hardest and most useful problems in AI
are no longer "can the model do it?" but "**can we rely on it when it does?**" That
conviction shows up in the two research directions I run in parallel.

On the **safety** side, I work on stopping generative models from producing harm while
keeping them fully useful for everyone else. My flagship project **EBSG** (Example-Based
Spatial Guidance, accepted at **NeurIPS 2026**, with Jinwoo Shin and Juho Lee) is a
*training-free* method that uses editable exemplar packs to decompose a broad unsafe
category into specific sub-concepts and steer against each with localized signals —
reaching state-of-the-art erasure across nudity, I2P, and MJA benchmarks, supporting
multi-concept removal, and transferring to a modern backbone (SD3). It grew out of
**ASCG** (accepted to the Workshop on Synthetic & Adversarial ForEnsics (SAFE@CVPR 2026)), which
gates classifier guidance on Grad-CAM evidence (on Stable Diffusion 1.4, evaluated across
three adversarial nudity benchmarks). Both introduce a **VLM-based** safety-vs-fidelity
evaluation that goes beyond binary detectors.

In a parallel line on **LLM safety**, I audit open-source models for *cross-lingual safety
asymmetry* (safety that holds in English but leaks in other languages) and for *safety
erosion introduced by reasoning* — auditing 6 open-source LLMs.

On the **reliability** side, I build clinical models that are honest about uncertainty. I
have used **evidential deep learning** (Dirichlet epistemic/aleatoric decomposition),
**split conformal prediction** (distribution-free coverage with temperature-scaling
calibration), **MC-Dropout**, and **attention over sparse clinical time series** (DATAN,
HealthAI 2026) — each designed so the model can say "I'm not sure" and defer rather than
guess.

The thread connecting both halves is a preference for **methods with guarantees or
mechanisms I can point to**: guidance that activates only on localized evidence,
prediction sets with distribution-free coverage, uncertainty that decomposes into
epistemic and aleatoric parts. I came to this from **industrial engineering** — a
discipline about making real systems dependable under uncertainty — and I bring that
systems-reliability mindset to modern AI.

## Research values

- **Reliability over raw capability.** I consistently choose the version of a problem that
  asks "will this hold up in the real world?" — safety that doesn't break benign use,
  predictions that come with coverage guarantees. *Evidence:* ASCG's selective guidance;
  conformal + evidential clinical models.
- **Bridge-builder across fields.** Industrial engineering + computer science → AI;
  safety ↔ healthcare; theory ↔ deployment. I'm comfortable being the person who connects a
  rigorous method to a messy real problem. *Evidence:* IE + CS double major feeding an AI
  research career; clinical + generative-safety portfolio.
- **High-volume, rigorous execution.** A large, evidence-backed body of work ({{ site.data.publications.size }} papers + {{ site.data.conference_posters.size | plus: 5 }}
  conference presentations spanning diffusion safety, LLM safety auditing, and clinical AI)
  produced alongside coursework, teaching, and national R&D projects. *Evidence:*
  publication list; *Summa Cum Laude*; 4 semesters of physics tutoring.
- **Service & teaching.** Four semesters tutoring General Physics; scholarship-recognized
  academic record. I like making hard things legible to others.

<details markdown="1">
<summary>Writing notes</summary>

The strongest personal-statement lines come from specific moments: the first time a
model's overconfidence felt risky, why safety mattered more than raw capability, or a
failure that changed the research approach. See [Values & Motivation]({{ '/wiki/values/' | relative_url }}) for prompts to fill these in.

</details>
