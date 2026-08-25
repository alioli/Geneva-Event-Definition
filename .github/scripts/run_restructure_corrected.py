from pathlib import Path
import ast
import re

main = Path('main.tex')
t = main.read_text()

# Reuse the carefully written replacement text for the combined lower-locality
# section from the staging script, but do not execute that script (its marker
# strings used literal \\n sequences).
src = Path('.github/scripts/restructure_lower_locality.py').read_text()
module = ast.parse(src)
new7 = None
for node in module.body:
    if isinstance(node, ast.Assign):
        if any(isinstance(x, ast.Name) and x.id == 'new7' for x in node.targets):
            new7 = ast.literal_eval(node.value)
            break
if new7 is None:
    raise SystemExit('could not recover new7 replacement text')


def pop_between(start, end, name):
    global t
    i = t.find(start)
    if i < 0:
        raise SystemExit(f'{name}: start marker not found')
    j = t.find(end, i + len(start))
    if j < 0:
        raise SystemExit(f'{name}: end marker not found')
    block = t[i:j]
    t = t[:i] + t[j:]
    return block.strip() + '\n\n'

# Full process examples currently split between Sec. 6 and the integrated NNLO section.
dy_local = pop_between(
    '\\subsubsection{Drell--Yan illustration}\n',
    '\\subsubsection{\\texorpdfstring{$Z+1$-jet}{Z+1-jet} illustration}\n',
    'DY local example')
z_local = pop_between(
    '\\subsubsection{\\texorpdfstring{$Z+1$-jet}{Z+1-jet} illustration}\n',
    '\\section{Differential locality of the lower map}\n',
    'Z+1jet local example')

# Process-specific specializations of the general minimized-jettiness bound.
start = 'For Drell--Yan double-real kinematics, the relevant configuration is '
end = '\\subsection{Observable response to projection-induced migrations}\n'
i = t.find(start); j = t.find(end, i)
if i < 0 or j < 0:
    raise SystemExit('process-specific jettiness block not found')
proc_bounds = t[i:j]
t = t[:i] + t[j:]
needle = 'For a three-parton configuration, relevant for the next multiplicity in the colour-singlet-plus-jet NNLO\n'
k = proc_bounds.find(needle)
if k < 0:
    raise SystemExit('process-specific jettiness block could not be split')
dy_bound = proc_bounds[:k].strip() + '\n\n'
z_bound = proc_bounds[k:].strip() + '\n\n'

# Replace the old standalone Sections 7--10 by the new single Section 7.
old7 = '\\section{Differential locality of the lower map}\n'
old11 = '\\section{From local projection effects to NNLO differential predictions}\n'
i = t.find(old7); j = t.find(old11, i)
if i < 0 or j < 0:
    raise SystemExit('old Sections 7--10 block not found')
t = t[:i] + new7 + t[j:]

# Extract the already-existing integrated pieces of the two process examples.
dy_cons = pop_between(
    '\\subsubsection{Drell--Yan consequence}\n',
    '\\subsubsection{\\texorpdfstring{$Z+1$-jet}{Z+1-jet} consequence}\n',
    'DY integrated consequence')
z_cons = pop_between(
    '\\subsubsection{\\texorpdfstring{$Z+1$-jet}{Z+1-jet} consequence}\n',
    '\\subsection{Lower \\texorpdfstring{$N+1\\to N$}{N+1 to N} projection, NNLO power corrections, and P2B}\n',
    'Z+1jet integrated consequence')

# Remove only the sentences that referred back to the now-moved local examples.
dy_cons = dy_cons.replace(
    'The local Drell--Yan analysis in Sec.~\\ref{subsubsec:dy-illustration} can now be integrated over\n'
    '$\\mathcal T_0$.  In the saturated region,\n\n', '', 1)
z_cons = z_cons.replace(
    'The local map and jet-response diagnostics were discussed in Sec.~\\ref{subsubsec:z1jet-illustration}.\n',
    '', 1)

# Put the specialized bounds inside the corresponding complete example.
dy_label = '\\label{subsubsec:dy-illustration}\n'
z_label = '\\label{subsubsec:z1jet-illustration}\n'
if dy_label not in dy_local or z_label not in z_local:
    raise SystemExit('process example labels not found')
