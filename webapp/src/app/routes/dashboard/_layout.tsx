import { DashboardLayout } from "components/layout/dashboard";
import { authMiddleware } from "middleware/auth";
import { Outlet, type LoaderFunction } from "react-router";

export default function Layout() {
  return (
    <DashboardLayout>
      <Outlet />
    </DashboardLayout>
  );
}

export const loader: LoaderFunction = async ({ request }) => {
  return await authMiddleware({ request, type: "private" });
};
