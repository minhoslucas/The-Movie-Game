export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-3xl font-bold mb-4">Next.js + Neon Demo</h1>
      <NeonTime />
    </main>
  );
}

async function getNeonTime() {
  const res = await fetch('/api/neon');
  const data = await res.json();
  return data.time || data.error;
}

import { useEffect, useState } from 'react';

function NeonTime() {
  const [time, setTime] = useState<string>('Carregando...');

  useEffect(() => {
    getNeonTime().then(setTime);
  }, []);

  return (
    <div className="mt-4 text-lg">Horário do banco Neon: {time}</div>
  );
}
