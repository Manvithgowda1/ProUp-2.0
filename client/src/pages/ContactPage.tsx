import React, { useState } from 'react';
import { Mail, Phone, MapPin, Send, CheckCircle2 } from 'lucide-react';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Button } from '@/components/ui/Button';
import { useToast } from '@/components/ui/Toast';

export default function ContactPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [subject, setSubject] = useState('');
  const [message, setMessage] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const { toast } = useToast();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !email || !message) {
      toast('error', 'Please fill in required fields.');
      return;
    }
    setSubmitted(true);
    toast('success', 'Inquiry dispatched. Institutional relations team will respond within 24 hours.');
  };

  return (
    <div className="min-h-[80vh] py-16 px-4 sm:px-6 lg:px-8 bg-zinc-50">
      <div className="container-main max-w-5xl">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <p className="text-xs font-mono uppercase tracking-widest text-zinc-500 mb-1">Inquiries & Partnerships</p>
          <h1 className="text-4xl font-bold tracking-tight text-black">Contact Proup</h1>
          <p className="mt-3 text-zinc-600">
            For academic institution onboarding, corporate hiring challenge setups, or general inquiries.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Institutional Contact Info */}
          <div className="border border-zinc-200 bg-white rounded-xl p-8 space-y-6">
            <h3 className="text-lg font-bold text-black border-b border-zinc-100 pb-3">Liaison Office</h3>

            <div className="flex items-start gap-3">
              <Mail className="w-5 h-5 text-black shrink-0 mt-0.5" />
              <div>
                <p className="text-xs font-mono uppercase text-zinc-500">Electronic Mail</p>
                <p className="text-sm font-medium text-black">contact@proup.engineering</p>
                <p className="text-xs text-zinc-500">partnerships@proup.engineering</p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <Phone className="w-5 h-5 text-black shrink-0 mt-0.5" />
              <div>
                <p className="text-xs font-mono uppercase text-zinc-500">Direct Telephone</p>
                <p className="text-sm font-medium text-black">+91 (080) 4123-9876</p>
                <p className="text-xs text-zinc-500">Mon - Fri: 09:00 - 18:00 IST</p>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <MapPin className="w-5 h-5 text-black shrink-0 mt-0.5" />
              <div>
                <p className="text-xs font-mono uppercase text-zinc-500">Headquarters</p>
                <p className="text-sm font-medium text-black leading-snug">
                  Proup Innovation Park<br />
                  Outer Ring Road, Bellandur<br />
                  Bengaluru, Karnataka 560103
                </p>
              </div>
            </div>

            <div className="pt-4 border-t border-zinc-100">
              <p className="text-xs text-zinc-500 font-mono">
                Standardized verification turnaround: 24 business hours.
              </p>
            </div>
          </div>

          {/* Form */}
          <div className="md:col-span-2 border border-zinc-200 bg-white rounded-xl p-8 sm:p-10">
            {submitted ? (
              <div className="py-12 text-center space-y-4">
                <CheckCircle2 className="w-12 h-12 text-black mx-auto" />
                <h3 className="text-2xl font-bold text-black">Inquiry Transmitted</h3>
                <p className="text-zinc-600 max-w-md mx-auto text-sm">
                  Thank you for reaching out. A representative from the institutional partnership division will respond to {email}.
                </p>
                <Button variant="outline" onClick={() => setSubmitted(false)}>
                  Send Another Inquiry
                </Button>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-5">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <Input
                    label="Full Name *"
                    placeholder="Dr. Alan Turing"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                  />
                  <Input
                    label="Corporate / Academic Email *"
                    type="email"
                    placeholder="aturing@cambridge.edu"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>

                <Input
                  label="Subject *"
                  placeholder="Campus-wide Hiring Challenge Partnership"
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  required
                />

                <Textarea
                  label="Inquiry Details *"
                  placeholder="Provide scope, dates, and number of expected candidates..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  rows={5}
                  required
                />

                <div className="pt-2">
                  <Button type="submit" className="w-full sm:w-auto">
                    <Send className="w-4 h-4 mr-2" /> Transmit Inquiry
                  </Button>
                </div>
              </form>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
