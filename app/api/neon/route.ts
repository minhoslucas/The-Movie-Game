import { NextResponse } from 'next/server';
import { Pool } from 'pg';

// Substitua pelos dados do seu Neon
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

export async function GET() {
  try {
    const client = await pool.connect();
    const result = await client.query('SELECT NOW()');
    client.release();
    return NextResponse.json({ time: result.rows[0].now });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
