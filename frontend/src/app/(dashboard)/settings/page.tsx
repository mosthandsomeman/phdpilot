"use client";

import { Card } from "@/components/ui/card";
import { PreferencesControls } from "@/components/layout/preferences-controls";
import { useI18n } from "@/components/providers/i18n-provider";

export default function SettingsPage() {
  const { t } = useI18n();

  return (
    <div className="max-w-2xl">
      <h1 className="text-3xl font-bold text-foreground">{t("settings.title")}</h1>
      <p className="mt-2 text-muted">{t("settings.subtitle")}</p>
      <Card className="mt-8">
        <PreferencesControls variant="full" />
      </Card>
    </div>
  );
}
