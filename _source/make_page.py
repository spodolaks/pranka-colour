#!/usr/bin/env python3
"""Generate the static portfolio page HTML (v2 - colourist-led)."""
import json

M = json.load(open("/home/claude/site/manifest2.json"))
DIM = {d["n"]: d for d in M}

# n: (kicker, note, [readouts])
ITEM = {
# --- Masks project -----------------------------------------------------------
52: ("Fox mask on the meadow, uncropped",
     "Almost the same frame in and out, so the colour is the whole change. Summer green pulled out of "
     "the grass and the far slope, the exposure taken down about a stop and a half, and the white of "
     "the mask and the swimwear held up so the figure survives it.",
     ["3:2 \u2192 1.42:1", "b* +6.8 \u2192 +1.9", "chroma \u221262%"]),
67: ("Snowfield above the treeline",
     "Colour was doing nothing here - green moss on grey rock under white snow. In mono the rock reads as "
     "mass and the figure finally has somewhere to stand. The recrop moves her off centre and hands the "
     "diagonal to the snowfield.",
     ["3:2 → 16:10", "converted to mono", "contrast +29%"]),
# --- The Endless Search ------------------------------------------------------
11: ("Boulder and typewriter, same frame",
     "The reference frame the rest of the set was built from, and the clearest look at what the grade "
     "does on its own: summer green pulled almost entirely out, the whole scene taken down to dusk, and "
     "the figure and the paper held up so they survive it.",
     ["no crop", "b* +9.9 \u2192 +1.4", "chroma \u221263%"]),
12: ("Forest, flat daylight in",
     "Shot at midday for a set that had to end up near-nocturnal. Exposure pulled right down, green taken "
     "almost out, and the figure held up with local dodging so she does not go with the rest of it.",
     ["3:2 → 5:4", "b* +13.8 → +0.7", "chroma −75%"]),
15: ("River crossing, cold grade",
     "Same set, opposite temperature. Summer green taken out of the water and the bank, the whole frame "
     "pushed cold, and the skin kept just warm enough to stay separate from it.",
     ["b* +8.3 → −6.1", "chroma −32%", "contrast +8%"]),
# --- Colour casts ------------------------------------------------------------
100: ("Sea stacks, flat light",
      "The whole stretch of coast came back magenta - not a colour choice, a tint bias in the raws. "
      "Corrected to neutral and then matched across every frame from that shoot, so the set can sit in "
      "one gallery without one picture looking like a different day.",
      ["a* +8.1 → −0.2", "chroma −66%", "contrast +12%"]),
99:  ("Painted houses, coastal",
      "Painted houses are the whole subject, so the cast had to come off without taking the paint with it. "
      "Neutral sky and grass, saturation held only where the buildings are.",
      ["3:2 → 16:10", "a* +4.7 → −2.9", "chroma −47%"]),
45:  ("Spring snow",
      "Snow is the hardest surface to white-balance: it takes the cast and shows it everywhere at once. "
      "Corrected against the snow, then the rock wall warmed back by hand so the frame keeps two "
      "temperatures instead of one.",
      ["a* +8.3 → +2.4", "chroma −60%"]),
109: ("Cracked flats",
      "Flat light on cracked mud with a warm-magenta cast over both. The correction is what lets the "
      "cracks read as texture instead of noise.",
      ["b* +7.9 → +2.8", "chroma −54%", "contrast +23%"]),
72:  ("North face, high cloud",
      "The strongest cast in the take - the snow was coming back lilac. Neutralised, recropped to vertical "
      "for the ridgeline, and the trees pulled down so they stop competing with the couloirs.",
      ["3:2 → 2:3", "a* +11.0 → +0.5", "chroma −78%"]),
# --- Land, weather, altitude -------------------------------------------------
75:  ("Storm over a valley town",
      "Handheld, high ISO, into a night storm. The colour was never going to survive - sodium street light "
      "below, violet cast above, lightning between them. Black and white lets the strike separate from "
      "the cloud instead of fighting the town for attention.",
      ["3:2 → 1:1", "converted to mono", "L̄ 28 → 16"]),
3:   ("Volcano above a hill town",
      "Midday haze had flattened mountain, town and sky into one plane. Dehaze plus a split tone puts "
      "them back at three distances; the crop drops a bright edge that was pulling the eye out of frame.",
      ["3:2 → 16:10", "b* −5.8 → −2.2"]),
103: ("Aerial, glacial water",
      "Drone frames carry their own problems: low contrast through the air column, a colour shift with "
      "altitude, and a horizon that is never quite where you left it. Straightened, cropped panoramic, "
      "and the water separated from the rock on colour rather than saturation.",
      ["3:2 → 2:1", "b* −10.5 → −3.0", "chroma −59%"]),
104: ("Ridge under cloud",
      "A frame where colour was working against the picture - a lilac sky flattening a mountain that is "
      "entirely about form. Nearly all of it taken out, then the exposure dropped hard so the snow does "
      "the drawing.",
      ["a* +9.5 → −0.2", "chroma −78%", "L̄ 48 → 23"]),
40:  ("Lake and glacier, gear removed",
      "A camera bag and a second black case were lying in the grass at the bottom left. Both removed and "
      "the ground rebuilt underneath, then the blown sky recovered and the whole frame taken down so the "
      "snowfield stops burning out.",
      ["objects removed", "L̄ 79 → 67", "contrast +22%"]),
# --- People on location ------------------------------------------------------
47:  ("Lakeside, overcast",
      "Nothing but available light and most of it wrong. Cast off, subject lifted about half a stop "
      "against the water, background cooled so she comes forward without a cut-out.",
      ["a* +8.4 → −2.9", "chroma −36%", "contrast +5%"]),
23:  ("Sandstone cave",
      "The sandstone was bouncing warm light onto everything, costume included. The grade splits them "
      "again - warm wall, cool figure - which is the separation the frame needed and a selection would "
      "have faked.",
      ["a* +6.0 → +1.1", "chroma −49%", "contrast +11%"]),
18:  ("Parking structure, night",
      "Mixed sodium and fluorescent, nothing neutral in the frame to balance against. Balanced on the "
      "white garment instead, then the concrete cooled until the two light sources agree.",
      ["a* +3.8 → −4.0", "L̄ 25 → 31"]),
96:  ("Close portrait, flowers",
      "Colour work only. The wood and the hair were the same orange; pulling them apart on the red "
      "channel is what puts the face in front of the background.",
      ["3:2 → 4:3", "a* +20.4 → +7.8", "chroma −51%"]),
6:   ("Coast, midday sun",
      "Blown sky, blocked rocks, about one stop of usable range between them. Highlight and shadow "
      "recovery first, then a crop to vertical because the horizon was the least interesting thing in "
      "the picture.",
      ["2:3 → 4:5", "contrast +41%"]),
54: ("Lake edge, paper ears",
     "Shot into the light with a white paper prop, white swimwear and a bright lake behind - every "
     "highlight on the edge of clipping. Recovered first, then the whole frame taken down more than two "
     "stops and recropped to vertical, with the paper held as the only clean white left.",
     ["3:2 \u2192 2:3", "L\u0304 42 \u2192 20", "chroma \u221237%"]),
56: ("Boulder in the pines",
     "Midday sun on green scrub, which is the worst light this series could have had. Green stripped "
     "almost out, exposure down nearly three stops, and the figure recovered back out of the shadow it "
     "would otherwise have fallen into.",
     ["3:2 \u2192 2:3", "L\u0304 41 \u2192 12", "chroma \u221266%"]),
59: ("Snowmelt, running water",
     "Snow, whitewater and a white mask in one frame - three different whites, all of them blown. Each "
     "recovered separately so they stay distinguishable, then the rock dropped to hold them apart.",
     ["3:2 \u2192 5:3", "L\u0304 67 \u2192 29", "chroma \u221240%"]),
65: ("Boulder field, wide",
     "Colour taken almost entirely out and the contrast pushed instead, so the frame reads as rock "
     "against snow. Cropped wide because the scale of the boulders is the story and the figure is "
     "supposed to be small in it.",
     ["3:2 \u2192 2:1", "chroma \u221283%", "contrast +32%"]),
69: ("Meadow, storm light",
     "Sun on the grass, storm on the ridge behind - two light sources pulling in opposite directions. "
     "The meadow is graded down to match the sky rather than the other way round, and the crop drops "
     "the horizon so the cloud does the work.",
     ["3:2 \u2192 2:3", "L\u0304 59 \u2192 27", "chroma \u221266%"]),
9:  ("Hillside at golden hour, uncropped",
     "The second frame in the set that needed no crop at all, which makes it the other clean look at "
     "the grade on its own. Warmth pulled back out of the grass, the whole frame taken down, and the "
     "figure and the typewriter kept readable in what is left.",
     ["no crop", "b* +10.3 \u2192 +5.2", "chroma \u221243%"]),
8:  ("Roadside, black dress",
     "Same set, opposite problem: a bright overcast sky with nothing in it. Recovered and cooled, the "
     "bank warmed slightly against it, and the crop tightened to 4:3 so the sky stops taking half "
     "the picture.",
     ["3:2 \u2192 4:3", "b* +5.8 \u2192 \u22121.2", "chroma \u221237%"]),
94: ("Black sand, breaking wave, uncropped",
     "Straight out of the camera with the blue cast the whole trip came back with. Corrected to "
     "neutral, the spray recovered, and the sand taken down until the cloak and the white water are "
     "the only two things left with any brightness.",
     ["no crop", "a* +8.8 \u2192 \u22124.1", "chroma \u221249%"]),
92: ("Moss and meltwater, second person removed",
     "There was a crew member standing at the right of the frame in a black t-shirt and jeans. Removed, "
     "and the rock and moss rebuilt behind where he was standing. After that the green is lifted on its "
     "own channel so the moss carries the frame and the dress stays a different green from it.",
     ["person removed", "a* +5.2 \u2192 \u22129.9", "chroma +36%"]),
89: ("Lava field, converted",
     "Strong magenta over sand that had almost no colour in it to begin with - so the honest answer was "
     "to take colour out of the decision entirely. Converted, recropped wider, and the dress left as "
     "the only true black in the frame.",
     ["3:2 \u2192 5:3", "a* +10.7 \u2192 \u22120.5", "converted to mono"]),
21: ("Rocks and surf, uncropped",
     "Nothing moved, nothing cropped - the frame was already right. Blue pulled out of the rock, the "
     "surf held back from clipping, and the subject warmed about half a stop so she separates from a "
     "background that is the same tonal range as she is.",
     ["no crop", "a* +0.5 \u2192 \u22121.0", "chroma \u221229%"]),
24: ("City at night, long exposure",
     "Sodium street light over everything, which on a night frame means the whole picture is one colour. "
     "Balanced back, the traffic trails left warm on purpose, and the buildings dropped so the roads "
     "are what the eye follows.",
     ["no crop", "b* +12.9 \u2192 +3.3", "chroma \u221237%"]),
25: ("Valley wall from above",
     "About one stop of usable contrast in the whole original. Local contrast added across the slope "
     "rather than a global curve, which is what separates the fields, the scree and the rock face into "
     "three readable things instead of one grey mass.",
     ["no crop", "L\u0304 28 \u2192 19", "contrast +12%"]),
27: ("Sea cliff, cropped vertical",
     "A colour decision and a crop decision in the same frame. The blue is taken almost fully out of "
     "the water so the cliff face reads as rock, and the frame is cut to 4:5 so the drop is the subject "
     "instead of the bay.",
     ["3:2 \u2192 4:5", "b* \u22127.8 \u2192 \u22121.6", "chroma \u221253%"]),
50: ("Rocks, riding coat",
     "The strongest magenta cast in this part of the take and the easiest to see it go: the stone comes "
     "back grey, the white trousers come back white, and the contrast lift is what gives the rock its "
     "texture again.",
     ["no crop", "a* +10.2 \u2192 \u22121.7", "contrast +25%"]),
71: ("Town from above, dusk",
     "Drone frame at the end of the light, flat and murky. Red roofs kept as the only saturated thing, "
     "everything else cooled and dropped, and enough local contrast added that the streets read from "
     "that height.",
     ["no crop", "contrast +25%", "a* +12.1 \u2192 +8.4"]),
73: ("Pass road into cloud",
     "The cast was doing the most damage here because the whole frame is cloud, and cloud has nowhere "
     "to hide a tint. Neutralised, then the road held slightly brighter than the fog so there is still "
     "somewhere for the eye to go.",
     ["a* +7.3 \u2192 +0.3", "chroma \u221274%"]),
# --- Colour as the decision --------------------------------------------------
80:  ("Poppy field",
      "Selective colour, not a filter. The field goes back to green and grey; only the flowers she is "
      "holding keep their red, so the eye goes where the picture wants it.",
      ["chroma −67%", "contrast +25%"]),
46:  ("Wave, breaking",
      "Spray frozen at the moment it breaks. The cast came off the water and the sky went back to blue; "
      "the spray keeps its edges because the contrast was added locally, not across the frame.",
      ["a* +7.9 → −3.2", "chroma −42%", "contrast +8%"]),
106: ("Umbrella in the fog",
      "Snow coming down in flat white light, which leaves nothing in the frame with any edge to it. "
      "The magenta cast came off first, then the treeline and the pylons were pulled back in behind the "
      "fog, and the umbrella left as the brightest thing so the figure has something to stand against.",
      ["a* +7.9 \u2192 \u22121.0", "chroma \u221253%", "contrast +23%"]),
}

