# Input data expected by the analysis code

The participant-level data are not released (see the top-level README). This file describes the inputs so that the code can be read and checked against the aggregate results.

```
<data_root>/
  sites.json                          {"social": "<substring of the host name>", "chatbot": "...", "search": "..."}
  recruitment/approved_ids.csv        one column, prolific_id: the retained participants
  survey/session_code_mapping.csv     prolific_id, session_code, response_id
  survey/responses_export.json        survey export: {"responses": [{"responseId", "values": {"QID..": code, "duration": seconds}}]}
  logs/by_table/<table>.csv           one file per log table (below)
  logs/by_participant/*.json          optional: {"participant_code", "tables": {<table>: [rows]}} for logs exported per participant
```

Log tables and the columns the code uses:

| Table | One row per | Columns used |
| --- | --- | --- |
| text_warning_metrics | episode of flagged text | set_id, export_participant_id, domain |
| text_anonymisation_attempts | request for suggestions | attempt_id, set_id, explanation_open_count, end_reason, requested_at |
| text_replacement_interactions | displayed suggestion | replacement_id, attempt_id, displayed_at, outcome (accepted, dismissed, unresolved, invalidated, pending), action_source (individual, apply_all), response_ms, category |
| anonymization_requests | request received by the backend | request_id, attempt_id, domain, text, request_metadata |
| usage_metrics | extension usage counter | read but not analysed |

Survey variables are mapped from question identifiers in `data.py` (`SURVEY_NAMES`); the wording of each question is in `materials/survey_instrument.md` under the same identifier. Records on domains other than the three study websites are dropped when the logs are loaded.
