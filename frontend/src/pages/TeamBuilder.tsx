import { useState, useMemo } from 'react';
import { Users, Trash2, Save, BarChart3, Search, X, Sparkles } from 'lucide-react';
import { TeamSlot } from '@/components/team/TeamSlot';
import { CoverageSummary } from '@/components/team/CoverageSummary';
import { TeamSuggestions } from '@/components/team/TeamSuggestions';
import { SearchBar } from '@/components/ui/SearchBar';
import { PokemonCard } from '@/components/pokemon/PokemonCard';
import { LoadingSpinner } from '@/components/ui/Loading';
import { useTeamBuilderStore } from '@/store';
import { usePokemonList, usePokemonDetails } from '@/hooks/useApi';
import { pokemonApi } from '@/services/api';
import { calculateTypeEffectiveness } from '@/utils/pokemon';
import type { PokemonListItem, PokemonDetails, TeamAnalysis } from '@/types';

export default function TeamBuilder() {
  const {
    slots,
    teamName,
    setTeamName,
    addPokemon,
    removePokemon,
    clearTeam,
    getPokemonIds,
  } = useTeamBuilderStore();

  const [showPokemonPicker, setShowPokemonPicker] = useState<number | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [showAnalysis, setShowAnalysis] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isLoadingPokemon, setIsLoadingPokemon] = useState(false);
  const [pokemonPool, setPokemonPool] = useState<'all' | 'pixelmon'>('all');

  // Fetch pokemon list for the picker
  const { data: pokemonData, isLoading: isLoadingList } = usePokemonList({
    search: searchQuery || undefined,
    page_size: 50,
    pokemon_pool: pokemonPool,
  });

  // Calculate team analysis locally
  const teamAnalysis = useMemo(() => {
    const teamPokemon = slots
      .filter((s) => s.details !== null)
      .map((s) => s.details!);

    if (teamPokemon.length === 0) return null;

    // Aggregate weaknesses, resistances, and immunities
    const weaknessCounts: Record<string, number> = {};
    const resistanceCounts: Record<string, number> = {};
    const immunitySet = new Set<string>();
    const sharedWeaknesses: Record<string, string[]> = {};

    teamPokemon.forEach((pokemon) => {
      // Add immunities
      pokemon.immunities?.forEach((type) => immunitySet.add(type));

      // Count weaknesses
      Object.entries(pokemon.weaknesses || {}).forEach(([type, mult]) => {
        if (mult > 1) {
          weaknessCounts[type] = (weaknessCounts[type] || 0) + 1;
          if (!sharedWeaknesses[type]) sharedWeaknesses[type] = [];
          sharedWeaknesses[type].push(pokemon.name);
        }
      });

      // Count resistances
      Object.entries(pokemon.resistances || {}).forEach(([type, mult]) => {
        if (mult < 1) {
          resistanceCounts[type] = (resistanceCounts[type] || 0) + 1;
        }
      });
    });

    // Find problematic types (3+ Pokemon weak to the same type)
    const problematicTypes = Object.entries(sharedWeaknesses)
      .filter(([_, pokemon]) => pokemon.length >= 3)
      .map(([type]) => type);

    // Calculate scores
    const totalWeaknesses = Object.values(weaknessCounts).reduce((a, b) => a + b, 0);
    const totalResistances = Object.values(resistanceCounts).reduce((a, b) => a + b, 0);
    const defensiveScore = Math.min(100, Math.max(0, 50 + (totalResistances - totalWeaknesses) * 5));
    
    // Coverage score based on type diversity
    const typeSet = new Set<string>();
    teamPokemon.forEach((p) => p.types.forEach((t) => typeSet.add(t.type.name)));
    const coverageScore = Math.min(100, (typeSet.size / 18) * 100 + immunitySet.size * 5);

    // Generate summary
    let summary = '';
    if (problematicTypes.length > 0) {
      summary = `Warning: Your team has ${problematicTypes.length} significant weaknesses. Consider adding Pokemon that resist ${problematicTypes.slice(0, 2).join(' and ')}.`;
    } else if (defensiveScore >= 70 && coverageScore >= 60) {
      summary = 'Great team composition! Good balance of offensive coverage and defensive typing.';
    } else if (defensiveScore < 50) {
      summary = 'Your team has defensive vulnerabilities. Consider adding Pokemon with better resistances.';
    } else {
      summary = 'Decent team setup. Consider expanding type coverage for better matchups.';
    }

    return {
      team_id: 0,
      weaknesses: weaknessCounts,
      resistances: resistanceCounts,
      immunities: Array.from(immunitySet),
      shared_weaknesses: Object.fromEntries(
        Object.entries(sharedWeaknesses).filter(([_, v]) => v.length >= 2)
      ),
      problematic_types: problematicTypes,
      role_distribution: {},
      coverage_score: coverageScore,
      defensive_score: defensiveScore,
      summary,
    } as TeamAnalysis;
  }, [slots]);

  const handleAddPokemon = async (pokemon: PokemonListItem, slotIndex?: number) => {
    const targetSlot = slotIndex ?? showPokemonPicker;
    if (targetSlot === null) return;

    setIsLoadingPokemon(true);
    try {
      const details = await pokemonApi.getDetails(pokemon.id);
      addPokemon(targetSlot, pokemon, details);
      setShowPokemonPicker(null);
      setSearchQuery('');
    } catch (error) {
      console.error('Failed to fetch Pokemon details:', error);
    } finally {
      setIsLoadingPokemon(false);
    }
  };

  const handleSuggestionSelect = async (pokemon: PokemonListItem) => {
    // Find first empty slot
    const emptySlot = slots.findIndex((s) => s.pokemon === null);
    if (emptySlot !== -1) {
      await handleAddPokemon(pokemon, emptySlot);
    }
    setShowSuggestions(false);
  };

  const filledSlots = slots.filter((s) => s.pokemon !== null).length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Users className="w-8 h-8 text-blue-600 dark:text-blue-400" />
          <div>
            <input
              type="text"
              value={teamName}
              onChange={(e) => setTeamName(e.target.value)}
              className="text-2xl font-bold text-gray-900 dark:text-white bg-transparent border-b-2 border-transparent hover:border-gray-300 dark:hover:border-gray-600 focus:border-blue-500 focus:outline-none transition-colors"
              placeholder="Team Name"
            />
            <p className="text-sm text-gray-500 dark:text-gray-400">{filledSlots}/6 Pokémon</p>
          </div>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => setShowSuggestions(true)}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gradient-to-r from-purple-600 to-blue-600 text-white hover:from-purple-700 hover:to-blue-700 transition-all shadow-lg shadow-purple-500/20"
          >
            <Sparkles className="w-4 h-4" />
            AI Suggestions
          </button>
          <button
            onClick={() => setShowAnalysis(!showAnalysis)}
            disabled={filledSlots === 0}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <BarChart3 className="w-4 h-4" />
            {showAnalysis ? 'Hide Analysis' : 'Analyze Team'}
          </button>
          <button
            onClick={clearTeam}
            disabled={filledSlots === 0}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 hover:bg-red-200 dark:hover:bg-red-900/50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Trash2 className="w-4 h-4" />
            Clear
          </button>
        </div>
      </div>

      {/* Team Slots */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {slots.map((slot, index) => (
          <TeamSlot
            key={index}
            slot={index}
            pokemon={slot.pokemon}
            details={slot.details}
            onAdd={() => setShowPokemonPicker(index)}
            onRemove={() => removePokemon(index)}
          />
        ))}
      </div>

      <div className="bg-gray-50 dark:bg-gray-800 rounded-xl p-4">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Pokémon Pool
        </label>
        <div className="grid grid-cols-2 gap-3">
          <button
            onClick={() => setPokemonPool('all')}
            className={`p-3 rounded-lg border-2 transition-all text-sm font-medium ${
              pokemonPool === 'all'
                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300'
                : 'border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:border-gray-300 dark:hover:border-gray-500 bg-white dark:bg-gray-700'
            }`}
          >
            All Pokémon
          </button>
          <button
            onClick={() => setPokemonPool('pixelmon')}
            className={`p-3 rounded-lg border-2 transition-all text-sm font-medium ${
              pokemonPool === 'pixelmon'
                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300'
                : 'border-gray-200 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:border-gray-300 dark:hover:border-gray-500 bg-white dark:bg-gray-700'
            }`}
          >
            Only Pixelmon/Cobblemon
          </button>
        </div>
      </div>

      {/* Team Analysis */}
      {showAnalysis && teamAnalysis && (
        <div className="bg-gray-50 dark:bg-gray-800 rounded-xl p-6">
          <h2 className="text-xl font-bold text-gray-800 dark:text-white mb-4">Team Analysis</h2>
          <CoverageSummary
            weaknesses={teamAnalysis.weaknesses}
            resistances={teamAnalysis.resistances}
            immunities={teamAnalysis.immunities}
            sharedWeaknesses={teamAnalysis.shared_weaknesses}
            problematicTypes={teamAnalysis.problematic_types}
            coverageScore={teamAnalysis.coverage_score}
            defensiveScore={teamAnalysis.defensive_score}
            summary={teamAnalysis.summary}
          />
        </div>
      )}

      {/* Pokemon Picker Modal */}
      {showPokemonPicker !== null && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-xl w-full max-w-4xl max-h-[80vh] overflow-hidden flex flex-col">
            {/* Modal Header */}
            <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
              <h3 className="text-lg font-semibold text-gray-800 dark:text-white">
                Add Pokémon to Slot {showPokemonPicker + 1}
              </h3>
              <button
                onClick={() => {
                  setShowPokemonPicker(null);
                  setSearchQuery('');
                }}
                className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
              >
                <X className="w-5 h-5 text-gray-500 dark:text-gray-400" />
              </button>
            </div>

            {/* Search */}
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search Pokémon..."
                  className="w-full pl-10 pr-4 py-2 border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  autoFocus
                />
              </div>
            </div>

            {/* Pokemon Grid */}
            <div className="flex-1 overflow-y-auto p-4">
              {isLoadingList || isLoadingPokemon ? (
                <div className="flex justify-center py-12">
                  <LoadingSpinner size="lg" />
                </div>
              ) : pokemonData && pokemonData.items.length > 0 ? (
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                  {pokemonData.items.map((pokemon) => (
                    <button
                      key={pokemon.id}
                      onClick={() => handleAddPokemon(pokemon)}
                      className="text-left"
                    >
                      <PokemonCard pokemon={pokemon} showFavorite={false} />
                    </button>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <p className="text-gray-500 dark:text-gray-400">No Pokémon found.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Empty State */}
      {filledSlots === 0 && !showPokemonPicker && (
        <div className="text-center py-12 bg-gray-50 dark:bg-gray-800 rounded-xl">
          <Users className="w-16 h-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-2">Build Your Team</h3>
          <p className="text-gray-500 dark:text-gray-400 max-w-md mx-auto">
            Click on any slot above to add a Pokémon. Build a balanced team of up to 6 Pokémon
            and analyze their type coverage and weaknesses.
          </p>
        </div>
      )}

      {/* Team Suggestions Modal */}
      {showSuggestions && (
        <TeamSuggestions
          onSelectPokemon={handleSuggestionSelect}
          currentTeamIds={getPokemonIds()}
          pokemonPool={pokemonPool}
          onClose={() => setShowSuggestions(false)}
        />
      )}
    </div>
  );
}
