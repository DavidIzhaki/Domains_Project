(define (problem settlers)
(:domain civ)
(:objects
	location0 - place
	location1 - place
	location2 - place
	location3 - place
	location4 - place
	location5 - place
	location6 - place
	location7 - place
	location8 - place
	vehicle0 - vehicle
	vehicle1 - vehicle
	vehicle2 - vehicle
	vehicle3 - vehicle
	vehicle4 - vehicle
	vehicle5 - vehicle
	vehicle6 - vehicle
	vehicle7 - vehicle
)
(:init
	(= (resource-use) 0)
	(= (labour) 0)
	(= (pollution) 0)
	(mountain location0)
	(woodland location0)
	(by-coast location0)
	(= (housing location0) 0)
	(= (available wood location0) 0)
	(= (carts-at location0) 0)
	(= (available timber location0) 0)
	(= (available ore location0) 0)
	(= (available stone location0) 0)
	(= (available iron location0) 0)
	(= (available coal location0) 0)
	(woodland location1)
	(metalliferous location1)
	(= (housing location1) 0)
	(= (available wood location1) 0)
	(= (carts-at location1) 0)
	(= (available timber location1) 0)
	(= (available ore location1) 0)
	(= (available stone location1) 0)
	(= (available iron location1) 0)
	(= (available coal location1) 0)
	(mountain location2)
	(woodland location2)
	(= (housing location2) 0)
	(= (available wood location2) 0)
	(= (carts-at location2) 0)
	(= (available timber location2) 0)
	(= (available ore location2) 0)
	(= (available stone location2) 0)
	(= (available iron location2) 0)
	(= (available coal location2) 0)
	(mountain location3)
	(woodland location3)
	(metalliferous location3)
	(= (housing location3) 0)
	(= (available wood location3) 0)
	(= (carts-at location3) 0)
	(= (available timber location3) 0)
	(= (available ore location3) 0)
	(= (available stone location3) 0)
	(= (available iron location3) 0)
	(= (available coal location3) 0)
	(woodland location4)
	(by-coast location4)
	(metalliferous location4)
	(= (housing location4) 0)
	(= (available wood location4) 0)
	(= (carts-at location4) 0)
	(= (available timber location4) 0)
	(= (available ore location4) 0)
	(= (available stone location4) 0)
	(= (available iron location4) 0)
	(= (available coal location4) 0)
	(mountain location5)
	(woodland location5)
	(= (housing location5) 0)
	(= (available wood location5) 0)
	(= (carts-at location5) 0)
	(= (available timber location5) 0)
	(= (available ore location5) 0)
	(= (available stone location5) 0)
	(= (available iron location5) 0)
	(= (available coal location5) 0)
	(woodland location6)
	(= (housing location6) 0)
	(= (available wood location6) 0)
	(= (carts-at location6) 0)
	(= (available timber location6) 0)
	(= (available ore location6) 0)
	(= (available stone location6) 0)
	(= (available iron location6) 0)
	(= (available coal location6) 0)
	(by-coast location7)
	(= (housing location7) 0)
	(= (available wood location7) 0)
	(= (carts-at location7) 0)
	(= (available timber location7) 0)
	(= (available ore location7) 0)
	(= (available stone location7) 0)
	(= (available iron location7) 0)
	(= (available coal location7) 0)
	(by-coast location8)
	(= (housing location8) 0)
	(= (available wood location8) 0)
	(= (carts-at location8) 0)
	(= (available timber location8) 0)
	(= (available ore location8) 0)
	(= (available stone location8) 0)
	(= (available iron location8) 0)
	(= (available coal location8) 0)
	(connected-by-land location0 location4)
	(connected-by-land location4 location0)
	(connected-by-land location1 location2)
	(connected-by-land location2 location1)
	(connected-by-land location1 location3)
	(connected-by-land location3 location1)
	(connected-by-land location1 location6)
	(connected-by-land location6 location1)
	(connected-by-land location2 location0)
	(connected-by-land location0 location2)
	(connected-by-land location2 location6)
	(connected-by-land location6 location2)
	(connected-by-land location3 location0)
	(connected-by-land location0 location3)
	(connected-by-land location4 location2)
	(connected-by-land location2 location4)
	(connected-by-land location4 location5)
	(connected-by-land location5 location4)
	(connected-by-land location4 location6)
	(connected-by-land location6 location4)
	(connected-by-land location4 location8)
	(connected-by-land location8 location4)
	(connected-by-land location5 location1)
	(connected-by-land location1 location5)
	(connected-by-land location5 location8)
	(connected-by-land location8 location5)
	(connected-by-land location6 location0)
	(connected-by-land location0 location6)
	(connected-by-land location6 location5)
	(connected-by-land location5 location6)
	(connected-by-land location6 location7)
	(connected-by-land location7 location6)
	(connected-by-land location6 location8)
	(connected-by-land location8 location6)
	(connected-by-land location7 location1)
	(connected-by-land location1 location7)
	(connected-by-land location7 location5)
	(connected-by-land location5 location7)
	(connected-by-land location7 location8)
	(connected-by-land location8 location7)
	(connected-by-land location8 location1)
	(connected-by-land location1 location8)
	(connected-by-land location8 location2)
	(connected-by-land location2 location8)
	(connected-by-sea location0 location8)
	(connected-by-sea location8 location0)
	(potential vehicle0)
	(potential vehicle1)
	(potential vehicle2)
	(potential vehicle3)
	(potential vehicle4)
	(potential vehicle5)
	(potential vehicle6)
	(potential vehicle7)


        (= (available timber vehicle0) 0)
        (= (available wood vehicle0) 0)
        (= (available coal vehicle0) 0)
        (= (available stone vehicle0) 0)
        (= (available iron vehicle0) 0)
        (= (available ore vehicle0) 0)
        (= (space-in vehicle0) 0)

        (= (available timber vehicle1) 0)
        (= (available wood vehicle1) 0)
        (= (available coal vehicle1) 0)
        (= (available stone vehicle1) 0)
        (= (available iron vehicle1) 0)
        (= (available ore vehicle1) 0)
        (= (space-in vehicle1) 0)

        (= (available timber vehicle2) 0)
        (= (available wood vehicle2) 0)
        (= (available coal vehicle2) 0)
        (= (available stone vehicle2) 0)
        (= (available iron vehicle2) 0)
        (= (available ore vehicle2) 0)
        (= (space-in vehicle2) 0)

        (= (available timber vehicle3) 0)
        (= (available wood vehicle3) 0)
        (= (available coal vehicle3) 0)
        (= (available stone vehicle3) 0)
        (= (available iron vehicle3) 0)
        (= (available ore vehicle3) 0)
        (= (space-in vehicle3) 0)

        (= (available timber vehicle4) 0)
        (= (available wood vehicle4) 0)
        (= (available coal vehicle4) 0)
        (= (available stone vehicle4) 0)
        (= (available iron vehicle4) 0)
        (= (available ore vehicle4) 0)
        (= (space-in vehicle4) 0)

        (= (available timber vehicle5) 0)
        (= (available wood vehicle5) 0)
        (= (available coal vehicle5) 0)
        (= (available stone vehicle5) 0)
        (= (available iron vehicle5) 0)
        (= (available ore vehicle5) 0)
        (= (space-in vehicle5) 0)

        (= (available timber vehicle6) 0)
        (= (available wood vehicle6) 0)
        (= (available coal vehicle6) 0)
        (= (available stone vehicle6) 0)
        (= (available iron vehicle6) 0)
        (= (available ore vehicle6) 0)
        (= (space-in vehicle6) 0)

        (= (available timber vehicle7) 0)
        (= (available wood vehicle7) 0)
        (= (available coal vehicle7) 0)
        (= (available stone vehicle7) 0)
        (= (available iron vehicle7) 0)
        (= (available ore vehicle7) 0)
        (= (space-in vehicle7) 0)

)
(:goal (and
	(connected-by-rail location7 location8)
	(connected-by-rail location8 location1)
	(connected-by-rail location1 location2)
	(connected-by-rail location7 location5)
	(connected-by-rail location5 location8)
	(has-coal-stack location3)
	(has-ironworks location5)
	(>= (housing location6) 2)
	(connected-by-rail location8 location2)
	(connected-by-rail location2 location6)
	(connected-by-rail location6 location5)
	(connected-by-rail location4 location8)
	(connected-by-rail location1 location3)
	(has-ironworks location0)
	(connected-by-rail location1 location6)
	(connected-by-rail location6 location8)
	(connected-by-rail location5 location1)
	(connected-by-rail location3 location0)
	)
)

(:metric minimize (+ (+ (* 3 (pollution)) (* 0 (resource-use))) (* 0 (labour))))
)
