import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Revix - Failed Payment Recovery",
  description: "AI-powered failed payment recovery workflows for subscription businesses."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
