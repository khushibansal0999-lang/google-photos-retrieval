# Deck theme — Google Material, extracted from PPt_design_google.pdf

Ten pages rendered and sampled. The text in that PDF is outlined, so no font names were
recoverable; everything below is measured from the vector fills or read off the renders.

## Colour

| Token | Hex | Use |
|---|---|---|
| Ink | `#202124` | primary text, and the black emphasis card |
| Grey | `#5F6368` | secondary text, section labels |
| Blue | `#1A73E8` | accent 1, CTA fill, selected state |
| Red | `#D93025` | accent 2, slide-number pill, warnings |
| Yellow | `#F9AB00` | accent 3 |
| Green | `#188038` | accent 4 |
| Amber | `#B45309` | readable text on a yellow tint |
| Blue tint | `#E8F0FE` | card fill |
| Red tint | `#FCE8E6` | card fill |
| Yellow tint | `#FEF7E0` | card fill |
| Green tint | `#E6F4EA` | card fill |
| Neutral tint | `#F8F9FA` | card fill |
| Border | `#DADCE0` | hairlines, image frames |

Background is white. Slide 7 of the source is a **full-bleed blue** slide with white cards
floating on it — reserved for the single pivotal moment.

## Type

Source looks like Google Sans, which Slides does not offer. Substitutes chosen because both
are reliably present in the Slides font picker:

- **Titles — Montserrat Bold, 21pt.** Geometric, double-storey `a`, closest available match.
- **Body — Roboto.** Google's own UI face; pairs naturally and is what the source body reads as.

Montserrat is wider than the previous Roboto Slab, so titles dropped 25pt → 21pt and the fit
table gained a `CPI_TITLE` entry.

## Motifs

1. **Numbered pill + section label**, top-left: a coloured rounded pill with the slide number
   in white, then the section name in grey. Yellow pills take ink text, not white.
2. **Four Google dots**, top-right, in blue/red/yellow/green order.
3. **Card sequences cycle** blue → red → yellow → green → **black**, each with a solid
   numbered circle, `→` between them. Applied to the two true sequences: the discovery-engine
   pipeline and the impact-sizing chain. Comparison cards keep semantic colour instead
   (selected = blue, warning = red) so the cycle never overrides meaning.
4. **Big stats** with a coloured left rule.
5. **Solid blue CTA button** with white text.

## Vertical rhythm

- badge `y=0.20`, height `0.28`
- title `y=0.50`, height `0.74`
- content from `y≈1.28`

This was re-cut specifically so the badge fits above content that was already laid out; no
slide needed its body moved.

## Screenshots on a white theme

The four Google Photos crops are dark-UI. On white they read as heavy blocks, so each sits in
a `#DADCE0` hairline frame to register as a screenshot rather than a design element.

## Type scale (NextLeap 14pt floor)

The brief sets a hard minimum of 14pt. `lib.py` enforces it: `box()` asserts on
any run below `FLOOR`, so a slide that breaks the rule cannot be generated.

| Token | Size | Used for |
|---|---|---|
| `FLOOR` | 14pt | body, captions, footnotes, section labels, badge number |
| `SUB`   | 16pt | card headers, inline labels |
| `LEAD`  | 20pt | card titles that must outrank SUB |
| `TITLE` | 26pt | slide title, one line only |
| `STAT`  | 30pt | the big numbers |

Vertical rhythm: badge y=0.14 (h 0.34), title y=0.46 (h 0.60), content from 1.15,
bottom margin 0.6.

### What the floor costs

At 14pt a full-width box holds ~114 characters a line; a three-across card holds
~32; a four-across card ~22 and a five-across ~17, which is why any row wider
than three columns had to be re-laid out rather than merely re-sized. Slide
capacity fell by roughly 40%, so copy was cut rather than shrunk. `fit()`
measures by paragraph, not by styled run, so inline bold labels no longer read
as false overflows.
