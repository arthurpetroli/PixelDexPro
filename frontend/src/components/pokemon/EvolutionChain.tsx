import { ChevronRight } from 'lucide-react';
import { formatPokemonName } from '@/utils/pokemon';
import type { Evolution } from '@/types';
import { Link } from 'react-router-dom';

interface EvolutionChainProps {
  evolutions: Evolution[];
  currentPokemonId: number;
  className?: string;
}

export function EvolutionChain({
  evolutions,
  currentPokemonId,
  className,
}: EvolutionChainProps) {
  if (!evolutions || evolutions.length === 0) {
    return null;
  }

  return (
    <div className={className}>
      <h3 className="text-lg font-semibold text-gray-800 mb-3">Evolution Chain</h3>
      <div className="flex flex-wrap items-center gap-2">
        {evolutions.map((evo, index) => (
          <div key={evo.to_pokemon_id} className="flex items-center gap-2">
            {index > 0 && <ChevronRight className="w-5 h-5 text-gray-400" />}
            <Link
              to={`/pokemon/${evo.to_pokemon_id}`}
              className="group flex flex-col items-center p-3 bg-white rounded-lg border border-gray-200 hover:border-blue-400 hover:shadow-md transition-all"
            >
              <div className="text-sm font-medium text-gray-700 group-hover:text-blue-600">
                #{evo.to_pokemon_id}
              </div>
              {evo.trigger && (
                <div className="text-xs text-gray-500 mt-1">
                  {evo.trigger}
                  {evo.min_level && ` Lv${evo.min_level}`}
                  {evo.item && ` (${evo.item})`}
                </div>
              )}
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}
