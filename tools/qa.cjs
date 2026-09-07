const {chromium}=require('@playwright/test');
const fs=require('node:fs');
const url=process.env.QA_URL||'http://127.0.0.1:4174/';
(async()=>{
fs.mkdirSync('.research/qa',{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true});
const reports=[];
for(const width of [360,375,390,430,768,1366,1440,1920]){
const p=await browser.newPage({viewport:{width,height:900},deviceScaleFactor:1});const errors=[];const failed=[];
p.on('pageerror',e=>errors.push(e.message));p.on('console',m=>{if(m.type()==='error')errors.push(m.text())});p.on('response',r=>{if(r.status()>=400)failed.push([r.status(),r.url()])});
const res=await p.goto(url,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.addStyleTag({content:'html{scroll-behavior:auto!important}'});
for(let top=0;top<await p.evaluate(()=>document.body.scrollHeight);top+=800){await p.evaluate(y=>window.scrollTo(0,y),top);await p.waitForTimeout(60)}
await p.waitForTimeout(300);await p.evaluate(()=>window.scrollTo(0,0));
await p.screenshot({path:`.research/qa/${width}-hero.png`});
if([390,1440].includes(width))await p.screenshot({path:`.research/qa/${width}-full.png`,fullPage:true});
const dom=await p.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,scrollWidth:document.documentElement.scrollWidth,height:document.body.scrollHeight,h1:document.querySelectorAll('h1').length,broken:[...document.images].filter(i=>i.id!=='lightbox-image'&&(!i.complete||i.naturalWidth===0)).map(i=>i.src),anchors:[...document.querySelectorAll('a[href^="#"]')].filter(a=>a.hash&&!document.getElementById(a.hash.slice(1))).map(a=>a.hash),smallTargets:[...document.querySelectorAll('a,button,summary')].filter(el=>{const r=el.getBoundingClientRect();return r.width>0&&r.height>0&&(r.height<24||r.width<24)}).map(x=>({text:x.textContent.trim().slice(0,30),rect:x.getBoundingClientRect().toJSON()}))}));
reports.push({width,status:res.status(),errors,failed,...dom});await p.close();
}
await browser.close();fs.writeFileSync('.research/qa/report.json',JSON.stringify(reports,null,2));console.log(JSON.stringify(reports,null,2));
if(reports.some(r=>r.status!==200||r.overflow||r.errors.length||r.failed.length||r.broken.length||r.anchors.length||r.h1!==1))process.exitCode=1;
})();
