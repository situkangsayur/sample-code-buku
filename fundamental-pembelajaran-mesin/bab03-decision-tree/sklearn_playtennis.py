"""Kode 3.4: melatih dan membaca pohon PlayTennis dengan scikit-learn."""
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text

df = pd.DataFrame({
    "Outlook": "Sunny Sunny Overcast Rain Rain Rain Overcast Sunny Sunny "
               "Rain Sunny Overcast Overcast Rain".split(),
    "Humidity": "High High High High Normal Normal Normal High Normal "
                "Normal Normal High Normal High".split(),
    "Wind": "Weak Strong Weak Weak Weak Strong Strong Weak Weak Weak "
            "Strong Strong Weak Strong".split(),
    "Play": "No No Yes Yes Yes No Yes No Yes Yes Yes Yes Yes No".split(),
})
# CART hanya menerima angka: ubah atribut kategorikal menjadi one-hot
X = pd.get_dummies(df.drop(columns="Play"), dtype=int)
y = df["Play"]

pohon = DecisionTreeClassifier(criterion="entropy", random_state=0)
pohon.fit(X, y)
print(export_text(pohon, feature_names=list(X.columns)))
print("akurasi latih:", pohon.score(X, y))

# Pohon kedalaman dua (keluaran di awal bab): 12 dari 14 hari benar
dangkal = DecisionTreeClassifier(criterion="entropy", max_depth=2,
                                 random_state=0).fit(X, y)
print(export_text(dangkal, feature_names=list(X.columns)))
