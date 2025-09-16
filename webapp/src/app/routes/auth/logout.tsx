import { redirect } from "react-router";

export async function loader() {
  const headers = new Headers();
  headers.append(
    "Set-Cookie",
    "access_token=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0"
  );

  return redirect("/", { headers });
}

export default function Logout() {
  return null;
}
