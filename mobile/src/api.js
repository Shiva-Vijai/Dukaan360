// Set EXPO_PUBLIC_API_URL for the local LAN backend or the deployed Render API.
const BASE = (process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000').replace(/\/$/, '');
export async function api(path, options={}) {
  const response = await fetch(`${BASE}${path}`, {headers:{'Content-Type':'application/json'}, ...options});
  if (!response.ok) throw new Error((await response.json().catch(()=>({}))).detail || 'Request failed');
  return response.json();
}
