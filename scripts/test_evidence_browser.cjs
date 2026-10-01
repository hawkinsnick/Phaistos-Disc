const {chromium}=require('playwright'),path=require('node:path'),fs=require('node:fs'),{pathToFileURL}=require('node:url');
(async()=>{
 const root=path.resolve(__dirname,'..'),out=path.join(root,'output/evidence-browser');fs.mkdirSync(out,{recursive:true});
 const browser=await chromium.launch({headless:true,channel:'chrome',args:['--no-sandbox']}),page=await browser.newPage({viewport:{width:1280,height:950}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(path.join(root,'workbench/evidence.html')).href);
 const count=await page.locator('#evidence-rows tr').count();if(count<1)throw Error('empty evidence');
 await page.fill('#find-evidence','no such evidence zzz');if(await page.locator('#evidence-rows tr').count()!==0)throw Error('filter');await page.fill('#find-evidence','');
 await page.selectOption('#category','research');if(!(await page.locator('#evidence-rows tr').count()>0))throw Error('category');await page.selectOption('#category','');
 async function exported(button){const promise=page.waitForEvent('download');await page.click(button);const dl=await promise;return JSON.parse(fs.readFileSync(await dl.path(),'utf8'));}
 async function cell(key,column){return page.locator('#scenario-metrics tr[data-metric="'+key+'"] td').nth(column).textContent();}
 if(await page.locator('#edition').isVisible()){
  if(await page.locator('#occurrence-rows tr').count()!==242)throw Error('slot coverage');await page.fill('#find-occurrence','A24');if(await page.locator('#occurrence-rows tr').count()!==5)throw Error('group filter');
  if(await cell('identified',1)!=='241'||await cell('unknown',1)!=='1'||await cell('identical_complete_group_pairs',1)!=='9')throw Error('native descriptive measures');
  await page.selectOption('#unknown','20');await page.selectOption('#b3','25');const s=JSON.parse(await page.locator('#scenario').textContent());
  if(s.all_slots.identified!==242||s.frequency_delta['PD-U101E3']!==1||s.frequency_delta['PD-U101E8']!==1)throw Error('hypothesis deltas');
  if(await cell('identified',2)!=='+1'||await cell('unknown',2)!=='-1')throw Error('table deltas');
  await page.click('#pin-scenario');if(await cell('identified',2)!=='0')throw Error('pin comparison');await page.selectOption('#unknown','');if(await cell('identified',2)!=='-1')throw Error('comparison remains pinned');
  await page.click('#reset-scenario');if(await cell('identified',2)!=='0')throw Error('reset native comparison');
  await page.selectOption('#unknown','20');await page.selectOption('#group-order','1');await page.selectOption('#slot-order','1');
  if(JSON.parse(await page.locator('#scenario').textContent()).graphical_groups.identical_complete_group_pairs!==9)throw Error('reversal');
  const selected=await exported('#export-scenario');if(selected.selected_scenario.scenario_id!=='u20-b25-g1-s1'||selected.comparison_scenario_id!=='uunknown-b7-g0-s0'||selected.native_changes_applied!==false||selected.expert_review_completed!==false||!/^[0-9a-f]{64}$/.test(selected.edition_workbench_sha256))throw Error('scenario provenance or scope');
  const editionBytes=fs.readFileSync(path.join(root,'analysis/edition-workbench-v1.json')),sha=require('node:crypto').createHash('sha256').update(editionBytes).digest('hex');if(selected.edition_workbench_sha256!==sha)throw Error('scenario edition hash');
  // Exercise every declared hypothesis through the actual controls and visible table.
  const scenarios=json=>JSON.parse(json).scenarios;
  const rows=scenarios(editionBytes.toString('utf8'));
  const results=await page.evaluate(rows=>{let checked=0;for(const r of rows){for(const [id,value] of [['unknown',r.unknown_sign_number===null?'':String(r.unknown_sign_number)],['b3',String(r.b3_sign_number)],['group-order',r.reverse_group_order?'1':'0'],['slot-order',r.reverse_within_group?'1':'0']]){const e=document.getElementById(id);e.value=value;e.dispatchEvent(new Event('change'));}const shown=JSON.parse(document.getElementById('scenario').textContent);if(shown.scenario_id!==r.scenario_id)throw Error('scenario selection coverage');const cells=document.querySelector('#scenario-metrics tr[data-metric="identified"]').querySelectorAll('td');if(cells[1].textContent!==String(r.all_slots.identified))throw Error('visible selected measure');checked++;}return checked;},rows);
  if(results!==368)throw Error('scenario enumeration');
  await page.selectOption('#unknown','20');await page.selectOption('#b3','25');await page.selectOption('#group-order','1');await page.selectOption('#slot-order','1');
 }
 await page.fill('#note-locus','source-inspection-fixture');await page.fill('#note-text','<script>Synthetic unverified note</script>');
 const n=await exported('#export-note');if(n.expert_review_completed!==false||n.native_changes_applied!==false||!/^[0-9a-f]{64}$/.test(n.evidence_index_sha256))throw Error('note promotion or missing pin');
 await page.click('#add-note');await page.click('#add-note');if(await page.locator('#note-collection li').count()!==1)throw Error('duplicate collection note');
 const collection=await exported('#export-notes');if(collection.notes.length!==1||collection.notes[0].note!==n.note)throw Error('collection export');
 async function imported(v){await page.setInputFiles('#import-notes',{name:'synthetic-collection.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(v))});await page.waitForFunction(()=>document.getElementById('import-notes').value==='');}
 for(const bad of [{...collection,project:'wrong-project'},{...collection,evidence_index_sha256:'0'.repeat(64)},{...collection,expert_review_completed:true},{...collection,notes:[{locus:'x',note:'x'.repeat(4001)}]}]){
  await imported(bad);if(await page.locator('#note-collection li').count()!==1||!(await page.locator('#collection-status').textContent()).includes('rejected'))throw Error('collection atomic rejection');
 }
 await imported({...collection,notes:[...collection.notes,{locus:'second-source-fixture',note:'Imported observation remains unverified.'}]});
 if(await page.locator('#note-collection li').count()!==2)throw Error('valid matching import');
 const merged=await exported('#export-notes');if(merged.notes.length!==2||merged.expert_review_completed!==false||merged.native_changes_applied!==false)throw Error('import promotion');
 if(await page.locator('#note-collection script').count()!==0||!(await page.locator('#note-collection').textContent()).includes('<script>'))throw Error('unsafe note rendering');
 await page.screenshot({path:path.join(out,'evidence-desktop.png'),fullPage:true});await page.setViewportSize({width:390,height:844});await page.screenshot({path:path.join(out,'evidence-mobile.png'),fullPage:true});
 if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('mobile overflow');if(errors.length)throw Error(errors.join(';'));
 await browser.close();console.log(JSON.stringify({status:'PASS',evidence_files:count,desktop:true,mobile:true,note_unverified:true,collection_atomic_rejection:true,disc_scenarios:await fs.existsSync(path.join(root,'analysis/edition-workbench-v1.json'))?368:null}));
})().catch(e=>{console.error(e);process.exit(1)});
