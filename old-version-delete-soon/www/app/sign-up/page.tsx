import Link from "next/link";
import { signUpAction } from "../_lib/actions";
interface SignUpPageProps {
  searchParams: Record<string, string | string[] | undefined>;
}
export default function SignUpPage({ searchParams }: SignUpPageProps) {
  const { errors } = searchParams;
  return (
    <main className="flex">
      <form
        className="border flex flex-col gap-5 border-white px-20 py-10"
        action={signUpAction}
      >
        <h1 className="text-3xl mb-5 text-white">Sign Up</h1>
        <div className="flex flex-col gap-2">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            className="px-4 py-2 border border-white text-black"
            name="email"
            type="email"
          />
        </div>
        <div className="flex flex-col gap-2">
          <label htmlFor="pass">Password</label>
          <input
            id="pass"
            className="px-4 py-2 border border-white text-black"
            name="pass"
            type="password"
          />
        </div>
        <button className="px-4 py-2 border border-white">Sign Up</button>
        {errors?.length ? (
          <div className="flex flex-col items-center justify-center gap-2">
            <p className="text-red-500">{errors}</p>
            <Link href="/login" className="underline">
              Login
            </Link>
          </div>
        ) : null}
      </form>
    </main>
  );
}
