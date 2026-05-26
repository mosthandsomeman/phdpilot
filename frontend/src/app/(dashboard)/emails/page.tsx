"use client";

import { useI18n } from "@/components/providers/i18n-provider";

export default function EmailsPage() {
  const { t } = useI18n();

  return (
    <div>
      <h1 className="text-3xl font-bold text-foreground">{t("emails.title")}</h1>
      <p className="mt-2 text-muted">{t("emails.subtitle")}</p>
    </div>
  );
}
