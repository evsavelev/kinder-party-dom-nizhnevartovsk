const {chromium}=require('@playwright/test');const fs=require('node:fs');
(async()=>{const browser=await chromium.launch({channel:'chrome',headless:true});const context=await browser.newContext();
for(const id of [2201,2386,2366,2224,2094]){const p=await context.newPage();try{await p.goto(`https://vk.ru/wall-106473815_${id}`,{waitUntil:'domcontentloaded',timeout:30000});await p.waitForTimeout(2500);fs.writeFileSync(`.research/post-${id}.html`,await p.content());fs.writeFileSync(`.research/post-${id}.txt`,await p.locator('body').innerText());console.log(id,(await p.locator('body').innerText()).slice(0,150));}catch(e){console.log(id,e.message)}await p.close()}
await browser.close()})();
