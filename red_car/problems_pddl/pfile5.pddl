(define (problem redcar-instance-5)
  (:domain RedCar)

  (:objects
    red-car blue-car purple-car - horizontalCar
    green-car orange-car white-car pink-car green-over-car yellow-over-car - verticalCar
    yellow-truck - verticalTruck
    
    p0 p1 p2 p3 p4 p5 - position
  )

  (:init
    ;; Vehicle positions
    (= (pos-x red-car) 0)
    (= (pos-y red-car) 2)
    (= (pos-x green-car) 0)
    (= (pos-y green-car) 0)
    (= (pos-x orange-car) 1)
    (= (pos-y orange-car) 0)
    (= (pos-x blue-car) 2)
    (= (pos-y blue-car) 0)
    (= (pos-x purple-car) 2)
    (= (pos-y purple-car) 1)
    (= (pos-x pink-car) 4)
    (= (pos-y pink-car) 0)
    (= (pos-x yellow-truck) 3)
    (= (pos-y yellow-truck) 2)
    (= (pos-x white-car) 4)
    (= (pos-y white-car) 3)
    (= (pos-x green-over-car) 2)
    (= (pos-y green-over-car) 2)
    (= (pos-x yellow-over-car) 2)
    (= (pos-y yellow-over-car) 4)

    ;; Grid boundaries
    (= (min_x) 0)
    (= (max_x) 5)
    (= (min_y) 0)
    (= (max_y) 5)
    (= (total-cost) 0)

    ;; Position mappings
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

                                                                          (clear p5 p0)
                                                                          (clear p5 p1)             
                                                            (clear p4 p2) (clear p5 p2)
    (clear p0 p3) (clear p1 p3)                                           (clear p5 p3)
    (clear p0 p4) (clear p1 p4)                                           (clear p5 p4)
    (clear p0 p5) (clear p1 p5)               (clear p3 p5) (clear p4 p5) (clear p5 p5)
  )

  (:goal (and
    (= (pos-x red-car) 4)
    (= (pos-y red-car) 2)
  ))

  (:metric minimize (total-cost))
)
