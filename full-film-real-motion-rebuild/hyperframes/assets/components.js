/* Reusable HyperFrames/GSAP graphic components. API contract: paused registered timelines + hf-seek. */
(function(){
  const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
  class CinematicHUDPanel{
    constructor(node){this.node=typeof node==='string'?document.querySelector(node):node;}
    animate(tl,start,end){tl.fromTo(this.node,{opacity:0,x:-18},{opacity:1,x:0,duration:.24,ease:'power3.out'},start);if(end)tl.to(this.node,{opacity:0,x:6,duration:.16,ease:'power2.in'},end-.16);return this;}
  }
  class AnimatedCounter{
    constructor(node,{initial=0,target=0,decimals=0,unit=''}={}){this.node=document.querySelector(node);this.initial=initial;this.target=target;this.decimals=decimals;this.unit=unit;this.render(initial);}
    render(value){this.node.textContent=Number(value).toFixed(this.decimals)+this.unit;}
    tween(tl,start,duration){const p={v:this.initial};tl.to(p,{v:this.target,duration,ease:'power2.inOut',onUpdate:()=>this.render(p.v)},start);}
  }
  class AnimatedProgressBar{
    constructor(node,{min=0,max=100}={}){this.node=document.querySelector(node);this.min=min;this.max=max;}
    render(value){gsap.set(this.node,{scaleX:clamp((value-this.min)/(this.max-this.min)),transformOrigin:'left center'});}
  }
  class DigitalClock{
    constructor(node,seconds=8220){this.node=document.querySelector(node);this.initial=seconds;}
    render(elapsed){const s=this.initial+Math.floor(elapsed);this.node.textContent=String(Math.floor(s/3600)%24).padStart(2,'0')+':'+String(Math.floor(s/60)%60).padStart(2,'0')+':'+String(s%60).padStart(2,'0');}
  }
  class SpeedometerOverlay{
    constructor({value,needle,bar,max=140}){this.counter=new AnimatedCounter(value,{initial:vehicleAt(0).speed_kmh,target:vehicleAt(window.FILM_DURATION||15).speed_kmh,decimals:0});this.needle=document.querySelector(needle);this.bar=new AnimatedProgressBar(bar,{min:0,max});this.max=max;}
    render(state){this.counter.render(state.speed_kmh);this.bar.render(state.speed_kmh);if(this.needle)this.needle.setAttribute('transform',`rotate(${140+260*state.speed_kmh/this.max} 170 144)`);}
  }
  class PursuitDistanceHUD{
    constructor(value,bar){this.counter=new AnimatedCounter(value,{initial:vehicleAt(0).pursuit_distance_m,target:vehicleAt(window.FILM_DURATION||15).pursuit_distance_m,decimals:1});this.bar=new AnimatedProgressBar(bar,{min:0,max:40});}
    render(state){this.counter.render(state.pursuit_distance_m);this.bar.render(40-state.pursuit_distance_m);}
  }
  class IncomingCallInterface extends CinematicHUDPanel{
    static markup(label='UNKNOWN CALLER'){return `<section class="panel"><div class="label">${label}</div><div class="value">INCOMING CALL</div><div class="call-controls">DECLINE · ANSWER</div></section>`;}
    ring(tl,start,duration){tl.fromTo(this.node,{rotation:-.3},{rotation:.3,duration:.08,repeat:Math.max(0,Math.floor(duration/.08)-1),yoyo:true,ease:'sine.inOut'},start);}
  }
  class MillionDollarOffer extends AnimatedCounter{
    constructor(node){super(node,{initial:0,target:1000000});}
    render(v){if(this.node)this.node.textContent='$'+Math.round(v).toLocaleString('en-US');}
  }
  class InteractiveChoiceCards{
    constructor(a,b){this.cards=[document.querySelector(a),document.querySelector(b)];}
    reveal(tl,start){this.cards.forEach((n,i)=>tl.fromTo(n,{opacity:0,y:22},{opacity:1,y:0,duration:.32,ease:'power3.out'},start+i*.12));}
    select(index){this.cards.forEach((n,i)=>n.dataset.selected=String(i===index));}
  }
  function vehicleAt(t){const a=window.VEHICLE_FRAMES;const f=clamp(t*30,0,a.length-1),i=Math.floor(f),j=Math.min(i+1,a.length-1),u=f-i;const s={};for(const k of Object.keys(a[i]))s[k]=typeof a[i][k]==='number'?a[i][k]+(a[j][k]-a[i][k])*u:a[i][k];return s;}
  window.HFComponents={CinematicHUDPanel,AnimatedCounter,AnimatedProgressBar,DigitalClock,SpeedometerOverlay,PursuitDistanceHUD,IncomingCallInterface,MillionDollarOffer,InteractiveChoiceCards,vehicleAt};
})();
