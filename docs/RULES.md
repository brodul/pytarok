# Slovenian Tarok — rules reference for pytarok

This is the description of the game pytarok implements. Slovenian Tarok has no
single rulebook: social play, club play and tournament play each disagree on
details. This document therefore defines **one baseline ruleset** (§1–§12) and
lists every known divergence as a named **variant** (§13). The engine should
implement the baseline and expose the variants as configuration.

**Both player counts are first-class:**
- **3 players**: the tournament form (Tarok zveza Slovenije). The declarer always plays alone.
- **4 players**: the social form, "klicanje kralja". The declarer may call a king to pick a secret partner.

Most of the game is shared: cards, counting, talon, trick rules, bonuses, klop, radelci and scoring. Rules that apply to only one form are tagged **[3p]** or **[4p]**; untagged rules apply to both. §12 summarises every difference between the two.

Where sources disagree, the choice made for the baseline is stated inline as **[baseline]**, with alternatives in §13. Baseline choices follow pagat.com, cross-checked against Slovenian club and tournament rules.

*Implementation order:* build the core around N players, ship 3-player first, then add the [4p] pieces: the 4×12 deal, king call and hidden partner, solo contracts, king ultimo and partner scoring.

## Sources

- **[P]** pagat.com, *Slovenian Tarok* (J. McLeod / Z. Obradovic, updated 2020) — https://www.pagat.com/tarot/sltarok.html
- **[TZS]** Tarok zveza Slovenije, *Pravila tekmovalnega taroka* (official tournament rules, 3-player) — https://pvds-se.si/wp-content/uploads/2021/11/PRAVILA-TEKMOVALNEGA-TAROKA.pdf
- **[TN]** M. Cigan, *Pravila taroka* v1.08, 2016 (Tarok.net; 2-, 3-, 4-player and "3+1" competitive) — https://www.tarok.net/pravila108.pdf
- **[B]** Društvo »BERAČ«, *Pravila igre tarok*, 2023 (club tournament rules, 3- and 4-player) — https://berac.si/wp-content/uploads/2023/09/Pravila-taroka-precisceno-9.9.2023.pdf

---

## 1. Glossary

| Slovenian | English | Meaning |
|---|---|---|
| tarok | trump | one of the 22 trump cards |
| škis | Skis / Excuse | highest trump (22) |
| mond | Mond | trump XXI |
| pagat | Pagat | trump I, the lowest trump |
| trula | trula | the set škis + mond + pagat |
| talon | talon / widow | the 6 cards dealt face down to the middle |
| štih, vzetek | trick | |
| licitacija | bidding / auction | |
| naprej / dalje | pass | |
| rufati, klicati kralja | call a king | pick a partner by naming a king's suit |
| zarufati se | — | to call a king that turns out to be in the talon |
| založiti | discard | put cards from your hand onto your trick pile after taking talon cards |
| ležim | "I lie down" | the declarer's signal that the talon exchange and his announcements are finished |
| napoved | announcement | committing in advance to a bonus |
| tiho | silent | a bonus achieved without being announced |
| kontra / re / sub / mort | double / redouble / ×8 / ×16 | |
| radelc (pl. radelci), refe | radl | the score-doubling marker |
| renons | revoke / foul | any rule violation, penalised |
| mondfang | captured mond | the mond falls in the same trick as the škis |
| obvezni klop | compulsory klop | |
| platelc / platerc | — | a 1-point card (any card worth 1 point) |
| forehand (obvezna trojka) | — | the first player dealt to, who has the highest bidding priority |

---

## 2. Cards

54 cards: 22 taroks plus 4 suits of 8.

**Taroks** rank from highest to lowest: škis (22), XXI (mond), XX, XIX, … II, I (pagat).
Every tarok beats every suit card (except in colour valat, §8.6).

**Suits.** The rank order differs between red and black suits:

| | high → low |
|---|---|
| ♥ ♦ red | King, Queen, Knight (kaval), Jack (fant), **1, 2, 3, 4** |
| ♣ ♠ black | King, Queen, Knight, Jack, **10, 9, 8, 7** |

> **Gotcha:** among the red pip cards the *1 is high and the 4 is low*. Rank order and face value run in opposite directions.

**Card point values**

