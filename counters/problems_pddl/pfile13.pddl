;; Enrico Scala (enricos83@gmail.com) and Miquel Ramirez (miquel.ramirez@gmail.com)
(define (problem instance_32_2)
  (:domain fn-counters)
  (:objects
    c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 c27 c28 c29 c30 c31 - counter
  )

  (:init
    (= (max_int) 64)
	(= (value c0) 31)
	(= (value c1) 20)
	(= (value c2) 4)
	(= (value c3) 10)
	(= (value c4) 6)
	(= (value c5) 57)
	(= (value c6) 1)
	(= (value c7) 10)
	(= (value c8) 34)
	(= (value c9) 29)
	(= (value c10) 55)
	(= (value c11) 57)
	(= (value c12) 40)
	(= (value c13) 39)
	(= (value c14) 54)
	(= (value c15) 14)
	(= (value c16) 24)
	(= (value c17) 34)
	(= (value c18) 24)
	(= (value c19) 42)
	(= (value c20) 16)
	(= (value c21) 37)
	(= (value c22) 54)
	(= (value c23) 25)
	(= (value c24) 35)
	(= (value c25) 58)
	(= (value c26) 2)
	(= (value c27) 18)
	(= (value c28) 4)
	(= (value c29) 49)
	(= (value c30) 1)
	(= (value c31) 35)
  )

  (:goal (and 
(<= (+ (value c0) 1) (value c1))
(<= (+ (value c1) 1) (value c2))
(<= (+ (value c2) 1) (value c3))
(<= (+ (value c3) 1) (value c4))
(<= (+ (value c4) 1) (value c5))
(<= (+ (value c5) 1) (value c6))
(<= (+ (value c6) 1) (value c7))
(<= (+ (value c7) 1) (value c8))
(<= (+ (value c8) 1) (value c9))
(<= (+ (value c9) 1) (value c10))
(<= (+ (value c10) 1) (value c11))
(<= (+ (value c11) 1) (value c12))
(<= (+ (value c12) 1) (value c13))
(<= (+ (value c13) 1) (value c14))
(<= (+ (value c14) 1) (value c15))
(<= (+ (value c15) 1) (value c16))
(<= (+ (value c16) 1) (value c17))
(<= (+ (value c17) 1) (value c18))
(<= (+ (value c18) 1) (value c19))
(<= (+ (value c19) 1) (value c20))
(<= (+ (value c20) 1) (value c21))
(<= (+ (value c21) 1) (value c22))
(<= (+ (value c22) 1) (value c23))
(<= (+ (value c23) 1) (value c24))
(<= (+ (value c24) 1) (value c25))
(<= (+ (value c25) 1) (value c26))
(<= (+ (value c26) 1) (value c27))
(<= (+ (value c27) 1) (value c28))
(<= (+ (value c28) 1) (value c29))
(<= (+ (value c29) 1) (value c30))
(<= (+ (value c30) 1) (value c31))
  ))

  
)
