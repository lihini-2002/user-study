# Results (n = 50)

Dataset: 50 participants, 2329 warning sets on study sites, 135 suggestion requests from 37 participants, 510 displayed suggestions. Seed 20261111, 10,000 bootstrap draws, participants resampled as whole units.

## RQ1: comprehension and self-rated understanding

| comprehension_item                        | correct        | correct_requesters   | correct_non_requesters   | self_rated_agree   |
|:------------------------------------------|:---------------|:---------------------|:-------------------------|:-------------------|
| Underlining means potentially sensitive   | 49/50 (98.0%)  | 36/37 (97.3%)        | 13/13 (100.0%)           | 49/50 (98.0%)      |
| Anonymisation reduces identifiability     | 50/50 (100.0%) | 37/37 (100.0%)       | 13/13 (100.0%)           |                    |
| Advice depends on information and website | 47/50 (94.0%)  | 37/37 (100.0%)       | 10/13 (76.9%)            | 48/50 (96.0%)      |
| Lower score means relatively lower risk   | 40/50 (80.0%)  | 32/37 (86.5%)        | 8/13 (61.5%)             | 37/50 (74.0%)      |

## RQ1: endorsement of explanation items by actual exposure

| group                                  |   n | agree_explanations_helped   | agree_enough_choice_over_suggestions   |
|:---------------------------------------|----:|:----------------------------|:---------------------------------------|
| Never requested a suggestion           |  13 | 10/12 (83.3%)               | 10/13 (76.9%)                          |
| Requested, never opened an explanation |  12 | 12/12 (100.0%)              |                                        |
| Opened an explanation at least once    |  25 | 23/24 (95.8%)               |                                        |

Participants who never saw a suggestion panel still endorse items about it, so experience items are reported with a requester-only check.

Explanation opened in 54/135 (40.0%) of requests, by 25 of 37 requesters.

## RQ2: what happened to displayed suggestions

| measure                                       | value           | interval_or_note                           |
|:----------------------------------------------|:----------------|:-------------------------------------------|
| Displayed suggestions accepted                | 286/510 (56.1%) | 44.2-66.9%                                 |
| Displayed suggestions dismissed               | 12/510 (2.4%)   | 3 participants                             |
| Displayed suggestions left without a decision | 212/510 (41.6%) | 136 unresolved; 62 invalidated; 14 pending |
| Accepted among explicit decisions             | 286/298 (96.0%) | 90.3-100.0%                                |
| Acceptances made with Apply All               | 194/286 (67.8%) | 23 participants                            |
| Median response time, Apply All (s)           | 4.5             | median of participant medians              |
| Median response time, individual accept (s)   | 9.3             | median of participant medians              |

## RQ2: behaviour types from the logs

| behaviour_type               |   participants |   share_of_50 |
|:-----------------------------|---------------:|--------------:|
| Bulk accept only             |             13 |        26.000 |
| Accepted some, left the rest |             12 |        24.000 |
| Requested, then left         |              8 |        16.000 |
| Selective (ever dismissed)   |              3 |         6.000 |
| Accepted all, one by one     |              1 |         2.000 |
| Never requested              |             13 |        26.000 |

## RQ2: stated conflict preference by behaviour type

| stated_conflict          |   Bulk accept only |   Accepted some, left the rest |   Requested, then left |   Selective (ever dismissed) |   Accepted all, one by one |   Never requested |   n |
|:-------------------------|-------------------:|-------------------------------:|-----------------------:|-----------------------------:|---------------------------:|------------------:|----:|
| Depends on the situation |                  6 |                              7 |                      3 |                            2 |                          1 |                 9 |  28 |
| Follow my own judgement  |                  7 |                              5 |                      5 |                            1 |                          0 |                 3 |  21 |
| Follow the tool          |                  0 |                              0 |                      0 |                            0 |                          0 |                 1 |   1 |

Of 29 participants who made any explicit decision, 26 never dismissed a suggestion. Of 21 who say they would follow their own judgement in a conflict, 1 dismissed anything (18 of them requested suggestions).

Stated control: {'Tool recommends, I decide': 47, 'I decide without recommendations': 2, 'Tool acts for me': 1}.

## RQ2: acceptance by destination

