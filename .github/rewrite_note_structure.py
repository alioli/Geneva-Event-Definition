from pathlib import Path

p = Path('main.tex')
t = p.read_text()

# 1. Move the fixed-order counterexample out of the LHE-spectrum section.
bad_start = r'\subsubsection{Why fixed-order NNLO slicing does not require uniform nested locality}'
bad_end = r'\subsubsection{Kinematic restriction for minimized \(N\)-jettiness}'
if t.count(bad_start) != 1 or t.count(bad_end) != 1:
    raise SystemExit('Could not identify fixed-order counterexample block uniquely')
ia = t.index(bad_start)
ib = t.index(bad_end, ia)
bad_block = t[ia:ib]
t = t[:ia] + t[ib:]
# Promote it when it is reinserted in the dedicated fixed-order section.
bad_block = bad_block.replace(bad_start, r'\subsection{Auxiliary subtraction maps versus physical event projections}', 1)

# 2. Remove the old lower-map section entirely. Its useful content is rewritten below.
old7 = r'\section{Lower-map locality and nested consistency before NNLO observables}'
old8 = r'\section{From local projection effects to NNLO differential predictions}'
if t.count(old7) != 1 or t.count(old8) != 1:
    raise SystemExit('Could not identify old Sections 7 and 8 uniquely')
i7 = t.index(old7)
i8 = t.index(old8, i7)
t = t[:i7] + t[i8:]

# 3. End Sec. 6 by closing the LHE-spectrum discussion, not by opening the fixed-order nesting problem.
old_transition = (
    'The preceding discussion deliberately stops at the singular spectrum differential in $\\rn$. '
    'Before integrating it into a final NNLO observable, the complementary $\\rn<\\rn^{\\cut}$ event representation '
    'and its lower projection $\\Pi_N$ must first be understood.\n\n'
)
new_transition = r'''The preceding discussion deliberately stops at the singular spectrum differential in $\rn$.
It concerns a problem that is specific to the \emph{LHE event definition}: below $\rnp^{\cut}$ an exact
$\Ph_{N+2}$ configuration is discarded and the projected $\widehat\Ph_{N+1}$ configuration is retained as the
physical event representative.  In a pure fixed-order calculation the same higher-multiplicity partition is
only an internal organization of an exact NLO contribution and does not generate this residual projection
effect.  We now integrate the fixed-$\rn$ result to obtain its consequences for NNLO LHE observables.  The
separate question of genuine slicing power corrections in a pure fixed-order NNLO calculation, and of using
such a sliced NNLO result inside an $\mathrm{N}^3\mathrm{LO}$ slicing calculation, is postponed to
Sec.~\ref{sec:fixed-order-nested-slicing}.

'''
if old_transition not in t:
    raise SystemExit('Sec. 6 transition sentence not found')
t = t.replace(old_transition, new_transition, 1)

# 4. Rewrite the opening of the NNLO-observable section and make its LHE-specific scope explicit.
sec8_start = r'\section{From local projection effects to NNLO differential predictions}'
sub_higher = r'\subsection{Higher $\Ph_{N+2}\to\widehat\Ph_{N+1}$ LHE projection}'
if t.count(sec8_start) != 1 or t.count(sub_higher) != 1:
    raise SystemExit('NNLO observable section markers not found uniquely')
i = t.index(sec8_start)
j = t.index(sub_higher, i)
new_nnlo_intro = r'''\section{From the lower singular spectrum to NNLO LHE observables}
\label{sec:nnlo-differential-predictions}

This section completes the LHE-specific problem studied in Sec.~\ref{sec:higher-singular-spectrum}.  The
higher cut $\rnp^{\cut}$ does not represent a dynamical LP approximation in the underlying fixed-order
calculation.  A dependence on it appears here only because, for the LHE sample, the measurement on exact
$\Ph_{N+2}$ kinematics is replaced below the cut by the measurement on the projected
$\widehat\Ph_{N+1}$ event.  The resulting effect is therefore a \emph{kinematic event-definition effect}.
It is absent if the same NNLO calculation is analyzed purely at fixed order with exact partonic kinematics.

The local analysis of Sec.~\ref{sec:higher-singular-spectrum} kept $\rn$ differential.  We now perform the
logically separate integration over the resolved region,
\begin{equation}
\left.\Delta_{\rm proj}^{(\rnp)}\frac{d\sigma}{dX_i}\right|_{\rn>\rn^{\cut}}
=
\int_{\rn^{\cut}}^{\rn^{\rm max}} d\rn\,
\Delta_{\rm proj}^{(\rnp)}\frac{d\sigma}{d\rn\,dX_i}.
\label{eq:integrated-higher-projection-definition}
\end{equation}
This integration converts the local behavior of the singular $\rn$ spectrum into a finite-cut dependence of
NNLO LHE distributions.  It should not be confused with the lower-region approximation used in a sliced
fixed-order NNLO calculation.  That second problem contains both genuine dynamical power corrections and
kinematic projection power corrections and is discussed only in Sec.~\ref{sec:fixed-order-nested-slicing}.

'''
t = t[:i] + new_nnlo_intro + t[j:]

