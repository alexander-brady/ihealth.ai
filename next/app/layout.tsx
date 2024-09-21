import type { Metadata } from "next";
import { Roboto, Source_Serif_4 } from "next/font/google";
import "./globals.css";

const roboto = Roboto({
  style: ["normal", "italic"],
  subsets: ["latin"],
  variable: "--font-roboto",
  weight: ["100", "300", "400", "500", "700", "900"],
});

const sourceSerif = Source_Serif_4({
  style: ["normal", "italic"],
  subsets: ["latin"],
  variable: "--font-source-serif",
  weight: ["300", "400", "500", "700", "900"],
});

export const metadata: Metadata = {
  title: "iHealth.Ai",
  description: "Penn Apps project name",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${roboto.variable} ${sourceSerif.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
