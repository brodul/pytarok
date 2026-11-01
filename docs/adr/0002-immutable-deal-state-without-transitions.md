# Immutable deal state with a plain phase enum, not `transitions`

The deal engine models its state as an immutable value (frozen dataclasses) with an explicit phase enum (bidding → king call → talon → announcements → play → scoring), and `apply(state, action)` returns a new state. We drop the `transitions` state-machine library the early code used.

AI development needs to branch search from any point and replay a deal from its seed and action log, and a multiplayer backend needs to serialize and copy state cheaply. An object mutated by a library-driven state machine makes all three awkward; a plain value makes them trivial.
