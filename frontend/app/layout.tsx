import type { Metadata } from "next";
import { Inter } from "next/font/google";

import "./globals.css";

import NavbarWrapper from "@/components/layout/NavbarWrapper";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "H2V-Trust | Blockchain Green Hydrogen Certification",
  description: "Plataforma de rastreabilidade blockchain para hidrogênio verde - Conformidade CBAM 2026",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <head>
        <link href="https://fonts.cdnfonts.com/css/rawline" rel="stylesheet" />
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway:300,400,500,600,700,800,900&display=swap" />
      </head>
      <body className={inter.className}>
        <NavbarWrapper />
        <main>{children}</main>
      </body>
    </html>
  );
}
