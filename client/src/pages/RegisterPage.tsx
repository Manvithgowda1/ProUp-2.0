import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { GraduationCap, Building2, AlertCircle, ArrowRight, Check } from 'lucide-react';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/components/ui/Toast';

export default function RegisterPage() {
  const [role, setRole] = useState<'student' | 'organizer'>('student');

  // Student form state
  const [studentName, setStudentName] = useState('');
  const [studentEmail, setStudentEmail] = useState('');
  const [studentPassword, setStudentPassword] = useState('');
  const [githubUrl, setGithubUrl] = useState('');
  const [linkedinUrl, setLinkedinUrl] = useState('');
  const [bio, setBio] = useState('');

  // Organizer form state
  const [orgEmail, setOrgEmail] = useState('');
  const [orgPassword, setOrgPassword] = useState('');
  const [orgName, setOrgName] = useState('');
  const [cin, setCin] = useState('');
  const [orgContactEmail, setOrgContactEmail] = useState('');
  const [website, setWebsite] = useState('');

  const [errorMsg, setErrorMsg] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { registerStudent, registerOrganizer } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();

  const getPasswordStrength = (pass: string) => {
    if (!pass) return { score: 0, label: 'Empty' };
    if (pass.length < 6) return { score: 1, label: 'Too short' };
    if (pass.length < 10) return { score: 2, label: 'Moderate' };
    return { score: 3, label: 'Strong' };
  };

  const strength = getPasswordStrength(role === 'student' ? studentPassword : orgPassword);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');

    if (role === 'student') {
      if (!studentName || !studentEmail || !studentPassword) {
        setErrorMsg('Please populate all mandatory fields.');
        return;
      }
      if (studentPassword.length < 6) {
        setErrorMsg('Password must be at least 6 characters.');
        return;
      }
      try {
        setIsSubmitting(true);
        await registerStudent({
          name: studentName,
          email: studentEmail,
          password: studentPassword,
          github_url: githubUrl || undefined,
          linkedin_url: linkedinUrl || undefined,
          bio: bio || undefined,
        });
        toast('success', 'Student registration confirmed.');
        navigate('/events');
      } catch (err: any) {
        const detail = err?.response?.data?.detail || err?.response?.data?.message || 'Registration failed.';
        setErrorMsg(typeof detail === 'string' ? detail : JSON.stringify(detail));
        toast('error', 'Registration error.');
      } finally {
        setIsSubmitting(false);
      }
    } else {
      if (!orgEmail || !orgPassword || !orgName || !cin) {
        setErrorMsg('Please populate all mandatory organizer fields.');
        return;
      }
      if (orgPassword.length < 6) {
        setErrorMsg('Password must be at least 6 characters.');
        return;
      }
      try {
        setIsSubmitting(true);
        await registerOrganizer({
          email: orgEmail,
          password: orgPassword,
          organization: {
            name: orgName,
            cin: cin,
            email: orgContactEmail || orgEmail,
            website: website || undefined,
          },
        });
        toast('success', 'Organizer account registered. Awaiting verification.');
        navigate('/organizer/dashboard');
      } catch (err: any) {
        const detail = err?.response?.data?.detail || err?.response?.data?.message || 'Registration failed.';
        setErrorMsg(typeof detail === 'string' ? detail : JSON.stringify(detail));
        toast('error', 'Registration error.');
      } finally {
        setIsSubmitting(false);
      }
    }
  };

  return (
    <div className="min-h-[85vh] py-12 px-4 sm:px-6 lg:px-8 bg-zinc-50 flex items-center justify-center">
      <div className="max-w-xl w-full bg-white border border-zinc-200 rounded-xl p-8 sm:p-10 shadow-sm">
        <div className="text-center mb-8">
          <p className="text-xs font-mono uppercase tracking-widest text-zinc-500 mb-1">Registration</p>
          <h2 className="text-3xl font-bold tracking-tight text-black">Create Institutional Account</h2>
          <p className="text-sm text-zinc-600 mt-2">Select your category to access the standardized portal</p>
        </div>

        {/* Role Segment Selector */}
        <div className="grid grid-cols-2 gap-2 p-1 bg-zinc-100 rounded-lg mb-8 border border-zinc-200">
          <button
            type="button"
            onClick={() => { setRole('student'); setErrorMsg(''); }}
            className={`flex items-center justify-center gap-2 py-2.5 text-xs font-mono uppercase tracking-wider rounded-md transition-all ${
              role === 'student' ? 'bg-black text-white shadow-sm font-semibold' : 'text-zinc-600 hover:text-black'
            }`}
          >
            <GraduationCap className="w-4 h-4" /> Student Candidate
          </button>
          <button
            type="button"
            onClick={() => { setRole('organizer'); setErrorMsg(''); }}
            className={`flex items-center justify-center gap-2 py-2.5 text-xs font-mono uppercase tracking-wider rounded-md transition-all ${
              role === 'organizer' ? 'bg-black text-white shadow-sm font-semibold' : 'text-zinc-600 hover:text-black'
            }`}
          >
            <Building2 className="w-4 h-4" /> Event Organizer
          </button>
        </div>

        {errorMsg && (
          <div className="mb-6 p-3 rounded-md bg-zinc-100 border border-black flex items-center gap-2 text-xs text-black font-mono">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {role === 'student' ? (
            <>
              <Input
                label="Full Name *"
                placeholder="Jane Doe"
                value={studentName}
                onChange={(e) => setStudentName(e.target.value)}
                required
              />
              <Input
                label="Institutional or Personal Email *"
                type="email"
                placeholder="candidate@university.edu"
                value={studentEmail}
                onChange={(e) => setStudentEmail(e.target.value)}
                required
              />
              <div>
                <Input
                  label="Password (min 6 characters) *"
                  type="password"
                  placeholder="••••••••••••"
                  value={studentPassword}
                  onChange={(e) => setStudentPassword(e.target.value)}
                  required
                />
                <div className="mt-1 flex items-center justify-between">
                  <div className="flex gap-1 w-32 h-1 bg-zinc-200 rounded overflow-hidden">
                    <div className={`h-full ${strength.score >= 1 ? 'bg-black' : 'bg-transparent'} w-1/3`} />
                    <div className={`h-full ${strength.score >= 2 ? 'bg-black' : 'bg-transparent'} w-1/3`} />
                    <div className={`h-full ${strength.score >= 3 ? 'bg-black' : 'bg-transparent'} w-1/3`} />
                  </div>
                  <span className="text-[10px] font-mono uppercase text-zinc-500">{strength.label}</span>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <Input
                  label="GitHub Profile URL (Optional)"
                  placeholder="https://github.com/username"
                  value={githubUrl}
                  onChange={(e) => setGithubUrl(e.target.value)}
                />
                <Input
                  label="LinkedIn URL (Optional)"
                  placeholder="https://linkedin.com/in/username"
                  value={linkedinUrl}
                  onChange={(e) => setLinkedinUrl(e.target.value)}
                />
              </div>

              <Textarea
                label="Professional Summary / Bio (Optional)"
                placeholder="Specializing in distributed systems, backend architectures, or algorithms..."
                value={bio}
                onChange={(e) => setBio(e.target.value)}
                rows={3}
              />
            </>
          ) : (
            <>
              <Input
                label="Organization / Company Name *"
                placeholder="Acme Technologies Ltd."
                value={orgName}
                onChange={(e) => setOrgName(e.target.value)}
                required
              />
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <Input
                  label="Corporate Identification Number (CIN) *"
                  placeholder="U72200KA2024PTC123456"
                  value={cin}
                  onChange={(e) => setCin(e.target.value)}
                  required
                />
                <Input
                  label="Website URL (Optional)"
                  placeholder="https://organization.com"
                  value={website}
                  onChange={(e) => setWebsite(e.target.value)}
                />
              </div>
              <Input
                label="Account Admin Email *"
                type="email"
                placeholder="recruitment.lead@organization.com"
                value={orgEmail}
                onChange={(e) => setOrgEmail(e.target.value)}
                required
              />
              <Input
                label="Public Contact Email (Optional)"
                type="email"
                placeholder="careers@organization.com"
                value={orgContactEmail}
                onChange={(e) => setOrgContactEmail(e.target.value)}
              />
              <div>
                <Input
                  label="Password (min 6 characters) *"
                  type="password"
                  placeholder="••••••••••••"
                  value={orgPassword}
                  onChange={(e) => setOrgPassword(e.target.value)}
                  required
                />
                <div className="mt-1 flex items-center justify-between">
                  <div className="flex gap-1 w-32 h-1 bg-zinc-200 rounded overflow-hidden">
                    <div className={`h-full ${strength.score >= 1 ? 'bg-black' : 'bg-transparent'} w-1/3`} />
                    <div className={`h-full ${strength.score >= 2 ? 'bg-black' : 'bg-transparent'} w-1/3`} />
                    <div className={`h-full ${strength.score >= 3 ? 'bg-black' : 'bg-transparent'} w-1/3`} />
                  </div>
                  <span className="text-[10px] font-mono uppercase text-zinc-500">{strength.label}</span>
                </div>
              </div>
            </>
          )}

          <div className="pt-2">
            <Button type="submit" loading={isSubmitting} className="w-full">
              Complete Registration <ArrowRight className="ml-2 w-4 h-4" />
            </Button>
          </div>
        </form>

        <div className="mt-8 pt-6 border-t border-zinc-100 text-center text-xs text-zinc-600">
          Already registered?{' '}
          <Link to="/login" className="font-semibold text-black hover:underline">
            Sign in
          </Link>
        </div>
      </div>
    </div>
  );
}
