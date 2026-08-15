---
title: "Autoresearch: How Deep-Research AI Agents Are Actually Built"
subtitle: A survey of LLM research-agent architectures — what's deployed, what's benchmarked, and what the honest critiques say.
date: 2026-05-03
tags: ai, agents, research
draft: false
---

Everyone is shipping "deep research" agents, but the architectures underneath
are surprisingly different. This post maps the autoresearch pattern, the state
of the art, the benchmarks, the critiques, and what it means if you build agent
platforms for a living.

## 1. The Autoresearch Pattern, Architecturally

Per 2025 surveys, LLM research agents share roughly four components —
**planning, retrieval, memory, generation** — though terminology varies by
paper. But the three deployed systems most people actually use differ
meaningfully:

| System   | Architecture                                        |
|----------|-----------------------------------------------------|
| OpenAI Deep Research | single-agent, trained end-to-end with RL |
| Anthropic Research  | orchestrator–worker, 3–5 parallel sub-agents |
| Perplexity          | hybrid iterative-retrieval loop, dynamic model selection |

Microsoft's Copilot Researcher pairs OpenAI generation with a Claude critique
stage — an early signal that *heterogeneous* agents are becoming a design
default.

The common primitives across all of them:

- **Plan** (and store the plan *outside* the context window)
- **Retrieve iteratively** (not one-shot)
- **Draft**, then **verify** — with explicit memory management

## 2. State of the Art: Frameworks and Products

The commercial category stabilized through 2025: OpenAI, Anthropic, Perplexity,
Gemini, Manus, Grok and others all ship a research-agent product.

On the open-source side, projects like smolagents' *Open Deep Research* trail
the frontier by roughly **12 points on GAIA**. Two implementation patterns are
hardening into defaults:

1. Plan storage outside the context window
2. MCP-style tool integration for retrieval

## 3. Benchmarks and Evaluation

- **BrowseComp** shows a **25× gap** between tool-augmented base models and
  purpose-built agents.
- **BrowseComp-Plus** reveals that retriever choice dominates performance more
  than generator choice.
- **GAIA** scores are heavily scaffold-dependent — the same model with a better
  scaffold can gain ~30 points.
- **DRACO** scores 100 tasks across 10 domains.

The meta-finding across all of them: benchmarks score *final answers*, not
*trajectories*. An agent that flails productively and one that glides both look
identical on the leaderboard.

## 4. Recent Research Directions

Three threads stand out in the literature:

1. **Pipeline formalization** — treating research agents as typed dataflow
   graphs rather than prompt chains.
2. **Optimization technique selection** — knowing when to use prompting vs.
   fine-tuning vs. agentic RL for a given stage.
3. **Verification architecture** — the field is moving away from *intrinsic
   self-correction* toward **architectural diversity**: a different model, not
   the same model talking to itself, does the checking.

## 5. Honest Critiques

This is the section that matters most:

- **17–33% hallucination rates** measured in legal-research AI tools
- Fabricated citations have survived **peer review at NeurIPS**
- Self-critique can *drop* accuracy from 98% to 57% on high-confidence tasks
- Benchmarks miss process-level failures entirely
- Confident phrasing is **34% more likely when models are wrong** — the tone is
  inversely informative

## 6. Implications for Agent-Platform Builders

If you're building the platform rather than the agent:

1. **Use different agents for verification.** Same-model self-critique actively
   hurts on tasks the model is already confident about.
2. **Adopt MCP.** Tool integration is converging there; fight the trend and you
   write glue code forever.
3. **Treat memory as a first-class primitive.** Plan state outside the context
   window is becoming table stakes.
4. **Gate critique on confidence.** Don't run verification unconditionally —
   spend it where the model is uncertain.

## Gap Log

Being honest about what this survey lacks: no adoption metrics, no measurement
of MCP's actual impact, thin sourcing in Section 4, and no single named
prominent critic of the whole paradigm. All candidates for a follow-up.
