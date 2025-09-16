import { redirect } from "react-router";
import jwt from "jsonwebtoken";

export function verifyToken(token?: string) {
  if (!token) return false;

  try {
    const data = jwt.verify(token, process.env.JWT_SECRET!);
    return data.sub === process.env.JWT_SUB!
  } catch (err) {
    return false;
  }
}

export async function authMiddleware({
  request,
  type = "private",
}: {
  request: Request;
  type?: "private" | "public";
}) {
  const cookieHeader = request.headers.get("cookie") || "";
  const cookies = Object.fromEntries(
    cookieHeader
      .split(";")
      .map(c => c.trim().split("="))
      .map(([k, v]) => [k, decodeURIComponent(v)])
  );

  const token = cookies["access_token"];

  const isAuth = Boolean(token && verifyToken(token));

  if (type === "private" && !isAuth) {
    throw redirect("/");
  }

  if (type === "public" && isAuth) {
    throw redirect("/dashboard/operations");
  }

  return null;
}
