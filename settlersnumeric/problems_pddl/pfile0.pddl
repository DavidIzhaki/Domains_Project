(define (problem settlers-simple)
  (:domain civ)
  (:objects
    location0 - place
    location1 - place
    vehicle0 - vehicle
  )
  (:init
    (= (resource-use) 0)
    (= (labour) 0)
    (= (pollution) 0)
    
    ;; Location properties
    (woodland location0)
    (by-coast location1)
    
    ;; Location0 resources
    (= (housing location0) 0)
    (= (available wood location0) 0)
    (= (carts-at location0) 0)
    (= (available timber location0) 0)
    (= (available ore location0) 0)
    (= (available stone location0) 0)
    (= (available iron location0) 0)
    (= (available coal location0) 0)
    
    ;; Location1 resources
    (= (housing location1) 0)
    (= (available wood location1) 0)
    (= (carts-at location1) 0)
    (= (available timber location1) 0)
    (= (available ore location1) 0)
    (= (available stone location1) 0)
    (= (available iron location1) 0)
    (= (available coal location1) 0)
    
    ;; Connections
    (connected-by-land location0 location1)
    (connected-by-land location1 location0)
    
    ;; Potential vehicle
    (potential vehicle0)
    
    ;; Initialize vehicle0 resources
    (= (available timber vehicle0) 0)
    (= (available wood vehicle0) 0)
    (= (available coal vehicle0) 0)
    (= (available stone vehicle0) 0)
    (= (available iron vehicle0) 0)
    (= (available ore vehicle0) 0)
    (= (space-in vehicle0) 0)
  )
  
  (:goal 
    (and
      (>= (available timber location1) 1)
    )
  )
  
  (:metric minimize (+ (+ (* 0 (pollution)) (* 3 (resource-use))) (* 3 (labour))))
)
