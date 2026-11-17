# TicketTriage — Support Ticket Priority Classifier

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

TF-IDF (word unigrams, sublinear TF, L2) + multinomial logistic regression (C=1.0) trained on 200 hand-written support tickets (50 per priority: critical, high, medium, low; 685 vocabulary words, seed 42).

- 5-fold CV accuracy: 74.5% (majority-class baseline: 25.0%)
- Live demo: https://tickettriage.vercel.app (runs fully in the browser — no backend)
- `train.py` trains the model and writes `model.json`; `index.html` applies the same weights in JavaScript.
