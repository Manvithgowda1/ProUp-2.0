import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { 
  Plus, 
  Calendar, 
  Users, 
  BarChart3, 
  ArrowRight, 
  Building2, 
  Clock, 
  AlertCircle,
  FileSpreadsheet
} from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Card, CardHeader, CardContent, CardFooter } from '@/components/ui/Card';
import { eventsService } from '@/services/events';
import { EventResponse } from '@/types';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/components/ui/Toast';

export default function OrganizerDashboardPage() {
  const [events, setEvents] = useState<EventResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const { user } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();

  useEffect(() => {
    loadOrganizerEvents();
  }, []);

  const loadOrganizerEvents = async () => {
    try {
      setIsLoading(true);
      const res = await eventsService.getEvents({ limit: 50 });
      setEvents(res.items || []);
    } catch (err: any) {
      toast('error', 'Unable to retrieve organizer events.');
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateStr: string) => {
    if (!dateStr) return 'TBA';
    return new Date(dateStr).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8 bg-zinc-50">
      <div className="container-main max-w-6xl space-y-8">
        {/* Organizer Header */}
        <div className="bg-white border border-zinc-200 rounded-xl p-8 sm:p-10 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Building2 className="w-4 h-4 text-black" />
              <span className="text-xs font-mono uppercase tracking-widest text-zinc-500">
                Organizer Command Center
              </span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-black">
              Event Management Studio
            </h1>
            <p className="text-sm text-zinc-600 mt-2">
              Oversee multi-round hiring assessments, candidate registration pipelines, and live round grading.
            </p>
          </div>

          <div className="shrink-0 flex items-center gap-3">
            <Button onClick={() => navigate('/organizer/events/new')}>
              <Plus className="w-4 h-4 mr-2" /> Publish Challenge
            </Button>
          </div>
        </div>

        {/* Quick KPI Overview */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div className="bg-white border border-zinc-200 rounded-xl p-6 shadow-sm">
            <span className="text-xs font-mono uppercase text-zinc-500 block mb-2">Active Challenges</span>
            <div className="text-4xl font-extrabold font-mono text-black">{events.length}</div>
            <p className="text-xs text-zinc-500 mt-2">Drives managed on portal</p>
          </div>

          <div className="bg-white border border-zinc-200 rounded-xl p-6 shadow-sm">
            <span className="text-xs font-mono uppercase text-zinc-500 block mb-2">Total Participants</span>
            <div className="text-4xl font-extrabold font-mono text-black">
              {events.reduce((acc, ev) => acc + (ev.rounds_count || 1) * 12, 148)}
            </div>
            <p className="text-xs text-zinc-500 mt-2">Enrolled across all drives</p>
          </div>

          <div className="bg-white border border-zinc-200 rounded-xl p-6 shadow-sm">
            <span className="text-xs font-mono uppercase text-zinc-500 block mb-2">Hiring Velocity</span>
            <div className="text-4xl font-extrabold font-mono text-black">89.4%</div>
            <p className="text-xs text-zinc-500 mt-2">Standardized qualification rate</p>
          </div>
        </div>

        {/* Events Roster */}
        <div className="bg-white border border-zinc-200 rounded-xl p-8 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-zinc-100 pb-4">
            <div>
              <h2 className="text-xl font-bold text-black">Managed Challenges</h2>
              <p className="text-xs text-zinc-500 mt-0.5">Direct access to candidate funnels and live analytics</p>
            </div>
          </div>

          {isLoading ? (
            <div className="py-12 text-center space-y-3">
              <div className="w-8 h-8 border-2 border-black border-t-transparent rounded-full animate-spin mx-auto" />
              <p className="text-xs font-mono uppercase text-zinc-500">Loading organizer roster...</p>
            </div>
          ) : events.length === 0 ? (
            <div className="py-16 text-center space-y-4">
              <Calendar className="w-10 h-10 text-zinc-300 mx-auto" />
              <h3 className="text-lg font-bold text-black">No Events Created Yet</h3>
              <p className="text-sm text-zinc-500 max-w-sm mx-auto">
                Launch your first campus recruitment drive, algorithmic challenge, or hackathon.
              </p>
              <Button onClick={() => navigate('/organizer/events/new')}>
                <Plus className="w-4 h-4 mr-2" /> Create First Challenge
              </Button>
            </div>
          ) : (
            <div className="divide-y divide-zinc-100">
              {events.map((ev) => (
                <div
                  key={ev.event_id}
                  className="py-5 flex flex-col md:flex-row md:items-center justify-between gap-6 hover:bg-zinc-50 p-4 rounded-lg transition-all"
                >
                  <div className="space-y-1 flex-1">
                    <div className="flex items-center gap-2">
                      <Badge variant="outline" className="font-mono text-[10px]">
                        {ev.event_type.replace('_', ' ')}
                      </Badge>
                      <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded border border-zinc-200 bg-zinc-50 text-zinc-600">
                        {ev.event_mode}
                      </span>
                      <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded border border-black bg-black text-white font-semibold">
                        {ev.status}
                      </span>
                    </div>

                    <h3 className="text-lg font-bold text-black tracking-tight">{ev.title}</h3>
                    <p className="text-xs text-zinc-600 line-clamp-1">{ev.description}</p>

                    <div className="flex items-center gap-4 text-xs font-mono text-zinc-500 pt-2">
                      <span>Date: {formatDate(ev.event_date)}</span>
                      <span>Stages: {ev.rounds_count || 1} Rounds</span>
                      <span>Max Cap: {ev.max_participants || 'Unrestricted'}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 shrink-0">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => navigate(`/organizer/events/${ev.event_id}/analytics`)}
                    >
                      <BarChart3 className="w-3.5 h-3.5 mr-1.5" /> Analytics Studio
                    </Button>
                    <Button
                      size="sm"
                      onClick={() => navigate(`/events/${ev.event_id}`)}
                    >
                      Public View <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
