(()=>{
// sliders: every photo (first and last too) sits centred; clicking a photo at the edge moves to it
document.querySelectorAll('.car').forEach(c=>{const t=c.querySelector('.track'),items=[...t.children],cc=c.querySelector('.cc');if(!items.length)return;
  const pad=()=>{const w=t.clientWidth;t.style.paddingLeft=Math.max(0,(w-items[0].offsetWidth)/2)+'px';t.style.paddingRight=Math.max(0,(w-items[items.length-1].offsetWidth)/2)+'px'};
  pad();addEventListener('resize',pad);
  if(items.length<2)return;
  // wide click zones on both sides
  ['l','r'].forEach(d=>{const z=document.createElement('button');z.className='zone '+d;z.setAttribute('aria-label',d==='l'?'Previous photo':'Next photo');z.onclick=()=>{go(cur()+(d==='l'?-1:1));stop()};c.appendChild(z)});
  const centre=a=>a.offsetLeft-t.offsetLeft+a.offsetWidth/2;
  const cur=()=>{const mid=t.scrollLeft+t.clientWidth/2;let b=0,d=1e9;items.forEach((a,i)=>{const x=Math.abs(centre(a)-mid);if(x<d){d=x;b=i}});return b};
  const go=i=>{i=(i+items.length)%items.length;t.scrollTo({left:centre(items[i])-t.clientWidth/2,behavior:'smooth'})};
  const label=()=>{const i=cur(),ti=items[i].dataset.title;cc.textContent=(i+1)+' / '+items.length+(ti?'  -  '+ti:'');items.forEach((a,k)=>a.classList.toggle('side',k!==i))};
  label();
  c.querySelector('.cp').onclick=()=>{go(cur()-1);stop()};c.querySelector('.cn').onclick=()=>{go(cur()+1);stop()};
  let raf;t.addEventListener('scroll',()=>{cancelAnimationFrame(raf);raf=requestAnimationFrame(label)},{passive:true});
  t.addEventListener('click',e=>{const a=e.target.closest('a');if(!a)return;const i=items.indexOf(a);if(i!==cur()){e.preventDefault();e.stopPropagation();go(i);stop()}},true);
  t.tabIndex=0;t.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){e.preventDefault();go(cur()+1);stop()}if(e.key==='ArrowLeft'){e.preventDefault();go(cur()-1);stop()}});
  // self-playing sliders: advance on a timer while on screen; stop for good once the visitor takes over
  let timer=null,stopped=false;const stop=()=>{stopped=true;clearInterval(timer);timer=null};
  if(c.dataset.auto){const ms=+c.dataset.auto;
    const play=()=>{if(!timer&&!stopped)timer=setInterval(()=>go(cur()+1),ms)},pause=()=>{clearInterval(timer);timer=null};
    new IntersectionObserver(es=>es[0].isIntersecting?play():pause(),{threshold:.5}).observe(c);
    c.addEventListener('mouseenter',pause);c.addEventListener('mouseleave',play);
    t.addEventListener('pointerdown',stop);t.addEventListener('wheel',stop,{passive:true});t.addEventListener('touchstart',stop,{passive:true});}
});
// YouTube previews: use the sharp picture, fall back when a video has none
document.querySelectorAll('.yt img').forEach(i=>{const fix=()=>{if(i.naturalWidth&&i.naturalWidth<200&&!i.dataset.fb){i.dataset.fb=1;i.src=i.src.replace('maxresdefault','hqdefault')}};i.complete?fix():i.addEventListener('load',fix)});
// YouTube: load the player only when the picture is clicked
document.querySelectorAll('.yt').forEach(b=>b.addEventListener('click',()=>{const f=document.createElement('iframe');
  f.src='https://www.youtube-nocookie.com/embed/'+b.dataset.id+'?autoplay=1'+(b.dataset.list?'&list='+b.dataset.list:'');f.allow='autoplay; encrypted-media; picture-in-picture';f.allowFullscreen=true;f.title='Video';b.replaceChildren(f);b.style.cursor='default'},{once:true}));
})();
