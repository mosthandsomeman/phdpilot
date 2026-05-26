import { cn } from "@/lib/utils";
import { HTMLAttributes } from "react";

export function Card({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "rounded-2xl border border-border bg-card p-6 backdrop-blur-xl shadow-xl shadow-black/5 dark:shadow-black/20",
        className,
      )}
      {...props}
    />
  );
}
