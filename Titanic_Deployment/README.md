4️⃣ README.md (Optional but recommended)
# Titanic Survival Prediction API

1. Install dependencies:  pip install -r requirements.txt

2. Run FastAPI server: uvicorn app:app --reload

3. Open browser at:  http://127.0.0.1:8000


4. To test the API, go to Swagger docs:  http://127.0.0.1:8000/docs


5. Use the `/predict` endpoint with input JSON, for example:

```json
{
  "Pclass": 3,
  "Sex": 1,
  "Age": 22,
  "Fare": 7.25,
  "Embarked": 2,
  "IsAlone": 1,
  "FamilySize": 1
}

Swagger UI: http://127.0.0.1:8000/docs → test predictions interactively.

Root endpoint: http://127.0.0.1:8000/ → welcome message.