'use client';

import LandingNav from "./components/nav/landingNav";
import MobileNav from "./components/nav/mobileNav";

export default function Home() {
  return (
    <div>
      <LandingNav />
      <MobileNav />
    </div>
  );
}
