const {defineConfig}=require('@playwright/test');
module.exports=defineConfig({testDir:'./tests',use:{channel:'chrome',baseURL:process.env.QA_URL||'http://127.0.0.1:4174/',headless:true},reporter:'list',workers:1});
