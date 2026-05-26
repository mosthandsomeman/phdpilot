"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { en, zh, LOCALE_STORAGE_KEY, type Dictionary, type Locale } from "@/lib/i18n";

type I18nContextValue = {
  locale: Locale;
  setLocale: (locale: Locale) => void;
  dict: Dictionary;
  t: (key: string, vars?: Record<string, string | number>) => string;
};

const I18nContext = createContext<I18nContextValue | null>(null);

const dictionaries: Record<Locale, Dictionary> = { en, zh };

function getByPath(obj: Record<string, unknown>, path: string): unknown {
  return path.split(".").reduce<unknown>((acc, part) => {
    if (acc && typeof acc === "object" && part in acc) {
      return (acc as Record<string, unknown>)[part];
    }
    return undefined;
  }, obj);
}

export function I18nProvider({ children }: { children: React.ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>("en");
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem(LOCALE_STORAGE_KEY) as Locale | null;
    if (stored === "en" || stored === "zh") {
      setLocaleState(stored);
    } else if (typeof navigator !== "undefined" && navigator.language.startsWith("zh")) {
      setLocaleState("zh");
    }
    setReady(true);
  }, []);

  const setLocale = useCallback((next: Locale) => {
    setLocaleState(next);
    localStorage.setItem(LOCALE_STORAGE_KEY, next);
    document.documentElement.lang = next === "zh" ? "zh-CN" : "en";
  }, []);

  useEffect(() => {
    if (ready) {
      document.documentElement.lang = locale === "zh" ? "zh-CN" : "en";
    }
  }, [locale, ready]);

  const dict = dictionaries[locale];

  const t = useCallback(
    (key: string, vars?: Record<string, string | number>) => {
      let value = getByPath(dict as unknown as Record<string, unknown>, key);
      if (typeof value !== "string") return key;
      if (vars) {
        Object.entries(vars).forEach(([k, v]) => {
          value = (value as string).replace(`{${k}}`, String(v));
        });
      }
      return value as string;
    },
    [dict],
  );

  const value = useMemo(
    () => ({ locale, setLocale, dict, t }),
    [locale, setLocale, dict, t],
  );

  if (!ready) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background text-muted">
        ...
      </div>
    );
  }

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export function useI18n() {
  const ctx = useContext(I18nContext);
  if (!ctx) throw new Error("useI18n must be used within I18nProvider");
  return ctx;
}
