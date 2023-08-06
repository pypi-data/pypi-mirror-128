from idict import let


def copy(source=None, target=None, **kwargs):
    """
    >>> from idict import idict
    >>> d = idict(x=1) >> let(copy, source="x", target="y")
    >>> d.evaluate()
    >>> d.show(colored=False)
    {
        "y": 1,
        "x": 1,
        "_id": "BXHxpDOhMNvGi7ZWULdH1YMUo8CLkPyFrsSywkFm",
        "_ids": {
            "y": "DqhRDi86ucDlAK-84iCYjgPhV0nLkPyFrsSywkFm",
            "x": "tY_a0e4015c066c1a73e43c6e7c4777abdeadb9f"
        }
    }
    """
    return {target: kwargs[source]}


trcopy = let(copy, source="Xtr", target="X") >> let(copy, source="ytr", target="y")
tscopy = let(copy, source="Xts", target="X") >> let(copy, source="yts", target="y")