| card | value |
|---|---|
| škis, mond, pagat | 5 |
| king | 5 |
| queen | 4 |
| knight | 3 |
| jack | 2 |
| every other card (taroks II–XX, pip cards) | 1 |

The raw values add up to 106. The real total of the pack is **70** because of the counting rule below.

---

## 3. Counting card points

Count a pile in **batches of 3 cards**: the batch is worth the sum of its values **minus 2**.
If 1 or 2 cards are left over at the end, they are worth their sum **minus 1**.

Closed form for a pile of `n` cards whose raw values add up to `S`:

```
points = S − 2·(n // 3) − (1 if n % 3 else 0)
```

Equivalent view: every card is worth (value − 2/3), and the total is rounded.

Invariants, useful for tests:
- The whole deck counts as 70.
- **The two sides' totals always add up to exactly 70**, however the 54 cards are split between them (n%3 = 1 on one side always pairs with n%3 = 2 on the other).
- A single 1-point card is worth 0; two or three 1-point cards are worth 1.

> **Gotcha (current code):** `count_original` gets a lone leftover card wrong (it counts `v` instead of `v−1`). Leftover pairs come out right by coincidence.

Batching is per pile. A side's pile is all its tricks **plus** any talon cards and discards credited to it. The batching order does not matter.

---

## 4. Players, seats, dealing

- **3 or 4 players.** A 5-player table plays the 4-player game with the dealer sitting out each hand; the dealer doesn't score but still receives radelci [P]. A 4-player table can also play "3+1" [TN]: one player rests each hand.
- Play rotates in one fixed direction: anticlockwise in [P] and [TN], clockwise in [TZS] and [B]. For the engine only "next seat" matters.
- **Forehand** is the player next to the dealer in the direction of play, i.e. the first player dealt to.
- **Deal:** shuffle, have the pack cut, then deal **6 cards to the talon first, as one packet from the top of the pack**, then 12 cards each in packets of 6 (in 3-player: 16 each in packets of 8).
  The talon packet keeps its order. That order matters later, because the talon is split into groups in that order.

  | | talon | hands |
  |---|---|---|
  | [3p] | 6 | 3 × 16, in packets of 8 |
  | [4p] | 6 | 4 × 12, in packets of 6 |

- **Knocking** instead of cutting [P] [4p]: the player who would cut chooses which packet of 12 they take. This is a social nicety and optional for the engine. [TZS] forbids knocking.
- **No-tarok hand:** a player dealt no taroks must show their hand. The hand is annulled and redealt by the same dealer.
  **[baseline]** The redeal is a compulsory klop [P]. In [TZS] and [TN] it is a plain redeal.
- **Misdeal:** the dealer is penalised −20, then −40, −80, … for repeat offences, and deals again [P][B]. [TZS] first gives a warning.

---

## 5. Contracts

### 5.1 [3p] contracts

The declarer always plays alone against the other two.

| # | contract | slo. | value | talon | goal |
|---|---|---|---|---|---|
| 0 | klop | klop | special (§10) | turned up in tricks 1–6 | take as few points as possible |
| 1 | three | tri / trojka | 10 + diff | takes 3 | ≥ 36 points |
| 2 | two | dva / dvojka | 20 + diff | takes 2 | ≥ 36 |
| 3 | one | ena / enka | 30 + diff | takes 1 | ≥ 36 |
| 4 | beggar | berač | 70 ([TZS]: 125) | unused | take no trick |
| 5 | solo without | solo brez (talona) | 80 ([TN]: + diff) | goes unseen to the opponents | ≥ 36 |

- **Optional high contracts** ([P] variant; listed in [TN] and [B]): open beggar 90, colour valat 125, valat 500. Each is played as in 4-player.
- **Normal contracts** are 1–3. Only these score difference and bonuses.

### 5.2 [4p] contracts

Contracts in ascending order. **[baseline]** values are from [P].

