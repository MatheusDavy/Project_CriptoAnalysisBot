import type { ColumnDef } from "@tanstack/react-table";
import { cn } from "lib/utils";
import { Badge } from "components/ui/badge";

export type CriptoOperations = {
  id: string;
  name: string;
  entry_price: number;
  percentage_operation: number;
  leverage: number;
  status: "open" | "success" | "failed";
  timeframe: string;
};

export const mockCriptoOperations: CriptoOperations[] = [
  {
    id: "1",
    name: "Bitcoin",
    entry_price: 25600,
    percentage_operation: 2.5,
    leverage: 10,
    status: "open",
    timeframe: "1h",
  },
  {
    id: "2",
    name: "Ethereum",
    entry_price: 1650,
    percentage_operation: -1.2,
    leverage: 20,
    status: "success",
    timeframe: "4h",
  },
  {
    id: "3",
    name: "BNB",
    entry_price: 310,
    percentage_operation: 3.8,
    leverage: 15,
    status: "failed",
    timeframe: "15m",
  },
  {
    id: "4",
    name: "Cardano",
    entry_price: 0.27,
    percentage_operation: 0.5,
    leverage: 5,
    status: "success",
    timeframe: "1d",
  },
  {
    id: "5",
    name: "Solana",
    entry_price: 21.5,
    percentage_operation: -0.8,
    leverage: 25,
    status: "open",
    timeframe: "5m",
  },
  {
    id: "6",
    name: "XRP",
    entry_price: 0.5,
    percentage_operation: 4.1,
    leverage: 10,
    status: "success",
    timeframe: "1h",
  },
  {
    id: "7",
    name: "Dogecoin",
    entry_price: 0.073,
    percentage_operation: -2.3,
    leverage: 30,
    status: "failed",
    timeframe: "30m",
  },
  {
    id: "8",
    name: "Polygon",
    entry_price: 0.68,
    percentage_operation: 1.7,
    leverage: 20,
    status: "open",
    timeframe: "4h",
  },
  {
    id: "9",
    name: "Avalanche",
    entry_price: 12.4,
    percentage_operation: -1.9,
    leverage: 50,
    status: "failed",
    timeframe: "15m",
  },
  {
    id: "10",
    name: "Litecoin",
    entry_price: 68,
    percentage_operation: 2.9,
    leverage: 10,
    status: "success",
    timeframe: "1d",
  },
];

export const columns: ColumnDef<CriptoOperations>[] = [
  {
    accessorKey: "name",
    header: "Criptomoeda",
  },
  {
    accessorKey: "entry_price",
    header: "Preço de Entrada",
    cell: ({ row }) => {
      const value = row.getValue<number>("entry_price");
      return <span>${value}</span>;
    },
  },
  {
    accessorKey: "percentage_operation",
    header: () => <div className="mx-auto text-center">Percent</div>,
    cell: ({ row }) => {
      const value = row.getValue<number>("percentage_operation");
      const color = value >= 0 ? "text-green-600" : "text-red-600";
      return (
        <div className={cn(color, "text-center")}>{value.toFixed(2)}%</div>
      );
    },
  },
  {
    accessorKey: "leverage",
    header: () => <div className="mx-auto text-center">Multiply</div>,
    cell: ({ row }) => {
      const value = row.getValue<number>("leverage");
      return <div className="text-center">{value}x</div>;
    },
  },
  {
    accessorKey: "timeframe",
    header: () => <div className="mx-auto text-center">Timeframe</div>,
    cell: ({ row }) => {
      const value = row.getValue<number>("timeframe");
      return <div className="text-center">{value}</div>;
    },
  },
  {
    accessorKey: "status",
    header: () => <div className="mx-auto text-center">Status</div>,
    cell: ({ row }) => {
      const status = row.getValue<"open" | "success" | "failed">("status");

      const variant: Record<string, "accent" | "error" | "success"> = {
        open: "accent",
        failed: "error",
        success: "success",
      };

      return (
        <div className="flex">
          <Badge variant={variant[status]} size="sm" className="mx-auto">
            {status}
          </Badge>
        </div>
      );
    },
  },
];
