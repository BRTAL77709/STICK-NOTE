# Remaining defects and limits

All eight clips require artistic review. No 10/10 or professional-quality rating is claimed.

- Acting is authored and kinematic. Native IK provides articulated geometry and contact targets; it does not solve full-body forces, dynamic balance or muscle effort. Some pauses, elbow paths and running transitions may still feel restrained or mechanical.
- The approved illustrated head is a camera-relative vector/card treatment with front/profile/rear visibility, not a volumetric facial rig. Head looks are graphic approximations; cap/face perspective and emotional acting still need visual judgment.
- Curtain material width is constrained through folded horizontal polylines, with row lag and damped settling. There is no general cloth-force, self-collision or friction simulation. Folds can still look regular.
- Vehicle movement is a 120Hz kinematic bicycle integration plus suspension/body-response approximations. It is not a tyre-force/friction simulator. Headlights/reflections and geometric mirror images are stylized, not full optical ray tracing.
- Character contact-marker success does not certify full mitten/finger/shoe surface contact. Full continuous swept collision detection is absent. Door/jamb and exit-ground sampled body checks are reported separately, including any failure; do not infer collision-free motion from wrist/foot-target metrics.
- The staircase is retained M05, not a newly approved climb. It depicts the final short flight and landing, not a complete ground-to-second-floor route. Native M04 baseline numerical measurements are independently rechecked; they are not falsely labelled as new M07 artistic improvements.
- The city/House17/window use shared transforms and the sedan uses the actual parked pursuit state. The complete house is not a certified navigable architectural model. Interior cutaway visibility is deliberate for cinematography and can expose simplified construction.
- Native actor edits can be exported into the cinematic pipeline. Native prop/world objects are editable mirrors of the Python controllers: changing a prop only in Blender does not automatically modify the scripted cinematic renderer. See REBUILD before editing.
- Actual final-frame inspection: cockpit elbows/seating remain angular, some angles magnify the head, and curtain folds can still read like vertical strips. These are unresolved artistic defects, not numerical successes.
- Lighting/contact shadows are stylized approximations. The environment is more detailed but remains procedural and may still look like a prototype beside the supplied direction reference.
- Foley is synthesized locally. Waveform, event timing and decode are checked; no human auditory approval or original studio recording is claimed. Narration/subtitles are intentionally omitted from isolated interaction tests.
- Camera cuts are motivated coverage, not a guarantee of flawless spatial continuity. Fixed diagnostic clips and complete ordered frame sheets expose contact paths separately.

Read the measured QA report before assessing technical readiness. Numerical passing tolerances are not artistic approval, and any measured failure remains a failure.
