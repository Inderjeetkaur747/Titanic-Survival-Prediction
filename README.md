Dataset: Titanic Survival Prediction

Level 1 — Data Preparation & Baseline Model

1. Dataset Selection

I selected the Titanic dataset from Kaggle, which contains data on passengers,
including personal details, ticket information, and survival status. This dataset is
suitable for classification tasks since the target variable, Survived, is binary (0 = did
not survive, 1 = survived).

Dataset Features:
• PassengerId: Unique identifier
• Pclass: Ticket class (1 = 1st, 2 = 2nd, 3 = 3rd)
• Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked
• Survived: Target variable (0/1)

3. Data Preparation
- Dropped columns: PassengerId, Name, Ticket, Cabin (irrelevant or too many
missing values).
- Missing value handling:
 - Age: filled with median.
 - Embarked: filled with mode.
- Categorical encoding:
 - Sex and Embarked encoded with label encoding.
- Feature scaling:
 - StandardScaler used to scale numeric features before training (improves Logistic
Regression convergence).
- Train/test split:
 - 80% train / 20% test, random_state=42.
   
3. Exploratory Data Analysis (key findings)
   
- Females had notably higher survival rates.
- Higher passenger class (Pclass = 1) correlates with higher survival.
- Fare is positively correlated with survival (higher fare → higher chance).
- No major outliers after inspection that required removal for this baseline.
  
4. Baseline Models (implementation)
   
- Models trained with default parameters:
 - Logistic Regression
 - Decision Tree
 - Random Forest
   
5. Results (from my run)
   
- Logistic Regression — Evaluation Metrics:
 - Accuracy: 0.81
 - Precision: 0.79
 - Recall: 0.74
 - F1 Score: 0.76
- Decision Tree — Evaluation Metrics:
 - Accuracy: 0.78
 - Precision: 0.72
 - Recall: 0.77
 - F1 Score: 0.75
- Random Forest — Evaluation Metrics:
 - Accuracy: 0.82
 - Precision: 0.81
 - Recall: 0.74
 - F1 Score: 0.77
   
6. Interpretation
   
- Logistic Regression provides a strong, simple baseline (0.81 accuracy), capturing
major linear effects such as Sex and Pclass.
- Random Forest (default) slightly outperformed Logistic Regression (0.82)
indicating the presence of some non-linear interactions that ensemble trees
capture.
- Decision Tree performed slightly worse than the ensemble, as expected (single
tree -> higher variance).
- At this stage (Level 1) the best performing baseline is Random Forest (default),
but Logistic Regression remains a good, interpretable baseline.


Level 2 — Model Optimization & Explainability

To improve the model’s performance using hyperparameter tuning, new feature
creation, and interpretability tools like LIME and SHAP.

Approach

1. Added two new features — FamilySize and IsAlone — to help the model
understand family travel patterns.
2. Used 5-fold GridSearchCV on Random Forest to find the best
hyperparameters.
3. Tested XGBoost as an advanced model for comparison.
4. Used LIME to explain individual predictions and understand how different
features affect survival chances.

Results

Model Accuracy Precision Recall F1 Score
Logistic Regression 0.81 0.79 0.74 0.76
Random Forest (Default) 0.82 0.81 0.74 0.77
Random Forest (Tuned) 0.81 0.83 0.67 0.74
XGBoost 0.78 0.73 0.74 0.73

Interpretation

• The default Random Forest performed the best with an accuracy of 0.82.
• After tuning, accuracy slightly dropped to 0.81 — this often happens with
smaller datasets due to minor overfitting during cross-validation.
• XGBoost gave similar results but no major improvement, showing that the
Titanic dataset is relatively simple and mostly linear.
• Both LIME and SHAP confirmed the most important features affecting

survival:

o Sex, Pclass, Fare, IsAlone, and Age.
o Being female and traveling in a higher class increased survival
chances.

Hyperparameter Tuning Choice

I used GridSearchCV because the dataset is small enough to test all possible
parameter combinations efficiently.
It provides a complete and reproducible way to understand how each
hyperparameter affects model accuracy.
If the dataset were larger, I would prefer RandomizedSearchCV or Optuna for
faster tuning and better coverage of parameter space.
But for this Titanic dataset, GridSearchCV was the most practical and suitable
choice.

