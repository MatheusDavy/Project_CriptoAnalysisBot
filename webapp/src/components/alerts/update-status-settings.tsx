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
import { ToggleLeft } from "lucide-react";

type Props = {
  status: boolean;
  onConfirm?: () => void;
};

export function UpdateStatusSettingsAlert({ status, onConfirm }: Props) {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <DropdownMenuItem variant={status ? 'error' : 'success'} onSelect={(e) => e.preventDefault()}>
          <ToggleLeft />
          {status ? "Disabled" : "Abble"}
        </DropdownMenuItem>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>
            {status
              ? "Do you really want to disable these settings?"
              : "Do you want to enable these settings?"
            }
          </DialogTitle>
          <DialogDescription>
            {status
              ? "Disabling will prevent these settings from being used. You can enable them again later."
              : "Enabling will make these settings active and available for use."
            }
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
