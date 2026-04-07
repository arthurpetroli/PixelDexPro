import { TypeBadge } from '@/components/pokemon/TypeBadge';
import { AlertTriangle, Shield, Zap } from 'lucide-react';
import { cn } from '@/utils/helpers';

interface CoverageSummaryProps {
  weaknesses: Record<string, number>;
  resistances: Record<string, number>;
  immunities: string[];
  sharedWeaknesses: Record<string, string[]>;
  problematicTypes: string[];
  coverageScore: number;
  defensiveScore: number;
  summary: string;
  className?: string;
}

export function CoverageSummary({
  weaknesses,
  resistances,
  immunities,
  sharedWeaknesses,
  problematicTypes,
  coverageScore,
  defensiveScore,
  summary,
  className,
}: CoverageSummaryProps) {
  const getScoreColor = (score: number) => {
    if (score >= 70) return 'text-green-600';
    if (score >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className={cn('space-y-6', className)}>
      {/* Scores */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-100">
          <div className="flex items-center gap-2 mb-2">
            <Shield className="w-5 h-5 text-blue-500" />
            <span className="text-sm font-medium text-gray-600">Defensive Score</span>
          </div>
          <div className={cn('text-3xl font-bold', getScoreColor(defensiveScore))}>
            {defensiveScore.toFixed(0)}
          </div>
        </div>
        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-100">
          <div className="flex items-center gap-2 mb-2">
            <Zap className="w-5 h-5 text-yellow-500" />
            <span className="text-sm font-medium text-gray-600">Coverage Score</span>
          </div>
          <div className={cn('text-3xl font-bold', getScoreColor(coverageScore))}>
            {coverageScore.toFixed(0)}
          </div>
        </div>
      </div>

      {/* Summary */}
      <div className="bg-blue-50 rounded-lg p-4">
        <p className="text-sm text-blue-800">{summary}</p>
      </div>

      {/* Problematic Types */}
      {problematicTypes.length > 0 && (
        <div className="bg-red-50 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-3">
            <AlertTriangle className="w-5 h-5 text-red-500" />
            <h4 className="font-semibold text-red-700">Problematic Types</h4>
          </div>
          <div className="flex flex-wrap gap-2">
            {problematicTypes.map((type) => (
              <TypeBadge key={type} type={type} size="md" />
            ))}
          </div>
        </div>
      )}

      {/* Shared Weaknesses */}
      {Object.keys(sharedWeaknesses).length > 0 && (
        <div>
          <h4 className="font-semibold text-gray-700 mb-3">Shared Weaknesses</h4>
          <div className="space-y-2">
            {Object.entries(sharedWeaknesses).map(([type, pokemon]) => (
              <div key={type} className="flex items-center gap-3 bg-orange-50 rounded-lg p-3">
                <TypeBadge type={type} size="sm" />
                <span className="text-sm text-gray-600">
                  {pokemon.length} Pokémon weak: {pokemon.join(', ')}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Immunities */}
      {immunities.length > 0 && (
        <div>
          <h4 className="font-semibold text-gray-700 mb-3">Team Immunities</h4>
          <div className="flex flex-wrap gap-2">
            {immunities.map((type) => (
              <TypeBadge key={type} type={type} size="md" />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
