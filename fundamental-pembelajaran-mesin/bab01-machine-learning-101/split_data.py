"""Kode 1.4: membagi data menjadi latih, validasi, dan uji, lalu memilih
kedalaman pohon keputusan memakai data validasi."""
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


def main():
    X, y = load_iris(return_X_y=True)

    # 60% latih, 20% validasi, 20% uji; stratify menjaga proporsi kelas
    X_tmp, X_test, y_tmp, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(
        X_tmp, y_tmp, test_size=0.25, stratify=y_tmp, random_state=42)

    print("kedalaman  skor_latih  skor_validasi")
    terbaik, skor_terbaik = None, -1.0
    for depth in [1, 2, 3, 5, None]:
        m = DecisionTreeClassifier(max_depth=depth, random_state=0)
        m.fit(X_train, y_train)
        s_val = m.score(X_val, y_val)
        print(f"{str(depth):>9}  {m.score(X_train, y_train):10.3f}  {s_val:13.3f}")
        if s_val > skor_terbaik:
            terbaik, skor_terbaik = depth, s_val

    # Data uji hanya disentuh SEKALI, setelah model final dipilih.
    final = DecisionTreeClassifier(max_depth=terbaik, random_state=0)
    final.fit(X_tmp, y_tmp)
    print(f"model final max_depth={terbaik}, skor uji = {final.score(X_test, y_test):.3f}")


if __name__ == "__main__":
    main()
