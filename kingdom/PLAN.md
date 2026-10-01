# KINGDOM: Interactive Build Plan

Goal: turn DeRouchie's KINGDOM figure (seven lettered tiles with hanging columns of icons) into an animated, clickable, quiz-ready page that can be dropped onto any website.

## 1. Deliverables

| File | Purpose |
|---|---|
| `kingdom/index.html` | The whole thing. One self-contained file: inline CSS, inline JS, inline SVG icons. No external requests, no build step, no libraries. |
| `kingdom/README.md` | How to put it on a website: (a) upload the file and link to it, (b) iframe snippet, (c) note on attribution. |

Hard rules:
- Vanilla HTML/CSS/JS only. No frameworks, no CDNs, no web fonts. Must work opened straight from disk (`file://`).
- All content lives in one `DATA` object at the top of the script so it is easy to edit later.
- Use the content in section 5 **verbatim**. Do not invent new theology, verses, or quotes. If something seems missing, leave it out and report it.
- Icons are **original SVG drawings** (see section 4). Do not embed or trace the uploaded images.

## 2. Look and feel

Match the source figure closely, then add polish.

- Primary blue `--blue: #0B6FAE`. Darker hover `--blue-deep: #085A8E`. Icons and letters white on blue.
- Page background white (`--bg: #FFFFFF`), ink `#1A2230`, muted `#5B6575`, soft panel `#F2F7FB`.
- Font stack: `"Helvetica Neue", Helvetica, Arial, system-ui, sans-serif`. Letters bold, ~700.
- Layout: a 7-column CSS grid. Each column = a rounded-square **letter tile** on top and, under a small gap, a **pill-shaped column** (border-radius = half its width) holding that stage's icons stacked vertically, evenly spaced.
- Column lengths differ, exactly as in the figure (K 4 icons, I 4, N 5, G 4, D 2, O 4, M 6). This ragged "hanging banner" shape is the visual signature. Keep it.
- Fluid sizing: column width `clamp(40px, 12vw, 130px)`; icons scale with it (~70% of column width). Must fit with no horizontal scroll at 360px wide, with a 16px side gutter. At phone width, the letter tiles and icons simply shrink.
- Dark mode: support `prefers-color-scheme: dark` (bg `#0E1520`, ink `#E6EDF5`, panel `#162231`; blue columns stay blue but slightly brighter `#1A82C4`).
- Above the figure: title "God's KINGDOM Plan" and one line: "Seven stages of the story of God's glory in Christ. Tap a letter or an icon to learn more."
- A small toolbar (pill buttons): **Explore** (default) · **Legend** · **Quiz** · **Replay** (re-runs the intro animation).

## 3. Behavior

### 3.1 Intro animation (on load and on Replay)
1. Letter tiles drop in left to right (translateY -30px → 0, opacity 0 → 1), 70ms stagger, 420ms each, ease-out-back.
2. Each column then "unrolls" downward from its tile (animate `clip-path: inset(0 0 100% 0 round …)` → `inset(0 0 0 0 round …)` or a scaleY from top), 600ms, staggered 90ms by column.
3. Icons pop in top to bottom inside each column (scale 0.6 → 1, opacity 0 → 1), 60ms stagger.
4. Total under ~2.5s. Clicking anything during the intro finishes it instantly.
5. `prefers-reduced-motion: reduce` → no motion, everything shown at once; panels fade only.

### 3.2 Hover and focus
- Every letter tile and every icon is a real `<button>` with an `aria-label` (e.g. "K: Kickoff and Rebellion", "Fall, sin, rebellion, in stage N").
- Hover/focus: icon lifts slightly (scale 1.12) and a small tooltip shows the icon name. Letter tile darkens to `--blue-deep`.
- Visible focus ring (3px, offset, yellow `#FFC94D` so it shows on blue).

### 3.3 Click a letter → Stage panel
- Opens a panel. Desktop (≥ 900px): slides in from the right, 420px wide, figure stays visible and the chosen column is highlighted (others dim to 35% opacity). Mobile: bottom sheet, up to 80% of viewport height, scrollable.
- Panel shows: big letter, stage number ("Stage 3 of 7"), title, era line, dates, covenant (if any), the summary paragraphs, key texts list, and a row of that column's icons (each clickable, opens the icon view below).
- Prev / Next buttons and Left/Right arrow keys move between stages. Esc or the × button closes. Focus moves into the panel on open and back to the trigger on close. Click on backdrop (mobile) closes.

