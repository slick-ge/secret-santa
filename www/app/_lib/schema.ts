import { z } from "zod";
export const userSchema = z.object({
  email: z.string().email(),
  pass: z.string().min(6),
});
