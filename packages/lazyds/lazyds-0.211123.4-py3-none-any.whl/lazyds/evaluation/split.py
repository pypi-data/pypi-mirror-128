from sklearn.model_selection import train_test_split


def split(X, y, ts_pct=33):
    Xtr, Xts, ytr, yts = train_test_split(X, y, test_size=ts_pct / 100, random_state=42)
    return {"Xtr": Xtr, "ytr": ytr, "Xts": Xts, "yts": yts}
