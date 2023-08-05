from idict import let


def copy(source=None, target=None, **kwargs):
    return {target: kwargs[source]}


trcopy = let(copy, source="Xtr", target="X") >> let(copy, source="ytr", target="y")
tscopy = let(copy, source="Xts", target="X") >> let(copy, source="yts", target="y")
