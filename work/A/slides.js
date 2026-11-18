(()=>{const slides=[...document.querySelectorAll('.slide')];let current=0,start=0,elapsed=0,running=false;
function resize(){document.documentElement.style.setProperty('--scale',Math.max(.15,Math.min((innerWidth-24)/1920,(innerHeight-90)/1080)))}
function show(n){current=Math.max(0,Math.min(slides.length-1,n));slides.forEach((s,i)=>s.classList.toggle('active',i===current));document.getElementById('page').textContent=`${current+1} / ${slides.length}`;history.replaceState(null,'',`#slide-${String(current+1).padStart(2,'0')}`);if(document.body.classList.contains('overview'))slides[current].scrollIntoView({block:'center'})}
document.getElementById('prev').onclick=()=>show(current-1);document.getElementById('next').onclick=()=>show(current+1);
document.getElementById('overview').onclick=()=>{document.body.classList.toggle('overview');show(current)};
document.getElementById('timer').onclick=()=>{if(running){elapsed+=Date.now()-start;running=false}else{start=Date.now();running=true}document.getElementById('timer').textContent=running?'타이머 정지':'타이머 시작'};
setInterval(()=>{const total=Math.floor((elapsed+(running?Date.now()-start:0))/1000);document.getElementById('clock').textContent=`${String(Math.floor(total/60)).padStart(2,'0')}:${String(total%60).padStart(2,'0')} / 20:00`},500);
document.addEventListener('keydown',ev=>{if(/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)||document.activeElement.tagName==='VIDEO')return;if(['ArrowRight','PageDown',' '].includes(ev.key)){ev.preventDefault();show(current+1)}if(['ArrowLeft','PageUp'].includes(ev.key)){ev.preventDefault();show(current-1)}if(ev.key==='Home'){ev.preventDefault();show(0)}if(ev.key==='End'){ev.preventDefault();show(slides.length-1)}if(ev.key.toLowerCase()==='g')document.getElementById('overview').click();if(ev.key.toLowerCase()==='f'&&!document.fullscreenElement)document.documentElement.requestFullscreen().catch(()=>{});});
const video=document.getElementById('demo-video');if(video){video.addEventListener('error',()=>{video.dataset.missing='true';},true)}
window.addEventListener('resize',resize);resize();const match=location.hash.match(/slide-(\d+)/);show(match?Number(match[1])-1:0);
})();
