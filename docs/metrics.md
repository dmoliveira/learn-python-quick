# Metrics field guide

A metric is a compressed view of behavior. Always pair it with the split method, a baseline, and an
error analysis. Report uncertainty when decisions matter.

## Regression

| Metric | Good for | Watch out for |
|---|---|---|
| MAE | Typical error in target units | Treats all error sizes linearly |
| RMSE | Making large errors more costly | Sensitive to outliers; same units as target |
| R² | Variance explained relative to a mean baseline | Can be negative; not an error in target units |

Avoid MAPE when targets can be zero or close to zero.

## Classification

| Metric | Good for | Watch out for |
|---|---|---|
| Accuracy | Balanced classes and equal error costs | Hides minority-class failure |
| Precision | False positives are expensive | Says nothing about missed positives |
| Recall | False negatives are expensive | Says nothing about false alarms |
| F1 | Balance of precision and recall | Ignores true negatives and probability quality |
| ROC-AUC | Ranking positives above negatives | Can look optimistic with rare positives |
| PR-AUC | Rare positive ranking | Depends strongly on prevalence |
| Log loss / Brier | Probability quality | Requires well-defined probabilities |

Always inspect a confusion matrix. For multiclass data, state whether averages are macro, micro, or
weighted. Macro gives each class equal weight.

## Retrieval and recommenders

- **Precision@K:** relevant results among the first K recommendations.
- **Recall@K:** known relevant items found in the first K.
- **MRR:** rewards the rank of the first relevant result.
- **NDCG@K:** rewards relevant items near the top and can use graded relevance.

State K, the candidate set, relevance definition, and split method. A temporal split often reflects
recommendation use better than a random split. Compare with popularity before a complex model.
Ranking outputs must contain unique item IDs; duplicates can make Recall@K or NDCG invalid.

## Embeddings and images

Use Recall@K/MRR for embedding retrieval and Spearman correlation for labeled similarity scores.
For image classification, start with top-1 accuracy, macro-F1, and a confusion matrix. Detection and
segmentation need different metrics such as mAP, IoU, or Dice.

## A minimum evaluation card

```text
Decision: Which action will use this output?
Split: How were train, validation, and test separated?
Baseline: What simple rule must the model beat?
Primary metric: Why does it match the decision cost?
Slices: Which groups or input ranges fail?
Uncertainty: How stable is the result across samples or seeds?
```
