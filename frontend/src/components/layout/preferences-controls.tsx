"use client";

import { Moon, Sun, Monitor } from "lucide-react";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";
import { useI18n } from "@/components/providers/i18n-provider";
import { LOCALES, type Locale } from "@/lib/i18n";

type Variant = "compact" | "full";

export function PreferencesControls({ variant = "compact" }: { variant?: Variant }) {
  const { theme, setTheme, resolvedTheme } = useTheme();
  const { locale, setLocale, t } = useI18n();
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);

  if (!mounted) {
    return <div className={variant === "compact" ? "h-9 w-24" : "h-20"} />;
  }

  const themes = [
    { value: "light", icon: Sun, label: t("preferences.themeLight") },
    { value: "dark", icon: Moon, label: t("preferences.themeDark") },
    { value: "system", icon: Monitor, label: t("preferences.themeSystem") },
  ] as const;

  if (variant === "full") {
    return (
      <div className="space-y-6">
        <div>
          <h3 className="text-sm font-medium text-foreground">{t("preferences.theme")}</h3>
          <p className="mt-1 text-sm text-muted">{t("settings.appearanceDesc")}</p>
          <div className="mt-3 flex flex-wrap gap-2">
            {themes.map(({ value, icon: Icon, label }) => (
              <button
                key={value}
                type="button"
                onClick={() => setTheme(value)}
                className={cn(
                  "flex items-center gap-2 rounded-xl border px-4 py-2.5 text-sm transition",
                  (theme === value || (!theme && value === "dark"))
                    ? "border-violet-500/50 bg-violet-500/10 text-violet-600 dark:text-violet-300"
                    : "border-border bg-card text-muted hover:text-foreground",
                )}
              >
                <Icon className="h-4 w-4" />
                {label}
              </button>
            ))}
          </div>
          <p className="mt-2 text-xs text-muted">
            {resolvedTheme === "light" ? "☀️" : "🌙"} {resolvedTheme}
          </p>
        </div>
        <div>
          <h3 className="text-sm font-medium text-foreground">{t("preferences.language")}</h3>
          <p className="mt-1 text-sm text-muted">{t("settings.languageDesc")}</p>
          <div className="mt-3 flex gap-2">
            {LOCALES.map(({ value, label }) => (
              <button
                key={value}
                type="button"
                onClick={() => setLocale(value as Locale)}
                className={cn(
                  "rounded-xl border px-4 py-2.5 text-sm transition",
                  locale === value
                    ? "border-violet-500/50 bg-violet-500/10 text-violet-600 dark:text-violet-300"
                    : "border-border bg-card text-muted hover:text-foreground",
                )}
              >
                {label}
              </button>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-1 rounded-xl border border-border bg-card/80 p-1">
      <button
        type="button"
        onClick={() => setTheme(resolvedTheme === "dark" ? "light" : "dark")}
        className="rounded-lg p-2 text-muted transition hover:bg-foreground/5 hover:text-foreground"
        title={t("preferences.theme")}
        aria-label={t("preferences.theme")}
      >
        {resolvedTheme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
      </button>
      <div className="h-4 w-px bg-border" />
      {LOCALES.map(({ value, label }) => (
        <button
          key={value}
          type="button"
          onClick={() => setLocale(value as Locale)}
          className={cn(
            "rounded-lg px-2 py-1.5 text-xs font-medium transition",
            locale === value
              ? "bg-violet-500/15 text-violet-600 dark:text-violet-300"
              : "text-muted hover:text-foreground",
          )}
        >
          {label}
        </button>
      ))}
    </div>
  );
}
