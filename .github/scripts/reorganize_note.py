from pathlib import Path
import re

p = Path('main.tex')
t = p.read_text()


def require_once(s, name):
    n = t.count(s)
    if n != 1:
        raise SystemExit(f'{name}: expected exactly one occurrence, found {n}')


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
    return block.strip() + '\n'


# Remove the temporary review marker.
t = re.sub(
    r'\n*\{\\bfseries NOTE REVIEWED ONLY UP TO THIS POINT, THE MATERIAL BELOW STILL NEEDS TO BE REVIEWED \}\n*',
    '\n\n', t, count=1
)

# Make the scope of Sec. 6 explicit: r_N is kept differential throughout.
sec6 = r'''\section{How a higher cut can contaminate a lower singular spectrum}
'''
require_once(sec6, 'section 6 heading')
t = t.replace(sec6, sec6 + r'''\label{sec:higher-singular-spectrum}

Throughout this section the lower resolution variable $\rn$ is kept differential.  The object of interest is
therefore the projection-induced modification of the singular spectrum
$d\sigma/(d\rn\,dX_i)$ at fixed $\rn$.  No integration over $\rn$ is used here to infer the size of a final
NNLO distribution differential only in $X_i$.  That separate step, and the resulting dependence on the
technical cuts after the $\rn$ integration, are discussed only in
Sec.~\ref{sec:nnlo-differential-predictions}.

''', 1)

# Move the strongly ordered r_N-integrated estimate out of Sec. 6.
strong_integrated = pop_between(
    'To see explicitly how the neighboring-cut ratio arises after integrating over the lower resolution variable,\n',
    '\n\\subsection{Comparable or inverted cuts and uniform nested infrared locality}\n',
    'strong-order integrated block'
)

# Replace the current comparable-cut introduction by a fixed-r_N statement, while retaining
# the original integrated discussion for Sec. 11.
comp_header = r'''\subsection{Comparable or inverted cuts and uniform nested infrared locality}
\label{subsec:uniform-nested-locality}

'''
require_once(comp_header, 'comparable-cut subsection header')
comp_start = t.index(comp_header) + len(comp_header)
comp_end_marker = r'''\subsubsection{Uniform nested infrared locality of the map}
'''
comp_end = t.find(comp_end_marker, comp_start)
if comp_end < 0:
    raise SystemExit('comparable-cut subsection: nested-locality marker not found')
comparable_integrated = t[comp_start:comp_end].strip() + '\n'
local_comparable = r'''The strong-ordering estimate of Sec.~\ref{subsec:strongly-ordered-higher-projection} is a statement at
fixed $\rn$ and cannot be extrapolated to configurations with a finite neighboring ratio
$z=\rnp/\rn$.  At fixed $\rn$, if $\rn\gg\rnp^{\cut}$ the higher technical cut enforces
$z\ll1$, whereas for $\rn$ comparable to or smaller than $\rnp^{\cut}$ it need not do so.  Particular
resolution variables can impose additional kinematic restrictions on the finite allowed range of $z$.
The singular spectrum in this region must therefore be analyzed directly in the simultaneous unresolved
limit, independently of the later integration over $\rn$.

'''
t = t[:comp_start] + local_comparable + t[comp_end:]

# Move the explicit fixed-kappa integral following the uniform nested-locality spectrum.
uniform_integrated = pop_between(
    'For a generic pair of resolution variables, and in the absence of an additional kinematic cap that becomes\n',
    '\n\\subsubsection{Why fixed-order NNLO slicing does not require uniform nested locality}\n',
    'uniform nested integrated block'
)

# Move the N-jettiness saturated-interval integral, leaving the kinematic bound itself in Sec. 6.
njettiness_integrated = pop_between(
    'If \\(\\mathcal T_0^{\\cut}<\\mathcal T_1^{\\cut}/c_M\\), the interval in which the kinematic bound rather than\n',
    '\nFor Drell--Yan double-real kinematics, the relevant configuration is',
    'N-jettiness integrated block'
)

# Observable-response notation must refer to the spectrum at fixed r_N, not to the final integrated prediction.
old_response = r'''Let
\begin{equation}
S_i(X_i)=\frac{d\sigma}{dX_i}
\label{eq:observable-spectrum-S}
\end{equation}
denote the relevant smooth spectrum in a region where a first-order migration expansion is meaningful, and
define its local variation scale by
\begin{equation}
L_i(X_i)
=
\left|
\partial_{X_i}\ln S_i(X_i)
\right|^{-1}
=
\left|
\frac{S_i(X_i)}{S_i'(X_i)}
\right|.
\label{eq:local-variation-scale}
\end{equation}
'''
require_once(old_response, 'observable-response definition')
new_response = r'''At fixed $\rn$, let
\begin{equation}
S_i(\rn,X_i)=\frac{d\sigma}{d\rn\,dX_i}
\label{eq:observable-spectrum-S}
\end{equation}
denote the relevant smooth singular spectrum in a region where a first-order migration expansion is meaningful,
and define its local variation scale in $X_i$ by
\begin{equation}
L_i(\rn,X_i)
=
\left|
\partial_{X_i}\ln S_i(\rn,X_i)
\right|^{-1}
=
\left|
\frac{S_i(\rn,X_i)}{\partial_{X_i}S_i(\rn,X_i)}
\right|.
\label{eq:local-variation-scale}
\end{equation}
'''
t = t.replace(old_response, new_response, 1)

