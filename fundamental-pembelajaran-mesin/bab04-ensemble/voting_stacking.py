"""Kode 4.6 - Voting dan stacking di scikit-learn."""
from sklearn.ensemble import RandomForestClassifier, StackingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

from data import muat_data

X_tr, X_te, y_tr, y_te, _ = muat_data()

dasar = [
    ("lr", make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))),
    ("rf", RandomForestClassifier(n_estimators=300, random_state=0)),
    ("knn", make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=7))),
]
vote = VotingClassifier(dasar, voting="soft").fit(X_tr, y_tr)
# cv=5: meta-learner dilatih pada prediksi out-of-fold
stack = StackingClassifier(dasar, final_estimator=LogisticRegression(), cv=5).fit(X_tr, y_tr)
print("voting   :", round(vote.score(X_te, y_te), 4))
print("stacking :", round(stack.score(X_te, y_te), 4))
