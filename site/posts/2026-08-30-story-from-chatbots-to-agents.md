---
title: The story so far: from chatbots to agents
subtitle: It's 2 AM and I'm wondering if I picked the wrong agent framework. Four years, three waves — and why the endgame was never a framework at all
date: 2026-08-30
tags: ai, agents, llm, frameworks
draft: false
---

Every few months a new agent framework lands, and the same question fills my
feed: *which one should I pick?* LangChain, LangGraph, CrewAI, ADK, OpenAI's
SDK — the names rotate, the anxiety doesn't.

I've felt it too. You start a prototype, reach for the library everyone's
talking about, ship a demo that looks great — and then it hits production and
things get weird. The agent skips a step and writes a confident answer anyway.
A run fails halfway and you can't tell where. State leaks between turns. You
stare at a stack trace that spans thirty frames of framework internals and
tells you almost nothing useful.

And here's the thought that creeps in at 2 AM: *was my framework choice wrong?
Is the reliability and determinism I need just… not in this thing? Do I rip it
out and start over — or is the next framework going to do the same thing?*

That last question is the trap. Because the real problem isn't usually the
framework you picked. It's that "which framework is best?" was the wrong
question to begin with.

Here's the thing that unstuck it for me. **Underneath, every one of them runs
the same loop.** Think, act, observe, repeat. The framework doesn't change the
loop. It changes who controls it — and how much you can see when it goes wrong.

```raw
<figure class="diag diag-loop">
  <figcaption><span class="diag-k">The loop</span> Every agent framework wraps this</figcaption>
  <div class="loop-row">
    <div class="loop-node">Think<span>reason about the goal</span></div>
    <div class="loop-arr">→</div>
    <div class="loop-node">Act<span>call a tool</span></div>
    <div class="loop-arr">→</div>
    <div class="loop-node">Observe<span>read the result</span></div>
    <div class="loop-arr">↺</div>
    <div class="loop-node loop-node-end">Repeat<span>until done — or forever</span></div>
  </div>
  <p class="loop-note">Four years of frameworks. One loop. The story below is three different answers to who controls it.</p>
</figure>
```

Once you see that, the four-year history of "agent frameworks" stops looking
like a feature race. It looks like three waves — each one fixing the failure of
the one before it. And your 2 AM question answers itself: you don't restart
from scratch. You figure out which failure mode you're actually trying to
engineer around.

## Wave one: when autonomy broke (2022–2023)

The industry started as plumbing. LangChain's first commit, October 2022, was a
thin wrapper around Python's `formatter.format` for gluing prompts together.
Harrison Chase built and shipped it in about nine days, announced it in a tweet
on October 24. Five weeks later ChatGPT launched, and the demand went vertical.

For a while the wrapper was enough. Then came the moment everyone remembers.

