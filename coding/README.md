# Task-need coding

- `coding_instructions.md`: the instruction given to each coder.
- `coding_sheet_blank.csv`: the 17 combinations of task and information type that occurred in the study tasks.
- `coder_A.csv`, `coder_B.csv`: the two coders' sheets (`needed`: Y or N; `unsure`: x if the coder thought the opposite code arguable; `note`: the coder's reason).

The coders agreed on 13 of 17 combinations (Cohen's kappa 0.44). `analysis/analysis.py` reads the two sheets, treats combinations on which the coders disagree as disputed, and reports the comparison with disputed combinations excluded, counted as needed, and counted as incidental.

Eight displayed suggestions came from two requests in which a participant pasted the bank message into the chatbot. They are not a study task and have no row here; the analysis gives them the codes of the bank-message rows.
