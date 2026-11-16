"""Read-only source collection for A01; writes only beside this script.

No chart, prediction, model call, case/experience retrieval, or algorithm execution.
Line convention: UTF-8-SIG decode followed by Python str.splitlines(), 1-based.
"""
from pathlib import Path
import hashlib
import json
import difflib

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
V55 = 'runtime/liuren/20261114-tool-reliability-55'
V62 = 'runtime/liuren/20261115-class-selection-62'
OLD = 'output/liuren-class-selection-trial-56/before'
specs = []

def add(eid, rel, ranges=None, identity='项目工程文件'):
    specs.append(dict(id=eid, path=rel, ranges=ranges, identity=identity))

for v, root in [('55', V55), ('62', V62)]:
    add('U'+v, root+'/references/judgment-core.md', identity=v+'版本执行规则（非原书）')
    add('L'+v, root+'/methods/liqi.md', identity=v+'版本方法规则（非原书）')
    add('QS'+v, root+'/references/quantity-strength.md', identity=v+'版本数量接口规则')
    add('QC'+v, root+'/references/quantity-correction.md', identity=v+'版本数量修正规则')
    add('EN'+v, root+'/entry.md', identity=v+'版本入口')
    add('REG'+v, root+'/references/confirmed-policy-register.json', identity=v+'版本采用登记（非原始专业证据）')
    # Only SP03/04/05; other supplements and old results excluded.
    add('SUP'+v, root+'/references/confirmed-policy-supplements.md', [(59,107)], v+'版本来源转录，需与实际书文核对')

add('TR', V62+'/references/class-selection-trial.md', identity='62短答执行规则')
add('LF-SP03','书籍库/北海闲人/理法简易.txt',[(4901,4923)],'北海讲解与其中《壬归》引文，按段落分层')
add('LF-GHOST','书籍库/北海闲人/理法简易.txt',[(865,897)],'北海讲解与引文，凶化长生、制鬼时序')
add('LF-MARR','书籍库/北海闲人/理法简易.txt',[(4011,4019)],'北海婚姻段讲解，含宽泛表述')
add('LF-FARM','书籍库/北海闲人/理法简易.txt',[(4651,4665)],'北海农牧段讲解与引文；非现实反馈')
add('LF-TIGER','书籍库/北海闲人/理法简易.txt',[(6053,6061)],'北海讲解；排除前方书载占例结果')
add('BF-SP04','书籍库/北海闲人/毕法赋全解-正式整理本.md',[(1233,1245)],'第13法标题、引文与北海讲解；排除前后预测例')
add('BF-SP05','书籍库/北海闲人/毕法赋全解-正式整理本.md',[(1259,1275)],'第14法标题、引文与北海讲解；假设和解释非实证')
add('BF-TIGER','书籍库/北海闲人/毕法赋全解-正式整理本.md',[(606,618)],'催官使者/催官符的作者说明')
add('RG-SP03','书籍库/经典古籍/佚名/壬归.txt',[(759,769)],'本地《壬归》电子文本，出行理论段')
add('RG-RESCUE','书籍库/经典古籍/佚名/壬归.txt',[(138,146),(218,230)],'本地《壬归》电子文本，制救/初末顺序')
add('RG-GIVE','书籍库/经典古籍/佚名/壬归.txt',[(405,413)],'本地《壬归》电子文本，谋望与施受')
add('ZN-NOTE','书籍库/经典古籍/明代/六壬指南注解-明-陈公献.txt',[(973,990)],'本地注解版，注者身份未核，不把注语冒充原赋')
add('ZN-BASE','书籍库/经典古籍/明代/六壬指南-明-陈公献.txt',[(493,507),(643,645),(733,735)],'本地《指南》正文及本地所录注释；未核印本')
add('JZ-GHOST','书籍库/北海闲人/六壬金针_修正版.md',[(901,919)],'本地北海金针修正版，日鬼理论段')
add('JZ-SUIT','书籍库/北海闲人/六壬金针_修正版.md',[(2689,2695)],'本地北海金针修正版，讼占制化')

