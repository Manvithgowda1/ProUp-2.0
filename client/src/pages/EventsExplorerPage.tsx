import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Search, 
  Filter, 
  Calendar, 
  MapPin, 
  Users, 
  LayoutGrid, 
  List, 
  ArrowRight,
  ShieldCheck,
  CheckCircle2
} from 'lucide-react';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Card, CardHeader, CardContent, CardFooter } from '@/components/ui/Card';
import { eventsService } from '@/services/events';
import { EventResponse } from '@/types';
import { useToast } from '@/components/ui/Toast';

export default function EventsExplorerPage() {
  const [events, setEvents] = useState<EventResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedType, setSelectedType] = useState('ALL');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const { toast } = useToast();
  const navigate = useNavigate();

  const eventTypes = [
    { label: 'All Challenges', value: 'ALL' },
    { label: 'Hiring Challenge', value: 'HIRING_CHALLENGE' },
    { label: 'Hackathon', value: 'HACKATHON' },
    { label: 'Competition', value: 'COMPETITION' },
    { label: 'Workshop', value: 'WORKSHOP' },
  ];

  useEffect(() => {
    fetchEvents();
  }, [selectedType, page]);

  const fetchEvents = async () => {
    try {
      setIsLoading(true);
      const params: any = { page, limit: 9 };
      if (selectedType !== 'ALL') params.event_type = selectedType;
      if (searchTerm) params.search = searchTerm;

      const res = await eventsService.getEvents(params);
      setEvents(res.items || []);
      setTotalPages(Math.ceil((res.total || 0) / 9) || 1);
    } catch (err: any) {
      toast('error', 'Unable to retrieve events from platform.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    fetchEvents();
  };

  const formatDate = (dateStr: string) => {
    if (!dateStr) return 'TBA';
    const d = new Date(dateStr);
    return d.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8 bg-zinc-50">
      <div className="container-main">
        {/* Header Title */}
        <div className="border-b border-zinc-200 pb-8 mb-8">
          <p className="text-xs font-mono uppercase tracking-widest text-zinc-500 mb-1">Competitive Catalog</p>
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h1 className="text-4xl font-extrabold tracking-tight text-black">Active Events & Challenges</h1>
              <p className="text-sm text-zinc-600 mt-1">Discover, qualify, and compete in standardized corporate hiring drives</p>
            </div>
            <div className="flex items-center gap-2">
              <Button
                variant={viewMode === 'grid' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setViewMode('grid')}
              >
                <LayoutGrid className="w-4 h-4" />
              </Button>
              <Button
                variant={viewMode === 'list' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setViewMode('list')}
              >
                <List className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>

        {/* Filter & Search Bar */}
        <div className="bg-white border border-zinc-200 rounded-xl p-4 sm:p-6 mb-8 shadow-sm space-y-4">
          <form onSubmit={handleSearchSubmit} className="flex flex-col sm:flex-row gap-3">
            <div className="relative flex-1">
              <Input
                placeholder="Search challenges by title, skills or keywords..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                icon={Search}
                className="w-full"
              />
            </div>
            <Button type="submit" className="shrink-0">
              Search
            </Button>
          </form>

          {/* Type Filter Pills */}
          <div className="flex items-center gap-2 overflow-x-auto pb-1 pt-2">
            <span className="text-xs font-mono uppercase tracking-wider text-zinc-400 mr-2 shrink-0">Filter:</span>
            {eventTypes.map((t) => (
              <button
                key={t.value}
                type="button"
                onClick={() => { setSelectedType(t.value); setPage(1); }}
                className={`text-xs font-mono uppercase tracking-wider px-3 py-1.5 rounded-full border whitespace-nowrap transition-all ${
                  selectedType === t.value
                    ? 'bg-black text-white border-black font-semibold'
                    : 'bg-white border-zinc-200 text-zinc-600 hover:border-black'
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>
        </div>

        {/* Event Cards Grid / List */}
        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map((n) => (
              <div key={n} className="border border-zinc-200 rounded-xl bg-white p-6 animate-pulse space-y-4">
                <div className="h-4 bg-zinc-200 rounded w-1/3" />
                <div className="h-6 bg-zinc-200 rounded w-3/4" />
                <div className="h-16 bg-zinc-100 rounded" />
                <div className="h-8 bg-zinc-200 rounded" />
              </div>
            ))}
          </div>
        ) : events.length === 0 ? (
          <div className="text-center py-24 bg-white border border-zinc-200 rounded-xl">
            <ShieldCheck className="w-12 h-12 text-zinc-300 mx-auto mb-3" />
            <h3 className="text-lg font-bold text-black">No events match the current filter</h3>
            <p className="text-sm text-zinc-500 mt-1 max-w-sm mx-auto">
              Modify your keyword query or select another competitive category to view upcoming rounds.
            </p>
            <Button
              variant="outline"
              size="sm"
              className="mt-6"
              onClick={() => { setSelectedType('ALL'); setSearchTerm(''); }}
            >
              Reset Filters
            </Button>
          </div>
        ) : viewMode === 'grid' ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {events.map((ev) => (
              <Card key={ev.event_id} className="flex flex-col justify-between hover:border-black transition-all">
                <CardHeader className="space-y-3">
                  <div className="flex items-center justify-between gap-2">
                    <Badge variant="outline" className="font-mono text-[10px]">
                      {ev.event_type.replace('_', ' ')}
                    </Badge>
                    <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded border border-zinc-200 bg-zinc-50 text-zinc-600">
                      {ev.event_mode}
                    </span>
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-black tracking-tight line-clamp-1 hover:underline cursor-pointer" onClick={() => navigate(`/events/${ev.event_id}`)}>
                      {ev.title}
                    </h3>
                    <p className="text-xs font-mono text-zinc-500 mt-1">
                      {ev.organization?.name || 'Verified Enterprise Host'}
                    </p>
                  </div>
                </CardHeader>

                <CardContent>
                  <p className="text-sm text-zinc-600 line-clamp-2 leading-relaxed">
                    {ev.description}
                  </p>

                  <div className="mt-4 pt-4 border-t border-zinc-100 space-y-2 text-xs text-zinc-600 font-mono">
                    <div className="flex items-center gap-2">
                      <Calendar className="w-3.5 h-3.5 text-black" />
                      <span>Date: {formatDate(ev.event_date)}</span>
                    </div>
                    {ev.location && (
                      <div className="flex items-center gap-2">
                        <MapPin className="w-3.5 h-3.5 text-black" />
                        <span className="truncate">{ev.location}</span>
                      </div>
                    )}
                    <div className="flex items-center gap-2">
                      <Users className="w-3.5 h-3.5 text-black" />
                      <span>Capacity: {ev.max_participants ? `${ev.max_participants} candidates` : 'Open'}</span>
                    </div>
                  </div>
                </CardContent>

                <CardFooter className="pt-0">
                  <Button
                    onClick={() => navigate(`/events/${ev.event_id}`)}
                    className="w-full"
                    size="sm"
                  >
                    View Round Details <ArrowRight className="w-3.5 h-3.5 ml-2" />
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
        ) : (
          <div className="space-y-4">
            {events.map((ev) => (
              <div
                key={ev.event_id}
                className="bg-white border border-zinc-200 rounded-xl p-6 hover:border-black transition-all flex flex-col md:flex-row md:items-center justify-between gap-6"
              >
                <div className="space-y-2 flex-1">
                  <div className="flex items-center gap-2">
                    <Badge variant="outline" className="font-mono text-[10px]">
                      {ev.event_type.replace('_', ' ')}
                    </Badge>
                    <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded border border-zinc-200 bg-zinc-50 text-zinc-600">
                      {ev.event_mode}
                    </span>
                    <span className="text-xs font-mono text-zinc-400">•</span>
                    <span className="text-xs font-mono text-zinc-500">{formatDate(ev.event_date)}</span>
                  </div>
                  <h3 className="text-xl font-bold text-black tracking-tight">{ev.title}</h3>
                  <p className="text-sm text-zinc-600 line-clamp-2">{ev.description}</p>
                </div>

                <div className="flex items-center gap-4 shrink-0">
                  <div className="text-right text-xs font-mono text-zinc-500 hidden sm:block">
                    <p>{ev.organization?.name || 'Verified Host'}</p>
                    <p>{ev.max_participants ? `${ev.max_participants} seats` : 'Open cap'}</p>
                  </div>
                  <Button onClick={() => navigate(`/events/${ev.event_id}`)} size="sm">
                    Enter <ArrowRight className="w-3.5 h-3.5 ml-2" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Pagination Bar */}
        {totalPages > 1 && (
          <div className="mt-12 flex items-center justify-center gap-4">
            <Button
              variant="outline"
              size="sm"
              disabled={page <= 1}
              onClick={() => setPage((p) => Math.max(1, p - 1))}
            >
              Previous Page
            </Button>
            <span className="text-xs font-mono text-zinc-600">
              Page {page} of {totalPages}
            </span>
            <Button
              variant="outline"
              size="sm"
              disabled={page >= totalPages}
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
            >
              Next Page
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
