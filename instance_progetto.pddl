(define (problem ordine) (:domain cucina)
    (:requirements :strips :fluents :durative-actions :timed-initial-literals :typing :conditional-effects :negative-preconditions :duration-inequalities :equality )
 
  
  (:objects 
    knife pan -tool 
    counter stove sink storage table -location
    Mario -chef
    chicken salmon potato carrot rice feta tomato  beans tuna avocado  -ingredient
)
 
(:init  
(chef_location Mario table)
(free stove)
(free sink)
(free storage)
(free counter)

(ingredient_location chicken storage)(ingredient_location salmon storage)(ingredient_location potato storage)
(ingredient_location carrot storage)(ingredient_location rice storage)(ingredient_location feta storage)
(ingredient_location tomato storage)(ingredient_location zucchini storage)(ingredient_location peas storage)
(ingredient_location asparagus storage)(ingredient_location beans storage)(ingredient_location black_rice storage)
(ingredient_location tuna storage)(ingredient_location avocado storage)(ingredient_location olives storage)

(needs_chopping chicken)(needs_cooking chicken)(needs_chopping salmon)(needs_chopping potato)(needs_cooking potato)
(needs_chopping carrot)(needs_cooking rice)(needs_chopping feta)(needs_chopping tomato)(needs_chopping zucchini)
(needs_cooking zucchini)(needs_cooking peas)(needs_cooking asparagus)(needs_chopping asparagus)(needs_cooking beans)
(needs_cooking black_rice)(needs_chopping tuna)(needs_cooking tuna)(needs_chopping avocado)(needs_chopping olives)

(tool_location pan stove)
(tool_location knife counter)



)

(:goal (and
(served chicken)(served salmon)(served rice)(served tuna)(served beans)(served avocado)(served carrot)
(served feta)
  
  


))


(:metric minimize (total-cost))
)
