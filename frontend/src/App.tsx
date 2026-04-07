import { Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import { Layout } from './components/ui/Layout';
import Home from './pages/Home';
import Pokedex from './pages/Pokedex';
import PokemonDetails from './pages/PokemonDetails';
import SpawnFinder from './pages/SpawnFinder';
import Compare from './pages/Compare';
import TeamBuilder from './pages/TeamBuilder';
import Favorites from './pages/Favorites';

function App() {
  return (
    <ThemeProvider>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/pokedex" element={<Pokedex />} />
          <Route path="/pokemon/:id" element={<PokemonDetails />} />
          <Route path="/spawns" element={<SpawnFinder />} />
          <Route path="/compare" element={<Compare />} />
          <Route path="/team-builder" element={<TeamBuilder />} />
          <Route path="/favorites" element={<Favorites />} />
        </Routes>
      </Layout>
    </ThemeProvider>
  );
}

export default App;
