import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  ArrowLeft,
  ArrowRight,
  Check,
  Calendar,
  MapPin,
  Users,
  FileText,
  Sparkles,
} from 'lucide-react';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Select } from '@/components/ui/Select';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { createEvent } from '@/services/events';
import { useToast } from '@/components/ui/Toast';

export default function CreateEventPage() {
  const [step, setStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Form state
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [eventType, setEventType] = useState('HIRING_CHALLENGE');
  const [eventMode, setEventMode] = useState('ONLINE');
  const [eventDate, setEventDate] = useState('');
  const [registrationDeadline, setRegistrationDeadline] = useState('');
  const [location, setLocation] = useState('');
  const [maxParticipants, setMaxParticipants] = useState('');

  const navigate = useNavigate();
  const { toast } = useToast();

  const eventTypeOptions = [
    { value: 'HIRING_CHALLENGE', label: 'Hiring Challenge' },
    { value: 'HACKATHON', label: 'Hackathon' },
    { value: 'COMPETITION', label: 'Coding Competition' },
    { value: 'WORKSHOP', label: 'Technical Workshop' },
  ];

  const eventModeOptions = [
    { value: 'ONLINE', label: 'Online (Remote Arena)' },
    { value: 'OFFLINE', label: 'Offline (In-Person)' },
    { value: 'HYBRID', label: 'Hybrid' },
  ];

  const validateStep1 = () => {
    if (!title.trim() || title.trim().length < 3) {
      toast('error', 'Event title must be at least 3 characters.');
      return false;
    }
    if (!description.trim() || description.trim().length < 10) {
      toast('error', 'Description must be at least 10 characters.');
      return false;
    }
    return true;
  };

  const validateStep2 = () => {
    if (!eventDate) {
      toast('error', 'Please select an event date and time.');
      return false;
    }
    if (!registrationDeadline) {
      toast('error', 'Please select a registration deadline.');
      return false;
    }
    if (new Date(registrationDeadline) >= new Date(eventDate)) {
      toast('error', 'Registration deadline must precede the event date.');
      return false;
    }
    if ((eventMode === 'OFFLINE' || eventMode === 'HYBRID') && !location.trim()) {
      toast('error', 'Venue location is required for offline or hybrid events.');
      return false;
    }
    return true;
  };

  const handleNext = () => {
    if (step === 1 && validateStep1()) {
      setStep(2);
    } else if (step === 2 && validateStep2()) {
      setStep(3);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setIsSubmitting(true);
      await createEvent({
        title: title.trim(),
        description: description.trim(),
        event_type: eventType,
        event_mode: eventMode,
        event_date: new Date(eventDate).toISOString(),
        registration_deadline: new Date(registrationDeadline).toISOString(),
        location: location.trim() || undefined,
        max_participants: maxParticipants ? parseInt(maxParticipants, 10) : undefined,
      });
      toast('success', 'Challenge published successfully.');
      navigate('/organizer/dashboard');
    } catch (err: any) {
      const detail =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        'Failed to create event.';
      toast('error', typeof detail === 'string' ? detail : 'Validation error.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const steps = [
    { num: 1, label: 'Specification' },
    { num: 2, label: 'Schedule & Capacity' },
    { num: 3, label: 'Review & Publish' },
  ];

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8 bg-zinc-50">
      <div className="container-main max-w-5xl">
        {/* Back Breadcrumb */}
        <div className="mb-6">
          <Link
            to="/organizer/dashboard"
            className="inline-flex items-center text-xs font-mono uppercase tracking-wider text-zinc-500 hover:text-black"
          >
            <ArrowLeft className="w-4 h-4 mr-1.5" /> Back to Dashboard
          </Link>
        </div>

        {/* Title Header */}
        <div className="mb-8">
          <p className="text-xs font-mono uppercase tracking-widest text-zinc-500 mb-1">
            Event Creation Wizard
          </p>
          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-black">
            Publish New Challenge
          </h1>
          <p className="text-sm text-zinc-600 mt-1">
            Configure standardized assessment parameters, scheduling, and candidate capacity.
          </p>
        </div>

        {/* Step Indicator */}
        <div className="bg-white border border-zinc-200 rounded-xl p-6 mb-8 shadow-sm">
          <div className="flex items-center justify-between max-w-2xl mx-auto">
            {steps.map((s, idx) => {
              const isCompleted = step > s.num;
              const isActive = step === s.num;
              return (
                <React.Fragment key={s.num}>
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-9 h-9 rounded-full border-2 flex items-center justify-center font-mono text-xs font-bold transition-all ${
                        isCompleted || isActive
                          ? 'bg-black text-white border-black'
                          : 'bg-white text-zinc-400 border-zinc-300'
                      }`}
                    >
                      {isCompleted ? <Check className="w-4 h-4" /> : `0${s.num}`}
                    </div>
                    <span
                      className={`text-xs font-mono uppercase tracking-wider hidden sm:inline ${
                        isActive ? 'text-black font-bold' : 'text-zinc-500'
                      }`}
                    >
                      {s.label}
                    </span>
                  </div>
                  {idx < steps.length - 1 && (
                    <div
                      className={`flex-1 h-[2px] mx-4 ${
                        step > s.num ? 'bg-black' : 'bg-zinc-200'
                      }`}
                    />
                  )}
                </React.Fragment>
              );
            })}
          </div>
        </div>

        {/* Wizard Body + Live Monochrome Card Preview */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Form Column */}
          <div className="lg:col-span-2 bg-white border border-zinc-200 rounded-xl p-8 shadow-sm">
            <form onSubmit={handleSubmit} className="space-y-6">
              {step === 1 && (
                <div className="space-y-5">
                  <div className="border-b border-zinc-100 pb-3">
                    <h2 className="text-lg font-bold text-black flex items-center gap-2">
                      <FileText className="w-4 h-4" /> Step 1: Basic Specification
                    </h2>
                  </div>

                  <Input
                    label="Challenge Title *"
                    placeholder="National Backend Engineering Challenge 2026"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                  />

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <Select
                      label="Event Category *"
                      options={eventTypeOptions}
                      value={eventType}
                      onChange={(e) => setEventType(e.target.value)}
                    />
                    <Select
                      label="Execution Mode *"
                      options={eventModeOptions}
                      value={eventMode}
                      onChange={(e) => setEventMode(e.target.value)}
                    />
                  </div>

                  <Textarea
                    label="Detailed Description & Eligibility *"
                    placeholder="Outline technical focus areas, round structure, evaluation criteria, and eligibility requirements..."
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={6}
                    required
                  />
                </div>
              )}

              {step === 2 && (
                <div className="space-y-5">
                  <div className="border-b border-zinc-100 pb-3">
                    <h2 className="text-lg font-bold text-black flex items-center gap-2">
                      <Calendar className="w-4 h-4" /> Step 2: Schedule & Capacity
                    </h2>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <Input
                      label="Registration Deadline *"
                      type="datetime-local"
                      value={registrationDeadline}
                      onChange={(e) => setRegistrationDeadline(e.target.value)}
                      required
                    />
                    <Input
                      label="Event Start Date & Time *"
                      type="datetime-local"
                      value={eventDate}
                      onChange={(e) => setEventDate(e.target.value)}
                      required
                    />
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <Input
                      label="Maximum Participants (Optional)"
                      type="number"
                      min="1"
                      placeholder="e.g. 250 (leave empty for unlimited)"
                      value={maxParticipants}
                      onChange={(e) => setMaxParticipants(e.target.value)}
                      icon={Users}
                    />

                    {(eventMode === 'OFFLINE' || eventMode === 'HYBRID') && (
                      <Input
                        label="Physical Venue Location *"
                        placeholder="Auditorium A, Innovation Campus"
                        value={location}
                        onChange={(e) => setLocation(e.target.value)}
                        icon={MapPin}
                        required
                      />
                    )}
                  </div>
                </div>
              )}

              {step === 3 && (
                <div className="space-y-5">
                  <div className="border-b border-zinc-100 pb-3">
                    <h2 className="text-lg font-bold text-black flex items-center gap-2">
                      <Sparkles className="w-4 h-4" /> Step 3: Final Review
                    </h2>
                  </div>

                  <div className="border border-zinc-200 rounded-lg p-6 bg-zinc-50 space-y-4 text-sm">
                    <div>
                      <span className="text-xs font-mono uppercase text-zinc-500 block">
                        Title
                      </span>
                      <p className="font-bold text-black text-base">{title}</p>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <span className="text-xs font-mono uppercase text-zinc-500 block">
                          Category
                        </span>
                        <p className="font-mono text-black">{eventType.replace('_', ' ')}</p>
                      </div>
                      <div>
                        <span className="text-xs font-mono uppercase text-zinc-500 block">
                          Mode
                        </span>
                        <p className="font-mono text-black">{eventMode}</p>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <span className="text-xs font-mono uppercase text-zinc-500 block">
                          Registration Deadline
                        </span>
                        <p className="font-mono text-black">
                          {registrationDeadline ? new Date(registrationDeadline).toLocaleString() : '—'}
                        </p>
                      </div>
                      <div>
                        <span className="text-xs font-mono uppercase text-zinc-500 block">
                          Event Date
                        </span>
                        <p className="font-mono text-black">
                          {eventDate ? new Date(eventDate).toLocaleString() : '—'}
                        </p>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <span className="text-xs font-mono uppercase text-zinc-500 block">
                          Capacity
                        </span>
                        <p className="font-mono text-black">
                          {maxParticipants ? `${maxParticipants} candidates` : 'Unlimited'}
                        </p>
                      </div>
                      {location && (
                        <div>
                          <span className="text-xs font-mono uppercase text-zinc-500 block">
                            Venue
                          </span>
                          <p className="font-mono text-black">{location}</p>
                        </div>
                      )}
                    </div>

                    <div>
                      <span className="text-xs font-mono uppercase text-zinc-500 block">
                        Description
                      </span>
                      <p className="text-zinc-700 whitespace-pre-wrap mt-1">{description}</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Footer Buttons */}
              <div className="flex items-center justify-between pt-6 border-t border-zinc-100">
                {step > 1 ? (
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => setStep((s) => s - 1)}
                  >
                    <ArrowLeft className="w-4 h-4 mr-2" /> Previous
                  </Button>
                ) : (
                  <div />
                )}

                {step < 3 ? (
                  <Button type="button" onClick={handleNext}>
                    Continue <ArrowRight className="w-4 h-4 ml-2" />
                  </Button>
                ) : (
                  <Button type="submit" loading={isSubmitting}>
                    <Check className="w-4 h-4 mr-2" /> Confirm & Publish Event
                  </Button>
                )}
              </div>
            </form>
          </div>

          {/* Live Monochrome Card Preview */}
          <div className="space-y-4">
            <p className="text-xs font-mono uppercase tracking-widest text-zinc-500">
              Live Catalog Card Preview
            </p>
            <div className="bg-white border border-black rounded-xl p-6 shadow-sm space-y-4">
              <div className="flex items-center justify-between">
                <Badge variant="outline" className="font-mono text-[10px]">
                  {eventType.replace('_', ' ')}
                </Badge>
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded border border-zinc-200 bg-zinc-50 text-zinc-600">
                  {eventMode}
                </span>
              </div>

              <div>
                <h3 className="text-lg font-bold text-black tracking-tight">
                  {title || 'Untitled Challenge'}
                </h3>
                <p className="text-xs font-mono text-zinc-500 mt-1">
                  Your Organization
                </p>
              </div>

              <p className="text-xs text-zinc-600 line-clamp-3 leading-relaxed">
                {description || 'Challenge description will appear here as you compose the specification...'}
              </p>

              <div className="pt-4 border-t border-zinc-100 space-y-1.5 text-xs font-mono text-zinc-500">
                <div className="flex items-center gap-2">
                  <Calendar className="w-3.5 h-3.5 text-black" />
                  <span>
                    {eventDate ? new Date(eventDate).toLocaleDateString() : 'Date TBA'}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <Users className="w-3.5 h-3.5 text-black" />
                  <span>
                    {maxParticipants ? `${maxParticipants} seats` : 'Open capacity'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
