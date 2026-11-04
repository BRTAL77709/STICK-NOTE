# Active animation system

`engine/composition/scene_sources.py` dispatches the 18 independently reusable scene entries. `engine/animation/scene_builder.py` composes SVG at global film time. Cairo/librsvg rasterizes; FFmpeg encodes independent previews and HD H.264 clips. Content hashes identify rendered source rather than relying only on timestamps.

`motion_state.py` supplies SI vehicle positions, speed, acceleration, heading, steering, wheels and RPM. `world.py` projects curved streets, tangent-aligned buildings, lights and depth-sorted traffic. `driver_rig.py` solves two arm chains onto the wheel; `driving.py` solves a rigid shoe and bent leg against a hinged pedal.

`articulated.py` solves fixed-length two-bone limbs and uses the approved head/hoodie language. Active action controllers are `house_site.py` (exit/run), `house_actions.py` (key/door), `stairs_actions.py` (15-step U-turn stair), and `room_actions.py` (curtain/phone/acting). Ground contacts are world targets independent of camera. Planted shoes use their own depth scale. Hand targets follow prop pivots or devices, with purposeful reach/grip/release intervals.

`v10_trunk.py` is unchanged. Legacy `house17.py` remains for compatibility but is not the active door/stair/phone action source. `engine/api.py` exposes the current state and controllers.

The system is 2D vector animation with projected 2.5D layouts, not a general-purpose dynamics or cloth simulator. Audits constrain bones and contact targets, not every painted mesh vertex.
