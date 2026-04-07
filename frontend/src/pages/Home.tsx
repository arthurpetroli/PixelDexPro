import { Link } from 'react-router-dom';
import { BookOpen, MapPin, GitCompare, Users, Heart, Zap, Search, ChevronRight, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';

const features = [
  {
    title: 'Pokédex',
    description: 'Browse all Pokémon with detailed stats, types, and abilities',
    icon: BookOpen,
    path: '/pokedex',
    gradient: 'from-red-500 via-orange-500 to-yellow-500',
    shadowColor: 'shadow-red-500/20',
  },
  {
    title: 'Spawn Finder',
    description: 'Discover where Pokémon spawn with biome filters',
    icon: MapPin,
    path: '/spawns',
    gradient: 'from-green-500 via-emerald-500 to-teal-500',
    shadowColor: 'shadow-green-500/20',
  },
  {
    title: 'Compare',
    description: 'Compare stats, types and weaknesses side by side',
    icon: GitCompare,
    path: '/compare',
    gradient: 'from-blue-500 via-cyan-500 to-sky-500',
    shadowColor: 'shadow-blue-500/20',
  },
  {
    title: 'Team Builder',
    description: 'Build and analyze your team type coverage',
    icon: Users,
    path: '/team-builder',
    gradient: 'from-purple-500 via-violet-500 to-fuchsia-500',
    shadowColor: 'shadow-purple-500/20',
  },
  {
    title: 'Type Analysis',
    description: 'Calculate matchups and strategic advantages',
    icon: Zap,
    path: '/pokedex',
    gradient: 'from-yellow-500 via-amber-500 to-orange-500',
    shadowColor: 'shadow-yellow-500/20',
  },
  {
    title: 'Favorites',
    description: 'Save your favorite Pokémon for quick access',
    icon: Heart,
    path: '/favorites',
    gradient: 'from-pink-500 via-rose-500 to-red-500',
    shadowColor: 'shadow-pink-500/20',
  },
];

const quickStats = [
  { value: '1000+', label: 'Pokémon', gradient: 'from-blue-600 to-cyan-500' },
  { value: '18', label: 'Types', gradient: 'from-green-600 to-emerald-500' },
  { value: '100+', label: 'Biomes', gradient: 'from-purple-600 to-pink-500' },
  { value: '9', label: 'Generations', gradient: 'from-orange-600 to-amber-500' },
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: 'easeOut' },
  },
};

