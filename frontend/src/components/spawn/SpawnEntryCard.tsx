import type { Spawn } from '@/types';
import { formatPokemonName } from '@/utils/pokemon';
import { MapPin, Clock, Cloud, Layers } from 'lucide-react';
import { cn } from '@/utils/helpers';

interface SpawnEntryCardProps {
  spawn: Spawn;
  showPokemonName?: boolean;
  className?: string;
}

export function SpawnEntryCard({ spawn, showPokemonName = false, className }: SpawnEntryCardProps) {
  return (
    <div className={cn('bg-white rounded-lg border border-gray-200 p-4', className)}>
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        {showPokemonName && spawn.pokemon_name && (
          <h4 className="font-semibold text-gray-800">
            {formatPokemonName(spawn.pokemon_name)}
          </h4>
        )}
        <div className="flex items-center gap-2 text-sm text-gray-500">
          {spawn.entry_number && (
            <span className="px-2 py-0.5 bg-gray-100 rounded">Entry #{spawn.entry_number}</span>
          )}
          {spawn.bucket && (
            <span className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded capitalize">
              {spawn.bucket}
            </span>
          )}
        </div>
      </div>

      {/* Level Range */}
      {(spawn.min_level || spawn.max_level) && (
        <div className="mb-3 text-sm">
          <span className="font-medium text-gray-600">Level: </span>
          <span className="text-gray-800">
            {spawn.min_level || '?'} - {spawn.max_level || '?'}
          </span>
        </div>
      )}

      {/* Info Grid */}
      <div className="grid grid-cols-2 gap-3 text-sm">
        {/* Biomes */}
        {spawn.biomes.length > 0 && (
          <div className="col-span-2">
            <div className="flex items-center gap-1.5 text-gray-600 mb-1">
              <MapPin className="w-4 h-4" />
              <span className="font-medium">Biomes</span>
            </div>
            <div className="flex flex-wrap gap-1">
              {spawn.biomes.slice(0, 5).map((biome) => (
                <span
                  key={biome}
                  className="px-2 py-0.5 bg-green-100 text-green-700 rounded text-xs"
                >
                  {biome}
                </span>
              ))}
              {spawn.biomes.length > 5 && (
                <span className="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-xs">
                  +{spawn.biomes.length - 5} more
                </span>
              )}
            </div>
          </div>
        )}

        {/* Time */}
        {spawn.time && (
          <div>
            <div className="flex items-center gap-1.5 text-gray-600 mb-1">
              <Clock className="w-4 h-4" />
              <span className="font-medium">Time</span>
            </div>
            <span className="capitalize">{spawn.time}</span>
          </div>
        )}

        {/* Weather */}
        {spawn.weather.length > 0 && (
          <div>
            <div className="flex items-center gap-1.5 text-gray-600 mb-1">
              <Cloud className="w-4 h-4" />
              <span className="font-medium">Weather</span>
            </div>
            <span className="capitalize">{spawn.weather.join(', ')}</span>
          </div>
        )}

        {/* Context */}
        {spawn.context && (
          <div>
            <div className="flex items-center gap-1.5 text-gray-600 mb-1">
              <Layers className="w-4 h-4" />
              <span className="font-medium">Context</span>
            </div>
            <span className="capitalize">{spawn.context}</span>
          </div>
        )}
      </div>

      {/* Conditions */}
      {spawn.conditions.length > 0 && (
        <div className="mt-3 pt-3 border-t border-gray-100">
          <span className="text-xs font-medium text-gray-500">Conditions: </span>
          <span className="text-xs text-gray-600">{spawn.conditions.join(', ')}</span>
        </div>
      )}

      {/* Anticonditions */}
      {spawn.anticonditions.length > 0 && (
        <div className="mt-2">
          <span className="text-xs font-medium text-red-500">Cannot spawn if: </span>
          <span className="text-xs text-gray-600">{spawn.anticonditions.join(', ')}</span>
        </div>
      )}
    </div>
  );
}
