import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "FoodieBot",
  description: "Restaurant reviews and diet plans",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gray-50 text-black`}>
        {/* Global Navigation Bar */}
        <nav className="bg-white shadow-sm border-b border-gray-100 sticky top-0 z-50">
          <div className="max-w-5xl mx-auto px-8 py-4 flex justify-between items-center">
            <Link href="/" className="text-2xl font-extrabold text-orange-600 tracking-tight">
              🍔 FoodieBot
            </Link>
            <div className="flex gap-6">
              <Link href="/" className="text-gray-600 hover:text-orange-600 font-medium transition">
                Search Restaurants
              </Link>
              <Link href="/diet-plan" className="text-gray-600 hover:text-orange-600 font-medium transition">
                DietAdvisor
              </Link>
            </div>
          </div>
        </nav>

        {/* This is where your page content renders */}
        {children}
      </body>
    </html>
  );
}