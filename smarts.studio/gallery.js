(()=>{
// sliders
document.querySelectorAll('.car').forEach(c=>{const t=c.querySelector('.track'),items=[...t.children],cc=c.querySelector('.cc');if(items.length<2)return;
  const cur=()=>{const mid=t.scrollLeft+t.clientWidth/2;let b=0,d=1e9;items.forEach((a,i)=>{const x=Math.abs(a.offsetLeft-t.offsetLeft+a.offsetWidth/2-mid);if(x<d){d=x;b=i}});return b};
  const go=i=>{i=Math.max(0,Math.min(items.length-1,i));const a=items[i];t.scrollTo({left:a.offsetLeft-t.offsetLeft-(t.clientWidth-a.offsetWidth)/2,behavior:'smooth'})};
  c.querySelector('.cp').onclick=()=>go(cur()-1);c.querySelector('.cn').onclick=()=>{const i=cur();go(i===items.length-1?0:i+1)};
  let raf;t.addEventListener('scroll',()=>{cancelAnimationFrame(raf);raf=requestAnimationFrame(()=>cc.textContent=(cur()+1)+' / '+items.length)},{passive:true});
  t.tabIndex=0;t.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){e.preventDefault();go(cur()+1)}if(e.key==='ArrowLeft'){e.preventDefault();go(cur()-1)}});
});
// "show all" on long grids
document.querySelectorAll('[data-more]').forEach(b=>b.addEventListener('click',()=>{b.closest('.gal').querySelectorAll('a[hidden]').forEach(a=>a.hidden=false);b.parentNode.remove()}));
})();
