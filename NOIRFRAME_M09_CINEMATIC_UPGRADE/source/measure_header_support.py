"""Authored fabric-pin/rail contact; native fabric parity is measured separately."""
import gzip,json,numpy as np
from bootstrap import ROOT as R
tag=json.loads((R/'reports/SHOT_REVISIONS.json').read_text())['WINDOW_CURTAIN'];d=json.load(gzip.open(R/'scenes'/f'WINDOW_CURTAIN_{tag}.json.gz','rt'));worst=0.;xmin=1e6;xmax=-1e6
for q in d['state']:
 top=np.array(q['fabric'])[0,::6];worst=max(worst,float(np.abs(top[:,2]+.21).max()),float(np.abs(top[:,1]-2.15).max()));xmin=min(xmin,float(top[:,0].min()));xmax=max(xmax,float(top[:,0].max()))
out={'native_source_tag':tag,'max_authored_top_pin_to_rail_tab_alignment_error_m':worst,'rail_y_m':2.23,'fabric_header_y_m':2.15,'tab_span_m':.08,'rail_z_m':-.21,'ring_x_range_m':[xmin,xmax],'rail_x_range_m':[-.86,.86],'technical_status':'TECHNICAL PASS' if worst<1e-6 and xmin>=-.86 and xmax<=.86 else 'TECHNICAL FAIL','scope':'Source mesh-pin positions plus actual scripted rail/tab geometry. This is a controlled attachment, not force/friction simulation; sampled saved-native fabric parity is reported separately.'};(R/'reports/CURTAIN_SUPPORT.json').write_text(json.dumps(out,indent=2));print(out)
