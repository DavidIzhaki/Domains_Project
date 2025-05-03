(define (problem redcar-instance-1)
  (:domain RedCar)
  (:objects
    red-car green-car white-car brown-car - horizontalCar
    pink-car green-over-car yellow-car orange-car yellow-over-car purple-car  blue-car  - verticalCar
    yellow-truck purple-truck - verticalTruck
    p0 p1 p2 p3 p4 p5  - position
  )

  (:init
    ;; Vehicle position
    (= (pos-x red-car) 2)
    (= (pos-y red-car) 2)
    
    (= (pos-x purple-car) 1)
    (= (pos-y purple-car) 1)
    
    (= (pos-x pink-car) 0)
    (= (pos-y pink-car) 1)
    
    (= (pos-x green-car) 0)
    (= (pos-y green-car) 0)
    
    (= (pos-x white-car) 1)
    (= (pos-y white-car) 3)
    
    (= (pos-x brown-car) 3)
    (= (pos-y brown-car) 5)
    
    (= (pos-x yellow-car) 2)
    (= (pos-y yellow-car) 4)
    
    (= (pos-x blue-car) 5)
    (= (pos-y blue-car) 0)
    
    (= (pos-x yellow-over-car) 3)
    (= (pos-y yellow-over-car) 3)
    
    (= (pos-x green-over-car) 5)
    (= (pos-y green-over-car) 2)
    
    (= (pos-x orange-car) 3)
    (= (pos-y orange-car) 0)
    
    
    (= (pos-x yellow-truck) 4)
    (= (pos-y yellow-truck) 2)

    (= (pos-x purple-truck) 0)
    (= (pos-y purple-truck) 3)
   
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
    
                                 (clear p2 p0)                  (clear p4 p0)
                                 (clear p2 p1)                  (clear p4 p1)
                                                                
                               
                  (clear p1 p4)                                               (clear p5 p4)  
                  (clear p1 p5)                                               (clear p5 p5)  
    
                  

  )

  (:goal (and 
    (= (pos-x red-car) 4)  
    (= (pos-y red-car) 2)
  ))
  (:metric minimize (total-cost))
)
