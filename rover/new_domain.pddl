;; Rover Domain (Fixed Version with (calibrated ?c ?o ?r))

;;;;; What Changed from the old domain:

;; :predicates	Replaced (calibrated ?c ?r) with (calibrated ?c ?o ?r)
;; :action calibrate	Now sets (calibrated ?c ?o ?r)
;; :action take_image	Requires (calibrated ?c ?o ?r) for that specific objective
;; :action communicate_soil_data	Added a guard against duplicate communication of soil data 
;; :action communicate_rock_data	Added a guard against duplicate communication of rock data 
;; :action communicate_image_data	Added a guard against duplicate communication of image data (needed to add objective as a perameter for this too work)
;; maybe need to add energy decrease in drop action, sounds logical
(define (domain rover)
  ;(:requirements :typing :fluents)
  
  (:types
    rover - object
    waypoint - object
    store - object
    camera - object
    mode - object
    lander - object
    objective - object
  )

  (:predicates
    (in ?x - rover ?y - waypoint)
    (at_lander ?x - lander ?y - waypoint)
    (can_traverse ?r - rover ?x - waypoint ?y - waypoint)
    (equipped_for_soil_analysis ?r - rover)
    (equipped_for_rock_analysis ?r - rover)
    (equipped_for_imaging ?r - rover)
    (empty ?s - store)
    (full ?s - store)
    (have_rock_analysis ?r - rover ?w - waypoint)
    (have_soil_analysis ?r - rover ?w - waypoint)
    (calibrated ?c - camera ?o - objective ?r - rover)   ;; NEW: calibrated on specific objective
    (supports ?c - camera ?m - mode)
    (available ?r - rover)
    (visible ?w - waypoint ?p - waypoint)
    (have_image ?r - rover ?o - objective ?m - mode)
    (communicated_soil_data ?w - waypoint)
    (communicated_rock_data ?w - waypoint)
    (communicated_image_data ?o - objective ?m - mode)
    (at_soil_sample ?w - waypoint)
    (at_rock_sample ?w - waypoint)
    (visible_from ?o - objective ?w - waypoint)
    (store_of ?s - store ?r - rover)
    (calibration_target ?i - camera ?o - objective)
    (on_board ?i - camera ?r - rover)
    (channel_free ?l - lander)
    (in_sun ?w - waypoint)
  )

  (:functions
    (energy ?r - rover)
    (recharges)
  )

  (:action navigate
    :parameters (?r - rover ?from - waypoint ?to - waypoint)
    :precondition (and
      (can_traverse ?r ?from ?to)
      (available ?r)
      (in ?r ?from)
      (visible ?from ?to)
      (>= (energy ?r) 8)
    )
    :effect (and
      (decrease (energy ?r) 8)
      (not (in ?r ?from))
      (in ?r ?to)
    )
  )

  (:action recharge
    :parameters (?r - rover ?w - waypoint)
    :precondition (and
      (in ?r ?w)
      (in_sun ?w)
      (<= (energy ?r) 80)
    )
    :effect (and
      (increase (energy ?r) 20)
      (increase (recharges) 1)
    )
  )

  (:action sample_soil
    :parameters (?r - rover ?s - store ?w - waypoint)
    :precondition (and
      (in ?r ?w)
      (>= (energy ?r) 3)
      (at_soil_sample ?w)
      (equipped_for_soil_analysis ?r)
      (store_of ?s ?r)
      (empty ?s)
    )
    :effect (and
      (not (empty ?s))
      (full ?s)
      (decrease (energy ?r) 3)
      (have_soil_analysis ?r ?w)
      (not (at_soil_sample ?w))
    )
  )

  (:action sample_rock
    :parameters (?r - rover ?s - store ?w - waypoint)
    :precondition (and
      (in ?r ?w)
      (>= (energy ?r) 5)
      (at_rock_sample ?w)
      (equipped_for_rock_analysis ?r)
      (store_of ?s ?r)
      (empty ?s)
    )
    :effect (and
      (not (empty ?s))
      (full ?s)
      (decrease (energy ?r) 5)
      (have_rock_analysis ?r ?w)
      (not (at_rock_sample ?w))
    )
  )

  (:action drop
    :parameters (?r - rover ?s - store)
    :precondition (and
      (store_of ?s ?r)
      (full ?s)
    )
    :effect (and
      (not (full ?s))
      (empty ?s)
    )
  )

  (:action calibrate
    :parameters (?r - rover ?c - camera ?o - objective ?w - waypoint)
    :precondition (and
      (equipped_for_imaging ?r)
      (calibration_target ?c ?o)
      (in ?r ?w)
      (visible_from ?o ?w)
      (on_board ?c ?r)
      (>= (energy ?r) 2)
    )
    :effect (and
      (calibrated ?c ?o ?r)
      (decrease (energy ?r) 2)
    )
  )

  (:action take_image
    :parameters (?r - rover ?w - waypoint ?o - objective ?c - camera ?m - mode)
    :precondition (and
      (calibrated ?c ?o ?r)
      (on_board ?c ?r)
      (equipped_for_imaging ?r)
      (supports ?c ?m)
      (visible_from ?o ?w)
      (in ?r ?w)
      (>= (energy ?r) 1)
    )
    :effect (and
      (have_image ?r ?o ?m)
      (not (calibrated ?c ?o ?r))  
      (decrease (energy ?r) 1)
    )
  )

  (:action communicate_soil_data
    :parameters (?r - rover ?l - lander ?p - waypoint ?x - waypoint ?y - waypoint)
    :precondition (and
      (in ?r ?x)
      (at_lander ?l ?y)
      (have_soil_analysis ?r ?p)
      (visible ?x ?y)
      (available ?r)
      (channel_free ?l)
      (not (communicated_soil_data ?p)) ;;  guard against duplicate
      (>= (energy ?r) 4)
    )
    :effect (and
      (communicated_soil_data ?p)
      (available ?r)
      (decrease (energy ?r) 4)
    )
  )

  (:action communicate_rock_data
    :parameters (?r - rover ?l - lander ?p - waypoint ?x - waypoint ?y - waypoint)
    :precondition (and
      (in ?r ?x)
      (at_lander ?l ?y)
      (have_rock_analysis ?r ?p)
      (visible ?x ?y)
      (available ?r)
      (channel_free ?l)
      (not (communicated_rock_data ?p)) ;;  guard against duplicate
      (>= (energy ?r) 4)
    )
    :effect (and
      (communicated_rock_data ?p)
      (available ?r)
      (decrease (energy ?r) 4)
    )
  )

  (:action communicate_image_data
    :parameters (?r - rover ?l - lander ?o - objective ?m - mode ?x - waypoint ?y - waypoint)
    :precondition (and
      (in ?r ?x)
      (at_lander ?l ?y)
      (have_image ?r ?o ?m)
      (visible ?x ?y)
      (available ?r)
      (channel_free ?l)
      (not (communicated_image_data ?o ?m)) ;;  guard against duplicate
      (>= (energy ?r) 6)
    )
    :effect (and
      (communicated_image_data ?o ?m)
      (available ?r)
      (decrease (energy ?r) 6)
    )
  )
)
