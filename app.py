from pathlib import Path
from uuid import uuid4
import json, os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from alex_design_studio_os.registry import create_all_agents
from alex_design_studio_os.campaign_workflow import run_advertising_campaign

BASE = Path(__file__).resolve().parent
OUT = Path(os.getenv('ALEX_OUTPUT_DIR', str(BASE / 'outputs')))
OUT.mkdir(parents=True, exist_ok=True)
app = FastAPI(title='ALEX DESIGN STUDIO OS', version='1.0.0', description='64-role creative campaign orchestration demo')

class CampaignRequest(BaseModel):
    brief: str = Field(min_length=3, max_length=4000)
    offer_price: str = Field(default='₹149', max_length=40)
    regular_price: str = Field(default='₹220', max_length=40)

@app.get('/health')
def health():
    return {'status':'ok','app':'ALEX DESIGN STUDIO OS','version':'1.0.0','registered_roles':len(create_all_agents()),'execution_mode':'local-template-orchestration','live_llm_calls':0}

@app.get('/api/agents')
def agents():
    registry = create_all_agents()
    rows=[]
    for key, agent in registry.items():
        rows.append({'key':key,'name':getattr(agent,'name',key),'class':agent.__class__.__name__,'mode':'LOCAL_TEMPLATE'})
    return {'count':len(rows),'agents':rows}

@app.post('/api/campaign')
def campaign(req: CampaignRequest):
    try:
        result = run_advertising_campaign(req.brief, offer_price=req.offer_price, regular_price=req.regular_price, output_dir=str(OUT))
        campaign = result['campaign']
        cid = uuid4().hex[:12]
        # Save stable API-friendly artifacts with unique names.
        json_path = OUT / f'{cid}.json'
        md_path = OUT / f'{cid}.md'
        json_path.write_text(json.dumps(campaign, ensure_ascii=False, indent=2), encoding='utf-8')
        md_path.write_text(Path(result['markdown_path']).read_text(encoding='utf-8'), encoding='utf-8')
        return {'job_id':cid,'status':'SUCCEEDED' if campaign['execution']['all_roles_completed'] else 'PARTIAL','mode':campaign['execution']['mode'],'registered_agents':campaign['execution']['registered_agent_roles'],'completed_agents':campaign['execution']['agent_roles_completed'],'failed_agents':campaign['execution']['agent_roles_failed'],'live_llm_calls':campaign['execution']['separate_llm_calls'],'campaign':campaign,'downloads':{'json':f'/api/jobs/{cid}/json','markdown':f'/api/jobs/{cid}/markdown'}}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Campaign execution failed: {type(e).__name__}: {e}')

@app.get('/api/jobs/{job_id}/json')
def get_json(job_id: str):
    p=OUT/f'{job_id}.json'
    if not p.exists(): raise HTTPException(404,'Job not found on this instance')
    return JSONResponse(json.loads(p.read_text(encoding='utf-8')), headers={'Content-Disposition':f'attachment; filename="alex-campaign-{job_id}.json"'})

@app.get('/api/jobs/{job_id}/markdown')
def get_markdown(job_id: str):
    p=OUT/f'{job_id}.md'
    if not p.exists(): raise HTTPException(404,'Job not found on this instance')
    return PlainTextResponse(p.read_text(encoding='utf-8'), media_type='text/markdown; charset=utf-8', headers={'Content-Disposition':f'attachment; filename="alex-campaign-{job_id}.md"'})

@app.get('/', response_class=HTMLResponse)
def home():
    return (BASE/'static'/'index.html').read_text(encoding='utf-8')