GRIDS = {
 "GRID_SEARCH": ("img/grid-search.jpg", 1600, 1162, "The full ten-frame set",
   "Shot across one summer day in changing light, finished as a single night. Nothing in here drifts "
   "from anything else in here - that is the deliverable."),
 "GRID_ICELAND": ("img/grid-iceland.jpg", 1600, 1590, "Eight frames from the trip",
   "Black sand, lava field, moss and meltwater, shot over several days in wildly different light and "
   "delivered as one body of work. A sample - the trip produced considerably more."),
 "GRID_MASKS": ("img/grid-masks.jpg", 1600, 1346, "Sixteen frames from the set",
   "A sample of the delivery, not the whole of it - the set ran to several times this many frames. "
   "What matters is not any one picture here but that no picture drifts from the others."),
}

CASES = {
 "CASE_SEARCH": ("Case one", "Narrative series: flat daylight in, one night out",
   "A ten-frame story shot at midday and delivered as a single nocturnal scene. The look is built once "
   "on a reference frame, then argued with image by image - green pulled almost out, exposure taken "
   "down, every figure dodged back up by hand so nobody disappears into the grade."),
 "CASE_ICELAND": ("Case two", "Editorial series: Iceland, one look across the whole trip",
   "Several days on volcanic coast, and the take came back with a blue-magenta cast over all of it. "
   "Corrected first, then graded as one body of work rather than as a set of individual pictures - "
   "which is why black sand, green moss and a lava field can sit next to each other without looking "
   "like three different jobs. One frame also lost a crew member who was standing in it."),
 "CASE_MASKS": ("Case three", "Conceptual fashion series: nineteen frames, one grade",
   "The hardest of the three. White paper masks and white swimwear in full mountain sun, so almost "
   "every frame came off the card with the highlights clipped: the recovery had to happen before any "
   "look could be applied. Then a crop per frame to carry the story, and a selective preset built for "
   "each mask so the paper stays paper-white while everything around it drops two or three stops. "
   "Doing that once is an edit. Doing it nineteen times and still having one series is the work. "
   "Delivered as full-resolution masters."),
}

