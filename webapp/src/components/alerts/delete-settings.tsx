import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "components/ui/dialog";
import { Button } from "components/ui/button";
import { DropdownMenuItem } from "components/ui/dropdown-menu";
import { Trash } from "lucide-react";

type Props = {
  onConfirm?: () => void;
};

export function DeleteSettingsAlert({ onConfirm }: Props) {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <DropdownMenuItem variant="error" onSelect={e => e.preventDefault()}>
          <Trash />
          Excluir
        </DropdownMenuItem>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Are you absolutely sure?</DialogTitle>
          <DialogDescription>
            This action cannot be undone. This will permanently delete your
            settings, but will not affect your active trades.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <DialogClose asChild>
            <Button variant="outline">Cancel</Button>
          </DialogClose>
          <DialogClose asChild>
            <Button variant="error" onClick={onConfirm}>
              Continue
            </Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
