import { Heart } from 'lucide-react';
import { useFavoritesStore } from '@/store';
import { cn } from '@/utils/helpers';

interface FavoriteButtonProps {
  pokemonId: number;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export function FavoriteButton({ pokemonId, size = 'md', className }: FavoriteButtonProps) {
  const { isFavorite, addFavorite, removeFavorite } = useFavoritesStore();
  const favorite = isFavorite(pokemonId);

  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (favorite) {
      removeFavorite(pokemonId);
    } else {
      addFavorite(pokemonId);
    }
  };

  const sizeClasses = {
    sm: 'p-1.5',
    md: 'p-2',
    lg: 'p-3',
  };

  const iconSizes = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
  };

  return (
    <button
      onClick={handleClick}
      className={cn(
        'rounded-full bg-white/80 hover:bg-white transition-all hover:scale-110',
        sizeClasses[size],
        className
      )}
      title={favorite ? 'Remove from favorites' : 'Add to favorites'}
    >
      <Heart
        className={cn(
          iconSizes[size],
          'transition-colors',
          favorite ? 'fill-red-500 text-red-500' : 'text-gray-400 hover:text-red-400'
        )}
      />
    </button>
  );
}
