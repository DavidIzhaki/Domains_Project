(define (domain RedCar)
  ;(:requirements :typing :action-costs)

  (:types
      position vehicle - object
      car truck - vehicle
      horizontalCar verticalCar - car
      horizontalTruck verticalTruck - truck
      cell - position
  )
  (:predicates (clear ?x - position ?y - position))

  (:functions
     (pos-x ?v - vehicle) ;; X coordinate
     (pos-y ?v - vehicle)  ;; Y coordinate
     (pos-cell-x ?x -position) ;; X coordinate of a cell
     (pos-cell-y ?y -position) ;; Y coordinate of a cell
     (max_x)           ;; Max X boundary
     (max_y)          ;; Max Y boundary
     (min_x)           ;; Min X boundary
     (min_y)          ;; Min Y boundary
     (total-cost)         ;; Sum of movement costs
  )

  (:action move-car-right
 :parameters (?c - horizontalCar ?x ?x2 ?y - position)
 :precondition (and
   (= (pos-cell-y ?y) (pos-y ?c))
   (= (pos-cell-x ?x) (pos-x ?c))
   (= (pos-cell-x ?x2) (+ (pos-x ?c) 2))
   (<= (pos-cell-x ?x2) (max_x))
   (clear ?x2 ?y) ;; 
 )
 :effect (and
   (clear ?x ?y)       ;; Mark old cell as clear
   (not (clear ?x2 ?y)) ;; Mark new cell as occupied
   (increase (pos-x ?c) 1)
   (increase (total-cost) 1)
 )
)
  ;; Move Horizontal Car Left
  (:action move-car-left
    :parameters (?c - horizontalCar ?x ?x2 ?y - position)
    :precondition (and
        (>= (pos-cell-x ?x2) (min_x)) ;; Ensure within grid
        (= (pos-cell-y ?y) (pos-y ?c))
        (= (pos-cell-x ?x) (+ (pos-x ?c) 1))
        (= (pos-cell-x ?x2) (- (pos-x ?c) 1))
        (clear ?x2 ?y) ;; 
    )
    :effect (and
   (clear ?x ?y)       ;; Mark old cell as clear
   (not (clear ?x2 ?y)) ;; Mark new cell as occupied
   (decrease (pos-x ?c) 1)
   (increase (total-cost) 1)
    )
  )


(:action move-car-up
  :parameters (?c - verticalCar ?x ?y ?y2 - position)
  :precondition (and
    (>= (pos-cell-y ?y2) (min_y))                      ;; Ensure within grid
    (= (pos-cell-x ?x) (pos-x ?c))              ;; X stays constant
    (= (pos-cell-y ?y) (+ (pos-y ?c) 1))              ;; target cell down (y+1)
    (= (pos-cell-y ?y2) (- (pos-y ?c) 1))       ;; target cell above (y - 1)
    (clear ?x ?y2)                              ;; new cell must be clear
  )
  :effect (and
    (clear ?x ?y)                         ;; free old bottom cell (was y+1)
    (not (clear ?x ?y2))                        ;; occupy new top cell
    (decrease (pos-y ?c) 1)
    (increase (total-cost) 1)
  )
)



 (:action move-car-down
  :parameters (?c - verticalCar ?x ?y ?y2 - position)
  :precondition (and
    (<= (pos-cell-y ?y2) (max_y))                 ;; Ensure grid bounds
    (= (pos-cell-x ?x) (pos-x ?c))               ;; X stays constant
    (= (pos-cell-y ?y) (pos-y ?c))               ;; current Y
    (= (pos-cell-y ?y2) (+ (pos-y ?c) 2))        ;; new cell below to occupy
    (clear ?x ?y2)                               ;; that cell must be clear
  )
  :effect (and
    (clear ?x ?y)                                ;; free old top cell
    (not (clear ?x ?y2))                         ;; occupy new bottom cell
    (increase (pos-y ?c) 1)
    (increase (total-cost) 1)
  )
)


 (:action move-truck-right
  :parameters (?t - horizontalTruck ?x ?x3 ?y - position)
  :precondition (and
    (<= (pos-cell-x ?x3) (max_x))                    ;; Ensure grid bound
    (= (pos-cell-x ?x) (pos-x ?t))                  ;; current leftmost cell
    (= (pos-cell-x ?x3) (+ (pos-x ?t) 3))           ;; new rightmost cell
    (= (pos-cell-y ?y) (pos-y ?t))                  ;; same row
    (clear ?x3 ?y)                                  ;; target cell must be clear
  )
  :effect (and
    (clear ?x ?y)                                   ;; free the old leftmost cell
    (not (clear ?x3 ?y))                            ;; occupy the new rightmost cell
    (increase (pos-x ?t) 1)
    (increase (total-cost) 1)
  )
)


  (:action move-truck-left
  :parameters (?t - horizontalTruck ?x1 ?x2 ?y - position)
  :precondition (and
    (>= (pos-cell-x ?x1) (min_x))                          ;; Ensure grid bound
    (= (pos-cell-x ?x1) (- (pos-x ?t) 1))           ;; new cell to occupy (x - 1)
    (= (pos-cell-x ?x2) (+ (pos-x ?t) 2))           ;; cell to be cleared (x + 2)
    (= (pos-cell-y ?y) (pos-y ?t))                  ;; same row
    (clear ?x1 ?y)                                  ;; new cell must be clear
  )
  :effect (and
    (not (clear ?x1 ?y))                            ;; occupy new cell
    (clear ?x2 ?y)                                  ;; free tail cell
    (decrease (pos-x ?t) 1)
    (increase (total-cost) 1)
  )
)


(:action move-truck-down
  :parameters (?t - verticalTruck ?x ?y1 ?y3 - position)
  :precondition (and
    (<= (pos-cell-y ?y3) (max_y))                  ;; within grid
    (= (pos-cell-x ?x) (pos-x ?t))                ;; fixed column
    (= (pos-cell-y ?y1) (pos-y ?t))               ;; old top cell to free
    (= (pos-cell-y ?y3) (+ (pos-y ?t) 3))         ;; new bottom cell to occupy
    (clear ?x ?y3)                                ;; new cell must be clear
  )
  :effect (and
    (clear ?x ?y1)                                ;; free old top cell
    (not (clear ?x ?y3))                          ;; occupy new bottom cell
    (increase (pos-y ?t) 1)
    (increase (total-cost) 1)
  )
)

(:action move-truck-up
  :parameters (?t - verticalTruck ?x ?y1 ?y2 - position)
  :precondition (and
    (>= (pos-cell-y ?y1) (min_y))                          ;; within grid
    (= (pos-cell-x ?x) (pos-x ?t))                  ;; fixed column
    (= (pos-cell-y ?y1) (- (pos-y ?t) 1))           ;; new cell above (y - 1)
    (= (pos-cell-y ?y2) (+ (pos-y ?t) 2))           ;; cell to free (y + 2)
    (clear ?x ?y1)                                  ;; new cell must be clear
  )
  :effect (and
    (not (clear ?x ?y1))                            ;; occupy new top cell
    (clear ?x ?y2)                                  ;; free old bottom cell
    (decrease (pos-y ?t) 1)
    (increase (total-cost) 1)
  )
)


)
  

