"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Sidebar } from "@/components/layout/sidebar";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { useI18n } from "@/components/providers/i18n-provider";

export function DashboardShell({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { t } = useI18n();
  const [credits, setCredits] = useState<number | undefined>();
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.replace("/login");
      return;
    }
    Promise.all([api.me(token), api.creditBalance(token)])
      .then(([user, balance]) => {
        setCredits(balance.credits ?? user.credits);
        setReady(true);
      })
      .catch(() => router.replace("/login"));
  }, [router]);

  if (!ready) {
    return (
      <div className="flex h-screen items-center justify-center bg-background text-muted">
        {t("common.loading")}
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar credits={credits} />
      <main className="flex-1 overflow-auto p-8">{children}</main>
    </div>
  );
}
