import { Filter } from 'lucide-react';
import { useState } from 'react';

export interface SpawnFilterValues {
  biome?: string;
  time?: string;
  weather?: string;
  minLevel?: number;
  maxLevel?: number;
  context?: string;
}

interface SpawnFiltersProps {
  onFilterChange: (filters: SpawnFilterValues) => void;
  availableBiomes?: string[];
  className?: string;
}

const TIMES = ['DAY', 'NIGHT', 'DAWN', 'DUSK'];
const WEATHERS = ['CLEAR', 'RAIN', 'THUNDER', 'SNOW'];
const CONTEXTS = ['SURFACE', 'UNDERGROUND', 'WATER', 'AIR'];

export function SpawnFilters({
  onFilterChange,
  availableBiomes = [],
  className,
}: SpawnFiltersProps) {
  const [filters, setFilters] = useState<SpawnFilterValues>({});
  const [showFilters, setShowFilters] = useState(false);

  const handleFilterChange = (key: keyof SpawnFilterValues, value: any) => {
    const newFilters = { ...filters, [key]: value || undefined };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const clearFilters = () => {
    setFilters({});
    onFilterChange({});
  };

  const activeFilterCount = Object.values(filters).filter((v) => v !== undefined).length;

  return (
    <div className={className}>
      <button
        onClick={() => setShowFilters(!showFilters)}
        className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
      >
        <Filter className="w-4 h-4" />
        Filters
        {activeFilterCount > 0 && (
          <span className="px-2 py-0.5 text-xs bg-blue-600 text-white rounded-full">
            {activeFilterCount}
          </span>
        )}
      </button>

      {showFilters && (
        <div className="mt-4 p-4 bg-white rounded-lg border border-gray-200 space-y-4">
          {/* Biome Filter */}
          {availableBiomes.length > 0 && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Biome
              </label>
              <select
                value={filters.biome || ''}
                onChange={(e) => handleFilterChange('biome', e.target.value)}
                className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Biomes</option>
                {availableBiomes.map((biome) => (
                  <option key={biome} value={biome}>
                    {biome}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Time Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Time</label>
            <select
              value={filters.time || ''}
              onChange={(e) => handleFilterChange('time', e.target.value)}
              className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Any Time</option>
              {TIMES.map((time) => (
                <option key={time} value={time}>
                  {time}
                </option>
              ))}
            </select>
          </div>

          {/* Weather Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Weather
            </label>
            <select
              value={filters.weather || ''}
              onChange={(e) => handleFilterChange('weather', e.target.value)}
              className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Any Weather</option>
              {WEATHERS.map((weather) => (
                <option key={weather} value={weather}>
                  {weather}
                </option>
              ))}
            </select>
          </div>

          {/* Context Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Context
            </label>
            <select
              value={filters.context || ''}
              onChange={(e) => handleFilterChange('context', e.target.value)}
              className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Any Context</option>
              {CONTEXTS.map((context) => (
                <option key={context} value={context}>
                  {context}
                </option>
              ))}
            </select>
          </div>

          {/* Level Range */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Min Level
              </label>
              <input
                type="number"
                value={filters.minLevel || ''}
                onChange={(e) =>
                  handleFilterChange('minLevel', e.target.value ? Number(e.target.value) : undefined)
                }
                placeholder="1"
                min="1"
                max="100"
                className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Max Level
              </label>
              <input
                type="number"
                value={filters.maxLevel || ''}
                onChange={(e) =>
                  handleFilterChange('maxLevel', e.target.value ? Number(e.target.value) : undefined)
                }
                placeholder="100"
                min="1"
                max="100"
                className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          {/* Clear Button */}
          {activeFilterCount > 0 && (
            <button
              onClick={clearFilters}
              className="w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            >
              Clear All Filters
            </button>
          )}
        </div>
      )}
    </div>
  );
}