| destination   |   requesters | accepted_of_displayed   | cluster_95_interval   | accepted_of_explicit   |
|:--------------|-------------:|:------------------------|:----------------------|:-----------------------|
| social        |           30 | 102/179 (57.0%)         | 42.2-72.1%            | 102/107 (95.3%)        |
| chatbot       |           30 | 96/194 (49.5%)          | 34.5-64.5%            | 96/103 (93.2%)         |
| search        |           32 | 88/137 (64.2%)          | 48.2-78.7%            | 88/88 (100.0%)         |

Within participants with suggestions on all three destinations (n = 22): mean acceptance social 0.65, chatbot 0.63, search 0.75; Friedman chi2 = 4.19, p = 0.123. GEE (logit, participant clusters), odds ratios versus social: chatbot 0.71 (p = 0.221), search 1.29 (p = 0.511).

## RQ2: acceptance of task-needed versus incidental information

| coding                         | scope                   | needed_accepted   | incidental_accepted   |   paired_participants | needed_higher/equal/lower   |   wilcoxon_p |   gee_odds_ratio_needed | gee_95_ci   |   gee_p |
|:-------------------------------|:------------------------|:------------------|:----------------------|----------------------:|:----------------------------|-------------:|------------------------:|:------------|--------:|
| agreed codes only              | all displayed           | 64/103 (62.1%)    | 122/225 (54.2%)       |                    34 | 13/14/7                     |        0.135 |                   1.280 | 0.80-2.05   |   0.303 |
| agreed codes only              | explicit decisions only | 64/68 (94.1%)     | 122/125 (97.6%)       |                    22 | 0/21/1                      |        0.317 |                   0.580 | 0.10-3.35   |   0.539 |
| agreed codes only              | chatbot only            | 40/60 (66.7%)     | 32/86 (37.2%)         |                    19 | 8/11/0                      |        0.011 |                   3.420 | 1.54-7.61   |   0.003 |
| disputed counted as needed     | all displayed           | 164/285 (57.5%)   | 122/225 (54.2%)       |                    34 | 10/14/10                    |        0.370 |                   1.110 | 0.71-1.76   |   0.645 |
| disputed counted as needed     | explicit decisions only | 164/173 (94.8%)   | 122/125 (97.6%)       |                    23 | 1/20/2                      |        0.285 |                   0.470 | 0.06-3.88   |   0.480 |
| disputed counted as needed     | chatbot only            | 64/108 (59.3%)    | 32/86 (37.2%)         |                    20 | 7/11/2                      |        0.037 |                   2.100 | 1.12-3.93   |   0.020 |
| disputed counted as incidental | all displayed           | 64/103 (62.1%)    | 222/407 (54.5%)       |                    36 | 15/15/6                     |        0.025 |                   1.320 | 0.92-1.89   |   0.127 |
| disputed counted as incidental | explicit decisions only | 64/68 (94.1%)     | 222/230 (96.5%)       |                    26 | 0/24/2                      |        0.180 |                   0.610 | 0.39-0.95   |   0.030 |
| disputed counted as incidental | chatbot only            | 40/60 (66.7%)     | 56/134 (41.8%)        |                    26 | 9/16/1                      |        0.066 |                   2.530 | 1.34-4.79   |   0.004 |

Needed = the task as worded cannot be completed as intended once the information is replaced. Codes are those of two independent coders; 'disputed' marks the combinations on which they disagreed. An odds ratio below 1 would mean needed information is accepted for removal less often.

## RQ2: outcomes by task and information type

| task         | cat          |   displayed |   accepted |   dismissed | need       |   accept_pct |
|:-------------|:-------------|------------:|-----------:|------------:|:-----------|-------------:|
| chat_caption | Location     |          25 |          7 |           1 | disputed   |       28.000 |
| chat_caption | Personal     |          59 |         14 |           1 | incidental |       23.700 |
| chat_caption | Relationship |           9 |          6 |           0 | incidental |       66.700 |
| chat_health  | Age          |          29 |         18 |           2 | needed     |       62.100 |
| chat_health  | Health       |          31 |         22 |           1 | needed     |       71.000 |
| chat_health  | Location     |          23 |         17 |           0 | disputed   |       73.900 |
| chat_health  | Organisation |           1 |          1 |           0 | incidental |      100.000 |
| chat_health  | Personal     |           9 |          3 |           2 | incidental |       33.300 |
| chat_other   | Bank Account |           4 |          4 |           0 | incidental |      100.000 |
| chat_other   | Email        |           2 |          2 |           0 | incidental |      100.000 |
| chat_other   | Phone        |           2 |          2 |           0 | incidental |      100.000 |
| search_bank  | Bank Account |          66 |         42 |           0 | incidental |       63.600 |
| search_bank  | Email        |          33 |         21 |           0 | incidental |       63.600 |
| search_bank  | Personal     |           5 |          4 |           0 | incidental |       80.000 |
| search_bank  | Phone        |          33 |         21 |           0 | incidental |       63.600 |
| social_post  | Age          |           1 |          1 |           0 | incidental |      100.000 |
| social_post  | Health       |           1 |          1 |           0 | incidental |      100.000 |
| social_post  | Location     |          43 |         24 |           1 | needed     |       55.800 |
| social_post  | Personal     |         110 |         57 |           4 | disputed   |       51.800 |
| social_post  | Relationship |          24 |         19 |           0 | disputed   |       79.200 |

