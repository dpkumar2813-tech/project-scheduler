from datetime import date, timedelta

def schedule(tasks, start_date, holidays=()):
    nodes = {t['id']: dict(t) for t in tasks}
    if len(nodes) != len(tasks): raise ValueError('Task IDs must be unique')
    order, visiting, done = [], [], set()
    def visit(key):
        if key not in nodes: raise ValueError(f'Unknown dependency: {key}')
        if key in visiting: raise ValueError('Circular dependency: ' + ' → '.join(visiting[visiting.index(key):] + [key]))
        if key in done: return
        visiting.append(key)
        t = nodes[key]
        if not isinstance(t['duration'], int) or t['duration'] < 1: raise ValueError('Duration must be a positive integer')
        for dep in t.get('dependencies', []): visit(dep)
        visiting.pop(); done.add(key); order.append(key)
    for key in nodes: visit(key)
    successors = {key: [] for key in nodes}
    for key in order:
        t = nodes[key]
        t['es'] = max((nodes[d]['ef'] for d in t.get('dependencies', [])), default=0)
        t['ef'] = t['es'] + t['duration']
        for d in t.get('dependencies', []): successors[d].append(key)
    total = max((t['ef'] for t in nodes.values()), default=0)
    for key in reversed(order):
        t = nodes[key]
        t['lf'] = min((nodes[s]['ls'] for s in successors[key]), default=total)
        t['ls'] = t['lf'] - t['duration']; t['slack'] = t['ls'] - t['es']; t['critical'] = t['slack'] == 0
    day = date.fromisoformat(start_date); dates = []; excluded = set(holidays)
    while len(dates) < max(total, 1):
        if day.weekday() < 5 and day.isoformat() not in excluded: dates.append(day.isoformat())
        day += timedelta(days=1)
    for t in nodes.values():
        t['start'] = dates[t['es']]; t['end'] = dates[t['ef'] - 1]
    return {'tasks': [nodes[k] for k in order], 'days': dates[:total], 'duration': total, 'finish': dates[total - 1] if total else None}
