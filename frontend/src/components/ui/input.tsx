import { cn } from "@/lib/utils";
import { InputHTMLAttributes, forwardRef } from "react";

export const Input = forwardRef<HTMLInputElement, InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => (
    <input
      ref={ref}
      className={cn(
        "flex h-11 w-full rounded-xl border border-border bg-foreground/5 px-4 text-sm text-foreground placeholder:text-muted backdrop-blur transition focus:border-violet-500/50 focus:outline-none focus:ring-2 focus:ring-violet-500/20",
        className,
      )}
      {...props}
    />
  ),
);
Input.displayName = "Input";
