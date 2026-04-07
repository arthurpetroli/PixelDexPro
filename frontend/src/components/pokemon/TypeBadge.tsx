import { getTypeColor, getTypeTextColor } from '@/utils/pokemon';
import { cn } from '@/utils/helpers';

interface TypeBadgeProps {
  type: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export function TypeBadge({ type, size = 'md', className }: TypeBadgeProps) {
  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-3 py-1 text-sm',
    lg: 'px-4 py-1.5 text-base',
  };

  return (
    <span
      className={cn(
        'inline-flex items-center justify-center rounded-full font-medium capitalize',
        sizeClasses[size],
        className
      )}
      style={{
        backgroundColor: getTypeColor(type),
        color: getTypeTextColor(type),
      }}
    >
      {type}
    </span>
  );
}
