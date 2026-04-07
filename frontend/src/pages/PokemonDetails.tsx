import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, ChevronRight } from 'lucide-react';
import { TypeBadge } from '@/components/pokemon/TypeBadge';
import { StatsDisplay } from '@/components/pokemon/StatBar';
import { WeaknessChart } from '@/components/pokemon/WeaknessChart';
import { SpawnEntryCard } from '@/components/spawn/SpawnEntryCard';
import { FavoriteButton } from '@/components/ui/FavoriteButton';
import { LoadingPage } from '@/components/ui/Loading';
import { usePokemonDetails } from '@/hooks/useApi';
import { formatPokemonName, formatPokedexNumber, getTypeColor } from '@/utils/pokemon';

export default function PokemonDetails() {
  const { id } = useParams<{ id: string }>();
  const pokemonId = id ? parseInt(id) : null;

  const { data: pokemon, isLoading, error } = usePokemonDetails(pokemonId);

  if (isLoading) {
    return <LoadingPage message="Loading Pokémon details..." />;
  }

  if (error || !pokemon) {
    return (
      <div className="text-center py-12">
        <p className="text-red-500">Failed to load Pokémon details.</p>
        <Link to="/pokedex" className="text-blue-600 hover:underline mt-4 inline-block">
          Back to Pokédex
        </Link>
      </div>
    );
  }

  const primaryType = pokemon.types[0]?.type.name || 'normal';

  return (
    <div className="space-y-8">
      {/* Back button */}
      <Link
        to="/pokedex"
        className="inline-flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Pokédex
      </Link>

      {/* Header Card */}
      <div
        className="rounded-2xl overflow-hidden shadow-lg"
        style={{
          background: `linear-gradient(135deg, ${getTypeColor(primaryType)}60 0%, ${getTypeColor(primaryType)}30 100%)`,
        }}
      >
        <div className="p-8">
          <div className="flex flex-col md:flex-row items-center gap-8">
            {/* Sprite */}
            <div className="relative">
              <img
                src={pokemon.sprite_official_url || pokemon.sprite_url || '/placeholder-pokemon.png'}
                alt={pokemon.name}
                className="w-48 h-48 object-contain drop-shadow-2xl"
              />
              <FavoriteButton
                pokemonId={pokemon.id}
                size="lg"
                className="absolute top-0 right-0"
              />
            </div>

            {/* Basic Info */}
            <div className="flex-1 text-center md:text-left">
              <p className="text-gray-600 dark:text-gray-300 font-medium">
                {formatPokedexNumber(pokemon.pokedex_number)}
              </p>
              <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
                {formatPokemonName(pokemon.name)}
              </h1>
              {pokemon.category && (
                <p className="text-gray-600 dark:text-gray-300 mb-4">{pokemon.category}</p>
              )}

              {/* Types */}
              <div className="flex gap-2 justify-center md:justify-start mb-4">
                {pokemon.types.map((t) => (
                  <TypeBadge key={t.type.name} type={t.type.name} size="lg" />
                ))}
              </div>

              {/* Physical */}
              <div className="flex gap-6 justify-center md:justify-start text-sm text-gray-600 dark:text-gray-300">
                <div>
                  <span className="font-medium">Height:</span> {pokemon.height}m
                </div>
                <div>
                  <span className="font-medium">Weight:</span> {pokemon.weight}kg
                </div>
                {pokemon.generation && (
                  <div>
                    <span className="font-medium">Gen:</span> {pokemon.generation}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Description */}
      {pokemon.description && (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Description</h2>
          <p className="text-gray-600 dark:text-gray-300">{pokemon.description}</p>
        </div>
      )}

      {/* Stats and Weaknesses */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Stats */}
        {pokemon.stats && (
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Base Stats</h2>
            <StatsDisplay stats={pokemon.stats} />
          </div>
        )}

        {/* Type Effectiveness */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Type Effectiveness</h2>
          <WeaknessChart
            weaknesses={pokemon.weaknesses}
            resistances={pokemon.resistances}
            immunities={pokemon.immunities}
            quadrupleWeaknesses={pokemon.quadruple_weaknesses}
            quadrupleResistances={pokemon.quadruple_resistances}
            compact
          />
        </div>
      </div>

      {/* Strategic Tags */}
      {pokemon.strategic_tags.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Strategic Tags</h2>
          <div className="flex flex-wrap gap-2">
            {pokemon.strategic_tags.map((tag) => (
              <span
                key={tag}
                className="px-3 py-1 bg-purple-100 dark:bg-purple-900/40 text-purple-700 dark:text-purple-300 rounded-full text-sm font-medium"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Abilities */}
      {pokemon.abilities.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Abilities</h2>
          <div className="space-y-3">
            {pokemon.abilities.map((a) => (
              <div key={a.ability.name} className="flex items-start gap-3">
                <span className="font-medium text-gray-900 dark:text-white capitalize">
                  {a.ability.name.replace('-', ' ')}
                </span>
                {a.is_hidden && (
                  <span className="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded text-xs">
                    Hidden
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Cobblemon Spawns */}
      {pokemon.cobblemon_spawns.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
            Cobblemon Spawns
            <span className="text-sm font-normal text-gray-500 dark:text-gray-400 ml-2">
              ({pokemon.cobblemon_spawns.length} entries)
            </span>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {pokemon.cobblemon_spawns.map((spawn) => (
              <SpawnEntryCard key={spawn.id} spawn={spawn} />
            ))}
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex flex-wrap gap-4 justify-center">
        <Link
          to={`/compare?pokemon1=${pokemon.id}`}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          Compare with another Pokémon
        </Link>
        <Link
          to="/team-builder"
          className="px-6 py-3 bg-purple-600 text-white rounded-lg font-medium hover:bg-purple-700 transition-colors"
        >
          Add to Team
        </Link>
      </div>
    </div>
  );
}
