"""Track 05: Bias, fairness, and clinical risk.

Bias in a clinical AI model enters at one of four points: in the training
data, in the labels, in the features, or in the deployment context. The
track addresses each entry point with a concrete clinical example,
demonstrates disparate subgroup performance on a synthetic model,
addresses the fairness-metric trade-off (the impossibility theorem
result), and closes with a vendor-evaluation checklist.
"""

import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import types

    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd

    _COURSE_TITLES = {
        "03": "Privacy, ethics, and governance",
        "04": "Clinical epidemiology",
        "16": "Leadership and professional practice",
    }

    def _course_label(course_id):
        title = _COURSE_TITLES.get(course_id.split("-")[0])
        return f"Course {course_id}: {title}" if title else f"Course {course_id}"

    def _xref_callback(from_course, to_course, topic, body):
        return mo.callout(
            mo.md(f"**Callback to {_course_label(to_course)}.** {topic}\n\n{body}"),
            kind="neutral",
        )

    def _xref_forward(from_course, to_course, topic, body):
        return mo.callout(
            mo.md(f"**Forward to {_course_label(to_course)}.** {topic}\n\n{body}"),
            kind="neutral",
        )

    xref = types.SimpleNamespace(callback=_xref_callback, forward=_xref_forward)

    def roc_curve_points(y_true, y_score):
        order = np.argsort(-y_score, kind="stable")
        y_sorted = np.asarray(y_true)[order]
        scores_sorted = np.asarray(y_score)[order]
        positives = float(y_sorted.sum())
        negatives = float(len(y_sorted) - positives)
        tpr_list = [0.0]
        fpr_list = [0.0]
        tp = 0.0
        fp = 0.0
        prev_score = None
        for label, s in zip(y_sorted, scores_sorted):
            if prev_score is not None and s != prev_score:
                tpr_list.append(tp / positives if positives else 0.0)
                fpr_list.append(fp / negatives if negatives else 0.0)
            if label == 1:
                tp += 1
            else:
                fp += 1
            prev_score = s
        tpr_list.append(tp / positives if positives else 0.0)
        fpr_list.append(fp / negatives if negatives else 0.0)
        return np.array(fpr_list), np.array(tpr_list)

    def auc_from_roc(fpr, tpr):
        return float(np.trapz(tpr, fpr))

    return alt, auc_from_roc, mo, np, pd, roc_curve_points, xref


