# Connected environment

Road travel uses the existing SI route in `motion_state.py`: approach, stopped alley, acceleration, merge, corner, false safety and House 17. Buildings align to the local road tangent; traffic shares the environmental depth sort. The alley has a flush apron where the black car joins the road.

House 17 is on the left side of the parked witness car, at site X −7.2 m. `house_site.W` registers the site to the parked car's heading. A graded curb approach meets the entrance. `house_site.door_world` registers entrance, interior, stairwell and upstairs window in a common frame.

The upper floor is 2.7 m above the entrance, reached by fifteen 0.18 m rises and 0.25 m treads, with a U-turn landing. `HOUSE17_PLAN.json` is the active plan. The upstairs window uses the existing upper-left facade opening and looks onto the same simulated black car and street. The phone cabinet lies outside the approach/backstep route.

See `assets/environments/route-map.json`, `HOUSE17_PLAN.json` and `reports/building-road-clearance.json`. Orthographic V10 staging remains preserved as a separate authored view.
