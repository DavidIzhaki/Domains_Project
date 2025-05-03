(define (problem redcar-instance-1)
  (:domain RedCar)
  (:objects
    red-car  yellow-car brown-car pink-car green-car white-car  - horizontalCar
    green-over-car yellow-over-car yellow-spe-car purple-car orange-car blue-car  - verticalCar
    purple-truck  yellow-truck - horizontalTruck
    p0 p1 p2 p3 p4 p5  - position
  )

  (:init
    ;; Vehicle position
    (= (pos-x red-car) 2)
    (= (pos-y red-car) 2)
    
    (= (pos-x pink-car) 2)
    (= (pos-y pink-car) 1)
    
    (= (pos-x green-car) 0)
    (= (pos-y green-car) 0)
    
    (= (pos-x white-car) 0)
    (= (pos-y white-car) 3)
    
    (= (pos-x brown-car) 0)
    (= (pos-y brown-car) 4)
    
    (= (pos-x yellow-car) 3)
    (= (pos-y yellow-car) 3)
    
    (= (pos-x blue-car) 0)
    (= (pos-y blue-car) 1)
    
    (= (pos-x yellow-over-car) 2)
    (= (pos-y yellow-over-car) 3)
    
    (= (pos-x yellow-spe-car) 3)
    (= (pos-y yellow-spe-car) 4)
    
    (= (pos-x green-over-car) 5)
    (= (pos-y green-over-car) 2)
    
    (= (pos-x orange-car) 5)
    (= (pos-y orange-car) 0)

    (= (pos-x purple-car) 4)
    (= (pos-y purple-car) 1)
    
    
    (= (pos-x yellow-truck) 2)
    (= (pos-y yellow-truck) 0)

    (= (pos-x purple-truck) 0)
    (= (pos-y purple-truck) 5)
   
    ;; Grid boundaries
    (= (min_x) 0)
    (= (max_x) 5)
    (= (min_y) 0)
    (= (max_y) 5)
    (= (total-cost) 0)

    ;; Map positions to numeric coordinates
    (= (pos-cell-x p0) 0)
    (= (pos-cell-x p1) 1)
    (= (pos-cell-x p2) 2)
    (= (pos-cell-x p3) 3)
    (= (pos-cell-x p4) 4)
    (= (pos-cell-x p5) 5)


    (= (pos-cell-y p0) 0)
    (= (pos-cell-y p1) 1)
    (= (pos-cell-y p2) 2)
    (= (pos-cell-y p3) 3)
    (= (pos-cell-y p4) 4)
    (= (pos-cell-y p5) 5)

    ;; Clear cells (as predicates!)
    
 
                  (clear p1 p1) 
                  (clear p1 p2)
                               
                                                                (clear p4 p4) (clear p5 p4)  
                                                                (clear p4 p5) (clear p5 p5)  
    
                  

  )

  (:goal (and 
    (= (pos-x red-car) 4)  
    (= (pos-y red-car) 2)
  ))
  (:metric minimize (total-cost))
)
