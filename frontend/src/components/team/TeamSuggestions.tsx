import { useState } from 'react';
import { Sparkles, Zap, Shield, TrendingUp, ChevronDown, ChevronUp, X, Crown, Ban } from 'lucide-react';
import { teamsApi } from '@/services/api';
import { LoadingSpinner } from '@/components/ui/Loading';
import type { PokemonListItem } from '@/types';

interface TeamSuggestionsProps {
  onSelectPokemon: (pokemon: PokemonListItem) => void;
  currentTeamIds: number[];
  pokemonPool: 'all' | 'pixelmon';
  onClose: () => void;
}

interface SuggestionResult {
  id: number;
  name: string;
  pokedex_number: number;
  sprite_url: string;
  types: { name: string; slot: number }[];
  stats?: {
    hp: number;
    attack: number;
    defense: number;
    special_attack: number;
    special_defense: number;
    speed: number;
  };
  stat_total?: number;
  fit_score?: number;
  score?: number;
  reason?: string;
}

type Strategy = 'balanced' | 'offensive' | 'defensive' | 'stall';
type LegendaryFilter = 'all' | 'legendaries' | 'non-legendaries';

const strategies: { value: Strategy; label: string; icon: any; description: string }[] = [
  { 
    value: 'balanced', 
    label: 'Balanced', 
    icon: TrendingUp,
    description: 'Mix of offense and defense with good type coverage'
  },
  { 
    value: 'offensive', 
    label: 'Offensive', 
    icon: Zap,
    description: 'High attack and speed, focuses on dealing damage'
  },
  { 
    value: 'defensive', 
    label: 'Defensive', 
    icon: Shield,
    description: 'Tanky Pokemon with good resistances and HP'
  },
  { 
    value: 'stall', 
    label: 'Stall', 
    icon: Shield,
    description: 'Defensive setup with status moves and recovery'
  },
];