SECTIONS = [
 ("01", "One look across a whole set",
  "This is the part that is worth paying for. A single frame graded well is a nice picture; forty frames "
  "graded <em>identically</em> is a deliverable - and it is where most cheap editing falls apart, because "
  "running one preset over a take is not the same thing as matching it. Three projects below. Each opens "
  "with an uncropped frame on a slider, so the grade is the only thing that changes, then frames where "
  "the recrop is part of the work, then the contact sheet.",
  ["CASE_SEARCH", 11, 9, 12, 15, 8, "GRID_SEARCH",
   "CASE_ICELAND", 94, 92, 89, "GRID_ICELAND",
   "CASE_MASKS", 52, 54, 56, 59, 65, 69, "GRID_MASKS"]),

 ("02", "Before and after",
  "Four frames, four different problems. Drag the handle - the file on the left is what came out of the "
  "camera, the file on the right is what the client published. Everything on this page is my own work, "
  "and the readouts under each pair are measured off the files rather than described.",
  [("WIDE", 47), 100, 40, 23]),

 ("03", "Colour casts and mixed light",
  "The most common thing a full take comes back with: a tint bias over every single raw, or two light "
  "sources that refuse to agree. On one frame it is two minutes of work. Across a hundred it is the "
  "whole job, because the correction has to be the <em>same</em> correction or the set stops looking "
  "like one set. <span class=\"mono\">a*</span> below is the green-magenta axis, which is what a cast "
  "actually is.",
  [50, 99, 45, 73, 109, 72, 18]),

 ("04", "Portraits on location",
  "Available light, no studio, no strobes. Subjects are separated from their backgrounds with exposure "
  "and colour rather than selections - slower to do, and much harder for anyone to spot afterwards. "
  "No beauty or skin retouching: that is a different craft.",
  [21, 106, 96, 6]),

 ("05", "Landscape, travel and drone",
  "Flat, hazy or badly-lit originals brought back to something publishable - and, where something did "
  "not belong in the frame, taken out of it. None of these could be reshot.",
  [75, 3, 71, 103, 24, 25, 104, 40] if False else [75, 3, 71, 103, 24, 25, 104]),

 ("06", "Colour as the decision",
  "Frames where the edit was a decision rather than a repair: convert or keep, saturate or strip, crop "
  "tight or leave the room. Each of these could have gone the other way, and choosing is the service.",
  [67, 27, 80, 46]),
]


