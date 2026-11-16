"""Verify audit citations, coverage and source integrity, never execute a prediction."""
from pathlib import Path
import hashlib
import json
import re
import zipfile

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
evidence=read('证据摘录.json')
manifest=read('读取与保护清单.json')
report=OUT/'A01-U02旺衰语义边界核查报告.md'
text=report.read_text(encoding='utf-8')
errors=[]
checks={}

source_checks=[]
for m in manifest:
    p=ROOT/m['path'];ok=p.is_file() and sha(p)==m['sha256']
    source_checks.append(dict(path=m['path'],unchanged=ok,sha256=m['sha256']))
    if not ok:errors.append('source changed/missing: '+m['path'])
checks['protected_sources_unchanged']=dict(total=len(source_checks),passed=sum(x['unchanged'] for x in source_checks))
count=0
for e in evidence:
    p=ROOT/e['path'];lines=p.read_text(encoding='utf-8-sig').splitlines()
    for x in e['excerpts']:
        count+=1
        if '\n'.join(lines[x['start']-1:x['end']])!=x['text']:errors.append('excerpt mismatch '+e['id'])
checks['exact_excerpt_ranges']=dict(total=count,all_match=not any('excerpt mismatch' in s for s in errors))
links=re.findall(r'\]\(<(.+?):([0-9]+)>\)',text)
for target,line in links:
    p=Path(target)
    if not p.is_file():errors.append('broken link '+target)
    elif int(line)>len(p.read_text(encoding='utf-8-sig').splitlines()):errors.append('line outside '+target+':'+line)
checks['local_source_links']=dict(total=len(links),all_resolve=not any('link' in s or 'line outside' in s for s in errors))
chapters=re.findall(r'^## ([0-9]+)\. ',text,re.M)
checks['ten_required_chapters']=chapters==[str(i) for i in range(1,11)]
if not checks['ten_required_chapters']:errors.append('chapter coverage')
checks['nine_derivation_sections']=all(f'### D{i:02d} ' in text for i in range(1,10))
checks['source_questions_eight']=all(s in text for s in ['仕人与庶人有差异吗','乘将改变适用方式吗','旺鬼必然减害吗','有时间条件吗','鬼旺与日干受害关系','财旺身弱必不利吗','制化救能改结果吗','对象旺衰与事件发生同层吗'])
checks['six_numeric_topics']=all(s in text for s in ['55与62的零','旧quantity 4—6','旧harm/favorable','分数是否替代对象作用判断','数量旺衰倍率是否可能重复','without_void'])
for key in ['nine_derivation_sections','source_questions_eight','six_numeric_topics']:
    if not checks[key]:errors.append(key)
checks['complete_u02_embedded']={}
for e in evidence:
    if e['id'] in ['U55','U62']:
        x=e['excerpts'][0];line=x['text'].split('\n')[85-x['start']]
        checks['complete_u02_embedded'][e['id']]=f'> **L85** {line}' in text
        if not checks['complete_u02_embedded'][e['id']]:errors.append('U02 incomplete '+e['id'])
bindings=read('版本绑定核对.json')
checks['bindings']=dict(total=len(bindings),passed=sum(x['match'] for x in bindings))
if any(not x['match'] for x in bindings):errors.append('binding mismatch')
sp=[x for x in read('逐版比较与来源转录核对.json') if x.get('id','').startswith('SP')]
checks['sp_originals_verified']={x['id']:x['source_sha_matches'] and x['registered_quote_matches'] for x in sp}
if len(sp)!=3 or not all(checks['sp_originals_verified'].values()):errors.append('SP verification')
erecs=read('来源登记定位核对.json')['selected_records']
checks['e_originals_verified']={x['id']:x['audit_source_sha_matches'] and x['audit_quote_matches'] for x in erecs}
if not all(checks['e_originals_verified'].values()):errors.append('E verification')
checks['labels_present']=all(x in text for x in ['DIRECT','VERSION_DIFF','PROGRAM_INTERPRETATION','MODEL_INFERENCE','CONFLICT','PENDING'])
checks['not_approved_as_rule']='候选设计' in text and '未实施任何候选修订' in text
checks['no_case_paths_in_collected_sources']=not any(any(x in m['path'].split('/') for x in ['案例项目库','经验日志']) for m in manifest)
checks['no_runtime_prediction_test']='未读真实任务' in text and '无算法试验' in text
checks['template_resolved']=not re.search(r'\{ref\(|\{quote\(',text)
for k in ['labels_present','not_approved_as_rule','no_case_paths_in_collected_sources','template_resolved']:
    if not checks[k]:errors.append(k)
result=dict(schema='a01-u02-audit-verification-v1',scope='文件身份、引文、结构和链接核查；不验证术理、预测效果或模型实际执行',passed=not errors,checks=checks,errors=errors,source_integrity=source_checks,report_sha256=sha(report),source_writes='本轮工具写入仅限本审计目录；未执行正式规则或算法修改')
(OUT/'验收核对.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if errors:raise SystemExit(json.dumps(errors,ensure_ascii=False))

readme='''# A01 外审材料阅读入口

先读《A01-U02旺衰语义边界核查报告.md》，其中含用户要求的十章及两版U02全文。
第10章列11个待决问题，可逐项回执，不必重新定位文件。

连续原文在《原文证据附件.md》及《证据摘录.json》；所有行号均为UTF-8-SIG解码后Python splitlines()一基行号。
本包保留理论、作者讲解、版本规则、程序解释与审计推论的身份差别，不能将DIRECT当作专业正确性认证。

《读取与保护清单.json》记录文件路径、范围及哈希；《验收核对.json》记录最终核对。
《九项推导核查索引.json》只是审计索引，不是正式规则注册表。
《55-62只读差异.patch》是未应用的只读差异，不是执行指令。
《opencode-liuren-prompt-only.json》只含liuren描述和提示词，不含其他配置。

本包未包含案例库、经验库、历史预测作答或原书邻段的预测结果证据；书中理论段自带的假设和解释比喻原样保留。
本轮没有调用模型、调整算法、激活版本或修改正式规则，未选定55/62为正确答案。
collect_evidence.py / build_report.py / verify_report.py 仅为本目录的材料整理与核验脚本；无需运行脚本即可审阅本包。
'''
(OUT/'README-外审阅读入口.md').write_text(readme,encoding='utf-8')
files=[p for p in OUT.iterdir() if p.is_file() and p.suffix!='.zip' and p.name!='交付文件SHA256.json']
hashes=[dict(file=p.name,sha256=sha(p),bytes=p.stat().st_size) for p in sorted(files)]
(OUT/'交付文件SHA256.json').write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
archive=OUT/'A01-U02外审材料包.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for p in files+[OUT/'交付文件SHA256.json']:z.write(p,arcname=p.name)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(files)+1
print(json.dumps(dict(passed=True,source_integrity=checks['protected_sources_unchanged'],excerpts=count,links=len(links),bindings=checks['bindings'],zip=str(archive),zip_bytes=archive.stat().st_size),ensure_ascii=False))
