(define (problem 5)
(:domain RedCar)
(:objects


 red-car green-car purple-car blue-sky-car - horizontalCar
 orange-car pink-car - verticalCar

 purple-truck yellow-truck blue-truck - verticalTruck
)
(:init
    (= (x red-car) 3)
(= (y red-car) 2)
(= (x green-car) 0)
(= (y green-car) 0)
(= (x purple-car) 1)
(= (y purple-car) 4)
(= (x blue-sky-car) 4)
(= (y blue-sky-car) 3)
(= (x orange-car) 4)
(= (y orange-car) 0)
(= (x pink-car) 0)
(= (y pink-car) 4)
(= (x purple-truck) 5)
(= (y purple-truck) 0)
(= (x yellow-truck) 2)
(= (y yellow-truck) 0)
(= (x blue-truck) 3)
(= (y blue-truck) 3)
    
    ;; Grid boundaries
    (= (min_x) 0)
    (= (max_x) 6)
    (= (min_y) 0)
    (= (max_y) 6)
    
    ;; Clear cells
    (= (clear 0 0) 0)
(= (clear 1 0) 0)
(= (clear 2 0) 0)
(= (clear 3 0) 1)
(= (clear 4 0) 0)
(= (clear 5 0) 0)
(= (clear 0 1) 1)
(= (clear 1 1) 1)
(= (clear 2 1) 0)
(= (clear 3 1) 1)
(= (clear 4 1) 0)
(= (clear 5 1) 0)
(= (clear 0 2) 1)
(= (clear 1 2) 1)
(= (clear 2 2) 0)
(= (clear 3 2) 0)
(= (clear 4 2) 0)
(= (clear 5 2) 0)
(= (clear 0 3) 1)
(= (clear 1 3) 1)
(= (clear 2 3) 1)
(= (clear 3 3) 0)
(= (clear 4 3) 0)
(= (clear 5 3) 0)
(= (clear 0 4) 0)
(= (clear 1 4) 0)
(= (clear 2 4) 0)
(= (clear 3 4) 0)
(= (clear 4 4) 1)
(= (clear 5 4) 1)
(= (clear 0 5) 0)
(= (clear 1 5) 1)
(= (clear 2 5) 1)
(= (clear 3 5) 0)
(= (clear 4 5) 1)
(= (clear 5 5) 1)
)
(:goal (and 
    (= (x red-car) (- (max_x) 2))
    (= (y red-car) 2)
))
)