# Predicting Stated Roommate Desirability from Bedtime and Cleanliness

**Lab Assignment №6 · InterNest · Gehad Hamada**

## 1. Problem and research question

Can two candidate household characteristics predict stated willingness to live with a hypothetical roommate among held-out US college students? The applied aim is to assess whether these attributes carry enough predictive signal to justify testing preference-aware models on locally collected data. This is supervised regression on a bounded ordinal rating.

## 2. Data and provenance

Shafranek's randomized conjoint study varied 11 candidate attributes. Students rated profiles on a 1–7 scale and chose between pairs in up to ten tasks. The rating measures stated willingness, and the choice is forced without an opt-out. The paper reports 205 participants. The standardized Item Response Warehouse v5.0 raw export labels its license CC0 1.0 and includes 203 respondents. The author's Harvard Dataverse archive was inaccessible during execution, so provenance traces through the standardized export. Its version, retrieval link and SHA-256 are recorded with the notebook.

The file has 4,036 observations and 57 columns. An older index reports 4,030 rows. The byte-audited v5.0 export controls this analysis. Rating is missing in 720 rows and choice in 82. Respondent, task and profile form a unique key. Repeated lifestyle combinations are distinct judgments and are retained. Complete-case training can be biased if rating availability depends on the users, profiles or survey process.

| Survey variable | InterNest relevance | Role |
|---|---|---|
| Candidate bedtime | Partial measure of sleep schedule. A single weekday or typical bedtime does not describe an entire routine. | Predictor |
| Candidate cleanliness | Overlaps own household cleanliness behavior. | Predictor |
| Respondent own bedtime and cleanliness | Own behavior is a different concept from desired roommate behavior. Own cleanliness also has ambiguous exported numeric-looking codes. | Omitted |
| Weekend social activity | Coarse proxy for social behavior. It does not measure household guest frequency or noise. | Omitted |
| Hobbies, music and values | Outside the relevant MVP preference fields and may convey identity proxies. | Omitted |
| Race, religion, sexual orientation, political interest and affiliation, respondent demographics | Sensitive or unnecessary for household matching. | Omitted |
| Budget, move-in, stay, smoking acceptance, pets and explicit dealbreakers | Key InterNest fields without comparable candidate constraints in the survey. | Unavailable |
| Rating, forced choice and respondent/task/profile | Rating is the regression outcome. Choice supports secondary evaluation. Keys support grouping and audits. | Never model inputs |

The Hugging Face Lifestyle Preferences Dataset shows 10,000 individual lifestyle profiles and advertises MIT licensing. The public schema has no observed pair-level outcomes, and its collection and annotation methods are undocumented. It cannot independently validate a ranking or establish the origin or real-world status of records. The Finnish Social Science Data Archive publishes open student housing preference data for Tampere, which could support a separately scoped housing-preference assignment. The Sabancı research uses student surveys for dorm-room assignment and friend preferences, but the public materials I found did not provide a verified downloadable individual rating dataset for this experiment. The search did not establish a comparable public dataset for Kazakhstan, Russia, Türkiye, Eastern Europe or nearby Asian countries.

## 3. Literature