| # | contract | slo. | value | partner? | talon | goal |
|---|---|---|---|---|---|---|
| 0 | klop | klop | special (§10) | everyone for themselves | turned up in tricks 1–6 | take as few points as possible |
| 1 | three | tri / trojka | 10 + diff | calls a king | takes 3 | ≥ 36 points |
| 2 | two | dva / dvojka | 20 + diff | calls a king | takes 2 | ≥ 36 |
| 3 | one | ena / enka | 30 + diff | calls a king | takes 1 | ≥ 36 |
| 4 | solo three | solo tri | 40 + diff | alone | takes 3 | ≥ 36 |
| 5 | solo two | solo dva | 50 + diff | alone | takes 2 | ≥ 36 |
| 6 | solo one | solo ena | 60 + diff | alone | takes 1 | ≥ 36 |
| 7 | beggar | berač | 70 | alone | unused | take no trick |
| 8 | solo without | solo brez (talona) | 80 | alone | goes unseen to the opponents | ≥ 36 |
| 9 | open beggar | odprti berač | 90 | alone | unused | no trick; hand exposed after trick 1 |
| 10 | colour valat without | barvni valat brez | 125 | alone | none | all tricks, taroks are not trumps |
| 11 | valat without | valat brez | 500 | alone | none | all tricks |

- **[4p] "Normal" contracts** are 1–6. Only these score difference and bonuses.
- Throughout this doc, "normal contracts" means 1–3 in [3p] and 1–6 in [4p].
- **High contracts** are 7 and up. They score their flat value only: no difference, no bonuses. The single exception is the mond penalty, which still applies in solo without (§8.5).
- Colour valat with a talon cannot be bid. It arises only by **upgrading** a solo three/two/one after the exchange (§7.4).

---

## 6. Bidding

1. Forehand is the most senior bidder; seniority decreases around the table, ending with the dealer.
2. **[baseline, P]** Forehand does not speak first. The others bid in turn; each either names a contract or passes.
   - Variant ([TZS][B] "obvezna trojka"): forehand holds an implicit compulsory bid of "three", and the others must outbid it.
3. **Seniority rule.** A junior player must bid **strictly higher** than the current bid. A senior player may **hold**, i.e. bid **equal** to a junior player's bid and take it over.
   Example (A forehand, then B, C, D): B "two", C passes, D must bid at least "one". If D bids "one", A may also say "one" and takes over.
4. **A pass is final.** A player who has passed cannot re-enter.
5. The auction ends when every other player has passed. The last bidder becomes the declarer.
6. If **everyone else passes**:
   - [4p]: forehand chooses any contract, **including klop or three**. Klop and three are available only to forehand and only in this case.
   - [3p] [P]: three is an ordinary bid that any player may make, and klop can't be bid. **If all three players pass, klop is played.**
   - [3p] [TZS]: forehand's compulsory "three" stands. If nobody outbids it, forehand chooses three, anything higher, or klop.
7. **[baseline, P]** The declarer then names the final contract: the bid, or anything higher.
   Variant [B] and many tables: you must play exactly what you bid, except for the colour-valat upgrade.
8. **Compulsory klop:** contracts three through beggar are unavailable, so the lowest bid is solo without. If nobody bids, forehand chooses between solo without or higher and klop; usually klop is played.
   Compulsory klop is triggered when a player's running score is **exactly 0**, and after a no-tarok redeal. [B] also makes the **first hand** of a session a compulsory klop. See §13 for more.

---

## 7. Before play: king call, talon, announcements

### 7.1 [4p] Calling a king (contracts three, two and one)

[3p] has no king call: the declarer is always alone.

- The declarer names a suit **before the talon is turned over**. Whoever holds that king is the secret partner and does not reveal it. Partnerships often become clear only during play.
- **Calling your own king is legal.** You then play 1-vs-3 while the others don't know they are a team. It's usually a mistake, since a solo bid scores 30 more.
- **If the called king is in the talon,** the declarer plays alone (*zarufal se je*):
  - If the declarer takes the talon group containing the king and later **wins a trick with that king**, the untaken rest of the talon is added to that trick, i.e. it goes to the declarer [P].
  - Otherwise the rest of the talon belongs to the opponents.
  - Variants: [B] says in "two" the declarer *must* take the pair containing the king. [TN] says that if the king is taken but never wins a trick, the declarer instead gets a 5-point bonus.
- Variants for holding all four kings: call a trula card, or call "the fourth king" without naming its suit (§13).

### 7.2 Talon exchange (contracts 1–6)

