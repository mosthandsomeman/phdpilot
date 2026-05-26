"use client";

import { GraduationCap } from "lucide-react";
import { useI18n } from "@/components/providers/i18n-provider";

export function Footer() {
  const { t } = useI18n();

  return (
    <footer className="border-t border-border px-6 py-12">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 md:flex-row">
        <div className="flex items-center gap-2 text-muted">
          <GraduationCap className="h-5 w-5" />
          <span>{t("footer.copyright")}</span>
        </div>
        <p className="text-sm text-muted">{t("footer.tagline")}</p>
      </div>
    </footer>
  );
}
