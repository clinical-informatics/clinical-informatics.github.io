# Go deeper: LLMs in clinical workflows

**If you want to understand the next-token-prediction intuition before moving on:**

- [Stephen Wolfram, "What Is ChatGPT Doing... and Why Does It Work?"](https://writings.stephenwolfram.com/2023/02/what-is-chatgpt-doing-and-why-does-it-work/) is the most-cited free essay on the intuition the track presents (next-token prediction, training corpus, emergent behavior). Wolfram writes for a general technical audience without requiring deep ML background.
- [Andrej Karpathy's "Let's build GPT" video](https://www.youtube.com/watch?v=kCc8FmEb1nY) builds a small character-level transformer from scratch in two hours. The video is the right next step for a reader who wants to see what training a small language model actually involves at the code level.

**If you want to see this applied clinically:**

- [Lee et al., "Benefits, Limits, and Risks of GPT-4 as an AI Chatbot for Medicine" (NEJM 2023)](https://www.nejm.org/doi/full/10.1056/NEJMsr2214184) is the clinical-medicine-audience overview of LLM capabilities and failure modes in clinical settings. It is short and frames the use-cases-vs-dangers split the track addresses.
- [Singhal et al., "Large language models encode clinical knowledge" (Med-PaLM; Nature 2023)](https://www.nature.com/articles/s41586-023-06291-2) is the most-cited demonstration of an LLM achieving competitive performance on a medical question-answering benchmark. The paper documents the evaluation challenges the track addresses (the no-single-ground-truth, prompt-sensitivity problem) and the techniques used to mitigate them.

**If you want to go significantly further:**

- [Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (2020)](https://arxiv.org/abs/2005.11401) is the original RAG paper. The introduction and method sections are accessible without deep ML background and describe the retrieval-then-generation pattern the track presents as the standard mitigation for hallucination on enterprise clinical content.
- [Vaswani et al., "Attention Is All You Need" (2017)](https://arxiv.org/abs/1706.03762) is the foundational transformer paper. The paper is the deep prerequisite for the technical AI literature on LLMs; reading it is the inflection point at which the LLM literature becomes accessible at the architectural level.