# Label the two illustrations and keep the DY discussion local in T0.
dyh = r'''\subsubsection{Drell--Yan illustration}
'''
require_once(dyh, 'DY illustration heading')
t = t.replace(dyh, dyh + '\\label{subsubsec:dy-illustration}\n', 1)

n, = (len(re.findall(
    r'Nevertheless,\nin GENEVA one finds that making .*?There are two conceptually separate reasons\. First,\n',
    t, flags=re.S
)),)
if n != 1:
    raise SystemExit(f'DY integrated lead-in: expected 1 match, found {n}')
t = re.sub(
    r'Nevertheless,\nin GENEVA one finds that making .*?There are two conceptually separate reasons\. First,\n',
    r'For the local singular spectrum at fixed \\(\\mathcal T_0\\), two features are important. First,\n',
    t, count=1, flags=re.S
)

dy_integrated = pop_between(
    'If \\(\\mathcal T_1^{\\cut}\\) is held fixed while \\(\\mathcal T_0^{\\cut}\\) is made much smaller, the higher cut\n',
    '\nThe important exception is the region\n',
    'DY integrated block'
)

# Move the actual Z+1-jet cut hierarchy and integrated LHE comparison to Sec. 11.
z_integrated = pop_between(
    'The numerical hierarchy of the technical cuts must also be treated using their actual definitions. In the\n',
    '\nThis pattern does not yet establish a formal failure of uniform nested infrared locality. The\n',
    'Z+1-jet integrated comparison block'
)

# Keep only the local scaling diagnostic in Sec. 6.3.2.
pat = re.compile(
    r'This pattern does not yet establish a formal failure of uniform nested infrared locality\. The\n'
    r'\$\\mathcal T_1\^\{\\rm FR\}\$ map could instead be nested-local with a larger coefficient or a slower approach to the\n'
    r'simultaneous unresolved limit than FKS\. The decisive next test is therefore local: apply both projections to\n'
)
if len(pat.findall(t)) != 1:
    raise SystemExit('Z+1-jet local-test lead-in not found uniquely')
t = pat.sub(
    'The decisive test of the nested-locality properties of the two mappings is local: apply both projections to\n',
    t, count=1
)

z_cutstudy = pop_between(
    'A complementary cut study can distinguish formal from merely numerical problems. Keeping the dynamical\n',
    '\nThe $Z+1$-jet example therefore illustrates why exact preservation of the chosen resolution variable is only\n',
    'Z+1-jet cut-study block'
)

# Label the lower-map block so Sec. 10 can synthesize it without duplicating it.
for heading, label in [
    ('\\section{Differential locality of the lower map}\n', '\\label{sec:lower-map-locality}\n'),
    ('\\section{Toy model for migration in \\texorpdfstring{\\(r_{N-1}\\)}{rN-1}}\n', '\\label{sec:lower-map-toy}\n'),
    ('\\section{Optional Born-level fiducial or generation boundaries}\n', '\\label{sec:born-boundaries}\n'),
]:
    require_once(heading, heading)
    t = t.replace(heading, heading + label, 1)

# Sec. 10 becomes the synthesis of the two locality layers.
old10 = '\\section{Nested consistency of the higher map}\n'
require_once(old10, 'section 10 heading')
t = t.replace(old10, '\\section{Consistency conditions for the nested event definition}\n\\label{sec:nested-event-consistency}\n', 1)

old11 = r'''\section{Lower \texorpdfstring{\(N+1\to N\)}{N+1 to N} projection, NNLO power corrections, and P2B}
'''
require_once(old11, 'old section 11 heading')

synthesis = r'''
The conditions on the lower map $\Pi_N$ are complementary rather than redundant.  As discussed in
Secs.~\ref{sec:lower-map-locality}--\ref{sec:born-boundaries}, $\Pi_N$ must be local in any lower variable in
which the singular prediction is kept differential, and it must preserve the classification of any active
Born-level generation or fiducial boundary.  The complete event definition therefore contains two distinct
locality layers: the nested behavior of $\Pi_{N+1}$ in the $N+2\to N+1\to N$ limit and the differential and
boundary locality of $\Pi_N$ in the $N+1\to N\to N-1$ limit.  Only after these local properties have been
specified is it useful to integrate over $\rn$ and discuss their net effect on an NNLO prediction.

'''