1. Turn the talon face up, split **in dealt order** into groups: 2×3 (three/solo three), 3×2 (two/solo two) or 6×1 (one/solo one). The same applies in [3p].
2. The declarer takes **one group** into hand.
3. The declarer discards (*založi*) the **same number** of cards face down onto their own trick pile. The discards count for the declarer's side.
4. **Kings and trula cards may never be discarded.**
5. **Other taroks may be discarded only face up**, so everyone knows how many trumps remain in play.
   [B] and [TN] go further: taroks and kings may not be discarded at all unless the hand has nothing else, in which case the hand must be shown.
6. The untaken talon groups go face down to the **opponents**. In [4p] king-call games, keep them **separate** until the partnerships are known.
7. In solo without and the high contracts the talon is not looked at. In solo without it goes to the opponents.

### 7.3 Mond left in the talon

If the declarer leaves the mond in an untaken talon group, the declarer gets the **mond penalty** (§8.5), with these exceptions:
- the called king is in another untaken group, and the declarer wins the rest of the talon with it [P] (variants in §13);
- solo without.

### 7.4 Colour-valat upgrade

- [4p]: after the exchange in **solo three, solo two or solo one**, the declarer may raise the contract to **colour valat** (125, nothing else scored). [TN] lets three/two/one upgrade too, with a partner, at lower values.
- [3p]: only if colour valat is enabled. Then three, two or one may be raised after the exchange [P].

### 7.5 Announcements and kontra

After the exchange, starting with the declarer and going round until everyone has passed:

**Bonuses** (normal contracts only):

| bonus | silent | announced | condition |
|---|---|---|---|
| trula | 10 | 20 | your side takes škis, mond and pagat in its tricks |
| kings (kralji) | 10 | 20 | your side takes all 4 kings |
| king ultimo (kralj ultimo) **[4p]** | 10 | 20 | the **called king** is played in the **last trick** and that trick is won by the declarer's side. *Only the partner (holder of the called king) may announce it* [P] |
| pagat ultimo | 25 | 50 | the **pagat wins the last trick** itself. Only the pagat holder may announce it |
| valat | 250 | 500 | your side wins every trick. **Replaces all other scores for the hand**, game included |

- "Silent" (*tiho*) = achieved but not announced, worth half.
- **Either side** can score bonuses. A bonus won by the defenders is subtracted from the declarer's side; a bonus they announce and lose is added to the declarer's side.
- You may announce trula or kings without holding the cards, planning to capture them.
- **Kontra:** an opponent of whoever made a bid or announcement doubles it (×2). The announcing side may rekontra (×4), then sub (×8), then mort (×16).
  Each kontra applies to **one named item** ("kontra the game", "kontra the trula"). The game and each bonus are doubled independently. "The game" covers the contract value plus the difference.
- **You may kontra only if you are certain the announcer is on the other side.** This matters in [4p] king-call games, where partnerships may still be hidden. In [3p] the sides are always known.
- [TZS]: silent bonuses are never subject to kontra.
- The declarer ends their turn by saying **"ležim"**; the others answer "dalje" (pass), or announce/kontra.

---

## 8. Play

### 8.1 Opening lead

- **[baseline]** In contracts up to and including **solo one**, **forehand leads** to trick 1, whoever the declarer is.
- From **beggar** upward, including colour valat and valat, the **declarer leads**.
  The sources disagree about solo without: [P] says the declarer leads; [TZS], [TN] and [B] list only berač and the valats. **[baseline]**: declarer leads in solo without as well.
- After trick 1, the winner of each trick leads to the next.

### 8.2 Legal plays (all contracts)

1. You **must follow the suit led** if you can. If taroks are led, you must play a tarok.
2. If you **can't follow suit, you must play a tarok**.
3. With neither the suit nor any tarok, you may play anything.
4. In **positive contracts you need not beat the cards on the table**. "Barvanje je obvezno, prevzem ni."

### 8.3 Extra rules in negative contracts (klop, beggar, open beggar)

1. **You must beat the highest card already in the trick if you can**, while still obeying 8.2: overtake within the led suit, or if you are trumping, overtrump.
2. **The pagat may be played only when forced:**
   - it is your last card, or
   - it is your only legal card (e.g. your only tarok when you must play a tarok), or
   - the škis and mond are already in the trick, so the pagat wins it (emperor trick, §8.4) and is therefore the "card that beats". [TZS] makes this compulsory: if the other two have played škis and mond in either order, the third player *must* play the pagat if they hold it.
