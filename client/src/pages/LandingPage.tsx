import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  GraduationCap, 
  Calendar, 
  Check, 
  ArrowRight, 
  Trophy, 
  ShieldCheck, 
  Briefcase, 
  Users 
} from 'lucide-react';
import { Button } from '@/components/ui/Button';

export default function LandingPage() {
  const navigate = useNavigate();

  const studentFeatures = [
    'Direct access to top campus hiring challenges & hackathons',
    'Real-time coding arena and automated evaluation',
    'Earn verifiable rank points, badges & achievement records',
    'Verified profiles scouted directly by enterprise recruiters'
  ];

  const organizerFeatures = [
    'Create customized multi-round challenges (MCQ + Coding + Interview)',
    'Automated test case runner & anti-cheat analytics',
    'Comprehensive candidate progression funnel & CSV exports',
    'Seamless candidate shortlisting & podium rank certification'
  ];

  return (
    <div className="flex flex-col min-h-screen bg-white">
      {/* Hero Section */}
      <section className="relative border-b border-zinc-200 py-24 sm:py-32 bg-white">
        <div className="container-main text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 mb-8 rounded-full border border-black text-xs font-mono tracking-widest uppercase bg-zinc-50">
            <ShieldCheck className="w-3.5 h-3.5" /> Institutional Talent Verification
          </div>
          
          <h1 className="text-5xl sm:text-7xl font-extrabold tracking-tight text-black max-w-4xl mx-auto uppercase leading-none">
            Professional Upgrade
          </h1>
          <p className="mt-4 text-xl sm:text-2xl font-mono text-zinc-600 max-w-2xl mx-auto tracking-tight">
            Meet. Compete. Get Hired.
          </p>
          <p className="mt-6 text-base sm:text-lg text-zinc-600 max-w-2xl mx-auto leading-relaxed">
            The formal meritocratic infrastructure connecting ambitious engineering students with leading technology organizations through standardized multi-round assessments.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button size="lg" onClick={() => navigate('/events')} className="w-full sm:w-auto">
              Explore Active Events <ArrowRight className="ml-2 w-4 h-4" />
            </Button>
            <Button size="lg" variant="outline" onClick={() => navigate('/register')} className="w-full sm:w-auto">
              Register Account
            </Button>
          </div>
        </div>
      </section>

      {/* Role Gateway Section */}
      <section className="py-20 border-b border-zinc-200 bg-zinc-50">
        <div className="container-main">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <p className="text-xs font-mono uppercase tracking-widest text-zinc-500 mb-2">Gateways</p>
            <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-black">Choose Your Role</h2>
            <p className="mt-3 text-zinc-600">Tailored portals built specifically for students striving for recognition and organizations scouting vetted engineers.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
            {/* Student Card */}
            <div className="border border-zinc-200 bg-white rounded-xl p-8 hover:border-black transition-all flex flex-col justify-between shadow-sm">
              <div>
                <div className="w-12 h-12 bg-black text-white rounded-lg flex items-center justify-center mb-6">
                  <GraduationCap className="w-6 h-6" />
                </div>
                <h3 className="text-2xl font-bold text-black mb-3">For Students</h3>
                <p className="text-zinc-600 text-sm mb-6 leading-relaxed">
                  Compete in standardized aptitude tests and algorithmic coding rounds. Earn verifiable points, build your verified achievement record, and unlock recruiter interviews.
                </p>
                <div className="space-y-3 mb-8">
                  {studentFeatures.map((feat, idx) => (
                    <div key={idx} className="flex items-start gap-3 text-sm text-zinc-700">
                      <Check className="w-4 h-4 text-black shrink-0 mt-0.5" />
                      <span>{feat}</span>
                    </div>
                  ))}
                </div>
              </div>
              <Button onClick={() => navigate('/register')} className="w-full">
                Continue as Student <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
            </div>

            {/* Organizer Card */}
            <div className="border border-zinc-200 bg-white rounded-xl p-8 hover:border-black transition-all flex flex-col justify-between shadow-sm">
              <div>
                <div className="w-12 h-12 bg-black text-white rounded-lg flex items-center justify-center mb-6">
                  <Calendar className="w-6 h-6" />
                </div>
                <h3 className="text-2xl font-bold text-black mb-3">For Event Organizers</h3>
                <p className="text-zinc-600 text-sm mb-6 leading-relaxed">
                  Design hackathons and hiring challenges. Automate multi-round qualification funnels, evaluate code submissions in real-time, and manage candidate rosters efficiently.
                </p>
                <div className="space-y-3 mb-8">
                  {organizerFeatures.map((feat, idx) => (
                    <div key={idx} className="flex items-start gap-3 text-sm text-zinc-700">
                      <Check className="w-4 h-4 text-black shrink-0 mt-0.5" />
                      <span>{feat}</span>
                    </div>
                  ))}
                </div>
              </div>
              <Button onClick={() => navigate('/register')} variant="outline" className="w-full">
                Continue as Organizer <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Counter Section */}
      <section className="py-20 bg-black text-white">
        <div className="container-main">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div className="p-4">
              <div className="text-4xl sm:text-5xl font-extrabold font-mono tracking-tight">50,000+</div>
              <p className="text-xs sm:text-sm uppercase tracking-wider text-zinc-400 mt-2 font-mono">Students Enrolled</p>
            </div>
            <div className="p-4">
              <div className="text-4xl sm:text-5xl font-extrabold font-mono tracking-tight">2,000+</div>
              <p className="text-xs sm:text-sm uppercase tracking-wider text-zinc-400 mt-2 font-mono">Verified Organizers</p>
            </div>
            <div className="p-4">
              <div className="text-4xl sm:text-5xl font-extrabold font-mono tracking-tight">10,000+</div>
              <p className="text-xs sm:text-sm uppercase tracking-wider text-zinc-400 mt-2 font-mono">Rounds Conducted</p>
            </div>
            <div className="p-4">
              <div className="text-4xl sm:text-5xl font-extrabold font-mono tracking-tight">95%</div>
              <p className="text-xs sm:text-sm uppercase tracking-wider text-zinc-400 mt-2 font-mono">Recruiter Approval</p>
            </div>
          </div>
        </div>
      </section>

      {/* Institutional Mission Callout */}
      <section className="py-20 bg-white">
        <div className="container-main max-w-4xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-black mb-4">
            A Formal Standard for Technical Talent
          </h2>
          <p className="text-zinc-600 leading-relaxed mb-8">
            Proup replaces subjective resumes with verifiable, skill-based competitive milestones. Every round attended, every algorithmic puzzle solved, and every podium rank earned creates a permanent, tamper-proof record of technical competence.
          </p>
          <div className="inline-flex gap-4">
            <Link to="/contact">
              <Button variant="outline">Enterprise Partnerships</Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
