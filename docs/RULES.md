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

Where sources disagree, the choice made for the baseline is stated inline as **[baseline]**, with alternatives in §13. Baseline choices follow pagat.com, cross-checked against Slovenian club and tournament rules. Points that no source settles are listed in §15 rather than guessed.

*Implementation order:* build the core around N players, ship 3-player first, then add the [4p] pieces: the 4×12 deal, king call and hidden partner, solo contracts, king ultimo and partner scoring.

## Sources

- **[P]** pagat.com, *Slovenian Tarok* (J. McLeod / Z. Obradovic, updated 2020) — https://www.pagat.com/tarot/sltarok.html
- **[TZS]** Tarok zveza Slovenije, *Pravila tekmovalnega taroka* (official tournament rules, 3-player) — https://pvds-se.si/wp-content/uploads/2021/11/PRAVILA-TEKMOVALNEGA-TAROKA.pdf
- **[TN]** M. Cigan, *Pravila taroka* v1.08, 2016 (Tarok.net; 2-, 3-, 4-player and "3+1" competitive) — https://www.tarok.net/pravila108.pdf
- **[B]** Društvo »BERAČ«, *Pravila igre tarok*, 2023 (club tournament rules, 3- and 4-player) — https://berac.si/wp-content/uploads/2023/09/Pravila-taroka-precisceno-9.9.2023.pdf
- **[MZT]** Mestna zveza tabornikov Ljubljana, *Taborniški tarok* booklet — https://www.mzt.org/wp-content/uploads/tarok_karte_navodila_print.pdf
- **[ST]** slovenski-tarok.si, *Pravila za igranje taroka* — https://slovenski-tarok.si/pravila
- **[ZIR]** *Žirovska pravila taroka* (regional; uses a different "poeni" scoring unit, so cited only for structural rules) — https://mahar.si/Tarok/ZIROVSKA_PRAVILA_TAROKA.pdf
- **[SEL]** ŠD Selca, *Pravila igranja taroka po »Selško«* (1998–2008; poeni scoring, structural rules only) — http://www.sdselca.si/wp-content/uploads/2014/11/2014-tarok-pravila-po-sel%C5%A1ko.pdf
- **[ZN]** znam.si, *Pravila igre Tarok (Tarok Semedela Open)* — https://znam.si/igre/pravila-igre-tarok-tarok-semedela-open/
- **[PSI]** pagat.si, Slovenian adaptation of [P] — https://pagat.si/tarok/
- **[WIKI]** sl.wikipedia.org, *Tarok* — https://sl.wikipedia.org/wiki/Tarok
- **[OS]** DeepMind OpenSpiel, Slovenian tarok engine, `open_spiel/games/tarok/tarok.cc` (code, not a rulebook) — https://github.com/google-deepmind/open_spiel/tree/master/open_spiel/games/tarok
- **[PAL]** Tarok Palčka / StockŠkis (mytja/tarok, commit 5a083f0, 2025): `backend/internal/ws/*.go`, `stockskis/lib/src/stockskis_base.dart` (code, not a rulebook) — https://github.com/mytja/tarok

[OS] and [PAL] are cited for what implementers actually chose, and as warnings where their code breaks the written rules.

> **Terminology trap ([TZS]):** in [TZS], *napovedi* are the bonuses, and ***posebne napovedi* are the kontras** (B1.19). [TN] and [B] use *posebne napovedi* for the bonuses. Read [TZS] B1.14 and B1.20–24 with that in mind.

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
   - **[baseline, P][OS][TN §3.2]** Any senior player may hold against any junior one.
   - Variants: only forehand may hold ([MZT][ST][PAL]; [TN §2.3] and [B] give it to "the first bidder"); nobody may hold, "ni čakanja, ni prevzemanja za nazaj" [SEL]. [TZS] B1.9 mentions only raising ("zviša le igralec s prednostjo"), never holding (§15).
4. **A pass is final.** A player who has passed cannot re-enter.
5. The auction ends when every other player has passed. The last bidder becomes the declarer.
6. If **everyone else passes**:
   - [4p]: forehand chooses any contract, **including klop or three**. Klop and three are available only to forehand and only in this case.
   - [3p] [P]: three is an ordinary bid that any player may make, and klop can't be bid. **If all three players pass, klop is played.**
   - [3p] [TZS]: forehand's compulsory "three" stands. If nobody outbids it, forehand chooses three, anything higher, or klop.
7. **[baseline, P]** The declarer then names the final contract: the bid, or anything higher.
   Variants: [B] rule 12 and [OS]: you must play exactly what you bid, except for the colour-valat upgrade. [TZS] B1.8–9: only forehand may choose higher, and only when their compulsory "three" was not outbid. [ST] [4p]: when the other three pass, forehand must choose something higher than the last bid.
8. **Compulsory klop:** contracts three through beggar are unavailable, so the lowest bid is solo without. If nobody bids, forehand chooses between solo without or higher and klop; usually klop is played.
   Compulsory klop is triggered when a player's running score is **exactly 0**, and after a no-tarok redeal. [B] also makes the **first hand** of a session a compulsory klop. See §13 for more.
   Kontra is never allowed in a compulsory klop [B].
