from pathlib import Path

p = Path('main.tex')
t = p.read_text()

# Keep the transition from Sec. 6 concise; Sec. 7 itself gives the full reason
# for delaying the final r_N integration.
old = (
    'The preceding discussion deliberately stops at the singular spectrum differential in $\\rn$. '
    'Concrete process examples are postponed until Sec.~\\ref{sec:nnlo-differential-predictions}, where '
    'the $\\rn$ integration and the complete NNLO measurement can be considered together. Before performing '
    'that integration, however, the representation of the complementary $\\rn<\\rn^{\\cut}$ bin must first '
    'be examined, which requires the lower projection $\\Pi_N$.\n\n')
new = (
    'The preceding discussion deliberately stops at the singular spectrum differential in $\\rn$. '
    'Before integrating it into a final NNLO observable, the complementary $\\rn<\\rn^{\\cut}$ event '
    'representation and its lower projection $\\Pi_N$ must first be understood.\n\n')
if t.count(old) != 1:
    raise SystemExit('Sec. 6 to Sec. 7 bridge not found uniquely')
t = t.replace(old, new, 1)

# Clarify the role of the r_N integration in the lower-map section. It is used
# to expose the next-lower singular spectrum, not yet to construct d sigma/dX.
marker = r'''\label{eq:lower-map-migration-master}
\end{equation}
'''
addition = r'''\label{eq:lower-map-migration-master}
\end{equation}
The integration over $\rn$ in Eq.~\eqref{eq:lower-map-migration-master} should not be confused with the
final integration that constructs an NNLO distribution in the physical observables $\mathbf X$.  Here it is
performed only to expose how the lower projection feeds into the next lower singular spectrum, which remains
differential in $\rnm$.
'''
if t.count(marker) != 1:
    raise SystemExit('lower-map master equation marker not found uniquely')
t = t.replace(marker, addition, 1)

# In the actual Z+1jet setup the process-defining lower variable is q_T.
old = r'''\begin{equation}
\rnm=\mathcal T_0\ \mathrm{or}\ q_T ,\qquad
\rn=\mathcal T_1,\qquad
\rnp=\mathcal T_2.
\label{eq:z1j-resolution-identification}
\end{equation}
'''
new = r'''\begin{equation}
\rnm=q_T,\qquad
\rn=\mathcal T_1,\qquad
\rnp=\mathcal T_2.
\label{eq:z1j-resolution-identification}
\end{equation}
'''
if t.count(old) != 1:
    raise SystemExit('Z+1jet resolution identification not found uniquely')
t = t.replace(old, new, 1)

# T0 remains useful only as a diagnostic coordinate on the limiting one-jet
# manifold; it is not an active generation variable in this setup.
marker = r'''Thus the physically relevant finite-$z$ region is compact, but it need not be strongly ordered.

A qualitative difference from Drell--Yan is that preserving the colour-singlet momentum does not completely
'''
addition = r'''Thus the physically relevant finite-$z$ region is compact, but it need not be strongly ordered.

In the setup considered here $q_T$ is the actual lower process-defining variable.  The quantity
$\mathcal T_0$ introduced below is not used as a generation cut; it is only a useful diagnostic coordinate
for identifying the point approached on the limiting one-jet Born manifold.

A qualitative difference from Drell--Yan is that preserving the colour-singlet momentum does not completely
'''
if t.count(marker) != 1:
    raise SystemExit('Z+1jet diagnostic-coordinate insertion point not found uniquely')
t = t.replace(marker, addition, 1)

p.write_text(t)
