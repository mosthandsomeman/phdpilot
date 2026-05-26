export type Locale = "en" | "zh";

export const LOCALES: { value: Locale; label: string }[] = [
  { value: "en", label: "EN" },
  { value: "zh", label: "中文" },
];

export const LOCALE_STORAGE_KEY = "phd_pilot_locale";

export { en } from "./dictionaries/en";
export type { Dictionary } from "./dictionaries/en";
export { zh } from "./dictionaries/zh";
