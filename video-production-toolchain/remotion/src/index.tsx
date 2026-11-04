import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Composition,registerRoot,useCurrentFrame,delayRender,continueRender,cancelRender,staticFile} from 'remotion';
import timeline from '../../shared/timeline.json';
let loaded:string[]|null=null;let pending:Promise<string[]>|null=null;
function loadFrames(){if(loaded)return Promise.resolve(loaded);if(!pending)pending=fetch(staticFile('frames.json.gz')).then(r=>{if(!r.ok||!r.body)throw Error('Missing evaluated rig frames');return new Response(r.body.pipeThrough(new DecompressionStream('gzip'))).json()}).then(x=>loaded=x);return pending;}
function useRigFrames(){const [data,set]=useState(loaded);const [wait]=useState(()=>delayRender('Load deterministic rig geometry',{timeoutInMilliseconds:120000}));useEffect(()=>{loadFrames().then(x=>{set(x);continueRender(wait)}).catch(cancelRender)},[]);return data;}

// Every SVG has freshly evaluated joints, wheel angles, prop contacts and projection.
// The Python solver owns rig mathematics; Remotion owns frame selection/composition.
export const ArticulatedVectorScene:React.FC<{frame:number}>=({frame})=>{const frames=useRigFrames();return frames?<div style={{width:timeline.width,height:timeline.height}} dangerouslySetInnerHTML={{__html:frames[frame]}}/>:null;};
export const PedalScene=({frame}:{frame:number})=><ArticulatedVectorScene frame={frame}/>;
export const StreetScene=({frame}:{frame:number})=><ArticulatedVectorScene frame={frame}/>;
export const Demo=()=>{const frame=useCurrentFrame();const shot=timeline.shots.find(s=>frame>=s.startFrame&&frame<s.startFrame+s.frames)!;
 return <AbsoluteFill style={{background:'#06131e'}}>{shot.kind==='A'?<PedalScene frame={frame}/>:<StreetScene frame={frame}/>}</AbsoluteFill>};
registerRoot(()=> <Composition id={timeline.id} component={Demo} width={timeline.width} height={timeline.height} fps={timeline.fps} durationInFrames={timeline.frames}/>);
