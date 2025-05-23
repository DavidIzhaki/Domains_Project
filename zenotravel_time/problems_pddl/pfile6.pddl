(define (problem zenotravel-problem-6)
  (:domain zenotravel)
  (:objects
    plane1 - aircraft
    plane2 - aircraft
    person1 - person
    person2 - person
    person3 - person
    person4 - person
    person5 - person
    city0 - city
    city1 - city
    city2 - city
    city3 - city)
  (:init
    (located plane1 city2)
    (= (capacity plane1) 5577)
    (= (fuel plane1) 873)
    (= (slow-burn plane1) 2)
    (= (fast-burn plane1) 6)
    (= (onboard plane1) 0)
    (= (zoom-limit plane1) 1)
    ;; NEW: Define speeds for plane1
    (= (slow-speed plane1) 350)
    (= (fast-speed plane1) 700)
    
    (located plane2 city1)
    (= (capacity plane2) 2911)
    (= (fuel plane2) 283)
    (= (slow-burn plane2) 1)
    (= (fast-burn plane2) 3)
    (= (onboard plane2) 0)
    (= (zoom-limit plane2) 7)
    ;; NEW: Define speeds for plane2
    (= (slow-speed plane2) 300)
    (= (fast-speed plane2) 600)
    
    (located person1 city0)
    (located person2 city0)
    (located person3 city3)
    (located person4 city1)
    (located person5 city2)
    
    (= (distance city0 city0) 0)
    (= (distance city0 city1) 917)
    (= (distance city0 city2) 811)
    (= (distance city0 city3) 641)
    (= (distance city1 city0) 917)
    (= (distance city1 city1) 0)
    (= (distance city1 city2) 972)
    (= (distance city1 city3) 757)
    (= (distance city2 city0) 811)
    (= (distance city2 city1) 972)
    (= (distance city2 city2) 0)
    (= (distance city2 city3) 554)
    (= (distance city3 city0) 641)
    (= (distance city3 city1) 757)
    (= (distance city3 city2) 554)
    (= (distance city3 city3) 0)
    
  
    (= (total-time-used) 0)    ;; NEW: initialize total time
  )
  (:goal (and
           (located person1 city3)
           (located person2 city1)
           (located person3 city3)
           (located person4 city3)
           (located person5 city1)))
    (:metric minimize (total-time-used)))
