"use client";

import { DataTable, type CustomColumnDef } from "components/ui/data-table";
import type { ColumnDef } from "@tanstack/react-table";
import { Badge } from "components/ui/badge";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "components/ui/dropdown-menu";
import { EllipsisVertical, SquarePen } from "lucide-react";
import { Button } from "components/ui/button";
import { DeleteSettingsAlert } from "components/alerts/delete-settings";
import {
  deleteSettings,
  listSettings,
  updateSettings,
  type ListSettingsTypes,
} from "http/settings";
import {
  candlePatterns,
  currencies,
  gainTargets,
  indicators,
  timeFrames,
  timeRanges,
} from "types/settings";
import { useMutation, useQuery } from "@tanstack/react-query";
import { Navigate } from "react-router";
import { toast } from "sonner";
import type { ErrorResponse } from "types/api";
import { errors } from "types/errors";
import { UpdateStatusSettingsAlert } from "components/alerts/update-status-settings";
import { Separator } from "components/ui/separator";

type Props = {
  onEdit: (id: string) => void;
};

export function TableSettings({ onEdit }: Props) {
  const {
    data = [],
    isPending,
    isError,
    refetch,
  } = useQuery({
    queryKey: ["settings"],
    queryFn: listSettings,
  });

  const { mutate: onDelete } = useMutation({
    mutationFn: deleteSettings,
    onSuccess: () => {
      toast.warning("Settings was delete", {
        description: "Your settings was delete succesfuly",
      });
      refetch();
    },
    onError: () => {
      toast.error("Erro to delete", {
        description: "A unespected error occured",
      });
    },
  });

  const { mutate: onUpdateStatus } = useMutation({
    mutationFn: updateSettings,
    onSuccess: () => {
      toast.success("Success", {
        description: "Status was updated",
      });
      refetch();
    },
    onError: (e: ErrorResponse) => {
      toast.error("Error", {
        description: errors[e?.error],
      });
    },
  });

  const columns: CustomColumnDef<ListSettingsTypes[number]>[] = [
    {
      accessorKey: "name",
      header: "Settings",
      customization: {
        rowClassName: (row) => (row.status ? "bg-green-700/2" : "bg-red-700/2"),
      },
    },
    {
      accessorKey: "currencies",
      header: "Currency Pair",
      cell: ({ row }) => {
        const values = row.getValue<string[]>("currencies");
        return (
          <div className="flex items-center flex-wrap gap-1">
            {values?.map((item, key) => {
              const currency = currencies.find((cr) => cr.value === item);
              return (
                <Badge variant="accent" key={key}>
                  {currency?.label}
                </Badge>
              );
            })}
          </div>
        );
      },
    },
    {
      accessorKey: "timeranges",
      header: () => <div className="mx-auto text-center">Timeranges</div>,
      cell: ({ row }) => {
        const values = row.getValue<string[]>("timeranges");
        return (
          <div className="flex justify-center items-center flex-wrap gap-1">
            {values?.map((item, key) => {
              const timerange = timeRanges.find((cr) => cr.value === item);
              return (
                <Badge variant="contrast-1" key={key}>
                  {timerange?.label}
                </Badge>
              );
            })}
          </div>
        );
      },
    },
    {
      accessorKey: "timeframes",
      header: () => <div className="mx-auto text-center">Timeframes</div>,
      cell: ({ row }) => {
        const values = row.getValue<string[]>("timeframes");
        return (
          <div className="flex justify-center items-center gap-1">
            {values?.map((item, key) => {
              const timeframe = timeFrames.find((cr) => cr.value === item);
              return (
                <Badge variant="contrast-2" key={key}>
                  {timeframe?.label}
                </Badge>
              );
            })}
          </div>
        );
      },
    },
    {
      accessorKey: "indicators",
      header: () => <div className="mx-auto">Indicadores</div>,
      cell: ({ row }) => {
        const values = row.getValue<string[]>("indicators");
        return (
          <div className="flex items-center flex-wrap gap-1">
            {values?.map((item, key) => {
              const indicator = indicators.find((cr) => cr.value === item);
              return (
                <Badge variant="default" key={key}>
                  {indicator?.label}
                </Badge>
              );
            })}
          </div>
        );
      },
    },
    {
      accessorKey: "candle_patterns",
      header: () => <div className="mx-auto">Candle Patterns</div>,
      cell: ({ row }) => {
        const values = row.getValue<string[]>("candle_patterns");
        return (
          <div className="flex items-center flex-wrap gap-1">
            {values?.map((item, key) => {
              const candles = candlePatterns.find((cr) => cr.value === item);
              return (
                <Badge variant="outline" key={key}>
                  {candles?.label}
                </Badge>
              );
            })}
          </div>
        );
      },
    },
    {
      accessorKey: "min_confluence",
      header: () => <div className="mx-auto text-center">Min Confluence</div>,
      cell: ({ row }) => {
        return (
          <div className="flex text-center justify-center mx-auto">
            <Badge variant={"outline"}>
              {row.getValue("min_confluence") || "-"}
            </Badge>
          </div>
        );
      },
    },
    {
      accessorKey: "gain_target",
      header: () => <div className="mx-auto text-center">Gain Target</div>,
      cell: ({ row }) => {
        const values =
          row.getValue<{ type: string; value: string }[]>("gain_target");
        return (
          <div className="flex justify-center items-center flex-wrap gap-1">
            {values?.map((item, key) => {
              const target = gainTargets.find((cr) => cr.value === item?.type);
              return (
                <Badge variant="success" key={key}>
                  {item.value} {target?.label}
                </Badge>
              );
            })}
          </div>
        );
      },
    },
    {
      accessorKey: "loss_target",
      header: () => <div className="mx-auto text-center">Loss Target</div>,
      cell: ({ row }) => {
        const values =
          row.getValue<{ type: string; value: string }[]>("loss_target");
        return (
          <div className="flex justify-center items-center gap-1">
            {values?.map((item, key) => {
              const target = gainTargets.find((cr) => cr.value === item?.type);
              return (
                <Badge variant="error" key={key}>
                  {item.value} {target?.label}
                </Badge>
              );
            })}
          </div>
        );
      },
    },
    {
      accessorKey: "actions",
      header: () => <div />,
      cell: ({ row }) => {
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon">
                <EllipsisVertical />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem
                variant="default"
                onClick={() => {
                  onEdit(row.original.id);
                }}
              >
                <SquarePen />
                Edit
              </DropdownMenuItem>
              <UpdateStatusSettingsAlert
                status={row.original.status}
                onConfirm={() =>
                  onUpdateStatus({
                    id: row.original.id as string,
                    status: !row.original.status,
                  })
                }
              />
              <Separator />
              <DeleteSettingsAlert
                onConfirm={() => onDelete(row.original.id as string)}
              />
            </DropdownMenuContent>
          </DropdownMenu>
        );
      },
    },
  ];

  if (isError) {
    return <Navigate to="/not-found" />;
  }

  return <DataTable data={data} isLoading={isPending} columns={columns} />;
}
