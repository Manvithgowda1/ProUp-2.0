import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Mail, Lock, AlertCircle, ArrowRight } from 'lucide-react';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/components/ui/Toast';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');

    if (!email || !password) {
      setErrorMsg('Please enter both email and password.');
      return;
    }

    try {
      setIsSubmitting(true);
      await login({ email, password });
      toast('success', 'Authentication successful.');
      navigate('/events');
    } catch (err: any) {
      const detail = err?.response?.data?.detail || err?.response?.data?.message || 'Invalid email or password.';
      setErrorMsg(detail);
      toast('error', detail);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-zinc-50">
      <div className="max-w-md w-full bg-white border border-zinc-200 rounded-xl p-8 sm:p-10 shadow-sm">
        <div className="text-center mb-8">
          <p className="text-xs font-mono uppercase tracking-widest text-zinc-500 mb-1">Access Portal</p>
          <h2 className="text-3xl font-bold tracking-tight text-black">Sign In to Proup</h2>
          <p className="text-sm text-zinc-600 mt-2">Enter your institutional credentials to continue</p>
        </div>

        {errorMsg && (
          <div className="mb-6 p-3 rounded-md bg-zinc-100 border border-black flex items-center gap-2 text-xs text-black font-mono">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <Input
            label="Email Address"
            type="email"
            placeholder="engineer@institution.edu"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            icon={Mail}
            required
          />

          <Input
            label="Password"
            type="password"
            placeholder="••••••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            icon={Lock}
            required
          />

          <div className="flex items-center justify-between text-xs text-zinc-500">
            <label className="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" className="rounded border-zinc-300 text-black focus:ring-black" />
              <span>Remember session</span>
            </label>
            <Link to="/contact" className="hover:text-black hover:underline">
              Need assistance?
            </Link>
          </div>

          <Button type="submit" loading={isSubmitting} className="w-full">
            Sign In <ArrowRight className="ml-2 w-4 h-4" />
          </Button>
        </form>

        <div className="mt-8 pt-6 border-t border-zinc-100 text-center text-xs text-zinc-600">
          Do not possess an account yet?{' '}
          <Link to="/register" className="font-semibold text-black hover:underline">
            Register now
          </Link>
        </div>
      </div>
    </div>
  );
}
