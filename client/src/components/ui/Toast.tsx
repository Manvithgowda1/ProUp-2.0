import React, { createContext, useCallback, useContext, useState } from 'react';
import { CheckCircle, AlertCircle, Info, X } from 'lucide-react';
import { cn } from '@/lib/utils';

type ToastType = 'success' | 'error' | 'info';

interface Toast {
  id: string;
  type: ToastType;
  message: string;
}

interface ToastContextValue {
  addToast: (type: ToastType, message: string) => void;
}

const ToastContext = createContext<ToastContextValue | undefined>(undefined);

const iconMap: Record<ToastType, React.FC<{ className?: string }>> = {
  success: CheckCircle,
  error: AlertCircle,
  info: Info,
};

const ToastItem: React.FC<{ toast: Toast; onDismiss: (id: string) => void }> = ({ toast, onDismiss }) => {
  const Icon = iconMap[toast.type];

  React.useEffect(() => {
    const timer = setTimeout(() => onDismiss(toast.id), 3000);
    return () => clearTimeout(timer);
  }, [toast.id, onDismiss]);

  return (
    <div
      className={cn(
        'bg-white border border-zinc-200 shadow-lg rounded-lg px-4 py-3 flex items-center gap-3',
        'border-l-4 border-l-black'
      )}
    >
      <Icon className="h-5 w-5 text-zinc-900 shrink-0" />
      <p className="text-sm text-zinc-900 flex-1">{toast.message}</p>
      <button onClick={() => onDismiss(toast.id)} className="text-zinc-400 hover:text-zinc-900 transition-colors shrink-0">
        <X className="h-4 w-4" />
      </button>
    </div>
  );
};

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = useCallback((type: ToastType, message: string) => {
    const id = crypto.randomUUID();
    setToasts((prev) => [...prev, { id, type, message }]);
  }, []);

  const dismissToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ addToast }}>
      {children}
      {/* Toast container */}
      <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2 w-80">
        {toasts.map((toast) => (
          <ToastItem key={toast.id} toast={toast} onDismiss={dismissToast} />
        ))}
      </div>
    </ToastContext.Provider>
  );
};

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }

  return {
    toast: context.addToast,
    success: (message: string) => context.addToast('success', message),
    error: (message: string) => context.addToast('error', message),
  };
};
