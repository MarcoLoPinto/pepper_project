(define (domain test1_domain)
(:requirements :conditional-effects :disjunctive-preconditions)

(:predicates
	(do_a0)
	(do_a1)
	(do_a2)
	(do_a3)
	(do_a4)
	(do_a5)
	(gg1)
	(gg2)
	(at0)
)

(:action a0 
	:parameters () 
	:precondition(
		and (do_a0) 
	) 
	:effect(
		and (not (do_a0)) (not (do_a3)) (not (do_a4)) (not (do_a5))  (oneof (do_a1) (do_a2)) (at0) 
	)
)

(:action a1 
	:parameters () 
	:precondition(
		and (do_a1) (at0)
	) 
	:effect(
		and (not (do_a0)) (not (do_a1)) (not (do_a2)) (not (do_a4)) (not (do_a5)) (do_a3)   
	)
)

(:action a2 
	:parameters () 
	:precondition(
		and (do_a2) (at0)
	) 
	:effect(
		and (not (do_a0)) (not (do_a1)) (not (do_a2)) (not (do_a3)) (do_a4) (do_a5)   
	)
)

(:action a3 
	:parameters () 
	:precondition(
		and (do_a3) 
	) 
	:effect(
		and (not (do_a0)) (not (do_a1)) (not (do_a2)) (not (do_a3)) (not (do_a4)) (not (do_a5))    ($end$)
	)
)

(:action a4 
	:parameters () 
	:precondition(
		and (do_a4) 
	) 
	:effect(
		and (not (do_a0)) (not (do_a1)) (not (do_a2)) (not (do_a3)) (not (do_a4)) (not (do_a5))   (gg1) ($end$)
	)
)

(:action a5 
	:parameters () 
	:precondition(
		and (do_a5) 
	) 
	:effect(
		and (not (do_a0)) (not (do_a1)) (not (do_a2)) (not (do_a3)) (not (do_a4)) (not (do_a5))   (gg2) ($end$)
	)
)


)