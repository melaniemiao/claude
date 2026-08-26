# Verified AI/ML book catalogue

Every book below was checked against an Open Library catalogue record for existence
and authorship (see `verification.md`). Recommend from here freely without
re-verifying. Anything *not* here goes through `scripts/verify_books.py` first.

Years are first-edition years. Several of these have later editions — catalogue
records and printings disagree about dates more often than you would expect, so
name an edition number only if you checked it in this session. "Free online" marks
books whose authors or publishers host a legitimate free copy; those links were
live when this file was written, and a reader will find them by searching the title
plus the author's name.

**Contents**
- [Router: one book for this reader](#router-one-book-for-this-reader)
- [Understanding AI without the math](#understanding-ai-without-the-math)
- [Learning to build: the practitioner path](#learning-to-build-the-practitioner-path)
- [LLMs specifically](#llms-specifically)
- [Textbooks and theory](#textbooks-and-theory)
- [Math and statistics prerequisites](#math-and-statistics-prerequisites)
- [History and origins](#history-and-origins)
- [Safety, alignment, and the long run](#safety-alignment-and-the-long-run)
- [Ethics, power, and critique](#ethics-power-and-critique)
- [Economics and work](#economics-and-work)
- [Fiction](#fiction)

## Router: one book for this reader

When someone wants a single recommendation rather than a list:

| The reader | The book |
|---|---|
| Curious adult, no technical background | *Artificial Intelligence: A Guide for Thinking Humans* — Mitchell |
| "Explain what ChatGPT actually is" | *Co-Intelligence* — Mollick, or *Why Machines Learn* — Ananthaswamy for the mechanism |
| Engineer who wants to ship a model | *Hands-On Machine Learning* — Géron |
| Engineer who wants to ship an LLM feature | *AI Engineering* — Huyen |
| CS student wanting the canonical text | *Artificial Intelligence: A Modern Approach* — Russell & Norvig |
| Wants the math, properly | *Pattern Recognition and Machine Learning* — Bishop, or *Probabilistic Machine Learning* — Murphy |
| Worried about where this is going | *The Alignment Problem* — Christian |
| Skeptical that any of this works | *AI Snake Oil* — Narayanan & Kapoor |
| Interested in who is harmed | *Weapons of Math Destruction* — O'Neil |
| Journalist or manager wanting the industry story | *Genius Makers* — Metz |
| Reads novels, not manuals | *Klara and the Sun* — Ishiguro |

## Understanding AI without the math

For readers who want to genuinely understand the field, not to implement it.

- **Artificial Intelligence: A Guide for Thinking Humans** — Melanie Mitchell (2019).
  The best single explainer of what these systems do and where they fail. Written
  by a researcher, sober about hype in both directions. Predates the LLM boom, so
  pair with something recent for current systems.
- **Why Machines Learn** — Anil Ananthaswamy (2024). Shows the actual mathematics
  of learning to a general reader willing to look at an equation. The bridge book
  between popular and technical.
- **Co-Intelligence: Living and Working with AI** — Ethan Mollick (2024). Practical
  and current on using LLMs as a working tool; the book to give a manager or a
  colleague who keeps asking what to do with ChatGPT.
- **The Master Algorithm** — Pedro Domingos (2015). Machine learning organised as
  five competing schools of thought. A useful map, though its framing predates the
  deep learning consolidation.
- **The Book of Why** — Judea Pearl and Dana Mackenzie (2018). Causation versus
  correlation, and why prediction alone is not understanding. The best argument for
  what current ML is structurally missing.
- **The Deep Learning Revolution** — Terrence Sejnowski (2018). Neural networks
  from an insider who was there for the neuroscience-adjacent early decades.
- **Rebooting AI** — Gary Marcus and Ernest Davis (2019). The systematic case that
  deep learning alone will not get to robust intelligence. Read as a strong
  argument to engage with, not as settled ground.

## Learning to build: the practitioner path

Order matters here; these build on each other.

- **Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow** — Aurélien
  Géron (2017; later editions). The default first book for a working programmer.
  Code-first, ends with you having trained real models. Assumes Python, not much
  math.
- **Deep Learning with Python** — François Chollet (2017; 2nd ed. later). Written
  by the creator of Keras and unusually good at explaining *why* architectures look
  the way they do. Excellent prose for a technical book.
- **Deep Learning for Coders with fastai and PyTorch** — Jeremy Howard and Sylvain
  Gugger (2020). Top-down: results in chapter one, theory once you care. Free
  online. Suits people who lose patience with foundations-first books.
- **Grokking Deep Learning** — Andrew Trask (2019). Builds neural networks from
  scratch in NumPy. The right book for someone who does not trust a framework they
  cannot see inside.
- **The Hundred-Page Machine Learning Book** — Andriy Burkov (2019). Exactly what it
  says; a fast orientation or a refresher, not a first and only book.
- **Designing Machine Learning Systems** — Chip Huyen (2022). The book about
  everything around the model: data, deployment, drift, monitoring. Where most
  real-world projects actually fail.
- **Machine Learning Engineering** — Andriy Burkov (2020). Complementary to Huyen,
  more checklist-shaped, strong on the project lifecycle.
- **Building Machine Learning Powered Applications** — Emmanuel Ameisen (2020).
  Product-minded: going from an idea to a shipped ML feature.
- **Interpretable Machine Learning** — Christoph Molnar (2019). The reference for
  explaining model behaviour — SHAP, LIME, partial dependence. Free online.

## LLMs specifically

- **AI Engineering: Building Applications with Foundation Models** — Chip Huyen
  (2024). The current best overview of building on top of foundation models rather
  than training them: evaluation, prompting, RAG, finetuning, cost.
- **Build a Large Language Model (From Scratch)** — Sebastian Raschka (2024).
  Implements a GPT-style model step by step in PyTorch. The clearest path from
  "I use the API" to "I know what is inside".
- **Hands-On Large Language Models** — Jay Alammar and Maarten Grootendorst (2024).
  Heavily illustrated, from the author of the *Illustrated Transformer* posts.
  Strong for visual learners.
- **Natural Language Processing with Transformers** — Lewis Tunstall, Leandro von
  Werra and Thomas Wolf (2022). Hugging Face-centric and practical. Note its age
  relative to the current model generation — the pipeline concepts hold up, the
  specific models have moved on.
- **Speech and Language Processing** — Daniel Jurafsky and James H. Martin (2000;
  ongoing editions). The NLP textbook. Draft chapters of the current edition are
  free online and are kept current with the field.

## Textbooks and theory

Assume undergraduate math unless noted; check the prerequisite before recommending.

- **Artificial Intelligence: A Modern Approach** — Stuart Russell and Peter Norvig
  (1995; 4th ed. later). The canonical survey of the whole field — search, logic,
  probability, learning, ethics. Broad rather than deep on modern deep learning.
- **Deep Learning** — Ian Goodfellow, Yoshua Bengio and Aaron Courville (2016). The
  foundational reference. Rigorous, pre-transformer; recommend for fundamentals and
  say so. Free online.
- **Understanding Deep Learning** — Simon J. D. Prince (2023). The modern successor
  in spirit: covers transformers and diffusion, unusually clear figures. Free
  online. Often the better recommendation now for a self-studier.
- **Dive into Deep Learning** — Aston Zhang, Zachary Lipton, Mu Li and Alexander
  Smola (2023). Interactive, notebook-based, multi-framework. Free online.
- **Pattern Recognition and Machine Learning** — Christopher M. Bishop (2006). The
  Bayesian classic. Demanding and worth it if the reader has the linear algebra and
  probability.
- **Probabilistic Machine Learning: An Introduction** — Kevin P. Murphy (2022), and
  its **Advanced Topics** companion. The modern, comprehensive successor to Murphy's
  2012 *Machine Learning: A Probabilistic Perspective*. Free online.
- **The Elements of Statistical Learning** — Trevor Hastie, Robert Tibshirani and
  Jerome Friedman (2001). Statistical learning from the statisticians' side.
  Free online. Recommend *An Introduction to Statistical Learning* first for most
  people.
- **Reinforcement Learning: An Introduction** — Richard S. Sutton and Andrew G.
  Barto (1998; 2nd ed. 2018). The RL book, still unmatched. Free online.
- **Probabilistic Graphical Models** — Daphne Koller and Nir Friedman (2009).
  Encyclopedic on structured probabilistic modelling; a reference more than a
  read-through.
- **Information Theory, Inference, and Learning Algorithms** — David J. C. MacKay
  (2003). Idiosyncratic, brilliant, and the book that makes inference click for
  many people. Free online.
- **Fairness and Machine Learning** — Solon Barocas, Moritz Hardt and Arvind
  Narayanan (2023). The technical treatment of fairness — impossibility results
  included — rather than the essayistic one. Free online.

## Math and statistics prerequisites

- **Mathematics for Machine Learning** — Marc Peter Deisenroth, A. Aldo Faisal and
  Cheng Soon Ong (2020). Exactly the linear algebra, calculus and probability the ML
  books assume, and nothing else. Free online.
- **An Introduction to Statistical Learning** — Gareth James, Daniela Witten, Trevor
  Hastie and Robert Tibshirani (2013). The gentler sibling of *Elements*, with R and
  Python versions. The best on-ramp for someone whose statistics is rusty. Free
  online.

## History and origins

- **The Quest for Artificial Intelligence** — Nils J. Nilsson (2009). A field
  history by someone who helped build it. Thorough and even-handed.
- **Machines Who Think** — Pamela McCorduck (1979). The early decades reported as
  they happened, with the founders as characters. Still the most human account of
  AI's origins.
- **Genius Makers** — Cade Metz (2021). How the deep learning generation went from
  academic fringe to the centre of the industry. Reads like reporting because it is.
- **The Worlds I See** — Fei-Fei Li (2023). Memoir plus the ImageNet story — how the
  data that started the deep learning era got built.
- **Empire of AI** — Karen Hao (2025). Investigative account of OpenAI and the
  industry's power structure. Adversarial in stance; read alongside industry-side
  accounts.
- **Gödel, Escher, Bach** — Douglas R. Hofstadter (1979). Not an AI textbook and not
  a quick read; the book that made a generation care about machine minds.
- **The Society of Mind** — Marvin Minsky (1986). Intelligence as many small
  non-intelligent processes. Historically central, aphoristic in form.
- **Perceptrons** — Marvin Minsky and Seymour Papert (1969). The book usually blamed
  for the first AI winter. Recommend to people who want the primary source rather
  than the legend about it.
- **The Emperor's New Mind** — Roger Penrose (1989). The classic argument that
  consciousness is not computation. Widely disputed; valuable as the strongest
  version of that position.
- **What Computers Can't Do** — Hubert L. Dreyfus (1972; later *What Computers Still
  Can't Do*). The philosophical critique of symbolic AI, and much of it aged well.

## Safety, alignment, and the long run

- **The Alignment Problem** — Brian Christian (2020). The best entry point:
  reported, specific, and grounded in real research rather than thought experiments.
  Start here for almost anyone.
- **Human Compatible** — Stuart Russell (2019). A leading AI researcher's argument
  that the field's standard model of objectives is the problem, plus a proposed fix.
- **Superintelligence** — Nick Bostrom (2014). The philosophical case that set the
  terms of the debate. Dense, pre-LLM, and now as much a historical document as a
  current argument — say that when recommending it.
- **Life 3.0** — Max Tegmark (2017). Broader and more readable than Bostrom, ranging
  from near-term to cosmic.
- **If Anyone Builds It, Everyone Dies** — Eliezer Yudkowsky and Nate Soares (2025).
  The strongest statement of the extreme-risk position. Recommend as one side of a
  live argument, ideally paired with a skeptical book.
- **AI Snake Oil** — Arvind Narayanan and Sayash Kapoor (2024). The counterweight:
  which AI claims are real, which are marketing, and how to tell. Pairs well with
  any of the above.
- **The Coming Wave** — Mustafa Suleyman (2023). Containment and governance, from a
  founder of DeepMind and Inflection.
- **Deep Utopia** — Nick Bostrom (2024). The rarely-asked other question: what if it
  goes well and human effort becomes optional?

## Ethics, power, and critique

- **Weapons of Math Destruction** — Cathy O'Neil (2016). Algorithmic scoring in
  hiring, credit, policing and schooling. The accessible starting point.
- **Atlas of AI** — Kate Crawford (2021). AI as a material system: minerals, labour,
  energy, data extraction. Reframes the field as infrastructure and politics.
- **Algorithms of Oppression** — Safiya Umoja Noble (2018). How search engines
  encode racism, based on years of documentation.
- **Race After Technology** — Ruha Benjamin (2019). Coins "the New Jim Code" for
  discrimination laundered through automated systems.
- **Automating Inequality** — Virginia Eubanks (2018). What automated decision
  systems do inside welfare and housing bureaucracies, reported case by case.
- **Unmasking AI** — Joy Buolamwini (2023). First-person account of finding and
  proving facial recognition's demographic failures.
- **Artificial Unintelligence** — Meredith Broussard (2018), and **More Than a
  Glitch** (2023). "Technochauvinism" — the assumption that a technical solution is
  the better one — and why bias is structural rather than accidental.
- **The Age of Surveillance Capitalism** — Shoshana Zuboff (2019). Long and
  polemical; the definitive statement of the behavioural-data business model that
  funds much of AI.
- **The Ethical Algorithm** — Michael Kearns and Aaron Roth (2019). What fairness
  and privacy look like when written into the algorithm itself. Technical but short.

## Economics and work

- **Prediction Machines** — Ajay Agrawal, Joshua Gans and Avi Goldfarb (2018). AI as
  a drop in the cost of prediction, and what that implies for decisions and firms.
  The most useful framing for business readers.
- **Power and Prediction** — same authors (2022). The follow-up on why adoption
  requires redesigning systems, not inserting models into existing ones.
- **The Second Machine Age** — Erik Brynjolfsson and Andrew McAfee (2014). The
  earlier macro account of automation and labour; foundational for the economics
  conversation.
- **AI Superpowers** — Kai-Fu Lee (2018). US–China competition from someone who
  worked in both ecosystems. Dated on specifics, still valuable on the structural
  differences.

## Fiction

Good when someone wants to think about AI without a technical book, or as a gift.

- **Klara and the Sun** — Kazuo Ishiguro (2021). An artificial companion narrates;
  quiet, devastating, no technical background needed.
- **The Lifecycle of Software Objects** — Ted Chiang (2010), and **Exhalation**
  (2019), the collection containing it. The most thoughtful fiction about raising
  and owning artificial minds.
- **I, Robot** — Isaac Asimov (1950). The Three Laws stories — where most popular
  intuitions about AI rules originally come from.
- **Do Androids Dream of Electric Sheep?** — Philip K. Dick (1968). The question of
  what distinguishes a person, before anyone had to ask it practically.
- **Neuromancer** — William Gibson (1984). Cyberpunk's founding text; its AIs still
  read as strange in a way most fiction's do not.
