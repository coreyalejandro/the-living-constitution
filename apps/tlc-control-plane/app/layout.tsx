import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TLC control plane",
  description:
    "Governance control-plane shell for TLC — static scaffold; see README for status.",
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