### 3.4 Click an icon → Icon panel (same panel component)
- Shows: icon large, its name, a badge **Promised** (dotted icons) or **Fulfilled / Present** (solid), which stage it sits in, and the stage-specific note from section 5.
- "Trace this thread" section: chips for every stage where this icon appears (e.g. Fall appears in K, N, G, D). Clicking a chip opens that occurrence. While the icon panel is open, all occurrences of that icon on the board glow (white outer ring) and everything else dims.
- Link: "Read about Stage X" → opens the stage panel.

### 3.5 Legend view
- A grid of the 14 icons with their names (two columns desktop, one mobile), in the legend order from section 5.
- A short key at top: "Dotted outline = promised, not yet fulfilled. Solid = fulfilled or present." Show the dotted and solid stars side by side.
- Clicking a legend item highlights every occurrence on the board (scroll the board into view) and opens its first occurrence in the icon panel.

### 3.6 Quiz view
Replaces the figure area with a quiz card (the figure returns when you leave Quiz).

Start screen: three choices.
1. **Letters** (7 questions): "What does K stand for?" for each letter, shuffled.
2. **Full quiz** (12 questions): random mix from all question types below, no repeats.
3. **Put it in order**: tap the seven stage titles (shuffled) in the right order. Each correct tap locks the tile into place under its letter; a wrong tap shakes and counts as a miss. Show misses at the end.

Question types (multiple choice, 4 options, one correct, options shuffled; distractors drawn from the same field of other stages/icons):
- a. Letter → title: "What does N stand for?"
- b. Title → letter: "Which letter is 'Overlap of the Ages'?"
- c. Era → stage: "Which stage covers Exodus, Sinai, and wilderness?"
- d. Dates → stage: "Which stage is dated ca. 600–400 B.C.?"
- e. Icon → meaning: show the icon SVG large, "What does this image stand for?"
- f. First appearance: "In which stage does [icon name] first appear?" (answers in section 5.4)
- g. Sequence: "Which stage comes right after Government in the Promised Land?"
- h. Covenant → stage: "Which stage centers on the Mosaic covenant?" (only stages with a covenant)
- i. Fixed question: "In stage I, why are the stars, house, and compass drawn with dotted lines?" Correct: "They are promised, not yet fulfilled." Distractors: "They were destroyed in the flood." / "They belong to other nations." / "They are only symbols of heaven."

Feedback after each answer: correct option turns green with a check; a wrong pick turns red, the right one turns green. Show one short "Why" line (use the stage's era line or the icon's legend name, plus "Stage N: Title"). "Next" button (also Enter key). Progress bar and "Question 4 of 12". Keyboard: 1–4 pick an option.

End screen: score (e.g. "10 / 12"), a short message (12/12 "Perfect!"; ≥ 9 "Well done."; else "Keep going. Try again?"), a list of missed questions with the right answer, buttons **Try again** and **Back to the figure**. Store best scores per quiz type in `localStorage` (wrap every read/write in try/catch; the page must work if storage is blocked).

Small delights (keep them light): on a perfect score, the KINGDOM letters do a quick wave (each tile hops in sequence). Nothing else.

### 3.7 URL hash (deep links)
`#k` … `#m` opens that stage panel on load. `#quiz` opens quiz. Update the hash as panels open/close (use `history.replaceState`, not new history entries).

### 3.8 Embedding
- Page must look right inside an iframe of any width from 360px up. Use no `position: fixed` that breaks inside iframes, except the mobile bottom sheet, which is fine.
- When in an iframe, post its height to the parent: `parent.postMessage({kingdomHeight: document.documentElement.scrollHeight}, "*")` on load and resize (ResizeObserver). README gives the 6-line listener snippet for the host page.

### 3.9 Footer
Small muted text: "Framework and stage titles from Jason S. DeRouchie, *What the Old Testament Authors Really Cared About* (Kregel, 2013) and *Delighting in the Old Testament* (Crossway, 2024). Summaries written for this page. Scripture references are given for further reading."

## 4. Icons (inline SVG `<symbol>`s)

One `<svg>` sprite at the top of `<body>` with 14 `<symbol id="i-…" viewBox="0 0 100 100">`. Use with `<svg><use href="#i-…"/></svg>`. Fill `currentColor` (white on the board, blue in the legend and panels). Simple, bold, flat shapes in the spirit of the figure. Each must read clearly at 32px.

