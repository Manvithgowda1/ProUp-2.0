import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  ArrowLeft, 
  Calendar, 
  Clock, 
  MapPin, 
  Users, 
  Building2, 
  CheckCircle2, 
  AlertCircle, 
  ArrowRight,
  ShieldCheck,
  Award
} from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { eventsService } from '@/services/events';
import { EventResponse, RoundResponse } from '@/types';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/components/ui/Toast';

export default function EventDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [event, setEvent] = useState<EventResponse | null>(null);
  const [rounds, setRounds] = useState<RoundResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRegistering, setIsRegistering] = useState(false);
  const [isRegistered, setIsRegistered] = useState(false);

  const { isAuthenticated, isStudent } = useAuth();
  const { toast } = useToast();
  const navigate = useNavigate();

  useEffect(() => {
    if (id) {
      loadEventData(parseInt(id, 10));
    }
  }, [id]);

  const loadEventData = async (eventId: number) => {
    try {
      setIsLoading(true);
      const [evData, rData] = await Promise.all([
        eventsService.getEvent(eventId),
        eventsService.getEventRounds(eventId).catch(() => []),
      ]);
      setEvent(evData);
      setRounds(rData || []);
    } catch (err: any) {
      toast('error', 'Unable to retrieve event information.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegister = async () => {
    if (!isAuthenticated) {
      toast('info', 'Please sign in to register for challenges.');
      navigate('/login');
      return;
    }
    if (!isStudent) {
      toast('error', 'Only student accounts can register for challenges.');
      return;
    }

    try {
      setIsRegistering(true);
      await eventsService.registerForEvent(event!.event_id);
      setIsRegistered(true);
      toast('success', 'Registration confirmed. You are enrolled in the event pipeline.');
    } catch (err: any) {
      const detail = err?.response?.data?.detail || err?.response?.data?.message || 'Registration failed.';
      if (typeof detail === 'string' && detail.toLowerCase().includes('already')) {
        setIsRegistered(true);
        toast('info', 'You are already registered for this challenge.');
      } else {
        toast('error', typeof detail === 'string' ? detail : 'Registration error.');
      }
    } finally {
      setIsRegistering(false);
    }
  };

  const formatDate = (dateStr: string) => {
    if (!dateStr) return 'TBA';
    return new Date(dateStr).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen py-16 px-4 bg-zinc-50 flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="w-8 h-8 border-2 border-black border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs font-mono uppercase text-zinc-500">Loading challenge specification...</p>
        </div>
      </div>
    );
  }

  if (!event) {
    return (
      <div className="min-h-screen py-16 px-4 bg-zinc-50 flex items-center justify-center">
        <div className="text-center bg-white border border-zinc-200 rounded-xl p-8 max-w-md">
          <AlertCircle className="w-10 h-10 text-black mx-auto mb-3" />
          <h2 className="text-xl font-bold text-black">Event Not Found</h2>
          <p className="text-sm text-zinc-600 mt-2">The requested challenge does not exist or has been archived.</p>
          <Button onClick={() => navigate('/events')} className="mt-6">
            Return to Explorer
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-10 px-4 sm:px-6 lg:px-8 bg-zinc-50">
      <div className="container-main max-w-6xl">
        {/* Navigation Breadcrumb */}
        <div className="mb-6">
          <Link to="/events" className="inline-flex items-center text-xs font-mono uppercase tracking-wider text-zinc-500 hover:text-black">
            <ArrowLeft className="w-4 h-4 mr-1.5" /> Back to Catalog
          </Link>
        </div>

        {/* Top Header Card */}
        <div className="bg-white border border-zinc-200 rounded-xl p-8 sm:p-10 mb-8 shadow-sm">
          <div className="flex flex-wrap items-center gap-2 mb-4">
            <Badge variant="outline" className="font-mono text-xs">
              {event.event_type.replace('_', ' ')}
            </Badge>
            <span className="text-xs font-mono uppercase px-2.5 py-0.5 rounded border border-zinc-200 bg-zinc-50 text-zinc-700">
              {event.event_mode}
            </span>
            <span className="text-xs font-mono uppercase px-2.5 py-0.5 rounded border border-black bg-black text-white">
              Status: {event.status}
            </span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-black leading-tight">
            {event.title}
          </h1>

          <div className="mt-4 flex flex-wrap items-center gap-6 text-xs font-mono text-zinc-600">
            <div className="flex items-center gap-1.5">
              <Building2 className="w-4 h-4 text-black" />
              <span>Host: <strong className="text-black">{event.organization?.name || 'Verified Enterprise'}</strong></span>
            </div>
            <div className="flex items-center gap-1.5">
              <Calendar className="w-4 h-4 text-black" />
              <span>Date: {formatDate(event.event_date)}</span>
            </div>
            <div className="flex items-center gap-1.5">
              <Clock className="w-4 h-4 text-black" />
              <span>Deadline: {formatDate(event.registration_deadline)}</span>
            </div>
          </div>
        </div>

        {/* Two-Column Detail Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content Column */}
          <div className="lg:col-span-2 space-y-8">
            {/* Description Card */}
            <div className="bg-white border border-zinc-200 rounded-xl p-8 shadow-sm">
              <h2 className="text-xl font-bold text-black border-b border-zinc-100 pb-3 mb-4">
                Challenge Overview
              </h2>
              <div className="prose prose-zinc max-w-none text-sm text-zinc-700 leading-relaxed whitespace-pre-wrap">
                {event.description}
              </div>
            </div>

            {/* Rounds Pipeline Preview */}
            <div className="bg-white border border-zinc-200 rounded-xl p-8 shadow-sm">
              <div className="flex items-center justify-between border-b border-zinc-100 pb-3 mb-6">
                <div>
                  <h2 className="text-xl font-bold text-black">Standardized Rounds Pipeline</h2>
                  <p className="text-xs text-zinc-500 mt-0.5">Qualification stages defined for this challenge</p>
                </div>
                {isStudent && (
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => navigate(`/events/${event.event_id}/rounds`)}
                  >
                    Open Live Pipeline <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
                  </Button>
                )}
              </div>

              {rounds.length === 0 ? (
                <p className="text-xs font-mono text-zinc-500 py-4">No formal rounds published yet for this challenge.</p>
              ) : (
                <div className="space-y-4">
                  {rounds.map((round) => (
                    <div
                      key={round.round_id}
                      className="border border-zinc-200 rounded-lg p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:border-black transition-all"
                    >
                      <div className="flex items-start gap-4">
                        <div className="w-8 h-8 rounded-full border border-black bg-zinc-50 flex items-center justify-center font-mono font-bold text-xs shrink-0">
                          {round.round_number}
                        </div>
                        <div>
                          <div className="flex items-center gap-2">
                            <h3 className="font-bold text-black text-base">{round.name}</h3>
                            <Badge variant="outline" className="text-[10px] font-mono">
                              {round.round_type}
                            </Badge>
                          </div>
                          {round.description && (
                            <p className="text-xs text-zinc-600 mt-1 line-clamp-2">{round.description}</p>
                          )}
                          <div className="flex items-center gap-4 text-xs font-mono text-zinc-500 mt-2">
                            <span>Duration: {round.duration_minutes} mins</span>
                            <span>Total Marks: {round.total_marks}</span>
                            <span>Passing: {round.passing_marks}</span>
                          </div>
                        </div>
                      </div>

                      <div className="shrink-0 text-right">
                        <span className={`inline-block text-xs font-mono px-2.5 py-1 rounded border uppercase ${
                          round.status === 'LIVE'
                            ? 'bg-black text-white border-black font-semibold'
                            : 'bg-zinc-50 border-zinc-200 text-zinc-600'
                        }`}>
                          {round.status}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Standard Points Incentives */}
            <div className="bg-zinc-100 border border-zinc-200 rounded-xl p-6">
              <div className="flex items-start gap-3">
                <Award className="w-5 h-5 text-black shrink-0 mt-0.5" />
                <div>
                  <h4 className="text-sm font-bold text-black">Standard Merit Point Distribution</h4>
                  <p className="text-xs text-zinc-600 mt-1 leading-relaxed">
                    Participation in this event yields <strong>+5 Points</strong> upon verified attendance. Securing 1st place awards <strong>+20 Points</strong>, 2nd place awards <strong>+15 Points</strong>, and 3rd place awards <strong>+10 Points</strong> to your verifiable candidate portfolio.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Sticky Sidebar Action Card */}
          <div className="space-y-6">
            <div className="bg-white border border-zinc-200 rounded-xl p-6 shadow-sm sticky top-24 space-y-6">
              <h3 className="text-lg font-bold text-black border-b border-zinc-100 pb-3">
                Enrollment Gate
              </h3>

              <div className="space-y-3 text-xs font-mono text-zinc-600">
                <div className="flex items-center justify-between py-1 border-b border-zinc-100">
                  <span className="text-zinc-500">Mode</span>
                  <span className="font-semibold text-black">{event.event_mode}</span>
                </div>
                <div className="flex items-center justify-between py-1 border-b border-zinc-100">
                  <span className="text-zinc-500">Capacity</span>
                  <span className="font-semibold text-black">
                    {event.max_participants ? `${event.max_participants} seats` : 'Unrestricted'}
                  </span>
                </div>
                {event.location && (
                  <div className="flex items-center justify-between py-1 border-b border-zinc-100">
                    <span className="text-zinc-500">Venue</span>
                    <span className="font-semibold text-black truncate max-w-[150px]">{event.location}</span>
                  </div>
                )}
                <div className="flex items-center justify-between py-1 border-b border-zinc-100">
                  <span className="text-zinc-500">Stages</span>
                  <span className="font-semibold text-black">{rounds.length} Rounds</span>
                </div>
              </div>

              {isRegistered ? (
                <div className="space-y-3">
                  <div className="p-3 bg-zinc-50 border border-black rounded-md flex items-center gap-2 text-xs font-mono text-black">
                    <CheckCircle2 className="w-4 h-4 shrink-0" />
                    <span>Candidate Enrolled Successfully</span>
                  </div>
                  <Button
                    onClick={() => navigate(`/events/${event.event_id}/rounds`)}
                    className="w-full"
                  >
                    Proceed to Rounds Pipeline <ArrowRight className="w-4 h-4 ml-2" />
                  </Button>
                </div>
              ) : (
                <Button
                  onClick={handleRegister}
                  loading={isRegistering}
                  className="w-full"
                >
                  Confirm Registration
                </Button>
              )}

              <p className="text-[11px] text-zinc-500 text-center leading-normal">
                By registering, you commit to upholding the standardized anti-cheat code of conduct.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
