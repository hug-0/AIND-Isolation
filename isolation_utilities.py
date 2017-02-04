"""Simple utility functions that help game agents in Isolation."""

def argmax(seq, fn):
    """Returns an element with largest fn(seq[i]) score."""
    best = seq[0]
    best_score = fn(seq)
    for i in seq:
        n_score = fn(i)
        if n_score > best_score:
            best, best_score = i, n_score
    return best
