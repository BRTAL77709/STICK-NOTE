# Fixed-world route and continuity

World Y up; witness initially drives +Z. Crime origin: (0,0,0). The black sedan begins 12m behind the witness. Commanded steering starts straight, turns toward +X, unwinds, then steers toward -X and returns toward straight. Both vehicles use this connected street and their own integrated state. Positive steering means a right turn toward +X; model wheelbase 2.60m. Final test positions are in `vehicle_dynamics.RUN` and the contact CSVs.

The city's centreline is sampled once from the input-driven witness route, with straight extensions before/after the six-second interval. Buildings, curbs, pavement, markings and House 17 have fixed coordinates. House 17 is at Z50 on the +X side, façade X=road_x(50)+6.8. Proposed parking area is near Z46–50, along that same street. The tests do not depict the full crime-to-arrival route; integration into the film remains pending approval.

Bedroom local floor maps to world Y2.6 at House 17. Local +Z points out toward the road (world -X), local +X maps along world +Z. The parked sedan is local(-4,-2.6,5.2), placing it on the street below and several metres before the house. The window reveal and city therefore have a declared transform; no claim is made that the six-second chase already includes parking.

Clean steering cuts once from cockpit to an exterior front-quarter angle at 3.15s. Both read the exact same time/state, heading, car geometry and city. Chase follows the midpoint of both actual cars. The corrected external camera stays within the road corridor; the earlier trial crossed a building and is excluded from delivery. No repeated scrolling background is used.

## Local test frames

The door, stair and bedroom interaction harnesses use local metre coordinates. For house integration, the stair test represents the upper four-riser flight from an intermediate landing at world Y1.88 to the bedroom floor at Y2.60 (.72m rise). It does not depict the entire lower flight. This avoids interpreting the local Y0 of a focused rig test as the street's ground floor. The rest of the lower flight/hallway connection has not been rendered in M03 and requires continuity review before full-film integration. No earlier building model is overwritten by these harnesses.
