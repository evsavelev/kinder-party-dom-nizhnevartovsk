"""Scoped GitHub API helper. Credential captured in memory, never logged."""
import subprocess,sys,json,requests
sys.stdout.reconfigure(encoding='utf-8')
repo='evsavelev/kinder-party-dom-nizhnevartovsk'
p=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',capture_output=True,text=True,check=True)
credential=dict(line.split('=',1) for line in p.stdout.splitlines() if '=' in line)
s=requests.Session();s.headers.update({'Authorization':'Bearer '+credential['password'],'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'})
def api(method,endpoint,payload=None):
    r=s.request(method,'https://api.github.com'+endpoint,json=payload,timeout=30)
    if r.status_code>=400 and r.status_code!=404:
        print('GitHub API:',r.status_code,r.json().get('message',''));sys.exit(1)
    return r
command=sys.argv[1]
if command=='inspect':
    r=api('GET','/repos/'+repo);print('Repository status:',r.status_code)
    if r.status_code==200:print(json.dumps({k:r.json().get(k) for k in ['html_url','default_branch','pushed_at','size']},ensure_ascii=False))
elif command=='create':
    r=api('GET','/repos/'+repo)
    if r.status_code==404:r=api('POST','/user/repos',{'name':repo.split('/')[1],'private':False,'description':'Киндер Пати Дом — детские праздники в Нижневартовске. Коммерческий демонстрационный сайт.','homepage':'https://evsavelev.github.io/kinder-party-dom-nizhnevartovsk/','auto_init':False})
    print('Repository:',r.status_code,r.json().get('html_url'))
elif command=='pages':
    r=api('GET','/repos/'+repo+'/pages')
    if r.status_code==404:r=api('POST','/repos/'+repo+'/pages',{'build_type':'workflow'})
    print('Pages:',r.status_code,r.json().get('html_url'))
elif command=='runs':
    r=api('GET','/repos/'+repo+'/actions/runs?per_page=3')
    print(json.dumps([{k:run.get(k) for k in ['id','head_sha','status','conclusion','html_url']} for run in r.json().get('workflow_runs',[])],indent=2))
elif command=='jobs':
    r=api('GET','/repos/'+repo+'/actions/runs/'+sys.argv[2]+'/jobs');print(json.dumps(r.json(),ensure_ascii=False)[:18000])
else:raise SystemExit('Unknown operation')
