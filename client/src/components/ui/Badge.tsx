import React from "react";
import { cn } from "@/lib/utils";

const variantStyles = {
  default: "bg-black text-white",
  outline: "border border-zinc-300 text-zinc-700",
  secondary: "bg-zinc-100 text-zinc-800",
} as const;

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: keyof typeof variantStyles;
}

const Badge: React.FC<BadgeProps> = ({
  variant = "default",
  className,
  children,
  ...props
}) => {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
        variantStyles[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
};

Badge.displayName = "Badge";

export { Badge };
