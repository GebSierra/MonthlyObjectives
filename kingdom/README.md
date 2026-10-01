# KINGDOM: interactive figure

An animated, clickable version of the KINGDOM figure (seven lettered tiles, K-I-N-G-D-O-M, each with a hanging column of icons), with a legend and a quiz.

Everything is in one file: `index.html`. It has no external requests, no libraries, no fonts, and no build step. It also works when opened straight from disk.

## What it does

- **Explore:** tap a letter for the stage summary, or tap any icon to see what it means and to trace it through the other stages.
- **Legend:** all 14 icons with their names. Tap one to light up every place it appears.
- **Quiz:** Letters (7 questions), Full quiz (12 questions), and Put it in order.
- **Replay** runs the opening animation again.
- Deep links: `index.html#k` through `#m` open a stage, and `#quiz` opens the quiz.
- Light and dark mode follow the visitor's device. Motion is turned off for visitors who ask for reduced motion.

## Put it on a website

### Option A: upload the file and link to it

1. Upload `index.html` to your site (for example `https://yourchurch.org/kingdom/index.html`).
2. Link to it from any page or menu. To link straight to one stage, add `#k`, `#i`, `#n`, `#g`, `#d`, `#o`, or `#m`.

### Option B: embed it in a page with an iframe

```html
<iframe id="kingdom" src="/kingdom/index.html" title="God's KINGDOM Plan"
        style="width:100%; border:0; min-height:900px" loading="lazy"></iframe>
```

The page tells its host how tall it is, so the frame can grow to fit and avoid inner scrollbars. Add this small listener on the host page (after the iframe):

```html
<script>
  window.addEventListener("message", function (e) {
    if (e.data && e.data.kingdomHeight) {
      document.getElementById("kingdom").style.height = e.data.kingdomHeight + "px";
    }
  });
</script>
```

If you would rather keep it locked down, replace `"*"` in the `postMessage` call near the bottom of `index.html` with your site's address.

It looks right in a frame from 360px wide and up. On a phone, the stage and icon panels open as a bottom sheet.

### Editing the content

All text lives in the `DATA` object at the top of the script in `index.html`: the stages, the legend names, the per-icon notes, and the quiz's fixed question. Edit the words there; no other code needs to change. In a stage's `icons` list, an `*` after a name (for example `"land*"`) draws that icon as a dotted outline (promised, not yet fulfilled).

## Attribution

The framework and stage titles come from Jason S. DeRouchie, *What the Old Testament Authors Really Cared About* (Kregel, 2013) and *Delighting in the Old Testament* (Crossway, 2024). The summaries on the page were written for this page, and the icons are original drawings made for it. The footer on the page carries this credit; please keep it. If you share or adapt the figure widely, check with the author and publishers about their wishes for reuse of the KINGDOM figure.
