import Link from "next/link";
import { getAuth } from "./_lib/actions";
import { redirect } from "next/navigation";
export default async function Home() {
  const auth = await getAuth();
  if (auth) {
    redirect("/dashboard");
  }
  return (
    <main className="flex flex-col gap-5">
      <Link className="px-4 py-2 border border-white text-center" href="/login">
        Login
      </Link>
      <Link
        className="px-4 py-2 border border-white text-center"
        href="/sign-up"
      >
        Sign Up
      </Link>
    </main>
  );
}
