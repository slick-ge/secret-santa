"use server";
import { cookies } from "next/headers";
import { userSchema } from "../_lib/schema";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { isRedirectError } from "next/dist/client/components/redirect";
import { ZodError } from "zod";
import { addUser, getUsers } from "./db";
export async function getAuth() {
  const cookieStore = cookies();
  const email = cookieStore.get("email")?.value;
  const pass = cookieStore.get("pass")?.value;
  const parsed = userSchema.safeParse({ email, pass });
  if (parsed.success) {
    const body = JSON.stringify(parsed.data);
    const res = (await fetch("http://localhost:3000/api/auth", {
      method: "post",
      body,
    }).then((res) => res.json())) as { success: boolean };
    return res.success;
  }
  return false;
}
export async function getUser() {
  const auth = await getAuth();
  const cookieStore = cookies();
  const email = cookieStore.get("email")?.value;
  if (auth && email) {
    return {
      email,
    };
  }
  return null;
}
export async function logOut() {
  const cookieStore = cookies();
  cookieStore.delete("email");
  cookieStore.delete("pass");
  revalidatePath("/dashboard");
}
export async function loginAction(fd: FormData) {
  "use server";
  try {
    const email = fd.get("email") as string;
    const pass = fd.get("pass") as string;
    const parsed = userSchema.parse({ email, pass });
    const users = getUsers();
    if (users.some((user) => user.email === email && user.pass === pass)) {
      const cookieStore = cookies();
      cookieStore.set("email", parsed.email);
      cookieStore.set("pass", parsed.pass);
      redirect("/dashboard");
    } else {
      redirect(`/login?errors=${encodeURIComponent("User does not exist")}`);
    }
  } catch (err) {
    if (isRedirectError(err)) {
      throw err;
    }
    if (err instanceof ZodError) {
      console.log(err);
      redirect(
        `/login?errors=${encodeURIComponent(
          JSON.stringify(err.flatten().fieldErrors),
        )}`,
      );
    } else {
      console.log(err);
      redirect(`/login?errors=${JSON.stringify(err)}`);
    }
  }
}
export async function signUpAction(fd: FormData) {
  "use server";
  try {
    const email = fd.get("email") as string;
    const pass = fd.get("pass") as string;
    const parsed = userSchema.safeParse({ email, pass });
    if (parsed.success) {
      const users = getUsers();
      if (users.every((user) => user.email !== email)) {
        addUser({ email, pass });
        redirect(
          `/login?success=${encodeURIComponent(
            "Successfully created a new user",
          )}`,
        );
      } else {
        redirect(
          `/sign-up?errors=${encodeURIComponent(
            "User with this email already exists",
          )}`,
        );
      }
    } else {
      redirect(`/sign-up?errors=${parsed.error.flatten().fieldErrors}`);
    }
  } catch (err) {
    if (isRedirectError(err)) {
      throw err;
    } else {
      console.error(err);
    }
  }
}
