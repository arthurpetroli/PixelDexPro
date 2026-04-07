import { TypeBadge } from './TypeBadge';
import { getMultiplierColor, getMultiplierText, ALL_TYPES } from '@/utils/pokemon';
import { cn } from '@/utils/helpers';

interface WeaknessChartProps {
  weaknesses: Record<string, number>;
  resistances: Record<string, number>;
  immunities: string[];
  quadrupleWeaknesses?: string[];
  quadrupleResistances?: string[];
  compact?: boolean;
  className?: string;
}

export function WeaknessChart({
  weaknesses,
  resistances,
  immunities,
  quadrupleWeaknesses = [],
  quadrupleResistances = [],
  compact = false,
  className,
}: WeaknessChartProps) {
  if (compact) {
    return (
      <div className={cn('space-y-4', className)}>
        {/* 4x Weaknesses */}
        {quadrupleWeaknesses.length > 0 && (
          <div>
            <h4 className="text-sm font-semibold text-red-600 dark:text-red-400 mb-2">4x Weak To</h4>
            <div className="flex flex-wrap gap-1">
              {quadrupleWeaknesses.map((type) => (
                <TypeBadge key={type} type={type} size="sm" />
              ))}
            </div>
          </div>
        )}

        {/* 2x Weaknesses */}
        {Object.keys(weaknesses).filter(t => !quadrupleWeaknesses.includes(t)).length > 0 && (
          <div>
            <h4 className="text-sm font-semibold text-orange-600 dark:text-orange-400 mb-2">2x Weak To</h4>
            <div className="flex flex-wrap gap-1">
              {Object.keys(weaknesses)
                .filter(t => !quadrupleWeaknesses.includes(t))
                .map((type) => (
                  <TypeBadge key={type} type={type} size="sm" />
                ))}
            </div>
          </div>
        )}

        {/* Resistances */}
        {Object.keys(resistances).length > 0 && (
          <div>
            <h4 className="text-sm font-semibold text-green-600 dark:text-green-400 mb-2">Resistant To</h4>
            <div className="flex flex-wrap gap-1">
              {Object.entries(resistances).map(([type, mult]) => (
                <div key={type} className="flex items-center gap-1">
                  <TypeBadge type={type} size="sm" />
                  <span className="text-xs text-gray-500 dark:text-gray-400">{getMultiplierText(mult)}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Immunities */}
        {immunities.length > 0 && (
          <div>
            <h4 className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-2">Immune To</h4>
            <div className="flex flex-wrap gap-1">
              {immunities.map((type) => (
                <TypeBadge key={type} type={type} size="sm" />
              ))}
            </div>
          </div>
        )}
      </div>
    );
  }

  // Full chart view
  return (
    <div className={cn('grid grid-cols-6 gap-2', className)}>
      {ALL_TYPES.map((type) => {
        const mult = immunities.includes(type)
          ? 0
          : weaknesses[type] || resistances[type] || 1;
        
        return (
          <div
            key={type}
            className="flex flex-col items-center p-2 rounded-lg"
            style={{ backgroundColor: getMultiplierColor(mult) + '20' }}
          >
            <TypeBadge type={type} size="sm" />
            <span
              className="text-xs font-bold mt-1"
              style={{ color: getMultiplierColor(mult) }}
            >
              {getMultiplierText(mult)}
            </span>
          </div>
        );
      })}
    </div>
  );
}