@app.cell
def _(mo):
    mo.md(
        r"""
        # Track 05: Bias, fairness, and clinical risk

        ## The premise: bias enters at one of four points

        A clinical AI model that performs unequally across patient subgroups did not become biased after deployment. The bias was introduced upstream, during the construction of the model, at one of four points in the pipeline. The track names each entry point, gives a clinical example of the failure mode it produces, and shows the subgroup-performance demonstration on a synthetic model.

        The four points are: the training data, the labels, the features, and the deployment context. The first three are choices made during model construction. The fourth is a choice made at deployment time and is the responsibility of the institution adopting the model, not the institution that trained it.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Entry point 1: bias in the training data

        The training dataset is a sample of patients. If the sample over-represents some subgroup and under-represents another, the trained model's parameters fit the over-represented subgroup well and the under-represented subgroup poorly. The model's overall performance is dominated by the over-represented subgroup; the under-represented subgroup's worse performance is invisible in the overall number.

        **Clinical example.** A skin-lesion classifier trained on a dermatology-clinic dataset of 130,000 images, 95% of which depict lighter skin tones. The model achieves overall accuracy comparable to dermatologists. On the 5% of training images that depict darker skin tones, accuracy is far lower. The model is deployed at a primary care clinic with a more diverse patient population; the diagnostic miss rate for darker-skinned patients is several times the miss rate for lighter-skinned patients. The bias was in the training data sampling; the model's parameters reflected the sample.

        **The remedy** is to audit the training cohort against the deployment population for every relevant subgroup, to stratified-sample if the training corpus allows, and to report subgroup performance separately in the published evaluation.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Entry point 2: bias in the labels

        The training label is supposed to be the ground truth the model learns to predict. When the available label is a proxy for the true outcome of clinical interest, any bias in the proxy becomes part of the model.

        **Clinical example.** The Obermeyer et al. 2019 Science paper documented a widely deployed risk-prediction tool that used healthcare cost in the prior year as a proxy for "patient who needs more care." Healthcare cost is systematically lower for Black patients at any given level of medical need, for reasons documented in the broader health-services literature (access barriers, mistrust, fewer specialist referrals, lower-reimbursement payer mix). The model learned to predict cost and was operationalized as a proxy for need. The result was that Black patients at a given level of medical need were assigned lower risk scores than White patients at the same level of need, and the algorithm systematically under-flagged Black patients for care management.

        **The remedy** is to audit the label for proxy bias before training begins. If healthcare cost is the only label available, the model's outputs cannot be reinterpreted as a measure of need without an additional calibration against actual need in the relevant subgroups.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Entry point 3: bias in the features

        The features the model sees are choices. Including a feature that is correlated with a protected attribute introduces that attribute into the model even when the attribute itself is excluded. Excluding a feature that the underlying biology depends on can produce uneven performance for the same reason.

        **Clinical example A: a proxy feature.** ZIP code is correlated with race, income, and access to care in the United States. A model that includes ZIP code as a feature has incorporated all three even if race, income, and access are not in the feature set. The model's predictions inherit the disparities present in the ZIP-code-to-outcome relationship in the training data.

        **Clinical example B: a missing feature.** A skin-cancer-risk model that does not include Fitzpatrick phototype as a feature is implicitly assuming the skin-cancer-risk biology is constant across phototypes. It is not; the model's risk estimates are systematically wrong for the phototypes the training data did not represent well.

        **The remedy** is to audit each feature for correlation with protected attributes and for relevance to the biology, and to be explicit about which proxies are present.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Entry point 4: bias in the deployment context

        The deployment context is everything about how the model is used after training: the workflow it is wired into, the clinicians who see its output, the threshold at which it fires, the patients who are presented to it. A model that is well-trained, well-validated, and well-calibrated can still cause disparate harm at deployment if any of these is unequal across subgroups.

        **Clinical example.** An EHR-based sepsis-alert model is deployed on the day shift but not the night shift because the implementation team only built the day-shift workflow integration. Patients admitted overnight do not benefit from the alerts. If the overnight-admission population is demographically different from the daytime-admission population (it usually is), the deployment-context choice produces a disparate effect even though the model itself is identical.

        **The remedy** is to plan the deployment with the same subgroup audit applied to the model. Course 16 (Leadership and Professional Practice) and Course 12 (Clinical Decision Support) both take up deployment-context questions in detail.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Demonstration: same model, two subgroups

        The chart below shows the performance of a single model on a 2,000-patient synthetic cohort. 70% of the cohort belongs to Group A; 30% belongs to Group B. The model was trained to optimize overall AUC. The result: overall AUC is 0.80, Group A AUC is 0.82, Group B AUC is 0.65. The model is excellent on the majority and substantially worse on the minority. The overall number hides this.
        """
    )
    return