| id | Name | Drawing |
|---|---|---|
| `paradise` | Paradise enjoyed | Wide flat-topped umbrella tree (acacia): a lumpy cloud canopy on a thin curved trunk that forks into 2 branches. |
| `fall` | Fall, sin, rebellion | Apple core: top and bottom apple lobes with a narrow bitten waist, short stem on top. |
| `exile` | Exile; paradise lost | Thick ring with a diagonal bar from top-left to bottom-right (a "no" sign). |
| `flood` | Waters of judgment (flood) | Half-bowl (semicircle, flat side up) with 2 wavy lines across it and a small boxy ark sitting on top. |
| `patriarchs` | Patriarchs | Simple standing robed figure in profile, holding a staff, tall narrow silhouette. |
| `offspring` | Much offspring | 12 small five-point stars scattered in a loose cluster. |
| `land` | Land, home, rest | Low flat-roofed house: a long rectangle with a step down on the right and an arched doorway cut out on the left half. |
| `nations` | Blessing to all nations | Compass: circle with N, E, S, W letters and a diagonal needle (NW to SE). |
| `exodus` | Waters of judgment (exodus) | Half-bowl split down the middle into two halves pulled apart (parted sea), wavy lines on each half. |
| `law` | Giving of the law | Two round-topped tablets, side by side, the right one slightly lower and overlapping. |
| `atonement` | Penal substitutionary atonement | Lamb lying down, side view, small head with ear. |
| `kingdom` | Conquest; kingdom established | Hanging banner on a crossbar with a small crown in the upper half; bottom edge slanted; short pole tip below. |
| `christ` | Saving/atoning work of Christ | A cross with a small lying lamb in front of its base (reuse the lamb shape, scaled). |
| `fire` | Fires of judgment | Half-bowl with flames rising from its top edge. |

**Promised (dotted) variant:** in stage I, `offspring`, `land`, and `nations` are drawn as outlines with a dotted stroke instead of solid fill. Implement as a CSS class `.promised` that swaps fill for `fill: none; stroke: currentColor; stroke-width: 3; stroke-dasharray: 1 5; stroke-linecap: round`. Each symbol must therefore be built from shapes that look right both filled and as a dotted outline. (Compass: its circle and needle become dotted.) Test this specifically.

## 5. Content (use verbatim)

### 5.1 Stages

