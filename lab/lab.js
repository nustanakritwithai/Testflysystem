const C=document.querySelector('#world'),ctx=C.getContext('2d');
const names=['foodL','foodR','threatL','threatR','hunger','approach','escape','motorL','motorR'];
const N=names.length, ix=Object.fromEntries(names.map((n,i)=>[n,i]));
let a=new Float64Array(N), input=new Float64Array(N); const tau=.22,dt=.02;
// Artificial circuit. Connections create behavior; sensors never issue motor commands.
const E=[]; const edge=(s,t,w)=>E.push([ix[s],ix[t],w]);
edge('foodL','approach',1.15); edge('foodR','approach',1.15); edge('hunger','approach',.75);
edge('threatL','escape',1.6); edge('threatR','escape',1.6); edge('escape','approach',-.9); edge('approach','escape',-.35);
edge('approach','motorL',.55); edge('approach','motorR',.55);
edge('foodL','motorR',.8); edge('foodR','motorL',.8); // orient toward food
edge('escape','motorL',.7); edge('escape','motorR',.7);
edge('threatL','motorL',.95); edge('threatR','motorR',.95); // turn away through differential drive
edge('approach','approach',.28); edge('escape','escape',.34);
let fly,food,threat;
function reset(){fly={x:400,y:270,ang:-1.4,energy:.65};food={x:160,y:110};threat={x:650,y:150};a.fill(0)} reset();
const rnd=()=>({x:60+Math.random()*680,y:60+Math.random()*400});
document.querySelector('#reset').onclick=reset;document.querySelector('#food').onclick=()=>food=rnd();document.querySelector('#threat').onclick=()=>threat=rnd();
function sense(obj,range){let dx=obj.x-fly.x,dy=obj.y-fly.y,d=Math.hypot(dx,dy),rel=Math.atan2(Math.sin(Math.atan2(dy,dx)-fly.ang),Math.cos(Math.atan2(dy,dx)-fly.ang));let v=Math.max(0,1-d/range);return {l:v*Math.max(0,Math.cos(rel+.7)),r:v*Math.max(0,Math.cos(rel-.7)),d}}
function neural(){input.fill(0);let f=sense(food,300),t=sense(threat,260);input[ix.foodL]=f.l;input[ix.foodR]=f.r;input[ix.threatL]=t.l;input[ix.threatR]=t.r;input[ix.hunger]=1-fly.energy;let drive=Float64Array.from(input);for(const[s,tg,w]of E)drive[tg]+=a[s]*w;let next=new Float64Array(N),alpha=dt/tau;for(let i=0;i<N;i++)next[i]=a[i]+alpha*(-a[i]+Math.tanh(drive[i]));a=next}
function physics(){let L=Math.max(0,a[ix.motorL]),R=Math.max(0,a[ix.motorR]);let speed=(L+R)*48,turn=(R-L)*2.8;fly.ang+=turn*dt;fly.x+=Math.cos(fly.ang)*speed*dt;fly.y+=Math.sin(fly.ang)*speed*dt;fly.x=(fly.x+C.width)%C.width;fly.y=(fly.y+C.height)%C.height;fly.energy=Math.max(0,fly.energy-.002*dt*60);if(Math.hypot(fly.x-food.x,fly.y-food.y)<18){fly.energy=Math.min(1,fly.energy+.35);food=rnd()}}
function dot(o,r,c){ctx.fillStyle=c;ctx.beginPath();ctx.arc(o.x,o.y,r,0,7);ctx.fill()}
function draw(){ctx.clearRect(0,0,C.width,C.height);ctx.strokeStyle='#17343e';for(let x=0;x<C.width;x+=40){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,C.height);ctx.stroke()}for(let y=0;y<C.height;y+=40){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(C.width,y);ctx.stroke()}dot(food,10,'#62e58b');dot(threat,13,'#ff6577');ctx.save();ctx.translate(fly.x,fly.y);ctx.rotate(fly.ang);ctx.fillStyle='#69d9ff';ctx.beginPath();ctx.moveTo(15,0);ctx.lineTo(-10,-8);ctx.lineTo(-10,8);ctx.closePath();ctx.fill();ctx.restore()}
const bars=document.querySelector('#bars');names.forEach((n,i)=>bars.insertAdjacentHTML('beforeend',`<div class="row"><span>${n}</span><div class="bar"><div class="fill" id="b${i}"></div></div><span id="v${i}"></span></div>`));
function ui(){names.forEach((n,i)=>{let v=Math.max(0,Math.min(1,(a[i]+1)/2));document.querySelector('#b'+i).style.width=(v*100)+'%';document.querySelector('#v'+i).textContent=a[i].toFixed(2)});document.querySelector('#state').textContent=`energy  ${fly.energy.toFixed(2)}\nheading ${fly.ang.toFixed(2)}\nneurons ${N}\nedges   ${E.length}\ndt      ${dt}s`}
let acc=0,last=performance.now();function loop(now){acc+=Math.min(.1,(now-last)/1000);last=now;while(acc>=dt){neural();physics();acc-=dt}draw();ui();requestAnimationFrame(loop)}requestAnimationFrame(loop);