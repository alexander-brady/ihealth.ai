import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import {AuthProvider} from "@propelauth/nextjs/client";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
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
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <AuthProvider authUrl={process.env.NEXT_PUBLIC_AUTH_URL}>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
