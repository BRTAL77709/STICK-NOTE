/* V4 reusable extensions to actual HyperFrames GSAP compositions. */
(()=>{
 const C=HFComponents;
 class TachometerOverlay{
  constructor(value,needle,bar){this.counter=new C.AnimatedCounter(value,{decimals:1});this.needle=document.querySelector(needle);this.bar=new C.AnimatedProgressBar(bar,{max:8});}
  render(state){const v=state.rpm/1000;this.counter.render(v);this.bar.render(v);this.needle.setAttribute('transform',`rotate(${140+260*v/8} 170 144)`);}
 }
 class AnimatedTransition{
  constructor(node){this.node=document.querySelector(node);}
  animate(tl,start,end){tl.fromTo(this.node,{scaleX:0,opacity:.3},{scaleX:1,opacity:1,duration:.28,ease:'power2.out'},start+.04);tl.to(this.node,{scaleX:.12,opacity:0,duration:.14,ease:'power2.in'},end-.14);}
 }
 class WordByWordCaptions{
  constructor(node){this.node=document.querySelector(node);}
  // Use measured word timing records only. No fabricated equal-duration subdivision.
  words(tl,records){records.forEach((r,i)=>{const n=this.node.querySelectorAll('.caption-word')[i];tl.fromTo(n,{opacity:.35,scale:1},{opacity:1,scale:1.025,duration:.08,ease:'power2.out'},r.start);tl.to(n,{scale:1,duration:.12},r.end-.06);});}
  // Production V4 uses exact measured full-sentence windows because word alignment is unavailable.
  phrase(tl,start,end){tl.fromTo(this.node,{opacity:0,y:8,scale:.985},{opacity:1,y:0,scale:1,duration:.12,ease:'power2.out'},start);tl.to(this.node,{opacity:0,y:-3,duration:.09,ease:'power2.in'},end-.09);}
 }
 window.V4Components={TachometerOverlay,AnimatedTransition,WordByWordCaptions};
})();