@app.cell
def _(auc_from_roc, np, pd, roc_curve_points):
    n_a = 1400
    n_b = 600
    sub_rng = np.random.default_rng(seed=2026)

    feat_a = sub_rng.normal(0, 1, n_a)
    feat_b = sub_rng.normal(0, 1, n_b)
    logit_a = -1.0 + 1.5 * feat_a
    logit_b = -1.0 + 0.4 * feat_b
    risk_a = 1 / (1 + np.exp(-logit_a))
    risk_b = 1 / (1 + np.exp(-logit_b))
    y_a = (sub_rng.uniform(size=n_a) < risk_a).astype(int)
    y_b = (sub_rng.uniform(size=n_b) < risk_b).astype(int)

    score_a = feat_a
    score_b = feat_b

    fpr_overall, tpr_overall = roc_curve_points(np.concatenate([y_a, y_b]), np.concatenate([score_a, score_b]))
    fpr_grp_a, tpr_grp_a = roc_curve_points(y_a, score_a)
    fpr_grp_b, tpr_grp_b = roc_curve_points(y_b, score_b)
    auc_overall = auc_from_roc(fpr_overall, tpr_overall)
    auc_grp_a = auc_from_roc(fpr_grp_a, tpr_grp_a)
    auc_grp_b = auc_from_roc(fpr_grp_b, tpr_grp_b)

    subgroup_rows = pd.DataFrame(
        [
            {"Subgroup": "Overall (n=2,000)", "AUC": round(auc_overall, 3), "Event rate": float(np.mean(np.concatenate([y_a, y_b])))},
            {"Subgroup": "Group A (n=1,400, majority)", "AUC": round(auc_grp_a, 3), "Event rate": float(np.mean(y_a))},
            {"Subgroup": "Group B (n=600, minority)", "AUC": round(auc_grp_b, 3), "Event rate": float(np.mean(y_b))},
        ]
    )
    subgroup_rows["Event rate"] = subgroup_rows["Event rate"].round(3)
    subgroup_rows.index = range(1, len(subgroup_rows) + 1)
    return (
        auc_grp_a,
        auc_grp_b,
        auc_overall,
        feat_a,
        feat_b,
        fpr_grp_a,
        fpr_grp_b,
        fpr_overall,
        logit_a,
        logit_b,
        n_a,
        n_b,
        risk_a,
        risk_b,
        score_a,
        score_b,
        sub_rng,
        subgroup_rows,
        tpr_grp_a,
        tpr_grp_b,
        tpr_overall,
        y_a,
        y_b,
    )


@app.cell
def _(subgroup_rows):
    subgroup_rows
    return


@app.cell
def _(alt, fpr_grp_a, fpr_grp_b, fpr_overall, pd, tpr_grp_a, tpr_grp_b, tpr_overall):
    overall_df = pd.DataFrame({"fpr": fpr_overall, "tpr": tpr_overall, "Subgroup": "Overall"})
    a_df = pd.DataFrame({"fpr": fpr_grp_a, "tpr": tpr_grp_a, "Subgroup": "Group A (majority)"})
    b_df = pd.DataFrame({"fpr": fpr_grp_b, "tpr": tpr_grp_b, "Subgroup": "Group B (minority)"})
    all_df = pd.concat([overall_df, a_df, b_df], ignore_index=True)
    diag_sub = pd.DataFrame({"fpr": [0, 1], "tpr": [0, 1]})

    subgroup_chart = (
        alt.Chart(all_df).mark_line().encode(
            x=alt.X("fpr:Q", title="1 - Specificity"),
            y=alt.Y("tpr:Q", title="Sensitivity"),
            color=alt.Color("Subgroup:N", title=""),
        )
        + alt.Chart(diag_sub).mark_line(strokeDash=[4, 4], color="#888").encode(x="fpr:Q", y="tpr:Q")
    ).properties(width=520, height=360, title="ROC by subgroup: the overall curve hides the minority disparity")
    subgroup_chart
    return a_df, all_df, b_df, diag_sub, overall_df, subgroup_chart


