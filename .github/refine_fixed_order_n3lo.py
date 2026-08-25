from pathlib import Path
p=Path('main.tex')
t=p.read_text()
old = r'''\subsection{Why a sliced NNLO ingredient is more restrictive inside an \texorpdfstring{$\mathrm{N}^3\mathrm{LO}$}{N3LO} slicing calculation}
\label{subsec:n3lo-embedding}

Consider now an outer $\mathrm{N}^3\mathrm{LO}$ calculation sliced in $\rnm$.  Its resolved region requires an
NNLO prediction for multiplicity $N$ that is differential in the outer resolution variable and in the
Born-like coordinates,'''
new = r'''\subsection{Outer $\mathrm{N}^3\mathrm{LO}$ slicing and an embedded sliced NNLO ingredient}
\label{subsec:n3lo-embedding}

A pure fixed-order $\mathrm{N}^3\mathrm{LO}$ calculation sliced directly in $\rnm$ already has the same two
classes of power corrections associated with its \emph{outer} cut,
\begin{equation}
\Delta_{\rm slice}^{(\rnm)}
=
\Delta_{\rm dyn}^{(\rnm)}
+
\Delta_{\rm kin}^{(\rnm)}.
\label{eq:n3lo-outer-pc-decomposition}
\end{equation}
Here $\Delta_{\rm dyn}^{(\rnm)}$ is the genuine subleading-power error of the outer LP factorization theorem,
while $\Delta_{\rm kin}^{(\rnm)}$ is caused by dropping exact kinematic dependence below the outer cut.  At
fixed order a suitable P2B construction can restore the latter, including fiducial migrations, but it cannot
restore the former.  This statement is independent of how the resolved NNLO ingredient is computed.

There is then a \emph{second}, nested issue if the NNLO ingredient required above the outer cut is itself
obtained from a slicing calculation.  Consider an outer $\mathrm{N}^3\mathrm{LO}$ calculation sliced in
$\rnm$.  Its resolved region requires an NNLO prediction for multiplicity $N$ that is differential in the
outer resolution variable and in the Born-like coordinates,'''
if t.count(old)!=1:
    raise SystemExit('N3LO subsection opening not found uniquely')
t=t.replace(old,new,1)
old2 = r'''\item \textbf{A sliced NNLO calculation embedded in an $\mathrm{N}^3\mathrm{LO}$ slicing calculation.}
The outer calculation requires the NNLO ingredient differential in $\rnm$ and in the Born-like variables.
The internal cut that can contaminate this lower singular spectrum is $\rn^{\cut}$, the lower-multiplicity cut
of the embedded NNLO calculation.  In a strongly ordered nested region the relevant parameters can be
$\rn^{\cut}/\rnm$ and, near the outer boundary, $\rn^{\cut}/\rnm^{\cut}$.  Kinematic contamination can be
removed by P2B; genuine dynamical contamination remains and must be controlled by the inner cut or by
subleading-power information.  The still higher $\rnp^{\cut}$ used only inside the exact NLO component is not
an additional fixed-order nesting error.'''
new2 = r'''\item \textbf{Pure fixed-order $\mathrm{N}^3\mathrm{LO}$ slicing and a sliced NNLO ingredient.}
The outer $\rnm^{\cut}$ slicing has its own dynamical and kinematic power corrections, exactly as at NNLO:
P2B can restore the outer kinematic part but not the outer dynamical LP truncation.  If the resolved NNLO
ingredient is itself sliced, an additional nested requirement appears.  The internal cut that can contaminate
the lower singular spectrum is $\rn^{\cut}$, the lower-multiplicity cut of the embedded NNLO calculation.
In a strongly ordered nested region the relevant parameters can be $\rn^{\cut}/\rnm$ and, near the outer
boundary, $\rn^{\cut}/\rnm^{\cut}$.  Kinematic contamination from the inner slicing can again be removed by
P2B; genuine dynamical contamination remains and must be controlled by the inner cut or by subleading-power
information.  The still higher $\rnp^{\cut}$ used only inside the exact NLO component is not an additional
fixed-order nesting error.'''
if t.count(old2)!=1:
    raise SystemExit('Summary N3LO item not found uniquely')
t=t.replace(old2,new2,1)
p.write_text(t)
print('Clarified outer N3LO slicing versus embedded NNLO slicing.')
