import { Link } from 'react-router-dom';
import { Heart } from 'lucide-react';
import { motion } from 'framer-motion';
import { TypeBadge } from './TypeBadge';
import { formatPokemonName, formatPokedexNumber, getTypeColor } from '@/utils/pokemon';
import { useFavoritesStore } from '@/store';
import type { PokemonListItem } from '@/types';
import { cn } from '@/utils/helpers';

interface PokemonCardProps {
  pokemon: PokemonListItem;
  showFavorite?: boolean;
  className?: string;
}

export function PokemonCard({ pokemon, showFavorite = true, className }: PokemonCardProps) {
  const { isFavorite, addFavorite, removeFavorite } = useFavoritesStore();
  const favorite = isFavorite(pokemon.id);
  const primaryType = pokemon.types[0]?.type.name || 'normal';

  const handleFavoriteClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (favorite) {
      removeFavorite(pokemon.id);
    } else {
      addFavorite(pokemon.id);
    }
  };

  return (
    <Link
      to={`/pokemon/${pokemon.id}`}
      className={cn('block relative', className)}
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        whileHover={{ y: -8, scale: 1.02 }}
        transition={{ duration: 0.2 }}
        className="rounded-xl overflow-hidden shadow-md hover:shadow-2xl transition-shadow"
        style={{
          background: `linear-gradient(135deg, ${getTypeColor(primaryType)}40 0%, ${getTypeColor(primaryType)}20 100%)`,
        }}
      >
        {/* Favorite button */}
        {showFavorite && (
          <motion.button
            onClick={handleFavoriteClick}
            className="absolute top-2 right-2 z-10 p-1.5 rounded-full bg-white/80 dark:bg-gray-800/80 hover:bg-white dark:hover:bg-gray-700 transition-colors"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
          >
            <Heart
              className={cn('w-5 h-5', favorite ? 'fill-red-500 text-red-500' : 'text-gray-400')}
            />
          </motion.button>
        )}

        {/* Pokédex number */}
        <div className="absolute top-2 left-2 text-sm font-bold text-gray-600/60 dark:text-gray-300/60">
          {formatPokedexNumber(pokemon.pokedex_number)}
        </div>

        {/* Sprite */}
        <div className="flex justify-center pt-8 pb-2">
          <motion.img
            src={pokemon.sprite_url || '/placeholder-pokemon.png'}
            alt={pokemon.name}
            className="w-24 h-24 object-contain drop-shadow-lg"
            loading="lazy"
            whileHover={{ scale: 1.1, rotate: 5 }}
            transition={{ duration: 0.2 }}
          />
        </div>

        {/* Info */}
        <div className="p-3 bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm">
          <h3 className="font-bold text-gray-800 dark:text-white truncate">
            {formatPokemonName(pokemon.name)}
          </h3>
          <div className="flex gap-1 mt-2">
            {pokemon.types.map((t) => (
              <TypeBadge key={t.type.name} type={t.type.name} size="sm" />
            ))}
          </div>
        </div>
      </motion.div>
    </Link>
  );
}
