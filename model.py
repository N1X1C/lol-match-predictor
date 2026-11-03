import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

DATA_FILE = "high_diamond_ranked_10min.csv"
df = pd.read_csv(DATA_FILE)

features = [
    "blueFirstBlood", "blueKills", "redKills",
    "blueAssists", "redAssists", "blueDragons", "redDragons",
    "blueTowersDestroyed", "redTowersDestroyed",
    "blueTotalGold", "redTotalGold",
    "blueTotalExperience", "redTotalExperience"
]

X = df[features]
y = df["blueWins"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

dt_model = DecisionTreeClassifier(max_depth=5, random_state=42)
dt_model.fit(X_train, y_train)

y_pred = dt_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

if __name__ == "__main__":
    print(f"✅ دقت مدل درخت تصمیم روی مسابقات LoL: {round(accuracy * 100, 2)} درصد")