# 5. Remove the old lower-projection/P2B subsection from the LHE-observable section.
lower_old = r'\subsection{Lower \texorpdfstring{$N+1\to N$}{N+1 to N} projection, NNLO power corrections, and P2B}'
summary = r'\section{Summary of mapping requirements}'
if t.count(lower_old) != 1 or t.count(summary) != 1:
    raise SystemExit('Could not identify old P2B subsection or summary uniquely')
il = t.index(lower_old)
isum = t.index(summary, il)
t = t[:il] + t[isum:]

# 6. Insert a new, self-contained fixed-order section before the summary.
fixed_section = r'''
\section{Pure fixed-order slicing and nested sliced calculations}
\label{sec:fixed-order-nested-slicing}

The discussion now changes problem.  Sections~\ref{sec:higher-singular-spectrum} and
\ref{sec:nnlo-differential-predictions} concerned the replacement of an exact configuration by a projected
\emph{physical LHE event}.  In a pure fixed-order calculation projections play a different role: they are
auxiliary devices used to organize subtraction or to evaluate the LP contribution below a slicing cut.  If
exact and projected terms are kept correlated, kinematic information lost by the projection can in principle
be restored.  What cannot be restored in this way is dynamics that was never retained because the cross
section itself was replaced by its leading-power expansion.

It is therefore useful to separate from the outset two kinds of slicing power corrections,
\begin{equation}
\boxed{
\Delta_{\rm slice}^{(\rn)}
=
\Delta_{\rm dyn}^{(\rn)}
+
\Delta_{\rm kin}^{(\rn)}
}
\label{eq:fixed-order-pc-decomposition}
\end{equation}
where $\Delta_{\rm dyn}^{(\rn)}$ denotes the genuine dynamical error of the LP expansion in $\rn$, while
$\Delta_{\rm kin}^{(\rn)}$ denotes the error induced by evaluating the measurement on projected
lower-multiplicity kinematics.  Projection-to-Born can restore the second contribution, but not the first.

\subsection{What a slicing cut does in a pure fixed-order NNLO calculation}
\label{subsec:fixed-order-nnlo-slicing}

Below the NNLO slicing cut $\rn^{\cut}$ the exact lower-multiplicity contribution is replaced by its LP
factorization theorem,
\begin{equation}
\frac{d\Sigma_N^{\rm NNLO}}{d\Ph_N}(\rn^{\cut})
\longrightarrow
\frac{d\Sigma_{N,\rm LP}^{\rm NNLO}}{d\Ph_N}(\rn^{\cut}).
\label{eq:nnlo-lp-replacement}
\end{equation}
The difference
\begin{equation}
\Delta_{\rm dyn}^{(\rn)}
=
\frac{d\Sigma_N^{\rm NNLO}}{d\Ph_N}(\rn^{\cut})
-
\frac{d\Sigma_{N,\rm LP}^{\rm NNLO}}{d\Ph_N}(\rn^{\cut})
\label{eq:dynamic-pc}
\end{equation}
is a genuine dynamical power correction.  Schematically,
\begin{equation}
\Delta_{\rm dyn}^{(\rn)}
\sim
\left(\frac{\rn^{\cut}}{Q}\right)^q
\sum_k a_k(\Ph_N)\ln^k\!\frac{\rn^{\cut}}{Q},
\qquad q>0,
\label{eq:dynamic-pc-scaling}
\end{equation}
when $Q$ is the relevant finite hard scale.  This error is present even for a completely inclusive
measurement of the Born variables.  It is not caused by a recoil prescription or by a mismatch between exact
and projected kinematics, and no P2B correction can reconstruct it.  Removing it requires taking a smaller
slicing cut, calculating subleading-power terms, or otherwise improving the dynamical approximation.

There is separately a kinematic power correction whenever exact higher-multiplicity kinematics are replaced
inside the measurement by a projection,
\begin{equation}
\Mcal(\Ph_{N+1})\longrightarrow
\Mcal\!\left(\Pi_N(\Ph_{N+1})\right).
\label{eq:fixed-order-lower-measurement-projection}
\end{equation}
This part is observable dependent and includes ordinary fiducial power corrections.  Unlike
Eq.~\eqref{eq:dynamic-pc}, it can be restored at fixed order by keeping the exact and projected measurements
correlated.

\subsection{Why a sliced NNLO ingredient is more restrictive inside an \texorpdfstring{$\mathrm{N}^3\mathrm{LO}$}{N3LO} slicing calculation}
\label{subsec:n3lo-embedding}

Consider now an outer $\mathrm{N}^3\mathrm{LO}$ calculation sliced in $\rnm$.  Its resolved region requires an
NNLO prediction for multiplicity $N$ that is differential in the outer resolution variable and in the
Born-like coordinates,
\begin{equation}
\frac{d\sigma_N^{\rm NNLO}}
{d\rnm\,d\mathbf X}.
\label{eq:nnlo-ingredient-for-n3lo}
\end{equation}
Suppose this NNLO ingredient is itself obtained with a slicing calculation in $\rn$.  Then the relevant
internal approximation is the \emph{lower-multiplicity NNLO cut} $\rn^{\cut}$.  It is this cut that can
contaminate the singular spectrum in $\rnm$ needed by the outer calculation.

By contrast, an additional $\rnp^{\cut}$ used only to organize the exact NLO $(N+1)$ contribution inside the
embedded NNLO calculation is not a new fixed-order slicing approximation.  When both sides of that partition
are treated with exact kinematics and the local and integrated subtraction terms are combined consistently,
its dependence cancels.  Thus, for a pure fixed-order nested calculation, the potentially problematic
neighboring hierarchy is
\begin{equation}
\boxed{
\rn^{\cut}\quad\hbox{versus}\quad \rnm,
}
\label{eq:relevant-inner-outer-hierarchy}
\end{equation}
not $\rnp^{\cut}$ versus $\rn$.  The latter becomes a physical issue only when the projected
$\widehat\Ph_{N+1}$ configuration is retained as an LHE event, as in Secs.~\ref{sec:higher-singular-spectrum}
and \ref{sec:nnlo-differential-predictions}.

For the outer slicing to inherit the correct singular structure, the sliced NNLO ingredient must reproduce
Eq.~\eqref{eq:nnlo-ingredient-for-n3lo} with an error that is sufficiently suppressed as $\rnm\to0$.  Both
parts of Eq.~\eqref{eq:fixed-order-pc-decomposition} must therefore be examined in the nested limit.  P2B can
remove the kinematic part; the dynamical part remains and may itself become nonuniform if the relevant scale
of the inner unresolved limit is set by $\rnm$ rather than by a fixed hard scale.

\subsection{Toy model for the locality of the embedded subtraction}
\label{subsec:nested-slicing-toy-model}

The original locality issue is most transparent in a simple toy model.  In the lower unresolved region of
the embedded NNLO calculation, take the singular contribution schematically as
\begin{equation}
\frac{d\sigma_{N+1}^{\rm sing}}
{d\rn\,d\rnm\,d\mathbf X}
\sim
\frac{1}{\rn}
F\!\left(\rnm,\mathbf X,
\ln\frac{\rn}{Q},\ldots\right).
\label{eq:nested-toy-singular}
\end{equation}
The outer calculation needs the dependence on $\rnm$ and $\mathbf X$ to remain correct.  Define the
exact-minus-projected displacements
\begin{align}
\Delta\rnm(\Ph_{N+1})
&=
\rnm(\Ph_{N+1})
-
\rnm\!\left(\Pi_N(\Ph_{N+1})\right),
\label{eq:delta-rnm}
\\
\Delta X_i(\Ph_{N+1})
&=
X_i(\Ph_{N+1})
-
X_i\!\left(\Pi_N(\Ph_{N+1})\right).
\label{eq:delta-x-lower-map}
\end{align}
Linearizing the measurement mismatch gives two distinct migration operators.  After integrating the inner
unresolved region, the kinematic contribution has the schematic form
\begin{align}
\Delta_{\rm kin}^{(\rn)}
\frac{d\sigma}{d\rnm\,d\mathbf X}
\sim{}&
\partial_{\rnm}
\int_0^{\rn^{\cut}}
\frac{d\rn}{\rn}
\left[F\,\Delta\rnm\right]
\nonumber\\
&+
\sum_i
\partial_{X_i}
\int_0^{\rn^{\cut}}
\frac{d\rn}{\rn}
\left[F\,\Delta X_i\right].
\label{eq:nested-toy-kinematic-migration}
\end{align}
The first line is the direct statement of locality of the inner subtraction with respect to the singular
outer variable $\rnm$.  The second line shows that preserving the singular variable alone is not sufficient
for a fully differential prediction: migrations in Born-like variables also modify the coefficient of the
$\rnm$ singular spectrum.  If an $X_i$ is integrated over its full range, its derivative term reduces to a
boundary contribution and can disappear; the $\rnm$ dependence, however, is intrinsic to the outer slicing
problem.

In a strongly ordered region
\begin{equation}
\rn\ll\rnm\ll Q,
\label{eq:lower-strong-ordering}
\end{equation}
let a generic kinematic displacement obey
\begin{equation}
\frac{\Delta Y}{Y_{\rm char}}
\sim
\left(\frac{\rn}{\rnm}\right)^p,
\qquad p>0,
\label{eq:nested-toy-kinematic-scaling}
\end{equation}
where $Y$ stands for either $\rnm$ or one of the $X_i$.  Then Eq.~\eqref{eq:nested-toy-kinematic-migration}
contains the neighboring-scale behavior
\begin{equation}
\Delta_{\rm kin}^{(\rn)}
\sim
\left(\frac{\rn^{\cut}}{\rnm}\right)^p
\times\hbox{derivatives of the lower singular spectrum},
\label{eq:nested-toy-kinematic-ratio}
\end{equation}
up to logarithms and finite coefficients.  Hence a cut that is harmless at fixed nonzero $\rnm$ can become
nonuniform as the outer singular limit is approached.  When the outer calculation itself probes
$\rnm\sim\rnm^{\cut}$, the natural ordered expansion parameter becomes
$\rn^{\cut}/\rnm^{\cut}$.

The same neighboring-scale issue can occur in the genuine dynamical power correction, but with a different
origin.  If the exact inner singular dynamics differ from their LP expansion by
\begin{equation}
\frac{d\sigma^{\rm exact}-d\sigma^{\rm LP}}
{d\rn\,d\rnm\,d\mathbf X}
\sim
\frac{1}{\rn}
\left(\frac{\rn}{\rnm}\right)^q
D(\rnm,\mathbf X,\ldots),
\qquad q>0,
\label{eq:nested-toy-dynamic-local}
\end{equation}
then integration below $\rn^{\cut}$ gives parametrically
\begin{equation}
\Delta_{\rm dyn}^{(\rn)}
\frac{d\sigma}{d\rnm\,d\mathbf X}
\sim
\left(\frac{\rn^{\cut}}{\rnm}\right)^q
D(\rnm,\mathbf X,\ldots),
\label{eq:nested-toy-dynamic-ratio}
\end{equation}
again up to logarithms.  This term is not a migration derivative and cannot be generated by changing the
measurement function.  It is therefore outside the reach of P2B.

\subsection{What P2B restores, and what it cannot restore}
\label{subsec:p2b-scope}

At fixed order, the kinematic term in Eq.~\eqref{eq:fixed-order-pc-decomposition} can be restored through a
projection-to-Born construction.  Schematically, suppressing the detailed subtraction structure,
\begin{equation}
\Delta_{\rm P2B}^{(\rn)}[\Mcal]
\sim
\int d\Ph_{N+1}\,
w_{\rm exact}(\Ph_{N+1})
\left[
\Mcal(\Ph_{N+1})-
\Mcal\!\left(\Pi_N(\Ph_{N+1})\right)
\right].
\label{eq:p2b-fpc-correlated}
\end{equation}
The two measurements are evaluated on the same exact higher-multiplicity phase-space point and carry
correlated weights.  This exactly targets the kinematic information lost by the projection: fiducial
migrations, recoil effects, and the derivative terms in Eq.~\eqref{eq:nested-toy-kinematic-migration}.
Within the perturbative order for which the exact higher-multiplicity ingredient is available, these
kinematic power corrections can therefore be recovered at fixed order.

P2B does \emph{not} modify the LP factorization theorem used for the dynamics below $\rn^{\cut}$.  It cannot
supply the missing term $D$ in Eq.~\eqref{eq:nested-toy-dynamic-local}, and hence cannot remove
$\Delta_{\rm dyn}^{(\rn)}$.  After a P2B restoration the residual slicing dependence of a pure fixed-order
calculation is therefore the genuine dynamical power correction.  Controlling it requires a sufficiently
small inner cut or explicit subleading-power information.

This distinction is especially important for an embedded NNLO calculation.  Without P2B, both
$\Delta_{\rm kin}^{(\rn)}$ and $\Delta_{\rm dyn}^{(\rn)}$ must be sufficiently local in the outer singular
variable.  With P2B, the kinematic part can be restored, but the dynamical part must still reproduce the
required $\rnm$ singular spectrum to the accuracy needed by the outer $\mathrm{N}^3\mathrm{LO}$ subtraction.

\subsection{Optional lower boundaries}
\label{sec:born-boundaries}

A process-defining lower boundary is an additional kinematic issue, not a new dynamical one.  If, for
example,
\begin{equation}
\Theta_B(\Ph_M)=
\Theta\!\left(\rnm(\Ph_M)-\rnm^{\cut}\right),
\label{eq:active-born-boundary}
\end{equation}
then a lower projection can move an event across that boundary.  For a small displacement,
\begin{equation}
\Theta\!\left(\rnm(\Pi_N\Ph_{N+1})-\rnm^{\cut}\right)
-
\Theta\!\left(\rnm(\Ph_{N+1})-\rnm^{\cut}\right)
\simeq
-\Delta\rnm\,
\delta\!\left(\rnm(\Ph_{N+1})-\rnm^{\cut}\right).
\label{eq:boundary-expansion}
\end{equation}
At fixed order this migration belongs to $\Delta_{\rm kin}$ and can be included in the correlated P2B
restoration.  If no such lower boundary is part of the process definition, this term is absent; the separate
requirement of reproducing the differential $\rnm$ spectrum remains.

''' + bad_block + r'''

The counterexample above also explains why the higher $\rnp^{\cut}$ projection must not be imported into the
fixed-order nesting discussion.  As long as $\Pi_{N+1}$ is used only inside the add--subtract organization of
the exact NLO $(N+1)$ contribution, its auxiliary map dependence cancels.  The stronger simultaneous-limit
condition derived in Sec.~\ref{subsec:uniform-nested-locality} becomes physically relevant only when the
projected configuration is retained as an event, not when it is merely an internal subtraction coordinate.

'''

