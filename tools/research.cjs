const { chromium } = require('@playwright/test');
const fs = require('node:fs');
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 for(const [name,url] of [['vk','https://vk.ru/kinderparty_nv'],['2gis','https://2gis.ru/nizhnevartovsk/firm/70000001047353725/tab/photos']]){
 const page=await context.newPage();
 try{await page.goto(url,{waitUntil:'domcontentloaded',timeout:45000}); await page.waitForTimeout(5000); fs.writeFileSync(`.research/${name}-browser.html`,await page.content()); fs.writeFileSync(`.research/${name}-browser.txt`,await page.locator('body').innerText()); await page.screenshot({path:`.research/${name}.png`}); console.log(name,page.url(),(await page.locator('body').innerText()).slice(0,1200));}catch(e){console.log(name,e.message)}
 await page.close();
 }
 await browser.close();
})();
