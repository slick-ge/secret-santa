import { siteConfig } from "@/config/site";

export function SiteFooter() {
  return (
    <footer className="w-full">
      <div className="flex items-center container mx-auto">
        <p className="text-sm text-muted-foreground">
          Copyright &copy; {new Date().getFullYear()} {siteConfig.name}
        </p>
      </div>
    </footer>
  );
}
