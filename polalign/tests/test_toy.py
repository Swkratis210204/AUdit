"""The toy dataset and the stand-in model of the tutorials: the planted structure must be found."""
import pandas as pd

from perspective_audit import annotate, run_dataset, save_au_tables, load_model_inputs
from perspective_audit.toy import standin_model, toy_ratings, toy_spec


def test_toy_attributes_the_planted_characteristics_only():
    result = run_dataset(toy_spec(), raw=toy_ratings())
    assert result.per_dimension["survived (AU)"].to_dict() == {"gender": 20, "politics": 20, "age": 0}


def test_standin_model_runs_without_any_api(tmp_path):
    result = run_dataset(toy_spec(), raw=toy_ratings())
    save_au_tables({"toy": result.au}, tmp_path)
    inputs = load_model_inputs(tmp_path / "aposteriori_for_models.csv")
    annotate(standin_model(), inputs, tmp_path, prompt=lambda texts, item: f"{item}s\n{texts}", run="baseline", show_progress=False)
    saved = pd.read_csv(tmp_path / "toy" / "baseline" / "standin.csv")
    assert len(saved) == 40 and set(saved["label"]) == {"toxic", "civil"}


def test_compare_prompts_sees_a_change_of_information_but_not_of_wording(tmp_path):
    from perspective_audit import compare_prompts

    result = run_dataset(toy_spec(), raw=toy_ratings())
    save_au_tables({"toy": result.au}, tmp_path)
    inputs = load_model_inputs(tmp_path / "aposteriori_for_models.csv")
    prompts = {"baseline": "Rate each {item}\n{texts}", "reworded": "Please rate every {item}\n{texts}", "strict": "Be strict, rate each {item}\n{texts}"}
    for run, template in prompts.items():
        annotate(standin_model(), inputs, tmp_path, prompt=lambda texts, item, t=template: t.format(item=item, texts=texts), run=run, show_progress=False)
    table = compare_prompts(tmp_path, ["toy"], list(prompts), ["standin"], reps=50).set_index(["first", "second"])
    assert table.loc[("baseline", "reworded"), "label_agreement_pct"] == 100.0
    assert table.loc[("baseline", "strict"), "label_agreement_pct"] == 50.0 and table.loc[("baseline", "strict"), "mean_shift"] > 0


def test_the_rules_of_the_analysis_are_parameters():
    from perspective_audit import attribution_gap

    raw = toy_ratings()
    default = run_dataset(toy_spec(min_au_texts=25), raw=raw)
    assert default.per_dimension["groups kept"].to_dict() == {"gender": 2, "politics": 2, "age": 2}          # every group is thin: the rule keeps them
    everything = run_dataset(toy_spec(), raw=raw, min_au_texts=0)                                         # 0: no 10-text rule, all AU texts
    assert everything.pruned["politics"].removed == [] and len(everything.au) == 40
    strict = run_dataset(toy_spec(), raw=raw, min_ratings=13)                                             # a group has 12 raters per text, so no group is big enough
    assert len(strict.au) == 0
    try:
        run_dataset(toy_spec(), raw=raw, min_texts=3)
        raise AssertionError("an unknown option must be refused")
    except TypeError:
        pass
    gap = attribution_gap({"toy": everything}, reps=50, demographic=("age",))                             # now only age is demographic
    assert gap.loc["toy", "testable D"] == 40 and gap.loc["toy", "attributed D"] == 0
