;Header and description

(define (domain cucina)

;remove requirements that are not needed
(:requirements :strips :fluents :durative-actions :timed-initial-literals :typing :conditional-effects :negative-preconditions :duration-inequalities :equality :disjunctive-preconditions)
(:types ingredient 
        tool 
        location
        chef
)
 


(:constants
        knife pan -tool 
        counter stove sink storage table -location
    )



(:predicates
    (chopped ?x - ingredient)
    (cooked ?x - ingredient)
    (served ?x -ingredient)
    
    (dirty ?x -tool)
    (chef_location ?x -chef ?y -location)
    (tool_location ?x -tool ?y -location)
    (ingredient_location ?x - ingredient ?y -location)
    
    
    (ing_held  ?y -ingredient)
    (ing_holding ?x -chef ?y -ingredient)
    (is_holding ?x -chef ?z -tool)
    (held ?x -tool)
    (is_holding_tool ?x -chef)
    (is_holding_ingredient ?x -chef )

    (free ?x -location)
    (needs_chopping ?x -ingredient)
    (needs_cooking ?x -ingredient)
    
)
(:functions (total-cost))    

(:action chop
    :parameters (?x -chef      ?y -ingredient  )
    :precondition (and 
    (is_holding ?x knife)
    (ing_holding ?x ?y)
    (chef_location ?x counter)
    (not(cooked ?y))
    (not(chopped ?y))
    (not(dirty knife))

    )
    :effect (and 
    (chopped ?y)
    (dirty knife)
    (not(needs_chopping ?y))
    (increase (total-cost) 2)
    )
)

(:action cook
    :parameters ( ?x - chef     ?y - ingredient   )
    :precondition (and
    (ing_holding ?x ?y)
    (not(cooked ?y))
    (not(dirty pan))
    (chef_location ?x stove)
    (is_holding ?x pan)
    (needs_cooking ?y)
    )

    :effect (and 
    (cooked ?y)
    (dirty pan)
    (not(needs_cooking ?y))
    (increase (total-cost) 2)
    )
)

(:action wash
    :parameters (?x -chef   ?y - tool )
    :precondition (and 
    (dirty ?y)
    (chef_location ?x sink)
    (is_holding ?x ?y)
    )
    :effect (and 
    (not(dirty ?y))
    (increase (total-cost) 2)
    )
)

(:action move
    :parameters (?x - chef      ?y1 - location       ?y2 - location)
    :precondition (and 
    (chef_location ?x ?y1)
    )
    :effect (and
    (not(chef_location ?x ?y1))
    (free ?y1)
    (chef_location ?x ?y2)
    (not(free ?y2))
    (increase (total-cost) 0.5)
    )
)
(:action take_tool
    :parameters (?x - chef      ?z - tool       ?y - location)
    :precondition (and 
    (chef_location ?x ?y)
    (tool_location ?z ?y)
    (not(held ?z))
    (not(is_holding_tool ?x))
    )
    :effect (and 
    (held ?z)
    (is_holding ?x ?z)
    (is_holding_tool ?x)
    (not(tool_location ?z ?y))
    (increase (total-cost) 2)
    )
)

(:action put_down_tool
    :parameters (?x - chef      ?z - tool       ?y - location)
    :precondition (and 
    (chef_location ?x ?y)
    (held ?z)
    (is_holding ?x ?z)
    (is_holding_tool ?x )
    )
    :effect (and 
    (not(held ?z))
    (not(is_holding ?x ?z))
    (not(is_holding_tool ?x))
    (tool_location ?z ?y) 
    (increase (total-cost) 2) 
    )   
)


(:action take_ingredient
    :parameters (?x -chef      ?z -ingredient       ?y -location)
    :precondition (and 
    (chef_location ?x ?y)
    (ingredient_location ?z ?y)
    (not(ing_held ?z))
    (not(is_holding_ingredient ?x))
    )
    :effect (and 
    (ing_held ?z)
    (ing_holding ?x ?z)
    (is_holding_ingredient ?x)
    (not(ingredient_location ?z ?y))
    (increase (total-cost) 2)
    )
)

(:action put_down_ingredient
    :parameters (?x -chef      ?z -ingredient       ?y -location)
    :precondition (and 
    (chef_location ?x ?y)
    (ing_held ?z)
    (ing_holding ?x ?z)
    (is_holding_ingredient ?x)
    )
    :effect (and 
    (not(ing_held ?z))
    (not(ing_holding ?x ?z))
    (ingredient_location ?x ?y)  
    (not(is_holding_ingredient ?x ))
    (increase (total-cost) 2)
    )   
)

(:action serve_plate
    :parameters ( ?x -chef      ?y - ingredient )
    :precondition (and 
    (not(needs_chopping ?y))
    (not(needs_cooking ?y))
    (is_holding_ingredient ?x)
    (chef_location ?x table)
    )
    :effect (and 
    (served ?y )
    (not(is_holding_ingredient ?x))
    (increase (total-cost)2 )
)


)   


)