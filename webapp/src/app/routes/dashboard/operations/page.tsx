import { DataTable } from "components/ui/data-table";
import { columns, mockCriptoOperations } from "./types.d";
import type { MetaArgs } from "react-router";

export function meta({}: MetaArgs) {
  return [
    { title: "Cripto Agent | Operations" },
  ];
}

export default function Operations () {
  return (
    <div className="flex flex-col space-y-5 w-full">
      <h1 className="text-2xl font-bold">Operations</h1>

      <DataTable data={mockCriptoOperations} columns={columns} />
    </div>
  );
}