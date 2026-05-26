const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message);
  }
}

async function request<T>(
  path: string,
  options: RequestInit = {},
  token?: string | null,
): Promise<T> {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(body.detail || res.statusText, res.status);
  }
  return res.json();
}

export const api = {
  register: (email: string, password: string) =>
    request<{ access_token: string }>("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  login: (email: string, password: string) =>
    request<{ access_token: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  me: (token: string) =>
    request<{
      id: number;
      email: string;
      role: string;
      membership_type: string;
      credits: number;
    }>("/auth/me", {}, token),

  positions: (params?: {
    page?: number;
    q?: string;
    country?: string;
    research_area?: string;
    funding?: string;
    source_name?: string;
    status?: string;
    sort?: string;
  }) => {
    const search = new URLSearchParams();
    if (params?.page) search.set("page", String(params.page));
    if (params?.q) search.set("q", params.q);
    if (params?.country) search.set("country", params.country);
    if (params?.research_area) search.set("research_area", params.research_area);
    if (params?.funding) search.set("funding", params.funding);
    if (params?.source_name) search.set("source_name", params.source_name);
    if (params?.status) search.set("status", params.status);
    if (params?.sort) search.set("sort", params.sort);
    const qs = search.toString();
    return request<{
      items: Position[];
      total: number;
      page: number;
      page_size: number;
    }>(`/positions${qs ? `?${qs}` : ""}`);
  },

  creditBalance: (token: string) =>
    request<{ credits: number; membership_type: string }>("/credits/balance", {}, token),

  creditCosts: () =>
    request<{ costs: { feature: string; credits: number }[] }>("/credits/costs"),
};

export interface Position {
  id: number;
  title: string;
  university: string;
  country: string;
  city: string | null;
  research_area: string | null;
  funding: string | null;
  deadline: string | null;
  description: string | null;
  source_name: string | null;
  source_url: string | null;
  application_url: string | null;
  status: string;
}
