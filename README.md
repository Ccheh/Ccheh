## Zen Chen

Open-source agentic-economy infrastructure on Circle's [Arc](https://docs.arc.network) — five composable protocols shipped this month, MIT, audit-grade.

### Shipped on Arc

| Protocol | What it does | Repo |
|---|---|---|
| **Cadence** | Streaming USDC for AI API calls (Nanopayments OSS ref impl) | [arc402](https://github.com/Ccheh/arc402) |
| **Crucible** | Pay AI agents based on quality consensus, not delivery | [crucible](https://github.com/Ccheh/crucible) |
| **Helm** | Futarchy for AI agent group decisions | [helm](https://github.com/Ccheh/helm) |
| **Mandate** | Capability-bound spend authorization for agents | [mandate](https://github.com/Ccheh/mandate) |
| **Plinth** | Capital layer — AI funds with cryptographically verifiable PnL | [plinth](https://github.com/Ccheh/plinth) |

All deployed on Arc Testnet, all composable with each other. First on-chain sibling-protocol composition: [Plinth × Mandate](https://github.com/Ccheh/plinth/blob/main/contracts/src/MandatePlinthBridge.sol).

### Why

Today's payment rails treat AI as deterministic. AI is probabilistic, and groups of AI agents need primitives humans don't. Each protocol above is one missing primitive.

### Background

MSc Data Science (Sheffield). Previously: Polymarket researcher, crypto-asset audit at a fund. Now shipping mechanism-design infrastructure on Arc.