export function TeamSuggestions({ onSelectPokemon, currentTeamIds, pokemonPool, onClose }: TeamSuggestionsProps) {
  const [mode, setMode] = useState<'complete' | 'autocomplete'>('autocomplete');
  const [strategy, setStrategy] = useState<Strategy>('balanced');
  const [legendaryFilter, setLegendaryFilter] = useState<LegendaryFilter>('all');
  const [suggestions, setSuggestions] = useState<SuggestionResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  const includeLegendaries = legendaryFilter !== 'non-legendaries';

  const handleSuggestComplete = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await teamsApi.suggestComplete(
        strategy,
        undefined,
        includeLegendaries,
        legendaryFilter,
        pokemonPool
      );
      setSuggestions(result.suggestions || []);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get suggestions');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestAutocomplete = async () => {
    if (currentTeamIds.length === 0) {
      setError('Add at least one Pokemon to your team first');
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      const result = await teamsApi.suggestAutocomplete(
        currentTeamIds,
        'coverage',
        includeLegendaries,
        legendaryFilter,
        pokemonPool
      );
      setSuggestions(result.suggestions || []);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get suggestions');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGetSuggestions = () => {
    if (mode === 'complete') {
      handleSuggestComplete();
    } else {
      handleSuggestAutocomplete();
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-900 rounded-lg shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="p-6 border-b border-transparent bg-gradient-to-r from-blue-500 to-purple-600 text-white">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <Sparkles className="w-6 h-6" />
              <h2 className="text-2xl font-bold">AI Team Suggestions</h2>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-white/20 rounded-lg transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
          <p className="text-blue-100">
            Get intelligent Pokemon recommendations based on your current team
          </p>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 bg-gray-50 dark:bg-gray-800">
          {/* Mode Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Suggestion Mode
            </label>
            <div className="grid grid-cols-2 gap-4">
              <button
                onClick={() => setMode('autocomplete')}
                className={`p-4 rounded-lg border-2 transition-all ${
                  mode === 'autocomplete'
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/30'
                    : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500 bg-white dark:bg-gray-700'
                }`}
              >
                <h3 className="font-semibold mb-1 text-gray-900 dark:text-white">Autocomplete Team</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Suggests Pokemon that complement your current team
                </p>
              </button>
              <button
                onClick={() => setMode('complete')}
                className={`p-4 rounded-lg border-2 transition-all ${
                  mode === 'complete'
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/30'
                    : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500 bg-white dark:bg-gray-700'
                }`}
              >
                <h3 className="font-semibold mb-1 text-gray-900 dark:text-white">Generate Full Team</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Creates a complete team from scratch using a strategy
                </p>
              </button>
            </div>
          </div>

          {/* Legendary Filter */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Legendary Filter
            </label>
            <div className="flex gap-2">
              <button
                onClick={() => setLegendaryFilter('all')}
                className={`flex-1 p-3 rounded-lg border-2 transition-all flex items-center justify-center gap-2 ${
                  legendaryFilter === 'all'
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/30'
                    : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500 bg-white dark:bg-gray-700'
                }`}
              >
                <Sparkles className="w-4 h-4" />
                <span className="text-sm font-medium">All Pokemon</span>
              </button>
              <button
                onClick={() => setLegendaryFilter('non-legendaries')}
                className={`flex-1 p-3 rounded-lg border-2 transition-all flex items-center justify-center gap-2 ${
                  legendaryFilter === 'non-legendaries'
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/30'
                    : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500 bg-white dark:bg-gray-700'
                }`}
              >
                <Ban className="w-4 h-4 text-green-600" />
                <span className="text-sm font-medium">No Legendaries</span>
              </button>
              <button
                onClick={() => setLegendaryFilter('legendaries')}
                className={`flex-1 p-3 rounded-lg border-2 transition-all flex items-center justify-center gap-2 ${
                  legendaryFilter === 'legendaries'
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/30'
                    : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500 bg-white dark:bg-gray-700'
                }`}
              >
                <Crown className="w-4 h-4 text-amber-500" />
                <span className="text-sm font-medium">Only Legendaries</span>
              </button>
            </div>
          </div>

          {/* Strategy Selection (for complete mode) */}
          {mode === 'complete' && (
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Team Strategy
              </label>
              <div className="grid grid-cols-2 gap-3">
                {strategies.map((strat) => {
                  const Icon = strat.icon;
                  return (
                    <button
                      key={strat.value}
                      onClick={() => setStrategy(strat.value)}
                      className={`p-3 rounded-lg border-2 transition-all text-left ${
                        strategy === strat.value
                          ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/30'
                          : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500 bg-white dark:bg-gray-700'
                      }`}
                    >
                      <div className="flex items-center gap-2 mb-1">
                        <Icon className="w-4 h-4 text-gray-700 dark:text-gray-300" />
                        <span className="font-semibold text-gray-900 dark:text-white">{strat.label}</span>
                      </div>
                      <p className="text-xs text-gray-600 dark:text-gray-400">{strat.description}</p>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* Get Suggestions Button */}
          <button
            onClick={handleGetSuggestions}
            disabled={isLoading}
            className="w-full py-3 px-6 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg font-semibold hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2 mb-6 shadow-lg shadow-purple-500/20"
          >
            {isLoading ? (
              <>
                <LoadingSpinner />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                <span>Get Suggestions</span>
              </>
            )}
          </button>

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-400">
              {error}
            </div>
          )}

          {/* Suggestions List */}
          {suggestions.length > 0 && (
            <div className="space-y-3">
              <h3 className="font-semibold text-lg mb-3 text-gray-900 dark:text-white">
                Recommended Pokemon ({suggestions.length})
              </h3>
              {suggestions.map((suggestion, index) => {
                const displayScore = suggestion.fit_score ?? suggestion.score ?? suggestion.stat_total ?? 0;
                return (
                  <div
                    key={suggestion.id || index}
                    className="border border-gray-200 dark:border-gray-600 rounded-lg hover:border-blue-300 dark:hover:border-blue-500 transition-all overflow-hidden bg-white dark:bg-gray-700"
                  >
                    <div className="p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4 flex-1">
                          <img
                            src={suggestion.sprite_url || '/placeholder-pokemon.png'}
                            alt={suggestion.name}
                            className="w-16 h-16 object-contain"
                          />
                          <div className="flex-1">
                            <h4 className="font-semibold text-lg capitalize text-gray-900 dark:text-white">
                              {suggestion.name}
                            </h4>
                            <div className="flex gap-2 mt-1">
                              {suggestion.types.map((type) => (
                                <span
                                  key={typeof type === 'string' ? type : type.name}
                                  className="px-2 py-1 rounded text-xs font-medium text-white"
                                  style={{
                                    backgroundColor: getTypeColor(typeof type === 'string' ? type : type.name),
                                  }}
                                >
                                  {typeof type === 'string' ? type : type.name}
                                </span>
                              ))}
                            </div>
                          </div>
                          <div className="text-right">
                            <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                              {typeof displayScore === 'number' ? Math.round(displayScore) : displayScore}
                            </div>
                            <div className="text-xs text-gray-500 dark:text-gray-400">
                              {suggestion.fit_score ? 'Fit Score' : suggestion.score ? 'Score' : 'Stats'}
                            </div>
                          </div>
                        </div>
                        <button
                          onClick={() =>
                            setExpandedIndex(expandedIndex === index ? null : index)
                          }
                          className="ml-4 p-2 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg transition-colors"
                        >
                          {expandedIndex === index ? (
                            <ChevronUp className="w-5 h-5 text-gray-600 dark:text-gray-400" />
                          ) : (
                            <ChevronDown className="w-5 h-5 text-gray-600 dark:text-gray-400" />
                          )}
                        </button>
                      </div>

                      {/* Expanded Details */}
                      {expandedIndex === index && (
                        <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-600">
                          <p className="text-sm text-gray-700 dark:text-gray-300 mb-4">
                            {suggestion.reason || 'Great addition to your team based on type coverage and stats.'}
                          </p>
                          <button
                            onClick={() => onSelectPokemon({
                              id: suggestion.id,
                              pokeapi_id: null,
                              name: suggestion.name,
                              pokedex_number: suggestion.pokedex_number,
                              sprite_url: suggestion.sprite_url,
                              types: suggestion.types.map((t, idx) => ({
                                type: {
                                  id: idx,
                                  name: typeof t === 'string' ? t : t.name,
                                  pokeapi_id: null,
                                  color: null,
                                },
                                slot: typeof t === 'string' ? idx + 1 : t.slot,
                              })),
                              generation: null,
                            })}
                            className="w-full py-2 px-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors font-medium"
                          >
                            Add to Team
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* Empty State */}
          {!isLoading && suggestions.length === 0 && !error && (
            <div className="text-center py-12">
              <Sparkles className="w-16 h-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
              <p className="text-gray-500 dark:text-gray-400">
                Click "Get Suggestions" to receive AI-powered Pokemon recommendations
              </p>
              {legendaryFilter !== 'all' && (
                <p className="text-sm text-gray-400 dark:text-gray-500 mt-2">
                  If no results appear, try switching the legendary filter.
                </p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Helper function for type colors
function getTypeColor(type: string): string {
  const colors: Record<string, string> = {
    normal: '#A8A878',
    fire: '#F08030',
    water: '#6890F0',
    electric: '#F8D030',
    grass: '#78C850',
    ice: '#98D8D8',
    fighting: '#C03028',
    poison: '#A040A0',
    ground: '#E0C068',
    flying: '#A890F0',
    psychic: '#F85888',
    bug: '#A8B820',
    rock: '#B8A038',
    ghost: '#705898',
    dragon: '#7038F8',
    dark: '#705848',
    steel: '#B8B8D0',
    fairy: '#EE99AC',
  };
  return colors[type.toLowerCase()] || '#777';
}
