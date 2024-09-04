import Link from "next/link";
import { loginAction } from "../_lib/actions";
interface LoginPageProps {
  searchParams: Record<string, string | string[] | undefined>;
}
export default function LoginPage({ searchParams }: LoginPageProps) {
  const { errors, success } = searchParams;
  return (
    <main className="flex">
      <form
        className="border flex flex-col gap-5 border-white px-20 py-10"
        action={loginAction}
      >
        <h1 className="text-3xl mb-5 text-white">Login</h1>
        {success?.length ? (
          <p className="text-green-500 text-center">{success}</p>
        ) : null}
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
        <button className="px-4 py-2 border border-white">Login</button>
        {errors?.length ? (
          <div className="flex flex-col items-center justify-center gap-2">
            <p className="text-red-500">{errors}</p>
            <Link href="/sign-up" className="underline">
              Sign Up
            </Link>
          </div>
        ) : null}
      </form>
    </main>
  );
}
