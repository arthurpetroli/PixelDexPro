import { useState, useMemo } from 'react';
import { MapPin, Search, Filter, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { SearchBar } from '@/components/ui/SearchBar';
import { LoadingSpinner } from '@/components/ui/Loading';
import { useBiomesFromSheets, useSpawnsFromSheets } from '@/hooks/useApi';
import { cobblemonApi } from '@/services/api';
import { useQuery } from '@tanstack/react-query';

interface SpawnEntry {
  pokedex_number: number | null;
  pokemon_name: string;
  entry: string;
  bucket: string;
  weight: number | null;
  level_min: number | null;
  level_max: number | null;
  biomes: string[];
  excluded_biomes: string[];
  time: string;
  weather: string;
  context: string;
}

const bucketColors: Record<string, string> = {
  common: 'from-green-500 to-emerald-500',
  uncommon: 'from-blue-500 to-cyan-500',
  rare: 'from-purple-500 to-pink-500',
  'ultra-rare': 'from-amber-500 to-orange-500',
};

export default function SpawnFinder() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedBiome, setSelectedBiome] = useState<string>('');
  const [showFilters, setShowFilters] = useState(false);

  // Fetch biomes from Google Sheets
  const { data: biomes, isLoading: loadingBiomes } = useBiomesFromSheets();

  // Fetch all spawns
  const { data: allSpawns, isLoading: loadingSpawns } = useQuery({
    queryKey: ['spawns', 'sheets', 'all'],
    queryFn: () => cobblemonApi.getSpawnsFromSheets(),
    staleTime: 5 * 60 * 1000,
  });

  // Filter spawns based on search and biome
  const filteredSpawns = useMemo(() => {
    if (!allSpawns) return [];
    
    return allSpawns.filter((spawn: SpawnEntry) => {
      // Filter by search query
      if (searchQuery) {
        const query = searchQuery.toLowerCase();
        if (!spawn.pokemon_name.toLowerCase().includes(query)) {
          return false;
        }
      }
      
      // Filter by biome
      if (selectedBiome) {
        if (!spawn.biomes.includes(selectedBiome)) {
          return false;
        }
      }
      
      return true;
    });
  }, [allSpawns, searchQuery, selectedBiome]);

  // Group spawns by Pokemon
  const groupedSpawns = useMemo(() => {
    const groups: Record<string, SpawnEntry[]> = {};
    filteredSpawns.forEach((spawn: SpawnEntry) => {
      if (!groups[spawn.pokemon_name]) {
        groups[spawn.pokemon_name] = [];
      }
      groups[spawn.pokemon_name].push(spawn);
    });
    return groups;
  }, [filteredSpawns]);

  const pokemonNames = Object.keys(groupedSpawns).sort();

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div 
        className="flex flex-col md:flex-row md:items-center justify-between gap-4"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-xl bg-gradient-to-br from-green-500 to-emerald-600">
            <MapPin className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Spawn Finder</h1>
            <p className="text-gray-500 dark:text-gray-400">Find where Pokémon spawn in Cobblemon</p>
          </div>
        </div>
      </motion.div>

      {/* Search and Filters */}
      <motion.div 
        className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 space-y-4"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <div className="flex flex-col md:flex-row gap-4">
          {/* Search */}
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search Pokémon..."
              className="w-full pl-10 pr-4 py-3 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all"
            />
          </div>

          {/* Biome Filter */}
          <div className="w-full md:w-64">
            <select
              value={selectedBiome}
              onChange={(e) => setSelectedBiome(e.target.value)}
              className="w-full px-4 py-3 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all"
            >
              <option value="">All Biomes</option>
              {biomes?.map((biome) => (
                <option key={biome} value={biome}>
                  {biome}
                </option>
              ))}
            </select>
          </div>

          {/* Clear Filters */}
          {(searchQuery || selectedBiome) && (
            <motion.button
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              onClick={() => {
                setSearchQuery('');
                setSelectedBiome('');
              }}
              className="px-4 py-3 bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 rounded-xl hover:bg-red-200 dark:hover:bg-red-900/50 transition-colors flex items-center gap-2"
            >
              <X className="w-4 h-4" />
              Clear
            </motion.button>
          )}
        </div>

        {/* Results Count */}
        {allSpawns && (
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Showing {pokemonNames.length} Pokémon ({filteredSpawns.length} spawn entries)
          </p>
        )}
      </motion.div>

      {/* Loading State */}
      {loadingSpawns && (
        <div className="flex flex-col items-center justify-center py-12">
          <LoadingSpinner />
          <p className="mt-4 text-gray-500 dark:text-gray-400">Loading spawn data from Cobblemon...</p>
        </div>
      )}

      {/* Results */}
      {!loadingSpawns && pokemonNames.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <AnimatePresence>
            {pokemonNames.slice(0, 50).map((pokemonName, index) => {
              const spawns = groupedSpawns[pokemonName];
              const firstSpawn = spawns[0];
              const bucketColor = bucketColors[firstSpawn.bucket] || 'from-gray-500 to-gray-600';
              
              return (
                <motion.div
                  key={pokemonName}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  transition={{ delay: index * 0.02 }}
                  className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow"
                >
                  {/* Header */}
                  <div className={`bg-gradient-to-r ${bucketColor} p-4`}>
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-bold text-white capitalize">
                        {pokemonName}
                      </h3>
                      <span className="px-2 py-1 bg-white/20 rounded-lg text-sm text-white">
                        #{firstSpawn.pokedex_number || '???'}
                      </span>
                    </div>
                    <p className="text-white/80 text-sm mt-1">
                      {spawns.length} spawn {spawns.length === 1 ? 'entry' : 'entries'}
                    </p>
                  </div>

                  {/* Spawn Details */}
                  <div className="p-4 space-y-3">
                    {spawns.slice(0, 3).map((spawn, idx) => (
                      <div 
                        key={idx}
                        className="text-sm border-b border-gray-100 dark:border-gray-700 pb-3 last:border-0 last:pb-0"
                      >
                        <div className="flex flex-wrap gap-1 mb-2">
                          {spawn.biomes.slice(0, 3).map((biome) => (
                            <span
                              key={biome}
                              className="px-2 py-0.5 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 rounded text-xs"
                            >
                              {biome}
                            </span>
                          ))}
                          {spawn.biomes.length > 3 && (
                            <span className="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded text-xs">
                              +{spawn.biomes.length - 3} more
                            </span>
                          )}
                        </div>
                        <div className="flex flex-wrap gap-2 text-xs text-gray-600 dark:text-gray-400">
                          {spawn.level_min && spawn.level_max && (
                            <span>Lv. {spawn.level_min}-{spawn.level_max}</span>
                          )}
                          {spawn.time && spawn.time !== 'any' && (
                            <span className="flex items-center gap-1">
                              {spawn.time === 'day' ? '☀️' : spawn.time === 'night' ? '🌙' : '🌅'} {spawn.time}
                            </span>
                          )}
                          {spawn.weather && spawn.weather !== 'any' && (
                            <span className="flex items-center gap-1">
                              {spawn.weather === 'rain' ? '🌧️' : spawn.weather === 'snow' ? '❄️' : '⛈️'} {spawn.weather}
                            </span>
                          )}
                          {spawn.bucket && (
                            <span className="capitalize font-medium">{spawn.bucket}</span>
                          )}
                        </div>
                      </div>
                    ))}
                    {spawns.length > 3 && (
                      <p className="text-xs text-gray-500 dark:text-gray-400 text-center">
                        +{spawns.length - 3} more spawn entries
                      </p>
                    )}
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>
      )}

      {/* Empty State */}
      {!loadingSpawns && pokemonNames.length === 0 && (
        <motion.div 
          className="text-center py-12 bg-white dark:bg-gray-800 rounded-xl"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <MapPin className="w-16 h-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-2">
            No Spawns Found
          </h3>
          <p className="text-gray-500 dark:text-gray-400">
            Try adjusting your search or filters
          </p>
        </motion.div>
      )}

      {/* Load More Notice */}
      {pokemonNames.length > 50 && (
        <p className="text-center text-gray-500 dark:text-gray-400 text-sm">
          Showing first 50 results. Use search to find specific Pokémon.
        </p>
      )}
    </div>
  );
}
