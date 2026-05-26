"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useI18n } from "@/components/providers/i18n-provider";

export function Hero() {
  const { t } = useI18n();

  return (
    <section className="relative flex min-h-screen flex-col items-center justify-center px-6 pt-24 mesh-bg">
      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7 }}
        className="mx-auto max-w-4xl text-center"
      >
        <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-violet-500/30 bg-violet-500/10 px-4 py-1.5 text-sm text-violet-600 dark:text-violet-300">
          <Sparkles className="h-4 w-4" />
          {t("hero.badge")}
        </div>
        <h1 className="text-5xl font-bold tracking-tight text-foreground md:text-7xl">
          {t("hero.title")}{" "}
          <span className="gradient-text">{t("hero.titleHighlight")}</span>{" "}
          {t("hero.titleSuffix")}
        </h1>
        <p className="mx-auto mt-6 max-w-2xl text-lg leading-relaxed text-muted">
          {t("hero.subtitle")}
        </p>
        <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <Link href="/register">
            <Button size="lg" className="group">
              {t("hero.cta")}
              <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
            </Button>
          </Link>
          <Link href="/dashboard">
            <Button variant="secondary" size="lg">
              {t("hero.demo")}
            </Button>
          </Link>
        </div>
        <p className="mt-6 text-sm text-muted">{t("hero.footnote")}</p>
      </motion.div>
    </section>
  );
}