dy_local = dy_local.replace(dy_label, dy_label + '\n' + dy_bound, 1)
z_local = z_local.replace(z_label, z_label + '\n' + z_bound, 1)

dy_complete = dy_local.rstrip() + '\n\n' + dy_cons.strip() + '\n\n'
z_complete = z_local.rstrip() + '\n\n' + z_cons.strip() + '\n\n'

marker = '\\subsection{Lower \\texorpdfstring{$N+1\\to N$}{N+1 to N} projection, NNLO power corrections, and P2B}\n'
idx = t.find(marker)
if idx < 0:
    raise SystemExit('lower-projection NNLO marker not found')
process_block = '\\subsection{Complete process examples}\n\n' + dy_complete + z_complete
t = t[:idx] + process_block + t[idx:]

# Explain at the end of Sec. 6 why examples are postponed until the NNLO observable is assembled.
last = (
    'when $|\\Delta X_i|\\ll L_i$. In a smooth region \\(L_i\\) is of the order of a hard or characteristic\n'
    'kinematic scale, so uniform nested infrared locality of the map together with IRC safety of the observable\n'
    'translates into a small projection effect. Near a kinematic boundary, Jacobian feature or Sudakov shoulder,\n'
    'however, \\(L_i\\) can become parametrically much smaller than the hard scale. A displacement that is small in\n'
    'absolute terms can then generate a large local change in the distribution. When \\(|\\Delta X_i|\\) becomes\n'
    'comparable to the distance from the nonanalytic point, the derivative expansion itself is no longer uniform\n'
    'and the effect is better viewed as migration across the feature rather than as a small derivative correction.\n')
if last not in t:
    raise SystemExit('end of generic observable-response discussion not found')
t = t.replace(last, last + (
    '\nThe statements in this subsection concern the spectrum at fixed $\\rn$. Concrete process examples are\n'
    'postponed to Sec.~\\ref{sec:nnlo-differential-predictions}, where the $\\rn$ integration and the complete NNLO\n'
    'measurement can be discussed at the same time rather than splitting each example between local and integrated\n'
    'arguments.\n'), 1)

old_intro = (
    'Sections~\\ref{sec:higher-singular-spectrum}--\\ref{sec:nested-event-consistency} characterized the local\n'
    'singular structure and the locality requirements of the nested maps.  We now perform the logically separate\n'
    'step of integrating over the lower resolution variable.')
new_intro = (
    'Sections~\\ref{sec:higher-singular-spectrum} and \\ref{sec:lower-map-locality} have now established the\n'
    'local structure of both projections before any final integration over $\\rn$. We now perform the logically\n'
    'separate step of constructing NNLO distributions differential only in the physical observables, integrating\n'
    'the resolved spectrum over the lower resolution variable and combining it with the lower-multiplicity bin.')
if old_intro not in t:
    raise SystemExit('NNLO section introduction not found')
t = t.replace(old_intro, new_intro, 1)

# Sanity checks: examples only once and only after the NNLO heading; old standalone sections gone.
for s in [
    '\\section{Toy model for migration',
    '\\section{Optional Born-level fiducial or generation boundaries}',
    '\\section{Consistency conditions for the nested event definition}',
]:
    if s in t:
        raise SystemExit('obsolete standalone section survived: ' + s)

nnlo = t.find('\\section{From local projection effects to NNLO differential predictions}')
for ex in [
    '\\subsubsection{Drell--Yan illustration}',
    '\\subsubsection{\\texorpdfstring{$Z+1$-jet}{Z+1-jet} illustration}',
]:
    if t.count(ex) != 1 or t.find(ex) < nnlo:
        raise SystemExit('process example missing, duplicated, or still before NNLO section: ' + ex)

labels = re.findall(r'\\label\{([^}]+)\}', t)
dups = sorted({x for x in labels if labels.count(x) > 1})
if dups:
    raise SystemExit('duplicate labels after restructuring: ' + ', '.join(dups))

main.write_text(t)
