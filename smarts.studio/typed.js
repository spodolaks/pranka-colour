// Typewriter: <span data-typed="word one;word two"> types each phrase, deletes it, types the next.
// With data-intro on a parent, the text before it is typed out first (as on the old site).
(()=>{const sleep=ms=>new Promise(r=>setTimeout(r,ms));
document.querySelectorAll('[data-typed]').forEach(async el=>{
  const words=el.dataset.typed.split(';'),box=el.closest('[data-intro]');
  if(box){const nodes=[...box.childNodes],texts=[];box.style.minHeight=box.offsetHeight+'px';
    // empty every text node, then refill them character by character in order
    const walk=n=>{if(n===el)return;if(n.nodeType===3){texts.push([n,n.textContent]);n.textContent=''}else n.childNodes.forEach(walk)};nodes.forEach(walk);
    el.textContent='';const wrap=el.parentNode;wrap.style.visibility='hidden';box.querySelectorAll('br').forEach(b=>b.hidden=true);
    await sleep(300);
    for(const [n,full] of texts){const br=n.previousSibling;if(br&&br.tagName==='BR')br.hidden=false;for(let i=1;i<=full.length;i++){n.textContent=full.slice(0,i);if(full[i-1].trim())await sleep(28)}}
    wrap.style.visibility='';}
  else el.textContent='';
  let i=0;for(;;){const w=words[i%words.length];
    for(let n=1;n<=w.length;n++){el.textContent=w.slice(0,n);await sleep(90)}
    if(words.length<2)break;await sleep(1800);
    for(let n=w.length-1;n>=0;n--){el.textContent=w.slice(0,n);await sleep(45)}
    await sleep(300);i++}
});})();