add('B55',OLD+'/tools/liuren-palace-strength.mjs',identity='55历史绑定工具（待哈希核对）')
add('E55',OLD+'/tools/liuren-strength-engine.mjs',[(1,44),(147,180),(268,325)],'55历史绑定研究引擎')
add('P55',OLD+'/tools/liuren-strength-profile.json',[(1,28),(80,107)],'55历史绑定工程系数')
add('N55',OLD+'/tools/liuren-local-strength.mjs',[(1,17),(60,84)],'55历史绑定局部计算')
add('R55',OLD+'/tools/liuren-strength-rules.mjs',[(1,30),(60,71)],'55历史绑定工具函数')
add('I62','tools/liuren-strength-interpretation.mjs',identity='62当前新旺衰语义显示/解释')
add('T62','tools/liuren-trial-decision.mjs',identity='62当前短答倾向包装（程序解释）')
add('B62','tools/liuren-palace-strength.mjs',identity='62当前普通strength接口')
add('C62','tools/liuren-chart-view.mjs',identity='62当前普通/研究AI盘输出')
add('E62','tools/liuren-strength-engine.mjs',[(1,44),(147,180),(268,325)],'62当前研究引擎')
add('P62','tools/liuren-strength-profile.json',[(1,28),(80,107)],'62当前工程系数')
add('N62','tools/liuren-local-strength.mjs',[(1,17),(60,84)],'62当前局部计算')
add('R62','tools/liuren-strength-rules.mjs',[(1,30),(60,71)],'62当前工具函数')
add('RESEARCH','tools/liuren-strength.mjs',identity='显式研究CLI（不运行）')
add('QA62','tools/liuren-quantity-adjustment.mjs',identity='当前数量回执/倍数接口（不运行）')
add('QA55',OLD+'/tools/liuren-quantity-adjustment.mjs',identity='55数量回执/倍数接口（不运行）')
add('IO','tools/liuren-deterministic-io.mjs',[(67,104)],'当前确定性分派层')
add('HANDOFF','tools/liuren-core-handoff.mjs',[(30,75)],'当前裁决核心装配与字段投影')
add('CODEX','tools/liuren-codex.mjs',[(137,162)],'当前Codex读取/计算分派')
add('PLUGIN','.opencode/plugins/liuren-adjudication.ts',[(164,180),(271,317)],'当前OpenCode工具说明/短答包装分派')
add('OSKILL','.opencode/skills/liuren/daliuren/SKILL.md',identity='当前OpenCode入口规则')
add('CSKILL','integrations/codex/daliuren-codex/SKILL.md',identity='当前项目Codex入口规则')
add('DOC35','docs/确定性工具使用说明-35.md',identity='工具文档（工程解释）')
add('READ','README.md',identity='当前路由说明，非理论依据')
add('INDEX','目录总索引.md',identity='当前目录路由，非理论依据')
add('TASK','output/liuren-architecture-phase1-20261116/06-未解冲突与外审决策清单.md',[(1,12)],'前阶段A01任务定位，不作原书证据')
add('KN-README','docs/六壬知识整理-20261102/README.md',identity='知识维护边界')
add('KN-DATA','docs/六壬知识整理-20261102/数据约定.md',identity='来源身份与数据边界')

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_json(name,v): (OUT/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def collect():
    evidence=[]; manifest={}; missing=[]
    for s in specs:
        p=ROOT/s['path']
        if not p.is_file(): missing.append(s);continue
        raw=p.read_bytes(); lines=raw.decode('utf-8-sig').splitlines()
        ranges=s['ranges'] or [(1,len(lines))]
        m=manifest.setdefault(s['path'],dict(path=s['path'],absolute_path=str(p.resolve()),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),lines=len(lines),read_ranges=[],evidence_ids=[],read_mode='定向范围/全文见read_ranges；整文件哈希不代表全文语义精读'))
        m['read_ranges']+=ranges;m['evidence_ids'].append(s['id'])
        excerpts=[]
        for a,b in ranges:
            if not(1<=a<=b<=len(lines)):raise ValueError((s['id'],a,b,len(lines)))
            excerpts.append(dict(start=a,end=b,text='\n'.join(lines[a-1:b])))
        evidence.append(dict(id=s['id'],path=s['path'],identity=s['identity'],sha256=m['sha256'],line_convention='utf-8-sig + str.splitlines(), 1-based',excerpts=excerpts))
    # Config: hash full file, export only liuren prompt and description lines.
    cfg=ROOT/'opencode.json'; lines=cfg.read_text(encoding='utf-8-sig').splitlines(); obj=json.loads(cfg.read_text(encoding='utf-8-sig'))
    agent=obj['agent']['liuren']; selected=[]
    for field in ['description','prompt']:
        value=agent.get(field)
        if value is None:continue
        hits=[i+1 for i,l in enumerate(lines) if ('"'+field+'"') in l and json.dumps(value,ensure_ascii=False) in l]
        selected.append(dict(field=field,lines=hits,value=value))
    write_json('opencode-liuren-prompt-only.json',dict(path='opencode.json',sha256=digest(cfg),selected=selected,excluded='其余配置不复制、不输出'))
    manifest['opencode.json']=dict(path='opencode.json',absolute_path=str(cfg.resolve()),sha256=digest(cfg),bytes=cfg.stat().st_size,lines=len(lines),read_mode='仅agent.liuren.description/prompt字段；其他字段不作证据',read_ranges=[(n,n) for s in selected for n in s['lines']],evidence_ids=['PROMPT'])
    # Bindings: compare actual bytes, no use of earlier audit verdicts.
    bindings=[]
    for version, pointerPath,base,runtime in [('55',OLD+'/.opencode/liuren-active.json',OLD,V55),('62','.opencode/liuren-active.json','',V62)]:
        pp=ROOT/pointerPath; ptr=json.loads(pp.read_text(encoding='utf-8-sig'))
        manifest[pointerPath]=dict(path=pointerPath,absolute_path=str(pp.resolve()),sha256=digest(pp),read_mode='结构读取release/runtime/workflowImplementation/strengthInterpretation；不作理论来源')
        for rel in ['tools/liuren-palace-strength.mjs','tools/liuren-strength-engine.mjs','tools/liuren-strength-rules.mjs','tools/liuren-strength-profile.json','tools/liuren-local-strength.mjs','tools/liuren-local-strength-profile.json','tools/liuren-quantity-adjustment.mjs','tools/liuren-chart-view.mjs']:
            target=ROOT/base/rel if base else ROOT/rel
            expected=ptr['workflowImplementation'].get(rel)
            actual=digest(target) if target.is_file() else None
            bindings.append(dict(version=version,kind='tool',pointer=pointerPath,declared_release=ptr['release'],logical_path=rel,actual_path=str(target.relative_to(ROOT)).replace('\\','/'),expected_sha256=expected,actual_sha256=actual,match=actual==expected))
            if str(target.relative_to(ROOT)).replace('\\','/') not in manifest and target.is_file():
                relp=str(target.relative_to(ROOT)).replace('\\','/');manifest[relp]=dict(path=relp,absolute_path=str(target.resolve()),sha256=actual,read_mode='仅字节哈希/绑定核对；未据此称为正文精读')
        mp=ROOT/runtime/'manifest.json'; md=json.loads(mp.read_text(encoding='utf-8-sig'))
        manifest[runtime+'/manifest.json']=dict(path=runtime+'/manifest.json',absolute_path=str(mp.resolve()),sha256=digest(mp),read_mode='只读取已引用文件哈希声明')
        runtimefiles=[x['path'] for x in specs if x['path'].startswith(runtime+'/')]
        for pth in runtimefiles:
            local=pth[len(runtime)+1:];p=ROOT/pth
            bindings.append(dict(version=version,kind='runtime',pointer=runtime+'/manifest.json',logical_path=local,actual_path=pth,expected_sha256=md['files'].get(local),actual_sha256=digest(p),match=md['files'].get(local)==digest(p)))
    write_json('版本绑定核对.json',bindings)
    # Read only the book-evidence records relevant to this semantic audit.
    records=[]
    def walk(v):
        if isinstance(v,dict):
            if v.get('id') in ['E09','E10','E14','E15','E20','E21','E22']:
                records.append(v)
            else:
                for x in v.values(): walk(x)
        elif isinstance(v,list):
            for x in v:walk(x)
    rel=V62+'/references/adjudicator-book-evidence.json'; pp=ROOT/rel
    walk(json.loads(pp.read_text(encoding='utf-8-sig')))
    for rec in records:
        src=ROOT/rec['path'];ls=src.read_text(encoding='utf-8-sig').splitlines()
        rec['audit_source_sha_matches']=digest(src)==rec['sha256']
        rec['audit_quote_matches']='\n'.join(ls[rec['line_start']-1:rec['line_end']])==rec['quote']
    write_json('来源登记定位核对.json',dict(path=rel,sha256=digest(pp),selected_records=records,notice='登记仅作定位；专业证据以实际原书摘录为准，E20等编号仅在此文件命名空间有效'))
    manifest[rel]=dict(path=rel,absolute_path=str(pp.resolve()),sha256=digest(pp),read_mode='只选E09/E10/E14/E15/E20/E21/E22；不遍读其他记录')
    write_json('证据摘录.json',evidence)
    write_json('读取与保护清单.json',list(manifest.values()))
    write_json('未找到的指定文件.json',missing)
    chunks=['# A01 原文证据附件','', '本附件为实际来源的定向转录。行号统一为 UTF-8-SIG 解码后 Python splitlines() 一基行号；原件换行字节可能不同。保留疑字/OCR，不自动校正。整文件 SHA256 仅证明字节身份，不证明专业正确或全文精读。', '', '来源身份、节选边界与哈希详见各条。书例结果不用于规则效果验证。', '']
    for e in evidence:
        chunks += [f"## {e['id']}｜{e['identity']}",'',f"路径：`{e['path']}`",'',f"SHA256：`{e['sha256']}`",'']
        for x in e['excerpts']:
            chunks += [f"L{x['start']}—L{x['end']}：",'','```text']
            chunks += [f'{i}: {l}' for i,l in enumerate(x['text'].split('\n'),x['start'])]
            chunks += ['```','']
    (OUT/'原文证据附件.md').write_text('\n'.join(chunks),encoding='utf-8')
    # Actual version comparisons. Report differences, never apply any patch.
    diffs=[]; compare=[]
    for rel in ['references/judgment-core.md','methods/liqi.md','references/quantity-strength.md','references/quantity-correction.md','references/confirmed-policy-supplements.md','references/confirmed-policy-evidence.json']:
        a=ROOT/V55/rel;b=ROOT/V62/rel;sa=a.read_text(encoding='utf-8-sig');sb=b.read_text(encoding='utf-8-sig')
        compare.append(dict(path=rel,sha55=digest(a),sha62=digest(b),bytes_equal=a.read_bytes()==b.read_bytes(),text_equal=sa==sb))
        diffs+=list(difflib.unified_diff(sa.splitlines(True),sb.splitlines(True),fromfile=V55+'/'+rel,tofile=V62+'/'+rel))
        if rel.endswith('confirmed-policy-evidence.json'):
            # Verify registered SP quotes against books rather than trust quote summaries.
            for record in json.loads(sb)['evidence']:
                if record['id'] not in ['SP03','SP04','SP05']:continue
                p=ROOT/record['path'];ls=p.read_text(encoding='utf-8-sig').splitlines();q='\n'.join(ls[record['line_start']-1:record['line_end']])
                compare.append(dict(id=record['id'],path=record['path'],registered_start=record['line_start'],registered_end=record['line_end'],source_sha_matches=digest(p)==record['sha256'],registered_quote_matches=q==record['quote']))
            for root in [V55,V62]:
                p=ROOT/root/rel;manifest[root+'/'+rel]=dict(path=root+'/'+rel,absolute_path=str(p.resolve()),sha256=digest(p),read_mode='仅读取SP03/04/05条目、并做字节版本比较')
    write_json('逐版比较与来源转录核对.json',compare)
    (OUT/'55-62只读差异.patch').write_text(''.join(diffs),encoding='utf-8')
    # Include source-evidence metadata in baseline (save after comparisons).
    write_json('读取与保护清单.json',list(manifest.values()))
    print(json.dumps(dict(evidence_records=len(evidence),protected_sources=len(manifest),missing=len(missing),binding_total=len(bindings),binding_passed=sum(x['match'] for x in bindings),out=str(OUT)),ensure_ascii=False))

if __name__=='__main__': collect()
