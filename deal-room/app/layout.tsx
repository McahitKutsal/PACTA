import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "The Deal Room",
  description: "A short negotiation game — a research study comparing how people and AIs handle promises and trust.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>{children}</body>
    </html>
  );
}
