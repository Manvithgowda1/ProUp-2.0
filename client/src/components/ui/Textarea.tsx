import React from 'react';
import { cn } from '@/lib/utils';

interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
}

export const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ label, error, className, ...props }, ref) => {
    return (
      <div className="space-y-1">
        {label && (
          <label className="block text-sm font-medium text-zinc-900">
            {label}
          </label>
        )}
        <textarea
          ref={ref}
          className={cn(
            'w-full border border-zinc-300 rounded-md px-3 py-2 text-sm text-zinc-900',
            'focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent',
            'disabled:opacity-50 disabled:cursor-not-allowed',
            'resize-vertical min-h-[80px]',
            error && 'border-red-500 focus:ring-red-500',
            className
          )}
          {...props}
        />
        {error && (
          <p className="text-sm text-red-500">{error}</p>
        )}
      </div>
    );
  }
);

Textarea.displayName = 'Textarea';

export default Textarea;
