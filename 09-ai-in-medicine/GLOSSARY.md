# Glossary: 09 AI in medicine

The terms below appear across the six tracks of this course. Terms in the curriculum-wide glossary are not repeated here.

**AUC (area under the ROC curve).** A single-number summary of a model's discrimination across all thresholds. AUC ranges from 0.5 (chance) to 1.0 (perfect ranking). AUC is the probability that a randomly chosen positive case receives a higher score than a randomly chosen negative case. AUC reports ranking quality; it says nothing about the absolute level of the probabilities the model produces.

**Brier score.** The mean squared error between the predicted probability and the binary outcome. A perfect model has a Brier score of 0. The Brier score is the standard scalar summary of calibration; lower is better.

**Calibration.** The agreement between the probabilities a model produces and the observed event rates among patients assigned those probabilities. A model that says 30% to a group of patients is well calibrated if 30% of them experience the outcome. Calibration is the second of the two model-quality questions (discrimination is the first).

**Calibration plot.** A scatter plot of observed event rate (y) against predicted probability (x), one point per probability bin. The diagonal is perfect calibration; points above the diagonal are model under-predictions; points below are over-predictions.

**Discrimination.** The model's ability to rank patients who experienced the outcome higher than patients who did not. Discrimination is measured by AUC and is independent of calibration. A perfectly discriminating model can still produce uncalibrated probabilities.

**Generalization.** The model's performance on patients drawn from the same population as the training set but not part of it. Generalization is the goal of training; overfitting is its failure.

**Hallucination.** A confidently produced output from a large language model that is not supported by any source the model had access to. Hallucinations are characteristic of LLMs, not bugs; they are a consequence of next-token prediction trained on a heterogeneous corpus.

**Overfitting.** A model that has memorized the training set has training error close to zero and test error well above zero. The model has learned features of the specific training examples rather than features of the population the examples are drawn from.

**Prediction.** Applying the trained model function to a new input and obtaining its output. The output is a score for regression tasks and a probability (or class) for classification tasks.

**Retrieval-augmented generation (RAG).** A pattern that retrieves source documents relevant to a query and supplies them to an LLM as context, so the LLM produces an answer grounded in the supplied sources rather than from its training distribution alone. RAG is the standard mitigation for hallucination on enterprise clinical content.

**ROC curve.** A plot of sensitivity (y-axis) against false-positive rate (x-axis) across all thresholds of a model's score. The curve summarizes how the model's sensitivity and specificity trade off as the alert threshold moves.

**Subgroup performance.** The model's discrimination and calibration computed separately within strata defined by patient demographics or clinical features. Equal overall performance does not imply equal subgroup performance; subgroup performance is the central concern of clinical fairness.

**Training.** The process of fitting the model's parameters to a labeled dataset by minimizing a loss function. Training does not produce a model that is correct; training produces a model that is consistent with the training set under the chosen loss function.

**Validation set.** A subset of the data held out from training and used to tune model hyperparameters or to compare candidate models. A separate test set, held out from both training and validation, is used for the final performance estimate.
