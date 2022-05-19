% ** The algorithm used in this assignment is adopted from rosettacode.org **
% In order to run the program, please only call number_chain in the query window.

init(3,2,46).
init(4,2,45).
init(6,2,55).
init(7,2,74).
init(2,3,38).
init(8,3,78).
init(2,4,35).
init(8,4,71).
init(3,5,33).
init(7,5,59).
init(2,6,17).
init(8,6,67).
init(2,7,18).
init(5,7,11).
init(8,7,64).
init(3,8,24).
init(4,8,21).
init(6,8,1).
init(7,8,2).


% Helper function to replace the an element in the list and return a new list
replaceInThePosition([_|T],1,E,[E|T]).
replaceInThePosition([H|T],P,E,[H|R]) :-
    P > 1, NP is P-1, replaceInThePosition(T,NP,E,R).

% Make a list with length 81 and replace the list elements with given init numbers
% The (x,y) position of the numbers are then converted to the list's index
% index = (Y*9) - (9-X)
solution_list(L,MAX,N) :- length(L,81),
    ( N==82 ->
         true
    ;
    	(init(X,Y,N) ->  replaceInThePosition(L,-((*(Y,9)),(-(9,X))),N,L) ; true),
        N1 is N +1,
        MAX1 is MAX - 1,
    	solution_list(L,MAX1,N1)
    ).

% Prints the solution
% it goes to the next line when index is a product of 9
print_solution([],_).
print_solution([H|T],N) :-
	write(H),write(' '),
	(0 is N mod 9 -> nl ; true), % nl goes to the next line
	N1 is N+1,
	print_solution(T,N1).
    

% Find the given numbers with their indexes, make another list which numbers are indexes from previous list
% and new indexes are numbers from previous list
% arg1=list, arg2=Element to find,  arg3=new list
index_finder([],_,_).
index_finder([H|T],N,S) :-
	(integer(H) -> nth1(H,S,N);true), % nth1 true when N is an Hth index of list S. list starts at 1
	N1 is N+1,
	index_finder(T,N1,S).


% left-right and up-down mapping rules...
lr(N,B) :- 
	between(1,81,N), M is N mod 9,
    (dif(M,0) ->  (succ(N,N1),B is N1) ; ( B is N , N is -(N-1))).
lr(0,0).
 
ud(N,B) :-
    between(1,72,N) , B is N+9.
ud(0,0).

mapping(A,B) :- lr(A,B) ; lr(B,A) ; ud(A,B) ; ud(B,A).


% following predicates use Index_finder and mapping rules to make the final solution list
% this is the adopted algorithm...
solve([A|T]) :-
	numlist(1,81,S), % S is a list from 1-81
	select(A,S,R), % if remove A from S, results in R
	solve2([A|T],R).
 
solve2([_],[]).
solve2([A,B|T],R) :-
	mapping(A,B),
	select(B,R,Rt),
	solve2([B|T],Rt).

final_solve([],_,_).
final_solve([A|T],N,G) :-
	nth1(A,G,N),
	succ(N,N1),
	final_solve(T,N1,G).


number_chain :-
    solution_list(L,81,1),
    length(S,81),
    index_finder(L,1,S),
    solve(S),
    final_solve(S,1,P),
    print_solution(P,1),
    !.
    
    