March 30, 2023. Toran Bruce Richards ships [AutoGPT](https://en.wikipedia.org/wiki/AutoGPT):
give an AI a goal, walk away, come back to finished work. 100,000 GitHub stars
in months. BabyAGI lands days later. The pitch — *full autonomy, no human in
the loop* — hit at the exact moment of maximum credulity.

I remember running it. You'd hand AutoGPT a task and come back to a folder of
files that had nothing to do with what you asked. The model would wander,
cycle, hallucinate progress, burn tokens with total confidence. Activity charts
from that year show a sharp spike, then a cliff — the hype outran the results,
and most of the copycat projects quietly went away.

> It didn't fail because the idea was wrong. It failed because autonomy had
> outrun the models.

The lesson the field took: 2023 models couldn't be trusted with freedom. The
next wave wouldn't add more autonomy. It would take it away.

## Wave two: the pendulum swings to control (2024)

Two frameworks defined this wave, and they attacked the problem from opposite
ends.

[LangGraph](https://www.langchain.com/blog/langgraph), shipped January 17, 2024,
was the LangChain team's own admission that chains couldn't carry agents. An
agent needs loops, shared state, and a stop button — things a linear chain
cannot express. So they modeled an agent run as a state machine: nodes,
routing edges, a checkpoint after every step, and the ability to pause mid-run
for a human approval and rewind when things went sideways.

[CrewAI](https://www.crewai.com/), open-sourced November 2023, borrowed the
most familiar structure on earth: a team. Define each agent with a role, a goal,
and a backstory. Hand the crew some tools. Let them work through tasks. It reads
like writing job descriptions — which is exactly why a newcomer can ship a
working multi-agent demo in an afternoon.

Different branding. Same question underneath.

> Who is in charge — the model, or the code?

The 2024 answer was the code. Let the LLM reason where reasoning is needed;
wrap it in deterministic control everywhere else. Production agents stopped
being autonomous spirits and became workflows with LLM steps inside. Less
magical. Dramatically more reliable. And honestly, a relief — because the thing
that keeps you up at night with an agent in prod isn't "is it smart enough," it's
"can I tell what it actually did."

```raw
<figure class="diag diag-control">
  <figcaption><span class="diag-k">The pendulum</span> 2023's answer vs. 2024's answer</figcaption>
  <div class="fail-grid">
    <div class="fail-col">
      <div class="fail-head"><span class="fail-ico">🤖</span><span>The model decides</span></div>
      <p>Full autonomy — give a goal, walk away, trust the loop to figure it out.</p>
      <div class="fail-sig bad">✕ wanders, cycles, burns tokens</div>
      <div class="fail-sig bad">✕ hallucinates progress</div>
      <div class="fail-sig bad">✕ no way to tell what it actually did</div>
    </div>
    <div class="fail-col">
      <div class="fail-head"><span class="fail-ico">⚙️</span><span>The code decides</span></div>
      <p>The LLM reasons where reasoning is needed — deterministic control everywhere else.</p>
      <div class="fail-sig ok">✓ checkpoint after every step</div>
      <div class="fail-sig ok">✓ pause mid-run for human approval</div>
      <div class="fail-sig ok">✓ rewind when it goes sideways</div>
    </div>
  </div>
</figure>
```

This is where that 2 AM feeling comes from, by the way. You don't hit the wall
because the model got dumber. You hit it because the framework couldn't tell
you *where* the run went sideways — no checkpoint to replay, no trace of the
tool calls, no way to see the hole. That's the real gap, and it's why so many
teams end up on the same path: prototype fast on whatever's easiest, then the
moment reliability matters, reach for the framework that treats an agent run
like something you can inspect and rewind. The community shorthand for it is
"start with CrewAI for speed, migrate to LangGraph when you hit scaling
limits" — and the fact that the shorthand exists at all tells you the choice
was never really about features.

And then, right as the framework race hit full speed, the most useful
contrarian voice in the field said the quiet part loudly.

## The people who skipped the question

December 2024. Anthropic publishes [Building Effective
Agents](https://www.anthropic.com/engineering/building-effective-agents), drawn
from watching dozens of teams ship. Its finding: **the most successful
production teams weren't using complex frameworks at all.** They were composing
simple patterns out of raw API calls, reaching for "agents" in cases where a
plain workflow — or a single well-prompted call — would do.

The framework warning was specific. Abstraction layers "obscure the underlying
prompts and responses, making them harder to debug." Many published patterns
"can be implemented in a few lines of code" against the raw API.

This wasn't a rejection of wave two. It was a boundary condition. For simple,
single-agent, few-tool systems, the framework tax buys you nothing. The tax
only earns its keep when you add multi-agent topology, durable state, and
compliance requirements. Hold that distinction — it's the hinge of the whole
story.

## Wave three: the bet moves off the frameworks (2025–2026)

The protocol wave started quietly. November 25, 2024: Anthropic ships the
[Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
— "USB for AI." One standard plug between any model and any tool. Within a
year, SDKs in every major language and adoption by OpenAI and Google DeepMind
as the de facto standard.

Then Google made it loud.

April 9, 2025, Google Cloud NEXT. Two announcements at once: ADK, its
open-source multi-agent framework, and the Agent2Agent (A2A) protocol for agents
talking to *each other*. Ten weeks later, Google donated A2A to the
[Linux Foundation](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents)
— spec, SDKs, tooling. AWS, Cisco, Microsoft, Salesforce, SAP, ServiceNow as
founding members. The conversation layer between agents is now governed by a
neutral foundation. Nobody owns it. That's the point.

While the protocols settled, the frameworks paid rent. LangChain rebuilt itself
as 1.0 in October 2025 — agents now run on LangGraph's runtime — and closed a
fresh Series B the same week. AutoGen, Microsoft's
flagship multi-agent framework and once the most-starred project in the
category, slid into maintenance mode, with Microsoft pointing new users to its
Agent Framework successor.

> A framework bet can expire even when it's backed by a trillion-dollar
> company.

That's the real reason the story doesn't end with "pick a framework." MCP
standardized how agents reach tools. A2A standardized how agents reach each
other. Once those two layers sit behind open protocols, **the framework
becomes an implementation detail** — something you swap per agent, not a
marriage you have to survive.

```raw
<figure class="diag diag-stack">
  <figcaption><span class="diag-k">The stack</span> Where the lock-in used to live</figcaption>
  <div class="proto-stack">
    <div class="proto-layer proto-people"><strong>Your agents</strong><span class="proto-sub">one per job, framework-agnostic</span></div>
    <div class="proto-layer proto-wire"><strong>A2A</strong><span class="proto-sub">agents ↔ agents · Linux Foundation governed</span></div>
    <div class="proto-layer proto-wire"><strong>MCP</strong><span class="proto-sub">agents → tools · the de facto standard</span></div>
    <div class="proto-layer proto-swap"><strong>The framework</strong><span class="proto-sub">LangGraph · ADK · CrewAI · none — swappable</span></div>
  </div>
  <p class="proto-note">The framework is no longer the foundation. It's the swappable part.</p>
</figure>
```

You can watch this work in practice. [kagent](https://kagent.dev), a CNCF
Sandbox project that runs agents on Kubernetes, was created by Solo.io — not
Google — yet it picked Google's ADK as its engine, speaks MCP for tools and A2A
between agents, and treats agents like any other cluster workload, with the
same lifecycle, identity, and policy treatment as everything else running
there. Crucially, it doesn't force the ADK bet: it will orchestrate LangGraph
or CrewAI agents under the same governance. Standardize the wires. Stay plural
about the loop.

## What the story actually tells you

```raw
<figure class="diag diag-waves">
  <figcaption><span class="diag-k">The arc</span> Three waves, each fixing the one before</figcaption>
  <div class="wave-grid">
    <div class="wave-card wave-1">
      <div class="wave-year">2022–2023</div>
      <div class="wave-name">Wrappers</div>
      <div class="wave-desc">Make LLM calls easier. Ends when autonomy outruns the models and AutoGPT crashes back to earth.</div>
      <div class="wave-fix">fixed: raw API + prompt plumbing</div>
    </div>
    <div class="wave-card wave-2">
      <div class="wave-year">2024</div>
      <div class="wave-name">Orchestration</div>
      <div class="wave-desc">Make agents controllable — state machines, crews, checkpoints, human approvals.</div>
      <div class="wave-fix">fixed: wandering, no state, no control</div>
    </div>
    <div class="wave-card wave-3">
      <div class="wave-year">2025–2026</div>
      <div class="wave-name">Protocols</div>
      <div class="wave-desc">Make agents interoperate — MCP for tools, A2A between agents, neutral governance.</div>
      <div class="wave-fix">fixing: lock-in — still being written</div>
    </div>
  </div>
</figure>
```

Every framework runs the same underlying loop, so the loop is commodity. What
differs is control, state, and observability — and those are engineering
choices, not loyalty oaths. The interesting question is never "which framework
wins." It's "who controls the loop, and can I leave?"

So back to that 2 AM question — *was my framework choice wrong, do I start
over?* Probably not, and probably not. The framework rarely broke your agent.
The thing that broke it was a gap in state, traceability, or control — and
those are gaps you can close without ripping the stack out. Restart from
scratch and you'll hit the same wall in a different framework. Pick the failure
mode you can live with, add the scaffolding around it, and standardize on the
protocols so next time the framework is the easy part to swap.

The durable layer — the one least likely to be a stranded investment — is the
protocols, because they're the only part of the stack every vendor agreed not
to fight over. Frameworks churn. Protocols accrete.

The framework wars had a winner, and it wasn't a framework.

Part 2 goes under the hood: how LangGraph, ADK, CrewAI, and LangChain 1.0 each
answer "who controls the loop" — what they trade away for it, when the right
framework is no framework at all, and why the platform layer above them might
matter more than any of them.

---

*Thanks for reading — ping me at dengalebr@gmail.com to discuss.*