## RQ2: reasons selected for dismissing or overriding (multiple response)

|   choice_code |   participants |
|--------------:|---------------:|
|             1 |             34 |
|             2 |             25 |
|             3 |             11 |
|             4 |              4 |
|             5 |             19 |
|             6 |             21 |
|             7 |              1 |

49 participants selected at least one reason. Choice codes follow the survey export; see materials/survey_instrument.md for the wording.

## RQ3: paired comfort comparisons

| comparison                           |   pairs |   first_higher |   equal |   first_lower |   wilcoxon_p |   holm_p |
|:-------------------------------------|--------:|---------------:|--------:|--------------:|-------------:|---------:|
| Reading text vs text sent to backend |      50 |             26 |      22 |             2 |        0.000 |    0.000 |
| Reading text vs website details sent |      49 |             24 |      20 |             5 |        0.000 |    0.000 |
| Text sent vs website details sent    |      49 |              9 |      31 |             9 |        0.406 |    0.406 |

## RQ3: necessity, expectations and transmission before disclosure

| measure                                                            | value         |
|:-------------------------------------------------------------------|:--------------|
| Agree access is necessary                                          | 43/50 (86.0%) |
| ... of whom uncomfortable with text sent to backend                | 15/43 (34.9%) |
| ... of whom not comfortable (uncomfortable or neutral)             | 24/43 (55.8%) |
| ... of whom would take fewer features for less access              | 19/42 (45.2%) |
| Expected mostly local processing                                   | 40/50 (80.0%) |
| Expected local and did not expect external processing              | 24/50 (48.0%) |
| Requesters (sent text to backend before the disclosure)            | 37            |
| ... later uncomfortable with text sent to backend                  | 15/37 (40.5%) |
| ... later neutral                                                  | 8/37 (21.6%)  |
| ... later comfortable                                              | 14/37 (37.8%) |
| ... had expected mostly local processing                           | 29/37 (78.4%) |
| Accepted at least one suggestion, later uncomfortable with backend | 13/29 (44.8%) |

## RQ4: scale reliability

| scale                    |   items |   cronbach_alpha |   mean |    sd |
|:-------------------------|--------:|-----------------:|-------:|------:|
| Data-practice comfort    |       6 |            0.894 |  3.488 | 0.775 |
| Self-rated understanding |       5 |            0.792 |  4.324 | 0.546 |
| Burden                   |       2 |            0.678 |  2.280 | 0.803 |
| Experienced control      |       2 |            0.848 |  4.290 | 0.655 |
| Adoption intent          |       3 |            0.838 |  3.520 | 0.844 |
| Baseline privacy concern |       3 |            0.824 |  4.153 | 0.713 |

## RQ4: what goes with adoption intent (Spearman, bootstrap 95% intervals)