# Insert fixed-order section immediately before the summary.
if t.count(summary) != 1:
    raise SystemExit('Summary marker not unique after edits')
isum = t.index(summary)
t = t[:isum] + fixed_section + t[isum:]

# 7. Replace the summary with one organized by the three different problems.
isum = t.index(summary)
enddoc = r'\end{document}'
if t.count(enddoc) != 1:
    raise SystemExit('end document marker not unique')
ie = t.index(enddoc, isum)
new_summary = r'''\section{Summary: three distinct uses of cuts and projections}

The main conclusions are most clearly organized by separating three applications.

\begin{enumerate}
\item \textbf{NNLO LHE event definition.}
The higher separation $\rnp^{\cut}$ sits inside a dynamically exact NLO $(N+1)$ contribution.  It generates
no fixed-order LP truncation.  A residual dependence appears only when exact $\Ph_{N+2}$ kinematics below the
cut are replaced by a projected $\widehat\Ph_{N+1}$ configuration that is retained as the physical LHE event.
The relevant questions are then uniform nested locality of $\Pi_{N+1}$, migration of Born-like variables
$X_i$, and nonuniform observable response near shoulders, jet-clustering boundaries or fiducial cuts.

\item \textbf{Pure fixed-order NNLO slicing.}
The lower cut $\rn^{\cut}$ does introduce a genuine LP approximation below the cut.  Its error naturally
splits into a dynamical part and a kinematic part,
\[
\Delta_{\rm slice}^{(\rn)}
=
\Delta_{\rm dyn}^{(\rn)}+
\Delta_{\rm kin}^{(\rn)}.
\]
The kinematic part is the loss of exact measurement dependence under the lower projection and can be restored
with a correlated P2B construction.  The dynamical part is the missing subleading-power QCD contribution to
the LP factorization theorem and cannot be reconstructed by P2B.

\item \textbf{A sliced NNLO calculation embedded in an $\mathrm{N}^3\mathrm{LO}$ slicing calculation.}
The outer calculation requires the NNLO ingredient differential in $\rnm$ and in the Born-like variables.
The internal cut that can contaminate this lower singular spectrum is $\rn^{\cut}$, the lower-multiplicity cut
of the embedded NNLO calculation.  In a strongly ordered nested region the relevant parameters can be
$\rn^{\cut}/\rnm$ and, near the outer boundary, $\rn^{\cut}/\rnm^{\cut}$.  Kinematic contamination can be
removed by P2B; genuine dynamical contamination remains and must be controlled by the inner cut or by
subleading-power information.  The still higher $\rnp^{\cut}$ used only inside the exact NLO component is not
an additional fixed-order nesting error.
\end{enumerate}

The same projection map can therefore be perfectly adequate as an auxiliary fixed-order subtraction map and
yet be inadequate as a physical LHE event map.  Conversely, restoring exact kinematics with P2B can remove
all projection-induced kinematic power corrections at fixed order without curing the genuinely dynamical
power corrections of the slicing expansion.  Keeping these distinctions explicit is essential when several
nested resolution variables are used in GENEVA.

'''
t = t[:isum] + new_summary + t[ie:]

