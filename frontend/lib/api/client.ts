const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export async function fetchApi<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  try {
    const res = await fetch(url, { ...options, headers });
    if (!res.ok) {
      const errorText = await res.text();
      let errorJson;
      try { errorJson = JSON.parse(errorText); } catch {}
      const message = errorJson?.detail || errorJson?.message || `HTTP Error ${res.status}: ${res.statusText}`;
      throw new Error(message);
    }
    return await res.json();
  } catch (err: any) {
    console.error(`API Fetch Error [${endpoint}]:`, err);
    throw err;
  }
}
