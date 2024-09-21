'use client';

import { useState } from "react";

interface DropDownMenuProps{
  question: string,
  answer: string,

}

export default function DropDownMenu(){

  const [showDropdown, setShowDropdown] = useState(false);

  const Callback = () => {
    setShowDropdown((prev) => !prev);
  }

  return(
    <div>
      
    </div>
  );
}