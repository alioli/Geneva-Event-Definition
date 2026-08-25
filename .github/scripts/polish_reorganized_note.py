from pathlib import Path

p = Path('main.tex')
t = p.read_text()

old = r'''\frac{\Delta S_i}{S_i}
\sim
\frac{\Delta X_i}{L_i(X_i)}
'''
new = r'''\frac{\Delta S_i}{S_i}
\sim
\frac{\Delta X_i}{L_i(\rn,X_i)}
'''
if t.count(old) != 1:
    raise SystemExit(f'expected one local-variation reference, found {t.count(old)}')
t = t.replace(old, new, 1)

old = r'''The local map and jet-response diagnostics were discussed in Sec.~\ref{subsubsec:z1jet-illustration}.  For the
actual NNLO LHE comparison, the technical cuts and process definition are

The numerical hierarchy of the technical cuts must also be treated using their actual definitions. In the
'''
new = r'''The local map and jet-response diagnostics were discussed in Sec.~\ref{subsubsec:z1jet-illustration}.
For the actual NNLO LHE comparison, the numerical hierarchy of the technical cuts must be treated using their
actual definitions. In the
'''
if t.count(old) != 1:
    raise SystemExit(f'expected one Z+1-jet transition paragraph, found {t.count(old)}')
t = t.replace(old, new, 1)

p.write_text(t)
