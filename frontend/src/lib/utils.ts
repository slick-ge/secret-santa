import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getBaseUrl() {
  if (typeof window !== "undefined") return "";
  if (process.env.BASE_URL) return `https://${process.env.BASE_URL}`;
  return "http://localhost:3000";
}

export function getApiUrl() {
  if (typeof window !== "undefined") return "";
  if (process.env.API_URL) return `https://${process.env.API_URL}`;
  return "http://localhost:8080";
}

export function getApiUrlWithPath(path: string) {
  return `${getApiUrl()}/${path}`;
}
