import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  ArrowLeft, 
  Clock, 
  Terminal, 
  FileCheck2, 
  Users, 
  ShieldAlert, 
  ArrowRight,
  CheckCircle2,
  Calendar
} from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { eventsService } from '@/services/events';
import { EventResponse, RoundResponse } from '@/types';
import { useToast } from '@/components/ui/Toast';

export default function EventRoundsPage() {
  const { id } = useParams<{ id: string }>();
  const [event, setEvent] = useState<EventResponse | null>(null);
  const [rounds, setRounds] = useState<RoundResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const navigate = useNavigate();
  const { toast } = useToast();

  useEffect(() => {
    if (id) {
      loadPipeline(parseInt(id, 10));
    }
  }, [id]);

  const loadPipeline = async (eventId: number) => {
    try {
      setIsLoading(true);
      const [ev, rList] = await Promise.all([
        eventsService.getEvent(eventId),
        eventsService.getEventRounds(eventId),
      ]);
      setEvent(ev);
      // Sort rounds by round_number
      setRounds((rList || []).sort((a, b) => a.round_number - b.round_number));
    } catch (err: any) {
      toast('error', 'Unable to retrieve rounds pipeline.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleEnterArena = (round: RoundResponse) => {
    if (round.round_type === 'CODING') {
      // Direct student to coding problem arena (using round_id as context)
      navigate(`/coding/arena/${round.round_id}`);
    } else if (round.round_type === 'MCQ' || round.round_type === 'APTITUDE') {
      navigate(`/assessments/${round.round_id}`);
    } else {
      toast('info', `${round.round_type} rounds are coordinated directly with your interview panel.`);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen py-16 px-4 bg-zinc-50 flex items-center justify-center">
        <div className="text-center space-y-3">
          <div className="w-8 h-8 border-2 border-black border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs font-mono uppercase text-zinc-500">Loading multi-round challenge pipeline...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-10 px-4 sm:px-6 lg:px-8 bg-zinc-50">
      <div className="container-main max-w-4xl">
        {/* Navigation Breadcrumb */}
        <div className="mb-6">
          <Link
            to={event ? `/events/${event.event_id}` : '/events'}
            className="inline-flex items-center text-xs font-mono uppercase tracking-wider text-zinc-500 hover:text-black"
          >
            <ArrowLeft className="w-4 h-4 mr-1.5" /> Back to Challenge Brief
          </Link>
        </div>

        {/* Pipeline Header */}
        <div className="bg-white border border-zinc-200 rounded-xl p-8 mb-8 shadow-sm">
          <p className="text-xs font-mono uppercase tracking-widest text-zinc-500 mb-1">Live Evaluation Pipeline</p>
          <h1 className="text-3xl font-extrabold tracking-tight text-black">{event?.title}</h1>
          <p className="text-sm text-zinc-600 mt-2">
            Candidates must progress sequentially through standardized assessment rounds. All submissions are automatically evaluated.
          </p>
        </div>

        {/* Rounds Pipeline Timeline */}
        {rounds.length === 0 ? (
          <div className="bg-white border border-zinc-200 rounded-xl p-12 text-center">
            <ShieldAlert className="w-10 h-10 text-zinc-400 mx-auto mb-3" />
            <h3 className="text-lg font-bold text-black">No Rounds Scheduled</h3>
            <p className="text-sm text-zinc-500 mt-1">
              The organizer has not published the stages for this event yet. Check back closer to the challenge start time.
            </p>
          </div>
        ) : (
          <div className="space-y-6">
            {rounds.map((round, index) => {
              const isLive = round.status === 'LIVE';
              const isCompleted = round.status === 'COMPLETED';
              const isUpcoming = round.status === 'UPCOMING';

              return (
                <div key={round.round_id} className="relative">
                  {/* Vertical Connector Line */}
                  {index < rounds.length - 1 && (
                    <div className="absolute left-6 top-16 bottom-[-24px] w-[2px] bg-zinc-200 z-0" />
                  )}

                  <div className={`relative z-10 bg-white border ${isLive ? 'border-black ring-1 ring-black' : 'border-zinc-200'} rounded-xl p-6 sm:p-8 transition-all shadow-sm`}>
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-6">
                      <div className="flex items-start gap-5">
                        {/* Round Number Circle */}
                        <div className={`w-12 h-12 rounded-full border-2 flex items-center justify-center font-mono font-bold text-base shrink-0 ${
                          isLive 
                            ? 'bg-black text-white border-black' 
                            : isCompleted 
                            ? 'bg-zinc-100 text-black border-black' 
                            : 'bg-white text-zinc-400 border-zinc-300'
                        }`}>
                          {isCompleted ? <CheckCircle2 className="w-5 h-5 text-black" /> : `0${round.round_number}`}
                        </div>

                        {/* Round Details */}
                        <div className="space-y-1">
                          <div className="flex flex-wrap items-center gap-2">
                            <h2 className="text-xl font-bold text-black">{round.name}</h2>
                            <Badge variant="outline" className="font-mono text-xs">
                              {round.round_type}
                            </Badge>
                            <span className={`text-[10px] font-mono uppercase px-2 py-0.5 rounded border ${
                              isLive
                                ? 'bg-black text-white border-black font-semibold'
                                : isCompleted
                                ? 'bg-zinc-100 text-zinc-800 border-zinc-300'
                                : 'bg-zinc-50 text-zinc-500 border-zinc-200'
                            }`}>
                              {round.status}
                            </span>
                          </div>

                          <p className="text-sm text-zinc-600 leading-relaxed pt-1">
                            {round.description || 'Standard technical evaluation round.'}
                          </p>

                          <div className="flex flex-wrap items-center gap-4 text-xs font-mono text-zinc-500 pt-3">
                            <span className="flex items-center gap-1">
                              <Clock className="w-3.5 h-3.5 text-black" /> Duration: {round.duration_minutes} mins
                            </span>
                            <span>Total Score: {round.total_marks} pts</span>
                            <span>Pass Threshold: {round.passing_marks} pts</span>
                          </div>
                        </div>
                      </div>

                      {/* Action Button */}
                      <div className="shrink-0 sm:self-center">
                        {isLive ? (
                          <Button
                            onClick={() => handleEnterArena(round)}
                            size="md"
                            className="w-full sm:w-auto"
                          >
                            {round.round_type === 'CODING' ? (
                              <>
                                <Terminal className="w-4 h-4 mr-2" /> Enter Coding Arena
                              </>
                            ) : (
                              <>
                                <FileCheck2 className="w-4 h-4 mr-2" /> Start Assessment
                              </>
                            )}
                          </Button>
                        ) : isCompleted ? (
                          <span className="inline-flex items-center text-xs font-mono uppercase text-zinc-500 px-3 py-1.5 border border-zinc-200 rounded-md bg-zinc-50">
                            Evaluated
                          </span>
                        ) : (
                          <Button variant="outline" size="sm" disabled className="w-full sm:w-auto font-mono text-xs">
                            Scheduled
                          </Button>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
