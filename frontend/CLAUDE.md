# Frontend -- React + Vite + TypeScript

## Commands
- `npm run dev` -- Start dev server (localhost:5173)
- `npm run build` -- Production build to dist/
- `npm run preview` -- Preview production build locally

## Visual Identity
Read `spec/visual-identity-research.md` for full context. Key constraints:

**Feeling:** Vertraut (trustworthy), Klar (clear), Ruhig (calm), Warm, Kompetent (competent), Direkt (direct), Modern.

**Color direction:**
| Token | Value | Notes |
|-------|-------|-------|
| Background | Dark charcoal (#1F1B1C range) or warm off-white | Dark = premium/modern. Warm white = approachable. Pick one. Avoid cold white. |
| Primary accent | Warm amber (#F5A623 range) or teal (#2EC4B6 range) | Amber = warm/trustworthy. Teal = modern/fresh. Pick one. |
| Text | White on dark, or dark charcoal on light | High contrast. Readability for a 50-year-old Meister is non-negotiable. |
| Success | Green | On track / positive margin |
| Warning | Amber | Needs attention / margin pressure |
| Danger | Red | Problem / negative margin |

**Avoid:** Corporate blue (#005BAB), neon green (#B0CA00), gradients, cold SaaS aesthetics.

**Typography:** Inter (clean sans-serif). Large headings, generous spacing. No decorative fonts.

**Icons:** Minimal, functional. No 3D illustrations, no cartoons, no emoji.

## Conventions
- Functional components with hooks. No class components.
- TypeScript interfaces for props and API response types.
- Tailwind CSS for all styling. No CSS modules, no styled-components.
- Keep components small (<80 lines). Extract when growing.
- API calls go through a single `api.ts` service file.
- All user-facing text in German. No English strings in the UI.
- Mobile-first: design for 375px width first, then scale up.

## Structure
```
src/
  components/    -- Reusable UI components
  pages/         -- Top-level views (one per screen from spec)
  api.ts         -- API client (fetch wrapper to backend)
  types.ts       -- Shared TypeScript interfaces
  App.tsx        -- Router + layout
  main.tsx       -- Entry point
```

## Screens (from spec)
8 screens total. See `spec/prototype-scope.md` for the full list and `spec/prototype-backlog.md` for build order.
