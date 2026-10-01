"""Compare immutable Git commits; report attribution changes without certifying readings."""
import argparse, hashlib, json, pathlib, subprocess
R = pathlib.Path(__file__).resolve().parents[1]

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])

def commit(root, ref):
    if ref.startswith('-'):
        raise ValueError('revision cannot begin with an option')
    return git(root, 'rev-parse', '--verify', ref + '^{commit}').decode().strip()

def inventory(root, sha):
    rows = {}
    for entry in git(root, 'ls-tree', '-r', '-z', sha).split(b'\0'):
        if not entry:
            continue
        meta, path = entry.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        rows[path.decode()] = (mode, kind, oid)
    return rows

def content(root, item):
    if item is None or item[1] != 'blob':
        return None
    return git(root, 'cat-file', 'blob', item[2])

def strict_equal(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, list):
        return len(a) == len(b) and all(strict_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(strict_equal(a[k], b[k]) for k in a)
    return a == b

def parse_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate JSON key')
            result[key] = value
        return result
    def constant(value):
        raise ValueError('nonfinite JSON number: ' + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)

def semantic(before, after, pointer=''):
    # JSON Pointer escaping keeps keys containing slash or tilde unambiguous.
    if type(before) is not type(after):
        return [{'pointer': pointer, 'operation': 'replace', 'before': before, 'after': after}]
    if isinstance(before, dict):
        out = []
        for key in sorted(before.keys() | after.keys()):
            p = pointer + '/' + key.replace('~', '~0').replace('/', '~1')
            if key not in before:
                out.append({'pointer': p, 'operation': 'add', 'after': after[key]})
            elif key not in after:
                out.append({'pointer': p, 'operation': 'remove', 'before': before[key]})
            else:
                out.extend(semantic(before[key], after[key], p))
        return out
    if isinstance(before, list):
        # Never infer stable identities or align scientific records by position.
        return [] if strict_equal(before, after) else [{'pointer': pointer, 'operation': 'replace_array', 'before': before, 'after': after}]
    return [] if before == after else [{'pointer': pointer, 'operation': 'replace', 'before': before, 'after': after}]

def category(path):
    if path.startswith(('corpus/', 'data/', 'sources/', 'reviews/')):
        return 'corpus_source_or_review'
    if path.startswith(('analysis/', 'research/')):
        return 'analysis_or_gate_record'
    if path.startswith(('scripts/', '.github/', 'workbench/')):
        return 'engineering'
    return 'documentation_or_metadata'

def calculate(root, baseline, target):
    old, new = commit(root, baseline), commit(root, target)
    a, b = inventory(root, old), inventory(root, new)
    changes = []
    for path in sorted(a.keys() | b.keys()):
        if a.get(path) == b.get(path):
            continue
        before, after = content(root, a.get(path)), content(root, b.get(path))
        row = {'path': path, 'category': category(path), 'operation': 'add' if path not in a else 'remove' if path not in b else 'modify',
               'before_git_entry': a.get(path), 'after_git_entry': b.get(path),
               'before_sha256': hashlib.sha256(before).hexdigest() if before is not None else None,
               'after_sha256': hashlib.sha256(after).hexdigest() if after is not None else None,
               'json_comparison': 'not_applicable', 'json_changes': []}
        if path.endswith('.json') and before is not None and after is not None:
            try:
                row['json_changes'] = semantic(parse_json(before), parse_json(after))
                row['json_comparison'] = 'compared'
            except (ValueError, UnicodeError):
                row['json_comparison'] = 'invalid_json'
        changes.append(row)
    return {'format': 'release-change-ledger-v1', 'baseline_commit': old, 'target_commit': new,
            'baseline_files': len(a), 'target_files': len(b), 'changed_files': len(changes), 'changes': changes,
            'boundary': 'Path categories are navigation aids, not scientific judgments. Every tracked Git entry is compared, including modes and submodules. Arrays are reported whole without guessed record alignment. No reading, source permission, gate or expert review is accepted by this report.'}

def markdown(report):
    lines = ['# Release change ledger', '', 'Baseline: `' + report['baseline_commit'] + '`', 'Target: `' + report['target_commit'] + '`', '', report['boundary'], '', '| Path | Change | Category | JSON changes |', '|---|---|---|---|']
    for row in report['changes']:
        path = row['path'].replace('|', '&#124;').replace('\n', ' ').replace('`', '&#96;')
        lines.append('| `' + path + '` | ' + row['operation'] + ' | ' + row['category'] + ' | ' + str(len(row['json_changes'])) + ' (' + row['json_comparison'] + ') |')
    return '\n'.join(lines) + '\n'

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--baseline', required=True)
    p.add_argument('--target', default='HEAD')
    p.add_argument('--output', type=pathlib.Path, required=True, help='JSON report path; Markdown is written alongside it')
    args = p.parse_args()
    report = calculate(R, args.baseline, args.target)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    args.output.with_suffix('.md').write_text(markdown(report))
    print(str(report['changed_files']) + ' changed tracked files; immutable endpoints recorded')
