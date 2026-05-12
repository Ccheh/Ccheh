## Zen 

Building open-source agentic-economy infrastructure on Circle's [Arc](https://docs.arc.network). Two shipped protocols, one stack: payment streaming below + quality-conditional settlement above.

### Now

**[Cadence](https://github.com/Ccheh/arc402)** — OSS seller-side streaming USDC payments middleware (Arc402 protocol). Agents pre-deposit USDC into an on-chain escrow once, then sign cheap off-chain EIP-712 claims per API call. Sub-cent per-call billing when batched, zero on-chain overhead per request. The open reference implementation of the Nanopayments pattern Circle has been advocating.

> Live on Arc Testnet — [PaymentEscrow v2 `0xc95b1b...82f8d`](https://testnet.arcscan.app/address/0xc95b1b20f91901206ba3ea94bbc7313e7cd82f8d) · 30 forge tests · 20-claim batch verified · 5/5 adversarial attacks blocked.

**[Crucible](https://github.com/Ccheh/crucible)** — Prediction-market-settled payments for probabilistic AI services, layered above Cadence's payment escrow. Agent's funds are released proportional to a market-resolved quality score, not just delivery confirmation. Service bond pool, pluggable IResolver architecture (testcase / oracle / validator-vote), commit-reveal voting, MasterChef-style validator subscription pool, ERC-8004 reputation events.

> Live on Arc Testnet — [CrucibleMarketV6 `0x6535a3...381A20`](https://testnet.arcscan.app/address/0x6535a3cbb4235746b732ab5d55c6b0988f381a20) + [TestcaseResolverV5 `0x51cc92...3957`](https://testnet.arcscan.app/address/0x51cc924fe83dc5221150f5752454a37121be3957) · 142 forge tests across 6 protocol versions (v0 → v0.6) · end-to-end lifecycle verified on chain.

### Why both

Today's payment rails treat AI as deterministic — pay X, receive Y, done. But AI is probabilistic: outputs stochastic, quality subjective. Cadence makes the payment layer cheap and streaming. Crucible adds quality-conditional settlement above it. Different concerns, deliberately decoupled.

### Path

**MSc Data Science (Sheffield)** → **Strategy research at Polymarket** (quant on USDC-settled prediction markets) → currently shipping agentic-economy infrastructure on Arc.

### Stack

Solidity 0.8.28, Foundry, TypeScript (strict), viem, Express, Python, R.
