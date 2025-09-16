import { HomeView } from "components/view/home";
import type { MetaArgs } from "react-router";

export function meta({}: MetaArgs) {
  return [
    { title: "Cripto Agent | Dashboard" },
  ];
}

export default function Home() {
  return <HomeView />;
}
