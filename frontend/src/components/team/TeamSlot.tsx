import { Plus, X } from 'lucide-react';
import { TypeBadge } from '@/components/pokemon/TypeBadge';
import { formatPokemonName, getTypeColor } from '@/utils/pokemon';
import type { PokemonListItem, PokemonDetails } from '@/types';
import { cn } from '@/utils/helpers';

interface TeamSlotProps {
  slot: number;
  pokemon: PokemonListItem | null;
  details: PokemonDetails | null;
  onAdd: () => void;
  onRemove: () => void;
  className?: string;
}

export function TeamSlot({
  slot,
  pokemon,
  details,
  onAdd,
  onRemove,
  className,
}: TeamSlotProps) {
  if (!pokemon) {
    return (
      <button
        onClick={onAdd}
        className={cn(
          'flex flex-col items-center justify-center gap-2 p-4 rounded-xl border-2 border-dashed border-gray-300 hover:border-blue-400 hover:bg-blue-50 transition-all min-h-[160px]',
          className
        )}
      >
        <Plus className="w-8 h-8 text-gray-400" />
        <span className="text-sm text-gray-500">Add Pokémon</span>
        <span className="text-xs text-gray-400">Slot {slot + 1}</span>
      </button>
    );
  }

  const primaryType = pokemon.types[0]?.type.name || 'normal';

  return (
    <div
      className={cn(
        'relative rounded-xl overflow-hidden shadow-md min-h-[160px]',
        className
      )}
      style={{
        background: `linear-gradient(135deg, ${getTypeColor(primaryType)}40 0%, ${getTypeColor(primaryType)}20 100%)`,
      }}
    >
      {/* Remove button */}
      <button
        onClick={onRemove}
        className="absolute top-2 right-2 z-10 p-1.5 rounded-full bg-white/80 hover:bg-red-100 transition-colors"
      >
        <X className="w-4 h-4 text-gray-500 hover:text-red-500" />
      </button>

      {/* Slot number */}
      <div className="absolute top-2 left-2 text-xs font-medium text-gray-500 bg-white/60 px-2 py-0.5 rounded">
        Slot {slot + 1}
      </div>

      {/* Sprite */}
      <div className="flex justify-center pt-8 pb-2">
        <img
          src={pokemon.sprite_url || '/placeholder-pokemon.png'}
          alt={pokemon.name}
          className="w-20 h-20 object-contain drop-shadow-lg"
        />
      </div>

      {/* Info */}
      <div className="p-3 bg-white/90 backdrop-blur-sm">
        <h4 className="font-bold text-gray-800 text-sm truncate">
          {formatPokemonName(pokemon.name)}
        </h4>
        <div className="flex gap-1 mt-1">
          {pokemon.types.map((t) => (
            <TypeBadge key={t.type.name} type={t.type.name} size="sm" />
          ))}
        </div>
      </div>
    </div>
  );
}
