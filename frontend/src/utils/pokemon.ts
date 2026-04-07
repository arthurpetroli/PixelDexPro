export const TYPE_COLORS: Record<string, string> = {
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

export const ALL_TYPES = Object.keys(TYPE_COLORS);

export const GENERATIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9];

export const SPAWN_TIMES = ['any', 'day', 'night', 'dawn', 'dusk'];

export const SPAWN_WEATHERS = ['any', 'clear', 'rain', 'thunder', 'snow'];

export const SPAWN_CONTEXTS = ['grounded', 'submerged', 'surface', 'seafloor'];

export function getTypeColor(type: string): string {
  return TYPE_COLORS[type.toLowerCase()] || '#777777';
}

export function getTypeTextColor(type: string): string {
  const darkTypes = ['dark', 'ghost', 'dragon', 'fighting', 'poison'];
  return darkTypes.includes(type.toLowerCase()) ? '#ffffff' : '#000000';
}

export function formatStatName(stat: string): string {
  const names: Record<string, string> = {
    hp: 'HP',
    attack: 'Attack',
    defense: 'Defense',
    special_attack: 'Sp. Atk',
    special_defense: 'Sp. Def',
    speed: 'Speed',
    total: 'Total',
  };
  return names[stat] || stat;
}

export function formatPokemonName(name: string): string {
  return name
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

export function formatPokedexNumber(num: number | null): string {
  if (!num) return '#???';
  return `#${num.toString().padStart(3, '0')}`;
}

export function getStatPercentage(value: number, max: number = 255): number {
  return Math.min(100, (value / max) * 100);
}

export function getStatColor(value: number): string {
  if (value >= 150) return '#22c55e'; // green
  if (value >= 100) return '#84cc16'; // lime
  if (value >= 75) return '#eab308'; // yellow
  if (value >= 50) return '#f97316'; // orange
  return '#ef4444'; // red
}

export function getMultiplierColor(multiplier: number): string {
  if (multiplier === 0) return '#6b7280'; // gray (immune)
  if (multiplier <= 0.25) return '#22c55e'; // green (4x resist)
  if (multiplier <= 0.5) return '#84cc16'; // lime (2x resist)
  if (multiplier >= 4) return '#dc2626'; // red (4x weak)
  if (multiplier >= 2) return '#f97316'; // orange (2x weak)
  return '#9ca3af'; // neutral
}

export function getMultiplierText(multiplier: number): string {
  if (multiplier === 0) return 'Immune';
  if (multiplier === 0.25) return '1/4x';
  if (multiplier === 0.5) return '1/2x';
  if (multiplier === 2) return '2x';
  if (multiplier === 4) return '4x';
  return '1x';
}
