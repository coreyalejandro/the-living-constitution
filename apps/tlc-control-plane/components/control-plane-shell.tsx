import type { ReactNode } from "react";
import Link from "next/link";

type Props = {
  children: ReactNode;
};

const NAV_LINKS = [
  { href: "/", label: "Dashboard" },
  { href: "/research", label: "Research" },
  { href: "/experiments", label: "Experiments" },
  { href: "/evals", label: "Evals" },
  { href: "/evidence", label: "Evidence" },
  { href: "/corpus", label: "Corpus" },
  { href: "/improvement", label: "Improvement" },
];

export function ControlPlaneShell({ children }: Props) {
  return (
    <div className="mx-auto flex min-h-screen max-w-[1600px] flex-col gap-3 p-4">
      <header className="border-b border-zinc-800 pb-3">
        <h1 className="text-lg font-semibold tracking-tight text-zinc-100">
          TLC AI Governance System — control plane
        </h1>
        <p className="mt-1 text-sm text-zinc-500">
          Subordinate operational surface: renders approved repository artifacts.
          Not the system of record — STATUS.json remains authoritative.
        </p>
        <nav className="mt-3 flex flex-wrap gap-2" aria-label="Control plane navigation">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="rounded px-3 py-1 text-xs font-medium text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100 transition-colors"
            >
              {link.label}
            </Link>
          ))}
        </nav>
      </header>
      <main
        className="grid flex-1 grid-cols-1 gap-3 lg:grid-cols-2 lg:grid-rows-2"
        aria-label="TLC control plane panels"
      >
        {children}
      </main>
    </div>
  );
}