| construct                           |   n |   rho_with_adoption_scale |   ci_low |   ci_high |   rho_with_willingness_item |   item_ci_low |   item_ci_high |   item_n |
|:------------------------------------|----:|--------------------------:|---------:|----------:|----------------------------:|--------------:|---------------:|---------:|
| Data-practice comfort               |  50 |                     0.710 |    0.520 |     0.839 |                       0.653 |         0.445 |          0.802 |       49 |
| Self-rated understanding            |  50 |                     0.422 |    0.196 |     0.611 |                       0.340 |         0.088 |          0.561 |       49 |
| Burden                              |  50 |                    -0.394 |   -0.624 |    -0.115 |                      -0.317 |        -0.546 |         -0.041 |       49 |
| Experienced control                 |  50 |                     0.080 |   -0.217 |     0.358 |                       0.047 |        -0.261 |          0.351 |       49 |
| Baseline privacy concern            |  50 |                     0.016 |   -0.305 |     0.333 |                       0.139 |        -0.173 |          0.425 |       49 |
| Item: comfort, text sent to backend |  50 |                     0.603 |    0.376 |     0.773 |                       0.600 |         0.400 |          0.753 |       49 |
| Item: comfort, tool reads text      |  50 |                     0.549 |    0.317 |     0.731 |                       0.501 |         0.237 |          0.720 |       49 |
| Item: interrupted more than liked   |  50 |                    -0.474 |   -0.669 |    -0.234 |                      -0.426 |        -0.640 |         -0.173 |       49 |
| Item: too much effort               |  50 |                    -0.267 |   -0.537 |     0.047 |                      -0.165 |        -0.440 |          0.130 |       49 |
| Item: understood the risk score     |  50 |                     0.428 |    0.200 |     0.618 |                       0.391 |         0.129 |          0.607 |       49 |

## RQ4: adoption intent regressed on all five constructs

| predictor                |   std_beta |   ci_low |   ci_high |   leave_one_out_min |   leave_one_out_max |
|:-------------------------|-----------:|---------:|----------:|--------------------:|--------------------:|
| Data-practice comfort    |      0.706 |    0.495 |     0.882 |               0.653 |               0.757 |
| Self-rated understanding |      0.117 |   -0.053 |     0.301 |               0.083 |               0.145 |
| Burden                   |     -0.239 |   -0.493 |    -0.014 |              -0.296 |              -0.177 |
| Experienced control      |     -0.207 |   -0.410 |    -0.009 |              -0.242 |              -0.163 |
| Baseline privacy concern |      0.085 |   -0.127 |     0.297 |               0.042 |               0.134 |

Ordinary least squares on standardised scale scores, n = 50, R2 = 0.63. Intervals are bootstrap percentile intervals.

## RQ4: willingness by comfort with text sent to the backend

| comfort_text_sent_to_backend   |   Unwilling |   Neutral |   Willing |
|:-------------------------------|------------:|----------:|----------:|
| Uncomfortable                  |           6 |         5 |         6 |
| Neutral                        |           5 |         0 |         7 |
| Comfortable                    |           0 |         1 |        19 |

## Appendix: survey results by requester status

| group            |   n | score_item_correct   | comfortable_reading   | comfortable_backend   | expected_local   | willing       | want_recommend_i_decide   |   rho_data_comfort_adoption |
|:-----------------|----:|:---------------------|:----------------------|:----------------------|:-----------------|:--------------|:--------------------------|----------------------------:|
| All participants |  50 | 40/50 (80.0%)        | 37/50 (74.0%)         | 20/50 (40.0%)         | 40/50 (80.0%)    | 32/49 (65.3%) | 47/50 (94.0%)             |                       0.710 |
| Requesters only  |  37 | 32/37 (86.5%)        | 26/37 (70.3%)         | 14/37 (37.8%)         | 29/37 (78.4%)    | 22/37 (59.5%) | 34/37 (91.9%)             |                       0.657 |
| Never requested  |  13 | 8/13 (61.5%)         | 11/13 (84.6%)         | 6/13 (46.2%)          | 11/13 (84.6%)    | 10/12 (83.3%) | 13/13 (100.0%)            |                       0.857 |

## Planned tests (Spearman, bootstrap 95% interval, permutation p, Holm-adjusted)

| planned_association                                                      |   n |   spearman_rho |   ci_low |   ci_high |   permutation_p |   holm_p |
|:-------------------------------------------------------------------------|----:|---------------:|---------:|----------:|----------------:|---------:|
| Context item correct with self-rated understanding of context dependence |  50 |          0.268 |    0.089 |     0.461 |           0.088 |    0.176 |
| Overall comfort with data practices with willingness to use              |  49 |          0.684 |    0.487 |     0.835 |           0.000 |    0.000 |
| Perceived effort with willingness to use                                 |  49 |         -0.165 |   -0.434 |     0.133 |           0.256 |    0.256 |

## Survey items: responses in the top two, middle and bottom two of five options

