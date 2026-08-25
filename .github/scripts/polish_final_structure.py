from pathlib import Path

p = Path('main.tex')
t = p.read_text()

# The two process examples are now self-contained. Remove the old internal
# 'consequence' headings so each process reads as one continuous discussion.
for heading in [
    '\\subsubsection{Drell--Yan consequence}\n\n',
    '\\subsubsection{\\texorpdfstring{$Z+1$-jet}{Z+1-jet} consequence}\n\n',
]:
    if t.count(heading) != 1:
        raise SystemExit(f'expected one obsolete process heading: {heading!r}')
    t = t.replace(heading, '', 1)

# Give the container subsection a phenomenological title.
old = '\\subsection{Complete process examples}\n'
new = '\\subsection{Process-specific NNLO observables}\n'
if t.count(old) != 1:
    raise SystemExit('process-example subsection heading not found uniquely')
t = t.replace(old, new, 1)

# The K=0 Phi_3 specialization is true but not the bound relevant to the
# higher Z+1j projection; the relevant neighboring bound T2/T1<=2/3 is derived
# explicitly a few lines later. Remove the distracting specialization here.
old = (
    'For a three-parton configuration, relevant for the next multiplicity in the colour-singlet-plus-jet NNLO\n'
    'calculation, Eq.~\\eqref{eq:t1-t0-multiplicity-bound} instead gives\n'
    '\\(\\mathcal T_1/\\mathcal T_0\\le2/3\\).\n\n\n')
if t.count(old) != 1:
    raise SystemExit('distracting Z+1jet T1/T0 specialization not found uniquely')
t = t.replace(old, '', 1)

# In the lower-map strong-ordering estimate the r_{N-1} derivative acts on
# the full r_{N-1}-dependent bracket, including the neighboring-scale power.
old = r'''\begin{equation}
\Delta_{\Pi_N}
\frac{d\sigma}{d\rnm}
\sim
\frac{1}{p}
\left(\frac{\rn^{\cut}}{\rnm}\right)^p
\partial_{\rnm}
\left[
r_{N-1,\rm char}\,\widetilde F(\rnm,\mathbf X)
\right].
\label{eq:lower-map-integrated-scaling}
\end{equation}
'''
new = r'''\begin{equation}
\Delta_{\Pi_N}
\frac{d\sigma}{d\rnm}
\sim
\frac{1}{p}
\partial_{\rnm}
\left[
r_{N-1,\rm char}\,\widetilde F(\rnm,\mathbf X)
\left(\frac{\rn^{\cut}}{\rnm}\right)^p
\right].
\label{eq:lower-map-integrated-scaling}
\end{equation}
'''
if t.count(old) != 1:
    raise SystemExit('lower-map integrated scaling equation not found uniquely')
t = t.replace(old, new, 1)

# Remove the obsolete 'toy' terminology from the label as well.
t = t.replace('sec:lower-map-toy', 'subsec:lower-spectrum-migration')

p.write_text(t)
