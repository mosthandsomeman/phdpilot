"use client";

import { useCallback, useEffect, useState } from "react";
import { Calendar, ExternalLink, MapPin, Search } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { api, Position } from "@/lib/api";
import { useI18n } from "@/components/providers/i18n-provider";

const COUNTRIES = [
  "",
  "Germany",
  "Netherlands",
  "Sweden",
  "Norway",
  "Denmark",
  "Finland",
  "Italy",
  "Spain",
  "Portugal",
  "Greece",
];

const SOURCES = ["", "EURAXESS", "FindAPhD", "Academic Positions"];

export default function PositionsPage() {
  const { t } = useI18n();
  const [positions, setPositions] = useState<Position[]>([]);
  const [total, setTotal] = useState(0);
  const [q, setQ] = useState("");
  const [country, setCountry] = useState("");
  const [sourceName, setSourceName] = useState("");
  const [funding, setFunding] = useState("");
  const [loading, setLoading] = useState(true);

  const load = useCallback(() => {
    setLoading(true);
    api
      .positions({
        q: q || undefined,
        country: country || undefined,
        source_name: sourceName || undefined,
        funding: funding || undefined,
        status: "active",
      })
      .then((data) => {
        setPositions(data.items);
        setTotal(data.total);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [q, country, sourceName, funding]);

  useEffect(() => {
    const timer = setTimeout(load, 300);
    return () => clearTimeout(timer);
  }, [load]);

  return (
    <div className="max-w-5xl">
      <div className="flex flex-col gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground">{t("positions.title")}</h1>
          <p className="mt-1 text-muted">{t("positions.openCount", { count: total })}</p>
        </div>

        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          <div className="relative sm:col-span-2 lg:col-span-4">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" />
            <Input
              className="pl-10"
              placeholder={t("positions.searchPlaceholder")}
              value={q}
              onChange={(e) => setQ(e.target.value)}
            />
          </div>
          <select
            className="h-11 rounded-xl border border-border bg-foreground/5 px-3 text-sm text-foreground"
            value={country}
            onChange={(e) => setCountry(e.target.value)}
          >
            <option value="">{t("positions.allCountries")}</option>
            {COUNTRIES.filter(Boolean).map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
          <select
            className="h-11 rounded-xl border border-border bg-foreground/5 px-3 text-sm text-foreground"
            value={sourceName}
            onChange={(e) => setSourceName(e.target.value)}
          >
            <option value="">{t("positions.allSources")}</option>
            {SOURCES.filter(Boolean).map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
          <Input
            placeholder={t("positions.filterFunding")}
            value={funding}
            onChange={(e) => setFunding(e.target.value)}
          />
        </div>
      </div>

      {loading ? (
        <p className="mt-12 text-muted">{t("positions.loading")}</p>
      ) : positions.length === 0 ? (
        <Card className="mt-8 text-center text-muted">
          <p>{t("positions.empty")}</p>
        </Card>
      ) : (
        <div className="mt-8 grid gap-4">
          {positions.map((p) => (
            <Card key={p.id} className="transition hover:border-violet-500/25">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                <div className="min-w-0 flex-1">
                  <h2 className="text-lg font-semibold text-foreground">{p.title}</h2>
                  <p className="mt-1 text-violet-600 dark:text-violet-300">{p.university}</p>
                  <div className="mt-3 flex flex-wrap gap-4 text-sm text-muted">
                    <span className="flex items-center gap-1">
                      <MapPin className="h-3.5 w-3.5" />
                      {p.country}
                      {p.city ? ` · ${p.city}` : ""}
                    </span>
                    {p.deadline && (
                      <span className="flex items-center gap-1">
                        <Calendar className="h-3.5 w-3.5" />
                        {t("positions.deadline")} {p.deadline}
                      </span>
                    )}
                    {p.source_name && (
                      <span className="rounded-md bg-foreground/5 px-2 py-0.5 text-xs">
                        {p.source_name}
                      </span>
                    )}
                  </div>
                  {p.research_area && (
                    <p className="mt-2 text-sm text-muted">{p.research_area}</p>
                  )}
                  {p.source_url && (
                    <a
                      href={p.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="mt-3 inline-flex items-center gap-1 text-sm text-violet-600 hover:underline dark:text-violet-400"
                    >
                      {t("positions.viewSource")}
                      <ExternalLink className="h-3.5 w-3.5" />
                    </a>
                  )}
                </div>
                {p.funding && (
                  <span className="shrink-0 rounded-lg bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-600 dark:text-emerald-400">
                    {p.funding}
                  </span>
                )}
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
