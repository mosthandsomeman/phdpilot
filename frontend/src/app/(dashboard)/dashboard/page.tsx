"use client";

import Link from "next/link";
import { ArrowRight, Briefcase, Mail, Sparkles } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useI18n } from "@/components/providers/i18n-provider";

export default function DashboardPage() {
  const { t, dict } = useI18n();

  const stats = [
    { label: t("dashboard.savedPositions"), value: "—", href: "/positions" },
    { label: t("dashboard.applications"), value: "—", href: "/applications" },
    { label: t("dashboard.outreachDrafts"), value: "—", href: "/emails" },
  ];

  return (
    <div className="max-w-5xl">
      <h1 className="text-3xl font-bold text-foreground">{t("dashboard.title")}</h1>
      <p className="mt-2 text-muted">{t("dashboard.subtitle")}</p>

      <div className="mt-8 grid gap-4 md:grid-cols-3">
        {stats.map((s) => (
          <Link key={s.label} href={s.href}>
            <Card className="cursor-pointer transition hover:border-violet-500/30">
              <p className="text-sm text-muted">{s.label}</p>
              <p className="mt-2 text-3xl font-bold text-foreground">{s.value}</p>
            </Card>
          </Link>
        ))}
      </div>

      <Card className="mt-8 border-violet-500/20 bg-gradient-to-r from-violet-500/10 to-indigo-500/5">
        <div className="flex items-start gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-violet-500/20">
            <Sparkles className="h-6 w-6 text-violet-600 dark:text-violet-400" />
          </div>
          <div className="flex-1">
            <h2 className="text-lg font-semibold text-foreground">{t("dashboard.aiComing")}</h2>
            <p className="mt-1 text-sm text-muted">{t("dashboard.aiComingDesc")}</p>
            <Link href="/positions" className="mt-4 inline-block">
              <Button size="sm" className="group">
                {t("dashboard.browsePositions")}
                <ArrowRight className="h-4 w-4 transition group-hover:translate-x-0.5" />
              </Button>
            </Link>
          </div>
        </div>
      </Card>

      <div className="mt-8 grid gap-4 md:grid-cols-2">
        <Card>
          <Briefcase className="h-5 w-5 text-violet-600 dark:text-violet-400" />
          <h3 className="mt-3 font-medium text-foreground">{t("dashboard.quickActions")}</h3>
          <ul className="mt-3 space-y-2 text-sm text-muted">
            {dict.dashboard.quickItems.map((item) => (
              <li key={item}>· {item}</li>
            ))}
          </ul>
        </Card>
        <Card>
          <Mail className="h-5 w-5 text-violet-600 dark:text-violet-400" />
          <h3 className="mt-3 font-medium text-foreground">{t("dashboard.creditCosts")}</h3>
          <ul className="mt-3 space-y-2 text-sm text-muted">
            {dict.dashboard.creditItems.map((item) => (
              <li key={item}>· {item}</li>
            ))}
          </ul>
        </Card>
      </div>
    </div>
  );
}
