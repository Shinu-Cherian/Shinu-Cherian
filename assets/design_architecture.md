# Premium Terminal Card UI Architecture

## 1. Complete Wireframe

```text
╭──────────────────────────────────────────────────────────────────────────╮
│ 🔴 🟡 🟢                                                 ~/github-profile │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  [ (Avatar) ]  ➜ ~ whoami                                                │
│      🟢        John Doe                                                  │
│                Senior Software Engineer                                    │
│                [=========>          ] 50% Building open-source tools     │
│                                                                          │
│  ➜ ~ cat system_info.json                                                │
│  {                                                                       │
│    "os": "macOS",                                                        │
│    "location": "San Francisco, CA",                                      │
│    "role": "Frontend & Systems Architecture",                            │
│    "education": "B.S. Computer Science",                                 │
│    "open_to": ["Open Source", "Consulting"],                             │
│    "current_focus": "Rust & WebAssembly"                                 │
│  }                                                                       │
│                                                                          │
│  ➜ ~ ls -l ./tech_stack/                                                 │
│  drwxr-xr-x  Languages : TypeScript, Python, Rust, Go                    │
│  drwxr-xr-x  Frameworks: React, Next.js, Vue, Svelte                     │
│  drwxr-xr-x  Frontend  : TailwindCSS, Framer Motion, Three.js            │
│  drwxr-xr-x  Backend   : Node.js, Express, FastAPI, GraphQL              │
│  drwxr-xr-x  AI        : TensorFlow, PyTorch, OpenAI API                 │
│  drwxr-xr-x  Databases : PostgreSQL, Redis, MongoDB                      │
│  drwxr-xr-x  DevOps    : Docker, Kubernetes, GitHub Actions              │
│  drwxr-xr-x  Cloud     : AWS, Vercel, Cloudflare                         │
│                                                                          │
│  ➜ ~ ./fetch_projects.sh --featured                                      │
│  [✦] SynapseIQ                                                           │
│      AI-powered knowledge graph for personal notes.                      │
│      [React] [Python] [Neo4j]   [GitHub 🔗] [Live Demo 🔗]               │
│                                                                          │
│  [✦] HireTrack                                                           │
│      Kanban board for tracking job applications.                         │
│      [Next.js] [Prisma] [TRPC]  [GitHub 🔗] [Live Demo 🔗]               │
│                                                                          │
│  ➜ ~ ./fetch_oss.sh --recent                                             │
│  ✓ Merged PR #124 in 'vercel/next.js': Fixed hydration mismatch          │
│  ✓ Merged PR #42 in 'tailwindlabs/tailwindcss': Added dynamic imports    │
│                                                                          │
│  ➜ ~ ping contact_info                                                   │
│  - GitHub   : github.com/johndoe                                         │
│  - LinkedIn : linkedin.com/in/johndoe                                    │
│  - Portfolio: johndoe.dev                                                │
│  - Email    : hello@johndoe.dev                                          │
│                                                                          │
│  ──────────────────────────────────────────────────────────────────────  │
│  v2.1.0 • Generated Automatically • Last Updated: 2024-05-20 14:32 UTC   │
│  █                                                                       │
╰──────────────────────────────────────────────────────────────────────────╯
```

## 2. Spacing System (8pt Grid)

To maintain a structured, mathematical layout consistent with high-end UI design:

- **Base Unit**: `8px`
- **Outer Window Padding**: `32px` (top, bottom, left, right of the terminal body)
- **Window Chrome Height**: `40px` (macOS style title bar)
- **Section Gap**: `32px` (spacing between different command blocks)
- **Command Gap**: `16px` (spacing between the `➜ ~` prompt and the output)
- **Line Height**: `1.6` (for comfortable readability in lists/JSON)
- **Item Gap**: `8px` (horizontal spacing between badges/tags)

## 3. Typography System

We will use modern, developer-favorite monospaced fonts to reinforce the terminal aesthetic.

- **Primary Font Family**: `JetBrains Mono, Fira Code, Geist Mono, monospace` (prioritized in the SVG `<style>`).
- **Font Weights**:
  - `400` (Regular) - Standard output, JSON keys, standard text.
  - `500` (Medium) - Values, Project titles, Section headers.
  - `700` (Bold) - Commands, Name, Important status.
- **Font Sizes**:
  - **Avatar Name**: `20px`
  - **Command Prompt (`➜ ~`)**: `14px`
  - **Standard Output (JSON, Lists)**: `13px`
  - **Badges/Tags**: `11px`
  - **Footer Text**: `11px`

## 4. Color Palette (Deep Space Glow)

Inspired by Warp, Ghostty, and modern syntax themes (like Tokyo Night and One Dark).