export default function Home() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <div className="space-y-16 pb-12">
      {/* Hero Section */}
      <motion.section
        className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-8 md:p-12"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* Animated background elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div
            className="absolute w-96 h-96 bg-purple-500/20 rounded-full blur-3xl"
            style={{
              transform: `translate(${mousePosition.x * 0.02}px, ${mousePosition.y * 0.02}px)`,
              left: '10%',
              top: '-20%',
            }}
          />
          <div
            className="absolute w-96 h-96 bg-blue-500/20 rounded-full blur-3xl"
            style={{
              transform: `translate(${-mousePosition.x * 0.015}px, ${mousePosition.y * 0.015}px)`,
              right: '10%',
              bottom: '-20%',
            }}
          />
          <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0zNiAxOGMtOS45NDEgMC0xOCA4LjA1OS0xOCAxOHM4LjA1OSAxOCAxOCAxOCAxOC04LjA1OSAxOC0xOC04LjA1OS0xOC0xOC0xOHptMCAzMmMtNy43MzIgMC0xNC02LjI2OC0xNC0xNHM2LjI2OC0xNCAxNC0xNCAxNCA2LjI2OCAxNCAxNC02LjI2OCAxNC0xNCAxNHoiIGZpbGw9InJnYmEoMjU1LDI1NSwyNTUsMC4wMykiLz48L2c+PC9zdmc+')] opacity-30" />
        </div>

        <div className="relative z-10 text-center max-w-3xl mx-auto">
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 mb-6"
          >
            <Sparkles className="w-4 h-4 text-yellow-400" />
            <span className="text-sm text-white/90">Your Ultimate Pokémon Companion</span>
          </motion.div>

          <motion.h1
            className="text-4xl md:text-6xl font-bold mb-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <span className="text-white">Pixel</span>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400">Dex</span>
            <span className="text-white"> Pro</span>
          </motion.h1>

          <motion.p
            className="text-lg md:text-xl text-white/70 mb-8 max-w-2xl mx-auto"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            Browse the complete Pokédex, find Cobblemon spawns, build competitive teams,
            and master type matchups - all in one place.
          </motion.p>

          <motion.div
            className="flex flex-col sm:flex-row gap-4 justify-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
          >
            <Link
              to="/pokedex"
              className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold hover:from-blue-600 hover:to-purple-700 transition-all shadow-lg shadow-purple-500/25 hover:shadow-purple-500/40"
            >
              <Search className="w-5 h-5" />
              Explore Pokédex
            </Link>
            <Link
              to="/team-builder"
              className="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-white/10 backdrop-blur-sm border border-white/20 text-white font-semibold hover:bg-white/20 transition-all"
            >
              <Users className="w-5 h-5" />
              Build Your Team
            </Link>
          </motion.div>
        </div>

        {/* Decorative Pokéball */}
        <div className="absolute -right-20 -bottom-20 w-64 h-64 opacity-10">
          <svg viewBox="0 0 100 100" className="w-full h-full">
            <circle cx="50" cy="50" r="45" fill="none" stroke="white" strokeWidth="4" />
            <line x1="5" y1="50" x2="95" y2="50" stroke="white" strokeWidth="4" />
            <circle cx="50" cy="50" r="12" fill="none" stroke="white" strokeWidth="4" />
          </svg>
        </div>
      </motion.section>

      {/* Quick Stats */}
      <motion.section
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="grid grid-cols-2 md:grid-cols-4 gap-4"
      >
        {quickStats.map((stat, index) => (
          <motion.div
            key={stat.label}
            variants={itemVariants}
            className="relative overflow-hidden rounded-2xl bg-white dark:bg-gray-800 p-6 shadow-lg hover:shadow-xl transition-shadow"
          >
            <div className="absolute top-0 right-0 w-20 h-20 -mr-6 -mt-6 rounded-full bg-gradient-to-br opacity-10 blur-xl" 
              style={{ backgroundImage: `linear-gradient(to bottom right, var(--tw-gradient-stops))` }}
            />
            <div className={`text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r ${stat.gradient}`}>
              {stat.value}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">{stat.label}</div>
          </motion.div>
        ))}
      </motion.section>

      {/* Features Grid */}
      <motion.section
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <div className="text-center mb-10">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-3">
            Everything You Need
          </h2>
          <p className="text-gray-600 dark:text-gray-400 max-w-xl mx-auto">
            Powerful tools designed for trainers who want to master the game
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <motion.div key={feature.title} variants={itemVariants}>
                <Link
                  to={feature.path}
                  className={`group relative flex flex-col h-full p-6 rounded-2xl bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 shadow-lg hover:shadow-xl ${feature.shadowColor} transition-all duration-300 overflow-hidden`}
                >
                  {/* Gradient overlay on hover */}
                  <div
                    className={`absolute inset-0 bg-gradient-to-br ${feature.gradient} opacity-0 group-hover:opacity-5 transition-opacity duration-300`}
                  />

                  {/* Icon */}
                  <div
                    className={`relative w-14 h-14 rounded-xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-5 shadow-lg group-hover:scale-110 transition-transform duration-300`}
                  >
                    <Icon className="w-7 h-7 text-white" />
                  </div>

                  {/* Content */}
                  <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
                    {feature.title}
                    <ChevronRight className="w-5 h-5 opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all duration-300 text-gray-400" />
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">
                    {feature.description}
                  </p>
                </Link>
              </motion.div>
            );
          })}
        </div>
      </motion.section>

      {/* CTA Section */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.6 }}
        className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 p-8 md:p-12"
      >
        <div className="absolute inset-0 bg-black/20" />
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0zNiAxOGMtOS45NDEgMC0xOCA4LjA1OS0xOCAxOHM4LjA1OSAxOCAxOCAxOCAxOC04LjA1OSAxOC0xOC04LjA1OS0xOC0xOC0xOHptMCAzMmMtNy43MzIgMC0xNC02LjI2OC0xNC0xNHM2LjI2OC0xNCAxNC0xNCAxNCA2LjI2OCAxNCAxNC02LjI2OCAxNC0xNCAxNHoiIGZpbGw9InJnYmEoMjU1LDI1NSwyNTUsMC4wNSkiLz48L2c+PC9zdmc+')] opacity-50" />
        
        <div className="relative z-10 text-center max-w-2xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-bold text-white mb-4">
            Ready to become a Pokémon Master?
          </h2>
          <p className="text-white/80 mb-6">
            Start exploring the complete Pokédex and discover everything about your favorite Pokémon.
          </p>
          <Link
            to="/pokedex"
            className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl bg-white text-purple-600 font-bold hover:bg-gray-100 transition-colors shadow-lg"
          >
            Get Started
            <ChevronRight className="w-5 h-5" />
          </Link>
        </div>
      </motion.section>
    </div>
  );
}
