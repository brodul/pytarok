# Lean core; the game is implemented by base plugins (pluggy)

pytarok should host several ways of playing Slovenian Tarok, so the engine is a **lean core** plus **plugins**, and the game itself is implemented by a set of **base plugins** rather than by the core. The core owns the skeleton: the deal loop and phases, immutable state, the action log, the registry and the plugin interfaces. Base plugins supply the rules: **contract** plugins (tri, dve, ena, solo, berač, barvni valat, klop, …), **table** plugins (3-player, 4-player) and the **trick rules** each contract plays with. A contract with unusual play, such as barvni valat where taroks are not trumps, implements its own trick rules.

Plugins are managed with **pluggy** (pytest's plugin system): plugin packages are found through entry points and add their objects through a registration hook; tests register plugins in code. The objects must satisfy the core's `Protocol` interfaces. Base plugins register exactly like third-party ones.

We rejected a game-agnostic core (the variety we need is between contracts and tables, not between card games) and a fat core that ships the trick rules itself (it would make the base rules privileged and harder to replace).

## Consequences

- When a session starts, the set of active plugins (names and versions) is recorded with it, so a session can be replayed against the same plugins.
- Contracts cannot change mid-deal: the colour valat upgrade after the talon exchange (RULES §7.4) is not supported.
- The first slice is core + 3-player table + the tri contract. While tri is the only contract, an all-pass deal is thrown in and compulsory klop does not trigger; both go away when the klop contract lands.
- Every contract plugin must pass the shared conformance suite at every table it supports.

See brodul/pytarok#3 for the full spec.
