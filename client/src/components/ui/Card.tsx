import React from "react";
import { cn } from "@/lib/utils";

/* ---------------------------------- Card ---------------------------------- */

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, children, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "overflow-hidden rounded-lg border border-zinc-200 bg-white shadow-sm",
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
);
Card.displayName = "Card";

/* ------------------------------- CardHeader ------------------------------- */

export interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {}

const CardHeader = React.forwardRef<HTMLDivElement, CardHeaderProps>(
  ({ className, children, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("border-b border-zinc-100 px-6 py-4", className)}
      {...props}
    >
      {children}
    </div>
  )
);
CardHeader.displayName = "CardHeader";

/* ------------------------------ CardContent ------------------------------- */

export interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {}

const CardContent = React.forwardRef<HTMLDivElement, CardContentProps>(
  ({ className, children, ...props }, ref) => (
    <div ref={ref} className={cn("p-6", className)} {...props}>
      {children}
    </div>
  )
);
CardContent.displayName = "CardContent";

/* ------------------------------- CardFooter ------------------------------- */

export interface CardFooterProps extends React.HTMLAttributes<HTMLDivElement> {}

const CardFooter = React.forwardRef<HTMLDivElement, CardFooterProps>(
  ({ className, children, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "border-t border-zinc-100 bg-zinc-50 px-6 py-4",
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
);
CardFooter.displayName = "CardFooter";

export { Card, CardHeader, CardContent, CardFooter };
