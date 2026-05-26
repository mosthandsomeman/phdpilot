"use client";

import { useI18n } from "@/components/providers/i18n-provider";

export default function ProfilePage() {
  const { t } = useI18n();

  return (
    <div className="max-w-3xl">
      <h1 className="text-3xl font-bold text-foreground">{t("profile.title")}</h1>
      <p className="mt-2 text-muted">{t("profile.subtitle")}</p>
    </div>
  );
}
