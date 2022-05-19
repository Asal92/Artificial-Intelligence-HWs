parent(charles, william).
parent(charles, harry).
parent(elizabeth, charles).
parent(george, elizabeth).
parent(george, margaret).
parent(elizabeth, anne).
parent(elizabeth, andrew).
parent(elizabeth, edward).
parent(anne, peter).
parent(anne, zara).
parent(andrew, beatrice).
parent(andrew, eugenie).
parent(edward, louise).
parent(edward, james).

% child definition
child(X,Y) :- parent(Y,X).
 
% siblings = having same parents
sibling(X, Y) :- parent(Z,X),parent(Z,Y),not(X=Y).
 
% cousins = Their parents are siblings
cousin(X,Y) :- parent(A,X),parent(B,Y),sibling(A,B).
 
% ancestor = X is Y's ancestor if X is parent of some Z who is Y's parent
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).


len([], 0).
len([_ | T], N) :- len(T, M), N is M+1.

% sorted(L) which is true if and only if list L is in ascending sorted order.
% query -> sorted([1,2,3]). True
% query -> sorted([2,1,3]). False
sorted([]).
sorted([_]).
sorted([X,Y|R]) :- X=<Y , sorted([Y|R]).

% Remove X from a list and return a new list - helper for perm
% query -> takeout(2,[1,2,3],X). returns [1,3]
takeout(X,[X|R],R).
takeout(X,[F|R],[F|S]) :- takeout(X,R,S).

% perm(L, M) which is true if and only if L is a permutation of M
% query -> perm([1,2,3],[3,2,1]). True
perm([],[]).
perm(L,[H|M]):- takeout(H,L,R),perm(R,M).

% mysort(L, M) where M is a sorted version of L using perm and sorted
% query -> mysort([3,2,1],X). will print out a sorted version of list
mysort(L, M) :- perm(L,M),sorted(M).


%No. of perms = n! which n is the number of elements in the list
% for mysort with 9 elements, it took around 0.835 seconds (worst case when its sorted descending.
% with 10 elements it took 8.088 seconds, and for 11 elements it took 88.574 seconds
% When ran mysort with 12 elements, it took forever and exceeded prolog time limit!
% it looks like the time complexity is O(n!) because we have n! permutations
% perm returns a permutation of L, and check if it's sorted. if it's not it will return another 
% permutations and check if it's sorted. it repeats this in worst scenario for n! times so 
% Time complexity ends up being O(n!)