Conclusion

In this level, I successfully applied feature engineering, model tuning, and
explainability techniques.
Even though hyperparameter tuning did not increase accuracy, it completed the
full model optimization workflow.

• The default Random Forest remained the most balanced and
interpretable model.
• LIME made the model easier to explain by showing how individual
features influenced specific predictions.
• Overall, this step improved my understanding of how tuning and
interpretability work together to build more transparent and reliable ML
models.

Level 3 — Reverse Engineering an AI Model

Goal:

To reverse-engineer a trained “black-box” model to understand its internal
decision logic, check for possible biases, and explore ways to secure the model.

1. What I Did
1. Selected the Model
I used my tuned Random Forest model from Level 2 as the black-box.

2. Built a Surrogate Model
   
• Chose a simple Decision Tree as the surrogate.
• Instead of training it on the original labels, I trained it on the
predictions made by the black-box Random Forest.
• The idea was to mimic the black-box behavior using a transparent,
explainable model.

3. Compared Both Models

• Evaluated how well the surrogate matched the black-box
predictions.
• Measured overall accuracy and agreement between the two
models.
• Used SHAP to visualize which features the surrogate relied on
most.

4. Bias and Vulnerability Check

• Compared predictions for males vs females to detect bias.
• Observed the surrogate’s structure to spot over-simplified or
sensitive rules.

2. Results

Model Accuracy (vs True Labels)
Agreement with BlackBox
Random Forest (BlackBox)
0.80 1.00
Decision Tree (Surrogate) 0.79 0.95

3. Interpretation and Findings
• The Decision Tree surrogate successfully learned to imitate about 95 % of
the Random Forest’s predictions.
• Accuracy stayed very close (0.80 → 0.79), meaning the surrogate captured
most of the black-box behavior.
• SHAP analysis confirmed the same top features as before:
o Sex, Pclass, Fare, IsAlone, and Age.
• Bias check: females had higher predicted survival rates in both models —
consistent with real-world Titanic data, not model bias.
• The surrogate’s tree plot clearly showed interpretable if-else paths
explaining why certain passengers were predicted to survive.

4. Key Insights
• A surrogate model is a safe, interpretable way to understand complex or
opaque systems.
• Reverse engineering helps identify hidden dependencies and potential
ethical risks before deployment.
• Even though the Decision Tree is simpler, it gives strong insight into what
drives predictions.

5. Recommendations & Defensive Techniques
1. Model Auditing & Bias Reduction:
• Regularly evaluate feature impacts using SHAP/LIME.
• Monitor accuracy separately for different gender or class groups.

2. Security & Intellectual Property Protection:
• Watermarking: embed a signature to verify model ownership.
• Obfuscation: hide internal parameters to prevent model theft.
• Encryption: secure the .pkl or API model before deployment.

3. Future Improvements:
• Try more advanced surrogates (e.g., logistic regression or gradient
boosting).
• Automate fairness checks in the pipeline.

6. Conclusion
By reverse-engineering my tuned Random Forest using a Decision Tree surrogate,
I was able to:
• Explain model logic in human-readable form,
• Verify that predictions are fair and consistent, and
• Suggest ways to protect and audit the model.

This step completed the end-to-end machine-learning workflow:
from data cleaning → optimization → interpretability → model auditing &
security.

After completing all three levels of the assignment, I recommend deploying the
Level 1 Random Forest (Default) model as the main predictive engine.
Reasoning:

• Level 1 Random Forest achieved the highest overall accuracy (0.82) and
balanced F1 score (0.77) compared to the tuned Level 2 model (accuracy
0.81, F1 0.74).

• Level 2 tuning did not improve accuracy on this small dataset and slightly
reduced recall, likely due to overfitting during cross-validation.

• Level 3 surrogate Decision Tree is very useful for interpretability, showing
how features like Sex, Pclass, Fare, and IsAlone influence predictions, but
it is not intended as the main predictive model.

Deployment Plan:
• The FastAPI / Streamlit app will use Level 1 Random Forest to provide
survival predictions.
This approach ensures that users get accurate predictions while still having the
option to understand the model’s decision logic, balancing performance and
interpretability.
