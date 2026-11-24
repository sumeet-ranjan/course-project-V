"""Plain words in the deliverable tables: replace the decision codes used while the work was decided (G1-G9, the review
rounds, "Step A/B/E") in the label columns of the deliverable CSVs with plain words. Run it last, after every builder
(src/40-63) and before the memo build: the builders still write the coded labels, this script rewrites them in place.
It is idempotent. Quote columns that hold document text are not touched. The decision log, with what each code meant,
is in HANDOVER.md.
"""
import os, re, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from common import OUT
DEL = OUT + "deliverables/"
SPECIFIC = [  # (old, new), applied first, in order
    ("(confirmed, G3)", "(confirmed)"), ("(closed at checkpoint 4)", "(closed)"), ("flags (checkpoint-5 review)", "flags"),
    ("(not a firm link, G4 R3)", "(not a firm link)"), ("(comparison; superseded at checkpoint 5)", "(comparison; replaced by the delivery test)"),
    ("(main cement result, checkpoint 5)", "(main cement result)"), ("(G5: the result; little power)", "(the result; little power)"),
    ("price evidence (corrected at G5)", "price evidence (corrected)"), ("(Step A, G7: confirmed, immaterial)", "(confirmed, immaterial)"),
    ("(Step A, G7: material hit)", "(material hit)"), ("B pack chemical belt (Step A)", "B pack chemical belt (breaks at the first step: no hit firm)"),
    ("(G7 R4 propagation measure)", "(propagation measure)"), ("the two delayed malls (G4 R4: ", "the two delayed malls ("),
    ("identification by the user (G4 R4)", "identification by the author"), ("(the user's reading, checkpoint-4 review)", "(the author's reading)"),
    ("checkpoint-5 review: flagged", "flagged"), ("footprint defined by sites (user, G2)", "footprint defined by sites (the author)"),
    ("within-zone contractor, material (G4; mechanism accepted at G5 on documents and quarterly numbers)", "within-zone contractor, material (mechanism accepted on documents and quarterly numbers)"),
    ("G5 result, kept as the comparison", "earlier market-level result, kept as the comparison"),
    ("candidate fallback weight for the NCR chain (decision G4)", "candidate fallback weight for the NCR chain (the author's decision)"),
    ("net of the 3 G2 specialty controls", "net of the 3 specialty controls"),
    ("contractor screened in Step B and found unlinked", "contractor screened for links and found unlinked"),
    ("supplier screened in Step B (outside the pack)", "supplier screened for links (outside the pack)"),
    ("see the two Step B tables", "see the two link-screening tables (research/realign/stepB_*.csv)"),
    ("see the Step B table", "see the link-screening table (research/realign/stepB_*.csv)"),
    ("context for NCR Step A (exposure of a hit firm)", "context for the NCR hit-firm search (exposure of a hit firm)"),
    ("pending Gujarat Step A", "pending the Gujarat hit-firm search"), ("unless Gujarat Step A", "unless the Gujarat hit-firm search"),
    ("Added at the user's request (G3).", "Added at the author's request."),
    ("(user, G3, 23 Nov 2026)", "(the author, 23 Nov 2026)"),
    ("G2 control firms", "control firms"), ("the G2 controls", "the controls"), ("G2 controls", "controls"),
]
REGEX = [  # generic clean-up, after the specific replacements
    (r"\s*\((?:decision )?G\d(?: R\d)?\)", ""),            # " (G4)", " (G7 R4)"
    (r"\bG\d(?: R\d)?:\s*", ""),                            # "G7: "
    (r"\((?:G\d(?: R\d)?);\s*", "("),                        # "(G4; ..."
    (r"\s*\(checkpoint[- ]\d(?: review)?\)", ""),            # " (checkpoint 5)", " (checkpoint-4 review)"
    (r"checkpoint[- ]\d review:\s*", ""),
    (r"\bStep [A-E]\b ?", ""),
    (r"\bthe user\b", "the author"), (r"\bThe user\b", "The author"),
    (r"\s{2,}", " "), (r"\(\s+", "("), (r"\s+\)", ")"), (r"\s+;", ";"),
]
DECIDED = re.compile(r"^(?:G\d (?:R\d )?)?\(?user, (\d+ \w+ \d{4})\)?$|^(\d+ \w+ \d{4}) \(G\d(?: R\d)?\)$")
def plain(t):
    if not isinstance(t, str) or not t: return t
    for a, b in SPECIFIC: t = t.replace(a, b)
    for a, b in REGEX: t = re.sub(a, b, t)
    return t.strip()
FILES = {"evidence_NCR.csv": ["node", "role", "status", "note", "quote"], "evidence_GJ.csv": ["node", "role", "status", "note", "quote"],
         "verified_links.csv": ["status", "status_reason", "decided", "read_mode", "notes"],
         "hit_register_NCR.csv": ["status", "grade"], "hit_register_GJ.csv": ["status", "grade"],
         "table2_dose_response.csv": ["panel", "link_status", "note"], "table3_placebo.csv": ["test", "note"], "table3_placebo_firms.csv": ["test", "flag"]}
SAFE_QUOTE = ("net of the 3 G2 specialty controls",)   # a quote column cell is changed only for these computed strings
for f, cols in FILES.items():
    p = DEL + f
    if not os.path.exists(p): continue
    d = pd.read_csv(p, dtype=str, keep_default_na=False)
    for c in [c for c in cols if c in d.columns]:
        if c == "quote":
            d[c] = [plain(v) if any(k in v for k in SAFE_QUOTE) else v for v in d[c]]
        elif c == "decided":
            d[c] = [("author, " + (m.group(1) or m.group(2))) if (m := DECIDED.match(v.strip())) else plain(v) for v in d[c]]
        else:
            d[c] = d[c].map(plain)
    d.to_csv(p, index=False)
    left = [c for c in cols if c in d.columns and c != "quote" and d[c].str.contains(r"\bG\d\b|checkpoint|\bStep [A-E]\b", regex=True).any()]
    print(f, "codes left in:", left or "none")
