import { ChartView } from "components/view/chart";
import type { MetaArgs } from "react-router";

export function meta({}: MetaArgs) {
  return [
     { title: "Cripto Agent | Chart" },
  ];
}

export default function Chart() {
  return <ChartView />;
}
