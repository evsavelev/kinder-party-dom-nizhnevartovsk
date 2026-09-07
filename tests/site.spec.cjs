const {test,expect}=require('@playwright/test');
test('Mobile: navigation, meaningful contact links, FAQ and lightbox keyboard',async({page})=>{
 await page.setViewportSize({width:390,height:844});await page.goto('/');
 const menu=page.locator('.menu-toggle');await menu.click();await expect(menu).toHaveAttribute('aria-expanded','true');await page.locator('#navigation a[href="#venue"]').click();await expect(menu).toHaveAttribute('aria-expanded','false');await expect(page).toHaveURL(/#venue$/);
 const photo=page.locator('#venue .photo-open').first();await photo.click();const dialog=page.locator('#lightbox');await expect(dialog).toBeVisible();await expect(page.locator('#lightbox-image')).toHaveJSProperty('complete',true);const before=await page.locator('#lightbox-image').getAttribute('src');await page.keyboard.press('ArrowRight');await expect(page.locator('#lightbox-image')).not.toHaveAttribute('src',before);await page.keyboard.press('ArrowLeft');await expect(page.locator('#lightbox-image')).toHaveAttribute('src',before);await page.keyboard.press('Escape');await expect(dialog).not.toBeVisible();await expect(photo).toBeFocused();
 const faq=page.locator('summary').first();await faq.click();await expect(faq.locator('..')).toHaveAttribute('open','');await faq.click();await expect(faq.locator('..')).not.toHaveAttribute('open','');
 const contactLinks=await page.locator('a[href*="wa.me"]').evaluateAll(links=>links.map(x=>x.href));expect(contactLinks.length).toBeGreaterThan(20);for(const href of contactLinks){const u=new URL(href);expect(u.pathname).toBe('/79825357237');expect(u.searchParams.get('text')).toContain('Здравствуйте');}
 const age=await page.locator('.age-links a').last().getAttribute('href');expect(new URL(age).searchParams.get('text')).toContain('10+');
 await expect(page.locator('.mobile-bar a[href="tel:+79825357237"]')).toBeVisible();
});
test('Static content works without JavaScript, schema and local assets resolve',async({browser,request,baseURL})=>{
 const c=await browser.newContext({javaScriptEnabled:false,viewport:{width:1440,height:900}});const p=await c.newPage();await p.goto(baseURL);await expect(p.locator('h1')).toHaveCount(1);await expect(p.locator('.program')).toHaveCount(7);await expect(p.locator('.review')).toHaveCount(4);await p.locator('summary').first().click();await expect(p.locator('details').first()).toHaveAttribute('open','');
 const graph=JSON.parse(await p.locator('script[type="application/ld+json"]').textContent())['@graph'];expect(graph[0].address.streetAddress).toBe('улица Чапаева, 36');expect(graph[0]).not.toHaveProperty('aggregateRating');expect(graph[1].mainEntity.length).toBe(await p.locator('details').count());
 for(const asset of ['assets/styles.css','assets/app.js','assets/favicon.svg','assets/favicon.png','assets/apple-touch-icon.png','assets/og-image.jpg','robots.txt','sitemap.xml']){const r=await request.get(new URL(asset,baseURL).href);expect(r.status(),asset).toBe(200);}
 const body=await p.locator('body').innerText();expect(body).not.toMatch(/Чапаева,? 34|Мира,? 5|Lorem ipsum|undefined|NaN/);await c.close();
});
test('Reduced motion and desktop lightbox focus stay usable',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});await page.goto('/');expect(await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior)).toBe('auto');await page.locator('#gallery .photo-open').first().click();await page.keyboard.press('Tab');expect(await page.evaluate(()=>document.querySelector('#lightbox').contains(document.activeElement))).toBe(true);await page.getByRole('button',{name:'Закрыть фото'}).click();await expect(page.locator('#lightbox')).not.toBeVisible();
});