9. **Compulsory three, engine model** ([TZS] B1.6–8, [MZT], [B]). When `forehand_compulsory_three` is on:
   - The auction starts at `high_bid = three, high_bidder = forehand`. Forehand's "three" is not a choice and cannot be withdrawn. It "doesn't mean forehand intends to play it" [MZT].
   - Everyone else bids strictly higher or passes (B1.7: "potrdi … z besedo »dalje« ali pa najavi višjo igro"). Forehand may hold if `hold_rights` allows.
   - If nobody exceeds "three" after the first round, forehand chooses three, any higher contract, or klop (B1.8). [TZS] B2.1: forehand then leads the klop.
   - [B] [4p]: the bid list starts at "two", because "three" belongs to forehand.
   - When compulsory three is **off**: [TN] §3.2 says a forehand who actively bids "three" loses the right to choose klop later.
10. **Beggar vs valat ([TZS] 3p).** The [TZS] ladder is three < two < one < solo without (80) < beggar (125). B3.4: "Prednost pred igro »berač« ima izjemoma samo napoved »valat«". B1.17: valat is a biddable contract **only** to outbid an earlier beggar bid. Valat can't be opened, and nothing else outranks beggar. [MZT] does the same one step higher: valat is biddable only to beat open beggar.
    - Equal high bids (beggar vs beggar, etc.) follow the ordinary hold rule (rule 3). No source has a special rule for them.

---

## 7. Before play: king call, talon, announcements

### 7.1 [4p] Calling a king (contracts three, two and one)

[3p] has no king call: the declarer is always alone.

