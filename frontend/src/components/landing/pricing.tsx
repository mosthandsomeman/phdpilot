"use client";

import { Check } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useI18n } from "@/components/providers/i18n-provider";

export function Pricing() {
  const { t, dict } = useI18n();

  const plans = [
    { id: "free" as const, highlight: false, href: "/register" },
    { id: "pro" as const, highlight: true, href: "/register" },
  ];

  return (
    <section id="pricing" className="px-6 py-32">
      <div className="mx-auto max-w-4xl">
        <h2 className="text-center text-3xl font-bold text-foreground">{t("pricing.title")}</h2>
        <p className="mt-4 text-center text-muted">{t("pricing.subtitle")}</p>
        <div className="mt-16 grid gap-8 md:grid-cols-2">
          {plans.map((plan) => {
            const p = dict.pricing[plan.id];
            return (
              <Card
                key={plan.id}
                className={
                  plan.highlight
                    ? "relative border-violet-500/40 bg-gradient-to-b from-violet-500/10 to-transparent"
                    : ""
                }
              >
                {plan.highlight && (
                  <span className="absolute -top-3 left-6 rounded-full bg-violet-600 px-3 py-0.5 text-xs font-medium text-white">
                    {t("pricing.popular")}
                  </span>
                )}
                <h3 className="text-xl font-semibold text-foreground">{p.name}</h3>
                <div className="mt-2 flex items-baseline gap-1">
                  <span className="text-4xl font-bold text-foreground">{p.price}</span>
                  {"period" in p && p.period && (
                    <span className="text-muted">{p.period}</span>
                  )}
                </div>
                <p className="mt-2 text-sm text-muted">{p.desc}</p>
                <ul className="mt-6 space-y-3">
                  {p.features.map((f) => (
                    <li key={f} className="flex items-center gap-2 text-sm text-foreground/80">
                      <Check className="h-4 w-4 shrink-0 text-violet-500" />
                      {f}
                    </li>
                  ))}
                </ul>
                <Link href={plan.href} className="mt-8 block">
                  <Button variant={plan.highlight ? "default" : "secondary"} className="w-full">
                    {p.cta}
                  </Button>
                </Link>
              </Card>
            );
          })}
        </div>
      </div>
    </section>
  );
}