```js
stages: [
 { letter:"K", n:1, title:"Kickoff and Rebellion", era:"Creation, fall, and flood", dates:"ca. ? B.C.", testament:"Old Testament",
   covenant:"Adamic/Noahic",
   summary:[
    "God made humans to image him and told them to “fill the earth and subdue it” (Gen 1:28). But they listened to the serpent and rebelled (Gen 3:1–6). Because Adam acted as our covenant head, God counts all humanity as having sinned in him (Rom 5:12, 18–19).",
    "Before the curse fell, God promised a human deliverer who would crush the power of evil (Gen 3:15). Sin kept spreading, so God judged the world with a flood, yet he kept a remnant and renewed his covenant with creation (Gen 6:7–8, 18; 9:9–11). At Babel, people exalted themselves again, and God scattered them (Gen 11:1–9)."
   ],
   keyTexts:["Gen 1:28","Gen 3:1–6","Gen 3:15","Gen 6:7–8","Gen 9:9–11","Gen 11:1–9","Rom 5:12"],
   icons:["paradise","fall","exile","flood"] },

 { letter:"I", n:2, title:"Instrument of Blessing", era:"Patriarchs", dates:"ca. 2100–1850 B.C.", testament:"Old Testament",
   covenant:"Abrahamic",
   summary:[
    "After Babel, God chose Abraham as the one through whom he would reverse the curse. He told him to “go” to Canaan and to “be a blessing” (Gen 12:1–3). First Abraham would become a great nation. Then, through one royal offspring, God would bless some from all the families of the earth.",
    "Sarah was barren, but Abraham believed God’s promise, and God counted it as righteousness (Gen 11:30; 15:6). God swore to give the land to Abraham’s offspring and said the coming King would rise from Judah (Gen 15:17–18; 49:8–10). He even sent Joseph to Egypt to keep the family alive (Gen 50:20)."
   ],
   keyTexts:["Gen 12:1–3","Gen 15:6","Gen 15:17–18","Gen 22:17–18","Gen 49:8–10","Gen 50:20"],
   icons:["patriarchs","offspring*","land*","nations*"] },   // * = promised (dotted)

 { letter:"N", n:3, title:"Nation Redeemed and Commissioned", era:"Exodus, Sinai, and wilderness", dates:"ca. 1450–1400 B.C.", testament:"Old Testament",
   covenant:"Mosaic",
   summary:[
    "God kept his word and multiplied Israel in Egypt (Exod 1:7). For the sake of his name he struck Egypt with plagues and freed his people (Exod 9:15–16). At Sinai he gave the law so Israel would display his holiness among the nations (Exod 19:5–6), and he gave sacrifices so they could draw near (Lev 9:3–6).",
    "Yet most of the people were “rebellious” and “unbelieving” (Deut 9:23–24). Moses foretold exile, but also a day when God would bring them back, raise up a prophet like Moses, and change their hearts so they would love him (Deut 18:15–19; 30:3–6)."
   ],
   keyTexts:["Exod 1:7","Exod 19:5–6","Lev 9:3–6","Deut 9:23–24","Deut 18:15–19","Deut 30:6"],
   icons:["offspring","exodus","law","atonement","fall"] },

 { letter:"G", n:4, title:"Government in the Promised Land", era:"Conquest and kingdoms (united and divided)", dates:"ca. 1400–600 B.C.", testament:"Old Testament",
   covenant:"Davidic",
   summary:[
    "In the conquest, God kept every promise of the land (Josh 21:43–45). But without a faithful king, “everyone did what was right in his own eyes” (Judg 21:25). The people asked for a king to replace the Lord (1 Sam 8:7). They would not heed the prophets, so the kingdom split, and both north and south ended in exile (2 Kgs 17:6–23; 25:1–21).",
    "Even so, God promised David a son whose throne would last forever (2 Sam 7:12, 16). This Servant-King would be a light to the nations and, though innocent, would die in the place of sinners to “make many to be accounted righteous” (Isa 49:6; 53:5, 11)."
   ],
   keyTexts:["Josh 21:43–45","Judg 21:25","1 Sam 8:7","2 Sam 7:12–16","Isa 49:6","Isa 53:5–11"],
   icons:["kingdom","paradise","land","fall"] },

 { letter:"D", n:5, title:"Dispersion and Return", era:"Exile and initial restoration", dates:"ca. 600–400 B.C.", testament:"Old Testament",
   covenant:null,
   summary:[
    "God cast Israel from the land because they would not listen to his voice (2 Kgs 17:7; 2 Chr 36:16). From exile, Daniel pleaded for mercy (Dan 9:18–19). God promised a kingdom that would never be destroyed and “one like a son of man” whom all peoples would serve (Dan 2:44; 7:13–14).",
    "God kept the Jews from being wiped out (Esther) and brought some back to the land (Ezra–Nehemiah). They rebuilt the temple (Hag 1:8). But the promised Servant-King had not yet come, and the story still waited for its fulfillment."
   ],
   keyTexts:["2 Kgs 17:7","Dan 2:44","Dan 7:13–14","Dan 9:18–19","Hag 1:8","Mal 1:14"],
   icons:["exile","fall"] },

 { letter:"O", n:6, title:"Overlap of the Ages", era:"Christ’s work and the church age", dates:"ca. 4 B.C.–A.D. ?", testament:"New Testament",
   covenant:"New",
   summary:[
    "Jesus came first as the suffering Servant and will come again as the conquering King (Heb 9:28). So we live in an overlap: Christ has rescued us from “the present evil age” (Gal 1:4), and we already taste “the powers of the age to come” (Heb 6:5).",
    "In the fullness of time “God sent forth his Son” (Gal 4:4), the Lamb of God who takes away sin (John 1:29). By his life, death, and resurrection he began the new covenant (Luke 22:20). God counts our sin to Christ and Christ’s righteousness to us (2 Cor 5:21). Now the church makes disciples of all nations (Matt 28:18–20; Acts 1:8)."
   ],
   keyTexts:["Gal 4:4","John 1:29","Luke 22:20","2 Cor 5:21","1 Cor 15:3–5","Matt 28:18–20","Acts 1:8"],
   icons:["christ","kingdom","nations","offspring"] },

 { letter:"M", n:7, title:"Mission Accomplished", era:"Christ’s return and kingdom consummation", dates:"ca. A.D. ?–eternity", testament:"New Testament",
   covenant:null,
   summary:[
    "The King will return “on the clouds of heaven with power and great glory” (Matt 24:30). Only those who fear God and give him glory will escape his wrath on that day (2 Thess 1:9–10; Rev 14:7).",
    "A great multitude will cry, “Salvation belongs to our God … and to the Lamb!” (Rev 7:10). God’s glory will light his city (Rev 21:23), and his servants “will reign forever and ever” (Rev 22:5), fulfilling the first calling given in Eden (Gen 1:26–28). With John we pray, “Come, Lord Jesus!” (Rev 22:20)."
   ],
   keyTexts:["Matt 24:30","2 Thess 1:9–10","Rev 5:9–10","Rev 7:9–10","Rev 21:23","Rev 22:5","Rev 22:20"],
   icons:["kingdom","fire","nations","offspring","paradise","land"] }
]
```

