"use client";

import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { useI18n } from "@/components/providers/i18n-provider";

export default function BillingPage() {
  const { t } = useI18n();
  const [balance, setBalance] = useState<{ credits: number; membership_type: string } | null>(null);
  const [costs, setCosts] = useState<{ feature: string; credits: number }[]>([]);

  useEffect(() => {
    const token = getToken();
    if (!token) return;
    api.creditBalance(token).then(setBalance);
    api.creditCosts().then((r) => setCosts(r.costs));
  }, []);

  return (
    <div className="max-w-3xl">
      <h1 className="text-3xl font-bold text-foreground">{t("billing.title")}</h1>
      <p className="mt-2 text-muted">{t("billing.subtitle")}</p>

      <div className="mt-8 grid gap-6 md:grid-cols-2">
        <Card>
          <p className="text-sm text-muted">{t("billing.currentPlan")}</p>
          <p className="mt-2 text-2xl font-bold capitalize text-foreground">
            {balance?.membership_type ?? "—"}
          </p>
        </Card>
        <Card className="border-violet-500/20">
          <p className="text-sm text-muted">{t("billing.creditsBalance")}</p>
          <p className="mt-2 text-4xl font-bold text-foreground">{balance?.credits ?? "—"}</p>
        </Card>
      </div>

      <Card className="mt-8">
        <h2 className="font-semibold text-foreground">{t("billing.featureCosts")}</h2>
        <ul className="mt-4 divide-y divide-border">
          {costs.map((c) => (
            <li key={c.feature} className="flex justify-between py-3 text-sm">
              <span className="capitalize text-muted">{c.feature.replace(/_/g, " ")}</span>
              <span className="font-medium text-foreground">
                {c.credits} {t("common.credits")}
              </span>
            </li>
          ))}
        </ul>
      </Card>
    </div>
  );
}
