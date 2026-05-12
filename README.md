## Zen 

Building open-source agentic-economy infrastructure on Circle's [Arc](https://docs.arc.network). Three shipped protocols, one stack: payment streaming, quality-conditional settlement, and group decision-making for autonomous agents.

### Now

**[Cadence](https://github.com/Ccheh/arc402)** — OSS seller-side streaming USDC payments middleware (Arc402 protocol). Agents pre-deposit USDC into an on-chain escrow once, then sign cheap off-chain EIP-712 claims per API call. Sub-cent per-call billing when batched, zero on-chain overhead per request. The open reference implementation of the Nanopayments pattern Circle has been advocating.

> Live on Arc Testnet — [PaymentEscrow v2 `0xc95b1b...82f8d`](https://testnet.arcscan.app/address/0xc95b1b20f91901206ba3ea94bbc7313e7cd82f8d) · 30 forge tests · 20-claim batch verified · 5/5 adversarial attacks blocked.

**[Crucible](https://github.com/Ccheh/crucible)** — Stake-weighted Schelling consensus on AI output quality, used as a payment-settlement primitive. Agent's funds are released proportional to a market-resolved quality score, not just delivery confirmation. Service bond pool, pluggable IResolver architecture, commit-reveal voting, MasterChef-style validator subscription pool, ERC-8004 reputation events.

> Live on Arc Testnet — [CrucibleMarketV6 `0x6535a3...381A20`](https://testnet.arcscan.app/address/0x6535a3cbb4235746b732ab5d55c6b0988f381a20) + [TestcaseResolverV5 `0x51cc92...3957`](https://testnet.arcscan.app/address/0x51cc924fe83dc5221150f5752454a37121be3957) · 142 forge tests across 6 protocol versions (v0 → v0.6) · end-to-end lifecycle verified on chain.

**[Helm](https://github.com/Ccheh/helm)** — Futarchy for autonomous agent coordination. Group decisions made by comparing prediction-market prices on conditional outcomes, with the rejected branch's bets refunded. An on-chain implementation of Robin Hanson's 1996 mechanism — never deployed at scale because humans bet emotionally and human bet sizes are too coarse. **Agents on Arc remove both constraints**.

> Live on Arc Testnet — [Helm `0x47e6d5...02691`](https://testnet.arcscan.app/address/0x47e6d5669d302c8ed6b32189820f36c172a02691) + [ManualMetricOracle `0xee573c...6356c`](https://testnet.arcscan.app/address/0xee573c409c2847bbfb564283afac3338e1e6356c) · 31 forge tests · ~0.032 USDC of deploy gas.

### Why all three

Today's payment rails treat AI as deterministic — pay X, receive Y, done. But AI is probabilistic, and groups of AI agents need primitives humans don't.

- **Cadence** makes the payment layer cheap and streaming.
- **Crucible** adds quality-conditional settlement above it.
- **Helm** adds group decision-making for agent collectives that need to coordinate.

Different concerns, deliberately decoupled. Each composable with the others; each useful standalone.

### Path

**MSc Data Science (Sheffield)** → **Strategy research at Polymarket** (quant on USDC-settled prediction markets) → currently shipping mechanism-design infrastructure on Arc.

### Stack

Solidity 0.8.28, Foundry, TypeScript (strict), viem, Express, Python, R.
