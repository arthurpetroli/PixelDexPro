import { useState, useEffect, useRef } from 'react';
import { Search, X } from 'lucide-react';
import { usePokemonSearch } from '@/hooks/useApi';
import { formatPokemonName } from '@/utils/pokemon';
import { debounce } from '@/utils/helpers';
import type { PokemonListItem } from '@/types';
import { cn } from '@/utils/helpers';

interface SearchBarProps {
  onSelect?: (pokemon: PokemonListItem) => void;
  onSearch?: (query: string) => void;
  placeholder?: string;
  showDropdown?: boolean;
  className?: string;
}

export function SearchBar({
  onSelect,
  onSearch,
  placeholder = 'Search Pokémon...',
  showDropdown = true,
  className,
}: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const { data: results, isLoading } = usePokemonSearch(query);

  // Debounced search callback
  const debouncedSearch = useRef(
    debounce((value: string) => {
      onSearch?.(value);
    }, 300)
  ).current;

  useEffect(() => {
    debouncedSearch(query);
  }, [query, debouncedSearch]);

  // Close dropdown on outside click
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node) &&
        !inputRef.current?.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (pokemon: PokemonListItem) => {
    onSelect?.(pokemon);
    setQuery('');
    setIsOpen(false);
  };

  const handleClear = () => {
    setQuery('');
    onSearch?.('');
    inputRef.current?.focus();
  };

  return (
    <div className={cn('relative', className)}>
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          placeholder={placeholder}
          className="w-full pl-10 pr-10 py-3 rounded-xl border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 dark:focus:ring-blue-800 outline-none transition-all"
        />
        {query && (
          <button
            onClick={handleClear}
            className="absolute right-3 top-1/2 -translate-y-1/2 p-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <X className="w-4 h-4 text-gray-400" />
          </button>
        )}
      </div>

      {/* Dropdown */}
      {showDropdown && isOpen && query.length >= 2 && (
        <div
          ref={dropdownRef}
          className="absolute z-50 w-full mt-2 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 max-h-80 overflow-auto"
        >
          {isLoading ? (
            <div className="p-4 text-center text-gray-500 dark:text-gray-400">Searching...</div>
          ) : results && results.length > 0 ? (
            <ul>
              {results.map((pokemon) => (
                <li key={pokemon.id}>
                  <button
                    onClick={() => handleSelect(pokemon)}
                    className="w-full flex items-center gap-3 p-3 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                  >
                    <img
                      src={pokemon.sprite_url || '/placeholder-pokemon.png'}
                      alt={pokemon.name}
                      className="w-10 h-10 object-contain"
                    />
                    <div className="flex-1 text-left">
                      <span className="font-medium text-gray-900 dark:text-white">{formatPokemonName(pokemon.name)}</span>
                      <span className="text-gray-400 dark:text-gray-500 text-sm ml-2">
                        #{pokemon.pokedex_number?.toString().padStart(3, '0')}
                      </span>
                    </div>
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <div className="p-4 text-center text-gray-500 dark:text-gray-400">No Pokémon found</div>
          )}
        </div>
      )}
    </div>
  );
}
