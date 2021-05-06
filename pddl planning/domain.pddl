(define (domain sokorobotto)
  (:requirements :typing)
  (:types  
    shipment order location thing saleitem -object
    robot pallette -thing
  )

  (:predicates 
  
    (includes ?x -shipment ?y -saleitem)
    (ships ?x -shipment ?y -order)           ; Says that order should be in shipment
    (orders ?x -order ?y -saleitem)          ; Says that saleitem should be in order
    (unstarted ?x -shipment)              ; True when shipment hasn't shipped
    (packing-location ?x -location)       ; specifies if location is a packing-location
    (contains ?x -pallette ?y -saleitem)     ; Sale item is on the pallete
    (carry ?x -robot ?y -pallette)            ; robot is carrying pallete
    (free ?x -robot)                      ; The robot is not carrying something
    (connected ?x -location ?y -location)    ; There is a path between from first to second location
    (at ?x -thing ?y -location)                          ; The pallete is at this location
    (no-robot ?x -location)               ; There is no robot at this location
    (no-pallette ?x -location)            ; There is no pallete at this location
    (available ?x -location)              ; This location is a packing location and there is no pallete or robot here
  )

  (:action move 
      :parameters (?robot -robot ?loc1 -location ?loc2 -location)
      :precondition (and 
        (connected ?loc1 ?loc2)
        (at ?robot ?loc1) 
        (no-robot ?loc2)
        (free ?robot)
      )

      :effect (and 
        (at ?robot ?loc2)
        (no-robot ?loc1)
        (not (at ?robot ?loc1))
        (not (no-robot ?loc2))
      )
  )
  
  (:action move-carry 
      :parameters (?robot -robot ?loc1 -location ?loc2 -location)
      :precondition (and 
        (not (free ?robot))
        (no-pallette ?loc2)
        (connected ?loc1 ?loc2)
        (at ?robot ?loc1) 
        (no-robot ?loc2)
      )

      :effect (and 
        (at ?robot ?loc2)
        (no-robot ?loc1)
        (not (at ?robot ?loc1))
        (not (no-robot ?loc2))
      )
  )
  

  (:action pickup
      :parameters (?robot -robot ?pallette -pallette ?loc1 -location)
      :precondition (and 
      (at ?robot ?loc1)
      (at ?pallette ?loc1)
      (free ?robot)
      )
      :effect (and 
      (carry ?robot ?pallette)
      (not (at ?pallette ?loc1))
      (not (free ?robot))
      (no-pallette ?loc1)
      )
  )

  (:action set
      :parameters (?robot -robot ?pallette -pallette ?loc1 -location)
      :precondition (and
      (no-pallette ?loc1)
      (at ?robot ?loc1)
      (carry ?robot ?pallette)
      )
      :effect (and 
      (at ?pallette ?loc1)
      (not (carry ?robot ?pallette))
      (free ?robot)
      (not (no-pallette ?loc1))
      )
  )

  (:action pack
      :parameters (?shipment1 - shipment ?order1 -order ?loc1 -location ?pal1 -pallette ?item -saleitem)
      :precondition (and 
      (packing-location ?loc1)
      (at ?pal1 ?loc1)
      (contains ?pal1 ?item)
      (orders ?order1 ?item)
      (ships ?shipment1 ?order1)
      (unstarted ?shipment1)
      )
      :effect (and 
      (includes ?shipment1 ?item)
      (not (contains ?pal1 ?item))
      )
  )
  
  
  


)