import type { Route } from "../+types/_layout";
import { FormsSettings } from "./form";
import { useState } from "react";
import { TableSettings } from "./table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "components/ui/tabs";

export function meta({}: Route.MetaArgs) {
  return [{ title: "Cripto Agent | Settings" }];
}

export default function Settings() {
  const [idEdit, setIdEdit] = useState<string | undefined>();
  const [tabs, setTabs] = useState("TABLE");

  return (
    <div className="flex flex-col space-y-5 w-full">
      <h1 className="text-2xl font-bold">Settings</h1>

      <Tabs onValueChange={(value) => setTabs(value)} value={tabs}>
        <TabsList className="mb-5">
          <TabsTrigger value="TABLE">Created</TabsTrigger>
          <TabsTrigger value="FORMS">Forms</TabsTrigger>
        </TabsList>
        <TabsContent value="TABLE">
          <TableSettings
            onEdit={(id) => {
              setIdEdit(id);
              setTabs("FORMS");
            }}
          />
        </TabsContent>
        <TabsContent value="FORMS">
          <FormsSettings
            id={idEdit}
            onCancelEdit={() => {
              setTabs("TABLE");
              setIdEdit(undefined);
            }}
          />
        </TabsContent>
      </Tabs>
    </div>
  );
}
