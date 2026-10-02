"""The computations of the example study's analysis, as the five functions `fig-step3-coordinator.studyflow.yaml`
calls: what the diagram hands off to Python when it coordinates rather than computes. Each function is a
call of a library the study pins (pandas, scipy, scikit-learn, matplotlib); the diagram keeps what is not
computation, the order of the steps, the hand-offs between them, the feasibility gates, the decision rules, and
the claim state each question ends in. Accuracy is the measure throughout: a language model's latency is the
time its server took to generate the reply, so it is reported and not tested. Deposited beside the study, so a
reader of the diagram can open the one file it names. Run `python3 analysis.py` for a self-check on a synthetic
cohort.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

KEYS = ["context.subject", "context.state.arm", "trialContext.task.id", "trialContext.block.name", "trialContext.trial.id"]
ACCURACY, LATENCY, CONGRUENCY = "result.isCorrect", "trialContext.trial.timeInTrial", "trialContext.congruency"
ARM, SUBJECT, TASK, BLOCK = "context.state.arm", "context.subject", "trialContext.task.id", "trialContext.block.name"


def trials_table(events: pd.DataFrame, columns: list[str], blocks: list[str]) -> pd.DataFrame:
    """One row per answered trial of the test blocks, from the run's event lines: the trial's keys, the congruency
    the task drew, whether the answer was correct, and its latency (the time of the trial's last event). `columns`
    and `blocks` are the lists the diagram names; the validator checks the columns against the trials schema
    before any data moves."""
    keys = [c for c in columns if c in KEYS]
    values = [c for c in columns if c not in KEYS]
    aggregate = {c: ("max" if c == LATENCY else "first") for c in values}
    rows = events.pivot_table(index=keys, values=values, aggfunc=aggregate).reset_index()
    rows = rows[rows[BLOCK].isin(blocks)]
    return rows.dropna(subset=[ACCURACY]).astype({ACCURACY: float, LATENCY: float})


def per_subject(trials: pd.DataFrame) -> dict:
    """One row per subject, its arm and its mean accuracy in each task, one column per task (`table`); and the two
    counts the feasibility gates read: the number of subjects and the size of the smaller arm, 0 with one arm."""
    table = trials.pivot_table(index=[SUBJECT, ARM], columns=TASK, values=ACCURACY, aggfunc="mean").reset_index()
    arms = table[ARM].value_counts()
    return {"table": table, "subjects": len(table), "smallest_arm": int(arms.min()) if len(arms) == 2 else 0}


def congruency_test(trials: pd.DataFrame) -> dict:
    """Is a subject less accurate on incongruent than on congruent trials? Per subject, the mean accuracy on
    congruent trials minus the mean on incongruent ones, tested against zero in the predicted direction."""
    from scipy import stats

    by = trials.pivot_table(index=SUBJECT, columns=CONGRUENCY, values=ACCURACY, aggfunc="mean")
    cost = by["Congruent"].sub(by["Incongruent"]).dropna()
    result = stats.ttest_1samp(cost, popmean=0, alternative="greater")
    return {"subjects": int(cost.count()), "statistic": float(result.statistic), "pvalue": float(result.pvalue)}


def divergence_test(per_subject: pd.DataFrame, n_permutations: int) -> dict:
    """Can a classifier tell the two arms apart? Logistic regression on each subject's accuracy in each task,
    scored leave-one-subject-out, against the same score under shuffled arm labels (the unit that was randomized)."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import LeaveOneOut, permutation_test_score

    features = per_subject.drop(columns=[SUBJECT, ARM])
    score, _, pvalue = permutation_test_score(LogisticRegression(max_iter=1000), features, per_subject[ARM],
                                              cv=LeaveOneOut(), n_permutations=n_permutations, scoring="accuracy")
    return {"accuracy": float(score), "pvalue": float(pvalue)}


def write_results(trials: pd.DataFrame, per_subject: pd.DataFrame, directory: str, **tests: dict | None) -> str:
    """The results dataset: the per-subject and group tables, one JSON per question that was tested, and the
    accuracy figure by arm and congruency."""
    import matplotlib

    matplotlib.use("Agg")
    out = Path(directory)
    out.mkdir(parents=True, exist_ok=True)
    per_subject.to_csv(out / "per_subject.csv", index=False)
    per_subject.drop(columns=[SUBJECT]).pivot_table(index=ARM, aggfunc=["mean", "std"]).to_csv(out / "group.csv")
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
        for task, block, n in (("WO", "Simon", 30), ("NB", "XCIT_NB_01_Practice", 14), ("NB", "XCIT_NB_01_Test_A", 28), ("NB", "XCIT_NB_01_Test_B", 28)):
            for trial in range(n):
                congruency = rng.choice(["Congruent", "Incongruent", "Neutral"]) if task == "WO" else None
                harder = 0.15 if congruency == "Incongruent" else 0.0
                for event in range(3):  # several event lines per trial, as the build logs them
                    events.append({SUBJECT: str(subject), ARM: arm, TASK: task, BLOCK: block, "trialContext.trial.id": str(trial),
                                   CONGRUENCY: congruency, ACCURACY: bool(rng.random() < (0.9 if arm == "cautious" else 0.7) - harder),
                                   LATENCY: float(event + rng.random())})
    columns = KEYS + [CONGRUENCY, ACCURACY, LATENCY]
    trials = trials_table(pd.DataFrame(events), columns, ["Simon", "XCIT_NB_01_Test_A", "XCIT_NB_01_Test_B"])
    assert set(trials[BLOCK]) == {"Simon", "XCIT_NB_01_Test_A", "XCIT_NB_01_Test_B"}
    summary = per_subject(trials)
    subjects, smallest_arm = summary["table"], summary["smallest_arm"]
    assert summary["subjects"] == 8 and smallest_arm == 4
    rules = {"alpha": 0.05, "min_subjects": 3, "min_per_arm": 4, "n_permutations": 200}
    congruency = congruency_test(trials) if len(subjects) >= rules["min_subjects"] else None
    divergence = divergence_test(subjects, rules["n_permutations"]) if smallest_arm >= rules["min_per_arm"] else None
    for name, result in (("congruency", congruency), ("divergence", divergence)):
        state = "Not testable" if result is None else ("Supported" if result["pvalue"] < rules["alpha"] else "Not supported")
        print(f"{name:12s} {state:14s} {result}")
    print(subjects.to_string(index=False))
    print("wrote", write_results(trials, subjects, "/tmp/studyflow-coordinator-selfcheck", congruency=congruency, divergence=divergence))
