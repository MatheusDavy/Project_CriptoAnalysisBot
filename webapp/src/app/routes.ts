import { type RouteConfig, route, index, layout,  } from "@react-router/dev/routes";

export default [
  // Auth
  index("routes/auth/login.tsx"),
  route("/logout" ,"routes/auth/logout.tsx"),

  // Dashboard
  layout("routes/dashboard/_layout.tsx", [
    route("/dashboard", "routes/dashboard/home/page.tsx"),
    route("/dashboard/settings", "routes/dashboard/settings/page.tsx"),
    route("/dashboard/chart", "routes/dashboard/chart/page.tsx"),
    route("/dashboard/operations", "routes/dashboard/operations/page.tsx"),
  ]),

  route("/not-found" ,"routes/not-found.tsx")

] satisfies RouteConfig;
