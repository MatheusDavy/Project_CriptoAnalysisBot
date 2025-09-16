import * as React from "react";
import { cn } from "lib/utils";

type InputProps =  Omit<React.ComponentProps<"input">, "prefix" | "suffix"> & {
  inputClassName?: string,
  prefix?: React.ReactNode | string | number;
  suffix?: React.ReactNode | string | number;
};

function Input({ className, inputClassName, type, prefix, suffix, ...props }: InputProps) {
  return (
    <div
      className={cn(
        "flex items-center h-10 w-full rounded-md border border-input bg-transparent text-accent shadow-xs transition-[color,box-shadow] focus-within:border-ring focus-within:ring-[3px] focus-within:ring-ring/50",
        "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive",
        className
      )}
    >
      {prefix && (
        <span className="px-2 text-sm text-muted-foreground flex items-center">
          {prefix}
        </span>
      )}

      <input
        type={type}
        data-slot="input"
        className={cn(
          "flex-1 bg-bg-100 min-w-0 h-full px-3 py-1 outline-none placeholder:text-accent-300 selection:bg-primary selection:text-primary-foreground disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 md:text-sm",
          inputClassName
        )}
        {...props}
      />

      {suffix && (
        <span className="px-2 text-sm text-muted-foreground flex items-center">
          {suffix}
        </span>
      )}
    </div>
  );
}

export { Input };
