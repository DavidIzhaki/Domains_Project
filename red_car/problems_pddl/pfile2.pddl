(define (problem redcar-instance-2)
  (:domain RedCar)

  (:objects
    red-car - horizontalCar
    green-car - verticalCar
    p0 p1 p2 p3 p4 p5  - position
  )

  (:init
    ;; Vehicle position
    (= (pos-x red-car) 0)
    (= (pos-y red-car) 2)

    (= (pos-x green-car) 2)
    (= (pos-y green-car) 2)
  
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
    
    (clear p0 p0) (clear p1 p0) (clear p2 p0) (clear p3 p0) (clear p4 p0) (clear p5 p0)
    (clear p0 p1) (clear p1 p1) (clear p2 p1) (clear p3 p1) (clear p4 p1) (clear p5 p1)             
                                              (clear p3 p2) (clear p4 p2) (clear p5 p2)
    (clear p0 p3) (clear p1 p3)               (clear p3 p3) (clear p4 p3) (clear p5 p3)
    (clear p0 p4) (clear p1 p4) (clear p2 p4) (clear p3 p4) (clear p4 p4) (clear p5 p4)
    (clear p0 p5) (clear p1 p5) (clear p2 p5) (clear p3 p5) (clear p4 p5) (clear p5 p5)
  )

  (:goal (and 
    (= (pos-x red-car) 4)  
    (= (pos-y red-car) 2)
  ))
  (:metric minimize (total-cost))
)
