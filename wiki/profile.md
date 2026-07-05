---
title: Profile
layout: default
parent: Wiki
nav_order: 1
permalink: /wiki/profile/
---

# Profile — Younghwan Kil (길영환)
{: .no_toc }

- TOC
{:toc}

---

## Snapshot

| | |
|---|---|
| **Name** | Younghwan Kil · 길영환 |
| **Role** | M.S. student & graduate researcher, KAIST Kim Jaechul Graduate School of AI |
| **Field** | Trustworthy AI — generative-model safety (diffusion, LLMs) & uncertainty-aware clinical AI |
| **Location** | Yangjae, Seoul, South Korea |
| **Contact** | yhgil99@snu.ac.kr (academic) · yhgil99@naver.com (personal) |
| **Links** | [github.com/YounghwanKil](https://github.com/YounghwanKil) |
| **Education** | KAIST M.S. (AI, 2025–) · SNU B.S. Industrial Engineering (2018–2025, *Summa Cum Laude*) |

## One-line

ML researcher building **AI you can trust** — models that refuse to generate harm and
that *know when they don't know*, validated at scale across diffusion backbones and
open-source LLMs.

## One-paragraph bio

Younghwan Kil is an M.S. student and graduate researcher at KAIST's Kim Jaechul Graduate
School of AI, working on Trustworthy AI. His research spans two complementary halves of
"AI you can trust": **generative-model safety** — making text-to-image diffusion models
and open-source LLMs refuse harmful outputs without breaking benign behaviour — and
**uncertainty-aware clinical AI** — building medical models that quantify their own
confidence so they can defer when unsure. He came to AI from **industrial engineering at
Seoul National University**, where he graduated *Summa Cum Laude* (GPA 4.00/4.30), and
now works across diffusion models, LLM alignment auditing, evidential/conformal
uncertainty, and graph neural networks. His work appears at the CVPR Workshop on Safe and
Trustworthy Foundation Models and HealthAI 2026, with a further body of clinical-AI and
LLM-safety papers under review.

## One-page bio

I am a Trustworthy-AI researcher who believes the hardest and most useful problems in AI
are no longer "can the model do it?" but "**can we rely on it when it does?**" That
conviction shows up in the two research directions I run in parallel.

On the **safety** side, I work on stopping generative models from producing harm while
keeping them fully useful for everyone else. My project **ASCG** (accepted to the CVPR
Workshop on Safe and Trustworthy Foundation Models) uses Grad-CAM to *localize* an
emerging harmful concept during diffusion sampling and applies classifier guidance only
where and when it is needed — erasing unsafe content across four diffusion backbones with
minimal collateral damage to benign prompts, evaluated over 60,000+ generations. In a
parallel line on **LLM safety**, I audit open-source models for *cross-lingual safety
asymmetry* (safety that holds in English but leaks in other languages) and for *safety
erosion introduced by reasoning* — auditing 6 open-source LLMs.

On the **reliability** side, I build clinical models that are honest about uncertainty.
Across dentistry and general medicine I have used **evidential deep learning**
(PerioEDL), **split conformal prediction** (ImplantXrayCP), **MC-Dropout on graph neural
networks** (OralGNN), and **attention over sparse clinical time series** (DATAN, HealthAI
2026) — each designed so the model can say "I'm not sure" and defer rather than guess.

The thread connecting both halves is a preference for **methods with guarantees or
mechanisms I can point to**: guidance that activates only on localized evidence,
prediction sets with distribution-free coverage, uncertainty that decomposes into
epistemic and aleatoric parts. I came to this from **industrial engineering** — a
discipline about making real systems dependable under uncertainty — and I bring that
systems-reliability mindset to modern AI.

## Identity threads (for narrative reuse)

These are the recurring "who I am" threads to draw on when writing 자소서 / statements:

- **Reliability over raw capability.** I consistently choose the version of a problem that
  asks "will this hold up in the real world?" — safety that doesn't break benign use,
  predictions that come with coverage guarantees. *Evidence:* ASCG's selective guidance;
  conformal + evidential clinical models.
- **Bridge-builder across fields.** Industrial engineering → AI; safety ↔ healthcare;
  theory ↔ deployment. I'm comfortable being the person who connects a rigorous method to
  a messy real problem. *Evidence:* IE degree feeding an AI research career; clinical +
  generative-safety portfolio.
- **High-volume, rigorous execution.** A large, evidence-backed body of work (13 papers,
  60k+ evaluated generations, multi-backbone/multi-LLM validation) produced alongside
  coursework and teaching. *Evidence:* publication list; *Summa Cum Laude*; 4 semesters of
  physics tutoring.
- **Service & teaching.** Four semesters tutoring General Physics; scholarship-recognized
  academic record. I like making hard things legible to others.

> **✍️ needs your voice.** The strongest 자소서 lines come from *specific moments* — the
> first time a model's overconfidence scared you, why safety over capability, a failure
> you learned from. See [Values & Motivation]({{ '/wiki/values/' \| relative_url }}) for the
> prompts to fill these in.
