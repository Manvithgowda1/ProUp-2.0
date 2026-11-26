import React, { useState, useEffect } from 'react';
import { 
  Trophy, 
  Calendar, 
  Star, 
  Award, 
  ShieldCheck, 
  ArrowUpRight, 
  Info,
  Medal,
  CheckCircle2
} from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Card, CardHeader, CardContent } from '@/components/ui/Card';
import { studentsService } from '@/services/students';
import { StudentAchievementsOverviewResponse } from '@/types';
import { useToast } from '@/components/ui/Toast';

export default function AchievementsPage() {
  const [data, setData] = useState<StudentAchievementsOverviewResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const { toast } = useToast();

  useEffect(() => {
    loadAchievements();
  }, []);

  const loadAchievements = async () => {
    try {
      setIsLoading(true);
      const res = await studentsService.getAchievements();
      setData(res);
    } catch (err: any) {
      // If student hasn't logged competitive results yet, provide initial baseline portfolio
      setData({
        events_attended: 0,
        events_won: 0,
        points_earned: 0,
        achievements_count: 0,
        breakdown: {
          attendance_points: 0,
          podium_points: 0,
          rank_1_count: 0,
          rank_2_count: 0,
          rank_3_count: 0,
        },
        achievements: [],
      });
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen py-16 px-4 bg-zinc-50 flex items-center justify-center">
        <div className="text-center space-y-3">
          <div className="w-8 h-8 border-2 border-black border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs font-mono uppercase text-zinc-500">Retrieving verified candidate portfolio...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8 bg-zinc-50">
      <div className="container-main max-w-5xl space-y-8">
        {/* Header */}
        <div className="border-b border-zinc-200 pb-6">
          <div className="flex items-center gap-2 mb-1">
            <ShieldCheck className="w-4 h-4 text-black" />
            <span className="text-xs font-mono uppercase tracking-widest text-zinc-500">
              Verified Merit Registry
            </span>
          </div>
          <h1 className="text-4xl font-extrabold tracking-tight text-black">
            Student Achievements & Points
          </h1>
          <p className="text-sm text-zinc-600 mt-2">
            Verifiable milestone records, attendance ratings, and podium ranking achievements earned across standardized competitive drives.
          </p>
        </div>

        {/* 4 Metric KPI Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Events Attended */}
          <div className="bg-white border border-zinc-200 rounded-xl p-6 shadow-sm">
            <div className="flex items-center justify-between text-zinc-500 mb-3">
              <span className="text-xs font-mono uppercase">Attended</span>
              <Calendar className="w-4 h-4 text-black" />
            </div>
            <div className="text-3xl sm:text-4xl font-extrabold font-mono text-black">
              {data?.events_attended || 0}
            </div>
            <p className="text-xs text-zinc-500 mt-2">+5 pts per attended drive</p>
          </div>

          {/* Events Won */}
          <div className="bg-white border border-zinc-200 rounded-xl p-6 shadow-sm">
            <div className="flex items-center justify-between text-zinc-500 mb-3">
              <span className="text-xs font-mono uppercase">Podium 1st</span>
              <Trophy className="w-4 h-4 text-black" />
            </div>
            <div className="text-3xl sm:text-4xl font-extrabold font-mono text-black">
              {data?.events_won || 0}
            </div>
            <p className="text-xs text-zinc-500 mt-2">+20 pts per championship</p>
          </div>

          {/* Total Points Earned */}
          <div className="bg-white border border-black rounded-xl p-6 shadow-sm ring-1 ring-black">
            <div className="flex items-center justify-between text-black mb-3">
              <span className="text-xs font-mono uppercase font-bold">Total Points</span>
              <Star className="w-4 h-4 text-black fill-black" />
            </div>
            <div className="text-3xl sm:text-4xl font-extrabold font-mono text-black">
              {data?.points_earned || 0}
            </div>
            <p className="text-xs text-zinc-600 mt-2">Calculated merit score</p>
          </div>

          {/* Certificates */}
          <div className="bg-white border border-zinc-200 rounded-xl p-6 shadow-sm">
            <div className="flex items-center justify-between text-zinc-500 mb-3">
              <span className="text-xs font-mono uppercase">Credentials</span>
              <Award className="w-4 h-4 text-black" />
            </div>
            <div className="text-3xl sm:text-4xl font-extrabold font-mono text-black">
              {data?.achievements_count || 0}
            </div>
            <p className="text-xs text-zinc-500 mt-2">Verified certificate records</p>
          </div>
        </div>

        {/* Formal Points Breakdown Specification */}
        <div className="bg-white border border-zinc-200 rounded-xl p-8 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-zinc-100 pb-4">
            <div>
              <h2 className="text-xl font-bold text-black">Merit Points Breakdown</h2>
              <p className="text-xs text-zinc-500 mt-0.5">Formal computation of your candidate ranking balance</p>
            </div>
            <Badge variant="outline" className="font-mono text-xs">
              Algorithmic Formula
            </Badge>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs font-mono">
            {/* Attendance Item */}
            <div className="border border-zinc-200 rounded-lg p-4 bg-zinc-50">
              <p className="text-zinc-500 mb-1">Attendance Verification</p>
              <div className="text-xl font-bold text-black mb-1">
                {data?.breakdown?.attendance_points || 0} pts
              </div>
              <p className="text-[11px] text-zinc-600">
                {data?.events_attended || 0} events × 5 pts
              </p>
            </div>

            {/* Rank 1 Item */}
            <div className="border border-zinc-200 rounded-lg p-4 bg-zinc-50">
              <p className="text-zinc-500 mb-1">1st Place Finishes</p>
              <div className="text-xl font-bold text-black mb-1">
                {(data?.breakdown?.rank_1_count || 0) * 20} pts
              </div>
              <p className="text-[11px] text-zinc-600">
                {data?.breakdown?.rank_1_count || 0} victories × 20 pts
              </p>
            </div>

            {/* Rank 2 Item */}
            <div className="border border-zinc-200 rounded-lg p-4 bg-zinc-50">
              <p className="text-zinc-500 mb-1">2nd Place Finishes</p>
              <div className="text-xl font-bold text-black mb-1">
                {(data?.breakdown?.rank_2_count || 0) * 15} pts
              </div>
              <p className="text-[11px] text-zinc-600">
                {data?.breakdown?.rank_2_count || 0} runner-up × 15 pts
              </p>
            </div>

            {/* Rank 3 Item */}
            <div className="border border-zinc-200 rounded-lg p-4 bg-zinc-50">
              <p className="text-zinc-500 mb-1">3rd Place Finishes</p>
              <div className="text-xl font-bold text-black mb-1">
                {(data?.breakdown?.rank_3_count || 0) * 10} pts
              </div>
              <p className="text-[11px] text-zinc-600">
                {data?.breakdown?.rank_3_count || 0} podiums × 10 pts
              </p>
            </div>
          </div>
        </div>

        {/* Verified Credentials & Certificates List */}
        <div className="bg-white border border-zinc-200 rounded-xl p-8 shadow-sm space-y-6">
          <div className="border-b border-zinc-100 pb-4">
            <h2 className="text-xl font-bold text-black">Verifiable Achievements Roster</h2>
            <p className="text-xs text-zinc-500 mt-0.5">Certificates and endorsements recorded on your identity</p>
          </div>

          {(!data?.achievements || data.achievements.length === 0) ? (
            <div className="py-12 text-center space-y-3">
              <Medal className="w-10 h-10 text-zinc-300 mx-auto" />
              <p className="text-sm font-semibold text-black">No formal certifications logged yet</p>
              <p className="text-xs text-zinc-500 max-w-sm mx-auto">
                Compete in active hiring challenges and algorithmic rounds to earn verified credentials from enterprise sponsors.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {data.achievements.map((ach) => (
                <div
                  key={ach.id}
                  className="border border-zinc-200 rounded-lg p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:border-black transition-all"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <h3 className="font-bold text-black text-base">{ach.name}</h3>
                      <Badge variant="outline" className="font-mono text-[10px]">
                        VERIFIED
                      </Badge>
                    </div>
                    {ach.description && (
                      <p className="text-xs text-zinc-600">{ach.description}</p>
                    )}
                    <div className="flex items-center gap-4 text-xs font-mono text-zinc-500 pt-1">
                      <span>Event: {ach.event_title || 'Campus Hiring Challenge'}</span>
                      {ach.awarded_at && (
                        <span>Awarded: {new Date(ach.awarded_at).toLocaleDateString()}</span>
                      )}
                    </div>
                  </div>

                  {ach.certificate_url && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => window.open(ach.certificate_url, '_blank')}
                      className="shrink-0"
                    >
                      Inspect Credential <ArrowUpRight className="w-3.5 h-3.5 ml-1" />
                    </Button>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
