import { ModeToggle } from "@/components/mode-toggle";
import { siteConfig } from "@/config/site";
import Link from "next/link";
import { Icons } from "./icons";

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/70 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex items-center justify-between h-14 container mx-auto">
        <SiteLogo />
        <div className="flex items-center gap-4">
          <div className="size-8 rounded-full border bg-muted">u</div>
          <ModeToggle />
        </div>
      </div>
    </header>
  );
}

function SiteLogo() {
  return (
    <Link href="/" className="flex items-center space-x-2">
      <Icons.logo className="h-6 w-6" />
      <span className="hidden font-bold lg:inline-block">
        {siteConfig.name}
      </span>
    </Link>
  );
}
