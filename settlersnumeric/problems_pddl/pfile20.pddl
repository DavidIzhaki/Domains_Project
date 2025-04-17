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
	location9 - place
	location10 - place
	location11 - place
	location12 - place
	location13 - place
	location14 - place
	vehicle0 - vehicle
	vehicle1 - vehicle
	vehicle2 - vehicle
	vehicle3 - vehicle
	vehicle4 - vehicle
	vehicle5 - vehicle
	vehicle6 - vehicle
	vehicle7 - vehicle
	vehicle8 - vehicle
	vehicle9 - vehicle
)
(:init
	(= (resource-use) 0)
	(= (labour) 0)
	(= (pollution) 0)
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
	(= (housing location1) 0)
	(= (available wood location1) 0)
	(= (carts-at location1) 0)
	(= (available timber location1) 0)
	(= (available ore location1) 0)
	(= (available stone location1) 0)
	(= (available iron location1) 0)
	(= (available coal location1) 0)
	(woodland location2)
	(by-coast location2)
	(metalliferous location2)
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
	(by-coast location3)
	(= (housing location3) 0)
	(= (available wood location3) 0)
	(= (carts-at location3) 0)
	(= (available timber location3) 0)
	(= (available ore location3) 0)
	(= (available stone location3) 0)
	(= (available iron location3) 0)
	(= (available coal location3) 0)
	(mountain location4)
	(woodland location4)
	(by-coast location4)
	(= (housing location4) 0)
	(= (available wood location4) 0)
	(= (carts-at location4) 0)
	(= (available timber location4) 0)
	(= (available ore location4) 0)
	(= (available stone location4) 0)
	(= (available iron location4) 0)
	(= (available coal location4) 0)
	(woodland location5)
	(= (housing location5) 0)
	(= (available wood location5) 0)
	(= (carts-at location5) 0)
	(= (available timber location5) 0)
	(= (available ore location5) 0)
	(= (available stone location5) 0)
	(= (available iron location5) 0)
	(= (available coal location5) 0)
	(mountain location6)
	(woodland location6)
	(by-coast location6)
	(= (housing location6) 0)
	(= (available wood location6) 0)
	(= (carts-at location6) 0)
	(= (available timber location6) 0)
	(= (available ore location6) 0)
	(= (available stone location6) 0)
	(= (available iron location6) 0)
	(= (available coal location6) 0)
	(woodland location7)
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
	(woodland location9)
	(by-coast location9)
	(= (housing location9) 0)
	(= (available wood location9) 0)
	(= (carts-at location9) 0)
	(= (available timber location9) 0)
	(= (available ore location9) 0)
	(= (available stone location9) 0)
	(= (available iron location9) 0)
	(= (available coal location9) 0)
	(mountain location10)
	(woodland location10)
	(by-coast location10)
	(= (housing location10) 0)
	(= (available wood location10) 0)
	(= (carts-at location10) 0)
	(= (available timber location10) 0)
	(= (available ore location10) 0)
	(= (available stone location10) 0)
	(= (available iron location10) 0)
	(= (available coal location10) 0)
	(mountain location11)
	(woodland location11)
	(by-coast location11)
	(= (housing location11) 0)
	(= (available wood location11) 0)
	(= (carts-at location11) 0)
	(= (available timber location11) 0)
	(= (available ore location11) 0)
	(= (available stone location11) 0)
	(= (available iron location11) 0)
	(= (available coal location11) 0)
	(mountain location12)
	(= (housing location12) 0)
	(= (available wood location12) 0)
	(= (carts-at location12) 0)
	(= (available timber location12) 0)
	(= (available ore location12) 0)
	(= (available stone location12) 0)
	(= (available iron location12) 0)
	(= (available coal location12) 0)
	(woodland location13)
	(= (housing location13) 0)
	(= (available wood location13) 0)
	(= (carts-at location13) 0)
	(= (available timber location13) 0)
	(= (available ore location13) 0)
	(= (available stone location13) 0)
	(= (available iron location13) 0)
	(= (available coal location13) 0)
	(mountain location14)
	(woodland location14)
	(= (housing location14) 0)
	(= (available wood location14) 0)
	(= (carts-at location14) 0)
	(= (available timber location14) 0)
	(= (available ore location14) 0)
	(= (available stone location14) 0)
	(= (available iron location14) 0)
	(= (available coal location14) 0)
	(connected-by-land location0 location1)
	(connected-by-land location1 location0)
	(connected-by-land location0 location5)
	(connected-by-land location5 location0)
	(connected-by-land location0 location7)
	(connected-by-land location7 location0)
	(connected-by-land location0 location10)
	(connected-by-land location10 location0)
	(connected-by-land location0 location11)
	(connected-by-land location11 location0)
	(connected-by-land location0 location12)
	(connected-by-land location12 location0)
	(connected-by-land location0 location14)
	(connected-by-land location14 location0)
	(connected-by-land location1 location5)
	(connected-by-land location5 location1)
	(connected-by-land location1 location12)
	(connected-by-land location12 location1)
	(connected-by-land location1 location14)
	(connected-by-land location14 location1)
	(connected-by-land location2 location3)
	(connected-by-land location3 location2)
	(connected-by-land location2 location6)
	(connected-by-land location6 location2)
	(connected-by-land location3 location1)
	(connected-by-land location1 location3)
	(connected-by-land location3 location12)
	(connected-by-land location12 location3)
	(connected-by-land location4 location7)
	(connected-by-land location7 location4)
	(connected-by-land location4 location8)
	(connected-by-land location8 location4)
	(connected-by-land location4 location9)
	(connected-by-land location9 location4)
	(connected-by-land location5 location3)
	(connected-by-land location3 location5)
	(connected-by-land location5 location4)
	(connected-by-land location4 location5)
	(connected-by-land location5 location9)
	(connected-by-land location9 location5)
	(connected-by-land location5 location11)
	(connected-by-land location11 location5)
	(connected-by-land location6 location3)
	(connected-by-land location3 location6)
	(connected-by-land location6 location4)
	(connected-by-land location4 location6)
	(connected-by-land location7 location5)
	(connected-by-land location5 location7)
	(connected-by-land location7 location6)
	(connected-by-land location6 location7)
	(connected-by-land location7 location8)
	(connected-by-land location8 location7)
	(connected-by-land location7 location10)
	(connected-by-land location10 location7)
	(connected-by-land location7 location11)
	(connected-by-land location11 location7)
	(connected-by-land location8 location2)
	(connected-by-land location2 location8)
	(connected-by-land location8 location6)
	(connected-by-land location6 location8)
	(connected-by-land location8 location11)
	(connected-by-land location11 location8)
	(connected-by-land location9 location0)
	(connected-by-land location0 location9)
	(connected-by-land location9 location3)
	(connected-by-land location3 location9)
	(connected-by-land location9 location7)
	(connected-by-land location7 location9)
	(connected-by-land location9 location12)
	(connected-by-land location12 location9)
	(connected-by-land location10 location11)
	(connected-by-land location11 location10)
	(connected-by-land location10 location13)
	(connected-by-land location13 location10)
	(connected-by-land location11 location3)
	(connected-by-land location3 location11)
	(connected-by-land location12 location6)
	(connected-by-land location6 location12)
	(connected-by-land location13 location1)
	(connected-by-land location1 location13)
	(connected-by-land location13 location4)
	(connected-by-land location4 location13)
	(connected-by-land location13 location11)
	(connected-by-land location11 location13)
	(connected-by-land location13 location12)
	(connected-by-land location12 location13)
	(connected-by-land location14 location3)
	(connected-by-land location3 location14)
	(connected-by-land location14 location12)
	(connected-by-land location12 location14)
	(connected-by-sea location0 location6)
	(connected-by-sea location6 location0)
	(connected-by-sea location0 location8)
	(connected-by-sea location8 location0)
	(connected-by-sea location0 location11)
	(connected-by-sea location11 location0)
	(connected-by-sea location6 location8)
	(connected-by-sea location8 location6)
	(connected-by-sea location6 location11)
	(connected-by-sea location11 location6)
	(connected-by-sea location8 location11)
	(connected-by-sea location11 location8)
	(connected-by-sea location2 location3)
	(connected-by-sea location3 location2)
	(connected-by-sea location4 location9)
	(connected-by-sea location9 location4)
	(connected-by-sea location4 location10)
	(connected-by-sea location10 location4)
	(connected-by-sea location9 location10)
	(connected-by-sea location10 location9)
	(potential vehicle0)
	(potential vehicle1)
	(potential vehicle2)
	(potential vehicle3)
	(potential vehicle4)
	(potential vehicle5)
	(potential vehicle6)
	(potential vehicle7)
	(potential vehicle8)
	(potential vehicle9)


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

        (= (available timber vehicle8) 0)
        (= (available wood vehicle8) 0)
        (= (available coal vehicle8) 0)
        (= (available stone vehicle8) 0)
        (= (available iron vehicle8) 0)
        (= (available ore vehicle8) 0)
        (= (space-in vehicle8) 0)

        (= (available timber vehicle9) 0)
        (= (available wood vehicle9) 0)
        (= (available coal vehicle9) 0)
        (= (available stone vehicle9) 0)
        (= (available iron vehicle9) 0)
        (= (available ore vehicle9) 0)
        (= (space-in vehicle9) 0)

)
(:goal (and
	(has-sawmill location9)
	(has-ironworks location11)
	(has-coal-stack location1)
	(has-sawmill location14)
	(>= (housing location13) 1)
	(has-ironworks location1)
	(has-sawmill location5)
	(has-sawmill location6)
	(>= (housing location0) 2)
	(has-ironworks location3)
	(has-sawmill location0)
	(has-ironworks location4)
	(has-ironworks location7)
	(has-sawmill location1)
	(connected-by-rail location0 location10)
	(connected-by-rail location10 location13)
	(connected-by-rail location13 location11)
	(connected-by-rail location11 location3)
	(connected-by-rail location3 location1)
	)
)

(:metric minimize (+ (+ (* 0 (pollution)) (* 0 (resource-use))) (* 0 (labour))))
)
