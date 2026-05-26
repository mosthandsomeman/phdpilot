"use client";

import { motion } from "framer-motion";
import { Brain, Mail, Search, Target, Users, Workflow } from "lucide-react";
import { Card } from "@/components/ui/card";
import { useI18n } from "@/components/providers/i18n-provider";

const featureKeys = [
  { key: "positions", icon: Search },
  { key: "match", icon: Target },
  { key: "supervisor", icon: Users },
  { key: "outreach", icon: Mail },
  { key: "workspace", icon: Workflow },
  { key: "credits", icon: Brain },
] as const;

export function Features() {
  const { t } = useI18n();

  return (
    <section id="features" className="px-6 py-32">
      <div className="mx-auto max-w-6xl">
        <h2 className="text-center text-3xl font-bold text-foreground md:text-4xl">
          {t("features.title")}
        </h2>
        <p className="mx-auto mt-4 max-w-xl text-center text-muted">{t("features.subtitle")}</p>
        <div className="mt-16 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {featureKeys.map((f, i) => (
            <motion.div
              key={f.key}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.08 }}
            >
              <Card className="h-full transition-colors hover:border-violet-500/30">
                <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-violet-500/15 text-violet-600 dark:text-violet-400">
                  <f.icon className="h-5 w-5" />
                </div>
                <h3 className="text-lg font-semibold text-foreground">
                  {t(`features.items.${f.key}.title`)}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-muted">
                  {t(`features.items.${f.key}.desc`)}
                </p>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