3. [B]: the pagat is likewise "forced" in all contracts worth more than 70.

### 8.4 Who wins a trick

- If the trick contains a tarok, the highest tarok wins; otherwise the highest card of the suit led.
- **Emperor trick (*cesarski štih*):** if **škis, mond and pagat** all fall in the same trick (in any order), **the pagat wins it**.
  - Exception: in colour valat, if a non-tarok was led and the other three cards are exactly the trula, the led card wins.

### 8.5 Captured mond (mondfang)

Applies in **normal contracts and solo without** only, not in klop, beggar or the valats.

- If the škis and the mond fall in the same trick, **the player who played the mond is penalised −20**. This holds even if their own partner won the trick.
- The penalty is **personal**: partners are not affected. It is **never doubled** by kontra or radelc.
- The same penalty applies for leaving the mond in the talon (§7.3).
- **[baseline, P]** It also applies inside an emperor trick. [TZS] says it does *not*.
- [TZS] and [TN] use −21 (they don't round, §9).
- [TN]: if you capture your own partner's mond, both of you pay −20.

### 8.6 Colour valat

- The declarer leads.
- **Taroks are not trumps:** if a suit is led, the highest card of that suit wins, even against taroks played on it.
- A player void in the led suit **must still play a tarok** if they have one. It just can't win.
- If a tarok is led, everyone follows with taroks and the highest tarok wins.
- [B]: the declarer names the suit. Some tables require the declarer to lead all suit cards before any taroks (§13).

### 8.7 Beggar mechanics

- The declarer leads. The talon stays face down and is never used.
- In **open beggar**, after trick 1 the declarer lays their whole hand face up. The opponents may not discuss play.
- Physical convention [P]: played cards are laid in a cross so everyone can see them. This only matters for UIs.

### 8.8 Ultimo bonuses in play

- **Pagat ultimo:** the pagat must **win** the last trick. Partner winning it doesn't count.
- **King ultimo:** the called king must be **in** the last trick and the declarer's **side** must win that trick.
- **Implied attempt:** if the pagat or the called king is played to the last trick **without** an announcement, it counts as a silent attempt. If it fails, the side loses the silent value (−25 or −10).
- An **announced** ultimo fails if:
  - the card is played to the last trick and loses;
  - the card is forced out earlier;
  - the side doesn't hold the card at all.
- The announcing side **must keep the card until the last trick** if the rules of play allow it.
- An announcement of **valat cancels** all other announcements, including the obligation to hold the ultimo card [P][B].

---

## 9. Scoring normal contracts

**Win condition:** the declarer's side takes **at least 36** of the 70 points. 35 is a loss.

**Difference:** `diff = points − 35`, then round:
- **[baseline, P][B]** round to the nearest 5;
- [TZS][TN] use the exact difference.

Examples with rounding to 5: 43 points → +10, 37 → 0, 34 → 0 (a loss "by 0"), 21 → −15.

**Score for the hand, from the declarer side's point of view:**

```
game     = ±(contract value + |diff|) × kontra multiplier for the game
bonuses  = Σ ±(silent or announced value) × that bonus's kontra multiplier
           (+ if won by the declarer's side or lost by the defenders; − otherwise)
hand     = (game + bonuses) × 2 if the declarer has an uncancelled radelc
mond     = −20 to whoever lost the mond (separate, never multiplied)
```

- The **game and each bonus are independent**. You can win the game and still lose points overall on bonuses.
- **Valat** (silent 250 / announced 500) replaces the game and all bonuses.
- [3p]: only the declarer writes the game score. Defenders write their own bonus results, and [TN] gives the non-announcing defender half.
- **[4p] [baseline, P] Partner solidarity:** the declarer and partner each write the same amount; the defenders write nothing.
  Variants: [TN] says the partner writes half. In "money" scoring, each player pays or receives individually (§13).

**High contracts:** the declarer's side writes ± the flat value (× kontra, × radelc). There is no difference and no bonuses.

**Radelci (*radlci*):**
- **Every** player gets a radelc after any hand in which:
  - klop was played,
  - beggar or a higher contract was played, or
  - any valat was won or lost.
  It is added **after** that hand is scored.
- When a declarer with a radelc plays, their hand score is **doubled**. If they **win**, one radelc is cancelled; if they lose, it isn't (and the loss is doubled).
- [P] doubles the partner too. [B] does not double the partner.
- At the end of the session, every uncancelled radelc costs **−100**.

---

## 10. Klop

Played when everyone passes and forehand chooses it, or when compulsory (§6.8).

- Every player for themselves. There are no bonuses and no announcements, except the kontra variant below.
- The negative-contract rules apply (§8.3): **must beat if possible**, and the **pagat only when forced**.
- **Talon "vitamins":** during the first 6 tricks, the top talon card (in dealt order) is turned up and added to each trick, going to its winner.
- **Scoring [P]:**
  - Anyone taking **more than 35** points loses and writes **−70**.
  - Anyone taking **no tricks** wins and writes **+70**.
  - If anybody won or lost this way, *only* those players score.
  - Otherwise each player writes −(their points, rounded to 5).
  - Players with an uncancelled radelc double their result; a radelc-holder who wins writes +140 and cancels a radelc.
- After a klop everyone gets a radelc.
- Klop scoring varies more than any other part of the game: [TZS] has no doubling for radelc in klop; [B] gives +70 for taking every trick and 0 for taking none. See §13.

---

## 11. Renons (fouls), session end

**Renons** includes:
- playing a wrong card, once it has been covered by the next card;
- an illegal discard;
- playing out of turn;
- bidding or announcing out of turn (warning first in [TN]);
- showing cards;
- signalling to a partner;
- (in the engine) any illegal state transition a human client attempts.

The culprit **alone** is charged the full value of the game: contract **+ 35 difference** + announced bonuses, with kontras and radelc. [TN] says kontras don't apply to a bad-discard renons. The engine can simply reject illegal moves; renons scoring matters only for imported or real-table games.

A claim works like this: a player may lay down their hand and claim the remaining tricks. If any claimed trick turns out to be wrong, all remaining tricks go to the opponents [TZS].

**Session end, the škis round:** when the players want to stop, they play a hand and note who was **dealt** the škis. That player's next deal is the last hand of the session. If the škis was in the talon, repeat the škis round. After the last hand, subtract the leftover radelci (−100 each) and rank by total.
Tournaments instead use fixed counts of hands: 12, 21, 24 …

---

## 12. 3-player vs 4-player at a glance

Everything not listed here is identical.

| aspect | [3p] | [4p] |
|---|---|---|
| deal | talon 6 + 3×16 (packets of 8) | talon 6 + 4×12 (packets of 6) |
| sides | declarer alone vs 2 | declarer + called partner vs 2, or alone vs 3 |
| hidden partner | never | yes, until the called king shows |
| contracts | klop, three, two, one, beggar, solo without (+ optional open beggar, colour valat, valat) | klop, three, two, one, solo three/two/one, beggar, solo without, open beggar, colour valat without, valat without |
| klop | played when all pass ([TZS]: forehand's choice) | forehand's choice when all others pass |
| three | any player may bid it ([TZS]: forehand's compulsory opening) | forehand only, when all others pass |
| bonuses | trula, kings, pagat ultimo, valat | + king ultimo |
| kontra legality | sides always known | must be certain of the announcer's side |
| colour valat | optional, upgrade from three/two/one | upgrade from solo three/two/one, or bid "without" |
| klop "talon player" | in "3+1" the resting player also plays klop [TN] | — |
| tournament use | standard [TZS] | club [B] |

**[3p]-only variants:**
- **Vogel frei** [P]: a player dealt the pagat as their only tarok may announce it. The pagat may then be played to any trick regardless of suit, and wins it.
- **Weak-hand annulment**: a hand with ≤ 2 taroks, all below X, may be annulled.

[TZS] tournament specifics: the difference is exact (no rounding), the mond penalty is −21, beggar is worth 125, kontra goes up to mort, and a game lasts 21 or 24 hands.

> **Note for pytarok:** `card_handling.split_deck` hard-codes 6 + 3×16, i.e. the 3-player deal. It must be parameterised by player count.

---

## 13. Variant catalogue (engine configuration)

Each variant is listed as `flag` = baseline, then the alternatives.

**Table**
- `players` = 3 · 4 (both first-class) · 5 (4p with dealer sitting out) · "3+1" (4p table playing 3p)
- `direction` = irrelevant to rules; seat order only

**Deal**
- `no_tarok` = redeal + compulsory klop [P] · plain redeal [TZS][TN]
- `annul_weak_hand` (3p) = off · on (≤ 2 taroks, all < X)

**Bidding**
- `forehand_compulsory_three` = off [P] · on [TZS][B]
- `may_raise_after_auction` = on [P] · off [B]
- `contracts_enabled` = all of §5 · add `piccolo` (exactly 1 trick, 70) · add `open_solo_without` (100 [B]) · drop open beggar / colour valat / valat (3p)

**Compulsory klop**
- `compulsory_klop_triggers` = {score == 0, no-tarok redeal} · plus first hand [B] · plus score multiple of 500 · plus after misdeal

**King call**
- `called_king_in_talon` = win the rest of the talon with the king [P] · must take that group [B] · +5 points if the king never wins a trick [TN]
- `four_kings_call` = must call own king · may call a trula card · "fourth king" without suit

**Discards**
- `discard_taroks` = face up [P] · only if nothing else, and show the hand [B][TN]

**Points**
- `win_threshold` = 36 · "35 + one card" (> 35)
- `diff_rounding` = 5 [P][B] · 1 [TZS][TN]
- `mond_penalty` = 20 · 21 (exact scoring)
- `mond_penalty_in_emperor_trick` = yes [P] · no [TZS]
- `mond_in_talon_with_called_king` = see §7.3 · [B]: always penalised if the mond is left, unless the king is also left

**Kontra**
- `kontra_levels` = 4 (kontra, re, sub, mort) · 2 [TN] · 5 (+ hirškontra)
- `kontra_on_silent` = no [TZS][TN] · yes [B]
- `rekontra_by` = either declarer-side player · declarer only [B]

**Partner and radelc**
- `partner_share` = equal [P][B] · half [TN]
- `radelc_doubles_partner` = yes [P] · no [B]
- `radelc_end_penalty` = 100

**Ultimo bonuses**
- `silent_pagat_ultimo_scope` = whole side · holder only (on loss, or always)
- `valat_cancels_ultimo_obligation` = yes

**Klop**
- `klop_scoring` = [P] (±70 / −points) · [TZS] (≥ 35 → −70) · [B] (+70 for taking every trick)
- `klop_kontra` = off · on (×2; contra-caller limits apply)
- `klop_mond_lead_restriction` = off · on (no mond lead while the škis is out)

**Beggar**
- `berac_with_skis` = off · on (lead the škis, the pagat is forced, emperor-trick gamble)

**Colour valat**
- `colour_valat_suit_first` = off · on (lead all suit cards before taroks)
- `colour_valat_with_partner` = off · on [TN]

**3-player**
- `vogel_frei` (3p) = off · on

**Session**
- `session_end` = škis round · fixed number of hands

---

## 14. Engine notes (non-rules, for implementers)

- **Keep the player count a parameter**, not a branch scattered through the code. [4p] differs from [3p] only in the deal, the contract list, the king call, king ultimo and partner scoring (§12). Put the side assignment behind one abstraction that is fixed in [3p] and resolved during play in [4p].
- **Hidden information is part of the rules.** In [4p] king-call games, the partner's identity, the face-down discards and which talon groups belong to whom are all unknown to some players. The legality of a kontra depends on what the *kontra-ing* player knows (§7.5). Model per-player views explicitly.
- **Keep the talon order.** The groups in §7.2 and the klop vitamins in §10 both depend on it.
- **Pile bookkeeping:** rejected talon groups and discards are credited to sides, not to tricks, and the called-king-in-talon rule can move a group between sides mid-hand.
- **Check every count with the sides-sum-to-70 invariant** (§3).
- **The session state machine** (`game.Session`) must check the round counter *before* the unconditional `round_finished` transition. Currently a session never reaches `finished`.
- **Card data:** `SpecialCard.rank_weigh` is a typo for `rank_weight`, and ordering across card types depends on it.
