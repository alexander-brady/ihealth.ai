import type { Metadata } from "next";
import { Roboto, Source_Serif_4 } from "next/font/google";
import "./globals.css";
import {AuthProvider} from "@propelauth/nextjs/client";

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
  title: "iHealth.ai",
  description: "Your friendly healthcare assistant",
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
        <AuthProvider authUrl={process.env.NEXT_PUBLIC_AUTH_URL!}>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