@app.cell
def _(mo):
    mo.md(
        r"""
        Three observations from the chart.

        First, the overall ROC curve (which most published papers report) lies between the two subgroup curves and looks acceptable. A reviewer who sees only the overall AUC would not detect the Group B problem.

        Second, the Group B ROC curve is dramatically worse. A model deployed against a Group B patient is operating at a much lower discrimination level than the published AUC suggests.

        Third, the subgroup gap exists despite the model being trained without any reference to subgroup membership. The model picked up a feature relationship that holds well in Group A and weakly in Group B; the optimizer concentrated its parameter budget on the Group A relationship because Group A patients dominate the training set.

        The audit that would have caught this gap is a subgroup-AUC table at evaluation time. Most clinical AI papers historically did not report this. TRIPOD-AI now requires it.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The fairness-metric trade-off

        Several plausible-sounding definitions of "the model is fair" cannot all be satisfied simultaneously except in degenerate cases (specifically, the case where the prevalence of the outcome is identical across subgroups, or the case where the model has perfect AUC). The Kleinberg, Mullainathan, Raghavan 2016 result and the Chouldechova 2017 ProPublica-COMPAS analysis pinned this in the algorithmic-fairness literature.

        Three fairness criteria appear most often:

        - **Demographic parity.** The model's positive-prediction rate is equal across subgroups (P(predicted positive) is the same for Group A and Group B).
        - **Equalized odds.** The model's true-positive rate and false-positive rate are equal across subgroups.
        - **Calibration parity.** The model's calibration is equal across subgroups (a patient with predicted probability 0.30 has a 30% outcome rate in both groups).

        The impossibility result: when the outcome prevalence differs across subgroups (the common clinical case), no model can satisfy all three simultaneously. A modeler has to choose two of the three at most, and the choice depends on the clinical setting.

        In most clinical-prediction settings, calibration parity is the necessary condition (the probability the model produces should mean the same thing across subgroups). Equalized odds may be the right second criterion when the cost of false negatives is high and equal across subgroups. Demographic parity is rarely the right criterion in clinical prediction because the underlying outcome rate often genuinely differs across subgroups; enforcing demographic parity then requires falsifying the predicted probabilities.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## The vendor-evaluation checklist

        The following questions, asked of a vendor before adoption, surface most clinical-AI bias and fairness problems at the appraisal stage rather than at the post-deployment stage.

        - **Training cohort.** Specifically: who is in it (race, sex, age, insurance, payer mix, geography), when (date range), and what fraction of the cohort comes from each major patient stratum at our institution?
        - **Outcome definition.** What was the label, and what proxy choices were made? Where could a proxy bias have entered?
        - **Subgroup AUC and calibration.** Reported separately for race, sex, age band, and any other locally relevant subgroup. Sample sizes per subgroup.
        - **External validation.** Reported on a population similar to ours. If not, on what population?
        - **Fairness criteria.** Which fairness criterion did the developers prioritize, and what trade-offs were accepted?
        - **Post-deployment monitoring.** What is the vendor's documented plan for monitoring subgroup performance after deployment, and what is the institution's responsibility?
        - **Recourse.** If the model gets a patient wrong, what is the recourse for the patient and the clinician?

        A vendor that cannot answer most of these questions is selling a product that is not ready for clinical deployment. The questions are the operational form of the appraisal framework from Track 04 plus the equity considerations from this track.
        """
    )
    return


@app.cell
def _(xref):
    xref.callback(
        "09",
        "03",
        "Algorithmic fairness as a privacy and governance question",
        "Course 03 Track 4 introduced the algorithmic-fairness frame. The four-entry-point taxonomy here is the operational form of that frame at the model-construction level. The vendor-evaluation checklist above is the negotiation form a clinical informaticist uses at procurement.",
    )
    return


@app.cell
def _(xref):
    xref.forward(
        "09",
        "16",
        "Deployment context is a leadership question",
        "Course 16 (Leadership and Professional Practice) takes up deployment-context decisions as a project-management and change-management question. The subgroup-equity audit at deployment is one of the standard governance items in the implementation plan a CMIO would present to the C-suite before go-live.",
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Summary

        Bias in a clinical AI model enters at one of four points: the training data, the labels, the features, or the deployment context. Each has a characteristic failure mode and a remedy. Disparate subgroup performance is visible at evaluation time only when subgroup AUC and calibration are reported separately; the overall number hides the gap. Several plausible fairness criteria cannot be simultaneously satisfied except in degenerate cases; the modeler has to pick which to prioritize. Calibration parity is the standard choice in clinical prediction. The vendor-evaluation checklist is the operational tool for asking the right questions at procurement.

        Track 06 takes up large language models. The bias and fairness questions apply to LLMs as well, with two additional considerations: the training corpus is even harder to audit than a clinical-prediction-model dataset, and the model's behavior shifts in poorly-understood ways when the prompt changes.
        """
    )
    return


if __name__ == "__main__":
    app.run()
