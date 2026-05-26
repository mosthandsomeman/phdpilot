"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { GraduationCap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { api, ApiError } from "@/lib/api";
import { setToken } from "@/lib/auth";
import { useI18n } from "@/components/providers/i18n-provider";
import { PreferencesControls } from "@/components/layout/preferences-controls";

export default function RegisterPage() {
  const router = useRouter();
  const { t } = useI18n();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");
    setLoading(true);
    const fd = new FormData(e.currentTarget);
    const password = fd.get("password") as string;
    if (password.length < 8) {
      setError(t("auth.passwordMin"));
      setLoading(false);
      return;
    }
    try {
      const { access_token } = await api.register(fd.get("email") as string, password);
      setToken(access_token);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof ApiError ? String(err.message) : t("auth.registerFailed"));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="relative flex min-h-screen items-center justify-center mesh-bg px-6">
      <div className="absolute right-6 top-6">
        <PreferencesControls />
      </div>
      <Card className="w-full max-w-md">
        <div className="mb-8 flex items-center gap-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-violet-600 to-indigo-600">
            <GraduationCap className="h-5 w-5 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-semibold text-foreground">{t("auth.createAccount")}</h1>
            <p className="text-sm text-muted">{t("auth.signupBonus")}</p>
          </div>
        </div>
        <form onSubmit={onSubmit} className="space-y-4">
          <div>
            <label className="mb-1.5 block text-sm text-muted">{t("common.email")}</label>
            <Input
              name="email"
              type="email"
              required
              placeholder={t("auth.emailPlaceholder")}
            />
          </div>
          <div>
            <label className="mb-1.5 block text-sm text-muted">{t("common.password")}</label>
            <Input
              name="password"
              type="password"
              required
              minLength={8}
              placeholder={t("auth.passwordPlaceholder")}
            />
          </div>
          {error && <p className="text-sm text-red-500">{error}</p>}
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? t("auth.creating") : t("auth.createAccountBtn")}
          </Button>
        </form>
        <p className="mt-6 text-center text-sm text-muted">
          {t("auth.hasAccount")}{" "}
          <Link href="/login" className="text-violet-600 hover:text-violet-500 dark:text-violet-400">
            {t("auth.signIn")}
          </Link>
        </p>
      </Card>
    </div>
  );
}