higher = r'''\section{From local projection effects to NNLO differential predictions}
\label{sec:nnlo-differential-predictions}

Sections~\ref{sec:higher-singular-spectrum}--\ref{sec:nested-event-consistency} characterized the local
singular structure and the locality requirements of the nested maps.  We now perform the logically separate
step of integrating over the lower resolution variable.  Schematically, the contribution of the higher
projection to a distribution differential only in $X_i$ is obtained from
\begin{equation}
\left.\Delta_{\rm proj}^{(\rnp)}\frac{d\sigma}{dX_i}\right|_{\rn>\rn^{\cut}}
=
\int_{\rn^{\cut}}^{\rn^{\rm max}} d\rn\,
\Delta_{\rm proj}^{(\rnp)}\frac{d\sigma}{d\rn\,dX_i}.
\label{eq:integrated-higher-projection-definition}
\end{equation}
This integration can convert a local neighboring-scale suppression into a dependence on the technical cuts,
but it must not be confused with the singularity analysis of the fixed-$\rn$ spectrum carried out above.

\subsection{Higher $\Ph_{N+2}\to\widehat\Ph_{N+1}$ LHE projection}
\label{subsec:higher-projection-nnlo}

\subsubsection{Strongly ordered hierarchy}

''' + strong_integrated + r'''
\subsubsection{Comparable cuts and uniform nested scaling}

''' + comparable_integrated + '\n' + uniform_integrated + r'''
\subsubsection{Axis-minimized $N$-jettiness}

Using the kinematic bounds derived in Sec.~\ref{subsec:uniform-nested-locality}, the corresponding integrated
region is obtained only after the fixed-$\mathcal T_0$ spectrum has been understood.  In particular,

''' + njettiness_integrated + r'''
\subsubsection{Drell--Yan consequence}

The local Drell--Yan analysis in Sec.~\ref{subsubsec:dy-illustration} can now be integrated over
$\mathcal T_0$.  In the saturated region,

''' + dy_integrated + r'''
\subsubsection{\texorpdfstring{$Z+1$-jet}{Z+1-jet} consequence}

The local map and jet-response diagnostics were discussed in Sec.~\ref{subsubsec:z1jet-illustration}.  For the
actual NNLO LHE comparison, the technical cuts and process definition are

''' + z_integrated + r'''
The observed hierarchy between the two mappings does not by itself establish a formal failure of uniform
nested infrared locality.  The $\mathcal T_1^{\rm FR}$ map could instead be nested-local with a larger
coefficient or a slower approach to the simultaneous unresolved limit than FKS.  The event-by-event scaling
test of Eq.~\eqref{eq:z1j-local-diagnostics}, performed at fixed finite $z$, is the appropriate way to
distinguish these possibilities.

''' + z_cutstudy + r'''
\subsection{Lower \texorpdfstring{$N+1\to N$}{N+1 to N} projection, NNLO power corrections, and P2B}

'''

# Insert the synthesis before the new Sec. 11, then replace the old Sec. 11 heading by the new architecture.
t = t.replace(old11, synthesis + higher, 1)

# Summary wording: distinguish the local strong-ordering result from its integrated consequence.
t = t.replace(
    'The scaling in \\(\\rnp^{\\cut}/\\rn^{\\cut}\\) derived in Sec.~\\ref{subsec:strongly-ordered-higher-projection}\nrequires a genuine hierarchy.',
    'The local strong-ordering expansion of Sec.~\\ref{subsec:strongly-ordered-higher-projection} and its\nintegrated consequence in Sec.~\\ref{subsec:higher-projection-nnlo} require a genuine hierarchy.',
    1
)

# Basic structural sanity checks.
if 'NOTE REVIEWED ONLY UP TO THIS POINT' in t:
    raise SystemExit('review marker survived')
if t.count('\\section{From local projection effects to NNLO differential predictions}') != 1:
    raise SystemExit('new NNLO differential section missing or duplicated')
if t.count('\\subsection{Lower \\texorpdfstring{$N+1\\to N$}{N+1 to N} projection, NNLO power corrections, and P2B}') != 1:
    raise SystemExit('lower NNLO/P2B subsection missing or duplicated')

labels = re.findall(r'\\label\{([^}]+)\}', t)
dups = sorted({x for x in labels if labels.count(x) > 1})
if dups:
    raise SystemExit('duplicate labels after reorganization: ' + ', '.join(dups))

p.write_text(t)
