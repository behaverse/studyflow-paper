"""The computations of the example study's analysis, as the five functions `fig-step3-coordinator.studyflow.yaml`
calls: what the diagram hands off to Python when it coordinates rather than computes. Each function is one
call of a library the study pins (pandas, scipy, statsmodels, scikit-learn, matplotlib); the diagram keeps what
is not computation, the order of the steps, the hand-offs between them, the feasibility gates, the decision
rules, and the claim state each question ends in. Deposited beside the study, so a reader of the diagram can
open the one file it names. Run `python3 analysis.py` for a self-check on a synthetic cohort.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

KEYS = ["context.subject", "context.state.arm", "trialContext.task.id", "trialContext.block.name", "trialContext.trial.id"]
ACCURACY, LATENCY, CONGRUENCY, ARM, SUBJECT = "result.isCorrect", "trialContext.trial.timeInTrial", "trialContext.congruency", "context.state.arm", "context.subject"


def trials_table(events: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """One row per answered trial, from the run's event lines: the trial's keys, the congruency the task drew,
    whether the answer was correct, and its latency (the time of the trial's last event). `columns` is the list
    the diagram names, which the validator checks against the trials schema before any data moves."""
    keys = [c for c in columns if c in KEYS]
    values = [c for c in columns if c not in KEYS]
    aggregate = {c: ("max" if c == LATENCY else "first") for c in values}
    rows = events.pivot_table(index=keys, values=values, aggfunc=aggregate).reset_index()
    return rows.dropna(subset=[ACCURACY]).astype({ACCURACY: float, LATENCY: float})


def per_subject(trials: pd.DataFrame) -> pd.DataFrame:
    """One row per subject: its arm, its mean accuracy, and its mean latency over its answered trials."""
    return trials.pivot_table(index=[SUBJECT, ARM], values=[ACCURACY, LATENCY], aggfunc="mean").reset_index()


def congruency_test(trials: pd.DataFrame) -> dict:
    """Is a subject slower on incongruent than on congruent trials? Per subject, the mean latency on incongruent
    trials minus the mean on congruent ones, tested against zero in the predicted direction."""
    from scipy import stats

    by = trials.pivot_table(index=SUBJECT, columns=CONGRUENCY, values=LATENCY, aggfunc="mean")
    cost = by["Incongruent"].sub(by["Congruent"]).dropna()
    result = stats.ttest_1samp(cost, popmean=0, alternative="greater")
    return {"subjects": int(cost.count()), "statistic": float(result.statistic), "pvalue": float(result.pvalue)}


def agreement_test(per_subject: pd.DataFrame, margin_low: float, margin_high: float) -> dict:
    """Do the two arms reach the same accuracy? Two one-sided tests of per-subject accuracy against the margin."""
    from statsmodels.stats.weightstats import ttost_ind

    arms = [group[ACCURACY].to_numpy() for _, group in per_subject.groupby(ARM)]
    pvalue, lower, upper = ttost_ind(arms[0], arms[1], low=margin_low, upp=margin_high, usevar="unequal")
    return {"pvalue": float(pvalue), "lower": float(lower[1]), "upper": float(upper[1])}


def divergence_test(per_subject: pd.DataFrame, n_permutations: int) -> dict:
    """Can a classifier tell the two arms apart? Logistic regression on per-subject accuracy and latency, scored
    leave-one-subject-out, against the same score under shuffled arm labels (the unit that was randomized)."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import LeaveOneOut, permutation_test_score

    score, _, pvalue = permutation_test_score(LogisticRegression(max_iter=1000), per_subject[[ACCURACY, LATENCY]],
                                              per_subject[ARM], cv=LeaveOneOut(), n_permutations=n_permutations, scoring="accuracy")
    return {"accuracy": float(score), "pvalue": float(pvalue)}


def write_results(trials: pd.DataFrame, per_subject: pd.DataFrame, directory: str, **tests: dict | None) -> str:
    """The results dataset: the per-subject and group tables, one JSON per question that was tested, and the
    accuracy figure by arm and congruency."""
    import matplotlib

    matplotlib.use("Agg")
    out = Path(directory)
    out.mkdir(parents=True, exist_ok=True)
    per_subject.to_csv(out / "per_subject.csv", index=False)
    per_subject.pivot_table(index=ARM, values=[ACCURACY, LATENCY], aggfunc=["mean", "std"]).to_csv(out / "group.csv")
    for question, result in tests.items():
        if result is not None:
            (out / f"{question}.json").write_text(json.dumps(result, indent=2))
    axes = trials.boxplot(column=[ACCURACY], by=[ARM, CONGRUENCY], grid=False, rot=30)
    axes.figure.savefig(out / "accuracy.png", bbox_inches="tight")
    return str(out)


if __name__ == "__main__":  # a synthetic cohort of eight, four per arm, walked the way the diagram walks it
    import numpy as np

    rng = np.random.default_rng(42)
    events = []
    for subject in range(8):
        arm = "cautious" if subject % 2 == 0 else "impulsive"
        for task, n in (("simon", 15), ("nback", 32)):
            for trial in range(n):
                congruency = rng.choice(["Congruent", "Incongruent", "Neutral"]) if task == "simon" else None
                slow = 0.4 if congruency == "Incongruent" else 0.0
                for event in range(3):  # several event lines per trial, as the build logs them
                    events.append({SUBJECT: str(subject), ARM: arm, "trialContext.task.id": task, "trialContext.block.name": "b1",
                                   "trialContext.trial.id": str(trial), CONGRUENCY: congruency,
                                   ACCURACY: bool(rng.random() < (0.9 if arm == "cautious" else 0.7)),
                                   LATENCY: float(event + slow + rng.random())})
    columns = KEYS + [CONGRUENCY, ACCURACY, LATENCY]
    trials = trials_table(pd.DataFrame(events), columns)
    subjects = per_subject(trials)
    smallest_arm = int(subjects[ARM].value_counts().min())
    rules = {"alpha": 0.05, "min_subjects": 3, "min_per_arm": 4, "margin_low": -0.1, "margin_high": 0.1, "n_permutations": 200}
    congruency = congruency_test(trials) if len(subjects) >= rules["min_subjects"] else None
    agreement = agreement_test(subjects, rules["margin_low"], rules["margin_high"]) if smallest_arm >= rules["min_per_arm"] else None
    divergence = divergence_test(subjects, rules["n_permutations"]) if smallest_arm >= rules["min_per_arm"] else None
    for name, result in (("congruency", congruency), ("agreement", agreement), ("divergence", divergence)):
        state = "Not testable" if result is None else ("Supported" if result["pvalue"] < rules["alpha"] else "Not supported")
        print(f"{name:12s} {state:14s} {result}")
    print("wrote", write_results(trials, subjects, "/tmp/studyflow-coordinator-selfcheck", congruency=congruency, agreement=agreement, divergence=divergence))
