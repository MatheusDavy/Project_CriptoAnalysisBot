import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "components/ui/form";
import { useLogic } from "./logic";
import { Button } from "components/ui/button";
import { Input } from "components/ui/input";
import { MultiSelect } from "components/ui/multi-select";
import {
  candlePatterns,
  currencies,
  gainTargets,
  indicators,
  lossTargets,
  timeFrames,
  timeRanges,
} from "types/settings";
import { Minus, Percent, Plus } from "lucide-react";
import { Select } from "components/ui/select";
import {
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "components/ui/select";
import { Loader } from "components/ui/loader";

type FormsSettingsProps = {
  id?: string;
  onCancelEdit: () => void;
};

export function FormsSettings({ id, onCancelEdit }: FormsSettingsProps) {
  const {
    form,
    gainFieldArray,
    lossFieldArray,
    isLoadingSetting,
    isLoadingCreate,
    isLoadingUpdate,
    methods,
  } = useLogic({ id, onCancelEdit });

  const handleCancel = () => {
    onCancelEdit();
    form.reset();
  };

  if (isLoadingSetting) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <Loader variant="progress" />
      </div>
    );
  }

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(methods.onSubmit)}
        className="space-y-6"
      >
        <div className="flex sm:flex-row flex-col gap-3 items-center justify-end">
          {id && (
            <Button
              variant="error"
              size="lg"
              type="button"
              className="w-full sm:w-auto"
              onClick={handleCancel}
            >
              Cancel
            </Button>
          )}
          <Button
            loading={isLoadingCreate || isLoadingUpdate}
            disabled={isLoadingCreate || isLoadingUpdate}
            size="lg"
            variant="accent"
            type="submit"
            className="w-full sm:w-auto"
          >
            {id ? "Update" : "Create"}
          </Button>
        </div>

        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Settings Name</FormLabel>
              <FormControl>
                <Input placeholder="Fibo + Candles" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
          <FormField
            control={form.control}
            name="currencies"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Currencies</FormLabel>
                <FormControl>
                  <MultiSelect
                    placeholder="Currencies"
                    value={field.value}
                    defaultValue={field.value}
                    onValueChange={field.onChange}
                    options={currencies}
                    searchable={false}
                    hideSelectAll={true}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="indicators"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Indicators</FormLabel>
                <FormControl>
                  <MultiSelect
                    placeholder="Indicators"
                    value={field.value}
                    defaultValue={field.value}
                    onValueChange={field.onChange}
                    options={indicators}
                    searchable={false}
                    hideSelectAll={true}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="candle_patterns"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Candle Patterns</FormLabel>
                <FormControl>
                  <MultiSelect
                    placeholder="Candle Patterns"
                    value={field.value}
                    defaultValue={field.value}
                    onValueChange={field.onChange}
                    options={candlePatterns}
                    searchable={false}
                    hideSelectAll={true}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          <FormField
            control={form.control}
            name="timeframes"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Time Frames</FormLabel>
                <FormControl>
                  <MultiSelect
                    placeholder="Time Frames"
                    value={field.value}
                    defaultValue={field.value}
                    onValueChange={field.onChange}
                    options={timeFrames}
                    searchable={false}
                    hideSelectAll={true}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="timeranges"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Time Frames</FormLabel>
                <FormControl>
                  <MultiSelect
                    placeholder="Time Ranges"
                    value={field.value}
                    defaultValue={field.value}
                    onValueChange={field.onChange}
                    options={timeRanges}
                    searchable={false}
                    hideSelectAll={true}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
        <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
          <FormField
            control={form.control}
            name="min_confluence"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Min Confluence</FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    type="number"
                    placeholder="Confluence"
                    onChange={(e) => {
                      const value = Number(e.target.value);
                      field.onChange(value);
                    }}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <div className="space-y-2">
            <FormLabel className="flex items-center">Gain Targets</FormLabel>
            {gainFieldArray.map((field, index) => (
              <div
                key={field.id}
                className="grid grid-cols-[1fr_auto] gap-2 items-center"
              >
                <div className="grid grid-cols-[1fr_auto] gap-1 items-center">
                  <FormField
                    control={form.control}
                    name={`gain_target.${index}.value`}
                    render={({ field }) => (
                      <FormItem>
                        <FormControl>
                          <Input
                            {...field}
                            type="number"
                            placeholder="20"
                            onChange={(e) => {
                              const value = Number(e.target.value);
                              field.onChange(value);
                            }}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={form.control}
                    name={`gain_target.${index}.type`}
                    render={({ field }) => (
                      <FormItem className="flex-1">
                        <FormControl>
                          <Select
                            value={field.value}
                            onValueChange={field.onChange}
                          >
                            <SelectTrigger>
                              <SelectValue placeholder="Type" />
                            </SelectTrigger>
                            <SelectContent>
                              {gainTargets.map(({ label, value }) => (
                                <SelectItem value={value}>{label}</SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </FormControl>
                      </FormItem>
                    )}
                  />
                </div>
                {index > 0 && (
                  <Button
                    type="button"
                    size="icon"
                    variant="outline"
                    onClick={() => methods.removeGain(index)}
                  >
                    <Minus className="h-4 w-4" />
                  </Button>
                )}
              </div>
            ))}
            <Button
              type="button"
              variant="muted"
              size="sm"
              onClick={() => methods.appendGain({ type: "PERCENT", value: 0 })}
              className="w-full"
            >
              <Plus className="h-4 w-4" /> Add
            </Button>
          </div>
          <div className="space-y-2">
            <FormLabel className="flex items-center">Loss Targets</FormLabel>
            {lossFieldArray.map((field, index) => (
              <div
                key={field.id}
                className="grid grid-cols-[1fr_auto] gap-2 items-center"
              >
                <div className="grid grid-cols-[1fr_auto] gap-1 items-center">
                  <FormField
                    control={form.control}
                    name={`loss_target.${index}.value`}
                    render={({ field }) => (
                      <FormItem>
                        <FormControl>
                          <Input
                            {...field}
                            type="number"
                            placeholder="20"
                            onChange={(e) => {
                              const value = Number(e.target.value);
                              field.onChange(value);
                            }}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={form.control}
                    name={`loss_target.${index}.type`}
                    render={({ field }) => (
                      <FormItem className="flex-1">
                        <FormControl>
                          <Select
                            value={field.value}
                            onValueChange={field.onChange}
                          >
                            <SelectTrigger>
                              <SelectValue placeholder="Type" />
                            </SelectTrigger>
                            <SelectContent>
                              {lossTargets.map(({ label, value }) => (
                                <SelectItem value={value}>{label}</SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </FormControl>
                      </FormItem>
                    )}
                  />
                </div>
                {index > 0 && (
                  <Button
                    type="button"
                    size="icon"
                    variant="outline"
                    onClick={() => methods.removeLoss(index)}
                  >
                    <Minus className="h-4 w-4" />
                  </Button>
                )}
              </div>
            ))}
            <Button
              type="button"
              variant="muted"
              size="sm"
              onClick={() => methods.appendLoss({ type: "PERCENT", value: 0 })}
              className="w-full"
            >
              <Plus className="h-4 w-4" /> Add
            </Button>
          </div>
        </div>
      </form>
    </Form>
  );
}