1. Hoerl and Kennard (1970), [Ridge Regression: Biased Estimation for Nonorthogonal Problems](https://doi.org/10.1080/00401706.1970.10488634). The authors introduce coefficient shrinkage to trade bias for lower variance. Ridge provides an additive comparison for the one-hot lifestyle features.
2. Breiman (2001), [Random Forests](https://doi.org/10.1023/A:1010933404324). Randomized trees combine diverse predictors through averaging. A shallow forest tests whether interactions add useful predictive signal to the additive model.
3. Shafranek (2021), [Political Considerations in Nonpolitical Decisions](https://doi.org/10.1007/s11109-019-09554-9). The paper studies the role of politics and lifestyle in hypothetical roommate selection, and provides the source instrument and outcomes for this secondary analysis.
4. Hainmueller, Hopkins and Yamamoto (2014), [Causal Inference in Conjoint Analysis](https://doi.org/10.1093/pan/mpt024). The authors formalize randomized multidimensional stated-preference experiments. Their work explains why the survey supports distinct profile-level judgments and why this predictive analysis alone supplies no causal estimate.

## 4. EDA and methods

The [notebook](../notebooks/roommate_prediction.ipynb) records data types, missingness, exact duplicates, key uniqueness, valid rating bounds, training target distribution, category distribution, group means and an indicator-based correlation plot. The rating endpoints are valid observations. Both predictors are categorical and require no numerical outlier removal or scaling. The pipeline assigns an explicit missing category if needed and fits one-hot encoding on training rows only. Missing outcomes are omitted before modeling.

The fixed seed is 42. The split is approximately 70/15/15 by respondent, with both profiles per task assigned to the same partition. The three candidates are a mean baseline, ridge regression with alpha 10, and a 200-tree forest of maximum depth four and minimum leaf size 30. Holding these settings fixed keeps the comparison small enough for oral defense. Validation MAE selects the model. Test MAE measures average absolute rating-point error, RMSE penalizes larger errors, and R² benchmarks against test-mean squared error. The notebook plots train/validation MAE by training respondent count and provides a respondent bootstrap interval for the paired test MAE difference. Fixed holding sets make the curves descriptive of this partition.

## 5. Results

Regression used 3,316 ratings from 199 respondents. The partitions contained 2,290 / 515 / 511 rows from 139 / 30 / 30 respondents respectively. In training, rating 5 was most common (759 rows). Mean ratings across cleanliness categories differed by up to 0.43 points. Membership in the lowest cleanliness category had the strongest rating correlation among the predictors (r = −0.14).

| Model | Validation MAE | Test MAE | Test RMSE | Test R² |
|---|---:|---:|---:|---:|
| Mean baseline | 1.2818 | 1.1359 | 1.3454 | −0.0001 |
| Ridge | 1.2496 | 1.1059 | 1.3222 | 0.0341 |
| Shallow forest | 1.2473 | 1.1017 | 1.3209 | 0.0360 |

The forest won on validation MAE, with a test improvement of 0.0341 rating points over the training mean. Its paired respondent-bootstrap interval for the test MAE difference was [−0.0591, −0.0121]. This interval is conditional on the fitted model and held-out sample and does not estimate transfer uncertainty. The forest's R² was 0.036 and its test MAE was only 0.0042 lower than ridge's. The learning curves show small changes in validation MAE across training sizes and a persistent training/validation gap even for the mean baseline, so the gap alone is weak evidence of forest overfitting.

Across 230 complete rated test pairs, with ties counting half, agreement with forced choice was 50.0% for the mean, 69.8% for ridge and 67.2% for the forest. This is exploratory evidence about relative choices in the survey. The study forced a selection and many pairs with incomplete ratings were excluded. Agreement and absolute rating error answer different questions, and the choice result does not change the prespecified model selection.

## 6. Limitations and product implications

Respondents rated US hypothetical profiles that included sensitive attributes visible to them during the study. Removing those columns from the predictors reduces direct use but does not remove the influence they may have had on the labels. The two allowed features predict aggregate desirability with only nine possible input combinations. They omit stated preferences about the candidate and cannot personalize rankings or test reciprocal eligibility. Missing outcomes, a single grouped split, score-scale assumptions and the modest number of independent test respondents limit interpretation. The experiment provides a baseline methodology and modest evidence about two attributes in this sample. Cohabitation success in Almaty requires its own outcome and validation.

For the MVP, implement SRS FR-08 and FR-09 with a shared eligibility check for account visibility, blocking, city, budget, dates, stay and both parties' explicit dealbreakers. Compare each person's desired behavior with the other's reported behavior. Use documented component weights or mixed-feature distance and return concise reasons derived from the matching fields. Treat missing and explicitly indifferent answers as distinct states. Use identical eligible pools and independent consenting ratings to compare methods with Precision@5 and NDCG@5. Document judgments, short lists and unjudged candidates.

Under FR-12, collect optional directional judgments (relevant / unsure / not relevant) independently of interest acceptance. Explain research use, eligibility for inclusion, access, retention and withdrawal. Keep contact details, identity fields and free-text reasons outside model inputs. Where possible, gather judgments across eligible candidates shown in varying order to limit exposure bias. Record which candidate was shown and the method/version, with separate storage controls for feedback data. An unseen candidate or unanswered prompt stays unlabeled. If enough consenting data accumulates, train a new model on pairwise compatibility features using only local labels, and compare it with the existing ranker on disjoint participants and a later cohort. Where candidate profiles repeat across users, design the holdout around both parties or clearly state which party is unseen. Track coverage, exclusion behavior and recommendation quality before any rollout. A later, voluntarily reported cohabitation outcome would require a separate protocol and evaluation.

## 7. Dataset resources

- [Item Response Warehouse table and CC0 designation](https://itemresponsewarehouse.org/tables/shafranek_2021_roommate_choice/)
- [Original Harvard Dataverse deposit](https://doi.org/10.7910/DVN/GUATS6)
- [Hugging Face Lifestyle Preferences Dataset](https://huggingface.co/datasets/cive202/Lifestyle_Preferences_Dataset)
- [Tampere student housing preferences data](https://services.fsd.tuni.fi/catalogue/FSD3021?lang=en)
- [Sabancı dorm assignment study](https://research.sabanciuniv.edu/52839/1/Finding.pdf)
