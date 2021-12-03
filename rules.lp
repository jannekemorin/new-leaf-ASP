reachable(Y, X) :- edge(X, Y).
reachable(Y, X) :- edge(X, Z), reachable(Y, Z).