import pandas as pd
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def Random_Forest(plan_model, premium_model, sex, year, month, smoke, income, optional_insured, weight, height, married):
    plan_prediction = get_plan_predictions(plan_model, sex, year, month, smoke, income, optional_insured, weight, height, married)
    premiums = get_premium_predictions(premium_model, sex, year, month, smoke, income, optional_insured, weight, height, married)
    return {"plan": plan_prediction, "bronze": premiums["bronze"],
            "silver": premiums["silver"], "gold": premiums["gold"],
            "platinum": premiums["platinum"]}

def get_plan_model():
  train = pd.read_csv("pandas-dump2.csv", delimiter=",", nrows=10000)
  X = train.drop([train.columns[0], "id", "purchased", "gold_quote", "silver_quote", "bronze_quote", "PLATINUM"], axis=1)
  Y = train['purchased']
  random_forest = RandomForestClassifier(n_estimators=30, max_depth=10, random_state=1)
  return RandomForestClassifier().fit(X, Y)

def get_premium_model():
  train = pd.read_csv("pandas-dump2.csv", delimiter=",", nrows=10000)

  X = train.drop([train.columns[0], "id", "gold_quote", "silver_quote", "bronze_quote", "PLATINUM", "purchased"], axis=1)
  Y1 = train['gold_quote']
  Y2 = train['silver_quote']
  Y3 = train['bronze_quote']
  Y4 = train['PLATINUM']

  random_forest = RandomForestClassifier(n_estimators=30, max_depth=10, random_state=1)
  return [RandomForestClassifier().fit(X, Y1), RandomForestClassifier().fit(X, Y2), RandomForestClassifier().fit(X, Y3), RandomForestClassifier().fit(X, Y4)]

def get_plan_predictions(plan_model, sex, year, month, smoke, income, optional_insured, weight, height, married):
  test = pd.DataFrame({"sex": sex, "year": year, "month": month, "smoker": smoke, "income":income, "optional_insured":optional_insured,
            "weight": weight, "height": height, "married": married}, index=[0])

  predictions = plan_model.predict(test)
  if(predictions == 0):
      return "bronze"
  elif(predictions == 1):
      return "silver"
  elif(predictions == 2):
      return "gold"
  elif(predictions == 3):
      return "platinum"

def get_premium_predictions(premium_model, sex, year, month, smoke, income, optional_insured, weight, height, married):
  test = pd.DataFrame({"sex": sex, "year": year, "month": month, "smoker": smoke, "income":income, "optional_insured":optional_insured,
           "weight": weight, "height": height, "married": married}, index=[0])

  predictions1 = premium_model[0].predict(test)
  predictions2 = premium_model[1].predict(test)
  predictions3 = premium_model[2].predict(test)
  predictions4 = premium_model[3].predict(test)

  return {"gold": predictions1, "silver": predictions2, "bronze": predictions3, "platinum": predictions4}
