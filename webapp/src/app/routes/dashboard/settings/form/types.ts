import { z } from "zod";

const targetSchema = z.object({
  type: z.enum(["NEXT_CANDLE", "PERCENT"]),
  value: z.number().min(1, { message: "Value must be at least 1." }),
});

export const formSchema = z.object({
  name: z
    .string()
    .min(2, { message: "Username must be at least 2 characters." }),

  indicators: z
    .array(z.string())
    .nonempty({ message: "At least one indicator must be selected." }),

  candle_patterns: z
    .array(z.string())
    .nonempty({ message: "At least one candle pattern must be selected." }),

  timeranges: z
    .array(z.string())
    .nonempty({ message: "At least one time range must be selected." }),

  timeframes: z
    .array(z.string())
    .nonempty({ message: "At least one time frame must be selected." }),

  currencies: z
    .array(z.string())
    .nonempty({ message: "At least one currency must be selected." }),

  min_confluence: z
    .number()
    .min(1, { message: "At least one confluence is required." }),

  gain_target: z
    .array(targetSchema)
    .nonempty({ message: "At least one gain target is required." }),

  loss_target: z
    .array(targetSchema)
    .nonempty({ message: "At least one loss target is required." }),
});

export const defaultValues: z.infer<typeof formSchema> = {
  name: "",
  indicators: [],
  candle_patterns: [],
  timeranges: [],
  timeframes: [],
  currencies: [],
  min_confluence: 1,
  gain_target: [
    { type: "PERCENT", value: 0 },
  ],
  loss_target: [
    { type: "PERCENT", value: 0 },
  ],
};
