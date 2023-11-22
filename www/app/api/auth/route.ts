import { getUsers } from "@/app/_lib/db";
import { userSchema } from "@/app/_lib/schema";
import { NextResponse } from "next/server";
export async function POST(req: Request) {
  const json = await req.json();
  const parsed = userSchema.parse(json);
  const users = getUsers();
  const success = users.some(
    (user) => user.email === parsed.email && user.pass === parsed.pass,
  );
  return NextResponse.json({ success });
}