Covenant display: show "Covenant in focus: Abrahamic" etc. Hide the line when `covenant` is null.

### 5.2 Legend (order and names)

```js
legend: [
 ["paradise","Paradise enjoyed"],
 ["fall","Fall, sin, rebellion"],
 ["exile","Exile; paradise lost"],
 ["flood","Waters of judgment (flood)"],
 ["patriarchs","Patriarchs"],
 ["offspring","Much offspring (promise-fulfillment)"],
 ["land","Land, home, rest (promise-fulfillment)"],
 ["nations","Blessing to all nations (promise-fulfillment)"],
 ["exodus","Waters of judgment (exodus)"],
 ["law","Giving of the law"],
 ["atonement","Penal substitutionary atonement"],
 ["kingdom","Conquest; kingdom established"],
 ["christ","Saving/atoning work of Christ"],
 ["fire","Fires of judgment"]
]
```

### 5.3 Icon notes, per stage (key = `letter:icon`)

```js
notes: {
 "K:paradise":"God made a good world and placed people in it to image him and rule it under him (Gen 1:26–28).",
 "K:fall":"Adam and Eve listened to the serpent and rebelled against God (Gen 3:1–6). All humanity fell in Adam (Rom 5:12).",
 "K:exile":"God sent them out of Eden and subjected the world to futility (Gen 3:16–19, 23; Rom 8:20). Yet he promised a deliverer (Gen 3:15).",
 "K:flood":"Sin kept spreading, so God judged the world by flood. He saved a remnant and renewed his covenant with creation (Gen 6:7–8; 9:9–11).",

 "I:patriarchs":"God chose Abraham, then Isaac and Jacob, as the family through whom he would bless the world (Gen 12:1–3).",
 "I:offspring":"Promised: Sarah was barren, yet God promised Abraham offspring like the stars (Gen 11:30; 15:5–6; 22:17).",
 "I:land":"Promised: God swore to give the land of Canaan to Abraham’s offspring (Gen 15:17–18; 17:8).",
 "I:nations":"Promised: through Abraham’s royal offspring, all the families of the earth would be blessed (Gen 12:3; 22:17–18).",

 "N:offspring":"Fulfilled: in Egypt, Israel grew from one family into a great people (Exod 1:7).",
 "N:exodus":"God judged Egypt and brought his people out through the sea, for the sake of his name (Exod 9:15–16; 14).",
 "N:law":"At Sinai God gave the law so Israel would be “a kingdom of priests and a holy nation” (Exod 19:5–6).",
 "N:atonement":"God gave sacrifices so a sinful people could live near a holy God (Lev 9:3–6). They point ahead to a greater substitute.",
 "N:fall":"Most of the people were “rebellious” and “unbelieving” (Deut 9:23–24). Moses foretold exile (Deut 4:25–29).",

 "G:kingdom":"Israel took the land, and later God promised David a son whose throne would last forever (Josh 21:43–45; 2 Sam 7:12, 16).",
 "G:paradise":"The land was a good land, a taste of Eden’s rest and plenty (Deut 8:7–10).",
 "G:land":"Fulfilled: “Not one word of all the good promises … had failed” (Josh 21:45).",
 "G:fall":"Kings and people turned from God. The kingdom split, and both halves fell into exile (1 Kgs 11:11–13; 2 Kgs 17; 25).",

 "D:exile":"Because they would not listen, God cast his people from the land (2 Kgs 17:7; 2 Chr 36:16).",
 "D:fall":"Some returned and rebuilt, but hearts were still unchanged, and the promised King had not yet come (Mal 1:6, 14).",

 "O:christ":"Jesus is the Lamb of God who takes away sin (John 1:29). By his death and resurrection he began the new covenant (Luke 22:20).",
 "O:kingdom":"Jesus proclaimed the kingdom of God (Luke 4:43). Risen, he holds all authority in heaven and on earth (Matt 28:18).",
 "O:nations":"Fulfilled now: the gospel is going from Jerusalem to the ends of the earth (Acts 1:8; Matt 28:19).",
 "O:offspring":"Fulfilled now: all who belong to Christ are Abraham’s offspring (Gal 3:29).",

 "M:kingdom":"The King will return “on the clouds of heaven with power and great glory” (Matt 24:30).",
 "M:fire":"Those who do not know God and do not obey the gospel will face eternal destruction (2 Thess 1:8–9).",
 "M:nations":"People from every nation, tribe, and language will stand before the Lamb (Rev 7:9).",
 "M:offspring":"A great multitude that no one can number, praising God and the Lamb (Rev 7:9–10).",
 "M:paradise":"Eden restored: the river of life and the tree of life in the city of God (Rev 22:1–2).",
 "M:land":"Our final home: God will dwell with his people in a new heaven and a new earth (Rev 21:1–3)."
}
```

