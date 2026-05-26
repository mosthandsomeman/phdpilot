"use client";

import Link from "next/link";
import { GraduationCap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PreferencesControls } from "@/components/layout/preferences-controls";
import { useI18n } from "@/components/providers/i18n-provider";

export function Navbar() {
  const { t } = useI18n();

  return (
    <header className="fixed top-0 z-50 w-full border-b border-border bg-background/80 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
        <Link href="/" className="flex items-center gap-2 font-semibold text-foreground">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-violet-600 to-indigo-600">
            <GraduationCap className="h-5 w-5 text-white" />
          </div>
          {t("common.brand")}
        </Link>
        <nav className="hidden items-center gap-8 text-sm text-muted md:flex">
          <a href="#features" className="transition hover:text-foreground">
            {t("nav.features")}
          </a>
          <a href="#pricing" className="transition hover:text-foreground">
            {t("nav.pricing")}
          </a>
          <a href="#faq" className="transition hover:text-foreground">
            {t("nav.faq")}
          </a>
        </nav>
        <div className="flex items-center gap-3">
          <PreferencesControls />
          <Link href="/login" className="hidden sm:block">
            <Button variant="ghost" size="sm">
              {t("nav.login")}
            </Button>
          </Link>
          <Link href="/register">
            <Button size="sm">{t("nav.getStarted")}</Button>
          </Link>
        </div>
      </div>
    </header>
  );
}
