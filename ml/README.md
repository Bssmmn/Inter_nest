# InterNest roommate preference experiment

Lab Assignment №6. The experiment predicts stated ratings of hypothetical roommate profiles in a US conjoint survey. Read the [academic report](reports/lab-06.md) and open the [executed notebook](notebooks/roommate_prediction.ipynb) to see the analysis and outputs.

## Reproduce

From the repository root, create an isolated Python environment, install the dependencies and follow the [data acquisition instructions](data/README.md).

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r ml/requirements.txt
python -m nbconvert --to notebook --execute --inplace ml/notebooks/roommate_prediction.ipynb
```

The notebook uses a pinned input hash, a fixed split seed and scikit-learn pipelines. It requires a Jupyter kernel environment with local socket access. In the restricted development session, the notebook cells were executed sequentially in an in-process IPython session and their tables and figures were saved back to the notebook.

## GitHub issue draft

**Evaluate whether lifestyle attributes predict stated roommate ratings (Lab №6)**

Study whether bedtime and cleanliness improve held-out rating prediction over a training-mean baseline. Deliver reproducible offline evaluation and an academic report to inform the design of InterNest's future feedback studies.

- [ ] Document the versioned dataset, target, eligibility coverage and limitations.
- [ ] Verify data integrity, retain real labels and enforce the predictor allowlist.
- [ ] Run respondent-disjoint evaluation, compare three models and save learning curves and outputs.
- [ ] Document how InterNest can evaluate the SRS recommenders on independent local feedback.
- [ ] Verify the change is confined to `ml/` and submit a reviewed pull request from `experiment/roommate-ml`.

Link this issue to the MVP's content-based evaluation work when that issue is identifiable. The course experiment has its own dependency file and no runtime imports from the application.
