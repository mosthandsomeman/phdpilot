"use client";

import { useI18n } from "@/components/providers/i18n-provider";

export function FAQ() {
  const { t, dict } = useI18n();

  return (
    <section id="faq" className="border-t border-border px-6 py-32">
      <div className="mx-auto max-w-2xl">
        <h2 className="text-center text-3xl font-bold text-foreground">{t("faq.title")}</h2>
        <dl className="mt-12 space-y-8">
          {dict.faq.items.map((item) => (
            <div key={item.q}>
              <dt className="text-lg font-medium text-foreground">{item.q}</dt>
              <dd className="mt-2 leading-relaxed text-muted">{item.a}</dd>
            </div>
          ))}
        </dl>
      </div>
    </section>
  );
}
