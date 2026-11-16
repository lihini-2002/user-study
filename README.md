# Artifact for "The Assistant Is a Recipient Too: How People Understand, Follow and Accept Disclosure-Time Privacy Assistance"

Anonymous artifact for review. It contains the study materials, the task-need coding, the analysis code, and the aggregate results behind every table and figure of the paper.

## Contents

| Folder | What it holds |
| --- | --- |
| `materials/` | The full survey instrument, including the three persona and task scripts, the guide shown before the tasks, and the disclosure text. |
| `coding/` | Instruction, blank sheet and the two coders' sheets for the task-need coding. |
| `analysis/` | `data.py` (loading), `analysis.py` (all tables and tests), `figures.py` (Figures 2 to 6), pinned `requirements.txt`, and `DATA_FORMAT.md`. |
| `results/` | `RESULTS.md` (readable summary), `tables/` (one CSV per analysis), `figures/` (PDF and PNG). |

## What is not included, and why

Participant-level survey responses and interaction logs are not released. The logs contain the text participants typed, and the consent form permits sharing participant-level data only with approved researchers. The analysis code therefore cannot be rerun from this repository alone; it is provided so that every reported number can be traced to the computation that produced it, and `analysis/DATA_FORMAT.md` documents the inputs. Links to the study websites and to the extension, and the consent page, are removed for anonymous review.

## Where each result in the paper comes from

| Paper | File in `results/tables/` |
| --- | --- |
| Section 4.4, sample description | `sample.csv`, `survey_items.csv` (baseline concern items) |
| Table 3, RQ1 | `rq1_comprehension.csv`, `rq1_selfreport_vs_exposure.csv` |
| Figure 3, outcomes of suggestions | `rq2_outcomes.csv`, `rq2_by_destination.csv` |
| Figure 4, stated and enacted control | `rq2_behaviour_types.csv`, `rq2_stated_vs_enacted.csv`, `rq2_override_reasons.csv` |
| Table 4 and Appendix B.2, task need | `rq2_task_need.csv`, `rq2_task_by_category.csv` |
| Figure 5 and RQ3 | `survey_items.csv`, `rq3_comfort_paired.csv`, `rq3_necessity_and_prior_transmission.csv` |
| Planned tests | `planned_tests.csv` |
| Figure 6 and RQ4 | `rq4_scale_reliability.csv`, `rq4_adoption_correlates.csv`, `rq4_adoption_regression.csv`, `rq4_willing_by_backend_comfort.csv` |
| Appendix B.1, requesters and non-requesters | `appendix_survey_by_group.csv` |

## Running the code (with access to the data)

```
pip install -r analysis/requirements.txt        # Python 3.13
python3 analysis/analysis.py <data_root> <output_dir>
python3 analysis/figures.py <output_dir>
```

`analysis.py` writes participant-level working files to `<output_dir>/private/` for `figures.py`; that folder must not be shared. The random seed is fixed (20261111) and all intervals use 10,000 resamples of whole participants.

## Licence

Study materials and results: CC BY 4.0. Code: MIT.
