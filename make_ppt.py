from pptx import Presentation
from pptx.util import Inches, Pt
import sys
DOMAIN = sys.argv[1] if len(sys.argv) > 1 else "tickettriage.vercel.app"
prs = Presentation(); prs.slide_width = Inches(13.33); prs.slide_height = Inches(7.5)
def add(i, title, lines):
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = title
    tf = s.placeholders[1].text_frame; tf.word_wrap = True
    for j, ln in enumerate(lines):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.text = ln; p.font.size = Pt(20); p.space_after = Pt(10)
add(0, "TicketTriage — Support Ticket Priority Classifier", ["An AI/ML project by Vikranth Reddy", "B.Tech CSE (AI & ML), 2nd Year — Woxsen University", "A model that reads a customer support ticket and tells you how urgent it is — critical, high, medium or low"])
add(1, "The Problem", ["Support teams get hundreds of tickets a day — outages, bugs, typos, feature requests", "Reading and sorting every ticket by hand is slow, and urgent tickets get buried", "A site-down ticket answered late costs customers and money", "Automatic triage puts the most urgent tickets first, every time"])
add(2, "The Solution — TicketTriage", ["Paste any support ticket into the browser demo", "A trained model returns the probability of each of the four priorities as bars", "The strongest priority is shown with a colour badge and a percentage", "Runs fully in the browser — no backend, no waiting"])
add(3, "Tech Stack", ["Python + scikit-learn: dataset and model training", "TF-IDF (word unigrams, sublinear TF, L2 normalisation) + multinomial logistic regression (C = 1.0)", "HTML, CSS and vanilla JavaScript for the interactive demo", "GitHub for source control, Vercel for free hosting"])
add(4, "Architecture", ["Dataset: 200 hand-written support tickets — 50 per priority, 685-word vocabulary", "Text -> tokens -> TF-IDF weights -> logistic regression (4 outputs) -> softmax -> model.json", "model.json ships with the site; JavaScript applies the same formula and a softmax", "Training script: train.py; site generator: gen_site.py"])
add(5, "Live Demo", ["Try it: paste a ticket and press Classify Priority", "Critical example: The entire website is down and no customer can log in at all -> critical, about 72.4%", "Low example: There is a small spelling mistake in the welcome message on the home page -> low, about 51.3%", f"Demo: https://{DOMAIN}"])
add(6, "Results", ["5-fold cross-validation accuracy: 74.5%", "Baseline (always guessing the most common priority): 25.0% accuracy — a 3.0x lift", "Best classes: low F1 0.84, critical F1 0.81; hardest: high F1 0.64", "Browser demo matches Python probabilities exactly on all test samples"])
add(7, "Future Scope", ["Train on a larger real-world ticket dataset with thousands of examples", "Add auto-assignment — route critical tickets to the on-call engineer", "Add urgency trends: how many critical tickets arrived this week", "Support more languages, starting with Telugu and Hindi"])
add(8, "Thank You", ["TicketTriage — Support Ticket Priority Classifier", "Vikranth Reddy, B.Tech CSE (AI & ML), Woxsen University", "Source: github.com/HVRGAMING2705/tickettriage", "Questions welcome!"])
prs.save("/home/hatch/workspace/goals/daily-ai-ml-project-factory/files/AIML_TicketTriage_2026-11-17.pptx")
print("slides:", len(prs.slides._sldIdLst))
