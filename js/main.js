/* COMUNIKOO — Minimal JS (<1KB)
   Only 3 features: mobile menu, header scroll, sidebar highlight */

// Mobile menu toggle
document.addEventListener('click',e=>{
  if(e.target.closest('.hamburger')){
    document.querySelector('.mobile-nav').classList.add('is-open');
    document.querySelector('.mobile-nav-overlay').classList.add('is-open');
  }
  if(e.target.closest('.mobile-nav-close')||e.target.closest('.mobile-nav-overlay')){
    document.querySelector('.mobile-nav').classList.remove('is-open');
    document.querySelector('.mobile-nav-overlay').classList.remove('is-open');
  }
});

// Header hide on scroll down, show on scroll up
let lastScroll=0;
const header=document.querySelector('.header');
window.addEventListener('scroll',()=>{
  const y=window.scrollY;
  header.style.transform=y>lastScroll&&y>100?'translateY(-100%)':'translateY(0)';
  lastScroll=y;
},{passive:true});

// Sidebar active link (service pages)
const sidebarLinks=document.querySelectorAll('.sidebar-nav a');
if(sidebarLinks.length){
  const sections=Array.from(sidebarLinks).map(a=>{
    const id=a.getAttribute('href')?.split('#')[1];
    return id?document.getElementById(id):null;
  }).filter(Boolean);
  const obs=new IntersectionObserver(entries=>{
    entries.forEach(e=>{
      if(e.isIntersecting){
        sidebarLinks.forEach(a=>a.classList.remove('is-active'));
        const link=document.querySelector(`.sidebar-nav a[href="#${e.target.id}"]`);
        if(link)link.classList.add('is-active');
      }
    });
  },{rootMargin:'-20% 0px -60% 0px'});
  sections.forEach(s=>obs.observe(s));
}
