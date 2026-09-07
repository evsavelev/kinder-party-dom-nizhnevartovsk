'use strict';
const menu=document.querySelector('.menu-toggle');
const nav=document.querySelector('#navigation');
function closeMenu(){menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Открыть меню');nav.classList.remove('open');}
menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?'Закрыть меню':'Открыть меню');nav.classList.toggle('open',open);});
nav.addEventListener('click',e=>{if(e.target.closest('a'))closeMenu();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.getAttribute('aria-expanded')==='true'){closeMenu();menu.focus();}});
document.addEventListener('click',e=>{if(!e.target.closest('.site-header'))closeMenu();});
const dialog=document.querySelector('#lightbox');
const pictures=[...document.querySelectorAll('.photo-open')];
let current=0,opener;
function showPhoto(index){current=(index+pictures.length)%pictures.length;const link=pictures[current];const image=document.querySelector('#lightbox-image');image.src=link.href;image.alt=link.dataset.caption;document.querySelector('#lightbox-caption').textContent=link.dataset.caption;document.querySelector('#photo-count').textContent=`${current+1} / ${pictures.length}`;}
pictures.forEach((link,index)=>link.addEventListener('click',event=>{if(event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;if(typeof dialog.showModal!=='function')return;event.preventDefault();opener=link;showPhoto(index);dialog.showModal();document.body.classList.add('modal-open');document.querySelector('.lightbox-close').focus();}));
document.querySelector('.lightbox-close').addEventListener('click',()=>dialog.close());
document.querySelector('.photo-prev').addEventListener('click',()=>showPhoto(current-1));
document.querySelector('.photo-next').addEventListener('click',()=>showPhoto(current+1));
dialog.addEventListener('keydown',event=>{if(event.key==='ArrowLeft'){event.preventDefault();showPhoto(current-1);}if(event.key==='ArrowRight'){event.preventDefault();showPhoto(current+1);}});
dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});
dialog.addEventListener('close',()=>{document.body.classList.remove('modal-open');opener?.focus();});
