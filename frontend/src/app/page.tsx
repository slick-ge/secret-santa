import { buttonVariants } from "@/components/ui/button";
import { siteConfig } from "@/config/site";
import Link from "next/link";

export default function Home() {
  return (
    <main className="container mx-auto flex flex-col min-h-[calc(100dvh-7rem)] py-10">
      <section className="flex items-center justify-center pt-32">
        <div className="text-center flex flex-col items-center gap-14">
          <h1 className="text-6xl font-bold">Welcome to {siteConfig.name}</h1>

          <Link className={buttonVariants({ size: "lg" })} href="/dashboard">
            Get Started
          </Link>
        </div>
      </section>
    </main>
  );
}
