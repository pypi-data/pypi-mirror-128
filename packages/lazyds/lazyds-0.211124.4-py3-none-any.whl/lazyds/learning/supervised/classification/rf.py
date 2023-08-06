def rf(X, y, n=500):
    from sklearn.ensemble import RandomForestClassifier
    rfc = RandomForestClassifier(n)
    rfc.fit(X, y)
    return {"model": rfc}