### 5.4 First appearances (for quiz type f; compute from data, but must match)
paradise K · fall K · exile K · flood K · patriarchs I · offspring I · land I · nations I · exodus N · law N · atonement N · kingdom G · christ O · fire M

## 6. Code structure (inside `index.html`)

```
<style>   tokens on :root, dark-mode override, layout, board, panel, legend, quiz, animations, reduced-motion
<body>
  <svg sprite hidden>  14 symbols
  <header> title, subtitle, toolbar
  <main>
    <section id="board">     7 columns (generated by JS from DATA)
    <section id="legend" hidden>
    <section id="quiz" hidden>
  <aside id="panel" role="dialog" aria-modal="false" aria-labelledby="panel-title">   (stage + icon views)
  <footer>
<script>
  const DATA = {...}            // section 5
  renderBoard(), playIntro(), openStage(i), openIcon(letter, iconId), highlightIcon(id), clearHighlight()
  renderLegend()
  Quiz: buildQuestions(mode) → [{type, prompt, iconId?, options[], answerIndex, why}], renderQuestion(), answer(i), renderEnd()
  Order game: startOrder(), tapOrder(i)
  Hash routing, postMessage height, keyboard handling
```

Keep it readable: small named functions, no clever one-liners. Aim for roughly 900–1400 lines total. Comments only where a reader would ask "why?".

## 7. Verification (must do before reporting done)

Write a Playwright script in the scratchpad (Chromium is at `/opt/pw-browsers/chromium`; do not run `playwright install`). It must:

1. Load `kingdom/index.html` via `file://`. Collect console errors; fail on any.
2. Screenshot after intro at 1280×900 (light), 1280×900 (dark, `colorScheme: 'dark'`), and 390×844 (mobile). Also 360×740: assert `document.documentElement.scrollWidth <= 360`.
3. Click each of the 7 letters; assert the panel title matches the stage title; test ArrowRight moves K→I; Esc closes and focus returns.
4. Click the `fall` icon in column N; assert the note text matches `N:fall`; assert 4 chips (K, N, G, D) and that 4 board icons have the highlight class.
5. Legend: assert 14 items; screenshot it.
6. Quiz Letters: answer all 7 correctly by reading the correct option from the DOM; assert "7 / 7". Full quiz: answer all wrong; assert "0 / 12" and 12 missed items listed. Order game: tap in correct order; assert completion.
7. Load `#g`; assert stage G panel is open.
8. Reduced motion (`reducedMotion: 'reduce'`): assert all icons visible immediately (opacity 1) at t=0+100ms.
9. Screenshot a close-up of column I to check the dotted (promised) icons render as dotted outlines.

Then **look at every screenshot yourself** and fix anything ugly: icons that don't read, crowding, overflow, misaligned columns, dotted icons that look broken. Iterate until it looks like a polished version of the source figure. Save final screenshots to `kingdom/screenshots/` (desktop, dark, mobile, panel-open, legend, quiz) so the owner can preview.

## 8. Report back

List: files created, how each verification step went (with any failures stated plainly), anything in this plan you could not do or changed, and any content you think needs the owner's review.
