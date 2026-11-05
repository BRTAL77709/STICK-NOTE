import React from 'react';
import {AbsoluteFill,Composition,Sequence,OffthreadVideo,registerRoot,staticFile,useCurrentFrame,interpolate} from 'remotion';
import narration from '../../audio/narration-tests.json';
const shots=[{key:'A',frames:150,start:0},{key:'B',frames:234,start:150},{key:'C',frames:240,start:384}];
const Shot=({id}:{id:string})=>{const f=useCurrentFrame();const cue=narration.find(x=>x.shot===id&&f/30>=x.start&&f/30<x.end);return <AbsoluteFill><OffthreadVideo src={staticFile('shot-'+id+'.mp4')}/>{cue&&<div style={{position:'absolute',top:90,left:65,right:65,textAlign:'center',fontFamily:'Arial,sans-serif',fontSize:46,fontWeight:700,color:'#f4efe6',textShadow:'0 3px 8px #000',opacity:interpolate(f,[cue.start*30,cue.start*30+3],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}>{cue.text}</div>}</AbsoluteFill>};
const Reel=()=> <AbsoluteFill style={{background:'#06131e'}}>{shots.map(s=><Sequence key={s.key} from={s.start} durationInFrames={s.frames}><Shot id={s.key}/></Sequence>)}</AbsoluteFill>;
registerRoot(()=> <Composition id="NOIRFRAME-PROOF-REVIEW" component={Reel} width={1080} height={1920} fps={30} durationInFrames={624}/>);
