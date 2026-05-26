"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  Briefcase,
  CreditCard,
  GraduationCap,
  LayoutDashboard,
  LogOut,
  Mail,
  Settings,
  User,
  Users,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { clearToken } from "@/lib/auth";
import { useI18n } from "@/components/providers/i18n-provider";
import { PreferencesControls } from "@/components/layout/preferences-controls";

const navKeys = [
  { href: "/dashboard", key: "dashboard", icon: LayoutDashboard },
  { href: "/positions", key: "positions", icon: Briefcase },
  { href: "/professors", key: "professors", icon: Users },
  { href: "/applications", key: "applications", icon: Briefcase },
  { href: "/emails", key: "emails", icon: Mail },
  { href: "/profile", key: "profile", icon: User },
  { href: "/billing", key: "billing", icon: CreditCard },
  { href: "/settings", key: "settings", icon: Settings },
] as const;

export function Sidebar({ credits }: { credits?: number }) {
  const pathname = usePathname();
  const router = useRouter();
  const { t } = useI18n();

  function logout() {
    clearToken();
    router.push("/login");
  }

  return (
    <aside className="flex h-screen w-64 flex-col border-r border-border bg-background/80 backdrop-blur-xl">
      <div className="flex h-16 items-center justify-between gap-2 border-b border-border px-4">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-violet-600 to-indigo-600">
            <GraduationCap className="h-4 w-4 text-white" />
          </div>
          <span className="font-semibold text-foreground">{t("common.brand")}</span>
        </div>
      </div>
      <div className="px-3 pt-3">
        <PreferencesControls />
      </div>
      <nav className="flex-1 space-y-1 p-3">
        {navKeys.map((item) => {
          const active = pathname === item.href || pathname.startsWith(item.href + "/");
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition",
                active
                  ? "bg-violet-500/15 text-violet-600 dark:text-violet-300"
                  : "text-muted hover:bg-foreground/5 hover:text-foreground",
              )}
            >
              <item.icon className="h-4 w-4 shrink-0" />
              {t(`nav.${item.key}`)}
            </Link>
          );
        })}
      </nav>
      {credits !== undefined && (
        <div className="mx-3 mb-3 rounded-xl border border-violet-500/20 bg-violet-500/10 p-4">
          <p className="text-xs text-muted">{t("nav.creditsBalance")}</p>
          <p className="text-2xl font-bold text-foreground">{credits}</p>
        </div>
      )}
      <button
        onClick={logout}
        className="mx-3 mb-4 flex items-center gap-2 rounded-xl px-3 py-2.5 text-sm text-muted transition hover:bg-foreground/5 hover:text-foreground"
      >
        <LogOut className="h-4 w-4" />
        {t("nav.logout")}
      </button>
    </aside>
  );
}
