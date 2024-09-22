import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "@/components/ui/avatar"

import Logo from "../../public/Logo.png"

export function AvatarGPTIcon() {
  return (
    <Avatar>
      <AvatarImage src={Logo.src} alt="iHealth.ai Icon" />
      <AvatarFallback>CN</AvatarFallback>
    </Avatar>
  )
}
