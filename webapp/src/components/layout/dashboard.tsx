import type { ReactNode } from "react";
import {
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
  SidebarTrigger,
  Sidebar,
  SidebarInset,
} from "components/ui/sidebar";
import {
  Bitcoin,
  ClipboardList,
  Home,
  Inbox,
  LogOut,
  Settings,
} from "lucide-react";
import { Separator } from "components/ui/separator";
import { cn } from "lib/utils";
import { Link, useLocation } from "react-router";
import { Button } from "components/ui/button";

type Props = {
  children: ReactNode;
};

export function DashboardLayout({ children }: Props) {
  return (
    <SidebarProvider defaultOpen={false}>
      <Sidebar variant="floating" collapsible="icon" className="h-screen w-64">
        <SidebarContent>
          <NavMain />
          <SidebarGroup className="flex-grow justify-end">
            <SidebarGroupContent>
              <SidebarMenuItem>
                <SidebarMenuButton asChild tooltip="Sair">
                  <Button
                    asChild
                    variant="error"
                    className="items-center justify-start gap-3"
                  >
                    <Link to="/logout">
                      <LogOut size={16} />
                      <span>Sair</span>
                    </Link>
                  </Button>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarGroupContent>
          </SidebarGroup>
        </SidebarContent>
      </Sidebar>
      <SidebarInset
        className={cn(
          "data-[content-layout=centered]:!mx-auto data-[content-layout=centered]:max-w-screen-2xl",
          "max-[113rem]:peer-data-[variant=inset]:!mr-2 min-[101rem]:peer-data-[variant=inset]:peer-data-[state=collapsed]:!mr-auto"
        )}
      >
        <header className="flex h-12 shrink-0 items-center gap-2 border-b transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12">
          <div className="flex w-full items-center justify-between px-4 lg:px-6">
            <div className="flex items-center gap-1 lg:gap-2">
              <SidebarTrigger className="-ml-1" />
              <Separator
                orientation="vertical"
                className="mx-2 data-[orientation=vertical]:h-4"
              />
            </div>
            <div className="flex items-center gap-2"></div>
          </div>
        </header>

        <div className="h-full p-4 md:p-6 max-w-full flex">{children}</div>
      </SidebarInset>
    </SidebarProvider>
  );
}

export function NavMain() {
  const groups = [
    {
      id: "main",
      label: "Main",
      items: [
        { title: "Home", url: "/dashboard", icon: Home },
        {
          title: "Operações",
          url: "/dashboard/operations",
          icon: ClipboardList,
        },
      ],
    },
    {
      id: "analysis",
      label: "Analysis",
      items: [
        { title: "Configurações", url: "/dashboard/settings", icon: Settings },
        { title: "Binance", url: "/dashboard/binance", icon: Bitcoin },
      ],
    },
  ];

  const location = useLocation();
  const path = location.pathname;

  const isItemActive = (url: string, subItems?: any) => {
    if (subItems?.length) {
      return subItems.some((sub: any) => path.startsWith(sub.url));
    }
    return path === url;
  };

  return (
    <>
      {groups.map((group) => (
        <SidebarGroup key={group.id}>
          {group.label && <SidebarGroupLabel>{group.label}</SidebarGroupLabel>}
          <SidebarGroupContent className="flex flex-col gap-2">
            <SidebarMenu>
              {group.items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild tooltip={item.title}>
                    <Button
                      asChild
                      variant={isItemActive(item.url) ? "accent" : "ghost"}
                      className="items-center justify-start gap-3"
                    >
                      <Link to={item.url}>
                        {item.icon && <item.icon />}
                        <span>{item.title}</span>
                      </Link>
                    </Button>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      ))}
    </>
  );
}