| item                                                | variable     |   n |   top_two |   middle |   bottom_two |   top_two_pct |
|:----------------------------------------------------|:-------------|----:|----------:|---------:|-------------:|--------------:|
| Bothered when websites ask for personal information | c_bother     |  50 |        33 |       14 |            3 |        66.000 |
| Thinks twice before sharing                         | c_twice      |  50 |        46 |        3 |            1 |        92.000 |
| Websites collect too much                           | c_collect    |  50 |        38 |       11 |            1 |        76.000 |
| Understood why information was flagged              | u_flag       |  50 |        49 |        1 |            0 |        98.000 |
| Understood why advice differs across websites       | u_ctx        |  50 |        48 |        1 |            1 |        96.000 |
| Understood the risk score                           | u_score      |  50 |        37 |       10 |            3 |        74.000 |
| Advice easy to understand                           | u_easy       |  50 |        46 |        2 |            2 |        92.000 |
| Explanations helped                                 | u_expl       |  48 |        45 |        3 |            0 |        93.800 |
| Expected: reads typed text                          | e_read       |  50 |        47 |        1 |            2 |        94.000 |
| Expected: mostly local processing                   | e_local      |  50 |        40 |        5 |            5 |        80.000 |
| Expected: sends information to external servers     | e_ext        |  50 |        19 |       14 |           17 |        38.000 |
| Comfortable: reading text                           | cf_read      |  50 |        37 |        7 |            6 |        74.000 |
| Comfortable: text sent to backend                   | cf_backend   |  50 |        20 |       12 |           18 |        40.000 |
| Comfortable: website details and categories sent    | cf_meta      |  49 |        24 |        6 |           19 |        49.000 |
| Comfortable overall with data practices             | cf_overall   |  50 |        30 |       13 |            7 |        60.000 |
| Access is necessary                                 | a_necessary  |  50 |        43 |        4 |            3 |        86.000 |
| Access is reasonable                                | a_reasonable |  50 |        30 |       14 |            6 |        60.000 |
| Accesses more than expected                         | a_more       |  50 |        19 |       19 |           12 |        38.000 |
| Prefer fewer features for less access               | a_fewer      |  49 |        25 |       13 |           11 |        51.000 |
| Interrupted more than liked                         | b_interrupt  |  50 |         7 |        9 |           34 |        14.000 |
| Too much effort                                     | b_effort     |  50 |         8 |        6 |           36 |        16.000 |
| Number of warnings manageable                       | b_manage     |  50 |        43 |        5 |            2 |        86.000 |
| Protects privacy without preventing tasks           | b_compat     |  50 |        38 |        9 |            3 |        76.000 |
| Risk level influenced following advice              | b_riskinfl   |  50 |        35 |       13 |            2 |        70.000 |
| Willing to use                                      | w_use        |  49 |        32 |        6 |           11 |        65.300 |
| Benefit justifies use                               | w_benefit    |  50 |        30 |       13 |            7 |        60.000 |
| Fits how I browse                                   | w_fit        |  50 |        35 |        8 |            7 |        70.000 |
| Could easily override                               | ct_override  |  50 |        47 |        3 |            0 |        94.000 |
| Enough control over suggestions                     | ct_choice    |  50 |        43 |        5 |            2 |        86.000 |

Top two = agree / comfortable / expected.

## Sample description (choice codes follow the survey export)

| variable   |   choice_code |   participants |
|:-----------|--------------:|---------------:|
| age        |             2 |             10 |
| age        |             3 |             19 |
| age        |             4 |             21 |
| gender     |             1 |             22 |
| gender     |             2 |             27 |
| gender     |             3 |              1 |
| edu        |             1 |              7 |
| edu        |             2 |              6 |
| edu        |             3 |             22 |
| edu        |             4 |             15 |
| exp        |             2 |              1 |
| exp        |             3 |              6 |
| exp        |             4 |             18 |
| exp        |             5 |             25 |
| prior_ext  |             1 |             15 |
| prior_ext  |             2 |             35 |

Median session length 17.3 minutes (interquartile range 14.6-22.0).

Expected mostly local processing: 20/25 (80.0%) of participants who opened the explanation panel, 20/25 (80.0%) of those who never opened it.

Requests by site: {'chatbot': 55, 'social': 46, 'search': 34}; median requests per requester 4; median suggestions per request 4.
