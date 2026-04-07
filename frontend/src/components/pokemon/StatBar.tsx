import { getStatColor, getStatPercentage, formatStatName } from '@/utils/pokemon';
import { cn } from '@/utils/helpers';

interface StatBarProps {
  name?: string;
  value: number;
  maxValue?: number;
  showValue?: boolean;
  variant?: 'default' | 'success' | 'danger';
  className?: string;
}

export function StatBar({ 
  name, 
  value, 
  maxValue = 255, 
  showValue = true, 
  variant = 'default',
  className 
}: StatBarProps) {
  const percentage = getStatPercentage(value, maxValue);
  
  let color: string;
  if (variant === 'success') {
    color = '#10b981'; // green-500
  } else if (variant === 'danger') {
    color = '#ef4444'; // red-500
  } else {
    color = getStatColor(value);
  }

  return (
    <div className={cn('flex items-center gap-3', className)}>
      {name && (
        <span className="w-20 text-sm font-medium text-gray-600 dark:text-gray-400">{formatStatName(name)}</span>
      )}
      {showValue && (
        <span className="w-10 text-sm font-bold text-right text-gray-900 dark:text-white">{value}</span>
      )}
      <div className="flex-1 h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-300"
          style={{
            width: `${percentage}%`,
            backgroundColor: color,
          }}
        />
      </div>
    </div>
  );
}

interface StatsDisplayProps {
  stats: {
    hp: number;
    attack: number;
    defense: number;
    special_attack: number;
    special_defense: number;
    speed: number;
    total: number;
  };
  className?: string;
}

export function StatsDisplay({ stats, className }: StatsDisplayProps) {
  const statList = [
    { name: 'hp', value: stats.hp },
    { name: 'attack', value: stats.attack },
    { name: 'defense', value: stats.defense },
    { name: 'special_attack', value: stats.special_attack },
    { name: 'special_defense', value: stats.special_defense },
    { name: 'speed', value: stats.speed },
  ];

  return (
    <div className={cn('space-y-2', className)}>
      {statList.map((stat) => (
        <StatBar key={stat.name} name={stat.name} value={stat.value} />
      ))}
      <div className="pt-2 border-t border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-3">
          <span className="w-20 text-sm font-medium text-gray-600 dark:text-gray-400">Total</span>
          <span className="w-10 text-sm font-bold text-right text-gray-900 dark:text-white">{stats.total}</span>
          <div className="flex-1" />
        </div>
      </div>
    </div>
  );
}