- **Background Gradient**:
  - `#0D1117` to `#161B22` (GitHub Dark Dimmed vibe) or a solid deep purple-black `#0F0F14`.
- **Window Border/Chrome**: `#2D2E3D` with a very subtle `<filter>` drop shadow for glassmorphism.
- **Window Controls**: `#FF5F56` (Close), `#FFBD2E` (Minimize), `#27C93F` (Expand).
- **Text & Syntax Highlighting**:
  - **Primary Text (Output)**: `#A9B1D6` (Soft cool gray)
  - **Command Prompt Path (`~/`)**: `#7AA2F7` (Electric Blue)
  - **Command Prompt Arrow (`➜`)**: `#9ECE6A` (Neon Green) or `#C678DD` (Purple)
  - **JSON Keys / Variables**: `#F7768E` (Pink/Red)
  - **JSON Strings / Values**: `#9ECE6A` (Green)
  - **Keywords (drwxr-xr-x)**: `#565F89` (Muted Indigo)
  - **Tech Stack Badges**: `#1A1B26` (Background) with `#7AA2F7` (Text)
  - **Cursor / Blinking Block**: `#E0E2EA`

## 5. Terminal Styling Decisions

- **Window Chrome**: Standard 3-dot window controls aligned to the left, with the title `~/github-profile` centered in muted text.
- **Command Simulation**: Each section of the profile is preceded by a simulated terminal command to establish the metaphor (e.g., `whoami`, `cat system_info.json`, `ls -l`, `./fetch_projects.sh`).
- **Syntax Highlighting**: Real code syntax highlighting mapped to the SVG text elements to make it feel like an authentic IDE/Terminal experience.
- **Status Indicators**: A pulsing SVG animation (using `<animate>`) on a tiny circular dot next to the avatar to represent "online" or "active" status.
- **Loading Bars**: ASCII-style loading bars for skills or status (e.g., `[=======>   ] 70%`).

## 6. Responsive Layout Decisions

- **SVG Dimensions**: 
  - Width: `800px` (Native 100% width on desktop GitHub, scales down flawlessly on mobile).
  - Height: `Dynamic / Auto` based on content, but typically ~`1200px`.
- **ViewBox**: `<svg viewBox="0 0 800 1200" width="100%" height="auto">`
- **Flexibility**: We will utilize SVG's `<foreignObject>` for complex wrapping (if strictly needed) OR mathematically plot `x` and `y` coordinates for `<text>` elements to ensure absolute precision across all browsers. Because standard `<text>` scaling is safer in GitHub's image caching (Camo), strict `x, y` positioning combined with `dy="1.5em"` for multiline is preferred over `foreignObject` (which GitHub Camo sometimes strips).

## 7. SVG Component Hierarchy

The SVG will be highly organized using `<g>` tags, resembling a DOM structure.

```xml
<svg>
  <defs>
    <!-- Fonts, Shadows, Blurs, Gradients, ClipPaths (for circular avatar) -->
  </defs>
  
  <g id="window">
    <rect id="window-background" />
    <rect id="window-border" />
    
    <g id="window-chrome">
      <circle class="btn-close" />
      <circle class="btn-min" />
      <circle class="btn-max" />
      <text class="title">~/github-profile</text>
    </g>

    <g id="terminal-body" transform="translate(32, 72)">
      
      <!-- HEADER -->
      <g id="section-whoami">
        <g class="prompt" />
        <image class="avatar" clip-path="url(#avatar-clip)" />
        <circle class="status-indicator" />
        <text class="name" />
        <text class="subtitle" />
        <text class="status-bar" />
      </g>

      <!-- SYSTEM INFO -->
      <g id="section-sysinfo" transform="translate(0, 160)">
        <g class="prompt" />
        <g class="json-output">
          <!-- Text spans with syntax highlighting colors -->
        </g>
      </g>

      <!-- TECH STACK -->
      <g id="section-techstack" transform="translate(0, 360)">
        <g class="prompt" />
        <g class="ls-output" />
      </g>

      <!-- FEATURED PROJECTS -->
      <g id="section-projects" transform="translate(0, 560)">
        <g class="prompt" />
        <g class="project-card-1" />
        <g class="project-card-2" />
      </g>

      <!-- OPEN SOURCE -->
      <g id="section-oss" transform="translate(0, 760)">
        <g class="prompt" />
        <g class="oss-list" />
      </g>

      <!-- CONTACT -->
      <g id="section-contact" transform="translate(0, 920)">
        <g class="prompt" />
        <g class="contact-list" />
      </g>

      <!-- FOOTER -->
      <g id="footer" transform="translate(0, 1080)">
        <line class="divider" />
        <text class="meta-info" />
        <rect class="blinking-cursor" />
      </g>

    </g>
  </g>
</svg>
```