- The declarer names a suit **before the talon is turned over**. Whoever holds that king is the secret partner and does not reveal it. Partnerships often become clear only during play.
- **Calling your own king is legal.** You then play 1-vs-3 while the others don't know they are a team. It's usually a mistake, since a solo bid scores 30 more.
- **If the called king is in the talon,** the declarer plays alone (*zarufal se je*):
  - If the declarer takes the talon group containing the king and later **wins a trick with that king**, the untaken rest of the talon is added to that trick, i.e. it goes to the declarer [P].
  - Otherwise the rest of the talon belongs to the opponents.
  - Variants: [B] says in "two" the declarer *must* take the pair containing the king. [ST] makes taking the king's group compulsory in every contract. [TN] says that if the king is taken but never wins a trick, the declarer instead gets a 5-point bonus.
  - **[baseline, P][TN][OS]** Taking the king's group is **optional**.
  - **The contract value doesn't change.** The declarer still scores three/two/one, not a solo value. No source says otherwise.
  - **The sides become public** when the talon is turned up. Everyone sees the declarer is alone, so the kontra-legality rule (§7.5) stops restricting anyone.
  - **"Wins a trick with the king" = "the declarer wins the trick the king was played to".** The declarer is alone and plays exactly one card per trick, so the king must be the winning card. [B]'s "pripeljal domov" is the same condition.
  - **"Taken but never wins a trick"** in [TN] can only mean the king lost its trick, because kings can't be discarded and every card gets played. The exceptions are a claim (§11) or an aborted hand. Under [TN] the +5 is **card points**: they are added to the declarer's pile before the win check and the difference, so 31 card points win ("zadošča že, če preseže 30").

  **Case table** ("remainder" = the groups the declarer didn't take) [P][TN][B][OS]:

  | case | remainder goes to | decided | mond penalty if the mond is in the remainder |
  |---|---|---|---|
  | A. king's group **not taken** | opponents | at the exchange | −20 to the declarer |
  | B. taken, king **wins** its trick | declarer, tossed onto that trick [P] | when the king's trick ends | **none** [P][OS] · −20 [B] |
  | C. taken, king **loses** its trick | opponents ([TN]: plus +5 card points to the declarer) | when the king's trick ends | −20 |
  | D. the mond is **in the king's group**, and it is taken | as B or C | — | none (the mond is in hand) |
  | E. king and mond in the **same untaken group** | opponents | at the exchange | −20 [P] · none [B] rule 8 |

  - The remainder is **not a trick**. In case B it adds card points to the declarer, and can complete their trula or kings bonus, but it doesn't count toward valat (§8.9).
  - Until the king's trick ends, keep the remainder in a **pending** pile that belongs to no one. [ST] has the dealer hold it physically. The penalty for a mond in the talon is therefore final only once the remainder's owner is known.
  - If the king's group is not taken, the called king lands in the opponents' pile and is never played. King ultimo is then impossible, and the engine should not offer it.
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

See the case table in §7.1. [B] rule 8 is stricter: "Puščen mond v talonu je vedno −20, tudi, če gre zarufan kralj okoli", i.e. a mond left in the talon always costs −20, but there is no −20 when the called king is left in the talon as well.

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
  With an own-king call the three opponents are partners without knowing it. Each of them may legally kontra only the declarer.
- **Silent bonuses and kontra.** [TN] §3.6: "Tihe realizacije ne gredo pod kontro". [B] §2.11: "Tihe realizacije gredo pod kontro". Nobody names a silent bonus, so [B]'s rule means **the game's kontra multiplier also applies to silent bonuses**. [TZS] doesn't say. Kontras are said "za vsako igro in napoved posebej" (B1.23), and a silent bonus is no *napoved*, so it is unaffected. **[baseline, TN]** silent bonuses are not multiplied.
- The declarer ends their turn by saying **"ležim"**; the others answer "dalje" (pass), or announce/kontra.

**Announcement phase, exact procedure** [P][TZS B1.10][B §2.11][TN §3.6]:

1. The phase is a loop that starts with the declarer, who exchanges, makes any announcements, and says "ležim".
2. On their turn, a player may make **any number** of these actions and then passes:
   - announce bonuses for their own side;
   - raise the kontra level by one on any item where the next level belongs to their side.

   **Kontra and the player's own announcements happen in the same turn.** The worked example in [B] and [TN]: `A: "ležim"`, `B: "dalje"`, `C: "kontra igri, napovem trulo in dalje"`, `A: "dalje"`.
3. **A pass here is not final** (unlike the auction). The loop runs until every player has passed in a row since the last action [P]. A player who passed may still kontra a bonus announced later, or sub an item that was rekontra'd.
4. **Who says which level.** Kontra (×2) and sub (×8) come from an opponent of whoever made the bid or announcement. Rekontra (×4) and mort (×16) come from that bid's or announcement's side. Each level raises the previous by exactly one step [P][PAL].
   - **[baseline, P]** Either declarer-side player may rekontra the game. [B] §2.6 "Rekontro da lahko samo licitator igre", plus [MZT] and [ST]: only the declarer.
   - [ZIR]: the same player may not say both kontra and sub. A per-player rule like this can't be modelled at team level.
   - [4p] A hidden partner who says re reveals themselves, just as with a king-ultimo announcement (§15).
5. **What can be kontra'd:**
   - **the game**: contract value **plus the difference** ([B] §2.11 "igra (h kateri spada še razlika)", [TN], [P], [PAL]);
   - every announced bonus, each separately [P][TZS][B][WIKI]. [PAL] does not allow kontra on trula and kings.
   - the game of **every contract except klop**, high contracts included (beggar, solo without, open beggar, valats). No source forbids it. [PAL] multiplies them all, and [TZS] B1.20 defines a successful kontra as the target losing their game, whatever the contract.
   - Each kontra must name its item: "Kontra mora biti točno določena" [B][TN]. [SEL] alone allows one kontra "na vse skupaj" (on everything).
   - Never the mond penalty [P][B][TN]. [PAL] has an optional *announced* mondfang (42) that can be kontra'd.
6. **[SEL]** restricts kontra on the contract "three" to players who had not yet bid, or whose bid was taken over. Anyone may kontra "two" and higher.

**Who pays for a kontra.** The sources settle kontras in three ways (m = the multiplier, T = the item value including difference):

| model | declarer wins (kontra failed) | declarer loses (kontra succeeded) | sources |
|---|---|---|---|
| **symmetric [baseline]** | declarer side +T·m | declarer side −T·m | [P][B][WIKI][MZT][PAL] |
| caller pays | declarer +T; **the kontra-er** −T·m/2; the other defender 0 | declarer −T·m | [TN] (3p, 3+1 and 4p tables; the partner always writes ±T/2, undoubled) |
| compensation | declarer +T·m; the defender who did **not** kontra gets a bonus equal to what the kontra cost them | declarer −T·m | [TZS] B1.22 |

- [TZS] B1.21 [3p]: when a defender's announcement fails, or a defender's silent pagat fails, "se soigralcu priznajo enake vrednosti, kot igralcu z igro". The other defender is credited the same amount as the declarer.
- **Defenders announce too.** They may announce trula, kings, pagat ultimo and valat [P][WIKI]. Kontra on those comes from the declarer side, subject to the [4p] certainty rule. King ultimo can be announced only by the called-king holder (§8.8), who is always on the declarer side.

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
4. In **positive contracts you need not beat the cards on the table**. "Barvanje je obvezno, prevzem ni." This holds **for taroks as well as suits** [TN][B]: a void player must trump but may undertrump.
5. In positive contracts the pagat may be led or played freely, including voluntarily into a trick with škis and mond, which it then wins. Exceptions: an announced pagat ultimo (§8.8), and the variants in 8.3.4.

### 8.3 Extra rules in negative contracts (klop, beggar, open beggar)

1. **You must beat the highest card already in the trick if you can**, while still obeying 8.2: overtake within the led suit, or if you are trumping, overtrump.
2. **The pagat may be played only when forced:**
   - it is your last card, or
   - it is your only legal card (e.g. your only tarok when you must play a tarok), or
   - the škis and mond are already in the trick, so the pagat wins it (emperor trick, §8.4) and is therefore the "card that beats". [TZS] makes this compulsory: if the other two have played škis and mond in either order, the third player *must* play the pagat if they hold it.
3. [B]: the pagat is likewise "forced" in all contracts worth more than 70.
4. **Precise legal-move algorithm** (negative contracts). It reproduces [P], [OS], [TN]/[B] ("pagat must fall last of the taroks") and [TZS] B2.7 in every case:
   1. `F` = the cards legal under follow-suit (8.2.1–3).
   2. **Must-beat, the "would take the lead" rule.** "The highest card on the table" means *the card currently winning the trick*, using the full winner rule including the emperor trick. If any card in `F` would win the trick if played now, `L` = those cards. Otherwise `L = F`.
   3. **Pagat filter.** If `|L| > 1`, remove the pagat from `L`.
   4. Play any card in `L`.

   Consequences, for tests:

   | situation | legal |
   |---|---|
   | suit led, no tarok in the trick yet, you hold the suit | led-suit cards above the highest led-suit card if you have any, else any led-suit card |
   | suit led, **a tarok already in the trick**, you hold the suit | **any** led-suit card: you can't win, so there is nothing to beat [OS], matching [P] literally |
   | void in the led suit, no tarok in the trick yet | any tarok (each one wins) |
   | void in the led suit, a tarok in the trick | a higher tarok if you have one, else **any** tarok (undertrumping is allowed, but a tarok must still be played [TN][B]) |
   | tarok led | a tarok higher than the highest in the trick if you have one, else any tarok |
   | škis and mond in the trick, you may play a tarok, and you hold the pagat | the pagat only (it is the only winning card) |
   | void in the led suit and no taroks | anything; nothing to beat |
   | leading | anything except the pagat, unless it is your last card ([TN]: "igrati ga sploh ne smemo") |

   - **Gotcha in [OS] and [PAL]:** both apply the emperor force *before* the follow-suit check. Example: ♥ led, A trumps with the škis, B trumps with the mond, and C holds ♥ and the pagat. [OS] then returns `{pagat}`, which is a revoke, and [PAL] deadlocks. **The emperor force applies only when the pagat is already legal under follow-suit.**
   - With the pagat and II, unable to overtrump: you must play the II.
   - [PAL] differs when following suit after a tarok: it still requires a card above the highest led-suit card. No written source supports that (§13 flag).
   - The [TZS] B2.7 "tretji igralec" means, in general, any player still to play after the škis and mond are both in the trick.
5. **Who is bound.** In beggar and open beggar, must-beat and the pagat rule bind **every player**, defenders included [P][ST][MZT][OS][PAL]. No written source limits them to the declarer.
6. **Contrary rule [ZIR]:** in klop the pagat must not take an emperor trick unless it is the player's last tarok.

### 8.4 Who wins a trick

- If the trick contains a tarok, the highest tarok wins; otherwise the highest card of the suit led.
- **Emperor trick (*cesarski štih*):** if **škis, mond and pagat** all fall in the same trick (in any order), **the pagat wins it**.
  - Exception: in colour valat, if a non-tarok was led and the other three cards are exactly the trula, the led card wins.
    **[baseline, OS][PAL]** General form: in colour valat the emperor rule applies only when a tarok is led. On a suit lead, the highest card of the led suit wins as usual. A suit lead plus the trula needs 4 cards, so this case exists only in [4p].
  - The emperor rule applies in **every** contract [P][TZS B1.13][OS][PAL], klop and beggar included. That is why the pagat gets forced in §8.3.
  - **The škis is not the French Excuse.** It must follow a tarok lead, may be led at any time, and wins every trick except an emperor trick, the last trick included. No Slovenian source gives it any excuse-like behaviour.

### 8.5 Captured mond (mondfang)

Applies in **normal contracts and solo without** only, not in klop, beggar or the valats.

- If the škis and the mond fall in the same trick, **the player who played the mond is penalised −20**. This holds even if their own partner won the trick.
- The penalty is **personal**: partners are not affected. It is **never doubled** by kontra or radelc.
- The same penalty applies for leaving the mond in the talon (§7.3).
- **[baseline, P][OS][PAL][ZIR]** It also applies inside an emperor trick. [TZS] B1.13 ("Taka izguba monda ne šteje kot kazenski vzetek") and [MZT] ("Ta scenarij ne velja za »mondfang«") say it does *not*. [TZS] B1.26 defines the mondfang as the škis, "kot najmočnejša karta", taking the mond.
- [TZS] and [TN] use −21 (they don't round, §9).
- [TN]: if you capture your own partner's mond, both of you pay −20. [ZIR]: only an **opponent's** capture counts.
- Contract scope: [OS] includes solo without; [PAL] excludes it. Every source excludes klop, beggar and the valats ([TZS] is ambiguous, §15).

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
  - *Every* play of the pagat to the last trick counts [P "you are deemed to be attempting"][WIKI][TN][PAL]. It is necessarily the player's last card, so "forced" vs "voluntary" can't be told apart there.
  - Pagat played **before** the last trick, unannounced: nothing is scored, whether it was forced or voluntary.
- An **announced** ultimo fails if:
  - the card is played to the last trick and loses;
  - the card is forced out earlier ([TN][B]: "če ga je igralec prisiljen izigrati (vreči) pred zadnjim vzetkom");
  - the side doesn't hold the card at all.
- The announcing side **must keep the card until the last trick** if the rules of play allow it.
  - **Engine:** while a pagat-ultimo announcement stands, the pagat is legal before the last trick only if it is the holder's only legal card. It may never be led unless it is the only card [TN "se ne sme izigrati (vreči ven)", "kot zadnji tarok"]. Treat an announced king ultimo the same way. Silent ultimos put no restriction on play.
- An announcement of **valat cancels** all other announcements, including the obligation to hold the ultimo card [P][B rule 11]. This holds even if the valat then fails.
- **Either side** can hold and score pagat ultimo. A defender's beaten pagat in the last trick is **+25 for the declarer side**; a defender's winning pagat is −25 [P scoring][TZS B1.21][PAL].
- **Pagat ultimo via an emperor trick** in the last trick counts as a success [TN][B 3p section][P][OS]. [TZS] B1.18 requires the last trick to be won "s pagatom, kot edinim tarokom", which read literally excludes it (§13, §15). Any mondfang in that trick is scored separately (§8.5).
- **Pagat and the called king in the same last trick:** score them **independently**. Examples:
  - a declarer-side pagat wins a trick that contains the called king: + pagat ultimo, + king ultimo;
  - a defender's pagat wins it: − pagat ultimo, − king ultimo (the silent king attempt failed);
  - a declarer-side pagat is beaten by a declarer-side tarok, with the king in the trick: − pagat ultimo, + king ultimo.

  [OS] wrongly treats the two as mutually exclusive, and it doesn't check that the pagat actually *won*.
- **[4p] King ultimo when the declarer holds the called king** (own king called, or a zarufan king taken from the talon): **[baseline]** the holder is "the called player" [P], so it scores 10/20 as normal. [TN] "kralj ultimo (vleče sam)" gives 25/50 (§15). If the zarufan king was not taken, king ultimo is impossible (§7.1).
- **[4p] Announcing king ultimo reveals the partner.** [WIKI] calls it "edini legalen način, da se partner razkrije" (the only legal way for the partner to reveal themselves).

### 8.9 Valat details

- **Definition:** one side wins **every trick**. Talon groups, discards and the zarufan remainder are not tricks. Test "won every trick", never the pile size.
- **Silent valat** (declarer side): +250, which **replaces** the game, the difference and every bonus [P][TZS][B][WIKI]. The mond penalty is personal, so it still stands.
- **Kontra on a silent valat:** it is multiplied by the kontras already said on the game, and by radelc. [TZS] B1.14: "obračuna se osnovna vrednost 250 točk, povečana za izrečene posebne napovedi in radelc" (remember that *posebne napovedi* means kontras in [TZS]); [PAL] agrees.
- **Announced valat:** +500 if made. **[baseline, PAL]** −500 if it fails, replacing the game and all bonuses (no rulebook confirms this, §15). It can be kontra'd as its own item [P]. [PAL] instead applies the game's kontra to it.
- **Defenders take every trick:** a valat for the defenders, −250 to the declarer side, replacing everything [WIKI "ena stran"][OS][PAL]. Defenders may also announce valat [WIKI "napove ga lahko kdorkoli"]: −500 to the declarer side if they make it, +500 if they fail.
- **Radelc:** doubles a valat like any hand score. Everyone gets a new radelc after any hand with a valat, won or lost, by either side [P][PAL].
- **High contracts:** colour valat and valat without are contracts with flat values. Taking every trick in beggar, solo without and the other high contracts is just the contract result: there is no valat bonus (§15 for solo without).
- **Klop:** one player taking every trick has > 35 points, so it scores −70 [P][TZS]. [B] rule 3b: +70.
- [TN] is very different: a silent valat is a **50-point bonus** added to the game like trula, and an announced valat has contract-dependent values (§13).

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
- **Order of operations** [P worked examples][PAL]:
  1. round the difference;
  2. multiply the game by its kontra;
  3. multiply each bonus by its own kontra;
  4. sum the game and the bonuses;
  5. double for radelc;
  6. add the mond penalty outside all of this.

  No source rounds after multiplying. Examples: [P] (40 + 15 + 20) × 2 = 150; (30 + 10 + 20 + 10) × 2 = 140, with the mond −20 separate.
- **A loss by 0** still flips the sign: −(value + 0) × m. With exact counting, 35 points is a loss with diff 0.
- **Defenders' bonuses go on the declarer side's line**, so the **declarer's** radelc doubles them. [B] rule 10: "Vedno se vse … piše igralcu, ki je licitiral igro (z radlcem, če ga ima) in njegovemu soigralcu (brez radlca)".
- **Valat** (silent 250 / announced 500) replaces the game and all bonuses. Details in §8.9.
- [3p]: only the declarer writes the game score. Defenders write their own bonus results, and [TN] gives the non-announcing defender half.
- **[4p] [baseline, P] Partner solidarity:** the declarer and partner each write the same amount; the defenders write nothing.
  Variants: [TN] says the partner writes half. In "money" scoring, each player pays or receives individually (§13).

**High contracts:** the declarer's side writes ± the flat value (× kontra, × radelc). There is no difference and no bonuses.

**Radelci (*radlci*):**
- **Every** player gets a radelc after any hand in which:
  - klop was played,
  - beggar or a higher contract was played, or
  - any valat was won or lost.
  It is added **after** that hand is scored, so the triggering hand never uses its own new radelc.
  - A **lost** beggar triggers radelci too: the trigger is the contract being *played* [P][TZS "po odigranem beraču"][PAL]. Colour valat triggers them [P][TN][PAL].
  - Trigger sets differ: [TZS] B1.25 lists klop, beggar and valat (not solo without). [TN] lists klop and the high contracts. [MZT] gives radelci after any game worth **≥ 60** (so solo one too), plus klop and valat. [ST] gives them after klop only.
  - [5p] The sitting-out dealer gets one too [P].
- When a declarer with a radelc plays, their hand score is **doubled**. If they **win**, one radelc is cancelled; if they lose, it isn't (and the loss is doubled).
  - **Only the declarer's radelc counts.** Defenders' radelci are never used or cancelled while they defend [P][B][TN][PAL]. The partner's own radelc is never used or cancelled either.
  - **Radelci never stack:** the score is ×2 however many the declarer holds, and one is cancelled [P][PAL].
  - **"Win" means the contract was made**, not that the hand total is positive. A made game that nets negative after lost bonuses still cancels a radelc [PAL].
- [P] and [TN] ("tudi soigralcu") double the partner too. [B] does not double the partner.
- At the end of the session, every uncancelled radelc costs **−100** [P]. [PAL]: −40.
- **[TZS] radelci work differently** (B1.24–25). A radelc doubles "odigrane igre, napovedi in posebnih napovedi" (game, bonuses and kontras). It is erased "po prvi odigrani igri po pridobitvi le-tega" (after the first hand played after it was gained), **win or lose**. So radelci never accumulate, and there is no end-of-session penalty.
- [ST] "Štajerci" use **collective radelci**: each trigger adds one per player to a shared pool. The next **won** hand, whoever plays it, is doubled and erases one; a lost hand is doubled and erases none.
- **Renons:** [baseline, P] the culprit's own radelc doubles the penalty and is not cancelled. [TZS] C2.3: the declarer's radelc counts, and it is erased if the declarer was the culprit. [TN] §3.4: the radelc counts only if the culprit is the declarer.

---

## 10. Klop

Played when everyone passes and forehand chooses it, or when compulsory (§6.8).

- Every player for themselves. There are no bonuses and no announcements, except the kontra variant below.
- The negative-contract rules apply (§8.3): **must beat if possible**, and the **pagat only when forced**.
- **Talon "vitamins":** during the first 6 tricks, the top talon card (in dealt order) is turned up and added to each trick, going to its winner.
  - Vitamin points count in the winner's pile and are batched like any other card (§3) [TZS B2.6 "točkovna vrednost dodanih kart se prišteje"][P][OS].
  - A vitamin is never a trick of its own. It attaches to a trick of played cards, so it can't change "took no tricks". Test `tricks_won == 0`, not `points == 0` (the two agree, but the first is clearer).
  - [ZIR] 3p variant: no vitamins; each player takes 2 talon cards into hand before play.
- The pagat and must-beat rules are given precisely in §8.3.4. Forehand leads [TZS B2.1].
- **Scoring [P]:**
  - Anyone taking **more than 35** points loses and writes **−70**.
  - Anyone taking **no tricks** wins and writes **+70**.
  - If anybody won or lost this way, *only* those players score.
  - Otherwise each player writes −(their points, rounded to 5).
  - Players with an uncancelled radelc double their result; a radelc-holder who wins writes +140 and cancels a radelc.
- **Exact algorithm [P][OS][PAL][TN]:**
  ```
  full  = {p : points(p) > 35}          # at most one player, since the total is 70
  empty = {p : tricks_won(p) == 0}      # may contain several players
  if full or empty:
      score(p) = -70 if p in full else +70 if p in empty else 0
  else:
      score(p) = -round5(points(p))     # remainder 1–2 rounds down, 3–4 up
  if radelc_in_klop: double each radelc holder's score; an empty holder cancels one
  ```
  - One full player and one empty player: −70 and +70, everyone else 0 ([TN] says so explicitly).
  - With a "≥ 35" threshold ([TZS][TN]), two players on exactly 35 can both be full.
  - Empty players: two in [4p]; two in [3p] only if one player takes every trick.
- After a klop everyone gets a radelc.
- Klop scoring varies more than any other part of the game:
  - [TZS] B2.3: ≥ 35 → −70, everyone else −points, no bonus for taking nothing, and no radelc doubling (B2.5).
  - [TN]: ≥ 35, no radelc ("Točke klopa ne gredo pod radelc").
  - [B]: > 35 → −70, taking no trick = 0, taking every trick = +70.
  - [MZT]: ±35.
  - [ST]: −35 / +10.

  See §13 for the flags.
- **Kontra in klop** (`klop_kontra`, off in the baseline):
  - **[B][PAL]**: anyone may say a single kontra, except the resting "talon" player. Never in compulsory klop. If the kontra-er has the highest total, only they write double; otherwise **everyone** writes double.
  - [TZS] B2.2–4: one kontra, by one player only, offered in seat order. Points are normally doubled for everyone. If the kontra-er has the most points and ≤ 34, only the kontra-er's result is doubled.
  - [TN] §3.8: kontra ×2 and rekontra ×4 for everyone. The kontra-er must take ≤ 17 points, otherwise their points are doubled again.
  - [P] variant: anyone > 35 loses 140; if nobody exceeds 35, the kontra-er loses 140.
  - [ZIR]: a player who hasn't decided by their first card is deemed to have said kontra.

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
- `forehand_compulsory_three` = off [P] · on [TZS][B][MZT][ST]
- `forehand_speaks` = last [P 4p][PAL] · first [TZS][TN][B][MZT][P 3p]
- `hold_rights` = any senior [P][OS][TN §3.2] · forehand only [MZT][ST][PAL][B][TN §2.3] · none [SEL]
- `may_raise_after_auction` = on [P] · off [B][OS] · forehand only, when unbeaten [TZS]
- `valat_bid_only_over_berac` = off · on [TZS B1.17][MZT (over open beggar)]
- `three_bidder_loses_klop` = off · on [TN §3.2] (only when compulsory three is off)
- `contracts_enabled` = all of §5 · add `piccolo` (exactly 1 trick, 70) · add `open_solo_without` (100 [B]) · drop open beggar / colour valat / valat (3p)

**Compulsory klop**
- `compulsory_klop_triggers` = {score == 0, no-tarok redeal} · plus first hand [B] · plus score multiple of 500 · plus after misdeal

**King call**
- `called_king_in_talon` = win the rest of the talon with the king [P] · must take that group [B] · +5 points if the king never wins a trick [TN]
  - split into: `called_king_take_group` = optional [P][TN][OS] · compulsory in "two" only [B] · always compulsory [ST]
  - `called_king_lost_compensation` = none [P][B] · +5 card points to the declarer [TN]
- `four_kings_call` = must call own king · may call a trula card · "fourth king" without suit

**Discards**
- `discard_taroks` = face up [P] · only if nothing else, and show the hand [B][TN]

**Points**
- `win_threshold` = 36 · "35 + one card" (> 35)
- `diff_rounding` = 5 [P][B] · 1 [TZS][TN]
- `mond_penalty` = 20 · 21 (exact scoring)
- `mond_penalty_in_emperor_trick` = yes [P][OS][PAL][ZIR] · no [TZS][MZT]
- `mond_in_talon_with_called_king` = see §7.3 · [B]: always penalised if the mond is left, unless the king is also left
- `mondfang_by_partner` = the mond's player pays [P][PAL] · no penalty [ZIR] · both partners pay [TN]
- `mondfang_contracts` = normal + solo without [P][OS] · normal only [PAL]
- `announced_mondfang` = off · on (−42, can be kontra'd) [PAL]

**Play (negative contracts)**
- `negative_follow_suit_after_trump` = free, any led-suit card [P][OS] · must still exceed the highest led-suit card [PAL]
- `pagat_restriction_contracts` = {klop, beggar, open beggar} [P][OS] · plus colour valat and valat [B rule 9]
- `emperor_force_in_positive_contracts` = off · on [PAL]
- `klop_emperor_pagat` = forced [P][TZS][B][MZT][ZN][OS] · forbidden unless it is the last tarok [ZIR]

**Kontra**
- `kontra_levels` = 4 (kontra, re, sub, mort) · 3 (no mort) [SEL] · 2 [TN] · 5 (+ hirškontra)
- `kontra_on_silent` (as `silent_bonus_multiplier`) = 1, silent bonuses unaffected [TN] · the game's kontra multiplier [B]. [TZS] is silent (§7.5).
- `rekontra_by` = either declarer-side player [P] · declarer only [B][MZT][ST]
- `same_player_kontra_and_sub` = allowed · forbidden [ZIR]
- `kontra_on_trula_kings` = yes · no [PAL]
- `valat_kontra` = a separate item [P] · uses the game's kontra [PAL]
- `kontra_settlement` = symmetric [P][B] · caller pays [TN] · compensation for the other defender [TZS B1.21–22]
- `kontra_three_restriction` = off · on [SEL]
- `grouped_kontra` = off · on [SEL]

**Partner and radelc**
- `partner_share` = equal [P][B] · half [TN]
- `radelc_doubles_partner` = yes [P][TN] · no [B]
- `radelc_triggers` = {klop, beggar or higher, any valat} [P][PAL] · {klop, beggar, valat} [TZS] · {klop, high contracts} [TN] · {klop, any game worth ≥ 60, valat} [MZT] · {klop} [ST]
- `radelc_lifetime` = until the holder wins a declared hand [P] · the next hand only, win or lose [TZS]
- `radelc_on_renons` = the culprit's [P] · the declarer's [TZS] · only if the culprit is the declarer [TN]
- `radelc_pool` = per player · collective [ST]
- `radelc_end_penalty` = 100 [P] · 40 [PAL] · 0 [TZS]

**Ultimo bonuses**
- `silent_pagat_ultimo_scope` = whole side · holder only (on loss, or always)
- `valat_cancels_ultimo_obligation` = yes
- `pagat_ultimo_via_emperor` = yes [P][TN][B][OS] · no [TZS literal]
- `pagat_ultimo_win_condition` = the pagat wins the last trick · the pagat's side wins the last trick [ZIR]
- `silent_ultimo_attempt` = any play to the last trick [P][WIKI][TN][PAL] · scores only when won (not attested; a guard)
- `king_ultimo_own_king` = 10/20 as normal [P] · 25/50 "vleče sam" [TN]

**Valat**
- `silent_valat_value` = 250, replaces everything [P][TZS][B][WIKI] · a 50-point bonus added to the game [TN]
- `announced_valat_value` = 500 flat [P][TZS][B] · contract-dependent [TN] (3p: 250/300/350/500; 4p: 200/220/240 with the partner on half, solo 250/300/350/500)
- `silent_valat_kontra` = inherits the game's kontra [TZS B1.14][PAL] · none
- `defender_valat` = scored as a valat against the declarer side [WIKI][OS][PAL] · plain game scoring (not attested; a guard)
- `failed_announced_valat` = −500 replaces the game [PAL] · −500 added to the game score

**Klop**
- `klop_scoring` = [P] (±70 / −points) · [TZS] (≥ 35 → −70) · [B] (+70 for taking every trick)
  - split into: `klop_full_threshold` = > 35 [P][B][OS][PAL][MZT] · ≥ 35 [TZS][TN]
  - `klop_full_score` = −70 · −35 [MZT][ST]
  - `klop_empty_score` = +70 [P][TN][OS][PAL] · 0 [B] · none [TZS] · +35 [MZT] · +10 [ST]
  - `klop_empty_requires_nobody_full` = no [P][TN] · yes [MZT]
  - `klop_others_score_when_decided` = 0 [P][TN][B][OS][PAL] · −points [TZS]
  - `klop_valat_bonus` = off · +70 [B]
  - `klop_rounding` = 5 [P][B] · exact [TZS][TN][OS][PAL]
  - `radelc_in_klop` = per player, cancel on +70 [P][B] · ignored [TZS][TN][PAL]
- `klop_talon` = vitamins in tricks 1–6 · 2 cards each before play, 3p [ZIR]
- `klop_kontra` = off · [B]/[PAL] semantics · [TZS] · [TN] · [P] (§10). Never in compulsory klop [B].
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
- **Learn from the open-source engines' bugs.** [OS] and [PAL] both apply the emperor force before follow-suit (§8.3.4). [OS] scores pagat ultimo without checking that the pagat won, and treats it and king ultimo as mutually exclusive (§8.8). Write tests for exactly these cases.
- **Per-player ledger.** Under the [TN] and [TZS] kontra settlements and [TZS] B1.21, players on the same side write different amounts. Don't store only a "declarer side score".
- **Early termination** ([OS]): the result is fixed once a beggar declarer wins a trick, or a (colour) valat declarer loses one. Make stopping an option. Claims (§11) and some bonus rules still need the remaining tricks.
- **Move legality must never depend on the engine's knowledge of the hidden sides** in [4p]. Must-beat, the pagat rules and the emperor trick are per-player rules.

---

## 15. Open questions — default resolutions

No source settles these. Each one is decided below so the engine has a definite behaviour. Every decision is a configurable flag, so a house rule can override it later.

How each default was chosen, in order:
1. Follow the majority of written sources.
2. Otherwise keep the rule consistent with the rest of this document.
3. Otherwise copy what an existing engine ([PAL], [OS]) does.

Each item gives the question, the **default**, and the reason.

**Bidding**
- **Holding in [TZS]** (B1.9 says only "zviša"). **Default:** the `tzs` preset uses `hold_rights = forehand_only`. *Why:* [MZT], [ST] and [PAL] all give forehand the hold, and nothing in [TZS] forbids it explicitly.

**Bonuses and kontra**
- **[TZS] "kot edinim tarokom"** (B1.18): does a pagat that wins the last trick via the emperor trick count as pagat ultimo? **Default:** yes. *Why:* [P], [B] and [TN] state this exception explicitly. B1.18 reads as describing the normal case, not excluding the emperor case.
- **[TZS] B1.22 compensation bonus**, exact formula at rekontra and above. **Default:** generalise the stated principle at every level: bonus = (the non-kontra-ing player's result with the kontra chain) − (their result with no kontra). *Why:* this is literally what B1.22 says, and it applies at any level.
- **[4p] Zarufan or own-king declarer announcing king ultimo.** **Default:** allowed; the declarer is the holder of the called king's side. *Why:* the [P] restriction exists to stop the *declarer* from announcing on behalf of an unknown partner. When the declarer holds or takes the king themselves, that reason disappears.
- **[4p] Hidden partner saying rekontra before revealing.** **Default:** allowed. Saying it reveals them, and that is the player's choice. *Why:* [P] says "either member of the declarer's team". Nothing forbids self-revealing.
- **[TN] "kralj ultimo (vleče sam)" 25/50.** **Default:** it means the declarer holds the called king (called their own king, or took it from the talon). *Why:* that reading matches the half-share columns in [TN]'s partner table.

**Valat**
- **Failed announced valat.** **Default:** −500 *replaces* the game and all bonuses. *Why:* consistent with "valat replaces all other scores" (§7.5), and [PAL] does the same.
- **Valat in solo without.** **Default:** contract result only (80 + difference rules as configured), no extra valat score. *Why:* high contracts score no bonuses (§5).
- **Defender valat in [4p].** **Default:** the declarer and partner each write −250 (announced −500), and the defenders write nothing. *Why:* direct consequence of partner solidarity (§9).

**Klop and radelci**
- **[TZS] does klop "use up" a radelc gained earlier** (B1.25 vs B2.5)? **Default:** no. A radelc is consumed only by a hand the radelc-holder declares and wins. *Why:* [P], [TN] and [B] all tie cancellation to winning a declared game. The other reading would make klops silently delete radelci.
- **[TZS] mondfang in klop.** **Default:** no penalty in klop. *Why:* every other source excludes klop. B1.29 lists situations where *other players* write scores, not penalty triggers.
- **[B] rule 4 "Klopa pišemo v radelcih".** **Default:** klop *grants* radelci; klop scores are not doubled by them. *Why:* matches [TZS] B2.5 and [TN].
- **[TN] 3+1 klop:** how does the resting player get cards? **Default:** not supported. In a 3+1 table, klop is played by the three active players only. *Why:* undocumented; revisit if 3+1 is ever needed.

**Play**
- **Must-beat after a tarok on a suit lead:** if you can follow suit but a tarok already tops the trick, must you still beat the highest card of the led suit? **Default:** yes, as [PAL] does. *Why:* it keeps the rule meaningful (you can't dump a high card under a tarok), and it is the only implemented precedent.
- **Beggar defenders and must-beat.** **Default:** the defenders are bound too. *Why:* every written source states must-beat for negative contracts as a whole. Releasing them is unsourced table lore.
- **[ST] beggar lead by the player left of the declarer.** **Default:** the declarer leads. *Why:* every other source agrees; [ST] is likely a typo.

**Talon**
- **[B] rule 8:** must the king and the mond be in the *same* group for "no −20 when the called king is also left in the talon"? **Default:** no; it's enough that both are anywhere in the untaken talon (only relevant in the `b` preset). *Why:* the literal text names no group condition.

**Contracts**
- **[B] colour valat "v eni barvi":** what does naming a suit change? **Default:** naming a suit is ignored; colour valat plays as in §8.6. *Why:* no source describes any rule change from the named suit.

> If someone who plays regularly disagrees with any default above, change the flag. These defaults are not claims about how the game "really" goes.
