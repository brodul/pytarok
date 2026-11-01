# Tarok core with contract and table plugins

pytarok should host several ways of playing, so the engine is split into a **core** and **plugins**. The core is the Slovenian Tarok engine itself (cards, deal, tricks, musanje and must-beat, talon, bidding, kontra, scoring building blocks, deal and session). Plugins are of two kinds: **contract** plugins (tri, dve, ena, solo, berač, klop, …) and **table** plugins (3-player, 4-player). Both are discovered through Python entry points, and built-in plugins register the same way as third-party ones.

We rejected a game-agnostic core where cards and tarok live in plugins: the variety we need is between contracts and tables, not between card games, and a generic core would only add an abstraction layer nobody uses. §13 variants stay config flags owned by one plugin or the core, not separate plugins.

## Consequences

- The first slice is core + 3-player table + the tri contract only. While tri is the only contract, an all-pass deal is thrown in and compulsory klop does not trigger; both go away when the klop contract lands.
- A contract plugin must pass the shared conformance suite at every table it supports.

See brodul/pytarok#3 for the full spec.