# 8. Update purpose/scope to flag the fixed-order distinction from the beginning.
old_scope = r'''\item genuine leading-power (LP) approximations in the lower-multiplicity NNLO contribution,
\item kinematic effects induced by phase-space projections in the MC event definition,
\item locality requirements on the projection maps for distributions differential in lower resolution variables,
\item fiducial power corrections that can be restored at fixed order through projection-to-Born constructions,
\item and additional constraints induced by optional Born-level fiducial or generation cuts.'''
new_scope = r'''\item genuine leading-power (LP) approximations generated by slicing cuts in pure fixed-order calculations,
\item kinematic effects induced specifically by replacing exact configurations with projected LHE events,
\item locality requirements needed when one sliced fixed-order calculation is embedded inside another,
\item kinematic and fiducial power corrections that can be restored at fixed order through projection-to-Born constructions,
\item genuine dynamical power corrections that cannot be restored by projection-to-Born,
\item and additional constraints induced by optional Born-level fiducial or generation cuts.'''
if old_scope not in t:
    raise SystemExit('Purpose/scope list not found')
t = t.replace(old_scope, new_scope, 1)

# Basic structural guards.
if r'\section{Lower-map locality and nested consistency before NNLO observables}' in t:
    raise SystemExit('Old lower-map section survived')
if t.count(r'\section{From the lower singular spectrum to NNLO LHE observables}') != 1:
    raise SystemExit('New LHE NNLO section count wrong')
if t.count(r'\section{Pure fixed-order slicing and nested sliced calculations}') != 1:
    raise SystemExit('New fixed-order section count wrong')
if t.count(r'\label{eq:nnlo-lp-replacement}') != 1:
    raise SystemExit('Duplicate or missing nnlo LP label')
if t.count(r'\label{eq:p2b-fpc-correlated}') != 1:
    raise SystemExit('Duplicate or missing P2B label')

p.write_text(t)
print('Reorganized note into LHE-specific NNLO and pure fixed-order slicing layers.')