def cmp_block(n, wide=False):
    d = DIM[n]
    kicker, note, reads = ITEM[n]
    reads_html = "".join(f"<li>{r}</li>" for r in reads)
    if d["mode"] == "slider":
        w, h = d["w"], d["h"]
        media = f"""      <div class="cmp slider" style="aspect-ratio:{w}/{h}">
        <img src="img/p{n}-b.jpg" width="{w}" height="{h}" alt="{kicker}, before" loading="lazy" decoding="async">
        <div class="rev"><img src="img/p{n}-a.jpg" width="{w}" height="{h}" alt="{kicker}, after" loading="lazy" decoding="async"></div>
        <span class="bar" aria-hidden="true"><span class="grip"></span></span>
        <span class="tag l" aria-hidden="true">Before</span>
        <span class="tag r" aria-hidden="true">After</span>
        <input type="range" min="0" max="100" value="52" id="sl{n}" aria-label="Reveal the graded version of {kicker}">
      </div>"""
    else:
        media = f"""      <div class="cmp duo">
        <figure><img src="img/p{n}-b.jpg" width="{d['w']}" height="{d['h']}" alt="{kicker}, before" loading="lazy" decoding="async"><figcaption>Before</figcaption></figure>
        <figure><img src="img/p{n}-a.jpg" width="{d['w2']}" height="{d['h2']}" alt="{kicker}, after" loading="lazy" decoding="async"><figcaption>After</figcaption></figure>
      </div>"""
    cls = "work wide" if wide else "work"
    return f"""    <article class="{cls}">
{media}
      <div class="meta">
        <h3>{kicker}</h3>
        <ul class="reads">{reads_html}</ul>
        <p>{note}</p>
      </div>
    </article>"""


