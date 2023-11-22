import { redirect } from "next/navigation";
import { getAuth, getUser, logOut } from "../_lib/actions";
export default async function DashboardPage() {
  const auth = await getAuth();
  const user = await getUser();
  if (!auth || !user) {
    redirect("/");
  }
  return (
    <main className="flex flex-col gap-5 items-center">
      <form action={logOut}>
        <button className="px-4 py-2 border border-white">Log Out</button>
      </form>
      <p>super secret dashboard</p>
      <p>hello {user.email}</p>
    </main>
  );
}
