import type { ReactNode } from "react";

type Props = {
  children: ReactNode;
};

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