def grid_block(key):
    src, w, h, kicker, note = GRIDS[key]
    return f"""    <article class="work wide">
      <div class="cmp solo">
        <img src="{src}" width="{w}" height="{h}" alt="{kicker}" loading="lazy" decoding="async">
      </div>
      <div class="meta">
        <h3>{kicker}</h3>
        <p>{note}</p>
      </div>
    </article>"""


def case_block(key):
    tag, title, note = CASES[key]
    return f"""    <div class="casehead">
      <span class="tagline">{tag}</span>
      <h3>{title}</h3>
      <p>{note}</p>
    </div>"""


def render(item):
    if isinstance(item, tuple):
        return cmp_block(item[1], wide=True)
    if isinstance(item, str):
        return case_block(item) if item.startswith("CASE") else grid_block(item)
    return cmp_block(item)


body = []
for num, title, intro, items in SECTIONS:
    blocks = "\n".join(render(i) for i in items)
    body.append(f"""  <section class="chapter" id="s{num}">
    <header class="chead">
      <span class="idx">\u00a7{num}</span>
      <h2>{title}</h2>
      <p class="intro">{intro}</p>
    </header>
{blocks}
  </section>""")

NAV = "".join(f'<a href="#s{n}">{n} &middot; {t}</a>' for n, t, _, _ in SECTIONS)
shell = open("/home/claude/page_shell.html", encoding="utf-8").read()
out = shell.replace("<!--SECTIONS-->", "\n".join(body)).replace("<!--NAV-->", NAV)
open("/home/claude/site/index.html", "w", encoding="utf-8").write(out)
print("written", len(out), "bytes")
