export const en = {
  common: {
    brand: "PhD Pilot",
    loading: "Loading...",
    email: "Email",
    password: "Password",
    credits: "Credits",
    save: "Save",
    cancel: "Cancel",
  },
  preferences: {
    theme: "Theme",
    themeLight: "Light",
    themeDark: "Dark",
    themeSystem: "System",
    language: "Language",
    langEn: "English",
    langZh: "中文",
  },
  nav: {
    features: "Features",
    pricing: "Pricing",
    faq: "FAQ",
    login: "Log in",
    getStarted: "Get started",
    dashboard: "Dashboard",
    positions: "Positions",
    professors: "Professors",
    applications: "Applications",
    emails: "Emails",
    profile: "Profile",
    billing: "Billing",
    settings: "Settings",
    logout: "Log out",
    creditsBalance: "Credits balance",
  },
  hero: {
    badge: "AI Copilot for European PhD Applications",
    title: "Your AI Copilot for",
    titleHighlight: "European PhD",
    titleSuffix: "Applications",
    subtitle:
      "Search funded positions, match with supervisors, analyze research fit, and craft personalized outreach — all in one modern workflow.",
    cta: "Start free — 100 Credits",
    demo: "View demo dashboard",
    footnote: "No credit card · AI / CS / Medical AI / Agriculture focus",
  },
  features: {
    title: "Built for the full PhD application workflow",
    subtitle: "Not a chatbot. Not a traditional agency. An AI-native application platform.",
    items: {
      positions: {
        title: "Position aggregation",
        desc: "Daily updates from EURAXESS, FindAPhD, and Academic Positions.",
      },
      match: {
        title: "AI match analysis",
        desc: "Understand fit, skill gaps, and tailored application advice.",
      },
      supervisor: {
        title: "Supervisor insights",
        desc: "Research direction summaries from profiles and recent papers.",
      },
      outreach: {
        title: "Outreach generation",
        desc: "Personalized cold emails with multi-version review workflow.",
      },
      workspace: {
        title: "Application workspace",
        desc: "Track Saved → Applied → Interview → Offer like Linear.",
      },
      credits: {
        title: "Credits-based AI",
        desc: "Transparent usage — no raw token billing surprises.",
      },
    },
  },
  pricing: {
    title: "Simple, transparent pricing",
    subtitle: "Credits instead of confusing token bills",
    popular: "Popular",
    free: {
      name: "Free",
      price: "¥0",
      desc: "100 Credits on signup",
      features: [
        "Basic position search",
        "3 AI analyses / day",
        "1 outreach / day",
        "20 saved positions",
      ],
      cta: "Get started",
    },
    pro: {
      name: "Pro",
      price: "¥39–99",
      period: "/ month",
      desc: "5,000–50,000 Credits",
      features: [
        "Unlimited position analysis",
        "Advanced supervisor matching",
        "Multi-version outreach",
        "Priority AI response",
      ],
      cta: "Coming in Phase 4",
    },
  },
  faq: {
    title: "FAQ",
    items: [
      {
        q: "Which countries and fields are supported?",
        a: "MVP focuses on European positions in AI, CS, Medical AI, and Agricultural research.",
      },
      {
        q: "How do Credits work?",
        a: "Each AI feature costs a fixed number of Credits (e.g. match analysis: 5, outreach: 15). No surprise token bills.",
      },
      {
        q: "Where do positions come from?",
        a: "Aggregated from EURAXESS, FindAPhD, and Academic Positions with daily updates.",
      },
    ],
  },
  footer: {
    tagline: "AI Copilot for European PhD Applications",
    copyright: "PhD Pilot © 2026",
  },
  auth: {
    welcomeBack: "Welcome back",
    signInSubtitle: "Sign in to PhD Pilot",
    createAccount: "Create account",
    signupBonus: "100 free Credits on signup",
    signIn: "Sign in",
    signingIn: "Signing in...",
    createAccountBtn: "Create account",
    creating: "Creating account...",
    noAccount: "No account?",
    registerFree: "Register free",
    hasAccount: "Already have an account?",
    loginFailed: "Login failed",
    registerFailed: "Registration failed",
    passwordMin: "Password must be at least 8 characters",
    emailPlaceholder: "you@university.edu",
    passwordPlaceholder: "Min. 8 characters",
  },
  dashboard: {
    title: "Dashboard",
    subtitle: "Your PhD application command center",
    savedPositions: "Saved positions",
    applications: "Applications",
    outreachDrafts: "Outreach drafts",
    aiComing: "AI features coming in Phase 3",
    aiComingDesc:
      "Position match analysis, supervisor insights, and personalized outreach generation.",
    browsePositions: "Browse positions",
    quickActions: "Quick actions",
    quickItems: [
      "Search European PhD positions",
      "Complete your applicant profile",
      "Track application pipeline",
    ],
    creditCosts: "Credit costs",
    creditItems: [
      "Match analysis — 5 credits",
      "Supervisor analysis — 10 credits",
      "Outreach generation — 15 credits",
    ],
  },
  positions: {
    title: "Positions",
    openCount: "{count} open positions",
    searchPlaceholder: "Search title, university...",
    loading: "Loading positions...",
    empty: "No positions yet. Run the crawler or seed script.",
    deadline: "Deadline",
    filterCountry: "Country",
    filterSource: "Source",
    filterFunding: "Funding",
    allCountries: "All countries",
    allSources: "All sources",
    viewSource: "View original",
  },
  billing: {
    title: "Billing",
    subtitle: "Credits & membership",
    currentPlan: "Current plan",
    creditsBalance: "Credits balance",
    featureCosts: "Feature costs",
  },
  profile: {
    title: "Profile",
    subtitle: "Complete your applicant profile for better AI matching (Phase 2+).",
  },
  professors: {
    title: "Professors",
    subtitle: "Supervisor analysis — Phase 3",
  },
  applications: {
    title: "Applications",
    subtitle: "Kanban workspace — Phase 2",
  },
  emails: {
    title: "Emails",
    subtitle: "Outreach editor — Phase 3",
  },
  settings: {
    title: "Settings",
    subtitle: "Account preferences",
    appearance: "Appearance",
    appearanceDesc: "Choose light or dark interface",
    languageDesc: "Choose display language",
  },
} as const;

/** Same nested keys as `en`, but leaf values are any locale string (not English literals). */
type DeepString<T> = T extends string
  ? string
  : T extends object
    ? { [K in keyof T]: DeepString<T[K]> }
    : T;

export type Dictionary = DeepString<typeof en>;
