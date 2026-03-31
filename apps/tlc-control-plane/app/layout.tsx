import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TLC AI Governance System — control plane",
  description:
    "Subordinate control-plane UI for The Living Constitution — reads repo artifacts; STATUS.json is authoritative.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
