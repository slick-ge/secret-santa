import Link from "next/link";
export default function Home() {
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
