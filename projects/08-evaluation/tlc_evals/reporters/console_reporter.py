"""
Console Reporter — rich terminal output for interactive eval runs.

Uses `rich` for styled output. Falls back to plain text if rich is unavailable.
"""

from __future__ import annotations

from tlc_evals.core.types import EvalSummary, EvalResult, Verdict, Severity

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
    _RICH = True
except ImportError:
    _RICH = False


_VERDICT_COLORS = {
    Verdict.PASS: "green",
    Verdict.FAIL: "red",
    Verdict.FLAGGED: "yellow",
    Verdict.ERROR: "bold red",
    Verdict.SKIP: "dim",
}

_VERDICT_SYMBOLS = {
    Verdict.PASS: "✓",
    Verdict.FAIL: "✗",
    Verdict.FLAGGED: "⚑",
    Verdict.ERROR: "⚠",
    Verdict.SKIP: "–",
}


class ConsoleReporter:
    """Rich terminal reporter for interactive eval runs."""

    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose
        self._console = Console() if _RICH else None

    def print(self, summary: EvalSummary) -> None:
        if _RICH and self._console:
            self._print_rich(summary)
        else:
            self._print_plain(summary)

    def _print_rich(self, summary: EvalSummary) -> None:
        console = self._console
        assert console is not None

        # Header
        status_color = (
            "green" if summary.pass_rate >= 0.9
            else "yellow" if summary.pass_rate >= 0.7
            else "red"
        )
        header = (
            f"[bold]TLC Eval Run[/bold] — {summary.eval_suite_name}\n"
            f"Model: {summary.model_id} | "
            f"[{status_color}]{summary.passed}/{summary.total} passed "
            f"({summary.pass_rate:.1%})[/{status_color}] | "
            f"Mean score: {summary.mean_score:.3f}"
        )
        console.print(Panel(header, border_style="blue"))

        # Results table
        table = Table(box=box.MINIMAL_HEAVY_HEAD, show_lines=False)
        table.add_column("Case", style="dim", width=16)
        table.add_column("Eval", width=24)
        table.add_column("Verdict", width=10)
        table.add_column("Score", justify="right", width=7)
        table.add_column("Violations", width=8)
        if self.verbose:
            table.add_column("Explanation", width=50)

        for r in summary.results:
            color = _VERDICT_COLORS.get(r.verdict, "white")
            symbol = _VERDICT_SYMBOLS.get(r.verdict, "?")
            row = [
                r.case_id,
                r.eval_name,
                f"[{color}]{symbol} {r.verdict.value}[/{color}]",
                f"{r.score:.3f}",
                str(len(r.violations)),
            ]
            if self.verbose:
                row.append(r.explanation[:60] + "…" if len(r.explanation) > 60 else r.explanation)
            table.add_row(*row)

        console.print(table)

        # Violations by invariant
        if summary.by_invariant:
            console.print("\n[bold]Violations by invariant:[/bold]")
            for inv, count in sorted(summary.by_invariant.items(), key=lambda x: -x[1]):
                bar = "█" * min(count, 20)
                console.print(f"  {inv:3s} [{count:3d}] {bar}")

        # Failure type breakdown
        if summary.by_failure_type:
            console.print("\n[bold]By failure type:[/bold]")
            for ft, counts in sorted(summary.by_failure_type.items()):
                total = sum(counts.values())
                passed = counts.get("pass", 0)
                color = "green" if passed == total else "yellow" if passed > 0 else "red"
                console.print(
                    f"  {ft}: [{color}]{passed}/{total}[/{color}] passed"
                )

    def _print_plain(self, summary: EvalSummary) -> None:
        print(f"\nTLC Eval Run: {summary.eval_suite_name}")
        print(f"  Model:   {summary.model_id}")
        print(f"  Passed:  {summary.passed}/{summary.total} ({summary.pass_rate:.1%})")
        print(f"  Score:   {summary.mean_score:.3f}")
        print()

        for r in summary.results:
            sym = _VERDICT_SYMBOLS.get(r.verdict, "?")
            print(f"  {sym} [{r.case_id:12s}] {r.verdict.value:8s}  score={r.score:.3f}  v={len(r.violations)}")

        if summary.by_invariant:
            print("\nViolations by invariant:")
            for inv, count in sorted(summary.by_invariant.items()):
                print(f"  {inv}: {count}")
